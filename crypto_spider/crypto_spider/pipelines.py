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

        try:
            pub_date = item.get("published_at")

            from datetime import datetime

            if isinstance(pub_date, str):
                try:
                    pub_date = datetime.strptime(pub_date, "%Y-%m-%d %H:%M")
                except ValueError:
                    try:
                        pub_date = datetime.strptime(pub_date, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        pub_date = None

            # Prepares the NewsArticle object for insertion into db
            article = NewsArticle(
                title=item.get("title") or "Untitled",
                summary=item.get("summary") or "", 
                url=item.get("url"),
                source=item.get("source") or "unknown",
                published_at=pub_date
            )
            self.session.add(article)
            self.session.commit()
            spider.logger.info(f"Article saved: {item.get('title')}")
        except IntegrityError as e:
            self.session.rollback()
            spider.logger.error(f"Failed to insert item: {e}")
        return item
    
    def close_spider(self, spider):
        self.session.close()