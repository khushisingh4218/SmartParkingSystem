import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

file_path = 'slot_data.csv'
df = pd.read_csv(file_path)

X = df[['DayOfWeek', 'TimeOfDay', 'IsSpecialDay', 'SlotNumber','Reservations', 'TotalAvailableSpots', 'PercentageAvailableSpots', 'CustomerType', 'MembershipStatus']]
y = df['DynamicPrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

new_reservation_features = pd.DataFrame({
    'DayOfWeek': [7],
    'TimeOfDay': [10],
    'IsSpecialDay': [1],
    'SlotNumber' : [2],
    'Reservations': [1],
    'TotalAvailableSpots': [5],
    'PercentageAvailableSpots': [1],
    'CustomerType': [0],
    'MembershipStatus': [1]
})

predicted_price = model.predict(new_reservation_features)
new_reservation_features['DynamicPrice'] = predicted_price.flatten()

new_reservation_features.to_csv(file_path, mode='a', header=False, index=False)

print(f"Predicted Price: Rs.{predicted_price[0]:.2f}")
