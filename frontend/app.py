import streamlit as st
import requests
import time

API_URL = "https://origin-ai.onrender.com"

st.set_page_config(page_title="Cypher by Origin", layout="wide")

# ===== SIDEBAR =====
with st.sidebar:
    st.title("Cypher")

    if st.button("➕ New Chat"):
        st.session_state.messages = []

    st.markdown("---")

    tool = st.selectbox("Tools", [
        "Normal Chat",
        "Code Generator",
        "Web Search",
        "Analyze File",
        "Thinking Mode"
    ])

# ===== STATE =====
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===== CHAT DISPLAY =====
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===== INPUT =====
user_input = st.chat_input("Ask Cypher...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed = ""

        try:
            res = requests.post(
                f"{API_URL}/chat",
                json={
                    "message": user_input,
                    "tool": tool
                }
            )

            reply = res.json().get("response", "")

        except Exception as e:
            reply = f"Error: {e}"

        for char in reply:
            streamed += char
            placeholder.markdown(streamed)
            time.sleep(0.003)

    st.session_state.messages.append({"role": "assistant", "content": reply})
