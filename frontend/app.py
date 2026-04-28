import streamlit as st
import requests
import time
from gtts import gTTS
import tempfile

st.set_page_config(page_title="Origin AI by Origin", layout="wide")

API_URL = "https://origin-ai.onrender.com"

# ===== UI STYLE =====
st.markdown("""
<style>
.chat-container { max-width: 800px; margin: auto; }
.user-msg { background: #2563eb; color: white; padding: 12px; border-radius: 12px; margin: 10px 0; text-align: right; }
.bot-msg { background: #111827; color: white; padding: 12px; border-radius: 12px; margin: 10px 0; text-align: left; }
</style>
""", unsafe_allow_html=True)

st.title("Cypher")

# ===== MEMORY =====
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===== FILE UPLOAD =====
uploaded_file = st.file_uploader("📎 Upload file (PDF, image, code)", type=["pdf", "png", "jpg", "txt", "py"])

file_content = ""
if uploaded_file:
    try:
        file_content = uploaded_file.read().decode("utf-8", errors="ignore")
        st.success("File loaded successfully")
    except:
        st.warning("Binary file uploaded (image/PDF). Will send as-is.")

# ===== CHAT DISPLAY =====
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)

# ===== INPUT =====
user_input = st.chat_input("Ask Origin AI...")

col1, col2 = st.columns(2)

# ===== VOICE INPUT BUTTON =====
with col1:
    if st.button("🎤 Voice Input"):
        st.warning("Voice input works best locally (browser mic limitations on cloud)")

# ===== SEND =====
if user_input:
    full_input = user_input

    if file_content:
        full_input += f"\n\n[Attached File Content]\n{file_content[:3000]}"

    st.session_state.messages.append({"role": "user", "content": full_input})

    try:
        res = requests.post(
            f"{API_URL}/chat",
            json={"message": full_input}
        )
        reply = res.json().get("response", "No response")

    except Exception as e:
        reply = f"Error: {e}"

    # ===== STREAMING EFFECT =====
    streamed = ""
    placeholder = st.empty()

    for char in reply:
        streamed += char
        placeholder.markdown(f'<div class="bot-msg">{streamed}</div>', unsafe_allow_html=True)
        time.sleep(0.005)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    # ===== VOICE OUTPUT =====
    try:
        tts = gTTS(reply)
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)
        st.audio(temp_audio.name)
    except:
        pass
