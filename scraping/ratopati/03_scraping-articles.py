import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --------------------------------------------------
# Headers
# --------------------------------------------------
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

# --------------------------------------------------
# Read article links
# --------------------------------------------------
articles_df = pd.read_csv(
    "data/raw/ratopati/ratopati_article_links.csv"
)

scraped_articles = []

print(f"Total articles to scrape: {len(articles_df)}")

# --------------------------------------------------
# Loop through every article
# --------------------------------------------------
for index, row in articles_df.iterrows():

    website = row["website"]
    website_category = row["website_category"]
    label = row["label"]
    article_url = row["article_url"]

    print("\n" + "=" * 60)
    print(f"[{index + 1}/{len(articles_df)}]")
    print(article_url)

    # ----------------------------------------------
    # Download page
    # ----------------------------------------------
    try:

        response = requests.get(
            article_url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

    except requests.RequestException as e:

        print("Request failed:", e)
        continue

    soup = BeautifulSoup(
        response.text,
        "lxml"
    )

    # ----------------------------------------------
    # Extract Title
    # ----------------------------------------------
    title = ""

    title_tag = soup.find(
        "h2",
        class_="heading"
    )

    if title_tag:

        title = title_tag.get_text(
            " ",
            strip=True
        )

    # ----------------------------------------------
    # Extract Article Content
    # ----------------------------------------------
    content = ""

    content_div = soup.find(
        "div",
        class_="the-content"
    )

    if content_div:

        paragraphs = content_div.find_all("p")

        content = " ".join(

            p.get_text(
                " ",
                strip=True
            )

            for p in paragraphs

        )

    # ----------------------------------------------
    # Skip bad pages
    # ----------------------------------------------
    if title == "":

        print("Skipped: No title")

        continue

    if len(content) < 100:

        print("Skipped: Content too short")

        continue

    # ----------------------------------------------
    # Save article
    # ----------------------------------------------
    scraped_articles.append({

        "website": website,

        "website_category": website_category,

        "label": label,

        "title": title,

        "content": content,

        "article_url": article_url

    })

    print("Saved")

    time.sleep(1)

# --------------------------------------------------
# Save CSV
# --------------------------------------------------
df = pd.DataFrame(scraped_articles)

print("\n" + "=" * 60)
print(f"Articles scraped: {len(df)}")

df.to_csv(

    "data/raw/ratopati/ratopati_articles.csv",

    index=False,

    encoding="utf-8-sig"

)

print("\nSaved successfully!")
print("File: data/raw/ratopati/ratopati_articles.csv")