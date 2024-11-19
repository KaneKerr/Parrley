from coinbase.rest import RESTClient
import dotenv
from dotenv import load_dotenv
from json import dumps
import time
import threading

order_state = {}

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
            lot = round(lot)
            lot = str(lot)
            make_order(lot)
            break


def monitor_price(order_id, lot, take, stop):
    while order_id in order_state:
        get_price = client.get_product("BTC-GBP")
        current_price = float(get_price["price"])

        print(f"fetched current price: , {current_price}")

        if current_price >= take:
            print(f"Take profit reached at {current_price:.3f}")
            take_profit(f"trade taken {current_price}", lot)
            order_state.pop(order_id)
            break
        elif current_price <= stop:
            print(f"Stop loss reached at {current_price:.3f}")
            stop_loss(f"trade lost {current_price}", lot)
            order_state.pop(order_id)
            break

        time.sleep(1800)


def make_order(lot):
    order = client.market_order_buy(
        client_order_id="",
        product_id="BTC-GBP",
        quote_size=lot,
    )

    if 'success_response' in order:
        order_id = order['success_response']['order_id']

        # Get the price at the time of the order
        price_at_buy = client.get_product("BTC-GBP")
        btc_gbp_price = float(price_at_buy["price"])

        # Calculate take profit and stop loss based on the price
        take = btc_gbp_price * 1.05
        stop = btc_gbp_price * 0.95

        print(f"Take profit price: {take:.3f}")
        print(f"Stop loss price: {stop:.3f}")

        order_state[order_id] = {}

        # new thread to ignore other sleep
        monitoring_thread = threading.Thread(target=monitor_price, args=(order_id, lot, take, stop))
        monitoring_thread.daemon = True
        monitoring_thread.start()

    elif 'error_response' in order:
        error_response = order['error_response']
        print(error_response)


def take_profit(current_price, lot):
    take_profit_price = current_price * 1.05
    print(f"Take profit price: {take_profit_price}")

    tp = lot * 1.05

    order = client.market_order_sell(
        client_order_id="",
        product_id="BTC-GBP",
        base_size=tp,
    )

    if 'success_response' in order:
        order_id = order['success_response']['order_id']
        fills = client.get_fills(order_id=order_id)
        print(dumps(fills, indent=2))
    elif 'error_response' in order:
        error_response = order['error_response']
        print(error_response)


def stop_loss(current_price, lot):
    stop_loss_price = current_price * 0.95
    print(f"Stop loss price: {stop_loss_price}")

    sl = lot * 0.95

    order = client.market_order_sell(
        client_order_id="",
        product_id="BTC-GBP",
        base_size=sl,
    )

    if 'success_response' in order:
        order_id = order['success_response']['order_id']
        fills = client.get_fills(order_id=order_id)
        print(dumps(fills, indent=2))
    elif 'error_response' in order:
        error_response = order['error_response']
        print(error_response)
