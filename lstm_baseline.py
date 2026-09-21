#!/usr/bin/env python3
"""LSTM baseline on IMTA panel_w data."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import warnings
warnings.filterwarnings('ignore')

# Load data
csv_path = 'data/imta_DEVICE_ID_20260630_095333.csv'
df = pd.read_csv(csv_path)

print("CSV shape:", df.shape)
print("Columns:", df.columns.tolist())

# Prepare timestamp
if 'timestamp' in df.columns:
    df['ds'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
else:
    print("No timestamp column found")
    exit(1)

# Get panel power
if 'panel_w' not in df.columns:
    print("Error: no 'panel_w' column")
    exit(1)

data = df[['ds', 'panel_w']].copy()
data = data.dropna()
data = data.sort_values('ds').reset_index(drop=True)

# Exclude the Jun 25+ charging-path outage: `state` was stuck at Off (0) for
# 100% of minutes, never Bulk/Absorption/Float — that's equipment failure, not
# real solar variation, and it sits right at the end of this file (thru Jun 30),
# exactly where the LSTM seeds its forecast from.
OUTAGE_START = pd.Timestamp('2026-06-25')
data = data[data['ds'] < OUTAGE_START].reset_index(drop=True)

# The raw CSV is per-minute. `lookback=24` below is meant to mean 24 HOURS,
# and the forecast is stamped with freq='h' — both only true if each row here
# is one hour apart, so resample before building sequences.
data = data.set_index('ds')[['panel_w']].resample('h').mean().dropna().reset_index()

print(f"\nData: {len(data)} rows (hourly)")
print(f"Date range: {data['ds'].min()} to {data['ds'].max()}")

# Normalize
scaler = MinMaxScaler(feature_range=(0, 1))
data_normalized = scaler.fit_transform(data[['panel_w']])

# Create sequences (past 24 hours → predict next 1 hour)
lookback = 24
X, y = [], []
for i in range(len(data_normalized) - lookback):
    X.append(data_normalized[i:i+lookback, 0])
    y.append(data_normalized[i+lookback, 0])

X = np.array(X)
y = np.array(y)

print(f"\nSequences created: {len(X)} samples")
print(f"Input shape: {X.shape}")
print(f"Output shape: {y.shape}")

# Train/test split (80/20, no shuffle)
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# Reshape for LSTM: (samples, timesteps, features)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Build LSTM model
print("\nBuilding LSTM model...")
model = keras.Sequential([
    layers.LSTM(50, activation='relu', input_shape=(lookback, 1)),
    layers.Dense(25, activation='relu'),
    layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])
print(model.summary())

# Train
print("\nTraining...")
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    verbose=1,
    validation_split=0.1
)

# Evaluate
print("\nEvaluating...")
train_pred = model.predict(X_train, verbose=0)
test_pred = model.predict(X_test, verbose=0)

# Inverse transform to get watts back
train_pred_watts = scaler.inverse_transform(train_pred)
test_pred_watts = scaler.inverse_transform(test_pred)
y_train_watts = scaler.inverse_transform(y_train.reshape(-1, 1))
y_test_watts = scaler.inverse_transform(y_test.reshape(-1, 1))

train_mae = mean_absolute_error(y_train_watts, train_pred_watts)
test_mae = mean_absolute_error(y_test_watts, test_pred_watts)

print(f"\nTraining MAE: {train_mae:.2f} W")
print(f"Test MAE: {test_mae:.2f} W")

# Forecast next 7 days (168 hours)
print("\nForecasting next 7 days...")
forecast_seq = data_normalized[-lookback:, 0].copy()
forecast_list = []

for _ in range(168):
    X_pred = forecast_seq[-lookback:].reshape(1, lookback, 1)
    next_pred = model.predict(X_pred, verbose=0)[0, 0]
    forecast_list.append(next_pred)
    forecast_seq = np.append(forecast_seq, next_pred)

forecast_watts = scaler.inverse_transform(np.array(forecast_list).reshape(-1, 1))

# Save forecast
last_time = data['ds'].iloc[-1]
forecast_times = pd.date_range(last_time, periods=169, freq='h')[1:]

forecast_df = pd.DataFrame({
    'ds': forecast_times,
    'yhat': forecast_watts.flatten()
})
forecast_df.to_csv('data/lstm_forecast.csv', index=False)

print("Forecast saved to lstm_forecast.csv")
print(f"\nForecast summary (watts):")
print(f"  Min: {forecast_watts.min():.2f} W")
print(f"  Max: {forecast_watts.max():.2f} W")
print(f"  Mean: {forecast_watts.mean():.2f} W")

# Comparison
print("\n" + "="*50)
print("COMPARISON")
print("="*50)
print(f"Prophet (MAE):     3.58 W")
print(f"LSTM Train (MAE):  {train_mae:.2f} W")
print(f"LSTM Test (MAE):   {test_mae:.2f} W ← (on unseen data)")
