import pandas as pd

# Load the historical data from the CSV file
df = pd.read_csv('btc_usdt_historical_data.csv')

# Display the first few rows of the data
print(df.head())

# Calculate the percentage change between each closing price
df['price_change'] = df['close'].pct_change()

# Calculate a 10-period moving average (short-term trend)
df['ma_10'] = df['close'].rolling(window=10).mean()

# Calculate a 50-period moving average (long-term trend)
df['ma_50'] = df['close'].rolling(window=50).mean()

# Drop any rows with missing values (e.g., NaNs from rolling calculations)
df.dropna(inplace=True)

# Display the first few rows of the DataFrame with new features
print(df.head())

# Save the processed data to a new CSV file
df.to_csv('btc_usdt_prepared_data.csv', index=False)

print("Data prepared and saved to btc_usdt_prepared_data.csv")
