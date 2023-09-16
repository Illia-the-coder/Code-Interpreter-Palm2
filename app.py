import streamlit as st
from bardapi import Bard
import os
import requests


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

bard = Bard(token=os.getenv("_BARD_API_KEY"), session=session)

TITLE = "Palm 2🌴 Chatbot"
DESCRIPTION = """
"""



# Prediction function
def predict(message):
    with st.status("Requesting Palm-2🌴..."):
        st.write("Requesting API...")
        response = bard.get_answer(message)
        st.write("Done...")
        
        st.write("Checking images...")
    for i in response['links']:
        st.image(i)
    return response['content']

# Streamlit UI
st.title(TITLE)
st.write(DESCRIPTION)


if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# React to user input
if prompt := st.chat_input("Ask Palm 2 anything..."):
    # Display user message in chat message container
    st.chat_message("human",avatar = "🧑‍💻").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "human", "content": prompt})

    response = predict(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar='🌴'):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
