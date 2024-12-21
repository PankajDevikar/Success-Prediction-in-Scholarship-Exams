from setuptools import setup, find_packages

setup(
    name="scholarship-prediction",
    version="0.1",
    author="Minal Madankar Devikar",
    author_email="meenal.madankar@gmail.com", 
    description="A Streamlit app for predicting scholarship status based on features.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/minalmmm/Success-Prediction-in-Scholarship-Exams.git", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "streamlit==1.17.0",
        "pandas==1.5.3",
        "numpy==1.24.1",
        "scikit-learn==1.2.0",
        "pickle-mixin==1.0.2",
    ],
    python_requires='>=3.12.0',  
)
