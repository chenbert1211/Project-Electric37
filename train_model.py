import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the prepared data
df = pd.read_csv('btc_usdt_prepared_data.csv')

# Define features (X) and target (y)
# We'll use the 'ma_10' and 'ma_50' as features to predict 'price_change'
X = df[['ma_10', 'ma_50']]
y = df['price_change']

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate and print the Mean Squared Error (MSE) to evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the trained model to a file using joblib
import joblib
joblib.dump(model, 'linear_regression_model.pkl')

print("Model training complete and saved as 'linear_regression_model.pkl'")
