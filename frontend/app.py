import streamlit as st
import requests

st.set_page_config(page_title="Origin AI by Origin")

st.title("🧠 Origin AI by Origin")
st.write("Hello, I'm Origin AI — Origin's central intelligence. How can I help build the future today?")

API_URL = "https://origin-ai.onrender.com"

user_input = st.text_input("Ask Origin AI:")

if st.button("Send") and user_input:
    try:
        res = requests.post(f"{API_URL}/chat", json={"message": user_input})
        st.write(res.json().get("response", "No response"))
    except Exception as e:
        st.error(f"Error: {e}")
