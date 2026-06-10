import streamlit as st
import google.generativeai as genai
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Internship Finder",
    page_icon="🚀",
    layout="wide"
)

# =========================
# GEMINI CONFIGURATION
# =========================
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# =========================
# HEADER
# =========================
st.title("🚀 AI Internship Finder")
st.markdown("### Find suitable internships, get recruiter emails, resume summaries, and a learning roadmap.")

st.markdown("---")

# =========================
# USER INPUTS
# =========================
name = st.text_input("👤 Full Name")

degree = st.selectbox(
    "🎓 Degree",
    [
        "BCA",
        "B.Tech",
        "B.Sc",
        "MCA",
        "M.Tech",
        "Other"
    ]
)

skills = st.text_area(
    "💻 Skills",
    placeholder="Python, Java, HTML, CSS, JavaScript, SQL, AI, Machine Learning"
)

location = st.text_input(
    "📍 Preferred Location",
    placeholder="Noida, Gurgaon, Delhi, Remote"
)

experience = st.selectbox(
    "📈 Experience Level",
    [
        "Fresher",
        "Beginner",
        "Intermediate"
    ]
)

career_interest = st.selectbox(
    "🎯 Career Interest",
    [
        "Software Development",
        "Web Development",
        "Data Science",
        "Artificial Intelligence",
        "Cyber Security",
        "Cloud Computing",
        "Mobile App Development"
    ]
)

# =========================
# BUTTON
# =========================
if st.button("🚀 Analyze My Profile"):

    if not api_key:
        st.error("GEMINI_API_KEY is not configured.")
    elif not skills:
        st.warning("Please enter your skills.")
    else:

        prompt = f"""
        You are an expert career counselor.

        Candidate Details:

        Name: {name}
        Degree: {degree}
        Skills: {skills}
        Preferred Location: {location}
        Experience Level: {experience}
        Career Interest: {career_interest}

        Generate a professional report with the following sections:

        1. Profile Analysis

        2. Top 10 Recommended Internship Roles

        3. Missing Skills To Learn

        4. Personalized Recruiter Cold Email

        5. Professional Resume Summary

        6. 30-Day Learning Roadmap

        7. Career Advice

        Use headings and bullet points.
        """

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")

            response = model.generate_content(prompt)

            st.success("Analysis Generated Successfully!")

            st.markdown(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Built with Python, Streamlit, and Gemini AI")
