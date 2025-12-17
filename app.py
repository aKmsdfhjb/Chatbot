from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# --- Load Model Artifacts ---
MODEL_DIR = 'model'
try:
    # Check if all required files exist before loading
    required_files = ['tfidf_vectorizer.pkl', 'tfidf_matrix_X.pkl', 'chatbot_data.pkl']
    for file in required_files:
        if not os.path.exists(os.path.join(MODEL_DIR, file)):
            raise FileNotFoundError(f"Missing model file: {file}")

    with open(os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'tfidf_matrix_X.pkl'), 'rb') as f:
        X = pickle.load(f)
    df = pd.read_pickle(os.path.join(MODEL_DIR, 'chatbot_data.pkl'))
    print("Model loaded successfully.")
except FileNotFoundError as e:
    print(f"FATAL ERROR: Model files not found. Run setup_model.py first. Details: {e}")
    exit()
except Exception as e:
    print(f"FATAL ERROR during model loading: {e}")
    exit()

# --- Chatbot Logic Function ---
def get_chatbot_response(question):
    """
    Finds the best answer for a given question using Cosine Similarity.
    """
    # 1. Vectorize the question
    q_vec = vectorizer.transform([question])

    # 2. Calculate Cosine Similarity
    sims = cosine_similarity(q_vec, X)[0]

    # 3. Get the index of the highest similarity score
    idx = sims.argmax()
    
    # Optional: Set a similarity threshold (e.g., 0.2)
    max_sim_score = sims[idx]
    if max_sim_score < 0.2: 
        return "I'm sorry, I couldn't find a good answer for that. Could you try rephrasing?"

    # 4. Return the corresponding answer
    answer = df['answer'][idx]
    
    return answer

# --- Flask Routes ---

@app.route('/')
def home():
    """Renders the main chatbot interface."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handles the AJAX request from the front end."""
    user_question = request.json.get('question', '')
    if not user_question.strip():
        return jsonify({'answer': 'Please enter a question.'})

    try:
        response = get_chatbot_response(user_question)
        return jsonify({'answer': response})
    except Exception as e:
        print(f"An error occurred during response generation: {e}")
        return jsonify({'answer': 'An error occurred while processing your request.'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)