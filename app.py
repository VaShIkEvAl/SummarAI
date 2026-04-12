import streamlit as st
import streamlit.components.v1 as components
from services.gemini_service import generate_summary
from utils.text_loader import load_text_from_file

st.set_page_config(page_title="SummarAI", page_icon="🧠", layout="wide")

# ---------------- SESSION STATE ----------------
if "summary" not in st.session_state:
    st.session_state.summary = ""

# ---------------- LOAD CSS ----------------
def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- UI HEADER ----------------
st.markdown('<div class="main-title">🧠 SummarAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-powered Chat Summarizer</div>', unsafe_allow_html=True)

# ---------------- INPUT SECTION ----------------
st.markdown("## 📥 Input Chat")

text_input = st.text_area("Paste your chat here:", height=250)

uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])

chat_text = ""

if uploaded_file is not None:
    st.info("📂 Uploaded file detected. Processing...")
    print("📂 Uploaded file detected in UI")
    chat_text = load_text_from_file(uploaded_file)

elif text_input:
    chat_text = text_input

# ---------------- GENERATE SUMMARY ----------------
if st.button("🚀 Generate Summary"):
    if not chat_text.strip():
        st.warning("Please provide input text.")
    else:
        st.info("🤖 Sending data to Gemini...")
        print("🤖 Sending data to Gemini...")

        with st.spinner("Generating summary..."):
            st.session_state.summary = generate_summary(chat_text)

        st.success("✅ Summary generated!")

# ---------------- DISPLAY SUMMARY ----------------
summary = st.session_state.summary

if summary:
    st.markdown("## 📄 Summary")

    col1, col2 = st.columns([1, 1])

    # LEFT → Copy section title
    with col1:
        st.markdown("### 📋 Copy Summary")

    # RIGHT → Download button
    with col2:
        st.download_button(
            label="⬇️ Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain"
        )

    # Wrapped text display
    st.text_area(
        label="Summary Output",
        value=summary,
        height=200,
        label_visibility="collapsed"
    )

    # ---------------- COPY TO CLIPBOARD BUTTON ----------------
    copy_button_html = f"""
    <div style="margin-top:10px;">
        <button onclick="navigator.clipboard.writeText(`{summary}`)" 
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
    """

    components.html(copy_button_html, height=60)