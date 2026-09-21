#!/usr/bin/env python3
"""Validate optimizer inputs against real IMTA data."""

import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

# Load IMTA data
csv_path = 'data/imta_DEVICE_ID_20260630_095333.csv'
df = pd.read_csv(csv_path)

# Filter to May 20 - June 24 (clean window)
df['ds'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
df = df[(df['ds'].dt.date >= pd.Timestamp('2026-05-20').date()) &
        (df['ds'].dt.date <= pd.Timestamp('2026-06-24').date())].copy()
df = df.sort_values('ds').reset_index(drop=True)

print("="*70)
print("OPTIMIZER INPUT VALIDATION")
print("="*70)

# Confirmed by Corey Crisp (Aug 17, 2026 hardware review): total system draw
# ~34-35W (all active hardware combined); underwater camera alone is only 5-6W.
CONFIRMED_TOTAL_DRAW_W = 34.5

# ── 1. Battery SoC calculation ──────────────────────────────────────────────

print("\n1. BATTERY SOC CALCULATION")
print("-" * 70)

# LiFePO4 12V: 10.5V = 0%, 13.6V = 100%
def voltage_to_soc(v):
    return np.clip((v - 10.5) / (13.6 - 10.5) * 100, 0, 100)

def soc_to_wh(soc, capacity=1200):
    return soc / 100 * capacity

df['soc_pct'] = df['batt_v'].apply(voltage_to_soc)
df['soc_wh'] = df['soc_pct'].apply(lambda s: soc_to_wh(s, 1200))

print(f"Battery voltage range: {df['batt_v'].min():.2f}V to {df['batt_v'].max():.2f}V")
print(f"Inferred SoC range:    {df['soc_pct'].min():.1f}% to {df['soc_pct'].max():.1f}%")
print(f"Inferred Wh range:     {df['soc_wh'].min():.0f} Wh to {df['soc_wh'].max():.0f} Wh")
print(f"\nAssumed safe range: 20-90% (240-1080 Wh)")
print(f"✓ Data fits safe range" if (df['soc_pct'].min() >= 10 and df['soc_pct'].max() <= 95) else "✗ WARNING: Outside safe range")

# ── 2. Base load estimation ────────────────────────────────────────────────

print("\n2. BASE LOAD (Jetson + router, always on)")
print("-" * 70)

# Base load ≈ battery current when cameras are OFF
# Assume cameras off = low solar (night or minimal sun)
night_hours = df[df['panel_w'] < 5.0].copy()

if len(night_hours) > 0:
    # Current during night: sum of base load + discharge
    # Negative current = discharge (battery supplying power)
    base_load_ma = night_hours['batt_ma'].quantile(0.75)  # 75th percentile to avoid outliers
    base_load_w = base_load_ma / 1000 * 12  # mA → A → W (12V system)

    print(f"Night-time battery current (75th pctl): {base_load_ma:.0f} mA")
    print(f"Inferred base load: {abs(base_load_w):.1f}W")
    print(f"\nOptimizer assumes: 0W base load")
    print(f"✗ WARNING: Missing {abs(base_load_w):.1f}W base load in model")
    print(f"  → Actual available power = panel_w - {abs(base_load_w):.1f}W")
else:
    print("No night data found for base load estimation")

# ── 3. Camera power draw ──────────────────────────────────────────────────

print("\n3. CAMERA POWER DRAW")
print("-" * 70)

# Camera draw = difference between day and night current
day_hours = df[df['panel_w'] > 30.0].copy()
if len(day_hours) > 0 and len(night_hours) > 0:
    day_current = day_hours['batt_ma'].median()
    night_current = night_hours['batt_ma'].median()
    cam_draw_ma = abs(day_current - night_current)
    cam_draw_w = cam_draw_ma / 1000 * 12

    print(f"Day current (median, high sun): {day_current:.0f} mA")
    print(f"Night current (median):         {night_current:.0f} mA")
    print(f"Difference (camera draw):       {cam_draw_ma:.0f} mA = {cam_draw_w:.1f}W")
    print(f"\nOptimizer assumes: {CONFIRMED_TOTAL_DRAW_W}W total system draw (confirmed w/ hardware, Aug 17 2026)")
    if abs(cam_draw_w - CONFIRMED_TOTAL_DRAW_W) < 10:
        print(f"✓ Reasonable match (±{abs(cam_draw_w - CONFIRMED_TOTAL_DRAW_W):.1f}W)")
    else:
        print(f"✗ WARNING: Mismatch of {abs(cam_draw_w - CONFIRMED_TOTAL_DRAW_W):.1f}W")
else:
    print("Insufficient day/night data")

# ── 4. K_SCALE validation ──────────────────────────────────────────────────

print("\n4. K_SCALE FACTOR (panel_w = K_SCALE × irradiance)")
print("-" * 70)
print("Need Open-Meteo forecast data for comparison.")
print("Current K_SCALE = 0.11 assumes:")
print("  - Panel 100W rated")
print("  - Clear-sky GHI = 900 W/m²")
print("  - Panel efficiency ≈ 11%")
print("\nValidation: Compare day of forecast vs actual")
print("(Run after optimizer scheduled a forecast day)")

# ── 5. Daily energy budget ─────────────────────────────────────────────────

print("\n5. DAILY ENERGY BUDGET")
print("-" * 70)

daily = df.groupby(df['ds'].dt.date).agg({
    'panel_w': ['sum', 'mean', 'max'],
    'soc_wh': ['min', 'max'],
}).reset_index()
daily.columns = ['day', 'panel_w_sum', 'panel_w_mean', 'panel_w_max', 'soc_min', 'soc_max']

# Convert panel_w sum to Wh (1 reading per minute, sum/60 = Wh)
daily['energy_wh'] = daily['panel_w_sum'] / 60

print(f"\nAverage daily input:     {daily['energy_wh'].mean():.0f} Wh")
print(f"Peak daily input:        {daily['energy_wh'].max():.0f} Wh")
print(f"Min daily input:         {daily['energy_wh'].min():.0f} Wh")

avg_daily = daily['energy_wh'].mean()
cam_draw_daily = CONFIRMED_TOTAL_DRAW_W * 24  # confirmed 34.5W total system draw × 24h
base_load_daily = abs(base_load_w) * 24 if len(night_hours) > 0 else 0
total_draw_daily = cam_draw_daily + base_load_daily

print(f"\nDaily draws (if always ON):")
print(f"  System ({CONFIRMED_TOTAL_DRAW_W}W × 24h):    {cam_draw_daily:.0f} Wh")
if len(night_hours) > 0:
    print(f"  Base load ({abs(base_load_w):.1f}W × 24h):  {base_load_daily:.0f} Wh")
print(f"  Total draw:              {total_draw_daily:.0f} Wh")

print(f"\nAvailable energy:        {avg_daily:.0f} Wh/day")
if avg_daily >= total_draw_daily:
    print(f"✓ Can run cameras 24/7 (surplus: {avg_daily - total_draw_daily:.0f} Wh/day)")
elif avg_daily >= cam_draw_daily:
    uptime_pct = avg_daily / cam_draw_daily * 100
    print(f"⚠ Can run cameras {uptime_pct:.0f}% of day (ignoring base load)")
else:
    print(f"✗ Cannot sustain continuous camera operation")

# ── 6. Summary table ───────────────────────────────────────────────────────

print("\n" + "="*70)
print("OPTIMIZER INPUT ASSUMPTIONS vs DATA")
print("="*70)

summary = pd.DataFrame({
    'Parameter': [
        'Battery capacity',
        'Battery SoC floor',
        'Battery SoC ceiling',
        'Total system draw',
        'Base load',
        'K_SCALE',
        'Forecast horizon'
    ],
    'Optimizer value': [
        '1200 Wh',
        '240 Wh (20%)',
        '1080 Wh (90%)',
        '34.5 W',
        '0 W',
        '0.11',
        '48 h'
    ],
    'Data reality': [
        '1200 Wh (fixed)',
        f"{df['soc_wh'].min():.0f} Wh observed",
        f"{df['soc_wh'].max():.0f} Wh observed",
        f"{cam_draw_w:.1f}W (estimated)" if len(night_hours) > 0 else 'unknown',
        f"{abs(base_load_w):.1f}W (estimated)" if len(night_hours) > 0 else 'unknown',
        'TBD (need forecast)',
        'Needs daily refresh'
    ],
    'Risk': [
        '✓ correct',
        '✓ safe',
        '✓ safe',
        '✓ confirmed via hardware, Aug 17 2026' if len(night_hours) > 0 else '?',
        '✗ MISSING' if len(night_hours) > 0 else '?',
        '⚠ TBD',
        '⚠ MEDIUM'
    ]
})

print(summary.to_string(index=False))

print("\n" + "="*70)
print("RECOMMENDATIONS")
print("="*70)
print("""
HIGH PRIORITY:
  1. DONE — total system draw confirmed at ~34-35W via Corey Crisp hardware
     review (Aug 17, 2026); underwater camera alone is only 5-6W. 2 of 3
     top-side cameras died shortly after deployment — don't plan a schedule
     around a full 3-camera load.
  2. Subtract base load from panel_w in optimizer (≈5-10W)
  3. Run optimizer daily with real battery SoC from buoy

MEDIUM PRIORITY:
  4. Validate K_SCALE with one day of forecast vs actual
  5. Add ±15% forecast error margin to constraints
  6. Monitor battery voltage drift (LiFePO4 curve may shift)

LOW PRIORITY:
  7. Profile Jetson/router to exact base load
  8. Update scheduler to reflect actual surviving camera count, not the
     original 3-camera design
""")
