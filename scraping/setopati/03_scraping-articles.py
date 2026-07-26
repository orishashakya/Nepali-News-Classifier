import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ----------------------------
# Headers
# ----------------------------
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

# ----------------------------
# Read article links
# ----------------------------
df_links = pd.read_csv(
    "data/raw/setopati/setopati_article_links.csv"
)

articles = []

print(f"Found {len(df_links)} article links.\n")

# ----------------------------
# Loop through articles
# ----------------------------
for i, row in df_links.iterrows():

    article_url = row["article_url"]
    website = row["website"]
    website_category = row["website_category"]
    label = row["label"]

    print("=" * 60)
    print(f"{i+1}/{len(df_links)}")
    print(article_url)

    try:

        response = requests.get(
            article_url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

    except requests.RequestException as e:

        print("Request failed:", e)
        continue

    soup = BeautifulSoup(response.text, "lxml")

    # -------------------------------------------------
    # Title
    # -------------------------------------------------
    title = ""

    title_tag = soup.find(
        "h1",
        class_="news-big-title"
    )

    if title_tag:
        title = title_tag.get_text(" ", strip=True)

    # -------------------------------------------------
    # Content
    # -------------------------------------------------
    content = ""

    content_div = soup.find(
        "div",
        class_="editor-box"
    )

    if content_div:

        # Remove advertisements
        for tag in content_div.find_all(
            "div",
            class_=["insert-ad", "media-ad-item"]
        ):
            tag.decompose()

        # Remove iframes
        for tag in content_div.find_all("iframe"):
            tag.decompose()

        # Remove blockquotes
        for tag in content_div.find_all("blockquote"):
            tag.decompose()

        paragraphs = content_div.find_all("p")

        content = " ".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )

    # -------------------------------------------------
    # Save article
    # -------------------------------------------------
    articles.append({

        "website": website,

        "website_category": website_category,

        "label": label,

        "title": title,

        "content": content,

        "article_url": article_url

    })

    time.sleep(1)

# ----------------------------
# Save CSV
# ----------------------------
df = pd.DataFrame(articles)

print("\n" + "=" * 60)
print("Scraped articles:", len(df))

df.to_csv(
    "data/raw/setopati/setopati.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved successfully!")
print("data/raw/setopati/setopati_articles.csv")