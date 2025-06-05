import pdfplumber
import google.generativeai as genai
import re
import json
from dotenv import load_dotenv
import os

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def parse_resume_with_gemini(resume_text):
    # Gemini config
    load_dotenv()
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY')) # replace with your key
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""
    You are an expert HR resume screener.

    Given the following resume text, extract the details and respond ONLY in valid JSON format without any explanation. 

    Return JSON with the following fields:
    - Name (string)
    - Skills (list of strings)
    - Projects (list of objects with 'title', 'description', 'technologies')
    - Work Experience (list of objects with 'job_title', 'company', 'duration')
    - Extra-curricular Activities (list of strings)
    - Education (string)

    Resume Text:
    {resume_text}
    """

    response = model.generate_content(prompt)
    response_text = response.text
    print("Gemini Raw Response:", response_text)

    # Extract JSON using regex
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if not json_match:
        print("No JSON found in Gemini response.")
        return None

    json_text = json_match.group(0)
    print("Extracted JSON Text:", json_text)

    try:
        parsed_json = json.loads(json_text)
        return parsed_json
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        return None
