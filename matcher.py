from resume_parser import extract_text
from job_description_parser import read_job_description
from skill_extractor import extract_skills


resume_text = extract_text("data/resumes/resume.pdf")
jd_text = read_job_description("data/job_description.txt")

resume_skills = set(extract_skills(resume_text))
jd_skills = set(extract_skills(jd_text))

matched = resume_skills.intersection(jd_skills)
missing = jd_skills - resume_skills

match_percentage = (len(matched) / len(jd_skills)) * 100

print("=" * 40)
print("RESUME SCREENING REPORT")
print("=" * 40)

print("\nMatched Skills:")
for skill in sorted(matched):
    print(f"✓ {skill}")

print("\nMissing Skills:")
for skill in sorted(missing):
    print(f"✗ {skill}")

print(f"\nSkill Match Percentage: {match_percentage:.2f}%")