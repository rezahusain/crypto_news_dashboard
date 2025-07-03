import scrapy
import json
import os
from dotenv import load_dotenv
from datetime import datetime

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["newsdata.io"]
    # Loads the API key from env file 
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
            # Creates a json array for each article
            # in order to be accessed by pipeline
            for article in data.get("results", []):
                yield {
                    "title": article.get("title"),
                    "summary" : article.get("description"),
                    "url": article.get("link"),
                    "source": article.get("source_name"),
                    "published_at": article.get("pubDate")
                }
        except Exception as e:
            self.logger.error(f"Failed to parse: {e}")
