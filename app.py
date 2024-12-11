import os
import requests
import streamlit as st
from streamlit_lottie import st_lottie

# Chatbot API URL
URL = "https://oreonmayo-akamaicare.hf.space/chatbot/"

# Load Lottie animation
@st.cache_data
def load_lottie_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

# Load animations
bot_animation = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_jcikwtux.json")
user_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_otqjv8le.json")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .title {
        color: #00ffcc;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    .info {
        color: #cccccc;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton button {
        background-color: #00ffcc;
        color: #000000;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    input, textarea {
        background-color: #333333 !important;
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title with animation
st.markdown("<h1 class='title'>AkamaiCare Chatbot</h1>", unsafe_allow_html=True)
if bot_animation:
    st_lottie(bot_animation, height=150, key="bot")
st.markdown(
    "<p class='info'>Ask me questions about Hawaiian healthcare: hospitals, care facilities, and more!</p>",
    unsafe_allow_html=True,
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    if message["role"] == "user" and user_animation:
        st_lottie(user_animation, height=100, key=f"user_{st.session_state.messages.index(message)}")
    with st.chat_message(message["role"]):
        st.markdown(message["output"])

# Input box for user prompt
if prompt := st.chat_input("What do you want to know?"):
    # Add user message to chat history
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "output": prompt})

    # Send the query to the API
    data = {"query": prompt}

    with st.spinner("Searching for an answer..."):
        try:
            response = requests.get(URL, params=data)
            if response.status_code == 200:
                response_data = response.json()
                output_text = response_data.get("response", "No response available.")
                output_text = output_text['text']
            else:
                output_text = (
                    f"An error occurred while processing your message.\n"
                    f"Error Code: {response.status_code}, {response.text}"
                )
        except Exception as e:
            output_text = (
                "An error occurred while processing your message. Please try again later.\n"
                f"Error details: {str(e)}"
            )

    # Add assistant response to chat history
    st.chat_message("assistant").markdown(output_text)
    st.session_state.messages.append({"role": "assistant", "output": output_text})