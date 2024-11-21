from newsFilter import newsFilter
from botLogic import over_sold
import time


def main():
    while True:
        over_sold()
        newsFilter()
        time.sleep(3600)


if __name__ == "__main__":
    main()
