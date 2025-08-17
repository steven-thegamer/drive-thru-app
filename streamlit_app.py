import streamlit as st
import genai as gen

gen.initialize()

st.title("🍔🚗 Drive-Thru Chatbot")
st.write(
    "This is a chatbot prototype for restaurant drive-thru. "
    "This program uses a text input instead of audio input. "
    "This program also uses a local database instead of a remote database. "
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#tab1, tab2 = st.tabs(["Order Chatbot", "Order Database"])

with st.chat_message("assistant"):
    st.write("Welcome to McTexas! How can I help you today?")
st.session_state.messages.append({"role": "assistant", "content": "Welcome to McTexas! How can I help you today?"})


prompt = st.chat_input("Say something...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        response = gen.chat(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

#with tab2:
#    pass