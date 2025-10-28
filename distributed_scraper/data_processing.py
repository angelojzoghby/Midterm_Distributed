import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["scraper_db"]
collection = db["cleaned_data"]

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())

with open("output.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

cleaned_records = []
for item in raw_data:
    combined = " ".join(item.get("paragraphs", []))
    cleaned = {
        "url": item.get("url"),
        "clean_text": clean_html(combined),
        "timestamp": datetime.now().isoformat()
    }
    cleaned_records.append(cleaned)
    collection.insert_one(cleaned)

print(f"✅ Inserted {len(cleaned_records)} cleaned documents.")
print("Sample document:")
print(cleaned_records[0])