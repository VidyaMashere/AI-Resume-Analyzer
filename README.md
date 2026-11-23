# AI Resume Analyzer

**Project:** PS 41 – AI Resume Analyzer

**Developed by:** VIDYA NILAKANTH MASHERE  
**College:** MIT ADT University, Loni Kalbhor

## About the Project

AI Resume Analyzer is an AI-powered application that analyzes a candidate's resume according to a given job description.

It uses Google Gemini AI to identify matching skills, missing skills, calculate a match score, and provide suggestions to improve the resume.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- PyPDF2
- python-dotenv

## Features

- Upload a resume in PDF format.
- Enter a job description.
- Extract text from the uploaded resume.
- Analyze the resume using Google Gemini AI.
- Display a resume match score.
- Identify matched and missing skills.
- Provide resume improvement suggestions.
- Generate a downloadable analysis report.

## How to Run the Project

1. Install Python.
2. Download or clone this repository.
3. Open the project folder in a terminal.
4. Install the required packages:

   `pip install -r requirements.txt`

5. Create a `.env` file in the project folder and add your Gemini API key:

   `GEMINI_API_KEY=your_api_key_here`

6. Run the application:

   `streamlit run app.py`

7. Open the local URL displayed in the terminal.

## Project Objective

The main objective is to help job seekers understand how well their resumes match a particular job description and identify areas for improvement.

## Note

A valid Google Gemini API key is required to use the AI analysis feature. Keep your API key private and never upload your `.env` file to GitHub.
