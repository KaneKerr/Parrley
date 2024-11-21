import datetime
import dotenv
from dotenv import load_dotenv
import requests

now = datetime.datetime.now().strftime("%Y-%m-%d")
load_dotenv()
api_key = dotenv.get_key("../.env", "news_api")


def newsFilter():
    urlbit = (
        f"https://newsapi.org/v2/top-headlines?q=bitcoin&category=business&from={now}&apiKey={api_key}"
    )

    urlbit2 = (
        f"https://newsapi.org/v2/top-headlines?q=BTC&category=business&from={now}&apiKey={api_key}"
    )

    urlfomc1 = (
        f"https://newsapi.org/v2/top-headlines?q=fomc&from={now}&apiKey={api_key}"
    )

    urlfomc2 = (
        f"https://newsapi.org/v2/top-headlines?q=federal reserve&from={now}&apiKey={api_key}"
    )

    urltrump = (
        f"https://newsapi.org/v2/top-headlines?q=trump&category=business&from={now}&sortBy=relevance&apiKey={api_key}"
    )

    #
    # response = requests.get(urlbit)
    # response2 = requests.get(urlfomc1)
    #
    # response3 = requests.get(urlbit2)
    # response4 = requests.get(urlfomc2)
    #
    # response5 = requests.get(urltrump)
    #
    # print(f"{response.json()}, \n {response2.json()} \n {response3.json()}, \n {response4.json()}, \n {response5.json()}")
