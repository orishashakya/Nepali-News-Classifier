import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

import pandas as pd

from utils.preprocess import preprocess_text
import pandas as pd

from utils.preprocess import preprocess_text


# --------------------------------------------------
# Load merged dataset
# --------------------------------------------------

INPUT_FILE = "data/processed/news_dataset.csv"
OUTPUT_FILE = "data/processed/news_dataset_processed.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print(f"Loaded {len(df)} articles")
print("=" * 60)


# --------------------------------------------------
# Remove duplicates
# --------------------------------------------------

before = len(df)

df = df.drop_duplicates(subset=["title", "content"])

after = len(df)

print(f"Duplicates removed : {before - after}")


# --------------------------------------------------
# Remove missing values
# --------------------------------------------------

df = df.dropna(subset=["title", "content", "label"])


# --------------------------------------------------
# Preprocess title
# --------------------------------------------------

print("\nCleaning titles...")

df["title"] = df["title"].apply(preprocess_text)


# --------------------------------------------------
# Preprocess content
# --------------------------------------------------

print("Cleaning contents...")

df["content"] = df["content"].apply(preprocess_text)


# --------------------------------------------------
# Remove empty rows
# --------------------------------------------------

df = df[
    (df["title"].str.len() > 0)
    &
    (df["content"].str.len() > 0)
]


# --------------------------------------------------
# Combine title + content
# --------------------------------------------------

df["text"] = df["title"] + " " + df["content"]


# --------------------------------------------------
# Normalize combined text
# --------------------------------------------------

df["text"] = df["text"].apply(preprocess_text)


# --------------------------------------------------
# Remove extremely short articles
# --------------------------------------------------

MIN_LENGTH = 100

before = len(df)

df = df[df["text"].str.len() >= MIN_LENGTH]

after = len(df)

print(f"\nRemoved short articles : {before-after}")


# --------------------------------------------------
# Reset index
# --------------------------------------------------

df = df.reset_index(drop=True)


# --------------------------------------------------
# Save
# --------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\n" + "=" * 60)

print("Saved processed dataset")

print(OUTPUT_FILE)

print("\nDataset Shape")

print(df.shape)

print("\nColumns")

print(df.columns.tolist())

print("\nLabel Distribution")

print(df["label"].value_counts().sort_index())

print("=" * 60)