import sys
# Install the asyncio reactor before importing scrapy or crochet
from twisted.internet import asyncioreactor
import asyncio
# Force SelectorEventLoop on Windows (instead of ProactorEventLoop)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncioreactor.install()
from math import ceil
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import or_
from scrapy_runner import run_spider
from flask import Flask, render_template, request
from models import SessionLocal, NewsArticle
import atexit

app = Flask(__name__)
DATABASE_PATH ='instance/news.db'

def get_last_updated():
    session = SessionLocal()
    latest_article = session.query(NewsArticle).order_by(NewsArticle.published_at.desc()).first()
    session.close()
    return latest_article.published_at.strftime('%b %d, %Y %I:%M %p') if latest_article else "N/A"


# Define the scheduled job
def scheduled_job():
    print("Scheduled job started")
    try:
        run_spider()
        print("Scheduled job completed")
    except Exception as e:
        print(f"Scheduled job failed: {e}")

# Create the scheduler and add the job
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=scheduled_job,
    trigger="interval",
    hours=1,
    misfire_grace_time=3600,
    id="scrapy_job"
)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

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
    query = session.query(NewsArticle)

    # Keyword Search
    search = request.args.get("q")
    if search:
        query = query.filter(or_(
            NewsArticle.title.ilike(f"%{search}%"),
            NewsArticle.summary.ilike(f"%{search}%")
        ))

    # Source Filter
    source = request.args.get("source")
    if source:
        query = query.filter(NewsArticle.source == source)

    # Sorting
    sort_order = request.args.get("sort", "desc")
    if sort_order == "asc":
        query = query.order_by(NewsArticle.published_at.asc())
    else:
        query = query.order_by(NewsArticle.published_at.desc())
    
    # Source Dropdown
    sources = session.query(NewsArticle.source).distinct().all()
    source_list = [s[0] for s in sources if s[0]]

    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = 9
    offset = (page - 1) * per_page

    # Get total count for pagination controls
    total_articles = session.query(NewsArticle).count()
    total_pages = ceil(total_articles / per_page)

    # Get the subset of articles for this page
    articles = (
        query
        .offset(offset)
        .limit(per_page)
        .all()
    )

    session.close()

    return render_template(
        'news.html',
        articles=articles,
        sources=source_list,
        current_page=page,
        total_pages=total_pages,
        last_updated=get_last_updated()
    )

if __name__ == '__main__':
    scheduled_job()
    app.run(debug=True, use_reloader=False)