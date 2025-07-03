from flask import Flask, render_template
import json
import sqlite3

app = Flask(__name__)
DATABASE_PATH ='instance/news.db'

@app.route('/')
def index():
    connect = sqlite3.connect(DATABASE_PATH)
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM news_articles;')

    news = cursor.fetchall()
    return render_template('index.html', articles=news)

if __name__ == '__main__':
    app.run(debug=True)