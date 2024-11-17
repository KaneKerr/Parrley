import requests
import time
from apiLogic import calc_trades


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


# Function to calculate if the market is oversold
def over_sold():
    try:
        rsi_values = fetch_and_calculate_rsi(period=14)
        latest_rsi = rsi_values[-1]

        print(f"Latest RSI: {latest_rsi}")

        if latest_rsi < 30:
            print("Market is oversold. Making buy order...")
            calc_trades()
        elif latest_rsi > 70:
            print("Market is overbought. Consider selling.")
        else:
            print("Market is neutral. Waiting for next check.")
    except Exception as e:
        print(f"Error in RSI calculation: {e}")


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
    start_timestamp = current_timestamp - (7 * 24 * 60 * 60)  # 7 days instead of 14 days

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
