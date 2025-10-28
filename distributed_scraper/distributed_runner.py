from dask.distributed import Client, as_completed
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from distributed_scraper.spiders.example_spider import ExampleSpider

def run_spider(url):
    process = CrawlerProcess(get_project_settings())
    process.crawl(ExampleSpider, start_urls=[url])
    process.start()

if __name__ == "__main__":
    client = Client()
    urls = [
           "https://quotes.toscrape.com/",
            "https://books.toscrape.com/"
    ]
    futures = [client.submit(run_spider, u) for u in urls]
    for f, _ in as_completed(futures, with_results=True):
        print("Finished:", f)
