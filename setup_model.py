import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# --- 1. Setup Data and Model ---
# Assuming 'Chatbot.csv' is in the same directory
try:
    df = pd.read_csv("Chatbot.csv")
except FileNotFoundError:
    print("Error: Chatbot.csv not found. Please place your data file here.")
    exit()

# Combine context and question for better search results
df['search_text'] = df['context'] + " " + df["question"]

# Initialize and fit the vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['search_text'])

# --- 2. Save Model Artifacts ---
# Create the model directory if it doesn't exist
model_dir = 'model'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Save the TfidfVectorizer
with open(os.path.join(model_dir, 'tfidf_vectorizer.pkl'), 'wb') as f:
    pickle.dump(vectorizer, f)

# Save the TF-IDF matrix (X)
with open(os.path.join(model_dir, 'tfidf_matrix_X.pkl'), 'wb') as f:
    pickle.dump(X, f)

# Save the DataFrame (especially the 'answer' column)
df.to_pickle(os.path.join(model_dir, 'chatbot_data.pkl'))

print("Model setup complete!")
print(f"Vectorizer, Matrix, and Data saved to the '{model_dir}/' directory.")