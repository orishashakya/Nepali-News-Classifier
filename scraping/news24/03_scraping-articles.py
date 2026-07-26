import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# ==================================================
# SETTINGS
# ==================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

session = requests.Session()
session.headers.update(HEADERS)

# ==================================================
# LOAD LINKS
# ==================================================

links = pd.read_csv(
    "data/raw/news24/news24_article_links.csv"
)

print(f"Loaded {len(links)} article URLs")

articles = []

# ==================================================
# SCRAPE
# ==================================================

for index, row in links.iterrows():

    url = row["article_url"]

    print("\n" + "=" * 70)
    print(f"[{index+1}/{len(links)}]")
    print(url)

    try:

        response = session.get(
            url,
            timeout=20
        )

        response.raise_for_status()

    except Exception as e:

        print("Request Failed:", e)
        continue

    soup = BeautifulSoup(
        response.text,
        "lxml"
    )

    # ------------------------------------------------
    # SAVE FIRST HTML FOR DEBUGGING
    # ------------------------------------------------

    if index == 0:

        with open(
            "debug_news24.html",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(response.text)

        print("Saved debug_news24.html")

    # ------------------------------------------------
    # TITLE
    # ------------------------------------------------

    title = ""

    selectors = [

        "span.news-title-inner",

        ".news-title-inner",

        ".title-showcase span",

        "div.title-showcase span",

        "h1",

        "title"

    ]

    for selector in selectors:

        tag = soup.select_one(selector)

        if tag:

            text = tag.get_text(
                " ",
                strip=True
            )

            if len(text) > len(title):

                title = text

    if title == "":

        print("Title NOT found")

        print("Page title:", soup.title)

    # ------------------------------------------------
    # CONTENT
    # ------------------------------------------------

    content = ""

    editor = soup.find(
        "div",
        class_="editor-box"
    )

    if editor:

        paragraphs = editor.find_all("p")

        texts = []

        for p in paragraphs:

            txt = p.get_text(
                " ",
                strip=True
            )

            if txt:

                texts.append(txt)

        content = " ".join(texts)

    print("Title length   :", len(title))
    print("Content length :", len(content))

    if len(content) < 100:

        print("Skipped")
        continue

    articles.append({

        "website": row["website"],

        "website_category": row["website_category"],

        "label": row["label"],

        "title": title,

        "content": content,

        "url": url

    })

    # ------------------------------------------------
    # AUTOSAVE
    # ------------------------------------------------

    if len(articles) % 25 == 0:

        pd.DataFrame(articles).to_csv(

            "data/raw/news24/news24.csv",

            index=False,

            encoding="utf-8-sig"

        )

        print(f"Autosaved {len(articles)} articles")

    time.sleep(random.uniform(1, 2))

# ==================================================
# FINAL SAVE
# ==================================================

df = pd.DataFrame(articles)

df.to_csv(

    "data/raw/news24/news24.csv",

    index=False,

    encoding="utf-8-sig"

)

print("\nFinished")

print(f"Saved {len(df)} articles")

print("\nLabel Distribution")

print(df["label"].value_counts())