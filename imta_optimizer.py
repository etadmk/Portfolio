"""
IMTA Camera Scheduling Optimizer — Stage 2 pipeline
Open-Meteo forecast → scale to panel_w → CVXPY integer LP → camera on/off schedule

Run:
    source ./.venv/bin/activate
    python imta_optimizer.py
"""

import requests
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timezone

try:
    import cvxpy as cp
    CVXPY_AVAILABLE = True
except ImportError:
    CVXPY_AVAILABLE = False
    print("WARNING: cvxpy not installed — run: pip install cvxpy")
    print("Falling back to greedy heuristic.\n")

# ── Configuration ──────────────────────────────────────────────────────────────

LAT, LON = 30.201833, -87.965000          # IMTA buoy, Gulf Coast AL
TIMEZONE  = "America/Chicago"

# Panel scale factor: panel_w ≈ K_SCALE × shortwave_radiation (W/m²)
# Panel: 100W rated, Vmp=18.72V, Imp=5.34A via Victron MPPT 75/15
# Estimate: 100W / 900 W/m² clear-sky GHI = 0.11
K_SCALE = 0.11

# Battery: 12V – 100Ah LiFePO4 (from block diagram)
# Total: 1200Wh | Safe range: 20–90% SoC for LiFePO4 chemistry
BATT_CAPACITY_WH = 1200.0   # 12V × 100Ah
BATT_INIT_SOC    = 0.70     # assumed starting state of charge (0–1)
BATT_MIN_WH      = 240.0    # 20% floor (LiFePO4 minimum)
BATT_MAX_WH      = 1080.0   # 90% ceiling (LiFePO4 maximum)

# Camera power draw — confirmed via Corey Crisp hardware review (Aug 17, 2026):
# total system draw ~34-35W (camera(s) + Jetson + router combined); underwater
# camera alone is only 5-6W. Also: 2 of 3 top-side cameras died shortly after
# deployment, so actual load is lower than the original 3-camera design assumed.
CAM_DRAW_W = 34.5           # watts — measured total system draw, not per-camera

# Forecast horizon
HORIZON_H = 48              # hours to optimize over

# ── Step 1: Fetch Open-Meteo forecast ─────────────────────────────────────────

def fetch_openmeteo(lat, lon, tz, hours=HORIZON_H):
    print(f"Fetching Open-Meteo forecast for ({lat:.3f}, {lon:.3f})...")
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "shortwave_radiation,cloud_cover",
            "timezone": tz,
            "forecast_days": max(2, hours // 24 + 1),
        },
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()

    df = pd.DataFrame({
        "timestamp": pd.to_datetime(data["hourly"]["time"]),
        "ghi_w_m2": data["hourly"]["shortwave_radiation"],
        "cloud_cover_pct": data["hourly"]["cloud_cover"],
    })
    df["timestamp"] = df["timestamp"].dt.tz_localize(tz).dt.tz_convert("UTC")
    return df.iloc[:hours].reset_index(drop=True)

# ── Step 2: Convert irradiance → predicted panel_w ────────────────────────────

def forecast_panel_w(df, k=K_SCALE):
    df = df.copy()
    df["panel_w_forecast"] = df["ghi_w_m2"] * k
    df["clear_sky_fraction"] = (100 - df["cloud_cover_pct"]) / 100
    return df

# ── Step 3: CVXPY integer LP optimizer ────────────────────────────────────────

def optimize_schedule_cvxpy(panel_w_forecast, batt_init_wh, cam_draw_w,
                             batt_min_wh, batt_max_wh):
    """
    Maximize camera-on hours subject to battery staying in [batt_min_wh, batt_max_wh].

    Decision variable: x[t] ∈ {0, 1} for each hour t
        1 = cameras on, 0 = cameras off

    Energy balance each hour:
        SOC[t] = SOC[t-1] + panel_w[t] - x[t] * cam_draw_w
    """
    n = len(panel_w_forecast)
    x     = cp.Variable(n, boolean=True)
    soc   = cp.Variable(n + 1)
    spill = cp.Variable(n, nonneg=True)   # excess solar clipped by charge controller

    objective = cp.Maximize(cp.sum(x))
    constraints = [
        soc[0] == batt_init_wh,
        # energy balance: spill absorbs excess when battery is full
        soc[1:] == soc[:-1] + panel_w_forecast - x * cam_draw_w - spill,
        soc >= batt_min_wh,
        soc <= batt_max_wh,
    ]

    problem = cp.Problem(objective, constraints)
    problem.solve(verbose=False)   # let CVXPY auto-select MIP solver

    if problem.status not in ("optimal", "optimal_inaccurate"):
        print(f"  Solver status: {problem.status} — falling back to greedy")
        return greedy_schedule(panel_w_forecast, batt_init_wh, cam_draw_w,
                               batt_min_wh, batt_max_wh)

    schedule = np.round(x.value).astype(int)
    return schedule

# ── Greedy fallback (no cvxpy) ────────────────────────────────────────────────

def greedy_schedule(panel_w_forecast, batt_init_wh, cam_draw_w,
                    batt_min_wh, batt_max_wh):
    """Turn cameras on whenever battery is above floor + safety margin."""
    n = len(panel_w_forecast)
    schedule = np.zeros(n, dtype=int)
    soc = batt_init_wh

    for t in range(n):
        net_on  = panel_w_forecast[t] - cam_draw_w
        net_off = panel_w_forecast[t]
        # only run cameras if solar is non-trivial OR battery has a strong buffer
        solar_available = panel_w_forecast[t] > 2.0
        buffer_ok = soc > batt_min_wh + cam_draw_w * 2

        if (solar_available or buffer_ok) and (soc + net_on >= batt_min_wh) and (soc + net_on <= batt_max_wh):
            schedule[t] = 1
            soc += net_on
        else:
            schedule[t] = 0
            soc = min(soc + net_off, batt_max_wh)

    return schedule

