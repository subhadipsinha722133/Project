import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
import pickle
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
@st.cache_resource
def download_nltk():
    nltk.download('stopwords', quiet=True)
    return stopwords.words('english')

stop_words = download_nltk()

# Page config
st.set_page_config(page_title="Twitter Sentiment Analysis", layout="wide")
st.title("🐦 Twitter Sentiment Analysis Dashboard")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Data Overview", "Train Model", "Predict Sentiment"])

# Text preprocessing function
def preprocess_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = ''.join([char for char in text if char not in string.punctuation])
        tokens = text.split()
        tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(tokens)
    return ""

# Load and cache data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('twitter_training.csv')
        data = data.drop(['id', 'game'], axis=1)
        data.drop_duplicates(inplace=True)
        data['cleaned_text'] = data['text'].apply(preprocess_text)
        data = data[data['cleaned_text'].str.len() > 0]
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Data Overview Page
if page == "Data Overview":
    st.header("📊 Data Overview")
    
    data = load_data()
    
    if data is not None:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tweets", len(data))
        with col2:
            st.metric("Unique Sentiments", data['sentiment'].nunique())
        with col3:
            st.metric("Cleaned Records", len(data))
        
        st.subheader("Sample Data")
        st.dataframe(data.head(10))
        
        # Sentiment Distribution
        st.subheader("Sentiment Distribution")
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            sentiment_counts = data['sentiment'].value_counts()
            ax.bar(sentiment_counts.index, sentiment_counts.values, color=['green', 'red', 'blue', 'orange'])
            ax.set_xlabel('Sentiment')
            ax.set_ylabel('Count')
            ax.set_title('Sentiment Distribution')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
            ax.set_title('Sentiment Proportion')
            st.pyplot(fig)
        
        # Word Cloud
        st.subheader("Word Cloud by Sentiment")
        selected_sentiment = st.selectbox("Select Sentiment", data['sentiment'].unique())
        
        sentiment_text = ' '.join(data[data['sentiment'] == selected_sentiment]['cleaned_text'])
        if sentiment_text:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(sentiment_text)
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title(f'Word Cloud for {selected_sentiment} Sentiment')
            st.pyplot(fig)

