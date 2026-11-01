# KMC Knowledge Assistant

A retrieval-based chatbot that answers questions from the repository's KMC knowledge-base dataset. It combines each row's context and question, builds TF-IDF vectors, compares a user's query with cosine similarity, and returns the answer from the closest row.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/API-Flask-171715?style=flat-square&logo=flask&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-TF--IDF%20%2B%20Cosine-c34b2e?style=flat-square)

## Browser interface

The static client is deployed separately from the Python API. After enabling **Settings → Pages → Build and deployment → GitHub Actions**, the interface will be available at:

[Open the chatbot interface](https://aKmsdfhjb.github.io/Chatbot/)

On GitHub Pages, enter the public URL of your Flask API in **Backend API Base URL**. When running the Flask server locally, leave that field blank.

## How it works

~~~mermaid
flowchart TD
 A[chatbot.csv: context, question, answer] --> B[setup_model.py]
 B --> C[TF-IDF vectorizer]
 B --> D[Document TF-IDF matrix]
 B --> E[Prepared knowledge-base data]
 F[User question] --> G[Vectorize query]
 C --> G
 G --> H[Cosine similarity]
 D --> H
 H --> I{Best score ≥ 0.20?}
 I -->|Yes| J[Return matched answer]
 I -->|No| K[Ask user to rephrase]
 E --> J
~~~

## Run locally

Use Python 3.10 or newer.

~~~bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python setup_model.py
python app.py
~~~

Open http://127.0.0.1:5000.

## API

- GET /health — reports whether model artifacts loaded successfully.
- POST /ask — JSON body: {"question":"What programmes are offered?"}.

The API returns an answer, a cosine-similarity score and whether a close match was found. Set CORS_ORIGINS to a comma-separated allowlist of trusted browser origins when deploying.

## Repository layout

- chatbot.csv — source knowledge base.
- setup_model.py — builds TF-IDF artifacts.
- model/ — generated vectorizer, matrix and prepared data.
- app.py — Flask API and local server.
- templates/index.html — responsive browser client; also used as the GitHub Pages artifact.
- .github/workflows/pages.yml — static GitHub Pages deployment.

## Limitations

This is a TF-IDF retrieval system, not an LLM. Answers are limited to the dataset and may be incorrect when a question is ambiguous or outside the knowledge base. The similarity threshold is a simple heuristic, not a calibrated confidence probability.

## License

MIT — see LICENSE.
