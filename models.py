from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String)
    url = Column(String, nullable=False)
    source = Column(String)
    published_at = Column(DateTime)

# SQLite connection string
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
engine = create_engine(f"sqlite:///{os.path.join(BASE_DIR, 'instance/news.db')}")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)