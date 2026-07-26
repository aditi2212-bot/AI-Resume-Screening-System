import os
from PyPDF2 import PdfReader
from docx import Document

def extract_text(file_path):
    """
    Extract text from PDF or DOCX files.
    """

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = ""

        for para in doc.paragraphs:
            text += para.text + "\n"

        return text

    else:
        raise ValueError("Unsupported file format")

# Test the parser
from skill_extractor import extract_skills

if __name__ == "__main__":
    resume_path = "data/resumes/resume.pdf"

    extracted_text = extract_text(resume_path)

    print("\nResume Text:\n")
    print(extracted_text)

    skills = extract_skills(extracted_text)

    print("\nExtracted Skills:\n")

    for skill in skills:
        print("-", skill)