import streamlit as st
from recorder import Recorder
from transcriber import transcribe_audio
from summarizer import summarize_text

st.title("🎤 Live Conversation Summarizer")

# Session state
if "recorder" not in st.session_state:
    st.session_state.recorder = Recorder()

if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

if "conversation" not in st.session_state:
    st.session_state.conversation = ""

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Start Recording"):
        st.session_state.recorder.start()
        st.session_state.is_recording = True
        st.success("🎤 Recording started")

with col2:
    if st.button("⏹️ Stop Recording"):
        file_path = st.session_state.recorder.stop()
        st.session_state.is_recording = False
        st.success("🛑 Recording stopped")

        # Transcribe
        with st.spinner("Transcribing..."):
            text = transcribe_audio(file_path)
            st.session_state.conversation = text

# Show conversation
if st.session_state.conversation:
    st.subheader("📜 Conversation")
    st.write(st.session_state.conversation)

    # Summary
    if st.button("🧠 Generate Summary"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(st.session_state.conversation)

        st.subheader("📝 Summary")
        st.write(summary)