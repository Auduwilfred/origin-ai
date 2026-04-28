import streamlit as st
import requests
import time

st.set_page_config(page_title="Origin AI by Origin", layout="wide")

API_URL = "https://origin-ai.onrender.com"

# ===== STYLE =====
st.markdown("""
<style>
.chat-container { max-width: 800px; margin: auto; }
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
.action-bar {
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Cypher")

# ===== SESSION =====
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===== DISPLAY CHAT =====
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)

# ===== ACTION BAR =====
col1, col2, col3 = st.columns([1, 6, 1])

# ➕ LEFT MENU
with col1:
    with st.expander("➕"):
        st.write("### Tools")
        tool = st.selectbox(
            "Choose action",
            [
                "Camera",
                "Photos",
                "Files",
                "Create Image",
                "Thinking",
                "Deep Research",
                "Web Search",
                "Quizzes",
                "Explore Apps",
                "Features"
            ]
        )

        if tool:
            st.info(f"{tool} selected")

# 💬 INPUT CENTER
with col2:
    user_input = st.text_input("Ask Origin AI...", label_visibility="collapsed")

# 🎤 RIGHT SIDE
with col3:
    if st.button("🎤"):
        st.warning("Voice input coming soon (browser mic limitations on Streamlit Cloud)")

# ===== SEND BUTTON =====
if st.button("Send") and user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        res = requests.post(
            f"{API_URL}/chat",
            json={"message": user_input}
        )
        reply = res.json().get("response", "No response")

    except Exception as e:
        reply = f"Error: {e}"

    # Streaming effect
    streamed = ""
    placeholder = st.empty()

    for char in reply:
        streamed += char
        placeholder.markdown(
            f'<div class="bot-msg">{streamed}</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.005)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
