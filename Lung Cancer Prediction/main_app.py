import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, roc_curve, auc
from sklearn.feature_selection import SelectKBest, f_classif
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib

# Set page configuration
st.set_page_config(
    page_title="Lung Cancer Prediction App",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1f77b4; text-align: center; margin-bottom: 30px;}
    .sub-header {font-size: 1.8rem; color: #1f77b4; border-bottom: 2px solid #1f77b4; padding-bottom: 5px;}
    .info-text {font-size: 1.1rem; line-height: 1.6;}
    .prediction-high {background-color: #fccc; padding: 20px; border-radius: 10px; border: 1px solid #ff0000;}
    .prediction-medium {background-color: #fff4; padding: 20px; border-radius: 10px; border: 1px solid #ffcc00;}
    .prediction-low {background-color: #ccffcc; padding: 20px; border-radius: 10px; border: 1px solid #00ff00;}
    .feature-importance {background-color: #f0f; padding: 15px; border-radius: 10px;}
    .stButton>button {background-color: #4CAF; color: white; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<p class="main-header"><h1>🫁 Lung Cancer Prediction App</h1></p>', unsafe_allow_html=True)
st.markdown("""
<p class="info-text">
This application predicts the likelihood of lung cancer based on patient health data and lifestyle factors.
Upload a CSV file with patient data or use the input form to make predictions.
</p>
""", unsafe_allow_html=True)

st.sidebar.header("Made By Subhadip 😎")
# Load and preprocess data
@st.cache_data
def load_data():
    # For demo purposes, we'll create a more realistic dataset
    np.random.seed(42)
    n_samples = 1000
    
    # Create synthetic data with meaningful relationships
    data = {
        'Age': np.random.normal(60, 12, n_samples).astype(int),
        'Gender': np.random.choice(['Male', 'Female'], n_samples, p=[0.6, 0.4]),
        'Air Pollution': np.random.randint(1, 9, n_samples),
        'Alcohol use': np.random.randint(1, 9, n_samples),
        'Dust Allergy': np.random.randint(1, 9, n_samples),
        'OccuPational Hazards': np.random.randint(1, 9, n_samples),
        'Genetic Risk': np.random.randint(1, 9, n_samples),
        'chronic Lung Disease': np.random.randint(1, 9, n_samples),
        'Balanced Diet': np.random.randint(1, 9, n_samples),
        'Obesity': np.random.randint(1, 9, n_samples),
        'Smoking': np.random.randint(1, 9, n_samples),
        'Passive Smoker': np.random.randint(1, 9, n_samples),
        'Chest Pain': np.random.randint(1, 9, n_samples),
        'Coughing of Blood': np.random.randint(1, 9, n_samples),
        'Fatigue': np.random.randint(1, 9, n_samples),
        'Weight Loss': np.random.randint(1, 9, n_samples),
        'Shortness of Breath': np.random.randint(1, 9, n_samples),
        'Wheezing': np.random.randint(1, 9, n_samples),
        'Swallowing Difficulty': np.random.randint(1, 9, n_samples),
        'Clubbing of Finger Nails': np.random.randint(1, 9, n_samples),
        'Frequent Cold': np.random.randint(1, 9, n_samples),
        'Dry Cough': np.random.randint(1, 9, n_samples),
        'Snoring': np.random.randint(1, 9, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create a more realistic target variable with meaningful relationships
    # High risk factors: Smoking, Genetic Risk, Air Pollution, Age, Coughing of Blood
    risk_score = (
        df['Smoking'] * 0.3 + 
        df['Genetic Risk'] * 0.25 + 
        df['Air Pollution'] * 0.15 +
        df['Coughing of Blood'] * 0.2 +
        (df['Age'] > 60) * 2 +
        np.random.normal(0, 1, n_samples)
    )
    
    # Convert to categories
    df['Level'] = pd.cut(risk_score, 
                         bins=[-10, 2, 4, 10], 
                         labels=['Low', 'Medium', 'High'])
    
    return df

# Function to preprocess data
def preprocess_data(df, target='Level'):
    df = df.copy()
    
    # Drop unnecessary columns if they exist
    cols_to_drop = ["index", "Patient Id"]
    for col in cols_to_drop:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
    
    # Encode categorical variables
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if col != target:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
    
    # Encode target variable
    if target in df.columns:
        le_target = LabelEncoder()
        df[target] = le_target.fit_transform(df[target])
        target_mapping = {i: label for i, label in enumerate(le_target.classes_)}
    else:
        le_target = None
        target_mapping = None
    
    return df, le_target, target_mapping

# Function for feature selection
def select_features(X, y, k=10):
    selector = SelectKBest(score_func=f_classif, k=min(k, X.shape[1]))
    selector.fit(X, y)
    selected_features = X.columns[selector.get_support()]
    return selected_features, selector.scores_

# Function to train model with hyperparameter tuning
def train_model(X, y, model_type='random_forest'):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    if model_type == 'random_forest':
        # Hyperparameter tuning for Random Forest
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }
        model = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X_train_scaled, y_train)
        best_model = grid_search.best_estimator_
        
    elif model_type == 'gradient_boosting':
        # Hyperparameter tuning for Gradient Boosting
        param_grid = {
            'n_estimators': [100, 200],
            'learning_rate': [0.05, 0.1],
            'max_depth': [3, 5],
            'subsample': [0.8, 1.0]
        }
        model = GradientBoostingClassifier(random_state=42)
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X_train_scaled, y_train)
        best_model = grid_search.best_estimator_
        
    elif model_type == 'svm':
        # Hyperparameter tuning for SVM
        param_grid = {
            'C': [0.1, 1, 10],
            'gamma': ['scale', 'auto'],
            'kernel': ['rbf', 'linear']
        }
        model = SVC(probability=True, random_state=42)
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X_train_scaled, y_train)
        best_model = grid_search.best_estimator_
    
    # Evaluate model
    y_pred = best_model.predict(X_test_scaled)
    y_pred_proba = best_model.predict_proba(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    return best_model, accuracy, cm, scaler, X_train.columns

# Main app
def main():
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose a page", 
                                   ["Home", "Data Overview", "Feature Selection", "Model Training", "Prediction"])
    
    # Load data
    df = load_data()
    
    if app_mode == "Home":
        st.markdown('<p class="sub-header">About This App</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="info-text">
        This application uses machine learning models to predict the risk level of lung cancer 
        based on various health and lifestyle factors. The model is trained on patient data including:
        </p>
        <ul class="info-text">
            <li>Demographic information (Age, Gender)</li>
            <li>Environmental factors (Air Pollution, Dust Allergy, Occupational Hazards)</li>
            <li>Lifestyle factors (Alcohol use, Smoking, Balanced Diet, Obesity)</li>
            <li>Genetic risk factors</li>
            <li>Health symptoms (Chest Pain, Coughing of Blood, Shortness of Breath, etc.)</li>
        </ul>
        <p class="info-text">
        Use the navigation menu to explore the data, select important features, train the model, and make predictions.
        </p>
        """, unsafe_allow_html=True)
        
        # Show sample data
        if st.checkbox("Show sample data"):
            st.dataframe(df.head())
    
    elif app_mode == "Data Overview":
        st.markdown('<p class="sub-header">Data Overview</p>', unsafe_allow_html=True)
        
        # Data preview
        st.write("### Dataset Preview")
        st.dataframe(df.head())
        
        # Basic statistics
        st.write("### Basic Statistics")
        st.write(df.describe())
        
        # Data visualization
        st.write("### Data Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            fig = px.histogram(df, x='Age', title='Age Distribution', nbins=20)
            st.plotly_chart(fig, use_container_width=True)
            
            # Gender distribution
            gender_counts = df['Gender'].value_counts()
            fig = px.pie(values=gender_counts.values, names=gender_counts.index, title='Gender Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk level distribution
            if 'Level' in df.columns:
                level_counts = df['Level'].value_counts()
                fig = px.bar(x=level_counts.index, y=level_counts.values, 
                            title='Risk Level Distribution', labels={'x': 'Risk Level', 'y': 'Count'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Correlation heatmap
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                corr = numeric_df.corr()
                fig = px.imshow(corr, title='Correlation Heatmap')
                st.plotly_chart(fig, use_container_width=True)
    
    elif app_mode == "Feature Selection":
        st.markdown('<p class="sub-header">Feature Selection</p>', unsafe_allow_html=True)
        
        # Preprocess data
        processed_df, le_target, target_mapping = preprocess_data(df)
        
        if 'Level' in processed_df.columns:
            X = processed_df.drop('Level', axis=1)
            y = processed_df['Level']
            
            # Feature selection
            k = st.slider("Number of features to select", 5, 20, 10)
            selected_features, feature_scores = select_features(X, y, k=k)
            
            st.write(f"### Top {k} Selected Features")
            
            # Create feature importance dataframe
            feature_importance_df = pd.DataFrame({
                'Feature': X.columns,
                'Importance Score': feature_scores
            }).sort_values('Importance Score', ascending=False)
            
            # Display top features
            st.dataframe(feature_importance_df.head(k))
            
            # Plot feature importance
            fig = px.bar(feature_importance_df.head(k), x='Importance Score', y='Feature', 
                        title='Feature Importance Scores', orientation='h')
            st.plotly_chart(fig, use_container_width=True)
            
            # Save selected features to session state
            st.session_state.selected_features = selected_features
            st.session_state.X = X[selected_features]
            st.session_state.y = y
            
        else:
            st.error("Target variable 'Level' not found in the dataset.")
    
    elif app_mode == "Model Training":
        st.markdown('<p class="sub-header">Model Training</p>', unsafe_allow_html=True)
        
        if 'selected_features' not in st.session_state:
            st.warning("Please perform feature selection first in the 'Feature Selection' section.")
            return
        
        X = st.session_state.X
        y = st.session_state.y
        
        # Model selection
        model_type = st.selectbox("Select Model", 
                                 ["random_forest", "gradient_boosting", "svm"])
        
        # Train model
        if st.button("Train Model"):
            with st.spinner("Training model (this may take a few minutes)..."):
                model, accuracy, cm, scaler, feature_names = train_model(X, y, model_type=model_type)
            
            st.success(f"Model trained successfully with accuracy: {accuracy:.2%}")
            
            # Display confusion matrix
            st.write("### Confusion Matrix")
            fig = px.imshow(cm, text_auto=True, 
                           labels=dict(x="Predicted", y="Actual", color="Count"),
                           x=['Low', 'Medium', 'High'], y=['Low', 'Medium', 'High'])
            st.plotly_chart(fig, use_container_width=True)
            
            # Feature importance for tree-based models
            if hasattr(model, 'feature_importances_'):
                st.write("### Feature Importance")
                feature_importance = pd.DataFrame({
                    'feature': feature_names,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                fig = px.bar(feature_importance, x='importance', y='feature', 
                            title='Feature Importance', orientation='h')
                st.plotly_chart(fig, use_container_width=True)
            
            # Save model to session state
            st.session_state.model = model
            st.session_state.scaler = scaler
            st.session_state.feature_names = feature_names
            
            # Show classification report
            st.write("### Classification Report")
            X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2, stratify=y)
            X_test_scaled = scaler.transform(X_test)
            y_pred = model.predict(X_test_scaled)
            
            report = classification_report(y_test, y_pred, target_names=['Low', 'Medium', 'High'], output_dict=True)
            report_df = pd.DataFrame(report).transpose()
            st.dataframe(report_df)
    
    elif app_mode == "Prediction":
        st.markdown('<p class="sub-header">Make Predictions</p>', unsafe_allow_html=True)
        
        # Check if model is trained
        if 'model' not in st.session_state:
            st.warning("Please train the model first in the 'Model Training' section.")
            return
        
        # Create input form with only selected features
        st.write("### Enter Patient Information")
        
        # Get selected features
        selected_features = st.session_state.get('selected_features', [])
        
        # Organize inputs into columns
        col1, col2, col3 = st.columns(3)
        input_data = {}
        
        # Age and Gender are always included
        with col1:
            input_data['Age'] = st.slider("Age", 20, 80, 50)
            input_data['Gender'] = st.selectbox("Gender", ["Male", "Female"])
            
        with col2:
            if 'Air Pollution' in selected_features:
                input_data['Air Pollution'] = st.slider("Air Pollution (1-8)", 1, 8, 4)
            if 'Alcohol use' in selected_features:
                input_data['Alcohol use'] = st.slider("Alcohol Use (1-8)", 1, 8, 4)
            if 'Smoking' in selected_features:
                input_data['Smoking'] = st.slider("Smoking (1-8)", 1, 8, 4)
                
        with col3:
            if 'Genetic Risk' in selected_features:
                input_data['Genetic Risk'] = st.slider("Genetic Risk (1-8)", 1, 8, 4)
            if 'Coughing of Blood' in selected_features:
                input_data['Coughing of Blood'] = st.slider("Coughing of Blood (1-8)", 1, 8, 4)
            if 'chronic Lung Disease' in selected_features:
                input_data['chronic Lung Disease'] = st.slider("Chronic Lung Disease (1-8)", 1, 8, 4)
        
        # Additional inputs for other features
        if len(selected_features) > 7:
            st.write("### Additional Factors")
            col4, col5, col6 = st.columns(3)
            
            with col4:
                if 'Dust Allergy' in selected_features:
                    input_data['Dust Allergy'] = st.slider("Dust Allergy (1-8)", 1, 8, 4)
                if 'OccuPational Hazards' in selected_features:
                    input_data['OccuPational Hazards'] = st.slider("Occupational Hazards (1-8)", 1, 8, 4)
                    
            with col5:
                if 'Balanced Diet' in selected_features:
                    input_data['Balanced Diet'] = st.slider("Balanced Diet (1-8)", 1, 8, 4)
                if 'Obesity' in selected_features:
                    input_data['Obesity'] = st.slider("Obesity (1-8)", 1, 8, 4)
                    
            with col6:
                if 'Passive Smoker' in selected_features:
                    input_data['Passive Smoker'] = st.slider("Passive Smoker (1-8)", 1, 8, 4)
                if 'Chest Pain' in selected_features:
                    input_data['Chest Pain'] = st.slider("Chest Pain (1-8)", 1, 8, 4)
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Encode categorical variables
        if 'Gender' in input_df.columns:
            input_df['Gender'] = LabelEncoder().fit_transform(input_df['Gender'])
        
        # Ensure we have all the selected features
        for feature in selected_features:
            if feature not in input_df.columns:
                input_df[feature] = 4  # Default value
        
        # Reorder columns to match training data
        input_df = input_df[selected_features]
        
        # Make prediction
        if st.button("Predict Risk Level"):
            model = st.session_state.model
            scaler = st.session_state.scaler
            
            # Scale input data
            input_scaled = scaler.transform(input_df)
            
            prediction = model.predict(input_scaled)
            prediction_proba = model.predict_proba(input_scaled)
            
            risk_levels = ['Low', 'Medium', 'High']
            risk_level = risk_levels[prediction[0]]
            confidence = np.max(prediction_proba) * 100
            
            st.markdown("### Prediction Result")
            
            if risk_level == "High":
                st.markdown(f'<div class="prediction-high">'
                           f'<h3>High Risk of Lung Cancer</h3>'
                           f'<p>Confidence: {confidence:.2f}%</p>'
                           f'<p>Please consult a healthcare professional for further evaluation.</p>'
                           f'</div>', unsafe_allow_html=True)
            elif risk_level == "Medium":
                st.markdown(f'<div class="prediction-medium">'
                           f'<h3>Medium Risk of Lung Cancer</h3>'
                           f'<p>Confidence: {confidence:.2f}%</p>'
                           f'<p>Consider lifestyle changes and regular health check-ups.</p>'
                           f'</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="prediction-low">'
                           f'<h3>Low Risk of Lung Cancer</h3>'
                           f'<p>Confidence: {confidence:.2f}%</p>'
                           f'<p>Continue maintaining healthy habits and regular check-ups.</p>'
                           f'</div>', unsafe_allow_html=True)
            
            # Show probability distribution
            st.write("### Risk Probability Distribution")
            prob_df = pd.DataFrame({
                'Risk Level': risk_levels,
                'Probability': prediction_proba[0] * 100
            })
            
            fig = px.bar(prob_df, x='Risk Level', y='Probability', 
                        title='Probability for Each Risk Level', text='Probability')
            fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
            # Show contributing factors
            st.write("### Top Contributing Factors")
            if hasattr(model, 'feature_importances_'):
                # For tree-based models
                feature_importance = pd.DataFrame({
                    'Feature': selected_features,
                    'Importance': model.feature_importances_
                }).sort_values('Importance', ascending=False)
                
                # Get values for top features
                top_features = feature_importance.head(5)
                top_features['Value'] = top_features['Feature'].apply(lambda x: input_data.get(x, 'N/A'))
                
                st.table(top_features[['Feature', 'Value', 'Importance']])
            else:
                # For linear models like SVM
                st.info("Feature importance is not available for the selected model type.")

if __name__ == "__main__":
    main()