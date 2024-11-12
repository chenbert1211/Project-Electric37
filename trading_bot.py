import pandas as pd

# Load the data with predictions
df = pd.read_csv('btc_usdt_predictions.csv')

# Initial conditions
cash = 10000  # Starting cash in USD
bitcoin = 0   # Starting Bitcoin holdings

# Simulate trading
for index, row in df.iterrows():
    # Check the predicted price change
    predicted_change = row['predicted_price_change']

    # Buy if prediction indicates a price increase
    if predicted_change > 0 and cash > 0:
        # Buy as much BTC as the available cash allows
        btc_to_buy = cash / row['close']
        bitcoin += btc_to_buy
        print(f"Bought {btc_to_buy:.6f} BTC at {row['close']} on {row['timestamp']}")
        cash = 0  # All cash is spent

    # Sell if prediction indicates a price decrease
    elif predicted_change < 0 and bitcoin > 0:
        # Sell all the BTC held
        usd_from_sale = bitcoin * row['close']
        cash += usd_from_sale
        print(f"Sold {bitcoin:.6f} BTC at {row['close']} on {row['timestamp']}")
        bitcoin = 0  # All BTC is sold

# Final portfolio value
portfolio_value = cash + (bitcoin * df.iloc[-1]['close'])
print(f"Final Portfolio Value: ${portfolio_value:.2f}")
