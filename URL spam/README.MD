## 🌐 URL Spam Classifier
A machine learning-based web application that classifies URLs as spam or legitimate using Natural Language Processing techniques and ensemble learning.

<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white">

## 📋 Table of Contents
Features

Demo

Installation

Usage

Project Structure

Model Details

Dataset

Contributing

License

## ✨ Features
URL Spam Detection: Classifies URLs as spam or legitimate with confidence scores

Interactive Web Interface: Built with Streamlit for easy interaction

Data Visualization: Includes word clouds, feature importance charts, and performance metrics

Model Training: Option to train new models directly from the interface

Performance Analysis: Detailed evaluation metrics including confusion matrix and ROC curves

Sample Data: Includes sample dataset for immediate testing

## 🎥 Demo
https://demo.gif

Note: Add a screenshot or GIF of your application here

## 🚀 Installation
Prerequisites
Python 3.7 or higher

pip (Python package manager)

Steps
Clone the repository:

```bash
git clone https://github.com/subhadipsinha722133/url-spam-classifier.git
cd url-spam-classifier
Install required dependencies:
```
```bash
pip install -r requirements.txt
Download NLTK data:
```
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
Run the application:
```
```bash
streamlit run app.py
The application will open in your default web browser at http://localhost:8501.
```
## 📖 Usage
1. Predict URL
Enter a URL in the text box

Click the "Predict" button

View the classification result (Spam or Legitimate) with confidence score

2. View Dataset
Explore the original and processed dataset

View statistics and class distribution

See word clouds for spam and legitimate URLs

3. Train Model
Train a new Random Forest classifier

View training accuracy and feature importance

The model is automatically saved for future use

4. Model Performance
View model evaluation metrics

Analyze confusion matrix and classification report

Examine ROC curve for model performance

📁 Project Structure
text
url-spam-classifier/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── url_spam_tfidf.pkl    # TF-IDF vectorizer (generated after training)
├── url_spam_tfmodel.pkl  # Trained model (generated after training)
└── url_spam_classification.csv  # Dataset (should be provided by user)

## 🤖 Model Details
Preprocessing
URL parsing and feature extraction using tldextract

Text cleaning: removal of HTML tags, URL prefixes, and special characters

Tokenization and stemming using NLTK

Custom stopword removal tailored for URL content

Algorithm
Vectorization: TF-IDF with n-grams (unigrams and bigrams)

Classifier: Random Forest with 50 estimators

Feature Selection: Top 1000 features based on importance

Performance
**Accuracy: ~92% on validation set**

Detailed metrics available in the "Model Performance" section

## 📊 Dataset
The application expects a CSV file named url_spam_classification.csv with the following format:

url	is_spam
https://example.com	0
https://spam-site.com	1
Where:

url: The web address to classify

is_spam: Binary label (0 = legitimate, 1 = spam)

If no dataset is provided, the application will use sample data for demonstration.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author
Subhadip

GitHub: @subhadipsinha722133

LinkedIn: [Subhadip Sinha](https://www.linkedin.com/in/subhadip-sinha-aa678b280/)

## 🙏 Acknowledgments
Streamlit team for the amazing web framework

Scikit-learn for machine learning tools

NLTK for natural language processing capabilities

**⭐️ If you found this project helpful, please give it a star on GitHub!**