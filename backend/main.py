from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from docx import Document
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing! Check your .env file.")

# ✅ Initialize OpenAI client
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# ✅ Enable CORS for frontend
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

    prompt = f"""
    Analyze this resume against the job description. Provide:
    1. A score from 0-100.
    2. Strengths of the resume.
    3. Weaknesses and areas for improvement.
    4. List of missing skills.
    5. Suggested improvements to make the resume stronger.

    Resume: {text}
    Job Description: {job_desc}
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        analysis_text = response.choices[0].message.content.strip().split("\n")

        return {
            "score": analysis_text[0],  
            "strengths": analysis_text[1],  
            "weaknesses": analysis_text[2],
            "missing_skills": analysis_text[3],
            "improvements": analysis_text[4]    
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
