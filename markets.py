import requests

def get_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency" : "usd",
        "order" : "market_cap_desc",
        "per_page" : 10,
        "page" : 1,
        "sparkline" : False
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data
    except Exception as e:
        print("Error fetching market data:", e)
        return []