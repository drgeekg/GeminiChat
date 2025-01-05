import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS

# Configure Streamlit page
st.set_page_config(
    page_title="GeminiChat",
    page_icon="🔥",
)

# Set up the app
st.title("GeminiChat")
st.caption("A chatbot powered by Google Gemini Pro.")

# Embed your API key here
API_KEY = "YOUR_API_KEY_HERE"

# Configure the Generative AI client
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Failed to configure the Gemini API. Please check your API key.")
    st.stop()

# Initialize model and chat history
if "history" not in st.session_state:
    st.session_state.history = []

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=st.session_state.history)

# Display chat history
for message in chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Chat input functionality
if prompt := st.chat_input("Type your message here..."):
    prompt = prompt.replace('\n', '  \n')  # Handle newlines in input
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            full_response = ""
            for chunk in chat.send_message(prompt, stream=True, safety_settings=SAFETY_SETTTINGS):
                word_count = 0
                random_int = random.randint(5, 10)
                for word in chunk.text:
                    full_response += word
                    word_count += 1
                    if word_count == random_int:
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "_")
                        word_count = 0
                        random_int = random.randint(5, 10)
            message_placeholder.markdown(full_response)
        except genai.types.generation_types.BlockedPromptException as e:
            st.warning("Blocked prompt: " + str(e))
        except Exception as e:
            st.error("An error occurred: " + str(e))

    # Update session history
    st.session_state.history = chat.history
