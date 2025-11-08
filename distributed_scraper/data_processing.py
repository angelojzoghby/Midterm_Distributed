import json
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["scraper_db"]
collection = db["cleaned_data"]


def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())


def clean_and_store(url: str):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[WARN] Skipping {url}, status {response.status_code}")
            return

        cleaned_text = clean_html(response.text)
        doc = {
            "url": url,
            "clean_text": cleaned_text,
            "timestamp": datetime.utcnow().isoformat(),
        }
        collection.insert_one(doc)
        print(f"[OK] Cleaned and stored: {url}")
    except Exception as e:
        print(f"[ERROR] Failed to process {url}: {e}")