# Train Model Page
elif page == "Train Model":
    st.header("🤖 Train Sentiment Analysis Model")
    
    data = load_data()
    
    if data is not None:
        st.info(f"Dataset loaded with {len(data)} records")
        
        # Model parameters
        col1, col2 = st.columns(2)
        with col1:
            max_words = st.slider("Max Words in Vocabulary", 1000, 10000, 5000)
            max_len = st.slider("Max Sequence Length", 50, 200, 100)
            epochs = st.slider("Training Epochs", 5, 50, 20)
        
        with col2:
            embedding_dim = st.slider("Embedding Dimension", 32, 256, 128)
            lstm_units = st.slider("LSTM Units", 32, 256, 128)
            batch_size = st.slider("Batch Size", 16, 128, 32)
        
        if st.button("Train Model", type="primary"):
            with st.spinner("Training model... This may take a few minutes."):
                # Encode labels
                sentiment_mapping = {label: idx for idx, label in enumerate(data['sentiment'].unique())}
                data['label'] = data['sentiment'].map(sentiment_mapping)
                
                # Tokenization
                tokenizer = Tokenizer(num_words=max_words, oov_token='<OOV>')
                tokenizer.fit_on_texts(data['cleaned_text'])
                sequences = tokenizer.texts_to_sequences(data['cleaned_text'])
                padded = pad_sequences(sequences, maxlen=max_len, padding='post', truncating='post')
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    padded, data['label'], test_size=0.2, random_state=42
                )
                
                # Build model
                model = Sequential([
                    Embedding(max_words, embedding_dim, input_length=max_len),
                    Bidirectional(LSTM(lstm_units, return_sequences=True)),
                    Dropout(0.5),
                    Bidirectional(LSTM(lstm_units//2)),
                    Dropout(0.5),
                    Dense(64, activation='relu'),
                    Dropout(0.3),
                    Dense(len(sentiment_mapping), activation='softmax')
                ])
                
                model.compile(
                    optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy']
                )
                
                # Callbacks
                early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
                reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-7)
                
                # Train
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                history = model.fit(
                    X_train, y_train,
                    validation_data=(X_test, y_test),
                    epochs=epochs,
                    batch_size=batch_size,
                    callbacks=[early_stop, reduce_lr],
                    verbose=0
                )
                
                progress_bar.progress(100)
                status_text.success("Training completed!")
                
                # Save model and tokenizer
                model.save('sentiment_model.h5')
                with open('tokenizer.pkl', 'wb') as f:
                    pickle.dump(tokenizer, f)
                with open('sentiment_mapping.pkl', 'wb') as f:
                    pickle.dump(sentiment_mapping, f)
                
                # Display results
                st.success("Model trained and saved successfully!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Training Accuracy", f"{history.history['accuracy'][-1]:.4f}")
                    st.metric("Validation Accuracy", f"{history.history['val_accuracy'][-1]:.4f}")
                
                with col2:
                    st.metric("Training Loss", f"{history.history['loss'][-1]:.4f}")
                    st.metric("Validation Loss", f"{history.history['val_loss'][-1]:.4f}")
                
                # Plot training history
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
                
                ax1.plot(history.history['accuracy'], label='Train Accuracy')
                ax1.plot(history.history['val_accuracy'], label='Val Accuracy')
                ax1.set_xlabel('Epoch')
                ax1.set_ylabel('Accuracy')
                ax1.set_title('Model Accuracy')
                ax1.legend()
                ax1.grid(True)
                
                ax2.plot(history.history['loss'], label='Train Loss')
                ax2.plot(history.history['val_loss'], label='Val Loss')
                ax2.set_xlabel('Epoch')
                ax2.set_ylabel('Loss')
                ax2.set_title('Model Loss')
                ax2.legend()
                ax2.grid(True)
                
                st.pyplot(fig)

# Predict Sentiment Page
elif page == "Predict Sentiment":
    st.header("🔮 Predict Tweet Sentiment")
    
    try:
        model = tf.keras.models.load_model('sentiment_model.h5')
        with open('tokenizer.pkl', 'rb') as f:
            tokenizer = pickle.load(f)
        with open('sentiment_mapping.pkl', 'rb') as f:
            sentiment_mapping = pickle.load(f)
        
        reverse_mapping = {v: k for k, v in sentiment_mapping.items()}
        
        st.success("Model loaded successfully!")
        
        # Input text
        user_input = st.text_area("Enter a tweet to analyze:", height=100)
        
        if st.button("Analyze Sentiment", type="primary"):
            if user_input:
                # Preprocess
                cleaned_input = preprocess_text(user_input)
                sequence = tokenizer.texts_to_sequences([cleaned_input])
                padded = pad_sequences(sequence, maxlen=100, padding='post', truncating='post')
                
                # Predict
                prediction = model.predict(padded, verbose=0)
                predicted_class = np.argmax(prediction[0])
                predicted_sentiment = reverse_mapping[predicted_class]
                confidence = prediction[0][predicted_class] * 100
                
                # Display results
                st.subheader("Analysis Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Predicted Sentiment", predicted_sentiment)
                    st.metric("Confidence", f"{confidence:.2f}%")
                
                with col2:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    sentiments = list(reverse_mapping.values())
                    confidences = prediction[0] * 100
                    colors = ['green' if i == predicted_class else 'lightgray' for i in range(len(sentiments))]
                    ax.barh(sentiments, confidences, color=colors)
                    ax.set_xlabel('Confidence (%)')
                    ax.set_title('Sentiment Probabilities')
                    st.pyplot(fig)
            else:
                st.warning("Please enter a tweet to analyze.")
    
    except Exception as e:
        st.error(f"Model not found or error loading: {e}")
        st.info("Please train the model first from the 'Train Model' page.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Built with Streamlit & TensorFlow")