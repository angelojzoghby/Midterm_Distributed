import queue
import threading
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from distributed_scraper.spiders.example_spider import ExampleSpider

url_queue = queue.Queue()

def producer():
    urls = [
        "https://quotes.toscrape.com/",
        "https://books.toscrape.com/",
    ]
    for url in urls:
        print(f"[Producer] Enqueued: {url}")
        url_queue.put(url)
        time.sleep(0.5)
    print("[Producer] Done adding URLs")

def consumer():
    while True:
        try:
            url = url_queue.get(timeout=3)
            print(f"[Consumer] Consuming: {url}")
            process = CrawlerProcess(get_project_settings())
            process.crawl(ExampleSpider, start_urls=[url])
            process.start()
            print(f"[Consumer] Finished: {url}")
        except queue.Empty:
            break

if __name__ == "__main__":
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()
    consumer_thread.join()
    print("✅ All scraping tasks completed")
