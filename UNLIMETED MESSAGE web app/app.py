import streamlit as st
import pyautogui
import time

# Streamlit UI
st.title("💬 Auto Message Sender")
st.write("This will automatically type messages - **Developed By Subhadip**")

message = st.text_input("Enter the message", " ")
repeat_count = st.number_input("Number of times to send", min_value=1, max_value=500, value=10)
delay = st.number_input("Delay before starting (seconds)", min_value=0, max_value=10, value=4)

if st.button("Start Sending"):
    st.warning(f"Switch to the chat window in {delay} seconds... typing will start automatically!")
    time.sleep(delay)  # Wait so user can focus the input field
    for count in range(repeat_count):
        pyautogui.typewrite(f"{message} {count}")
        pyautogui.press("enter")
    st.success("✅ Done sending messages!")
