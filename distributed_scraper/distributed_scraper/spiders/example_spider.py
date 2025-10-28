import scrapy
from bs4 import BeautifulSoup

class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = []

    def __init__(self, start_urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if start_urls:
            self.start_urls = [u.strip() for u in start_urls.split(",") if u.startswith("http")]
        else:
            self.start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        yield {
            "url": response.url,
            "paragraphs": paragraphs
        }
