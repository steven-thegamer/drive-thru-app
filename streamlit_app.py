import streamlit as st
import genai as gen

gen.initialize()

st.title("🍔🚗 Drive-Thru Chatbot")
st.write(
    "This is a chatbot prototype for restaurant drive-thru. "
    "This program uses a text input instead of audio input. "
    "This program also uses a local database instead of a remote database. "
)
with st.chat_message("assistant"):
    st.write("Welcome to McTexas! How can I help you today?")
prompt = st.chat_input("Say something...")
if prompt:
    with st.chat_message("user"):
        st.write("Hello!")
    with st.chat_message("assistant"):
        response = gen.chat(prompt)
        st.write(response)