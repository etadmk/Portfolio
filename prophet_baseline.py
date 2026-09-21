#!/usr/bin/env python3
"""Quick Prophet baseline on IMTA panel_w data."""

import pandas as pd
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

# Load data
csv_path = 'data/imta_DEVICE_ID_20260630_095333.csv'
df = pd.read_csv(csv_path)

# Inspect
print("CSV shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# Prepare for Prophet (needs 'ds' and 'y')
# Assuming there's a timestamp column and 'panel_w' column
if 'timestamp' in df.columns:
    df['ds'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
elif 'time' in df.columns:
    df['ds'] = pd.to_datetime(df['time']).dt.tz_localize(None)
else:
    print("Warning: no obvious timestamp column. Columns:", df.columns.tolist())
    exit(1)

# Target: panel power
if 'panel_w' not in df.columns:
    print("Error: no 'panel_w' column")
    exit(1)

df_prophet = df[['ds', 'panel_w']].copy()
df_prophet.columns = ['ds', 'y']

# Remove nulls
df_prophet = df_prophet.dropna()

# Exclude the Jun 25+ charging-path outage: `state` was stuck at Off (0) for
# 100% of minutes, never Bulk/Absorption/Float — that's equipment failure, not
# real solar variation, and it sits right at the end of this file (thru Jun 30),
# which would otherwise drag down the fitted trend/seasonality.
OUTAGE_START = pd.Timestamp('2026-06-25')
df_prophet = df_prophet[df_prophet['ds'] < OUTAGE_START].reset_index(drop=True)

print(f"\nPrepared data: {len(df_prophet)} rows")
print(f"Date range: {df_prophet['ds'].min()} to {df_prophet['ds'].max()}")

# Train Prophet with tuning for solar (high day, low night)
print("\nTraining Prophet...")
m = Prophet(
    yearly_seasonality=False,
    daily_seasonality=True,
    seasonality_mode='multiplicative',  # Solar scales with daylight
    seasonality_prior_scale=20,  # Trust daily pattern strongly
    interval_width=0.95
)

m.fit(df_prophet)

# Forecast next 7 days (168 hours)
future = m.make_future_dataframe(periods=168, freq='h')
forecast = m.predict(future)

print("\nForecast for next 7 days (48 hours shown):")
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(48))

# Save forecast
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv('data/prophet_forecast.csv', index=False)
print("\nForecast saved to: prophet_forecast.csv")

# Metrics on training data
from sklearn.metrics import mean_absolute_error
train_forecast = m.predict(df_prophet[['ds']])
mae = mean_absolute_error(df_prophet['y'], train_forecast['yhat'])
print(f"\nTraining MAE: {mae:.2f} W")
