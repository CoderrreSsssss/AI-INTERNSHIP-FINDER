import streamlit as st
import google.generativeai as genai
import os
from pypdf import PdfReader
from duckduckgo_search import DDGS

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="AI Intern MVP",
    page_icon="🤖",
    layout="wide"
)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not configured")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# MEMORY
# =========================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🤖 AI Intern")

feature = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Chat",
        "Content Drafting",
        "Summarization",
        "Task Extraction",
        "PDF Q&A",
        "Web Search"
    ]
)

# =========================
# TITLE
# =========================

st.title("🤖 AI Intern MVP")

# =========================
# CHAT
# =========================

if feature == "Chat":

    user_input = st.text_area("Ask Anything")

    if st.button("Send"):

        prompt = f"""
        Chat History:
        {st.session_state.chat_history}

        User:
        {user_input}
        """

        response = model.generate_content(prompt)

        st.session_state.chat_history.append(
            {"user": user_input}
        )

        st.session_state.chat_history.append(
            {"assistant": response.text}
        )

        st.markdown(response.text)

# =========================
# CONTENT DRAFTING
# =========================

elif feature == "Content Drafting":

    draft_prompt = st.text_area(
        "What do you want drafted?"
    )

    if st.button("Generate Draft"):

        prompt = f"""
        Create professional content.

        Request:
        {draft_prompt}
        """

        response = model.generate_content(prompt)

        st.markdown(response.text)

# =========================
# SUMMARIZATION
# =========================

elif feature == "Summarization":

    text = st.text_area(
        "Paste Long Text"
    )

    if st.button("Summarize"):

        prompt = f"""
        Summarize this text.

        {text}
        """

        response = model.generate_content(prompt)

        st.markdown(response.text)

# =========================
# TASK EXTRACTION
# =========================

elif feature == "Task Extraction":

    text = st.text_area(
        "Paste Meeting Notes"
    )

    if st.button("Extract Tasks"):

        prompt = f"""
        Extract actionable tasks.

        Give:

        - Task
        - Priority
        - Deadline if found

        Text:
        {text}
        """

        response = model.generate_content(prompt)

        st.markdown(response.text)

# =========================
# PDF Q&A
# =========================

elif feature == "PDF Q&A":

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    question = st.text_input(
        "Ask Question"
    )

    if uploaded_file:

        pdf = PdfReader(uploaded_file)

        text = ""

        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

        st.success("PDF Loaded")

        if st.button("Answer Question"):

            prompt = f"""
            Answer ONLY from this document.

            Document:
            {text[:15000]}

            Question:
            {question}
            """

            response = model.generate_content(prompt)

            st.markdown(response.text)

# =========================
# WEB SEARCH
# =========================

elif feature == "Web Search":

    query = st.text_input(
        "Search Internet"
    )

    if st.button("Search"):

        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    query,
                    max_results=5
                )
            )

        context = ""

        for r in results:
            context += (
                r["title"] + "\n" +
                r["body"] + "\n\n"
            )

        prompt = f"""
        Use these search results.

        {context}

        Give concise answer.
        """

        response = model.generate_content(prompt)

        st.markdown(response.text)

        with st.expander("Sources"):

            for r in results:

                st.write(r["title"])

                st.write(r["href"])

                st.divider()
