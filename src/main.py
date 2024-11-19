from apiLogic import *
from botLogic import over_sold
import time


def main():
    while True:
        over_sold()
        time.sleep(3600)


if __name__ == "__main__":
    main()
