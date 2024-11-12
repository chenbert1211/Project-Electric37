import ccxt
import pandas as pd
import joblib
import time

# Load API keys (make sure to replace with your own keys)
api_key = 'rOLC2ZNl0CI2VRetB2Eknmklci8OiQO9knxd14KpcAEBdRj6kQdluDfyairKDk7q'
api_secret = '5B8JbiPH5JTUw1uctKFMToGygjuVO5Jf1lpIrmbDu9VRJ3euoMiGz1lG1Ki1ItmT'

# Initialize the Binance exchange with API keys
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'urls': {
        'api': {
            'public': 'https://testnet.binance.vision/api/v3',
            'private': 'https://testnet.binance.vision/api/v3',
        },
    }
})

exchange.set_sandbox_mode(True)

# Load the trained model (make sure this path matches the file location)
model = joblib.load('linear_regression_model.pkl')

# Check account balance to verify API key and set starting balances
def fetch_balances():
    try:
        balance = exchange.fetch_balance()
        usdt_balance = balance['total'].get('USDT', 0)
        btc_balance = balance['total'].get('BTC', 0)
        print(f"USDT Balance: {usdt_balance}, BTC Balance: {btc_balance}")
        return usdt_balance, btc_balance
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0, 0

# Function to fetch live price data for BTC/USDT
def fetch_live_data(symbol):
    ticker = exchange.fetch_ticker(symbol)
    return {
        'timestamp': pd.to_datetime(ticker['timestamp'], unit='ms'),
        'open': ticker['open'],
        'high': ticker['high'],
        'low': ticker['low'],
        'close': ticker['last'],
        'volume': ticker['quoteVolume']
    }

# Function to place a limit buy order 
    try:
        order = exchange.create_limit_buy_order(symbol, amount, price)
        print(f"Limit Buy Order placed for {amount} {symbol} at price {price}")
        return order
    except Exception as e:
        print(f"Error placing buy order: {e}")

# Function to place a limit sell order
def place_limit_sell_order(symbol, amount, price):
    try:
        order = exchange.create_limit_sell_order(symbol, amount, price)
        print(f"Limit Sell Order placed for {amount} {symbol} at price {price}")
        return order
    except Exception as e:
        print(f"Error placing sell order: {e}")

# Trading logic with live data
def trading_logic():
    symbol = 'BTC/USDT'
    
    # Get initial balances
    usdt_balance, btc_balance = fetch_balances()

    while True:
        # Fetch live data
        live_data = fetch_live_data(symbol)
        df_live = pd.DataFrame([live_data])

        # Add moving averages (based on live data)
        df_live['ma_10'] = df_live['close'].rolling(window=10).mean()
        df_live['ma_50'] = df_live['close'].rolling(window=50).mean()

        # Drop rows with NaN values (until enough data is collected for moving averages)
        df_live.dropna(inplace=True)

        # Make predictions using the model
        if not df_live.empty:
            X_live = df_live[['ma_10', 'ma_50']]
            predicted_change = model.predict(X_live)[0]

            current_price = live_data['close']
            amount_to_buy = min(1000, usdt_balance) / current_price

            # Decision-making logic based on predictions
            if predicted_change > 0 and usdt_balance >= 1000:
                # Place a limit buy order if prediction indicates price will rise
                place_limit_buy_order(symbol, amount_to_buy, current_price * 0.99)
                usdt_balance -= amount_to_buy * current_price  # Deduct from balance

            elif predicted_change < 0 and btc_balance > 0:
                # Place a limit sell order if prediction indicates price will drop
                place_limit_sell_order(symbol, btc_balance, current_price * 1.01)
                btc_balance = 0  # Assume we're selling all BTC

        # Wait before fetching the next live price
        time.sleep(60)  # Adjust time interval as needed

# Run the trading logic with live data
trading_logic()