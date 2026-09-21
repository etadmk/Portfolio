#!/usr/bin/env python3
"""Analyze power allocation to sensors each day."""

import pandas as pd
import numpy as np

# Load data
csv_path = 'data/imta_DEVICE_ID_20260630_095333.csv'
df = pd.read_csv(csv_path)

print("Columns available:")
print(df.columns.tolist())
print("\nFirst 10 rows:")
print(df.head(10))

# Parse timestamp
if 'timestamp' in df.columns:
    df['ds'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
    df = df.sort_values('ds').reset_index(drop=True)
else:
    print("No timestamp")
    exit(1)

df_clean = df.dropna(subset=['panel_w']).copy()

# Check what relay/sensor columns exist
relay_cols = [col for col in df.columns if 'relay' in col.lower() or 'cam' in col.lower() or 'sensor' in col.lower()]
print(f"\nRelay/sensor columns found: {relay_cols}")

# Add day column
df_clean['day'] = df_clean['ds'].dt.date

# Summarize by day
print("\n" + "="*70)
print("DAILY POWER SUMMARY")
print("="*70)

daily = df_clean.groupby('day').agg({
    'panel_w': 'sum',  # Total energy harvested (Wh)
    'batt_v': 'mean',  # Average battery voltage
}).reset_index()

daily.columns = ['Date', 'Total_Energy_Wh', 'Avg_Batt_V']

print(daily.to_string(index=False))

print("\n" + "="*70)
print("ANALYSIS")
print("="*70)

# Estimate power draw
# panel_w = solar generation
# If we know total energy harvested and battery state, we can infer draw

# Confirmed via Corey Crisp hardware review (Aug 17, 2026):
#   - Base load (Jetson + router): 1.7W, measured at night
#   - Underwater camera: 5-6W
#   - Total system draw when everything is running: ~34-35W
#   - 2 of 3 top-side cameras died shortly after deployment — actual load is
#     lower than a full 3-camera design, so don't plan around "both/all cameras"
base_load_w = 1.7          # Jetson, router
underwater_camera_w = 5.5  # underwater camera only
total_system_w = 34.5      # everything running (base + underwater + surviving top-side camera)

avg_energy = daily['Total_Energy_Wh'].mean()
print(f"\nAverage daily energy input:  {avg_energy:.0f} Wh/day")

continuous_base_cost = 24 * base_load_w
continuous_underwater_cost = 24 * underwater_camera_w
continuous_total_cost = 24 * total_system_w

print(f"\nEstimated power budget:")
print(f"  Base load (24h):                {continuous_base_cost:.0f} Wh")
print(f"  Underwater camera only (24h):   {continuous_underwater_cost:.0f} Wh")
print(f"  Full system, 24h (base + underwater + surviving top-side camera): {continuous_total_cost:.0f} Wh")

print(f"\nWith {avg_energy:.0f} Wh available:")
print(f"  Can run full system 24/7:  {avg_energy >= continuous_total_cost}")
print(f"  System duty cycle:         {(avg_energy / continuous_total_cost) * 100:.0f}%")

print("\n" + "="*70)
print("NOTE: Without relay state data in the CSV, power allocation")
print("is inferred from total panel_w. For actual device-level breakdown,")
print("need per-device current monitoring or explicit relay logs.")
print("="*70)
