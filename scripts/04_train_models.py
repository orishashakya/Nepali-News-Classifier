#importing required libraires
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import time
import joblib
import pandas as pd

from sklearn.preprocessing import LabelEncoder

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

#--------------------------------------------------
# Load train and test datasets
#--------------------------------------------------

train = pd.read_csv("data/processed/train.csv")
test = pd.read_csv("data/processed/test.csv")

print("=" * 60)
print("Training Articles :", len(train))
print("Testing Articles  :", len(test))
print("=" * 60)

#--------------------------------------------------
# Encode labels
#--------------------------------------------------
encoder = LabelEncoder()

y_train = encoder.fit_transform(train["label"])
y_test = encoder.transform(test["label"])
#--------------------------------------------------
# Save the label encoder
#-------------------------------------------------- 
joblib.dump(
    encoder,
    "models/label_encoder.pkl"
)
#--------------------------------------------------
# TF-IDF Vectorization
#--------------------------------------------------
vectorizer = TfidfVectorizer(

    max_features=30000,

    ngram_range=(1,2),

    min_df=2,

    max_df=0.95,

    sublinear_tf=True

)

#--------------------------------------------------
# Fit and transform the training data
#--------------------------------------------------
X_train = vectorizer.fit_transform(train["text"])

X_test = vectorizer.transform(test["text"])

print("\nVocabulary Size:", len(vectorizer.vocabulary_))
print("Training Matrix:", X_train.shape)
print("Testing Matrix :", X_test.shape)

#--------------------------------------------------
# Save the vectorizer
#--------------------------------------------------
joblib.dump(
    vectorizer,
    "models/tfidf_vectorizer.pkl"
)
#--------------------------------------------------
# Train and evaluate models dictionary
#--------------------------------------------------
models = {

    "Naive Bayes":
        MultinomialNB(),

    "Logistic Regression":
        LogisticRegression(
            max_iter=1000,
            random_state=42
        ),

    "Linear SVM":
        LinearSVC(
            random_state=42
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            n_jobs=-1
        ),

    "Decision Tree":
        DecisionTreeClassifier(
            random_state=42
        ),

    "KNN":
        KNeighborsClassifier(
            n_neighbors=7
        ),
}
#-------------------------------------------------- 
#Results list to store the evaluation metrics for each model
#--------------------------------------------------
results = []
best_accuracy = 0

best_model = None

best_name = ""

print("\n" + "=" * 60)
print("Training Models")
print("=" * 60)

best_report = None
best_confusion_matrix = None

for name, model in models.items():

    print(f"\n{name}")

    start = time.time()

    model.fit(X_train, y_train)

    train_time = time.time() - start

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"Time      : {train_time:.2f} sec")

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "Training Time": train_time
    })

    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model
        best_name = name

        best_report = classification_report(
            y_test,
            predictions,
            target_names=encoder.classes_
        )

        best_confusion_matrix = confusion_matrix(
            y_test,
            predictions
        )

#Saving the comparison table

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
        by="Accuracy",
        ascending=False
    )

results_df.to_csv(
        "data/results/model_results.csv",
        index=False
    )

print("\n" + "=" * 60)
print("Model Comparison")
print("=" * 60)

print(results_df)

#save best model

joblib.dump(
    best_model,
    "models/best_model.pkl"
)

print("\nBest Model")
print(best_name)
with open("models/best_model.txt", "w") as f:
    f.write(best_name)
print(f"Accuracy: {best_accuracy:.4f}")

#save classification report and confusion matrix for best model

with open(
    "data/results/classification_report.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(best_report)

cm_df = pd.DataFrame(
    best_confusion_matrix,
    index=encoder.classes_,
    columns=encoder.classes_
)

cm_df.to_csv(
    "data/results/confusion_matrix.csv",
    encoding="utf-8-sig"
)

print("\nSaved Files")

print("models/best_model.pkl")
print("models/tfidf_vectorizer.pkl")
print("models/label_encoder.pkl")

print("data/results/model_results.csv")
print("data/results/classification_report.txt")
print("data/results/confusion_matrix.csv")

print("\nTraining Complete!")

