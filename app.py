import streamlit as st
import streamlit.components.v1 as components
from services.gemini_service import generate_summary
from utils.text_loader import load_text_from_file
import json
import re
from audio_processing.recorder import Recorder
from audio_processing.transcriber import transcribe_audio
import os

def render_copy_button(text, key):
    safe_text = get_safe_text(text)

    copy_html = f"""
    <button id="copyBtn_{key}" onclick="copyText_{key}()" 
    style="
        background-color:#4CAF50;
        color:white;
        padding:6px 12px;
        border:none;
        border-radius:6px;
        cursor:pointer;
    ">
        📋
    </button>

    <script>
    function copyText_{key}() {{
        const text = {safe_text};
        const btn = document.getElementById("copyBtn_{key}");

        navigator.clipboard.writeText(text).then(function() {{
            btn.innerText = "✅";
            btn.style.backgroundColor = "#2ecc71";

            setTimeout(() => {{
                btn.innerText = "📋";
                btn.style.backgroundColor = "#4CAF50";
            }}, 1500);
        }});
    }}
    </script>
    """

    components.html(copy_html, height=40)

def get_safe_text(text):
    return json.dumps(text)

st.set_page_config(page_title="SummarAI", page_icon="🧠", layout="wide")

# ---------------- SESSION STATE ----------------
if "summary_data" not in st.session_state:
    st.session_state.summary_data = {}

if "recorder" not in st.session_state:
    st.session_state.recorder = Recorder()

if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

if "chat_text" not in st.session_state:
    st.session_state.chat_text = ""

# ---------------- LOAD CSS ----------------
def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- UI HEADER ----------------
st.markdown('<div class="main-title">🧠 SummarAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-powered Chat Summarizer</div>', unsafe_allow_html=True)

# ---------------- INPUT SECTION ----------------
st.markdown("## 🎤 Record Conversation")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎙️ Start Recording"):
        if not st.session_state.is_recording:
            st.session_state.recorder.start()
            st.session_state.is_recording = True
            st.success("🎙️ Recording started...")
        else:
            st.warning("Already recording!")

with col2:
    if st.button("⏹️ Stop Recording"):
        if st.session_state.is_recording:
            file_path = st.session_state.recorder.stop()
            st.session_state.is_recording = False
            st.info("🛑 Recording stopped. Transcribing...")

            # 🔥 Transcription
            with st.spinner("Converting speech to text..."):
                transcribed_text = transcribe_audio(file_path)

            # 🔥 Inject into chat input
            chat_text = transcribed_text

            st.session_state.chat_text = transcribed_text
            st.session_state.transcribed_text = transcribed_text

            st.success("✅ Transcription complete!")
        else:
            st.warning("Not recording!")

st.markdown("## 📥 Input Chat")
text_input = st.text_area(
    "Paste your chat here:",
    key="chat_text",
    height=250
)

# 🔥 Sync user edits
# st.session_state.chat_text = text_input

uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])

chat_text = st.session_state.get("chat_text", "")

if uploaded_file is not None:
    st.info("📂 Uploaded file detected. Processing...")
    print("📂 Uploaded file detected in UI")
    chat_text = load_text_from_file(uploaded_file)
elif text_input and not st.session_state.is_recording:
    chat_text = text_input

# ---------------- ALWAYS SHOW TRANSCRIPTION ----------------
if st.session_state.transcribed_text:
    st.subheader("Transcribed Text:")

    st.text_area(
        "",
        st.session_state.transcribed_text,
        height=200,
        key="persistent_transcription"
    )

    col1, col2 = st.columns(2)

    # Copy button
    with col1:
        render_copy_button(st.session_state.transcribed_text, "transcription")

    # Download text
    with col2:
        st.download_button(
            "⬇️ Download Text",
            st.session_state.transcribed_text,
            "transcription.txt"
        )

# ---------------- GENERATE SUMMARY ----------------
if st.button("🚀 Generate Summary"):
    final_text = st.session_state.chat_text

    if not final_text.strip():
        st.warning("Please provide input text.")
    else:
        st.info("🤖 Sending data to Gemini...")
        print("🤖 Sending data to Gemini...")

        with st.spinner("Generating summary..."):
            st.session_state.summary_data = generate_summary(final_text)

        st.success("✅ Summary generated!")

# ---------------- DISPLAY SUMMARY ----------------
data = st.session_state.summary_data
summary_text = data.get("summary", "")
key_points = data.get("key_points", [])
action_items = data.get("action_items", [])


full_output = f"""Summary:
{summary_text}

Key Points:
""" + "\n".join(f"- {kp}" for kp in key_points) + f"""

Action Items:
""" + "\n".join(f"- {ai}" for ai in action_items)

def copy_to_clipboard(text, label):
    st.code(text, language="text")
    st.toast(f"✅ {label} copied! (Use Ctrl+C)", icon="📋")

def clean_filename(text):
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = text.replace(" ", "_")
    return text[:50]

if data:
    title = data.get("title", "summary")

    file_name = f"{clean_filename(title)}_summary.txt"

    # Prepare safe text
    safe_summary = get_safe_text(summary_text)

    # HEADER ROW
    col1, col2 = st.columns([6, 2])

    with col1:
        st.markdown("## 📄 Summary")

    with col2:
        btn1, btn2 = st.columns(2)

        # Copy button (JS)
        with btn1:
            render_copy_button(summary_text, "summary")

        # Download button
        with btn2:
            st.download_button(
                label="⬇️ Download",
                data=full_output,
                file_name=file_name,
                mime="text/plain"
            )

    # CONTENT
    st.markdown(summary_text)

    # st.markdown("## 📌 Key Points")

    key_points_text = "\n".join(f"- {kp}" for kp in key_points)

    safe_kp = get_safe_text(key_points_text)

    col1, col2 = st.columns([6, 2])

    with col1:
        st.markdown("## 📌 Key Points")

    with col2:
        render_copy_button(key_points_text, "kp")

    # CONTENT
    if key_points:
        st.markdown(key_points_text)
    else:
        st.info("No key points found.")

    # st.markdown("## ✅ Action Items")

    action_items_text = "\n".join(f"- {ai}" for ai in action_items)

    safe_ai = get_safe_text(action_items_text)

    col1, col2 = st.columns([6, 2])

    with col1:
        st.markdown("## ✅ Action Items")

    with col2:
        render_copy_button(action_items_text, "ai")

    # CONTENT
    if action_items:
        st.markdown(action_items_text)
    else:
        st.info("No action items found.")

    # ---------------- COPY TO CLIPBOARD BUTTON ----------------
    safe_text = json.dumps(full_output)

    copy_button_html = f"""
    <div style="margin-top:10px;">
        <button id="copyBtn" onclick="copyText()" 
        style="
            background-color:#4CAF50;
            color:white;
            padding:10px 20px;
            border:none;
            border-radius:6px;
            cursor:pointer;
            font-size:15px;
        ">
            📋 Copy to Clipboard
        </button>
    </div>

    <script>
    function copyText() {{
        const text = {safe_text};
        const btn = document.getElementById("copyBtn");  // ✅ FIX

        navigator.clipboard.writeText(text).then(function() {{
            btn.innerText = "✅ Copied";
            btn.style.backgroundColor = "#2ecc71";

            setTimeout(() => {{
                btn.innerText = "📋 Copy to Clipboard";
                btn.style.backgroundColor = "#4CAF50";
            }}, 1500);
        }});
    }}
    </script>
    """

    components.html(copy_button_html, height=60)