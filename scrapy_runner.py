from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from crypto_spider.crypto_spider.spiders.news_spider import NewsSpider

def run_scraper():

    settings = Settings()
    settings.set('BOT_NAME', 'news_spider')
    settings.set('ROBOTSTXT_OBEY', False)
    settings.set('ITEM_PIPELINES', {
        'crypto_spider.crypto_spider.pipelines.SaveToDatabasePipeline': 300,
    })
    settings.set('LOG_LEVEL', 'INFO')

    process = CrawlerProcess(settings)
    process.crawl(NewsSpider)
    process.start()  # <- This blocks until spider is done