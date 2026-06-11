import streamlit as st
import google.generativeai as genai
import os
from pypdf import PdfReader

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="AI Intern Pro",
    page_icon="🤖",
    layout="wide"
)

# --------------------
# CUSTOM CSS
# --------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
}

h1, h2, h3 {
    color: #00E5FF;
}

.stButton > button {
    background-color: #00E5FF;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}

div[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------
# GEMINI API
# --------------------

# For local testing use:
# api_key = "YOUR_GEMINI_API_KEY"

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning("Please configure GEMINI_API_KEY")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# --------------------
# HEADER
# --------------------

st.title("🤖 AI Intern Pro")
st.subheader("Your Personal AI Assistant")

st.markdown("---")

# --------------------
# METRICS
# --------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Features", "6")

with col2:
    st.metric("AI Model", "Gemini")

with col3:
    st.metric("Version", "1.0")

# --------------------
# SIDEBAR
# --------------------

feature = st.sidebar.selectbox(
    "Choose Feature",
    [
        "AI Chat",
        "Content Drafting",
        "Summarization",
        "Task Extraction",
        "PDF Q&A"
    ]
)

# --------------------
# AI CHAT
# --------------------

if feature == "AI Chat":

    st.header("💬 AI Chat")

    user_query = st.text_area(
        "Ask anything"
    )

    if st.button("Send"):

        response = model.generate_content(
            user_query
        )

        st.markdown(response.text)

# --------------------
# CONTENT DRAFTING
# --------------------

elif feature == "Content Drafting":

    st.header("📝 Content Drafting")

    prompt = st.text_area(
        "Describe what you want"
    )

    if st.button("Generate Draft"):

        response = model.generate_content(
            f"""
            Write professional content for:

            {prompt}
            """
        )

        st.markdown(response.text)

# --------------------
# SUMMARIZATION
# --------------------

elif feature == "Summarization":

    st.header("📄 Summarizer")

    long_text = st.text_area(
        "Paste text here"
    )

    if st.button("Summarize"):

        response = model.generate_content(
            f"""
            Summarize this:

            {long_text}
            """
        )

        st.markdown(response.text)

# --------------------
# TASK EXTRACTION
# --------------------

elif feature == "Task Extraction":

    st.header("✅ Task Extractor")

    meeting_notes = st.text_area(
        "Paste meeting notes"
    )

    if st.button("Extract Tasks"):

        response = model.generate_content(
            f"""
            Extract tasks.

            Give:
            - Task
            - Priority
            - Deadline

            Notes:

            {meeting_notes}
            """
        )

        st.markdown(response.text)

# --------------------
# PDF Q&A
# --------------------

elif feature == "PDF Q&A":

    st.header("📚 PDF Question Answering")

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    question = st.text_input(
        "Ask Question"
    )

    if uploaded_pdf:

        reader = PdfReader(uploaded_pdf)

        pdf_text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                pdf_text += page_text

        st.success("PDF Loaded Successfully")

        if st.button("Answer Question"):

            prompt = f"""
            Answer ONLY from the document.

            DOCUMENT:

            {pdf_text[:15000]}

            QUESTION:

            {question}
            """

            response = model.generate_content(
                prompt
            )

            st.markdown(response.text)

# --------------------
# FOOTER
# --------------------

st.markdown("---")
st.caption("🚀 Built using Streamlit + Gemini AI")
