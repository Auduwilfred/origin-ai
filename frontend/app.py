import streamlit as st
import requests
import time

st.set_page_config(page_title="Origin AI by Origin", layout="wide")

API_URL = "https://origin-ai.onrender.com"

# ===== SESSION =====
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ===== SIDEBAR (Gemini-style) =====
with st.sidebar:
    st.title("Cypher")

    if st.button("➕ New Chat"):
        st.session_state.messages = []

    st.markdown("---")

    st.subheader("History")
    for i, chat in enumerate(st.session_state.chat_history[-5:]):
        if st.button(chat[:30], key=f"chat_{i}"):
            st.session_state.messages = [{"role": "assistant", "content": chat}]

    st.markdown("---")

    st.subheader("Tools")

    tool = st.selectbox(
        "",
        [
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
        st.caption(f"{tool} mode selected")

# ===== MAIN CHAT AREA =====
st.title("")

chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ===== SUGGESTIONS (Gemini-like) =====
if not st.session_state.messages:
    st.markdown("### Suggestions")
    cols = st.columns(3)

    suggestions = [
        "Build a fintech SaaS",
        "Explain this code",
        "Design system architecture",
        "Create mobile app UI",
        "Optimize backend performance",
        "Act as CTO"
    ]

    for i, suggestion in enumerate(suggestions):
        if cols[i % 3].button(suggestion):
            st.session_state.messages.append(
                {"role": "user", "content": suggestion}
            )

# ===== INPUT BAR (BOTTOM) =====
st.markdown("---")

col1, col2, col3, col4 = st.columns([1, 8, 1, 1])

# ➕ MENU
with col1:
    with st.popover("➕"):
        st.write("### Add to chat")

        st.file_uploader("📁 Files")
        st.button("📷 Camera")
        st.button("🖼 Photos")
        st.button("🎨 Create Image")
        st.button("🧠 Thinking")
        st.button("🔬 Deep Research")
        st.button("🌐 Web Search")
        st.button("🧩 Quizzes")
        st.button("🧭 Explore Apps")
        st.button("⚙️ Features")

# INPUT
with col2:
    user_input = st.text_input(
        "Ask Origin AI...",
        label_visibility="collapsed"
    )

# 🎤 VOICE
with col3:
    if st.button("🎤"):
        st.warning("Voice coming soon")

# SEND
with col4:
    send = st.button("➤")

# ===== SEND LOGIC =====
if send and user_input:
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
    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed = ""

        for char in reply:
            streamed += char
            placeholder.markdown(streamed)
            time.sleep(0.005)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    st.session_state.chat_history.append(user_input)
