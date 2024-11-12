import ccxt

# Create an instance of the Binance exchange
exchange = ccxt.binance()

# Fetch the current price of Bitcoin
symbol = 'BTC/USDT'
ticker = exchange.fetch_ticker(symbol)

# Print the current price
print(f"The current price of {symbol} is {ticker['last']}")
