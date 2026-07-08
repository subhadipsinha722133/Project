import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import LabelEncoder

import warnings
warnings.filterwarnings('ignore')

# Download stopwords
try:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
except:
    st.warning("Could not download stopwords. Using basic stopwords list.")
    stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

# Set page configuration
st.set_page_config(
    page_title="Twitter Sentiment Analysis",
    page_icon="🐦",
    layout="wide"
)

# Title and description
st.title("🐦 Twitter Sentiment Analysis")
st.markdown("""
This app analyzes sentiment from Twitter data and trains a deep learning model to classify tweets.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose a section",
    ["Data Overview", "Data Visualization", "Model Training", "Make Predictions"]
)

# Text preprocessing function
def preprocess_text(text):
    if isinstance(text, str):
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove numbers
        text = ''.join([char for char in text if not char.isdigit()])
        
        # Remove stopwords
        text = ' '.join([word for word in text.split() if word not in stop_words])
        
        return text
    else:
        return ""

# Load and preprocess data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('twitter_training.csv')
        # Drop unnecessary columns
        data = data.drop(['id', 'game'], axis=1)
        # Remove duplicates
        data.drop_duplicates(inplace=True)
        # Remove rows with missing values
        data = data.dropna()
        # Preprocess text
        data['cleaned_text'] = data['text'].apply(preprocess_text)
        return data
    except FileNotFoundError:
        st.error("File 'twitter_training.csv' not found. Please make sure the file exists in the same directory.")
        return None

data = load_data()

if data is not None:
    if app_mode == "Data Overview":
        st.header("📊 Data Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dataset Preview")
            st.dataframe(data.head(10))
            
        with col2:
            st.subheader("Dataset Information")
            st.write(f"**Total samples:** {len(data)}")
            st.write(f"**Number of features:** {len(data.columns)}")
            st.write(f"**Missing values:** {data.isnull().sum().sum()}")
        
        st.subheader("Sentiment Distribution")
        sentiment_counts = data['sentiment'].value_counts()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Bar plot
        sentiment_counts.plot(kind='bar', ax=ax1, color=['skyblue', 'lightcoral', 'lightgreen', 'gold'])
        ax1.set_title('Sentiment Distribution')
        ax1.set_xlabel('Sentiment')
        ax1.set_ylabel('Count')
        ax1.tick_params(axis='x', rotation=45)
        
        # Pie chart
        ax2.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', 
                colors=['skyblue', 'lightcoral', 'lightgreen', 'gold'])
        ax2.set_title('Sentiment Proportion')
        
        st.pyplot(fig)
        
        st.subheader("Sample Texts by Sentiment")
        sentiment_option = st.selectbox("Select sentiment to view samples:", data['sentiment'].unique())
        
        sample_texts = data[data['sentiment'] == sentiment_option]['text'].head(5).tolist()
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{i}. {text}")

    elif app_mode == "Data Visualization":
        st.header("📈 Data Visualization")
        
        # Word Cloud
        st.subheader("Word Clouds by Sentiment")
        
        sentiment_option_viz = st.selectbox("Select sentiment for word cloud:", data['sentiment'].unique())
        
        sentiment_texts = ' '.join(data[data['sentiment'] == sentiment_option_viz]['cleaned_text'])
        
        if sentiment_texts.strip():
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(sentiment_texts)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title(f'Word Cloud for {sentiment_option_viz} Sentiment')
            st.pyplot(fig)
        else:
            st.warning("No text data available for this sentiment.")
        
        # Text Length Analysis
        st.subheader("Text Length Analysis")
        data['text_length'] = data['cleaned_text'].apply(lambda x: len(x.split()))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=data, x='sentiment', y='text_length', ax=ax)
        ax.set_title('Text Length Distribution by Sentiment')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
        
        # Most Common Words
        st.subheader("Most Common Words by Sentiment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sentiment_common = st.selectbox("Select sentiment:", data['sentiment'].unique(), key="common_words")
        
        with col2:
            top_n = st.slider("Number of top words to show:", min_value=5, max_value=20, value=10)
        
        sentiment_data = data[data['sentiment'] == sentiment_common]
        all_words = ' '.join(sentiment_data['cleaned_text']).split()
        word_freq = Counter(all_words)
        common_words = word_freq.most_common(top_n)
        
        words, counts = zip(*common_words)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(words, counts, color='skyblue')
        ax.set_title(f'Top {top_n} Most Common Words in {sentiment_common} Sentiment')
        ax.set_xlabel('Frequency')
        st.pyplot(fig)

    elif app_mode == "Model Training":
        st.header("🤖 Model Training")
        
        st.info("This section trains a neural network model for sentiment classification.")
        
        # Model parameters
        st.subheader("Model Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            vocab_size = st.slider("Vocabulary Size", min_value=1000, max_value=20000, value=10000, step=1000)
            embedding_dim = st.slider("Embedding Dimension", min_value=50, max_value=300, value=100, step=50)
        
        with col2:
            max_length = st.slider("Maximum Sequence Length", min_value=50, max_value=200, value=100, step=10)
            lstm_units = st.slider("LSTM Units", min_value=32, max_value=128, value=64, step=16)
        
        with col3:
            test_size = st.slider("Test Set Size", min_value=0.1, max_value=0.4, value=0.2, step=0.05)
            epochs = st.slider("Training Epochs", min_value=5, max_value=50, value=20, step=5)
        
        if st.button("Train Model"):
            with st.spinner("Training model... This may take a few minutes."):
                # Prepare the data
                X = data['cleaned_text']
                y = data['sentiment']
                
                # Encode labels
                label_encoder = LabelEncoder()
                y_encoded = label_encoder.fit_transform(y)
                num_classes = len(label_encoder.classes_)
                
                # Split the data
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y_encoded, test_size=test_size, random_state=42, stratify=y_encoded
                )
                
                # Tokenize text
                tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
                tokenizer.fit_on_texts(X_train)
                
                # Convert to sequences
                X_train_seq = tokenizer.texts_to_sequences(X_train)
                X_test_seq = tokenizer.texts_to_sequences(X_test)
                
                # Pad sequences
                X_train_pad = pad_sequences(X_train_seq, maxlen=max_length, padding='post', truncating='post')
                X_test_pad = pad_sequences(X_test_seq, maxlen=max_length, padding='post', truncating='post')
                
                # Build the model
                model = tf.keras.Sequential([
                    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
                    tf.keras.layers.LSTM(lstm_units, return_sequences=False),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(num_classes, activation='softmax')
                ])
                
                model.compile(
                    optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy']
                )
                
                # Callbacks
                early_stopping = EarlyStopping(patience=3, restore_best_weights=True)
                reduce_lr = ReduceLROnPlateau(factor=0.2, patience=2)
                
                # Train the model
                history = model.fit(
                    X_train_pad, y_train,
                    epochs=epochs,
                    validation_data=(X_test_pad, y_test),
                    callbacks=[early_stopping, reduce_lr],
                    verbose=0
                )
                
                # Evaluate the model
                train_loss, train_accuracy = model.evaluate(X_train_pad, y_train, verbose=0)
                test_loss, test_accuracy = model.evaluate(X_test_pad, y_test, verbose=0)
                
                # Store model and tokenizer in session state
                st.session_state.model = model
                st.session_state.tokenizer = tokenizer
                st.session_state.label_encoder = label_encoder
                st.session_state.max_length = max_length
                
                # Display results
                st.success("Model training completed!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Training Accuracy", f"{train_accuracy:.2%}")
                    st.metric("Test Accuracy", f"{test_accuracy:.2%}")
                
                with col2:
                    st.metric("Training Loss", f"{train_loss:.4f}")
                    st.metric("Test Loss", f"{test_loss:.4f}")
                
                # Plot training history
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
                
                ax1.plot(history.history['accuracy'], label='Training Accuracy')
                ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
                ax1.set_title('Model Accuracy')
                ax1.set_xlabel('Epoch')
                ax1.set_ylabel('Accuracy')
                ax1.legend()
                
                ax2.plot(history.history['loss'], label='Training Loss')
                ax2.plot(history.history['val_loss'], label='Validation Loss')
                ax2.set_title('Model Loss')
                ax2.set_xlabel('Epoch')
                ax2.set_ylabel('Loss')
                ax2.legend()
                
                st.pyplot(fig)
                
                # Confusion Matrix
                st.subheader("Confusion Matrix")
                y_pred = model.predict(X_test_pad)
                y_pred_classes = np.argmax(y_pred, axis=1)
                
                cm = confusion_matrix(y_test, y_pred_classes)
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                           xticklabels=label_encoder.classes_, 
                           yticklabels=label_encoder.classes_, ax=ax)
                ax.set_xlabel('Predicted')
                ax.set_ylabel('Actual')
                ax.set_title('Confusion Matrix')
                st.pyplot(fig)

    elif app_mode == "Make Predictions":
        st.header("🔮 Make Predictions")
        
        if 'model' not in st.session_state:
            st.warning("Please train the model first in the 'Model Training' section.")
        else:
            st.subheader("Predict Sentiment for New Text")
            
            input_option = st.radio("Choose input method:", 
                                  ["Single Text Input", "Batch Upload (CSV)"])
            
            if input_option == "Single Text Input":
                user_input = st.text_area("Enter text to analyze:", 
                                        "I love this game! It's amazing!")
                
                if st.button("Analyze Sentiment"):
                    if user_input.strip():
                        # Preprocess input
                        cleaned_input = preprocess_text(user_input)
                        
                        # Tokenize and pad
                        tokenizer = st.session_state.tokenizer
                        sequence = tokenizer.texts_to_sequences([cleaned_input])
                        padded_sequence = pad_sequences(sequence, maxlen=st.session_state.max_length)
                        
                        # Make prediction
                        model = st.session_state.model
                        prediction = model.predict(padded_sequence)
                        predicted_class = np.argmax(prediction, axis=1)[0]
                        confidence = np.max(prediction)
                        
                        # Decode prediction
                        label_encoder = st.session_state.label_encoder
                        sentiment_label = label_encoder.inverse_transform([predicted_class])[0]
                        
                        # Display results
                        st.subheader("Prediction Results")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Predicted Sentiment", sentiment_label)
                            st.metric("Confidence", f"{confidence:.2%}")
                        
                        with col2:
                            # Show probability distribution
                            fig, ax = plt.subplots(figsize=(8, 4))
                            classes = label_encoder.classes_
                            y_pos = np.arange(len(classes))
                            
                            ax.barh(y_pos, prediction[0], color='lightblue')
                            ax.set_yticks(y_pos)
                            ax.set_yticklabels(classes)
                            ax.set_xlabel('Probability')
                            ax.set_title('Sentiment Probability Distribution')
                            ax.invert_yaxis()
                            
                            st.pyplot(fig)
                        
                        st.subheader("Original Text")
                        st.write(user_input)
                        
                        st.subheader("Preprocessed Text")
                        st.write(cleaned_input)
                    
                    else:
                        st.error("Please enter some text to analyze.")
            
            else:  # Batch Upload
                uploaded_file = st.file_uploader("Upload CSV file with 'text' column", type=['csv'])
                
                if uploaded_file is not None:
                    batch_data = pd.read_csv(uploaded_file)
                    
                    if 'text' not in batch_data.columns:
                        st.error("Uploaded CSV must contain a 'text' column.")
                    else:
                        if st.button("Analyze Batch"):
                            with st.spinner("Processing batch data..."):
                                # Preprocess texts
                                batch_data['cleaned_text'] = batch_data['text'].apply(preprocess_text)
                                
                                # Tokenize and pad
                                tokenizer = st.session_state.tokenizer
                                sequences = tokenizer.texts_to_sequences(batch_data['cleaned_text'])
                                padded_sequences = pad_sequences(sequences, maxlen=st.session_state.max_length)
                                
                                # Make predictions
                                model = st.session_state.model
                                predictions = model.predict(padded_sequences)
                                predicted_classes = np.argmax(predictions, axis=1)
                                confidences = np.max(predictions, axis=1)
                                
                                # Decode predictions
                                label_encoder = st.session_state.label_encoder
                                sentiment_labels = label_encoder.inverse_transform(predicted_classes)
                                
                                # Add predictions to dataframe
                                batch_data['predicted_sentiment'] = sentiment_labels
                                batch_data['confidence'] = confidences
                                
                                # Display results
                                st.subheader("Batch Prediction Results")
                                st.dataframe(batch_data[['text', 'predicted_sentiment', 'confidence']])
                                
                                # Download results
                                csv = batch_data.to_csv(index=False)
                                st.download_button(
                                    label="Download Predictions as CSV",
                                    data=csv,
                                    file_name="sentiment_predictions.csv",
                                    mime="text/csv"
                                )
                                
                                # Show summary statistics
                                st.subheader("Batch Summary")
                                sentiment_summary = batch_data['predicted_sentiment'].value_counts()
                                
                                fig, ax = plt.subplots(figsize=(10, 6))
                                sentiment_summary.plot(kind='bar', ax=ax, color='lightgreen')
                                ax.set_title('Predicted Sentiment Distribution')
                                ax.set_xlabel('Sentiment')
                                ax.set_ylabel('Count')
                                ax.tick_params(axis='x', rotation=45)
                                st.pyplot(fig)

else:
    st.error("Unable to load data. Please check if 'twitter_training.csv' exists in the correct location.")

# Footer
st.markdown("---")
st.markdown("Twitter Sentiment Analysis App | Built with Streamlit")