import streamlit as st
import tempfile
import os
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from PyPDF2 import PdfReader
from docx import Document

from resume_parser import extract_text
from skill_extractor import extract_skills
from similarity import calculate_similarity

#  PAGE SETTINGS

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)
#  CUSTOM CSS FOR A MORE ATTRACTIVE UI

st.markdown("""
<style>
    .main-header {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #6B7280;
        font-size: 1.05rem;
        margin-top: -8px;
    }
     div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
     div[data-testid="stMetric"] label {
    font-weight: 600;
    color: #374151 !important;
    }
      div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #111827 !important;
    }
      div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
    color: #111827 !important;
    }
    }
    .skill-pill {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .pill-match {
        background-color: #DCFCE7;
        color: #166534;
        border: 1px solid #86EFAC;
    }
    .pill-missing {
        background-color: #FEE2E2;
        color: #991B1B;
        border: 1px solid #FCA5A5;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 700;
        padding: 0.6rem 1.4rem;
        background: linear-gradient(90deg, #4F46E5, #06B6D4);
        color: white;
        border: none;
    }
    .stButton>button:hover {
        opacity: 0.9;
        color: white;
    }
    section[data-testid="stSidebar"] {
        background-color: #0E1117;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📄 AI Resume Screening System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload a Job Description and a Resume to get an instant, AI-powered screening report.</div>', unsafe_allow_html=True)
st.write("")

#  FUNCTION TO READ JOB DESCRIPTION

def read_job_description(uploaded_file):

    extension = uploaded_file.name.split(".")[-1].lower()

    if extension == "txt":
        return uploaded_file.read().decode("utf-8")

    elif extension == "pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text

    elif extension == "docx":
        doc = Document(uploaded_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    else:
        return ""


def make_gauge(value, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': "%", 'font': {'size': 34}},
        title={'text': title, 'font': {'size': 16}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#E5E7EB",
            'steps': [
                {'range': [0, 40], 'color': '#FEE2E2'},
                {'range': [40, 60], 'color': '#FEF3C7'},
                {'range': [60, 80], 'color': '#DBEAFE'},
                {'range': [80, 100], 'color': '#DCFCE7'},
            ],
        }
    ))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=10))
    return fig


#  SIDEBAR — FILE UPLOAD

with st.sidebar:
    st.header("📁 Upload Files")

    job_description = st.file_uploader(
        "Job Description",
        type=["txt", "pdf", "docx"],
        help="Upload the job description as .txt, .pdf, or .docx"
    )

    resume = st.file_uploader(
        "Resume / CV",
        type=["pdf", "docx", "csv"],
        help="Upload the candidate's resume as .pdf, .docx, or .csv"
    )

    st.write("")
    analyze_clicked = st.button("🚀 Analyze Resume", use_container_width=True)

    st.write("---")
    st.caption("💡 Tip: results include keyword matching, AI-based semantic similarity, and a final recommendation.")
    
    st.write("---")
    st.markdown(
        "<p style='text-align:center; color:gray; font-size:0.8rem;'>Done by Aditi Chaudhari</p>",
        unsafe_allow_html=True
    )
#  ANALYZE

if analyze_clicked:

    if job_description is None:
        st.error("⚠️ Please upload a Job Description.")
        st.stop()

    if resume is None:
        st.error("⚠️ Please upload a Resume.")
        st.stop()

    progress_text = st.empty()
    progress_bar = st.progress(0)

    # Save Resume Temporarily
    progress_text.info("📥 Reading uploaded files...")
    suffix = os.path.splitext(resume.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(resume.getbuffer())
        resume_path = tmp.name
    progress_bar.progress(25)
    time.sleep(0.2)

    # Extract Resume Text
    progress_text.info("🧾 Extracting resume text...")
    resume_text = extract_text(resume_path)
    progress_bar.progress(45)
    time.sleep(0.2)

    # Read Job Description
    jd_text = read_job_description(job_description)
    progress_bar.progress(60)
    time.sleep(0.2)

    # Extract Skills
    progress_text.info("🧠 Extracting and comparing skills...")
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills

    if len(jd_skills) > 0:
        keyword_score = (len(matched) / len(jd_skills)) * 100
    else:
        keyword_score = 0
    progress_bar.progress(80)
    time.sleep(0.2)

    # AI Similarity
    progress_text.info("🤖 Calculating AI similarity score...")
    ai_score = calculate_similarity(resume_text, jd_text)
    progress_bar.progress(100)
    time.sleep(0.2)

    progress_text.empty()
    progress_bar.empty()

    # ========================================================
    #  RESULTS
    # ========================================================

    st.success("✅ Analysis Completed Successfully!")
    st.header("📊 Resume Screening Report")

    tab_overview, tab_skills, tab_recommendation = st.tabs(
        ["📈 Overview", "🧩 Skill Breakdown", "🎯 Recommendation"]
    )

    # ---------------- OVERVIEW TAB ----------------
    with tab_overview:
        col1, col2, col3 = st.columns(3)
        col1.metric("🔑 Keyword Match", f"{keyword_score:.2f}%")
        col2.metric("🤖 AI Similarity", f"{ai_score:.2f}%")
        col3.metric("📌 Skills Compared", f"{len(jd_skills)}")

        st.write("")
        gcol1, gcol2 = st.columns(2)
        with gcol1:
            st.plotly_chart(make_gauge(keyword_score, "Keyword Match", "#06B6D4"), use_container_width=True)
        with gcol2:
            st.plotly_chart(make_gauge(ai_score, "AI Similarity", "#4F46E5"), use_container_width=True)

    # ---------------- SKILLS TAB ----------------
    with tab_skills:
        scol1, scol2 = st.columns(2)

        with scol1:
            st.subheader(f"✅ Matched Skills ({len(matched)})")
            if matched:
                pills_html = "".join(
                    [f'<span class="skill-pill pill-match">{s}</span>' for s in sorted(matched)]
                )
                st.markdown(pills_html, unsafe_allow_html=True)
            else:
                st.warning("No matching skills found.")

        with scol2:
            st.subheader(f"❌ Missing Skills ({len(missing)})")
            if missing:
                pills_html = "".join(
                    [f'<span class="skill-pill pill-missing">{s}</span>' for s in sorted(missing)]
                )
                st.markdown(pills_html, unsafe_allow_html=True)
            else:
                st.success("No missing skills!")

        st.write("---")

        if len(jd_skills) > 0:
            chart_df = pd.DataFrame({
                "Category": ["Matched", "Missing"],
                "Count": [len(matched), len(missing)]
            })
            fig = px.pie(
                chart_df, names="Category", values="Count",
                color="Category",
                color_discrete_map={"Matched": "#22C55E", "Missing": "#EF4444"},
                hole=0.55,
                title="Skill Match Distribution"
            )
            fig.update_layout(height=380)
            st.plotly_chart(fig, use_container_width=True)

    # ---------------- RECOMMENDATION TAB ----------------
    with tab_recommendation:
        st.subheader("🎯 Final Recommendation")

        if ai_score >= 80:
            st.success("⭐⭐⭐⭐⭐ Highly Recommended")
            st.balloons()
        elif ai_score >= 60:
            st.success("⭐⭐⭐⭐ Recommended")
        elif ai_score >= 40:
            st.warning("⭐⭐⭐ Consider for Interview")
        else:
            st.error("⭐⭐ Not Recommended")

        st.write("")
        st.caption(
            f"Based on a combined evaluation of keyword overlap ({keyword_score:.2f}%) "
            f"and AI semantic similarity ({ai_score:.2f}%) between the resume and job description."
        )

        # Downloadable report
        report_text = f"""AI RESUME SCREENING REPORT
==============================
Keyword Match: {keyword_score:.2f}%
AI Similarity: {ai_score:.2f}%

Matched Skills ({len(matched)}):
{', '.join(sorted(matched)) if matched else 'None'}

Missing Skills ({len(missing)}):
{', '.join(sorted(missing)) if missing else 'None'}
"""
        st.download_button(
            "⬇️ Download Report (.txt)",
            data=report_text,
            file_name="resume_screening_report.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    st.info("👈 Upload a Job Description and Resume in the sidebar, then click **Analyze Resume** to get started.")