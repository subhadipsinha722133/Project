# 🫁 Lung Cancer Prediction Web App
A Streamlit-based web application that predicts lung cancer risk levels using machine learning. This app analyzes patient health data and lifestyle factors to provide risk assessments with visualizations and detailed insights.

https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white
https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white
https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white

# 📋 Table of Contents
Features

Demo

Installation

Usage

Project Structure

Model Details

Data Description

Contributing

License

# ✨ Features
Interactive Web Interface: User-friendly Streamlit app with intuitive navigation

Multiple Machine Learning Models: Support for Random Forest, Gradient Boosting, and SVM classifiers

Feature Selection: Automated identification of the most predictive features

Model Optimization: Hyperparameter tuning for improved accuracy

Data Visualization: Interactive charts and heatmaps for data exploration

Risk Prediction: Detailed probability distribution and contributing factors analysis

Responsive Design: Clean UI with customized styling

# 🎥 Demo
https://via.placeholder.com/800x400.png?text=Lung+Cancer+Prediction+App+Screenshot

You can access a live demo of the app at [Insert deployed app URL here].

# 🛠 Installation
Prerequisites
Python 3.7 or higher

pip (Python package manager)

Steps
Clone the repository:

bash
git clone https://github.com/your-username/lung-cancer-prediction-app.git
cd lung-cancer-prediction-app
Create a virtual environment (recommended):

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install required packages:

bash
pip install -r requirements.txt


# 🚀 Usage
Run the Streamlit app:

bash
streamlit run lung_cancer_app.py
Open your web browser and navigate to the local URL shown in the terminal (typically http://localhost:8501)

Use the sidebar to navigate through different sections:

Home: Overview of the application

Data Overview: Explore the dataset with visualizations

Feature Selection: Identify the most important predictive features

Model Training: Train and evaluate machine learning models

Prediction: Input patient data and get risk predictions

For prediction:

Navigate to the Prediction section

Adjust the sliders to match patient characteristics

Click "Predict Risk Level" to see results

# 📁 Project Structure
text
lung-cancer-prediction-app/
│
├── lung_cancer_app.py      # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── data/                  # Data directory (optional)
│   └── Lung Cancer Prediction.csv  # Sample dataset
└── assets/                # Additional assets (optional)
    └── images/            # Screenshots or logos
🤖 Model Details
The application uses several machine learning algorithms:

# Supported Models
Random Forest Classifier: Ensemble method with multiple decision trees

Gradient Boosting Classifier: Sequential building of trees to correct errors

Support Vector Machine (SVM): Finds optimal hyperplane for classification

# Model Optimization
Hyperparameter tuning using GridSearchCV

Feature scaling with StandardScaler

Feature selection using SelectKBest with ANOVA F-value

Stratified sampling to maintain class distribution

3 Performance Metrics
Accuracy score

Confusion matrix

Classification report (precision, recall, F1-score)

Feature importance visualization

# 📊 Data Description
The app uses synthetic data with the following features:

Demographic Information
Age: Patient age (20-80 years)

Gender: Male or Female

# Environmental Factors
Air Pollution: Exposure level (1-8)

Dust Allergy: Sensitivity level (1-8)

Occupational Hazards: Workplace exposure level (1-8)

# Lifestyle Factors
Alcohol Use: Consumption level (1-8)

Smoking: Smoking habit intensity (1-8)

Passive Smoker: Secondhand smoke exposure (1-8)

Balanced Diet: Dietary quality (1-8)

Obesity: Body mass index level (1-8)

Genetic & Health Factors
Genetic Risk: Family history level (1-8)

Chronic Lung Disease: Pre-existing condition severity (1-8)

# Symptoms
Chest Pain: Discomfort level (1-8)

Coughing of Blood: Hemoptysis severity (1-8)

Fatigue: Tiredness level (1-8)

Weight Loss: Unintended weight reduction (1-8)

Shortness of Breath: Dyspnea severity (1-8)

Wheezing: Breathing difficulty (1-8)

Swallowing Difficulty: Dysphagia level (1-8)

Clubbing of Finger Nails: Digital clubbing presence (1-8)

Frequent Cold: Susceptibility to colds (1-8)

Dry Cough: Non-productive cough severity (1-8)

Snoring: Sleep disturbance level (1-8)

Target Variable
Level: Risk classification (Low, Medium, High)

# 🤝 Contributing
We welcome contributions to improve this project! Here's how you can help:

Fork the repository

Create a feature branch: git checkout -b feature-name

Make your changes and test thoroughly

Commit your changes: git commit -m 'Add some feature'

Push to the branch: git push origin feature-name

Submit a pull request

# Areas for Improvement
Additional machine learning models

Enhanced data visualization

More comprehensive dataset

Deployment automation scripts

Multi-language support

Mobile-responsive design

# 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

# ⚠️ Disclaimer
This application is intended for educational and research purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with questions about medical conditions.

# 📞 Support
If you have any questions or issues, please:

Check the existing issues to see if your problem has already been reported

Create a new issue with a detailed description of the problem

Contact the maintainers at [sinhasubhadip34@gmail.com]

Note: For production use with real patient data, ensure compliance with healthcare data regulations such as HIPAA (Health Insurance Portability and Accountability Act) in the US or GDPR (General Data Protection Regulation) in the EU.