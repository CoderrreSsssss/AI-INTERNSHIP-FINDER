import streamlit as st
import google.generativeai as genai

# Configure Page
st.set_page_config(
    page_title="AI Internship Finder",
    page_icon="🚀",
    layout="wide"
)

# Header
st.title("🚀 AI Internship Finder")
st.subheader("Get Internship Recommendations, Cold Emails & Learning Roadmap")

# Sidebar
st.sidebar.title("Settings")

api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password"
)

if api_key:
    genai.configure(api_key=api_key)

# User Inputs
name = st.text_input("Your Name")

degree = st.selectbox(
    "Degree",
    ["BCA", "B.Tech", "B.Sc", "MCA", "M.Tech"]
)

skills = st.text_area(
    "Enter Your Skills",
    placeholder="Python, HTML, CSS, JavaScript, SQL"
)

location = st.text_input(
    "Preferred Location",
    placeholder="Noida, Gurgaon, Remote"
)

experience = st.selectbox(
    "Experience Level",
    ["Fresher", "Beginner", "Intermediate"]
)

if st.button("Find My Internship 🚀"):

    if not api_key:
        st.error("Please enter Gemini API Key")
    else:

        prompt = f"""
        User Details:

        Name: {name}
        Degree: {degree}
        Skills: {skills}
        Preferred Location: {location}
        Experience: {experience}

        Act as a professional Career Counselor.

        Provide:

        1. Top 10 internship roles.
        2. Skills missing.
        3. Personalized recruiter cold email.
        4. 30-day roadmap.
        5. Resume summary.
        6. Career advice.

        Format beautifully.
        """

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")

            response = model.generate_content(prompt)

            st.success("Analysis Completed")

            st.markdown(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit & Gemini AI"
)
