from flask import Flask, render_template
from models import SessionLocal, NewsArticle
from datetime import datetime

app = Flask(__name__)
DATABASE_PATH ='instance/news.db'

@app.route('/')
def index():
    # You can pass preview articles to the landing page too
    session = SessionLocal()
    sample_articles = session.query(NewsArticle).order_by(NewsArticle.published_at.desc()).limit(6).all()
    session.close()
    return render_template('landing_page.html', sample_articles=sample_articles)

@app.route('/news')
def news():
    session = SessionLocal()
    articles = session.query(NewsArticle).order_by(NewsArticle.published_at.desc()).all()
    session.close()
    return render_template('news.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)