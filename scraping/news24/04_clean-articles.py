import pandas as pd

# --------------------------------------------------
# Load scraped articles
# --------------------------------------------------

df = pd.read_csv(
    "data/raw/news24/news24.csv"
)

print(f"Loaded {len(df)} articles")

# --------------------------------------------------
# Remove duplicate URLs
# --------------------------------------------------

df = df.drop_duplicates(subset=["url"])

# --------------------------------------------------
# Remove missing values
# --------------------------------------------------

df = df.dropna(
    subset=["title", "content"]
)

# --------------------------------------------------
# Remove empty text
# --------------------------------------------------

df["title"] = df["title"].astype(str).str.strip()
df["content"] = df["content"].astype(str).str.strip()

df = df[
    (df["title"] != "")
    &
    (df["content"] != "")
]

# --------------------------------------------------
# Clean title
# --------------------------------------------------

df["title"] = (
    df["title"]
    .str.replace("\n", " ", regex=False)
    .str.replace("\r", " ", regex=False)
    .str.replace("\t", " ", regex=False)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# --------------------------------------------------
# Clean content
# --------------------------------------------------

df["content"] = (
    df["content"]
    .str.replace("\n", " ", regex=False)
    .str.replace("\r", " ", regex=False)
    .str.replace("\t", " ", regex=False)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# --------------------------------------------------
# Remove extremely short articles
# --------------------------------------------------

df = df[
    df["content"].str.len() >= 100
]

# --------------------------------------------------
# Keep columns
# --------------------------------------------------

df = df[
    [
        "website",
        "website_category",
        "label",
        "title",
        "content",
        "url"
    ]
]

# --------------------------------------------------
# Sort for readability
# --------------------------------------------------

df = df.sort_values(
    by="label"
).reset_index(drop=True)

# --------------------------------------------------
# Save cleaned dataset
# --------------------------------------------------

output = "data/processed/news24_clean.csv"

df.to_csv(
    output,
    index=False,
    encoding="utf-8-sig"
)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\nSaved cleaned dataset")
print(output)

print(f"\nFinal Articles: {len(df)}")

print("\nLabel Distribution\n")

print(df["label"].value_counts().sort_index())