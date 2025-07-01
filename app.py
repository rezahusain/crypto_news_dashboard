from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('bitcoin_news.json', 'r', encoding='utf-8') as f:
        news = json.load(f)
    return render_template('crypto_spider/index.html', articles=news)

if __name__ == '__main__':
    app.run(debug=True)