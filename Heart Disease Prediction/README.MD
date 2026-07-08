## ❤️ Heart Disease Prediction App
A Streamlit web application that predicts the likelihood of heart disease using multiple machine learning algorithms. This interactive app allows healthcare professionals and researchers to input patient data and receive instant risk assessments with probability scores.

https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/Machine%2520Learning-FF6F00?style=for-the-badge&logo=scikitlearn&logoColor=white

# 📋 Features
Multiple ML Algorithms: Logistic Regression, Random Forest, XGBoost, SVM, and K-Nearest Neighbors

Interactive Interface: User-friendly form for inputting patient data

Model Comparison: Visual comparison of different algorithms' performance

Real-time Prediction: Instant risk assessment with probability scores

Data Visualization: Charts showing model accuracy and performance metrics

Best Model Selection: Automatically selects the best performing model for predictions

Responsive Design: Clean, organized layout with columns and expandable sections

# 🚀 Quick Start
Prerequisites
Python 3.7+

pip (Python package manager)

Installation
Clone the repository:

bash
git clone https://github.com/subhadipsinha722133/Heart-Disease-Prediction.git
cd heart-disease-prediction-app
Install the required dependencies:

bash
pip install -r requirements.txt
Place your heart_disease_data.csv file in the project directory

Run the application:

bash
streamlit run app.py
Open your web browser and navigate to http://localhost:8501

# 📁 Project Structure
text
heart-disease-prediction-app/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── heart_disease_data.csv # Dataset (not included in repo)
└── README.md             # Project documentation

# 🎯 Usage
Data Input: Fill in the patient details form with the required medical parameters:

Age, Sex, Chest Pain Type

Resting Blood Pressure, Cholesterol levels

Fasting Blood Sugar, Resting ECG results

Maximum Heart Rate, Exercise Induced Angina

ST Depression, Slope of Peak Exercise ST

Number of Major Vessels, Thalassemia

Model Selection: Choose which machine learning algorithms to compare from the sidebar

Prediction: Click the "Predict" button to get an instant risk assessment

Results: View the probability score and risk level (Low/High risk)

# 🔧 Configuration
The app allows you to customize:

Test set size (10-40% of data)

Selection of ML algorithms to compare

View raw dataset statistics

# 📊 Dataset
The application uses a CSV file with the following features:

Feature	Description	Values
age	Age in years	Numerical
sex	Gender	0 = Female, 1 = Male
cp	Chest pain type	0-3 (Typical angina, Atypical angina, Non-anginal pain, Asymptomatic)
trestbps	Resting blood pressure	Numerical (mm Hg)
chol	Serum cholesterol	Numerical (mg/dl)
fbs	Fasting blood sugar > 120 mg/dl	0 = No, 1 = Yes
restecg	Resting electrocardiographic results	0-2 (Normal, ST-T wave abnormality, Left ventricular hypertrophy)
thalach	Maximum heart rate achieved	Numerical
exang	Exercise induced angina	0 = No, 1 = Yes
oldpeak	ST depression induced by exercise	Numerical
slope	Slope of the peak exercise ST segment	0-2 (Upsloping, Flat, Downsloping)
ca	Number of major vessels colored by fluoroscopy	0-3
thal	Thalassemia	0-3 (Normal, Fixed defect, Reversible defect, Unknown)
target	Presence of heart disease	0 = No, 1 = Yes

# 🤖 Machine Learning Models
The app implements and compares five different algorithms:

Logistic Regression: Baseline classification model

Random Forest: Ensemble method with multiple decision trees

XGBoost: Optimized gradient boosting algorithm

SVM: Support Vector Machine with probability estimates

K-Nearest Neighbors: Instance-based learning algorithm

# 📈 Performance Metrics
The application provides detailed performance metrics for each model:

Training accuracy

Test accuracy

Classification reports

Confusion matrices (visualized)

# 🛠️ Technical Details
Framework: Streamlit for the web interface

Machine Learning: Scikit-learn and XGBoost

Data Visualization: Matplotlib and Seaborn

Data Processing: Pandas and NumPy

# 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

# 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check issues page.

# 📞 Support
If you have any questions or need help, please open an issue in the GitHub repository.

# ⚠️ Disclaimer
This application is for educational and research purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment.