import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --------------------------------------------------
# Settings
# --------------------------------------------------

BASE_URL = "https://www.news24nepal.com"

TARGET_ARTICLES = 80

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

# --------------------------------------------------
# Read Categories
# --------------------------------------------------

categories = pd.read_csv(
    "data/raw/news24/categories.csv"
)

mapping = pd.read_csv(
    "configs/category_mapping.csv"
)

mapping = mapping[
    mapping["website"] == "News24"
]

categories = categories[
    categories["website_category"].isin(
        mapping["website_category"]
    )
]

category_to_label = dict(
    zip(
        mapping["website_category"],
        mapping["label"]
    )
)

# --------------------------------------------------
# Storage
# --------------------------------------------------

all_articles = []

seen_urls = set()

label_counts = {}

# --------------------------------------------------
# Loop categories
# --------------------------------------------------

for _, row in categories.iterrows():

    website_category = row["website_category"]

    label = category_to_label[website_category]

    # Skip if label already complete
    if label_counts.get(label, 0) >= TARGET_ARTICLES:

        print("\n" + "=" * 60)
        print(f"Skipping {website_category}")
        print(f"{label} already has {TARGET_ARTICLES} articles.")
        continue

    print("\n" + "=" * 60)
    print(f"Website Category : {website_category}")
    print(f"Final Label      : {label}")

    page = 1

    while label_counts.get(label, 0) < TARGET_ARTICLES:

        current_url = row["category_url"]

        if page > 1:
            current_url += f"?page={page}"

        print(f"\nPage {page}")
        print(current_url)

        try:

            response = requests.get(
                current_url,
                headers=headers,
                timeout=20
            )

            response.raise_for_status()

        except requests.RequestException as e:

            print(e)
            break

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        # ----------------------------------------
        # Find article links
        # ----------------------------------------

        article_links = set()

        for a in soup.find_all("a", href=True):

            href = a["href"]

            if "/detail/" not in href:
                continue

            if not href.startswith(BASE_URL):
                continue

            article_links.add(href)

        print(f"Found {len(article_links)} links")

        if len(article_links) == 0:
            print("No more articles.")
            break

        added = 0

        for url in article_links:

            if url in seen_urls:
                continue

            if label_counts.get(label, 0) >= TARGET_ARTICLES:
                break

            seen_urls.add(url)

            all_articles.append({

                "website": "News24",

                "website_category": website_category,

                "label": label,

                "article_url": url

            })

            label_counts[label] = (
                label_counts.get(label, 0) + 1
            )

            added += 1

        print(f"Added this page : {added}")
        print(
            f"{label}: "
            f"{label_counts[label]}/{TARGET_ARTICLES}"
        )

        # ----------------------------------------
        # Check if next page exists
        # ----------------------------------------

        next_button = soup.find(
            "a",
            class_="nextpostslink"
        )

        if next_button is None:
            print("No next page.")
            break

        page += 1

        time.sleep(1)

# --------------------------------------------------
# Save
# --------------------------------------------------

df = pd.DataFrame(all_articles)

print("\n" + "=" * 60)
print(f"Total collected: {len(df)}")

df.to_csv(
    "data/raw/news24/news24_article_links.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved!")
print("data/raw/news24/news24_article_links.csv")

print("\n" + "=" * 60)
print("FINAL LABEL COUNTS")
print("=" * 60)

print(df["label"].value_counts().sort_index())