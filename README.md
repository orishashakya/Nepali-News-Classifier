# Nepali News Classification using Machine Learning

A machine learning project for automatically classifying Nepali news articles into multiple categories using TF-IDF feature extraction and traditional machine learning algorithms.

---

## Project Overview

This project builds an end-to-end Nepali News Classification system.

The workflow includes:

- Web scraping Nepali news websites
- Data cleaning and preprocessing
- TF-IDF feature extraction
- Training multiple machine learning models
- Model evaluation
- Streamlit web application for prediction

---

## News Sources

The dataset was collected from:

- News24 Nepal
- Ratopati
- Setopati

---

## Categories

The classifier predicts the following categories:

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

---

## Project Structure

```
Nepali-News-Classification
│
├── app.py
├── requirements.txt
├── README.md
│
├── configs/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── results/
│
├── models/
│
├── notebooks/
│
├── scripts/
│
├── scraping/
│
├── utils/
│
└── venv/
```

---

## Machine Learning Pipeline

1. Web Scraping
2. Data Cleaning
3. Text Preprocessing
4. TF-IDF Vectorization
5. Train/Test Split
6. Model Training
7. Model Evaluation
8. Prediction using Streamlit

---

## Models Compared

- Multinomial Naive Bayes
- Logistic Regression
- Linear SVM
- Random Forest
- Decision Tree
- K-Nearest Neighbors

---

## Best Performing Model

| Model | Accuracy |
|-------|----------|
| Linear SVM | **80.31%** |

---

## Technologies Used

- Python
- BeautifulSoup
- Requests
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib
- Seaborn
- Joblib

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Nepali-News-Classification.git

cd Nepali-News-Classification
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Mac/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

---

## Run Streamlit

```bash
streamlit run app.py
```

---

## Example Prediction

Input

```
काभा मेन्स भलिबल च्याम्पियनसिप २०२६ मा नेपाल लगातार दोस्रो खेलमा पराजित भएको छ।
```

Prediction

```
Sports
```

---

## Future Improvements

- Deep Learning models
- Transformer-based models
- NepaliBERT integration
- Hugging Face models
- RAG-based Nepali News Assistant

---

## Author

Orisha Shakya
