# Girlfriend GPT 💕
An interactive AI girlfriend chatbot with multiple personalities, built with Streamlit and Keras. Experience conversations with different AI personalities including girlfriend mode, bro mode, and anime character mode!

<img src="https://img.shields.io/badge/Girlfriend-GPT-pink https://img.shields.io/badge/Python-3.8%252B-blue https://img.shields.io/badge/Streamlit-1.28%252B-red https://img.shields.io/badge/Keras-2.12%252B-orange https://img.shields.io/badge/License-MIT-green">

🌟 Live Demo
<img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg">

## 📸 Screenshots
<div align="center"> <img src="https://via.placeholder.com/400x250/ff4b4b/ffffff?text=Chat+Interface" alt="Chat Interface" width="400" /> <img src="https://via.placeholder.com/400x250/4b78ff/ffffff?text=Model+Training" alt="Model Training" width="400" /> </div>

## ✨ Features

🤖 AI-powered conversational chatbot with multiple personalities

💕 Girlfriend mode with romantic responses

👊 Bro mode with casual, friendly interactions

🎌 Anime character mode (Mikasa from Attack on Titan)

📊 Real-time model training with accuracy metrics

💬 Beautiful Streamlit chat interface

🎯 Neural network-based intent recognition

📱 Fully responsive web interface

🔄 Session-based chat history

## 🚀 Quick Start
Prerequisites
Python 3.8 or higher

pip package manager

Installation
Clone the repository

```bash
git clone https://github.com/subhadipsinha722133/Girlfriend-GPT.git
cd Girlfriend-GPT
```
Install dependencies
```bash
pip install -r requirements.txt
```
Run the application

```bash
streamlit run girlfriend_gpt.py
Open your browser and go to http://localhost:8501
```

# 🎮 How to Use
Open the application in your web browser

Train the model by clicking the "Train Model" button in the sidebar

Wait for training to complete (typically takes 1-2 minutes)

Start chatting by typing messages in the chat input

View model accuracy in the sidebar after training

Example Conversations
Girlfriend mode: "Write a poem for me" → Romantic poetry response

Bro mode: "bro have any good jokes" → Funny jokes and banter

Anime mode: "hi there Mikasa" → Mikasa Ackerman responses

Advice mode: "bro should I play games or study" → Helpful advice

# 🏗️ Project Structure
text <br>
Girlfriend-GPT/
├── app.py          # Main application file
├── requirements.txt           # Python dependencies
├── README.md                 # This documentation file
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── models/                   # Trained models directory
│   ├── chatbot_model.h5      # Keras model (generated)
│   ├── words.pkl             # Vocabulary (generated)
│   └── classes.pkl           # Classes (generated)
└── .gitignore               # Git ignore rules

## 🧠 Model Architecture
The chatbot uses a neural network with the following architecture:

Input Layer: 5 neurons with ReLU activation

Hidden Layers: 40 and 4 neurons with Batch Normalization

Output Layer: Softmax activation for intent classification

Regularization: Dropout (0.5) to prevent overfitting

Optimizer: SGD with Nesterov momentum

Loss Function: Categorical cross-entropy

Training Process
Text Preprocessing: Tokenization and lemmatization

Bag-of-Words: Convert patterns to numerical vectors

Model Training: 200 epochs with batch size of 5

Intent Prediction: Probability threshold of 0.25

# 🌐 Deployment
Deploy to Streamlit Cloud
Fork this repository on GitHub

Connect your GitHub account to Streamlit Cloud

Select your repository and set main file to girlfriend_gpt.py

Click Deploy - your app will be live in minutes!


## 📑 Customizing Responses
Edit the girlfriend variable in the code to add new intents and responses:

python
    {
      "tag": "greeting",
      "patterns": ["hi", "hello", "hey", "hiya", "howdy", "hey there", "hello there", "hi there", "greetings", "hey you", "hi sweetie", "hello beautiful", "hey love", "hi my love", "morning", "good morning", "afternoon", "good afternoon", "evening", "good evening", "hey babe", "hi honey", "hey darling", "hi angel", "hey sweetheart", "hi gorgeous", "hey cutie", "hi dear", "hey boo", "well hello", "look who it is", "hi sweetness", "hey my love", "hello darling", "good day", "hey sunshine", "hi precious", "hey lover", "hi handsome", "hey sexy", "hi sweetheart", "hey honey bunny", "hi lovebug", "hey sugar", "hi muffin"],
      "responses": ["Hey babe 😊 How was your day?", "Hi! I've missed you 💕 What did you do today?", "Hello, my love! 🥰 Seeing your name pop up made me smile.", "Hey you! 💖 I was just thinking about you.", "Hi sweetheart! 😘 Tell me everything!", "Well hello there, handsome! 😍 This is a nice surprise!", "Hey sunshine! ☀️ You just brightened my day!", "Hi my love! My heart did a little jump when I saw your message. 💓", "Good morning, sleepyhead! 😴💤 Did you dream of me?", "Hey you! I was hoping you'd text. 💌"]
    }

# 🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the project

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

Development Setup
Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  
Install development dependencies:
```
```bash
pip install -r requirements-dev.txt
Run tests:
```
```bash
pytest
Format code:
```
```bash
black app.py
```
# 🐛 Troubleshooting
Common Issues
NLTK data not found:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
TensorFlow compatibility issues:
```
```bash
pip uninstall tensorflow keras
pip install tensorflow==2.13.0 keras==2.13.1
Port already in use:
```
```bash
streamlit run --server.port 8502 girlfriend_gpt.py
Memory errors on deployment: Reduce model complexity or use pre-trained models
```
Getting Help
If you encounter issues:

Check the FAQ section below

Search existing GitHub Issues

Create a new issue with details about your problem

# ❓ FAQ
Q: How accurate is the chatbot?
A: The model typically achieves around 95% accuracy after training with the provided dataset.

Q: Can I add custom responses?
A: Yes! Edit the girlfriend variable in the code to add new intents and responses.

Q: Is my chat data stored?
A: No, all conversations are stored only in your browser session and are not saved to any server.

Q: Can I deploy this commercially?
A: Please check the MIT license terms for commercial use.

Q: How can I improve the model accuracy?
A: Add more training examples to each intent, increase training epochs, or adjust the neural network architecture.

Q: Does this work on mobile devices?
A: Yes, the Streamlit interface is fully responsive and works on mobile devices.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
Built with Streamlit for the web interface

Uses Keras and TensorFlow for machine learning

Natural Language Processing with NLTK

Inspired by conversational AI projects and chatbot frameworks

## 👥 Contributors
Subhadip Sinha - Creator and maintainer


# 📞 Support
If you like this project, please give it a star ⭐ on GitHub!

For questions and support:

Open an issue

Join our Discord community

Email: your-sinhasubhadip34@gmail.com

# 🔗 Related Projects
Boyfriend GPT - Male version of the chatbot

Anime Character AI - Anime-themed chatbot

Chatbot Framework - General purpose chatbot framework

## 📊 Stats
<img src="https://img.shields.io/github/forks/yourusername/girlfriend-gpt?style=social">
<img src="https://img.shields.io/github/stars/yourusername/girlfriend-gpt?style=social">
<img src="https://img.shields.io/github/issues/yourusername/girlfriend-gpt">
<img src="https://img.shields.io/github/issues-pr/yourusername/girlfriend-gpt">

<div align="center"> Made with ❤️ and Python </div>