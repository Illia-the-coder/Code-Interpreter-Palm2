import streamlit as st
import json
import os
import requests
from bardapi import Bard

# Load the GOOGLE_LANGUAGES_TO_CODES dictionary from lang.json
with open("lang.json", "r") as file:
    GOOGLE_LANGUAGES_TO_CODES = json.load(file)

# Set up the session for Bard API
session = requests.Session()
session.headers = {
    "Host": "bard.google.com",
    "X-Same-Domain": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://bard.google.com",
    "Referer": "https://bard.google.com/",
}
session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY"))
with st.sidebar:
    # Add a selector in the sidebar using the dictionary's keys
    selected_language_name = st.sidebar.selectbox("Select Language", list(GOOGLE_LANGUAGES_TO_CODES.keys()))
    code_interpreter = st.sidebar.checkbox("Code Interpreter", value=True)
    
# Retrieve the corresponding language code from the dictionary
selected_language_code = GOOGLE_LANGUAGES_TO_CODES[selected_language_name]

# Initialize Bard with the selected language code
bard = Bard(token=os.getenv("_BARD_API_KEY"), language=selected_language_code, session=session, timeout=30)

TITLE = "Palm 2🌴 Chatbot"
DESCRIPTION = """
"""

# Streamlit UI
st.title(TITLE)
st.write(DESCRIPTION)

# Prediction function
def predict(message):
    with st.status("Requesting Palm-2🌴..."):
        st.write("Requesting API...")
        response = bard.get_answer(message if not code_interpreter else message + "Rule 1: If User requires a code snippet, write each only one code snippet and only in that way that it would run in streamlit app, and but don't output anything if it requires some additional libraries.")
        st.write("Done...")
        
        st.write("Checking images...")
    for i in response['images']:
        st.image(i)
    
    return response

# Display chat messages from history on app rerun
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=("🧑‍💻" if message["role"] == 'human' else '🌴')):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask Palm 2 anything..."):
    st.chat_message("human", avatar="🧑‍💻").markdown(prompt)
    # st.session_state.messages.append({"role": "human", "content": prompt})

    response = predict(prompt)
    with st.chat_message("assistant", avatar='🌴'):
        st.markdown(response['content'])
    
    if response['code'] and code_interpreter:
        try:
            exec(response['code'])
        except Exception as e:
            st.write(f"ERROR {e}...")
    
    # st.session_state.messages.append({"role": "assistant", "content": response['content']})
