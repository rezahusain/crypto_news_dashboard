from apscheduler.schedulers.background import BackgroundScheduler
from scrapy_runner import run_scraper  # This should be a clean function
from flask import Flask, render_template
from models import SessionLocal, NewsArticle
from datetime import datetime, timezone

app = Flask(__name__)
DATABASE_PATH ='instance/news.db'

last_updated = None

def scheduled_job():
    global last_updated
    run_scraper()
    last_updated = datetime.now(tz=timezone.utc)
    print(f"Scraped at {last_updated}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_job, trigger="interval", hours=1)
scheduler.start()

@app.route('/')
def index():
    # You can pass preview articles to the landing page too
    session = SessionLocal()
    sample_articles = session.query(NewsArticle).order_by(NewsArticle.published_at.desc()).limit(6).all()
    session.close()
    return render_template('landing_page.html', sample_articles=sample_articles, last_updated=last_updated)

@app.route('/news')
def news():
    session = SessionLocal()
    articles = session.query(NewsArticle).order_by(NewsArticle.published_at.desc()).all()
    session.close()
    return render_template('news.html', articles=articles, last_updated=last_updated)

if __name__ == '__main__':
    scheduled_job()
    app.run(debug=True)