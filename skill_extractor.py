import re

# List of skills to look for
SKILLS = [
    "Python",
    "Machine Learning",
    "Deep Learning",
    "SQL",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Git",
    "Docker",
    "AWS",
    "Azure",
    "Flask",
    "Django",
    "Power BI",
    "Excel",
    "NLP",
    "Computer Vision"
]

def extract_skills(text):
    """
    Extract matching skills from resume text.
    """
    found_skills = []

    text = text.lower()

    for skill in SKILLS:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
            found_skills.append(skill)

    return sorted(found_skills)