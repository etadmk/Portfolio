"""
IMTA panel-health diagnosis — revised after testing Corey Crisp's curtailment
explanation (Aug 17, 2026 meeting) against the raw telemetry, then confirmed
against the actual charge-controller state codes Corey provided:
    0 = Off, 2 = Fault, 3 = Bulk charge, 4 = Absorption charge, 5 = Float charge

Result — a clean split, not one blanket story:

  - Jun 4-24: `state` cycles normally through Bulk -> Absorption -> Float most
    days (a textbook full charge cycle, Float logged every day). This directly
    confirms Corey's curtailment explanation for this window.
  - Jun 25 onward: `state` = Off for 100% of minutes, every day. Never once
    enters Bulk/Absorption/Float, AND never logs Fault (state=2) either. A
    battery that's simply satisfied would still show Float; this shows the
    charging path never engaging at all, self-reported "off" rather than
    "satisfied" or "faulted." Corey confirmed: the unit was likely pulled out
    (physically disconnected/retrieved) after June 25 — not a wiring fault or
    controller failure, which is why it never self-reports as Fault.

QA rules from Corey: drop rows where ve_error == 1.
Requires: pandas, numpy, matplotlib
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

IMTA_CSV = "/home/marinesitu/Downloads/imta_solar_20260817_174154.csv"

FLOAT_VOLTAGE = 14.3  # observed float plateau in this dataset (Jun 1-24)

STATE_NAMES = {0: "Off", 2: "Fault", 3: "Bulk", 4: "Absorption", 5: "Float"}

CURTAIL_WINDOW = ("2026-06-04", "2026-06-25")   # confirmed: Bulk/Absorption/Float cycle daily
OUTAGE_WINDOW = ("2026-06-25", "2026-07-02")    # confirmed: 100% Off, never Fault either

COLOR_PANEL = "#2a78d6"      # slot 1 blue
COLOR_VOLT = "#eb6834"       # slot 2 orange
COLOR_BULK = "#2a78d6"       # slot 1 blue
COLOR_ABSORPTION = "#eda100"  # slot 4 yellow
COLOR_FLOAT = "#1baf7a"      # slot 3 aqua
BG_CURTAIL = "#e1e0d9"       # neutral gray tint — confirmed curtailment
BG_OUTAGE = "#f6ded6"        # light warm tint — confirmed outage, not curtailment
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"


def load_imta():
    df = pd.read_csv(IMTA_CSV, parse_dates=["timestamp"])
    df = df[df["ve_error"] != 1]  # Corey QA rule
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    df = df.set_index("timestamp").sort_index()
    raw_state = df["state"]
    hourly = df[["panel_w", "batt_v", "batt_ma"]].resample("h").mean().dropna()
    return hourly, raw_state


def build_daily_state_minutes(raw_state):
    """Minutes per day in each confirmed charge-controller state."""
    named = raw_state.map(STATE_NAMES)
    daily = named.groupby(named.index.floor("D")).value_counts().unstack(fill_value=0)
    for col in ["Bulk", "Absorption", "Float", "Off", "Fault"]:
        if col not in daily.columns:
            daily[col] = 0
    return daily


def plot(hourly, daily_state):
    fig, axes = plt.subplots(
        3, 1, figsize=(13, 9), sharex=True,
        gridspec_kw={"height_ratios": [2, 1.6, 1.4], "hspace": 0.1},
        facecolor="#fcfcfb",
    )
    ax_panel, ax_volt, ax_state = axes

    span_curtail = (pd.Timestamp(CURTAIL_WINDOW[0], tz="UTC"), pd.Timestamp(CURTAIL_WINDOW[1], tz="UTC"))
    span_outage = (pd.Timestamp(OUTAGE_WINDOW[0], tz="UTC"), pd.Timestamp(OUTAGE_WINDOW[1], tz="UTC"))

    for ax in axes:
        ax.axvspan(*span_curtail, color=BG_CURTAIL, zorder=0)
        ax.axvspan(*span_outage, color=BG_OUTAGE, zorder=0)
        ax.grid(True, alpha=0.5, color=GRID)
        ax.spines[["top", "right"]].set_visible(False)

    # Panel output
    ax_panel.plot(hourly.index, hourly["panel_w"], color=COLOR_PANEL, linewidth=1.1)
    ax_panel.set_ylabel("Panel output\n(W, hourly avg)", fontsize=9, color=INK_SECONDARY)
    ax_panel.set_title(
        "IMTA panel/battery telemetry, May 20 - Jul 2 — confirmed against charge-controller state codes\n"
        "(0=Off, 2=Fault, 3=Bulk, 4=Absorption, 5=Float)",
        fontsize=12, fontweight="bold", color=INK_PRIMARY, loc="left",
    )

    # Battery voltage with float reference
    ax_volt.plot(hourly.index, hourly["batt_v"], color=COLOR_VOLT, linewidth=1.1)
    ax_volt.axhline(FLOAT_VOLTAGE, color=INK_MUTED, linewidth=1, linestyle=":")
    ax_volt.text(hourly.index.min(), FLOAT_VOLTAGE + 0.05, "float (~14.3V)",
                 fontsize=8, color=INK_MUTED, va="bottom")
    ax_volt.set_ylabel("Battery voltage (V)", fontsize=9, color=INK_SECONDARY)

    # Daily minutes in each confirmed charging state — the ground-truth signal
    bottom = np.zeros(len(daily_state))
    for name, color in [("Bulk", COLOR_BULK), ("Absorption", COLOR_ABSORPTION), ("Float", COLOR_FLOAT)]:
        ax_state.bar(daily_state.index, daily_state[name], bottom=bottom, width=0.9,
                     color=color, label=f"{name} charge")
        bottom += daily_state[name].values
    ax_state.set_ylabel("Minutes/day\nin charge state", fontsize=9, color=INK_SECONDARY)
    ax_state.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax_state.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.setp(ax_state.get_xticklabels(), rotation=45, ha="right", color=INK_MUTED)
    ax_state.legend(loc="upper left", fontsize=8.5, frameon=False, ncol=3)

    # Annotations calling out the two windows explicitly
    ax_panel.annotate(
        "Jun 4-24: state cycles Bulk→Absorption→Float\nevery day (textbook full charge cycle)\n→ CURTAILMENT CONFIRMED",
        xy=(pd.Timestamp("2026-06-14", tz="UTC"), hourly["panel_w"].max() * 0.9),
        fontsize=8.5, color=INK_SECONDARY, ha="center",
    )
    ax_panel.annotate(
        "Jun 25+: state = Off 100% of minutes,\nnever Bulk/Absorption/Float,\nnever Fault either\n→ unit was likely pulled out, not curtailment or a fault",
        xy=(pd.Timestamp("2026-06-28", tz="UTC"), hourly["panel_w"].max() * 0.55),
        fontsize=8.5, color="#8a3a1f", ha="center",
    )

    from matplotlib.patches import Patch
    legend_handles = [
        Patch(facecolor=BG_CURTAIL, label="Curtailment confirmed (Jun 4-24)"),
        Patch(facecolor=BG_OUTAGE, label="Stuck Off — unit likely pulled out (Jun 25+)"),
    ]
    ax_panel.legend(handles=legend_handles, loc="upper left", fontsize=8.5, frameon=False)

    fig.text(
        0.01, 0.005,
        "Confirmed state codes: 0=Off, 2=Fault, 3=Bulk, 4=Absorption, 5=Float. "
        "Fault (2) never appears anywhere in this dataset.",
        fontsize=8, color=INK_MUTED, ha="left",
    )

    plt.tight_layout(rect=[0, 0.02, 1, 1])
    out = "/home/marinesitu/daily_harvest_diagnosis_corrected.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="#fcfcfb")
    print(f"Saved -> {out}")


def main():
    hourly, raw_state = load_imta()
    daily_state = build_daily_state_minutes(raw_state)
    plot(hourly, daily_state)


if __name__ == "__main__":
    main()
