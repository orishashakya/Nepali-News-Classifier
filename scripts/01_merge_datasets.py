import pandas as pd

# --------------------------------------------------
# File paths
# --------------------------------------------------

NEWS24_PATH = "data/processed/news24_clean.csv"
RATOPATI_PATH = "data/processed/ratopati_clean.csv"
SETOPATI_PATH = "data/processed/setopati_clean.csv"

OUTPUT_PATH = "data/processed/news_dataset.csv"

# --------------------------------------------------
# Load datasets
# --------------------------------------------------

news24 = pd.read_csv(NEWS24_PATH)
ratopati = pd.read_csv(RATOPATI_PATH)
setopati = pd.read_csv(SETOPATI_PATH)

print(f"News24    : {len(news24)}")
print(f"Ratopati  : {len(ratopati)}")
print(f"Setopati  : {len(setopati)}")

# --------------------------------------------------
# Standardize column names
# --------------------------------------------------

if "article_url" in news24.columns:
    news24.rename(columns={"article_url": "url"}, inplace=True)

if "article_url" in ratopati.columns:
    ratopati.rename(columns={"article_url": "url"}, inplace=True)

if "article_url" in setopati.columns:
    setopati.rename(columns={"article_url": "url"}, inplace=True)

# --------------------------------------------------
# Keep only required columns
# --------------------------------------------------

columns = [
    "website",
    "website_category",
    "label",
    "title",
    "content",
    "url"
]

news24 = news24[columns]
ratopati = ratopati[columns]
setopati = setopati[columns]

# --------------------------------------------------
# Merge
# --------------------------------------------------

dataset = pd.concat(
    [news24, ratopati, setopati],
    ignore_index=True
)

print(f"\nMerged articles : {len(dataset)}")

# --------------------------------------------------
# Remove duplicates
# --------------------------------------------------

before = len(dataset)

dataset.drop_duplicates(
    subset=["title", "content"],
    inplace=True
)

after = len(dataset)

print(f"Duplicates removed : {before - after}")

# --------------------------------------------------
# Shuffle
# --------------------------------------------------

dataset = dataset.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# --------------------------------------------------
# Save
# --------------------------------------------------

dataset.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved merged dataset")
print(OUTPUT_PATH)

print("\nFinal Dataset Shape")
print(dataset.shape)

print("\nLabel Distribution\n")
print(dataset["label"].value_counts().sort_index())

import pandas as pd

print("News24")
print(pd.read_csv("data/processed/news24_clean.csv")["label"].value_counts().sort_index())

print("\nRatopati")
print(pd.read_csv("data/processed/ratopati_clean.csv")["label"].value_counts().sort_index())

print("\nSetopati")
print(pd.read_csv("data/processed/setopati_clean.csv")["label"].value_counts().sort_index())