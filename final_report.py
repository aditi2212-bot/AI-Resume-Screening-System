from resume_parser import extract_text
from job_description_parser import read_job_description
from skill_extractor import extract_skills
from similarity import calculate_similarity

# Read files
resume_text = extract_text("data/resumes/resume.pdf")
jd_text = read_job_description("data/job_description.txt")

# Extract skills
resume_skills = set(extract_skills(resume_text))
jd_skills = set(extract_skills(jd_text))

# Skill matching
matched = resume_skills.intersection(jd_skills)
missing = jd_skills - resume_skills

keyword_score = (len(matched) / len(jd_skills)) * 100

# AI similarity
ai_score = calculate_similarity(resume_text, jd_text)

print("=" * 50)
print("        AI RESUME SCREENING REPORT")
print("=" * 50)

print(f"\nKeyword Match Score : {keyword_score:.2f}%")
print(f"AI Similarity Score : {ai_score:.2f}%")

print("\nMatched Skills:")
for skill in sorted(matched):
    print(f"✓ {skill}")

print("\nMissing Skills:")
for skill in sorted(missing):
    print(f"✗ {skill}")

# Recommendation
if ai_score >= 80:
    recommendation = "⭐⭐⭐⭐⭐ Highly Recommended"
elif ai_score >= 60:
    recommendation = "⭐⭐⭐⭐ Recommended"
elif ai_score >= 40:
    recommendation = "⭐⭐⭐ Consider for Interview"
else:
    recommendation = "⭐⭐ Not Recommended"

print(f"\nRecommendation: {recommendation}")