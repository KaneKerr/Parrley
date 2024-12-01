from coinbase.rest import RESTClient
import dotenv
from dotenv import load_dotenv
from json import dumps
import time
import threading
from state_manager import order_state, save_order_state, order_state_lock

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


# if vol
def calc_trades_scary():
    # Get all accounts
    accounts = client.get_accounts()
    print("working")

    for account in accounts.accounts:
        if account["currency"] == "GBP":
            gbp_balance = account["available_balance"]["value"]
            print(f"GBP Balance: {gbp_balance}")

            lot = float(gbp_balance) / 150
            lot = round(lot)
            lot = str(lot)
            make_order(lot)
            break


def monitor_price(order_id, lot, take, stop, btc_gbp_price):
    print(f"Current order state: {order_state}")
    print("Monitor thread started.")

    try:
        while order_id in order_state:
            get_price = client.get_product("BTC-GBP")
            current_price = float(get_price["price"])

            if current_price >= take / 2:
                print(f"Moving stop loss to break-even: {btc_gbp_price:.3f}")
                stop = btc_gbp_price

            if current_price >= take:
                print(f"Take profit reached at {current_price:.3f}")
                take_profit(lot)
                with order_state_lock:
                    order_state.pop(order_id, None)
                    save_order_state()
                break

            elif current_price <= stop:
                print(f"Stop loss reached at {current_price:.3f}")
                stop_loss(lot)
                with order_state_lock:
                    order_state.pop(order_id, None)
                    save_order_state()
                break

            time.sleep(1800)
    except Exception as e:
        print(f"Error in monitor_price: {e}")


def make_order(lot):
    if len(order_state) >= 5:
        print("Maximum number of orders reached. Exiting.")
        return
    else:
        order = client.market_order_buy(
            client_order_id="",
            product_id="BTC-GBP",
            quote_size=lot,
        )

        if hasattr(order, 'success') and order.success:
            order_id = order.response['order_id']
            price_at_buy = client.get_product("BTC-GBP")
            btc_gbp_price = float(price_at_buy["price"])

            take = btc_gbp_price * 1.10
            stop = btc_gbp_price * 0.90

            with order_state_lock:
                if order_id not in order_state:
                    order_state[order_id] = {
                        "lot": lot,
                        "take": take,
                        "stop": stop
                    }
                    save_order_state()

                    # Start monitoring in a thread
                    monitoring_thread = threading.Thread(
                        target=monitor_price,
                        args=(order_id, lot, take, stop, btc_gbp_price)
                    )
                    monitoring_thread.daemon = True
                    monitoring_thread.start()
                else:
                    print(f"Order with ID {order_id} already exists.")


def take_profit(lot):
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


def partial_take_profit(lot):
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


def stop_loss(lot):
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
