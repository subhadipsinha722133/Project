import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import os

# For now assuming you have trained and saved it
MODEL_PATH = r"C:\Users\sinha\Desktop\Human Facial Emotions Detection\facial_emotion_detection_model.h5"
model = load_model(MODEL_PATH)

# Define your class names (make sure they match your dataset classes)
class_names = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Streamlit UI
st.title("🎭 Face Emotion Recognition App")
st.write("Made By Subhadip 🔥")
st.write("Upload a face image to detect the emotion.")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load image
    img = image.load_img(uploaded_file, target_size=(48, 48), color_mode='grayscale')
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Prediction
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction)
    predicted_class = class_names[predicted_index]
    confidence = round(prediction[0][predicted_index] * 100, 2)

    # Display results
    st.image(uploaded_file, caption=f"Predicted: {predicted_class} ({confidence}%)", use_column_width=True)
    st.success(f"🎯 Emotion: **{predicted_class}** with confidence **{confidence}%**")

    # Show probabilities as a bar chart
    st.bar_chart(dict(zip(class_names, prediction[0])))
