import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://www.news24nepal.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(BASE_URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

nav = soup.find("div", class_="navigation_boxs")

categories = []

seen = set()

for a in nav.find_all("a", href=True):

    href = a["href"]

    if not href.startswith("https://www.news24nepal.com"):
        continue

    title = a.get_text(strip=True)

    if title == "":
        continue

    if title == "गृहपृष्ठ":
        continue

    if href in seen:
        continue

    seen.add(href)

    categories.append({
        "website_category": title,
        "category_url": href
    })

df = pd.DataFrame(categories)

print(df)

df.to_csv(
    "data/raw/news24/categories.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:")
print("data/raw/news24/categories.csv")