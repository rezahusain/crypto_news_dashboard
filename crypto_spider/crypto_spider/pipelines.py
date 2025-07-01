# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from models import SessionLocal, NewsArticle
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class SaveToDatabasePipeline:

    def __init__(self):
        self.session = SessionLocal()
    
    def process_item(self, item, spider):
        article = NewsArticle(
            title=item.get("title"),
            summary=item.get("description") or "",  # if using NewsData API
            url=item.get("link"),
            source=item.get("source") or item.get("source_id"),
            published_at=datetime.fromisoformat(item.get("pubDate")) if item.get("pubDate") else None
        )
        try:
            self.session.add(article)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
        return item
    
    def close_spider(self, spider):
        self.session.close()