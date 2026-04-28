import streamlit as st
import requests
import time

st.set_page_config(page_title="Origin AI by Origin", layout="wide")

# ====== CONFIG ======
API_URL = "https://origin-ai.onrender.com"

# ====== STYLING ======
st.markdown("""
<style>
.chat-container {
    max-width: 800px;
    margin: auto;
}
.user-msg {
    background: #2563eb;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
    text-align: right;
}
.bot-msg {
    background: #111827;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
    text-align: left;
}
input {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ====== HEADER ======
st.title("🧠 Origin AI by Origin")
st.caption("Hello, I'm Origin AI — Origin's central intelligence. How can I help build the future today?")

# ====== MEMORY ======
if "messages" not in st.session_state:
    st.session_state.messages = []

# ====== CHAT DISPLAY ======
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ====== INPUT ======
user_input = st.chat_input("Ask Origin AI anything...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message instantly
    with chat_container:
        st.markdown(f'<div class="user-msg">{user_input}</div>', unsafe_allow_html=True)

    # Call backend
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": user_input}
        )

        bot_reply = response.json().get("response", "No response")

    except Exception as e:
        bot_reply = f"Error: {e}"

    # Simulate streaming
    streamed_text = ""
    placeholder = st.empty()

    for char in bot_reply:
        streamed_text += char
        placeholder.markdown(
            f'<div class="bot-msg">{streamed_text}</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.01)

    # Save bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
