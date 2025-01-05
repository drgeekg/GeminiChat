import google.generativeai as genai
import streamlit as st
import time
import random

# Streamlit configuration
st.set_page_config(
    page_title="GeminiChat",
    page_icon="🔥",
)

st.title("GeminiChat")
st.caption("A chatbot powered by Google Gemini Pro.")

# Embedded API key
API_KEY = "YOUR_API_KEY_HERE"

if "history" not in st.session_state:
    st.session_state.history = []

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.warning("Error configuring the API key. Please check your API_KEY.")

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=st.session_state.history)

# Chat interface
for message in chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("Type your message here..."):
    prompt = prompt.replace('\n', '  \n')
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            full_response = ""
            for chunk in chat.send_message(prompt, stream=True):  # Removed safety_settings
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
            st.error("Blocked prompt detected: Please rephrase your input.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        st.session_state.history = chat.history
