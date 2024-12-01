import requests
import time
from apiLogic import calc_trades, calc_trades_scary



def fetch_candles(start_timestamp, end_timestamp):
    url = f"https://api.exchange.coinbase.com/products/BTC-GBP/candles?granularity=3600"
    params = {
        "start": time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(start_timestamp)),
        "end": time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(end_timestamp)),
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()  # Returns candle data
    else:
        print(f"Error fetching candles: {response.status_code} - {response.text}")
        return []


def over_sold():
    try:
        rsi_values = fetch_and_calculate_rsi(period=14)
        ema_values = fetch_and_calculate_ema(period=200)

        latest_rsi = rsi_values[-1]
        latest_ema = ema_values[-1]

        # Latest closing price (from the most recent candle)
        current_price = float(fetch_candles(int(time.time()) - 3600, int(time.time()))[-1][4])

        print(f"Latest RSI: {latest_rsi}")
        print(f"Latest EMA: {latest_ema}")
        print(f"Current price: {current_price}")

        vol = daily_candles()

        # Check if the current price is above or below the EMAs
        if current_price > latest_ema and latest_rsi < 30 and vol:
            print("Market is bullish and OverSold. The current price is above the EMA and the RSI is below 30 but "
                  "very volatile.")
            calc_trades_scary()
        elif current_price > latest_ema and latest_rsi < 30 and not vol:
            print("Market is bullish and OverSold. The current price is above the EMA and the RSI is below 30.")
            calc_trades()
        elif current_price < latest_ema and latest_rsi < 30:
            print(
                "Market is bearish. The current price is below the EMA but the market is OverSold. The RSI is below 30.")
        elif latest_rsi > 30 and latest_ema > current_price:
            print("Market is over 30 rsi and EMA is above the current price, the RSI is above 30.")
        elif current_price > latest_ema and latest_rsi > 70:
            print("Market is bullish but overbought. The current price is above the EMA and the RSI is above 70.")
        elif current_price < latest_ema and latest_rsi > 70:
            print("Market is bearish and overbought. The current price is below the EMA and the RSI is above 70.")
        elif current_price > latest_ema and 30 <= latest_rsi <= 70:
            print("Market is bullish but neutral. The current price is above the EMA and the RSI is between 30 and 70.")
        else:
            print("Market is neutral. The current price is equal to the EMA or the RSI is between 30 and 70.")
    except Exception as e:
        print(f"Error in RSI or EMA calculation: {e}")


# Function to calculate the RSI
def calculate_rsi(prices, period=14):
    """
    Calculate the Relative Strength Index (RSI) for a list of closing prices.
    """
    if len(prices) < period:
        raise ValueError("Not enough data to calculate RSI")

    # price change
    changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]

    # Separate gains and losses
    gains = [max(change, 0) for change in changes]
    losses = [-min(change, 0) for change in changes]

    # Calculate average gain and average loss
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    rsi_values = []
    for i in range(period, len(prices)):
        gain = gains[i - 1]
        loss = losses[i - 1]

        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        rsi_values.append(rsi)

    return rsi_values


def fetch_and_calculate_rsi(period=14):
    current_timestamp = int(time.time())
    start_timestamp = current_timestamp - (12 * 24 * 60 * 60) # highest period we can go with coinbase

    candles = fetch_candles(
        start_timestamp=start_timestamp,
        end_timestamp=current_timestamp,
    )

    if not candles:
        raise RuntimeError("Failed to fetch candle data")

    # Extract closing prices from the fetched candles
    prices = [float(candle[4]) for candle in candles]

    # Calculate RSI based on the closing prices
    return calculate_rsi(prices, period=period)


def calculate_ema(prices, period=200):
    if len(prices) < period:
        raise ValueError("Not enough data to calculate EMA")

    # Calculate the smoothing factor
    alpha = 2 / (period + 1)

    # Initialize EMA with the first price
    ema_values = [prices[0]]

    # Calculate the EMA for each subsequent price
    for price in prices[1:]:
        new_ema = (price * alpha) + (ema_values[-1] * (1 - alpha))
        ema_values.append(new_ema)

    return ema_values


# Fetch and calculate EMA
def fetch_and_calculate_ema(period=200):
    current_timestamp = int(time.time())
    start_timestamp = current_timestamp - (9 * 24 * 60 * 60)

    candles = fetch_candles(
        start_timestamp=start_timestamp,
        end_timestamp=current_timestamp,
    )

    if not candles:
        raise RuntimeError("Failed to fetch candle data")

    # Extract closing prices from the fetched candles
    prices = [float(candle[4]) for candle in candles]

    # Calculate EMA based on the closing prices
    return calculate_ema(prices, period=period)


def daily_candles():
    current_timestamp = int(time.time())
    start_timestamp = current_timestamp - (24 * 60 * 60)

    url = "https://api.exchange.coinbase.com/products/BTC-GBP/candles"

    params = {
        "start": time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(start_timestamp)),
        "end": time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(current_timestamp)),
        "granularity": 86400
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        candles = response.json()

        if candles:
            highest_price = candles[0][2]
            lowest_price = candles[0][1]

            diff = highest_price - lowest_price
            avg = (highest_price + lowest_price) / 2
            to_decimal = diff / avg
            change = float(round(to_decimal * 100, 2))
            print(f"Change: {change}%")

            if change > 5:
                return True
            else:
                return False
        else:
            return "No Candle Data"
    else:
        print(f"Error fetching daily candles: {response.status_code} - {response.text}")
        return None, None
