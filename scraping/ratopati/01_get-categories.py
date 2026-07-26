import requests
from bs4 import BeautifulSoup
import pandas as pd

HOME_URL = "https://www.ratopati.com"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

response = requests.get(HOME_URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

nav = soup.find("nav", class_="nav-menu")

categories = []

seen = set()

for a in nav.find_all("a", href=True):

    name = a.get_text(strip=True)
    url = a["href"]

    # Skip empty names
    if not name:
        continue

    # Skip anchors
    if url.endswith("#"):
        continue

    # Skip duplicate URLs
    if url in seen:
        continue

    seen.add(url)

    categories.append({
        "category": name,
        "url": url
    })

df = pd.DataFrame(categories)

print(df)

df.to_csv(
    "data/raw/ratopati/ratopati_categories.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"\nSaved {len(df)} categories.")