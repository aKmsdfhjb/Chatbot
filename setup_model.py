from pathlib import Path
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "chatbot.csv"
MODEL_DIR = BASE_DIR / "model"


def main():
    if not DATA_FILE.is_file():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    data = pd.read_csv(DATA_FILE)
    required_columns = {"context", "question", "answer"}
    missing = required_columns.difference(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")

    data = data.dropna(subset=["context", "question", "answer"]).copy()
    if data.empty:
        raise ValueError("The dataset contains no complete question/answer rows.")

    data["search_text"] = data["context"].astype(str) + " " + data["question"].astype(str)
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(data["search_text"])

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with (MODEL_DIR / "tfidf_vectorizer.pkl").open("wb") as file:
        pickle.dump(vectorizer, file)
    with (MODEL_DIR / "tfidf_matrix_X.pkl").open("wb") as file:
        pickle.dump(matrix, file)
    data.to_pickle(MODEL_DIR / "chatbot_data.pkl")

    print(f"Model artifacts saved to {MODEL_DIR}")


if __name__ == "__main__":
    main()
