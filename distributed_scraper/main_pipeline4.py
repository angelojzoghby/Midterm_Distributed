import queue
import threading
from dask.distributed import Client, as_completed
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from distributed_scraper.spiders.example_spider import ExampleSpider

url_queue = queue.Queue()

def producer():
    urls = [
        "https://quotes.toscrape.com/",
        "https://books.toscrape.com/",
    ]
    for u in urls:
        print(f"[Producer] Enqueued: {u}")
        url_queue.put(u)
    print("[Producer] ✅ Finished enqueueing URLs")

def run_spider(url):
    process = CrawlerProcess(get_project_settings())
    process.crawl(ExampleSpider, start_urls=[url])
    process.start()

def consumer():
    client = Client()
    tasks = []
    while not url_queue.empty():
        url = url_queue.get()
        print(f"[Consumer] Dispatching worker for {url}")
        tasks.append(client.submit(run_spider, url))
    for f, _ in as_completed(tasks, with_results=True):
        print("✅ Completed one scraping job")
    client.close()
    print("[Consumer] ✅ All tasks completed")

if __name__ == "__main__":
    print("🚀 Starting Step 2 Full Pipeline")
    producer_thread = threading.Thread(target=producer)
    producer_thread.start()
    producer_thread.join()
    consumer()
    print("🏁 Step 2 Pipeline finished successfully.")
