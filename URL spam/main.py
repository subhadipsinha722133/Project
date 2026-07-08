import streamlit as st
import pickle
import string
import re
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import urllib.parse
from urllib.parse import urlparse
import tldextract

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Set page config
st.set_page_config(
    page_title="URL Spam Classifier",
    page_icon="🌐",
    layout="wide"
)

# Initialize stemmer
ps = PorterStemmer()

def extract_url_features(url):
    """Extract meaningful features from URLs without destroying the content"""
    if not isinstance(url, str) or not url.strip():
        return ""
    
    try:
        # Parse URL
        parsed = urlparse(url)
        
        # Extract domain information
        extracted = tldextract.extract(url)
        domain = extracted.domain
        suffix = extracted.suffix
        
        # Get path components
        path = parsed.path
        path_components = [comp for comp in path.split('/') if comp and len(comp) > 2]
        
        # Get query parameters
        query = parsed.query
        query_params = []
        if query:
            for key, value in urllib.parse.parse_qsl(query):
                if value and len(value) > 2:
                    query_params.append(value)
        
        # Combine all meaningful parts
        meaningful_parts = []
        
        if domain and len(domain) > 2:
            meaningful_parts.append(domain)
        
        if path_components:
            meaningful_parts.extend(path_components)
        
        if query_params:
            meaningful_parts.extend(query_params)
        
        # If we have meaningful parts, join them
        if meaningful_parts:
            return " ".join(meaningful_parts)
        else:
            # Fallback: use the entire URL but clean it
            cleaned = re.sub(r'https?://|www\.|\.[a-z]{2,3}/?', '', url)
            cleaned = re.sub(r'[^a-zA-Z0-9]', ' ', cleaned)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            return cleaned if cleaned else "unknown_url"
            
    except:
        # If parsing fails, use a simple cleaning approach
        cleaned = re.sub(r'https?://|www\.|\.[a-z]{2,3}/?', '', url)
        cleaned = re.sub(r'[^a-zA-Z0-9]', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned if cleaned else "unknown_url"

def transform_text(text):
    """Light text processing for URL features"""
    if not isinstance(text, str) or not text.strip():
        return ""
    
    text = text.lower()
    
    # Tokenize
    tokens = nltk.word_tokenize(text)
    
    # Remove very short tokens and numbers
    tokens = [token for token in tokens if len(token) > 2 and not token.isdigit()]
    
    # Remove stopwords but be less aggressive
    custom_stopwords = set(['http', 'https', 'www', 'com', 'org', 'net', 'html'])
    tokens = [token for token in tokens if token not in custom_stopwords]
    
    # Apply stemming
    tokens = [ps.stem(token) for token in tokens]
    
    return " ".join(tokens)

def preprocess_data(df):
    """Preprocess the URL data with URL-specific techniques"""
    df = df.copy()
    
    # Handle missing values
    df = df.dropna()
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Limit dataset size if too large
    df = df.iloc[:35000] if len(df) > 35000 else df
    
    # Extract features from URLs
    df["cleaned_url"] = df["url"].apply(extract_url_features)
    df["cleaned_url"] = df["cleaned_url"].apply(transform_text)
    
    # Remove empty strings after preprocessing
    df = df[df["cleaned_url"].str.len() > 0]
    
    return df

# Load or train model
@st.cache_resource
def load_or_train_model():
    try:
        tfidf = pickle.load(open('url_spam_tfidf.pkl', 'rb'))
        model = pickle.load(open('url_spam_tfmodel.pkl', 'rb'))
        st.success("Pre-trained model loaded successfully!")
        return tfidf, model, None, None
    except:
        st.info("No pre-trained model found. You can train a new model in the 'Train Model' section.")
        return None, None, None, None

# Sample data creation function (for testing)
def create_sample_data():
    """Create sample data if no CSV file is found"""
    sample_urls = [
        "https://example.com/login",
        "http://facebook.com/profile",
        "https://google.com/search?q=python",
        "https://amazon.com/product/12345",
        "https://spam-site.com/free-gift",
        "http://bad-website.com/win-prize",
        "https://legit-site.com/about",
        "http://trusted-site.com/contact",
        "https://shopping-site.com/cart",
        "http://news-site.com/article"
    ]
    
    sample_is_spam = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
    
    return pd.DataFrame({
        "url": sample_urls,
        "is_spam": sample_is_spam
    })

# Main app
def main():
    st.title("🌐 URL Spam Classifier")
    st.write("Made By Subhadip 🔥")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose the app mode", 
                                   ["Predict URL", "View Dataset", "Train Model", "Model Performance"])
    
    # Load dataset
    try:
        df = pd.read_csv("url_spam_classification.csv")
        st.success("Dataset loaded successfully!")
    except:
        st.warning("Could not find 'url_spam_classification.csv'. Using sample data for demonstration.")
        df = create_sample_data()
    
    # Preprocess data
    df_processed = preprocess_data(df)
    
    if df_processed.empty:
        st.error("After preprocessing, no valid data remains. Using sample data instead.")
        df = create_sample_data()
        df_processed = preprocess_data(df)
    
    # Prepare features and labels
    X = df_processed["cleaned_url"]
    y = df_processed["is_spam"]
    
    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, random_state=42, test_size=0.2)
    
    # Load or initialize model
    tfidf, model, _, _ = load_or_train_model()
    
    if app_mode == "Predict URL":
        predict_url(tfidf, model)
    elif app_mode == "View Dataset":
        view_dataset(df, df_processed)
    elif app_mode == "Train Model":
        train_model(X_train, X_test, y_train, y_test)
    elif app_mode == "Model Performance":
        model_performance(X_train, X_test, y_train, y_test, df_processed)

