#import required libraries

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import joblib
import numpy as np

from utils.preprocess import preprocess_text

# --------------------------------------------------
# Load trained files
# --------------------------------------------------

model = joblib.load(
    "models/best_model.pkl"
)

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)

encoder = joblib.load(
    "models/label_encoder.pkl"
)

print("=" * 65)
print("         Nepali News Classification System")
print("=" * 65)

print("\nLoaded Successfully")
print("Best Model :", type(model).__name__)
print()

# --------------------------------------------------
# Prediction Loop
# --------------------------------------------------

while True:

    print("-" * 65)

    news = input("Paste Nepali News (type 'exit' to quit):\n\n")

    if news.lower() == "exit":

        print("\nGoodbye!")
        break

    if len(news.strip()) == 0:

        print("\nPlease enter some news.\n")
        continue

    # --------------------------------------------------
    # Preprocess
    # --------------------------------------------------

    processed = preprocess_text(news)

    # --------------------------------------------------
    # Vectorize
    # --------------------------------------------------

    vector = vectorizer.transform([processed])

    # --------------------------------------------------
    # Predict
    # --------------------------------------------------

    prediction = model.predict(vector)

    predicted_label = encoder.inverse_transform(prediction)[0]

    # --------------------------------------------------
    # Decision Scores
    # --------------------------------------------------

    scores = model.decision_function(vector)[0]

# Convert scores to probabilities-like values
    exp_scores = np.exp(scores - np.max(scores))    
    probabilities = exp_scores / exp_scores.sum()

    top3 = np.argsort(probabilities)[::-1][:3]

    print("\nPrediction")
    print("=" * 65)

    print(f"Predicted Category : {predicted_label}")

    print("\nTop 3 Predictions\n")

    for rank, idx in enumerate(top3, start=1):

        label = encoder.inverse_transform([idx])[0]

        confidence = probabilities[idx] * 100

        print(f"{rank}. {label:<25} Confidence : {confidence:.2f}%")

    print("=" * 65)
    print()