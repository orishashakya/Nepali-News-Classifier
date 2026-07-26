import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin

# --------------------------------
# Headers
# --------------------------------
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

# --------------------------------
# Load categories
# --------------------------------
categories = pd.read_csv("data/raw/setopati/setopati_categories.csv")

mapping = pd.read_csv("configs/category_mapping.csv")
mapping = mapping[mapping["website"] == "Setopati"]

categories = categories[
    categories["category"].isin(mapping["website_category"])
]

category_to_label = dict(
    zip(mapping["website_category"], mapping["label"])
)

# --------------------------------
# Settings
# --------------------------------
TARGET_PER_LABEL = 80

all_articles = []

seen_urls = set()

label_counts = {}

# --------------------------------
# Loop through categories
# --------------------------------
for _, row in categories.iterrows():

    website_category = row["category"]
    label = category_to_label[website_category]

    if label not in label_counts:
        label_counts[label] = 0

    if label_counts[label] >= TARGET_PER_LABEL:

        print("\n" + "=" * 60)
        print(f"Skipping {website_category}")
        print(f"{label} already has {TARGET_PER_LABEL} articles.")
        continue

    base_url = row["url"]

    print("\n" + "=" * 60)
    print("Website Category :", website_category)
    print("Final Label      :", label)

    page = 1

    while label_counts[label] < TARGET_PER_LABEL:

        # ----------------------------
        # Build page URL ourselves
        # ----------------------------
        if page == 1:
            current_url = base_url
        else:
            current_url = f"{base_url}?page={page}"

        print(f"\nPage {page}")
        print(current_url)

        try:

            response = requests.get(
                current_url,
                headers=headers,
                timeout=15
            )

            response.raise_for_status()

        except Exception as e:

            print("Request failed:", e)
            break

        soup = BeautifulSoup(response.text, "lxml")

        article_links = set()

        # ----------------------------
        # Find article links
        # ----------------------------
        for article in soup.select("span.main-title"):

            parent = article.find_parent("a")

            if parent is None:
                continue

            href = parent.get("href")

            if not href:
                continue

            full_url = urljoin(current_url, href)

            if re.search(r"/\d+$", full_url):
                article_links.add(full_url)

        print(f"Found {len(article_links)} links")

        # No more articles
        if len(article_links) == 0:
            print("No articles found. End of category.")
            break

        added = 0

        for article_url in article_links:

            if article_url in seen_urls:
                continue

            if label_counts[label] >= TARGET_PER_LABEL:
                break

            seen_urls.add(article_url)

            all_articles.append({
                "website": "Setopati",
                "website_category": website_category,
                "label": label,
                "article_url": article_url
            })

            label_counts[label] += 1
            added += 1

        print(f"Added this page : {added}")
        print(f"{label}: {label_counts[label]}/{TARGET_PER_LABEL}")

        # ----------------------------
        # If this page added nothing,
        # stop to avoid infinite pages.
        # ----------------------------
        if added == 0:
            print("No new articles added.")
            break

        page += 1

        time.sleep(1)

# --------------------------------
# Save
# --------------------------------
df = pd.DataFrame(all_articles)

print("\n" + "=" * 60)
print("Total collected:", len(df))

df.to_csv(
    "data/raw/setopati/setopati_article_links.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved!")
print("data/raw/setopati/setopati_article_links.csv")

print("\n" + "=" * 60)
print("FINAL LABEL COUNTS")
print("=" * 60)

for label, count in sorted(label_counts.items()):
    print(f"{label:<25} {count}")