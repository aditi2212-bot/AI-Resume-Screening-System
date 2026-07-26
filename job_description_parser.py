from skill_extractor import extract_skills

def read_job_description(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    jd_text = read_job_description("data/job_description.txt")

    print("Job Description:\n")
    print(jd_text)

    jd_skills = extract_skills(jd_text)

    print("\nRequired Skills:\n")

    for skill in jd_skills:
        print("-", skill)