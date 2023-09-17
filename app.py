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

# Set up the sidebar with language selection and code interpreter checkbox
selected_language_name = st.sidebar.selectbox(
    "Select Language", list(GOOGLE_LANGUAGES_TO_CODES.keys()), index=0
)
code_interpreter = st.sidebar.checkbox("Code Interpreter", value=True)

# Retrieve the corresponding language code from the dictionary
selected_language_code = GOOGLE_LANGUAGES_TO_CODES[selected_language_name]

# Initialize Bard with the selected language code
bard = Bard(
    token=os.getenv("_BARD_API_KEY"),
    language=selected_language_code,
    session=session,
    timeout=30,
)

TITLE = "Palm 2🌴 Chatbot"
DESCRIPTION = """
"""

# Streamlit UI
st.title(TITLE)
st.write(DESCRIPTION)

# Prediction function
def predict(message):
    with st.spinner("Requesting Palm-2🌴..."):
        st.write("Requesting API...")
        response = bard.get_answer(
            message if not code_interpreter else message + " Rule 1: If User requires a code snippet, write only one code snippet that would run in the Streamlit app without requiring additional libraries."
        )
        st.write("Done...")

        if "images" in response:
            st.write("Checking images...")
            for i in response["images"]:
                st.image(i)

        return response

# Create a class to handle the chat messages
class ChatMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def display(self):
        if self.role == "human":
            st.text(self.content)
        else:
            with st.echo():
                exec(self.content)

# Display chat messages from history on app rerun
st.session_state.messages = st.session_state.get("messages", [])

for message in st.session_state.messages:
    chat_message = ChatMessage(message["role"], message["content"])
    chat_message.display()

# React to user input
if prompt := st.text_input("Ask Palm 2 anything..."):
    chat_message = ChatMessage("human", prompt)
    chat_message.display()

    response = predict(prompt)
    chat_message = ChatMessage("assistant", response["content"])
    chat_message.display()

    if response.get("code"):
        with st.spinner("Exporting to repl.it..."):
            url = bard.export_replit(
                code=response["code"], program_lang=response["program_lang"]
            )["url"]
        st.title("Export to repl.it")
        st.markdown(f"[link]({url})")
        if code_interpreter:
            try:
                exec(response["code"])
            except Exception as e:
                st.error(f"Error: {e}")

    # Append chat messages to the session state
    st.session_state.messages.append(
        {"role": "human", "content": prompt},
        {"role": "assistant", "content": response["content"]},
    )