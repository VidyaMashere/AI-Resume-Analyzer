
import streamlit as st
import os
import json
import time
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from google import genai

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f7f8fc;
}
.header-box {
    background: linear-gradient(120deg, #263b80, #7357c8);
    padding: 30px;
    border-radius: 15px;
    color: white;
    margin-bottom: 25px;
}
.header-box h1 {
    color: white;
}
.header-box p {
    color: #eeeeff;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-box">
    <h1>📄 AI Resume Analyzer</h1>
    <p>Analyze your resume, discover missing skills
    and improve your job opportunities with AI.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ About Project")
    st.write("AI-powered Resume Analysis System")
    st.write("**Problem Statement:** PS 41")
    st.write("**AI Model:** Google Gemini")
    st.write("**Framework:** Streamlit")
    st.write("**PDF Library:** PyPDF2")
    st.divider()
    st.info(
        "Upload your resume and provide a job "
        "description to get an AI-powered analysis."
    )

# User inputs
st.subheader("📌 Upload Your Details")

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"]
    )

with col2:
    job_description = st.text_area(
        "Paste the Job Description here",
        height=180,
        placeholder="Paste the complete job requirements..."
    )


# Function 1: Extract text from PDF
def extract_resume_text(pdf_file):

    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text.strip()


# Function 2: Analyze resume using Gemini AI
def analyze_resume(resume_text, job_description):

    client = genai.Client(api_key=API_KEY)

    prompt = f"""
You are an expert resume analysis assistant.

Compare the candidate's resume with the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON using this structure:

{{
    "match_score": 75,
    "matched_skills": ["Python", "HTML"],
    "missing_skills": ["React", "SQL"],
    "improvement_tips": [
        "Add relevant projects.",
        "Improve technical skills.",
        "Include measurable achievements."
    ],
    "summary": "Short resume analysis."
}}

Rules:
1. Match score must be between 0 and 100.
2. Identify skills using actual resume evidence.
3. Do not invent qualifications.
4. Give exactly three improvement tips.
5. Return JSON only.
"""

    # Maximum two attempts
    for attempt in range(2):

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            return json.loads(response.text)

        except Exception as e:

            error = str(e)

            if "503" in error or "UNAVAILABLE" in error:

                if attempt == 0:
                    time.sleep(2)
                    continue

                raise Exception(
                    "Gemini is temporarily busy. "
                    "Please try again after some time."
                )

            raise


# Analyze button
st.divider()

if st.button("✨ Analyze My Resume", use_container_width=True):

    if not API_KEY:
        st.error("Gemini API key not found. Check your .env file.")

    elif not resume_file:
        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:

        try:

            with st.spinner("🤖 AI is analyzing your resume..."):

                # Extract resume text
                resume_text = extract_resume_text(resume_file)

                if len(resume_text) < 50:
                    st.error(
                        "Could not extract enough text. "
                        "Please upload a text-based PDF resume."
                    )
                    st.stop()

                # Limit input to reduce processing time
                if len(resume_text) > 12000:
                    resume_text = resume_text[:12000]
                    st.warning(
                        "Long resume detected. "
                        "Only the first 12,000 characters will be analyzed."
                    )

                # Analyze with Gemini
                result = analyze_resume(
                    resume_text,
                    job_description
                )

                # Validate score
                score = int(result["match_score"])
                score = max(0, min(100, score))

            st.success("✅ Resume analysis completed!")

            # Results
            st.divider()
            st.header("📊 Resume Analysis Results")

            st.subheader("Resume Match Score")

            st.progress(score / 100)

            st.metric(
                label="Overall Match",
                value=f"{score}%"
            )

            # Skills
            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matched Skills")

                matched = result.get("matched_skills", [])

                if matched:
                    for skill in matched:
                        st.success(skill)
                else:
                    st.write("No matched skills identified.")

            with col2:
                st.subheader("❌ Missing Skills")

                missing = result.get("missing_skills", [])

                if missing:
                    for skill in missing:
                        st.error(skill)
                else:
                    st.write("No missing skills identified.")

            # Improvement tips
            st.divider()
            st.subheader("💡 Three Improvement Tips")

            tips = result.get("improvement_tips", [])

            for i, tip in enumerate(tips[:3], start=1):
                st.info(f"{i}. {tip}")

            # Summary
            st.divider()
            st.subheader("📝 AI Analysis Summary")

            summary = result.get("summary", "No summary available.")
            st.write(summary)

            # Download report
            report = f"""
AI RESUME ANALYZER REPORT

Overall Match Score: {score}%

MATCHED SKILLS:
{chr(10).join(matched)}

MISSING SKILLS:
{chr(10).join(missing)}

IMPROVEMENT TIPS:
{chr(10).join(tips[:3])}

SUMMARY:
{summary}

Note: This is an AI-generated advisory report,
not a guarantee of job selection.
"""

            st.download_button(
                label="⬇️ Download Analysis Report",
                data=report,
                file_name="Resume_Analysis_Report.txt",
                mime="text/plain",
                use_container_width=True
            )

        except json.JSONDecodeError:
            st.error(
                "AI returned an invalid response. Please try again."
            )

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")


# Footer
st.divider()

st.caption(
    "AI Resume Analyzer | PS 41 | "
    "Developed using Python, Streamlit and Google Gemini"
)
