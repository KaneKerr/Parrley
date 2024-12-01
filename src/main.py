from apiLogic import monitor_price
from state_manager import load_order_state, order_state
import threading
import time
from newsFilter import get_news


def resume_monitoring():
    for order_id, trade_data in order_state.items():
        monitoring_thread = threading.Thread(
            target=monitor_price,
            args=(
                order_id,
                trade_data["lot"],
                trade_data["take"],
                trade_data["stop"],
                None
            )
        )
        monitoring_thread.daemon = True
        monitoring_thread.start()
        print(f"Resumed monitoring for Order ID: {order_id}")


def main():
    load_order_state()
    resume_monitoring()

    while True:
        get_news()
        time.sleep(3600)


if __name__ == "__main__":
    main()
