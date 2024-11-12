import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# Load the saved model
model = joblib.load('linear_regression_model.pkl')

# Load new data for prediction (for simplicity, we can use the prepared data)
df = pd.read_csv('btc_usdt_prepared_data.csv')

# Define features (X) for prediction
X_new = df[['ma_10', 'ma_50']]

# Make predictions using the loaded model
predictions = model.predict(X_new)

# Add the predictions to the DataFrame
df['predicted_price_change'] = predictions

# Display the last few predictions
print(df[['timestamp', 'close', 'predicted_price_change']].tail())

# Save the DataFrame with predictions to a new CSV file
df.to_csv('btc_usdt_predictions.csv', index=False)

print("Predictions saved to 'btc_usdt_predictions.csv'")
