import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

# ============================================================
# SETTINGS
# ============================================================

TARGET_PER_LABEL = 80

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

# ============================================================
# LOAD FILES
# ============================================================

categories = pd.read_csv(
    "data/raw/ratopati/ratopati_categories.csv"
)

mapping = pd.read_csv(
    "configs/category_mapping.csv"
)

mapping = mapping[
    mapping["website"] == "Ratopati"
]

categories = categories[
    categories["category"].isin(
        mapping["website_category"]
    )
]

category_to_label = dict(
    zip(
        mapping["website_category"],
        mapping["label"]
    )
)

# ============================================================
# VARIABLES
# ============================================================

all_articles = []

seen_urls = set()

label_counts = {}

# initialize counts

for label in mapping["label"].unique():
    label_counts[label] = 0

# ============================================================
# SCRAPE
# ============================================================

for _, row in categories.iterrows():

    website_category = row["category"]

    label = category_to_label[website_category]

    # Skip if label already complete
    if label_counts[label] >= TARGET_PER_LABEL:

        print("\n" + "=" * 60)
        print(f"Skipping {website_category}")
        print(f"{label} already has {label_counts[label]} articles.")
        continue

    current_url = row["url"]

    page = 1

    print("\n" + "=" * 60)
    print("Website Category :", website_category)
    print("Final Label      :", label)

    while current_url:

        # Stop if label target reached
        if label_counts[label] >= TARGET_PER_LABEL:
            break

        print(f"\nPage {page}")
        print(current_url)

        try:

            response = requests.get(
                current_url,
                headers=HEADERS,
                timeout=15
            )

            response.raise_for_status()

        except requests.RequestException as e:

            print("Request failed:", e)
            break

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        article_links = set()

        # -----------------------------------
        # Find Story Links
        # -----------------------------------

        for link in soup.find_all("a", href=True):

            href = link["href"]

            if "/story/" not in href:
                continue

            full_url = urljoin(
                current_url,
                href
            )

            article_links.add(full_url)

        print(
            f"Found {len(article_links)} links"
        )

        # -----------------------------------
        # Save Unique Articles
        # -----------------------------------

        added_this_page = 0

        for article_url in article_links:

            if article_url in seen_urls:
                continue

            if label_counts[label] >= TARGET_PER_LABEL:
                break

            seen_urls.add(article_url)

            all_articles.append({

                "website": "Ratopati",

                "website_category": website_category,

                "label": label,

                "article_url": article_url

            })

            label_counts[label] += 1

            added_this_page += 1

        print(
            f"Added this page : {added_this_page}"
        )

        print(
            f"{label}: "
            f"{label_counts[label]}/{TARGET_PER_LABEL}"
        )

        # -----------------------------------
        # Next Page
        # -----------------------------------

        next_button = soup.find(
            "a",
            rel="next"
        )

        if next_button:

            current_url = urljoin(
                current_url,
                next_button["href"]
            )

            page += 1

            time.sleep(1)

        else:

            break

# ============================================================
# SAVE
# ============================================================

df = pd.DataFrame(all_articles)

print("\n" + "=" * 60)
print("Total collected:", len(df))

df.to_csv(
    "data/raw/ratopati/ratopati_article_links.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved!")
print("data/raw/ratopati/ratopati_article_links.csv")

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FINAL LABEL COUNTS")
print("=" * 60)

for label in sorted(label_counts):

    print(
        f"{label:25}"
        f"{label_counts[label]}"
    )