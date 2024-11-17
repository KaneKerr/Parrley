from apiLogic import *
from botLogic import over_sold
import time


def main():
    while True:  # Loop to keep the process running continuously
        get_btc_gbp_price()
        over_sold()
        time.sleep(120)


if __name__ == "__main__":
    main()
