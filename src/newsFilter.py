import datetime
import dotenv
from dotenv import load_dotenv
import requests
from botLogic import over_sold

today = datetime.datetime.now().date()
load_dotenv()
api_key = dotenv.get_key("../.env", "news_api")


def get_news():
    url = "https://crypto-news16.p.rapidapi.com/news/coincu"

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "crypto-news16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    filtered_data = []

    filters = ["bitcoin", "btc", "coinbase", "fomc", "warren buffett", "eth", "ethereum", "ether"]

    for article in data:
        try:
            article_date = datetime.datetime.strptime(article['date'], "%a, %d %b %Y %H:%M:%S %z").date()
            for filter1 in filters:
                if filter1 in article['title'].lower() and article_date >= today:
                    filtered_data.append(article)
        except ValueError:
            continue

    if len(filtered_data) < 5:
        print("Not enough news running bot")
        over_sold()
    else:
        print(filtered_data)
        print("Too much news")
