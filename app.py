import streamlit as st
import json
import os
import requests
from bardapi import AsyncBard

# Load the GOOGLE_LANGUAGES_TO_CODES dictionary from lang.json
with open("lang.json", "r") as file:
    GOOGLE_LANGUAGES_TO_CODES = json.load(file)

with st.sidebar:
    # Add a selector in the sidebar using the dictionary's keys
    selected_language_name = st.sidebar.selectbox("Select Language", list(GOOGLE_LANGUAGES_TO_CODES.keys()))
    code_interpreter = st.sidebar.toggle("Code Interpreter", value=True)
    system_prompt = st.sidebar.text_input("System prompt for code interpreter", value = "Rule 1: If a user requests a code snippet, provide only one that can run in a Streamlit app without requiring additional libraries.")
    useSystemPrompt = st.sidebar.toggle("Use System prompt", value=True)
    exportToReplIt = st.sidebar.toggle("Export to repl.it", value=False)
    showImages = st.sidebar.toggle("Show images", value=True)
    
# Retrieve the corresponding language code from the dictionary
selected_language_code = GOOGLE_LANGUAGES_TO_CODES[selected_language_name]

# Initialize Bard with the selected language code
bard = AsyncBard(token=os.getenv("_BARD_API_KEY"), language=selected_language_code)

TITLE = "Palm 2🌴 Chatbot"
DESCRIPTION = """
"""

# Streamlit UI
st.title(TITLE)
st.write(DESCRIPTION)

# Prediction function
 async def predict(message):
    with st.status("Requesting Palm-2🌴..."):
        st.write("Requesting API...")
        response = await bard.get_answer(message if not (code_interpreter and useSystemPrompt) else message + system_prompt)
        st.write("Done...")
        
        st.write("Checking images...")
    if 'images' in response.keys() and showImages:
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
    st.session_state.messages.append({"role": "human", "content": prompt})

    response = predict(prompt)
    with st.chat_message("assistant", avatar='🌴'):
        st.markdown(response['content'])
    
    if response['code']:
        if exportToReplIt:
            with st.status("Exporting replit..."):
                fale = False
                try:
                    url = bard.export_replit(code=response['code'],program_lang=response['program_lang'])['url']
                except error:
                    fale=True
                    st.write('ERROR')
            if not fale:
                st.title('Export to repl.it')
                st.markdown(f'[link]({url})')
        if code_interpreter:
            try:
                exec(response['code'])
            except Exception as e:
                st.write(f"ERROR {e}...")
    
    st.session_state.messages.append({"role": "assistant", "content": response['content']})
