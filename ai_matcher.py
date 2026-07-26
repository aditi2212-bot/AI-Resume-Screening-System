from resume_parser import extract_text
from job_description_parser import read_job_description
from similarity import calculate_similarity

resume_text = extract_text("data/resumes/resume.pdf")
jd_text = read_job_description("data/job_description.txt")

score = calculate_similarity(resume_text, jd_text)

print("=" * 40)
print("AI RESUME SCREENING")
print("=" * 40)

print(f"\nAI Similarity Score: {score:.2f}%")