import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# Set page config
st.set_page_config(
    page_title="Heart Disease Prediction App",
    page_icon="❤️",
    layout="wide"
)

# Load and preprocess data
@st.cache_data
def load_data():
    try:
        heart_data = pd.read_csv('heart_disease_data.csv')
        return heart_data
    except FileNotFoundError:
        st.error("File 'heart_disease_data.csv' not found. Please make sure the file is in the same directory.")
        return None

def preprocess_data(data):
    # Handle missing values if any
    data = data.dropna()
    
    # Separate features and target
    X = data.drop(columns='target', axis=1)
    Y = data['target']
    
    return X, Y

# Train models
def train_models(X_train, X_test, Y_train, Y_test, selected_models):
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
        'XGBoost': XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss'),
        'SVM': SVC(random_state=42, probability=True),
        'K-Nearest Neighbors': KNeighborsClassifier()
    }
    
    results = {}
    
    for model_name in selected_models:
        model = models[model_name]
        model.fit(X_train, Y_train)
        
        # Predictions
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        # Probabilities
        train_proba = model.predict_proba(X_train)[:, 1]
        test_proba = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        train_accuracy = accuracy_score(Y_train, train_pred)
        test_accuracy = accuracy_score(Y_test, test_pred)
        
        results[model_name] = {
            'model': model,
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'train_pred': train_pred,
            'test_pred': test_pred,
            'train_proba': train_proba,
            'test_proba': test_proba
        }
    
    return results
st.sidebar.header("Made By Subhadip 🔥")
# Main app
def main():
    st.title("❤️ Heart Disease Prediction App")
    st.write("Predict the likelihood of heart disease using machine learning algorithms")
    
    # Load data
    heart_data = load_data()
    if heart_data is None:
        return
    
    # Sidebar
    st.sidebar.header("Dataset Information")
    st.sidebar.write(f"Total samples: {len(heart_data)}")
    st.sidebar.write(f"Number of features: {len(heart_data.columns) - 1}")
    st.sidebar.write(f"Target distribution:\n{heart_data['target'].value_counts()}")
    
    # Show data
    if st.sidebar.checkbox("Show raw data"):
        st.subheader("Raw Data")
        st.dataframe(heart_data.head())
    
    # Preprocess data
    X, Y = preprocess_data(heart_data)
    
    # Model selection
    st.sidebar.header("Model Selection")
    model_options = ['Logistic Regression', 'Random Forest', 'XGBoost', 'SVM', 'K-Nearest Neighbors']
    selected_models = st.sidebar.multiselect(
        "Choose models to train:",
        model_options,
        default=['Logistic Regression', 'Random Forest', 'XGBoost']
    )
    
    # Test size slider
    test_size = st.sidebar.slider("Test set size:", 0.1, 0.4, 0.2, 0.05)
    
    # Train-test split
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=test_size, stratify=Y, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    if selected_models:
        # Train models
        results = train_models(X_train_scaled, X_test_scaled, Y_train, Y_test, selected_models)
        
        # Display results
        st.header("Model Performance")
        
        # Create columns for metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Training Accuracy")
            train_accuracies = {name: result['train_accuracy'] for name, result in results.items()}
            st.bar_chart(train_accuracies)
        
        with col2:
            st.subheader("Test Accuracy")
            test_accuracies = {name: result['test_accuracy'] for name, result in results.items()}
            st.bar_chart(test_accuracies)
        
        # Detailed metrics
        st.subheader("Detailed Metrics")
        for model_name, result in results.items():
            with st.expander(f"{model_name} Details"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Training Accuracy:** {result['train_accuracy']:.4f}")
                    st.write(f"**Test Accuracy:** {result['test_accuracy']:.4f}")
                
                with col2:
                    st.write("**Classification Report:**")
                    st.text(classification_report(Y_test, result['test_pred']))
        
        # Best model selection
        best_model_name = max(results.items(), key=lambda x: x[1]['test_accuracy'])[0]
        best_model = results[best_model_name]['model']
        
        st.success(f"🎯 Best performing model: {best_model_name} (Test Accuracy: {results[best_model_name]['test_accuracy']:.4f})")
        
        # Prediction section
        st.header("🔮 Make a Prediction")
        
        # Create input form
        with st.form("prediction_form"):
            st.write("Enter patient details:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                age = st.number_input("Age", min_value=0, max_value=120, value=50)
                sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
                cp = st.selectbox("Chest Pain Type", options=[0, 1, 2, 3], 
                                 format_func=lambda x: ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"][x])
                trestbps = st.number_input("Resting Blood Pressure", min_value=0, max_value=200, value=120)
            
            with col2:
                chol = st.number_input("Cholesterol", min_value=0, max_value=600, value=200)
                fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1], 
                                  format_func=lambda x: "No" if x == 0 else "Yes")
                restecg = st.selectbox("Resting ECG", options=[0, 1, 2], 
                                      format_func=lambda x: ["Normal", "ST-T wave abnormality", "Left ventricular hypertrophy"][x])
                thalach = st.number_input("Maximum Heart Rate", min_value=0, max_value=220, value=150)
            
            with col3:
                exang = st.selectbox("Exercise Induced Angina", options=[0, 1], 
                                    format_func=lambda x: "No" if x == 0 else "Yes")
                oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
                slope = st.selectbox("Slope of Peak Exercise ST", options=[0, 1, 2], 
                                    format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x])
                ca = st.slider("Number of Major Vessels", min_value=0, max_value=4, value=0)
                thal = st.selectbox("Thalassemia", options=[0, 1, 2, 3], 
                                   format_func=lambda x: ["Normal", "Fixed defect", "Reversible defect", "Unknown"][x])
            
            submitted = st.form_submit_button("Predict")
            
            if submitted:
                # Create input array
                input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
                input_scaled = scaler.transform(input_data)
                
                # Make prediction
                prediction = best_model.predict(input_scaled)
                probability = best_model.predict_proba(input_scaled)[0][1]
                
                # Display result
                if prediction[0] == 0:
                    st.success(f"✅ Low risk of heart disease (Probability: {probability:.2%})")
                else:
                    st.error(f"⚠️ High risk of heart disease (Probability: {probability:.2%})")
                
                # Show probability gauge
                st.subheader("Risk Probability")
                st.progress(float(probability))
                st.write(f"Probability of heart disease: {probability:.2%}")
    
    else:
        st.warning("Please select at least one model to train.")

if __name__ == "__main__":
    main()