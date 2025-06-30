import scrapy
import json
import os
from dotenv import load_dotenv

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["newsdata.io"]
    load_dotenv()

    def __init__(self, *args, **kwargs):
        self.api_key = os.getenv("API_KEY")
        self.base_url = "https://newsdata.io/api/1/news"
        self.query = "bitcoin"

    def start_requests(self):
        params = {
            "apikey": self.api_key,
            "q": self.query,
            "language": "en"
        }
        url = f"{self.base_url}?apikey={params['apikey']}&q={params['q']}&language={params['language']}"
        yield scrapy.Request(url=url, callback=self.parse, headers={'Accept': 'application/json'})

    def parse(self, response):
        try:
            data = json.loads(response.body)
            for article in data.get("results", []):
                yield {
                    "title": article.get("title"),
                    "link": article.get("link"),
                    "pubDate": article.get("pubDate"),
                    "source": article.get("source_id")
                }
        except Exception as e:
            self.logger.error(f"Failed to parse: {e}")
