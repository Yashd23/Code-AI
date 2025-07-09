import streamlit as st

def store_message(role, content):
    st.session_state['chat_history'].append({"role": role, "content": content})

def get_history():
    return st.session_state['chat_history'] 