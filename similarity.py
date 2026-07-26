from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(resume_text, jd_text):
    """
    Calculate semantic similarity between resume and job description.
    """

    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([jd_text])

    similarity = cosine_similarity(
        resume_embedding,
        jd_embedding
    )

    return similarity[0][0] * 100