import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from sklearn.model_selection import train_test_split

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

INPUT_FILE = "data/processed/news_dataset_processed.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print(f"Loaded {len(df)} articles")
print("=" * 60)

# --------------------------------------------------
# Features and labels
# --------------------------------------------------

X = df["text"]

y = df["label"]

# --------------------------------------------------
# Split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# --------------------------------------------------
# Save
# --------------------------------------------------

train = pd.DataFrame({
    "text": X_train,
    "label": y_train,
})

test = pd.DataFrame({
    "text": X_test,
    "label": y_test,
})

train.to_csv(
    "data/processed/train.csv",
    index=False,
    encoding="utf-8-sig",
)

test.to_csv(
    "data/processed/test.csv",
    index=False,
    encoding="utf-8-sig",
)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print(f"Training articles : {len(train)}")
print(f"Testing articles  : {len(test)}")

print("\nTraining labels")
print(train["label"].value_counts().sort_index())

print("\nTesting labels")
print(test["label"].value_counts().sort_index())

print("\nSaved")
print("data/processed/train.csv")
print("data/processed/test.csv")