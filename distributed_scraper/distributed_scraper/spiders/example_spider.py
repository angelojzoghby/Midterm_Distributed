import scrapy
from bs4 import BeautifulSoup

class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = ["https://example.com"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        yield {
            "url": response.url,
            "paragraphs": paragraphs
        }
