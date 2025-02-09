from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
import openai
import os
from dotenv import load_dotenv

# Load API keys securely
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# ✅ FIXED: Enable CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ✅ Extract text from PDF resumes
def extract_text_from_pdf(file):
    try:
        pdf = PdfReader(file)
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return text if text.strip() else "No readable text found."
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid PDF format: {str(e)}")

# ✅ Resume Analysis API
@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...), job_desc: str = Form(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are allowed.")

    text = extract_text_from_pdf(file.file)

    prompt = f"Compare this resume: {text} with this job description: {job_desc}. Score it from 0-100 and provide feedback."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            api_key=OPENAI_API_KEY
        )
        return {"score": response["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")
