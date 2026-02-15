from flask import Flask, render_template, request, jsonify
from cv_parser import extract_text
from career_analyzer import analyze_career_path

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("career_dashboard.html")   # ✅ IMPORTANT


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["cv"]
    text = extract_text(file)

    results = analyze_career_path(text)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
