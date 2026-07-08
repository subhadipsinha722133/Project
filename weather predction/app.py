import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.utils import resample
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
from io import StringIO
import os

# Set page configuration
st.set_page_config(
    page_title="Rainfall Prediction App",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🌧️ Rainfall Prediction Analysis")
st.markdown("""
This application predicts rainfall based on meteorological data using a Random Forest Classifier.
Using the built-in Rainfall.csv dataset.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a page:", 
                          ["Data Overview", "Data Analysis", "Model Training", "Prediction"])

# Load data function
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("Rainfall.csv")
        return data
    except FileNotFoundError:
        st.error("Error: Rainfall.csv file not found. Please make sure the file exists in the same directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# Main data processing function
def process_data(data):
    # Remove extra spaces in all columns
    data.columns = data.columns.str.strip()
    
    # Remove day column if it exists
    if "day" in data.columns:
        data = data.drop(columns=["day"])
    
    # Handle missing values
    if "winddirection" in data.columns:
        data["winddirection"] = data["winddirection"].fillna(data["winddirection"].mode()[0])
    if "windspeed" in data.columns:
        data["windspeed"] = data["windspeed"].fillna(data["windspeed"].median())
    
    # Convert rainfall to binary
    if "rainfall" in data.columns:
        data["rainfall"] = data["rainfall"].map({"yes": 1, "no": 0})
    
    return data

# Load and process data
data = load_data()
data = process_data(data)

# Store data in session state
st.session_state.data = data

# Display different pages based on selection
if options == "Data Overview":
    st.header("📊 Data Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Preview")
        st.dataframe(data.head())
    
    with col2:
        st.subheader("Dataset Information")
        # Use StringIO instead of BytesIO for text data
        buffer = StringIO()
        data.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
    
    st.subheader("Statistical Summary")
    st.dataframe(data.describe())
    
    st.subheader("Missing Values")
    missing_df = pd.DataFrame({
        'Column': data.columns,
        'Missing Values': data.isnull().sum(),
        'Percentage': (data.isnull().sum() / len(data)) * 100
    })
    st.dataframe(missing_df)

elif options == "Data Analysis":
    st.header("📈 Data Analysis")
    
    # Distribution plots
    st.subheader("Feature Distributions")
    numerical_cols = ['pressure', 'maxtemp', 'temparature', 'mintemp', 'dewpoint', 
                     'humidity', 'cloud', 'sunshine', 'windspeed']
    numerical_cols = [col for col in numerical_cols if col in data.columns]
    
    if numerical_cols:
        cols_per_row = 3
        rows = (len(numerical_cols) + cols_per_row - 1) // cols_per_row
        
        for i in range(rows):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                idx = i * cols_per_row + j
                if idx < len(numerical_cols):
                    col = numerical_cols[idx]
                    fig, ax = plt.subplots(figsize=(4, 3))
                    sns.histplot(data[col], kde=True, ax=ax)
                    ax.set_title(f"Distribution of {col}")
                    cols[j].pyplot(fig)
                    plt.close(fig)
    
    # Rainfall distribution
    if "rainfall" in data.columns:
        st.subheader("Rainfall Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(x=data["rainfall"], ax=ax)
        ax.set_title("Distribution of Rainfall")
        st.pyplot(fig)
    
    # Correlation matrix
    st.subheader("Correlation Matrix")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(data.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)
    
    # Boxplots for outlier detection
    st.subheader("Outlier Detection (Boxplots)")
    if numerical_cols:
        cols_per_row = 3
        rows = (len(numerical_cols) + cols_per_row - 1) // cols_per_row
        
        for i in range(rows):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                idx = i * cols_per_row + j
                if idx < len(numerical_cols):
                    col = numerical_cols[idx]
                    fig, ax = plt.subplots(figsize=(4, 3))
                    sns.boxplot(data[col], ax=ax)
                    ax.set_title(f"Boxplot of {col}")
                    cols[j].pyplot(fig)
                    plt.close(fig)

elif options == "Model Training":
    st.header("🤖 Model Training")
    
    if "rainfall" not in data.columns:
        st.error("Target variable 'rainfall' not found in the dataset!")
        st.stop()
    
    # Data preprocessing options
    st.subheader("Data Preprocessing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        remove_correlated = st.checkbox("Remove highly correlated features", value=True)
        downsample = st.checkbox("Balance classes using downsampling", value=True)
    
    with col2:
        test_size = st.slider("Test set size (%)", 10, 40, 20)
        random_state = st.number_input("Random state", value=42)
    
    # Process data based on user choices
    processed_data = data.copy()
    
    if remove_correlated:
        columns_to_remove = ['maxtemp', 'temparature', 'mintemp']
        columns_to_remove = [col for col in columns_to_remove if col in processed_data.columns]
        processed_data = processed_data.drop(columns=columns_to_remove)
        st.info(f"Removed columns: {columns_to_remove}")
    
    # Separate features and target
    X = processed_data.drop(columns=["rainfall"])
    y = processed_data["rainfall"]
    
    if downsample:
        st.subheader("Class Balance Before Downsampling")
        st.write(y.value_counts())
        
        # Downsample majority class
        df_majority = processed_data[processed_data["rainfall"] == 1]
        df_minority = processed_data[processed_data["rainfall"] == 0]
        
        if len(df_majority) > 0 and len(df_minority) > 0:
            df_majority_downsampled = resample(
                df_majority, 
                replace=False, 
                n_samples=len(df_minority), 
                random_state=random_state
            )
            df_downsampled = pd.concat([df_majority_downsampled, df_minority])
            df_downsampled = df_downsampled.sample(frac=1, random_state=random_state).reset_index(drop=True)
            
            X = df_downsampled.drop(columns=["rainfall"])
            y = df_downsampled["rainfall"]
            
            st.subheader("Class Balance After Downsampling")
            st.write(y.value_counts())
        else:
            st.warning("Cannot perform downsampling - check class distribution")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size/100, random_state=random_state
    )
    
    st.subheader("Data Split Information")
    col1, col2, col3 = st.columns(3)
    col1.metric("Training samples", len(X_train))
    col2.metric("Test samples", len(X_test))
    col3.metric("Total features", X_train.shape[1])
    
    # Model training
    st.subheader("Model Training Parameters")
    
    param_options = st.radio("Parameter selection:", 
                           ["Use default parameters", "Use optimized parameters", "Custom parameters"])
    
    if st.button("Train Model", type="primary"):
        with st.spinner("Training model... This may take a few minutes."):
            if param_options == "Use default parameters":
                rf_model = RandomForestClassifier(random_state=random_state)
                rf_model.fit(X_train, y_train)
                
            elif param_options == "Use optimized parameters":
                # Use the parameters from your original code
                param_grid_rf = {
                    "n_estimators": [50, 100, 200],
                    "max_features": ["sqrt", "log2"],
                    "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4]
                }
                
                grid_search_rf = GridSearchCV(
                    estimator=RandomForestClassifier(random_state=random_state),
                    param_grid=param_grid_rf,
                    cv=5,
                    n_jobs=-1,
                    verbose=0
                )
                
                grid_search_rf.fit(X_train, y_train)
                rf_model = grid_search_rf.best_estimator_
                
                st.success(f"Best parameters: {grid_search_rf.best_params_}")
            
            else:  # Custom parameters
                col1, col2 = st.columns(2)
                with col1:
                    n_estimators = st.slider("n_estimators", 10, 500, 100)
                    max_depth = st.slider("max_depth", 1, 50, 10)
                with col2:
                    min_samples_split = st.slider("min_samples_split", 2, 20, 2)
                    min_samples_leaf = st.slider("min_samples_leaf", 1, 10, 1)
                
                rf_model = RandomForestClassifier(
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    min_samples_split=min_samples_split,
                    min_samples_leaf=min_samples_leaf,
                    random_state=random_state
                )
                rf_model.fit(X_train, y_train)
            
            # Cross-validation
            cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5)
            
            # Predictions
            y_pred = rf_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Store model in session state
            st.session_state.model = rf_model
            st.session_state.X_test = X_test
            st.session_state.y_test = y_test
            st.session_state.y_pred = y_pred
            st.session_state.feature_names = X.columns.tolist()
            
            # Display results
            st.subheader("Model Performance")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Test Accuracy", f"{accuracy:.3f}")
            col2.metric("Mean CV Score", f"{np.mean(cv_scores):.3f}")
            col3.metric("CV Std Dev", f"{np.std(cv_scores):.3f}")
            
            st.subheader("Confusion Matrix")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', ax=ax)
            ax.set_xlabel('Predicted')
            ax.set_ylabel('Actual')
            st.pyplot(fig)
            
            st.subheader("Classification Report")
            report = classification_report(y_test, y_pred, output_dict=True)
            st.dataframe(pd.DataFrame(report).transpose())
            
            # Feature importance
            st.subheader("Feature Importance")
            feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': rf_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='importance', y='feature', data=feature_importance, ax=ax)
            ax.set_title('Feature Importance')
            st.pyplot(fig)
            
            # Download model
            model_bytes = pickle.dumps(rf_model)
            st.download_button(
                label="Download Trained Model",
                data=model_bytes,
                file_name="rainfall_model.pkl",
                mime="application/octet-stream"
            )

elif options == "Prediction":
    st.header("🔮 Make Predictions")
    
    if "model" not in st.session_state:
        st.warning("Please train the model first in the 'Model Training' section.")
        st.stop()
    
    model = st.session_state.model
    
    # Get feature names from session state or model
    if hasattr(st.session_state, 'feature_names'):
        feature_names = st.session_state.feature_names
    else:
        feature_names = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else []
    
    if not feature_names:
        st.error("Feature names not available. Please retrain the model.")
        st.stop()
    
    st.subheader("Input Features for Prediction")
    
    # Create input fields for each feature
    input_data = {}
    cols = st.columns(2)
    
    for i, feature in enumerate(feature_names):
        col = cols[i % 2]
        if data[feature].dtype in ['int64', 'float64']:
            min_val = float(data[feature].min())
            max_val = float(data[feature].max())
            default_val = float(data[feature].median())
            input_data[feature] = col.number_input(
                f"{feature}", min_value=min_val, max_value=max_val, value=default_val
            )
        else:
            input_data[feature] = col.selectbox(
                f"{feature}", options=data[feature].unique()
            )
    
    if st.button("Predict Rainfall", type="primary"):
        # Prepare input data
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        # Display results
        st.subheader("Prediction Results")
        
        col1, col2 = st.columns(2)
        col1.metric("Prediction", "Rain 🌧️" if prediction == 1 else "No Rain ☀️")
        col2.metric("Confidence", f"{max(probability)*100:.1f}%")
        
        st.subheader("Probability Distribution")
        fig, ax = plt.subplots(figsize=(8, 4))
        labels = ['No Rain', 'Rain']
        colors = ['#ff9999', '#66b3ff']
        ax.pie(probability, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**Note:** This application uses Random Forest Classifier for rainfall prediction. 
Using data from Rainfall.csv.
""")

# Display file info in sidebar
st.sidebar.markdown("### Dataset Info")
st.sidebar.write(f"**Rows:** {len(data)}")
st.sidebar.write(f"**Columns:** {len(data.columns)}")
st.sidebar.write(f"**Features:** {', '.join(data.columns)}")