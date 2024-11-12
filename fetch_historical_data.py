import ccxt
import pandas as pd

# Create an instance of the Binance exchange
exchange = ccxt.binance()

# Define the symbol and timeframe for the historical data
symbol = 'BTC/USDT'
timeframe = '1h'  # 1-hour candles
limit = 1000  # Number of data points to fetch

# Fetch the historical OHLCV data (Open, High, Low, Close, Volume)
ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

# Convert the data into a DataFrame for easier manipulation
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Convert timestamp to a readable date format
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Save the DataFrame to a CSV file
df.to_csv('btc_usdt_historical_data.csv', index=False)

print("Historical data saved to btc_usdt_historical_data.csv")
