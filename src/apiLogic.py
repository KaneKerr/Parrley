from coinbase.rest import RESTClient
import dotenv
from dotenv import load_dotenv
from json import dumps

load_dotenv()
api_key = dotenv.get_key("../.env", "api_key")
api_secret = dotenv.get_key("../.env", "api_secret")

# Initialize Coinbase client
client = RESTClient(api_key=api_key, api_secret=api_secret)


def calc_trades():
    # Get all accounts
    accounts = client.get_accounts()

    for account in accounts.accounts:
        if account["currency"] == "GBP":
            gbp_balance = account["available_balance"]["value"]
            print(f"GBP Balance: {gbp_balance}")

            lot = float(gbp_balance) / 100
            lot = str(lot)
            make_order(lot)
            break


def get_btc_gbp_price():
    product = client.get_product("BTC-GBP")
    btc_gbp_price = float(product["price"])
    print(f"Current BTC-GBP price: {btc_gbp_price}")


def make_order(lot):
    order = client.market_order_buy(
        client_order_id="",
        product_id="BTC-GBP",
        quote_size=lot,
    )

    if 'success_response' in order:
        order_id = order['success_response']['order_id']
        fills = client.get_fills(order_id=order_id)
        print(dumps(fills, indent=2))
    elif 'error_response' in order:
        error_response = order['error_response']
        print(error_response)
