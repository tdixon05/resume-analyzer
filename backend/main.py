from fastapi import FastAPI, File, UploadFile, HTTPException
from PyPDF2 import PdfReader
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extract_text(file):
    pdf = PdfReader(file)
    return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...), job_desc: str = ""):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files allowed.")

    text = extract_text(file.file)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Compare this resume: {text} with this job description: {job_desc}. Score it from 0-100."}],
        api_key=OPENAI_API_KEY
    )

    return {"score": response["choices"][0]["message"]["content"]}
