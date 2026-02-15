import joblib
import re


# -----------------------
# TEXT UTILS
# -----------------------
def extract_words(text):
    return set(re.findall(r"\b[a-zA-Z]+\b", str(text).lower()))


# -----------------------
# LOAD MODELS
# -----------------------
def load_models():
    tfidf = joblib.load("tfidf.pkl")
    model = joblib.load("role_model.pkl")
    role_skills = joblib.load("role_skills.pkl")
    return tfidf, model, role_skills


# -----------------------
# TOP CAREER PREDICTION
# -----------------------
def predict_top_careers(text, top_n=3):
    tfidf, model, role_skills = load_models()

    X = tfidf.transform([text])
    scores = model.decision_function(X)[0]
    roles = model.classes_

    ranking = sorted(
        zip(roles, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ranking[:top_n]


# -----------------------
# CAREER ROADMAP
# -----------------------
def build_career_path(role, role_skills, resume_words):

    skills = role_skills.get(role.lower(), [])

    present = [s for s in skills if s in resume_words]
    missing = [s for s in skills if s not in resume_words]

    coverage = round(len(present) / len(skills) * 100, 2) if skills else 0

    roadmap = []

    for i, skill in enumerate(missing[:6]):
        roadmap.append({
            "step": i + 1,
            "skill": skill,
            "course": f"https://www.coursera.org/search?query={skill}"
        })

    return coverage, roadmap


# -----------------------
# MAIN ANALYSIS
# -----------------------
def analyze_career_path(text):

    tfidf, model, role_skills = load_models()

    resume_words = extract_words(text)
    careers = predict_top_careers(text)

    results = []

    for role, score in careers:
        coverage, roadmap = build_career_path(role, role_skills, resume_words)

        results.append({
            "career": role,
            "match_score": round(float(score), 2),
            "coverage": coverage,
            "roadmap": roadmap
        })

    return results
