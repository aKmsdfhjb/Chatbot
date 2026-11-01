from pathlib import Path
import os
import pickle

import pandas as pd
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
REQUIRED_FILES = ("tfidf_vectorizer.pkl", "tfidf_matrix_X.pkl", "chatbot_data.pkl")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "https://aKmsdfhjb.github.io,http://localhost:8000,http://127.0.0.1:8000",
    ).split(",")
    if origin.strip()
]
CORS(app, resources={r"/ask": {"origins": allowed_origins}, r"/health": {"origins": allowed_origins}})

vectorizer = None
document_matrix = None
chatbot_data = None
model_error = None


def load_model():
    """Load the TF-IDF artifacts created by setup_model.py."""
    global vectorizer, document_matrix, chatbot_data, model_error

    missing = [name for name in REQUIRED_FILES if not (MODEL_DIR / name).is_file()]
    if missing:
        model_error = (
            "Model artifacts are missing: "
            + ", ".join(missing)
            + ". Run python setup_model.py first."
        )
        return

    try:
        with (MODEL_DIR / "tfidf_vectorizer.pkl").open("rb") as file:
            vectorizer = pickle.load(file)
        with (MODEL_DIR / "tfidf_matrix_X.pkl").open("rb") as file:
            document_matrix = pickle.load(file)
        chatbot_data = pd.read_pickle(MODEL_DIR / "chatbot_data.pkl")
        model_error = None
    except Exception as exc:
        model_error = f"Could not load model artifacts: {exc}"


def get_chatbot_response(question):
    """Return the answer belonging to the most similar context/question row."""
    if model_error or vectorizer is None or document_matrix is None or chatbot_data is None:
        raise RuntimeError(model_error or "The model is not ready.")

    query_vector = vectorizer.transform([question])
    similarities = cosine_similarity(query_vector, document_matrix)[0]
    best_index = int(similarities.argmax())
    score = float(similarities[best_index])

    if score < 0.2:
        return {
            "answer": "I couldn't find a close match in the knowledge base. Try rephrasing your question.",
            "confidence": score,
            "matched": False,
        }

    return {
        "answer": str(chatbot_data.iloc[best_index]["answer"]),
        "confidence": score,
        "matched": True,
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"ready": model_error is None, "error": model_error})


@app.route("/ask", methods=["POST"])
def ask():
    payload = request.get_json(silent=True) or {}
    question = payload.get("question", "")
    if not isinstance(question, str) or not question.strip():
        return jsonify({"error": "Please enter a question."}), 400
    if len(question) > 2000:
        return jsonify({"error": "Questions must be 2,000 characters or fewer."}), 400
    if model_error:
        return jsonify({"error": model_error}), 503

    try:
        result = get_chatbot_response(question.strip())
        return jsonify(result)
    except Exception:
        app.logger.exception("Question processing failed")
        return jsonify({"error": "The question could not be processed."}), 500


load_model()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
