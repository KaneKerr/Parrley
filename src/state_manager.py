import json
from threading import Lock

order_state = {}
order_state_lock = Lock()

STATE_FILE = "order_state.json"


def load_order_state():
    global order_state
    try:
        with open(STATE_FILE, "r") as f:
            order_state = json.load(f)
            print("Order state loaded:", order_state)
    except FileNotFoundError:
        order_state = {}


def save_order_state():
    with order_state_lock:
        with open(STATE_FILE, "w") as f:
            json.dump(order_state, f)
            print("Order state saved.")
