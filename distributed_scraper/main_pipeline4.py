import json, time, sys, subprocess
from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dask.distributed import Client, as_completed

client_db = MongoClient("mongodb://localhost:27017/")
db = client_db["scraper_db"]
collection = db["cleaned_data"]

def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())

def insert_to_mongo(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not data:
            return
        for item in data:
            combined = " ".join(item.get("paragraphs", []))
            doc = {
                "url": item.get("url"),
                "clean_text": clean_html(combined),
                "timestamp": datetime.now().isoformat()
            }
            collection.insert_one(doc)
        print(f"Inserted {len(data)} records from {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON in {file_path}")

def run_command(url):
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_")
    output_file = f"output_{safe_name}.json"
    cmd = [sys.executable, "-m", "scrapy", "crawl", "example", "-a", f"start_urls={url}", "-O", output_file]
    subprocess.run(cmd)
    insert_to_mongo(output_file)
    print(f"Finished crawl for {url}")

if __name__ == "__main__":
    urls = [
        "https://edition.cnn.com/",
        "https://www.bbc.com/news",
        "https://techcrunch.com/",
        "https://www.theguardian.com/international",
    ]
    client = Client()
    futures = [client.submit(subprocess.run, [sys.executable, "-m", "scrapy", "crawl", "example", "-a", f"start_urls={u}", "-O", f"output_{u.replace('https://', '').replace('http://', '').replace('/', '_')}.json"]) for u in urls]
    for f, _ in as_completed(futures, with_results=True):
        pass
    for u in urls:
        safe_name = u.replace("https://", "").replace("http://", "").replace("/", "_")
        insert_to_mongo(f"output_{safe_name}.json")
    client.close()
    print("All scraping and cleaning tasks done.")
