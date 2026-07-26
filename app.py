import streamlit as st
import joblib
import numpy as np
from utils.preprocess import preprocess_text
from scipy.special import softmax
import pandas as pd

# ----------------------------------------
# Page Configuration
# ----------------------------------------

st.set_page_config(
    page_title="Nepali News Classification",
    page_icon=None,
    layout="wide"
)
# ----------------------------------------
# Load Saved Model
# ----------------------------------------

@st.cache_resource
def load_models():

    model = joblib.load("models/best_model.pkl")

    vectorizer = joblib.load(
        "models/tfidf_vectorizer.pkl"
    )

    encoder = joblib.load(
        "models/label_encoder.pkl"
    )

    with open("models/best_model.txt") as f:
        model_name = f.read().strip()

    return model, vectorizer, encoder, model_name


model, vectorizer, encoder, model_name = load_models()

st.sidebar.title("Model Information")

st.sidebar.markdown(
    """
**Best Model**

Linear SVM

---

**Vectorizer**

TF-IDF

---

**Training Articles**

1543

**Testing Articles**

386

---

**Accuracy**

80.31%

---

**Categories**

- Business & Economy
- Crime
- Education
- Entertainment
- General News
- Health
- International
- Opinion
- Politics & Government
- Sports
"""
)

# ----------------------------------------
# Sidebar
# ----------------------------------------

st.sidebar.title("Project Information")

st.sidebar.markdown(f"""
### Model

{model_name}

### Feature Extraction

TF-IDF

### Categories

10

### Dataset

1,929 Articles

### Accuracy

80.31%
""")

# ----------------------------------------
# Main Title
# ----------------------------------------

st.title("Nepali News Classification")

st.caption(
    "Machine Learning based Nepali News Category Prediction using TF-IDF and Linear SVM."
)

st.markdown("""
This application classifies Nepali news articles into one of ten predefined
categories using a Linear Support Vector Machine trained on a dataset collected
from News24, Ratopati, and Setopati.
""")

st.divider()

# ----------------------------------------
# Text Input
# ----------------------------------------

news = st.text_area(
    "Paste Nepali News Article",
    height=250,
    placeholder="Paste your Nepali news article here..."
)

predict = st.button(
    "Predict Category",
    use_container_width=True
)

# --------------------------------------------------
# Prediction
# --------------------------------------------------

if predict:

    if len(news.strip()) < 30:

        st.warning(
            "Please enter a longer Nepali news article."
        )

    else:

        cleaned_text = preprocess_text(news)

        vector = vectorizer.transform(
            [cleaned_text]
        )

        prediction = model.predict(vector)[0]

        category = encoder.inverse_transform(
            [prediction]
        )[0]

        st.divider()

    # Confidence Scores
    # ----------------------------------------

    scores = model.decision_function(vector)

    probabilities = softmax(scores[0])

    top3 = probabilities.argsort()[-3:][::-1]

    results = pd.DataFrame({
        "Category": encoder.inverse_transform(top3),
        "Confidence": probabilities[top3] * 100
    })
        # ----------------------------------------
    st.subheader("Prediction")

    col1, col2 = st.columns([2,1])

    with col1:

        st.subheader("Predicted Category")

    st.info(
        f"**{category}**"
    )

    with col2:

        confidence = results.iloc[0]["Confidence"]
        st.progress(confidence / 100)

        st.write(f"Confidence: **{confidence:.2f}%**")

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

    st.divider()

    st.caption(
    "Developed using Python, Scikit-learn, Streamlit and TF-IDF."
)

    st.subheader("Top Predictions")

    results["Confidence"] = results["Confidence"].map(
        lambda x: f"{x:.2f}%"
    )

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )
