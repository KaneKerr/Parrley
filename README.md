# Parrley Trading Bot
Parrley is a cryptocurrency trading bot that interacts with the Coinbase API to perform trading actions based on market conditions, specifically using technical indicators like the Relative Strength Index (RSI) and Exponential Moving Average (EMA). It can place buy orders based on market conditions, such as oversold scenarios where the price is lower than the EMA and the RSI is under 30.


## Setup:

To use Parrley, you will need to install the following dependencies:

```pip install coinbase dotenv requests pandas```

The bot interacts with the Coinbase API, so you'll need a Coinbase account and your API keys (API Key and API Secret).

Example usage in .env:

```
api_key=your_api_key_here
api_secret=your_api_secret_here
```

## Usage:

Fetches the account balances from Coinbase and checks if the GBP balance is available.
If GBP balance exists, it calculates the lot size (1% of the balance can be changed) and places a buy order for Bitcoin.

## File Descriptions:

Places a market buy order on Coinbase using the calculated lot size (in GBP) for the BTC-GBP pair and fetches the historical 1-hour candlestick data for the BTC-GBP trading pair from Coinbase for a specified time range, analyses  the current market by calculating the RSI and EMA values.

If the market is considered oversold (RSI < 30) and the price is in an uptrend (the price is above the 200 ema), it triggers a trade.

After the price of the asset has either gone up or down 5% it will trigger a sell acting as a stop-loss or take-profit.

## Dependencies:

To use Parrley, you will need to install the following dependencies:

```coinbase```: Used for interacting with the Coinbase Pro API.

```dotenv```: Used for loading API credentials from a .env file.

```requests```: Used for making HTTP requests to fetch market data (candlestick data).

```pandas```: Used for data manipulation and analysis.

```datetime, time```: Used for handling time-based logic and timestamps.

