import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Function to load the model
def load_model():
    try:
        model = joblib.load('model/scholarship_prediction_model.pkl')
        st.write("Model loaded successfully!")
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Function to preprocess the input data
def preprocess_data(input_data):
    label_encoder = LabelEncoder()

    # Encoding 'Gender' column
    if 'Gender' in input_data.columns:
        input_data['Gender'] = label_encoder.fit_transform(input_data['Gender'])
    
    # Encoding 'ParentalEducation' column
    if 'ParentalEducation' in input_data.columns:
        input_data['ParentalEducation'] = label_encoder.fit_transform(input_data['ParentalEducation'])
    
    # Encoding 'PreviousScholarship' column
    if 'PreviousScholarship' in input_data.columns:
        input_data['PreviousScholarship'] = label_encoder.fit_transform(input_data['PreviousScholarship'])
    
    # Convert 'AttendanceRate' from percentage to float
    if 'AttendanceRate' in input_data.columns:
        input_data['AttendanceRate'] = input_data['AttendanceRate'].str.replace('%', '').astype(float) / 100.0
    
    # Create 'AverageScore' column
    input_data['AverageScore'] = input_data[['PracticeExam1', 'PracticeExam2', 'PracticeExam3']].mean(axis=1)
    
    # Scaling numerical features
    numerical_cols = ['Age', 'PracticeExam1', 'PracticeExam2', 'PracticeExam3', 'AttendanceRate', 'AverageScore']
    scaler = StandardScaler()
    input_data[numerical_cols] = scaler.fit_transform(input_data[numerical_cols])
    
    return input_data

# Streamlit app layout
st.title("Scholarship Prediction App")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file is not None:
    try:
        # Load uploaded data
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:", df.head())

        # Define required columns
        required_columns = ['StudentID', 'Name', 'Age', 'Gender', 'PracticeExam1', 'PracticeExam2', 'PracticeExam3',
                            'AttendanceRate', 'ParentalEducation', 'PreviousScholarship']
        
        # Check for missing columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing columns in uploaded data: {', '.join(missing_columns)}")
        else:
            # Extract relevant features and preprocess the data
            features = df[required_columns]
            features_preprocessed = preprocess_data(features)

            # Load the model
            model = load_model()
            if model:
                # Drop columns not required by the model
                features_for_model = features_preprocessed.drop(columns=['StudentID', 'Name'])

                # Perform predictions
                predictions = model.predict(features_for_model)
                df['Predicted Scholarship Status'] = predictions

                # Display predictions
                st.write("Predictions:", df[['StudentID', 'Name', 'Predicted Scholarship Status']])
                st.write("Complete Data with Predictions:", df)
    except Exception as e:
        st.error(f"Error occurred: {e}")
