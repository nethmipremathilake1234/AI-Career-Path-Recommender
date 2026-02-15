import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# LOAD DATASET
df = pd.read_csv("dataset/cv_dataset.csv")


# ------------------
# TEXT UTILS
# ------------------
def extract_words(text):
    return set(re.findall(r'\b[a-zA-Z]+\b', str(text).lower()))


# ------------------
# TRAIN ROLE MODEL
# ------------------
def train_model():

    tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
    X = tfidf.fit_transform(df["Resume"])

    model = LinearSVC()
    model.fit(X, df["Category"])

    joblib.dump(tfidf, "tfidf.pkl")
    joblib.dump(model, "role_model.pkl")

    print("Role prediction model trained")


# ------------------
# BUILD ROLE SKILL MODEL (ML)
# ------------------
def build_role_skill_model():

    tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
    X = tfidf.fit_transform(df["Resume"])

    words = tfidf.get_feature_names_out()

    role_skills = {}

    for role in df["Category"].unique():

        role_texts = df[df["Category"] == role]["Resume"]
        role_matrix = tfidf.transform(role_texts)

        scores = role_matrix.mean(axis=0).A1
        word_scores = dict(zip(words, scores))

        top_skills = sorted(word_scores, key=word_scores.get, reverse=True)[:50]

        role_skills[role.lower()] = top_skills

    joblib.dump(role_skills, "role_skills.pkl")

    print("Role skill model built")


# ------------------
# LOAD MODELS
# ------------------
def predict_role(text):
    tfidf = joblib.load("tfidf.pkl")
    model = joblib.load("role_model.pkl")
    return model.predict(tfidf.transform([text]))[0]


def load_role_skills():
    return joblib.load("role_skills.pkl")


# ------------------
# DETECT SECTIONS
# ------------------
def detect_sections(text):

    patterns = {
        "Summary": r"(summary|objective|profile)",
        "Experience": r"(experience|employment|work history)",
        "Education": r"(education|academic)",
        "Skills": r"(skills|technical skills)",
        "Projects": r"(projects|portfolio)"
    }

    text = text.lower()

    return {k: bool(re.search(v, text)) for k, v in patterns.items()}


# ------------------
# AI MISSING SKILLS
# ------------------
def detect_missing_skills(text, target_role):

    role_skills = load_role_skills()
    resume_words = extract_words(text)

    target_skills = role_skills.get(target_role.lower(), [])

    missing = [s for s in target_skills if s not in resume_words]
    present = [s for s in target_skills if s in resume_words]

    coverage = len(present) / len(target_skills) * 100 if target_skills else 0

    return missing[:10], round(coverage, 2)


# ------------------
# AI COURSE RECOMMENDER
# ------------------
def recommend_courses_ai(missing_skills):

    courses = []

    for skill in missing_skills[:5]:
        query = skill.replace("_", " ")
        url = f"https://www.coursera.org/search?query={query}"

        courses.append({
            "skill": skill,
            "course": url
        })

    return courses


# ------------------
# MAIN ANALYSIS
# ------------------
def analyze_resume(text, target_role):

    detected_role = predict_role(text)

    sections = detect_sections(text)

    missing_skills, coverage = detect_missing_skills(text, target_role)

    courses = recommend_courses_ai(missing_skills)

    suggestions = []

    if not sections["Summary"]:
        suggestions.append(f"Add professional summary for {target_role} role.")

    if not sections["Projects"]:
        suggestions.append(f"Include project experience related to {target_role}.")

    if missing_skills:
        suggestions.append("Add important role-specific skills.")

    score = round(coverage * 0.7 + 30, 2)

    return (
        detected_role,
        sections,
        missing_skills,
        courses,
        coverage,
        score,
        suggestions
    )


# ------------------
# TRAIN ALL
# ------------------
if __name__ == "__main__":
    train_model()
    build_role_skill_model()
