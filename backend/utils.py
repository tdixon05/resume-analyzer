from PyPDF2 import PdfReader

def extract_text(file):
    pdf = PdfReader(file)
    return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