def predict_url(tfidf, model):
    st.header("🔍 Predict if a URL is Spam")
    
    input_url = st.text_area("Enter the URL", height=100, placeholder="https://example.com")
    
    if st.button('Predict', type="primary"):
        if not input_url.strip():
            st.warning("Please enter a URL")
        else:
            with st.spinner("Analyzing URL..."):
                # Extract features from the URL
                transformed_url = extract_url_features(input_url)
                transformed_url = transform_text(transformed_url)
                
                if not transformed_url.strip():
                    st.error("Could not extract meaningful features from this URL.")
                    return
                
                # Vectorize and predict
                if tfidf and model:
                    try:
                        vector_input = tfidf.transform([transformed_url])
                        prediction = model.predict(vector_input)[0]
                        
                        
                        # Display results
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if prediction == 1:
                                st.error("🚫 Spam URL")
                            else:
                                st.success("✅ Not Spam URL")
                        
                       
                        
                     
                        # Show processed features
                        with st.expander("See extracted features"):
                            st.write(transformed_url)
                        
                        st.snow()
                    except Exception as e:
                        st.error(f"Error during prediction: {e}")
                else:
                    st.error("Model not available. Please train the model first.")

def view_dataset(df, df_processed):
    st.header("📊 Dataset Overview")
    
    st.subheader("Original Data")
    st.dataframe(df.head(100))
    
    st.subheader("Processed Data")
    st.dataframe(df_processed[["url", "cleaned_url", "is_spam"]].head(100))
    
    # Show dataset statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total URLs", len(df))
    
    with col2:
        spam_count = df["is_spam"].value_counts().get(1, 0)
        st.metric("Spam URLs", spam_count)
    
    with col3:
        legit_count = df["is_spam"].value_counts().get(0, 0)
        st.metric("Legitimate URLs", legit_count)
    
    # Show class distribution
    fig, ax = plt.subplots()
    df["is_spam"].value_counts().plot(kind='bar', ax=ax, color=['green', 'red'])
    ax.set_title('Class Distribution')
    ax.set_xticklabels(['Legitimate', 'Spam'], rotation=0)
    st.pyplot(fig)
    
    # Show word clouds if we have text data
    st.subheader("Word Clouds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Legitimate URLs")
        legit_text = " ".join(df_processed[df_processed["is_spam"] == 0]["cleaned_url"].dropna())
        if legit_text.strip():
            wordcloud = WordCloud(width=400, height=300, background_color='white').generate(legit_text)
            plt.figure(figsize=(10, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)
        else:
            st.info("No text data available for word cloud")
    
    with col2:
        st.write("Spam URLs")
        spam_text = " ".join(df_processed[df_processed["is_spam"] == 1]["cleaned_url"].dropna())
        if spam_text.strip():
            wordcloud = WordCloud(width=400, height=300, background_color='white').generate(spam_text)
            plt.figure(figsize=(10, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)
        else:
            st.info("No text data available for word cloud")

def train_model(X_train, X_test, y_train, y_test):
    st.header("🤖 Train Model")
    
    st.info(f"Training set: {len(X_train)} samples")
    st.info(f"Test set: {len(X_test)} samples")
    
    if st.button("Train Model", type="primary"):
        with st.spinner("Training model... This may take a while"):
            try:
                # Create and fit TF-IDF vectorizer with URL-appropriate parameters
                tfidf = TfidfVectorizer(
                    max_features=1000, 
                    min_df=1,  # Reduced from 2 to handle smaller datasets
                    max_df=0.95,
                    ngram_range=(1, 2)  # Use unigrams and bigrams
                )
                X_train_tfidf = tfidf.fit_transform(X_train).toarray()
                X_test_tfidf = tfidf.transform(X_test).toarray()
                
                # Check if we have features
                if X_train_tfidf.shape[1] == 0:
                    st.error("No features found after vectorization. Try using a different dataset.")
                    return
                
                # Train a model
                model = RandomForestClassifier(n_estimators=50, random_state=42)  # Reduced trees for speed
                model.fit(X_train_tfidf, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test_tfidf)
                accuracy = accuracy_score(y_test, y_pred)
                
                # Save the model
                pickle.dump(tfidf, open('url_spam_tfidf.pkl', 'wb'))
                pickle.dump(model, open('url_spam_tfmodel.pkl', 'wb'))
                
                st.success(f"Model trained successfully! Accuracy: {accuracy:.2%}")
                st.balloons()
                
                # Show feature importance if we have features
                if len(tfidf.get_feature_names_out()) > 0:
                    st.subheader("Top 10 Important Features")
                    feature_names = tfidf.get_feature_names_out()
                    importances = model.feature_importances_
                    indices = np.argsort(importances)[-10:]  # Top 10 features
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.barh(range(len(indices)), importances[indices], color='b', align='center')
                    ax.set_yticks(range(len(indices)))
                    ax.set_yticklabels([feature_names[i] for i in indices])
                    ax.set_xlabel('Relative Importance')
                    ax.set_title('Top 10 Important Features')
                    st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Error during training: {e}")

def model_performance(X_train, X_test, y_train, y_test, df_processed):
    st.header("📈 Model Performance")
    
    try:
        tfidf = pickle.load(open('url_spam_tfidf.pkl', 'rb'))
        model = pickle.load(open('url_spam_tfmodel.pkl', 'rb'))
    except:
        st.error("No trained model found. Please train a model first.")
        return
    
    # Transform the test data
    X_test_tfidf = tfidf.transform(X_test).toarray()
    
    # Make predictions
    y_pred = model.predict(X_test_tfidf)
    y_pred_proba = model.predict_proba(X_test_tfidf)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accuracy", f"{accuracy:.2%}")
    
    with col2:
        st.metric("Test Samples", len(X_test))
    
    # Confusion matrix
    st.subheader("Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.set_xticklabels(['Legitimate', 'Spam'])
    ax.set_yticklabels(['Legitimate', 'Spam'])
    st.pyplot(fig)
    
    # Classification report
    st.subheader("Classification Report")
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    st.dataframe(report_df)

if __name__ == "__main__":
    main()