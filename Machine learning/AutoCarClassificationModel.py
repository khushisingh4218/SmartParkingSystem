import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv('automated_car.csv')
# sensor1 is left ultrasound sensor and sensor2 is right ultrasound sensor
X = df[['sensor1', 'sensor2']]
y = df['action']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

new_sensor_readings = pd.DataFrame({'sensor1': [30], 'sensor2': [70]})
prediction = clf.predict(new_sensor_readings)
print("Predicted Action:", prediction[0])
