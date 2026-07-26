# AI-Resume-Screening-System

AI Resume Screening System
Overview

The AI Resume Screening System is an intelligent recruitment assistant that compares resumes with job descriptions using Natural Language Processing (NLP) and AI.

The application extracts text from resumes, identifies relevant technical skills, calculates keyword matching, computes semantic similarity using Sentence Transformers, and generates an interactive screening report through a modern Streamlit dashboard.

 # Features
  - Upload Resume (PDF/DOCX)
  - Upload Job Description (TXT/PDF/DOCX)
  - Automatic Resume Parsing
  - Technical Skill Extraction
  - Keyword Match Percentage
  - AI Semantic Similarity Score
  - Interactive Dashboard
  - Skill Match Visualization
  - Resume Recommendation
  - Download Screening Report

 # Technologies Used
   - Python
   - Streamlit
   - Sentence Transformers
   - Scikit-learn
   - PyPDF2
   - python-docx
   - Plotly
   - Pandas

     
 ## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/AI-Resume-Screening-System.git
cd AI-Resume-Screening-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

### 4. Open your browser

Visit:

```
http://localhost:8501
```

### 5. Upload

- Job Description (.txt/.pdf/.docx)
- Resume (.pdf/.docx)

Click **Analyze** to view the AI screening report.
