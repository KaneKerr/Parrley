from newsFilter import get_news
import time


def main():
    while True:
        get_news()
        time.sleep(3600)


if __name__ == "__main__":
    main()
