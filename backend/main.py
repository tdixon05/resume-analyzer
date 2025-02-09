from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from docx import Document
import openai
import os
from dotenv import load_dotenv

# Load API keys securely
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Extract text from PDFs and DOCX files
def extract_text(file, content_type):
    if content_type == "application/pdf":
        try:
            pdf = PdfReader(file)
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            return text if text.strip() else "No readable text found."
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid PDF format: {str(e)}")

    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            doc = Document(file)
            text = "\n".join([para.text for para in doc.paragraphs if para.text])
            return text if text.strip() else "No readable text found."
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid DOCX format: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are allowed.")

# ✅ Resume Analysis API
@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...), job_desc: str = Form(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    if not job_desc:
        raise HTTPException(status_code=400, detail="Job description is missing.")

    text = extract_text(file.file, file.content_type)

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