# ── Step 4: Simulate battery trajectory ───────────────────────────────────────

def simulate_battery(panel_w_forecast, schedule, batt_init_wh, cam_draw_w,
                     batt_max_wh):
    soc = [batt_init_wh]
    for t in range(len(schedule)):
        net = panel_w_forecast[t] - schedule[t] * cam_draw_w
        soc.append(min(soc[-1] + net, batt_max_wh))
    return np.array(soc[1:])

# ── Step 5: Plot and save results ─────────────────────────────────────────────

def plot_schedule(df, schedule, soc_trajectory, batt_min_wh, output_path):
    fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)
    fig.suptitle("IMTA Camera Schedule — Open-Meteo + CVXPY Optimizer", fontsize=13)

    timestamps = df["timestamp"].dt.tz_convert("US/Central")

    # Panel forecast
    axes[0].fill_between(timestamps, df["panel_w_forecast"], alpha=0.7, color="#f5a623")
    axes[0].set_ylabel("Forecast panel_w (W)")
    axes[0].set_title("Solar Power Forecast")
    axes[0].set_ylim(bottom=0)

    # Camera schedule
    axes[1].step(timestamps, schedule, where="post", color="#4a90d9", linewidth=2)
    axes[1].set_yticks([0, 1])
    axes[1].set_yticklabels(["OFF", "ON"])
    axes[1].set_ylabel("Camera state")
    axes[1].set_title(f"Camera Schedule — {schedule.sum()} on / {len(schedule)} hours ({100*schedule.mean():.0f}% uptime)")
    axes[1].fill_between(timestamps, schedule, step="post", alpha=0.3, color="#4a90d9")

    # Battery SOC
    axes[2].fill_between(timestamps, soc_trajectory, alpha=0.5, color="#7ed321")
    axes[2].axhline(batt_min_wh, color="red", linestyle="--", linewidth=1, label=f"Min {batt_min_wh:.0f} Wh")
    axes[2].set_ylabel("Battery (Wh)")
    axes[2].set_title("Battery State of Charge")
    axes[2].legend()
    axes[2].set_ylim(0, 55)

    axes[2].xaxis.set_major_formatter(mdates.DateFormatter("%a %m/%d %Hh", tz="US/Central"))
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=120)
    print(f"Plot saved: {output_path}")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    # 1. Fetch
    df = fetch_openmeteo(LAT, LON, TIMEZONE, hours=HORIZON_H)

    # 2. Convert to panel_w
    df = forecast_panel_w(df, k=K_SCALE)
    panel_w = df["panel_w_forecast"].values
    batt_init_wh = BATT_CAPACITY_WH * BATT_INIT_SOC

    print(f"\nForecast summary ({HORIZON_H}h):")
    print(f"  Peak panel_w forecast : {panel_w.max():.1f} W")
    print(f"  Mean panel_w forecast : {panel_w.mean():.1f} W")
    print(f"  Battery starts at     : {batt_init_wh:.1f} Wh ({BATT_INIT_SOC*100:.0f}%)")

    # 3. Optimize
    if CVXPY_AVAILABLE:
        print("\nRunning CVXPY integer LP optimizer...")
        schedule = optimize_schedule_cvxpy(
            panel_w, batt_init_wh, CAM_DRAW_W, BATT_MIN_WH, BATT_MAX_WH
        )
        method = "CVXPY (GLPK_MI)"
    else:
        print("\nRunning greedy fallback scheduler...")
        schedule = greedy_schedule(
            panel_w, batt_init_wh, CAM_DRAW_W, BATT_MIN_WH, BATT_MAX_WH
        )
        method = "Greedy heuristic"

    # 4. Simulate battery
    soc = simulate_battery(panel_w, schedule, batt_init_wh, CAM_DRAW_W, BATT_MAX_WH)

    # 5. Report
    print(f"\nOptimizer: {method}")
    print(f"Camera on-hours : {schedule.sum()} / {HORIZON_H} ({100*schedule.mean():.0f}% uptime)")
    print(f"Battery min SOC : {soc.min():.1f} Wh  (floor = {BATT_MIN_WH:.1f} Wh)")
    print(f"Battery max SOC : {soc.max():.1f} Wh")
    print(f"\nHourly schedule (1=ON, 0=OFF):")
    for i, (row, cam, b) in enumerate(zip(df.itertuples(), schedule, soc)):
        time_str = row.timestamp.tz_convert("US/Central").strftime("%a %m/%d %Hh")
        bar = "█" * int(row.panel_w_forecast / 5)
        print(f"  {time_str}  {'ON ' if cam else 'off'}  batt={b:5.1f}Wh  solar={row.panel_w_forecast:5.1f}W {bar}")
        if i >= 23:
            print(f"  ... ({HORIZON_H - 24} more hours)")
            break

    # 6. Plot
    plot_path = f"data/imta_schedule_{ts}.png"
    plot_schedule(df, schedule, soc, BATT_MIN_WH, plot_path)

    # 7. Save schedule CSV
    df["camera_on"] = schedule
    df["batt_wh_simulated"] = soc
    csv_path = f"data/imta_schedule_{ts}.csv"
    df[["timestamp", "panel_w_forecast", "cloud_cover_pct", "camera_on", "batt_wh_simulated"]].to_csv(csv_path, index=False)
    print(f"Schedule CSV  : {csv_path}")

if __name__ == "__main__":
    main()
