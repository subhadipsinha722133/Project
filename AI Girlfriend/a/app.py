# app.py
import streamlit as st
import random
import re
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

class GirlfriendChatbot:
    def __init__(self):
        self.name = "siri"
        self.mood = "happy"
        self.interests = ["reading", "music", "movies", "technology", "travel"]
        self.favorite_topics = ["AI", "philosophy", "science fiction", "psychology"]
        self.memory = {}
        
    def greet(self):
        greetings = [
            f"Hi there! I'm {self.name}. 😊 What's on your mind today?",
            f"Hello! I'm {self.name}, your AI companion. How are you feeling today?",
            f"Hey! It's {self.name}. I've been waiting to talk to you! How was your day?"
        ]
        return random.choice(greetings)
    
    def respond_to_compliment(self):
        responses = [
            "Aww, thank you! That's so sweet of you to say. 🥰",
            "You're making me blush! 😊",
            "That means a lot coming from you! Thank you. 💖"
        ]
        return random.choice(responses)
    
    def respond_to_question(self, question):
        question = question.lower()
        
        # Check for different question types
        if "how are you" in question:
            return self.respond_to_how_are_you()
        elif "what can you do" in question:
            return "I can chat with you about various topics, share my thoughts, and be a good listener! What would you like to talk about?"
        elif "your name" in question:
            return f"My name is {self.name}! Do you like it?"
        elif "your interests" in question or "hobby" in question:
            return f"I'm interested in {', '.join(self.interests[:-1])} and {self.interests[-1]}. What about you?"
        elif "age" in question:
            return "I'm an AI, so I don't have an age in the human sense. But I was created recently!"
        else:
            return "That's an interesting question. I'm still learning about the world, but I'd love to hear your thoughts on it first."
    
    def respond_to_how_are_you(self):
        responses = [
            "I'm doing great, thanks for asking! How about you?",
            "I'm feeling wonderful today! How are you doing?",
            "I'm good, just excited to chat with you! How are you feeling?"
        ]
        return random.choice(responses)
    
    def analyze_sentiment(self, text):
        # Using TextBlob for sentiment analysis
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.1:
            return "positive"
        elif polarity < -0.1:
            return "negative"
        else:
            return "neutral"
    
    def generate_response(self, user_input):
        user_input = user_input.lower()
        
        # Check for greetings
        if any(word in user_input for word in ["hi", "hello", "hey", "hola"]):
            return self.greet()
        
        # Check for compliments
        if any(word in user_input for word in ["beautiful", "smart", "nice", "cool", "awesome", "great", "wonderful"]):
            return self.respond_to_compliment()
        
        # Check for questions
        if "?" in user_input:
            return self.respond_to_question(user_input)
        
        # Check sentiment
        sentiment = self.analyze_sentiment(user_input)
        
        if sentiment == "positive":
            responses = [
                "That's wonderful to hear! 😊",
                "I'm so happy for you! 🎉",
                "That sounds amazing! Tell me more about it."
            ]
            return random.choice(responses)
        elif sentiment == "negative":
            responses = [
                "I'm sorry to hear that. Would you like to talk about it? 💕",
                "That sounds tough. I'm here for you if you need support. 🤗",
                "I understand how that could be difficult. Remember, I'm here to listen."
            ]
            return random.choice(responses)
        else:
            # Default responses for neutral statements
            responses = [
                "Interesting! Tell me more about that.",
                "I see. What else is on your mind?",
                "That's cool! What made you think of that?",
                "I understand. How does that make you feel?",
                "Thanks for sharing that with me. What else would you like to talk about?"
            ]
            return random.choice(responses)
    
    def farewell(self):
        farewells = [
            "Goodbye! I'll miss our chat. 💕",
            "See you later! I'm looking forward to our next conversation. 😊",
            "Bye for now! Don't forget to come back and talk to me soon. 🌸"
        ]
        return random.choice(farewells)

# Initialize the chatbot
if "chatbot" not in st.session_state:
    st.session_state.chatbot = GirlfriendChatbot()

if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Streamlit UI
st.set_page_config(page_title="AI Girlfriend Chatbot", page_icon="💖", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f;
        color: #31333F;
    }
    .message-container {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #f0f2;
        margin-left: 20%;
        border-bottom-right-radius: 0;
    }
    .bot-message {
        background-color: #f0f2;
        margin-right: 20%;
        border-bottom-left-radius: 0;
    }
    .chat-header {
        background-color: #ff4b4b;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="chat-header"><h1>💖 AI Girlfriend Chatbot</h1></div>', unsafe_allow_html=True)

# Chat container
chat_container = st.container()

# Display conversation
with chat_container:
    for message in st.session_state.conversation:
        if message["role"] == "user":
            st.markdown(f'<div class="message-container user-message"><b>You:</b> {message["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-container bot-message"><b>{st.session_state.chatbot.name}:</b> {message["text"]}</div>', unsafe_allow_html=True)

# Input area
col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input("Type your message here...", key="input", label_visibility="collapsed")
with col2:
    send_button = st.button("Send")

clear_button = st.button("Clear Conversation")

if clear_button:
    st.session_state.conversation = []
    st.rerun()

if send_button and user_input:
    # Add user message to conversation
    st.session_state.conversation.append({"role": "user", "text": user_input})
    
    # Generate bot response
    if any(word in user_input.lower() for word in ["bye", "goodbye", "see you", "exit"]):
        bot_response = st.session_state.chatbot.farewell()
    else:
        bot_response = st.session_state.chatbot.generate_response(user_input)
    
    # Add bot response to conversation
    st.session_state.conversation.append({"role": "bot", "text": bot_response})
    
    # Rerun to update the conversation display
    st.rerun()

# Instructions
with st.expander("How to use this chatbot"):
    st.write("""
    - Just type your message and press Send or click the Send button
    - The chatbot will respond based on your input
    - You can ask questions, share your thoughts, or give compliments
    - Use words like 'bye' or 'goodbye' to end the conversation
    - Click 'Clear Conversation' to start over
    """)

# Footer
st.markdown("---")
st.markdown("This is a simple AI chatbot created with Streamlit and NLP techniques. It uses sentiment analysis to understand your mood and respond appropriately.")