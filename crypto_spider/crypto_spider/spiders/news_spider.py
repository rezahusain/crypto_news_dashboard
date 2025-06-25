import scrapy

class NewsSpider(scrapy.Spider):

    name="news"

    allowed_domains = ["coindesk.com"]

    start_urls = ["https://www.coindesk.com/"]

    def parse(self, response):

        for article in response.css("div.card-title-wrapper"):
            pass