import pandas as pd
import re

# --------------------------------------------------
# Read scraped articles
# --------------------------------------------------
df = pd.read_csv(
    "data/raw/ratopati/ratopati_articles.csv"
)

print("=" * 60)
print("Original dataset")
print(f"Articles : {len(df)}")

# --------------------------------------------------
# Remove duplicate URLs
# --------------------------------------------------
df = df.drop_duplicates(
    subset=["article_url"]
)

print(f"After removing duplicate URLs : {len(df)}")

# --------------------------------------------------
# Remove duplicate title + content
# --------------------------------------------------
df = df.drop_duplicates(
    subset=["title", "content"]
)

print(f"After removing duplicate articles : {len(df)}")

# --------------------------------------------------
# Remove missing values
# --------------------------------------------------
df = df.dropna(
    subset=[
        "title",
        "content",
        "label"
    ]
)

print(f"After removing missing values : {len(df)}")

# --------------------------------------------------
# Clean title
# --------------------------------------------------
def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # Remove new lines
    text = text.replace("\n", " ")

    # Remove tabs
    text = text.replace("\t", " ")

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# --------------------------------------------------
# Apply cleaning
# --------------------------------------------------
df["title"] = df["title"].apply(clean_text)

df["content"] = df["content"].apply(clean_text)

# --------------------------------------------------
# Remove empty rows after cleaning
# --------------------------------------------------
df = df[
    (df["title"] != "")
]

df = df[
    (df["content"] != "")
]

print(f"After removing empty rows : {len(df)}")

# --------------------------------------------------
# Remove very short articles
# --------------------------------------------------
MIN_CONTENT_LENGTH = 150

df = df[
    df["content"].str.len() >= MIN_CONTENT_LENGTH
]

print(f"After removing short articles : {len(df)}")

# --------------------------------------------------
# Reset index
# --------------------------------------------------
df = df.reset_index(drop=True)

# --------------------------------------------------
# Save cleaned dataset
# --------------------------------------------------
output_path = "data/processed/ratopati_clean.csv"

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("=" * 60)
print("Cleaning completed successfully!")
print(f"Final articles : {len(df)}")
print(f"Saved to : {output_path}")

# --------------------------------------------------
# Show label distribution
# --------------------------------------------------
print("\nLabel Distribution")
print("=" * 60)

print(
    df["label"]
    .value_counts()
    .sort_index()
)