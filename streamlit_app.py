import streamlit as st
import genai as gen

gen.initialize()

st.title("🎈 Drive-Thru Chatbot")
st.write(
    "This is a chatbot prototype for restaurant drive-thru. "
    "This program uses a text input instead of audio input. "
)
with st.chat_message("user"):
    st.write("Hello!")
prompt = st.chat_input("Say something...")
if prompt:
    st.write(prompt)