import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.setopati.com"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

nav = soup.find("div", class_="navigation_box")

categories = []

seen = set()

for a in nav.find_all("a", href=True):

    name = a.get_text(strip=True)
    href = a["href"]

    if not name:
        continue

    if href.startswith("javascript"):
        continue

    if "search" in href:
        continue

    if href in seen:
        continue

    seen.add(href)

    categories.append({
        "category": name,
        "url": href
    })

df = pd.DataFrame(categories)

print(df)

df.to_csv(
    "data/raw/setopati/setopati_categories.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved", len(df), "categories.")