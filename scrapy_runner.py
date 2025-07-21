# scrapy_runner.py

from crochet import setup, wait_for
setup()

from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from crypto_spider.crypto_spider.spiders.news_spider import NewsSpider

settings = Settings()
settings.set('BOT_NAME', 'news_spider')
settings.set('ROBOTSTXT_OBEY', False)
settings.set('ITEM_PIPELINES', {
    'crypto_spider.crypto_spider.pipelines.SaveToDatabasePipeline': 300,
})
settings.set('LOG_LEVEL', 'INFO')

runner = CrawlerRunner(settings)

@wait_for(timeout=60.0)  # This will block until crawl is complete or timeout
def run_spider():
    return runner.crawl(NewsSpider)
