from math import ceil
from apscheduler.schedulers.background import BackgroundScheduler
from scrapy_runner import run_scraper
from flask import Flask, render_template, request
from models import SessionLocal, NewsArticle

app = Flask(__name__)
DATABASE_PATH ='instance/news.db'

def get_last_updated():
    session = SessionLocal()
    latest_article = session.query(NewsArticle).order_by(NewsArticle.published_at.desc()).first()
    session.close()
    return latest_article.published_at.strftime('%b %d, %Y %I:%M %p') if latest_article else "N/A"

def scheduled_job():
    run_scraper()

scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_job, trigger="interval", hours=1, misfire_grace_time=3600)
scheduler.start()

@app.route('/')
def index():
    # You can pass preview articles to the landing page too
    session = SessionLocal()
    sample_articles = (session.query(NewsArticle)
                       .order_by(NewsArticle.published_at.desc())
                       .limit(6)
                       .all())
    session.close()
    return render_template('landing_page.html', sample_articles=sample_articles, last_updated=get_last_updated())


@app.route('/news')
def news():
    session = SessionLocal()

    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = 9
    offset = (page - 1) * per_page

    # Get total count for pagination controls
    total_articles = session.query(NewsArticle).count()
    total_pages = ceil(total_articles / per_page)

    # Get the subset of articles for this page
    articles = (
        session.query(NewsArticle)
        .order_by(NewsArticle.published_at.desc())
        .offset(offset)
        .limit(per_page)
        .all()
    )

    session.close()

    return render_template(
        'news.html',
        articles=articles,
        current_page=page,
        total_pages=total_pages,
        last_updated=get_last_updated()
    )

if __name__ == '__main__':
    #scheduled_job()
    app.run(debug=True)