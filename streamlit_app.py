import streamlit as st
import genai as gen
import pandas as pd
import database_tools as db_tools

st.title("🍔🚗 Drive-Thru Chatbot")
st.write(
    "This is a chatbot prototype for restaurant drive-thru. "
    "This program uses a text input instead of audio input. "
    "This program also uses a local database instead of a remote database. "
)

if st.session_state == {}:
    gen.initialize()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.header("Order Chatbot")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.messages) == 0:
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

st.header("Orders")
df = pd.DataFrame(db_tools.get_orders(), columns=["Order ID", "Customer", "Order Details"])
st.table(df)