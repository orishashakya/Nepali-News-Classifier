import pandas as pd

# ==========================================================
# Load scraped articles
# ==========================================================
INPUT_FILE = "data/raw/setopati/setopati.csv"
OUTPUT_FILE = "data/processed/setopati_clean.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print(f"Loaded {len(df)} articles")

print("\nColumns found:")
print(df.columns.tolist())

# ==========================================================
# Standardize text columns
# ==========================================================
text_columns = [
    "title",
    "content",
    "website",
    "website_category",
    "label",
    "article_url"
]

for col in text_columns:

    if col in df.columns:

        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

# ==========================================================
# Remove rows missing essential information
# ==========================================================
required_columns = [
    "title",
    "content",
    "article_url"
]

for col in required_columns:

    df = df[df[col] != ""]

print(f"\nAfter removing empty rows: {len(df)}")

# ==========================================================
# Remove duplicate URLs
# ==========================================================
before = len(df)

df = df.drop_duplicates(subset=["article_url"])

removed = before - len(df)

print(f"Removed {removed} duplicate articles")

# ==========================================================
# Keep only required columns
# ==========================================================
required_output = [
    "website",
    "website_category",
    "label",
    "title",
    "content",
    "article_url"
]

df = df[required_output]

# ==========================================================
# Sort by label (optional)
# ==========================================================
df = df.sort_values(
    by="label"
).reset_index(drop=True)

# ==========================================================
# Save cleaned dataset
# ==========================================================
df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# Summary
# ==========================================================
print("\n" + "=" * 60)
print("Cleaning completed successfully!")

print(f"\nFinal articles : {len(df)}")

print(f"\nSaved to:\n{OUTPUT_FILE}")

print("\nLabel Distribution")
print("-" * 60)
print(df["label"].value_counts().sort_index())

print("\nPreview")
print("-" * 60)
print(df.head())