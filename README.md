# Marine Energy: power and data budgets for off-grid monitoring

A year of work on one question: how do you keep a scientific instrument running in the ocean
when its whole power budget depends on the weather, and nobody can reach the hardware.

**Aditi Kalle** · DOE / ORISE Marine Energy Fellow, MarineSitu · Sept 2025 to Sept 2026

The answer turned out to be less about better forecasting and more about **telling a healthy
system apart from a broken one using telemetry alone**.

---

## Start here

Open [`index.html`](index.html) in a browser. Everything is self-contained, no build step,
no server. The only external request is to Google Fonts.

| | |
|---|---|
| [**Duty Cycle Planner**](duty-cycle-planner.html) | Interactive tool. Enter a site, a battery and instruments in priority order; it allocates power, simulates the battery hour by hour, and cuts duty cycles back rather than cross the safety floor. |
| [**Panel Loss, Revisited**](panel-loss-revisited.html) | The investigation. A buoy appeared to be losing 60% of its solar output. It wasn't. What was actually happening, and the real fault hiding inside it. |
| [**Technical report**](capstone-report.html) | The full evaluation: telemetry pipeline, optimisation framework, an 11-model forecasting benchmark, fail-safe scheduling, hardware validation across two sites. |

## Code

| File | What it does |
|---|---|
| [`code/verified_benchmark.py`](code/verified_benchmark.py) | 11-model forecasting benchmark on a strict 28-day train / 7-day test split. Replaces an earlier version whose evaluation leaked test data into training. |
| [`code/power_allocation.py`](code/power_allocation.py) | The priority cascade. Pay the always-on load first, spend what remains down the priority order. |
| [`code/imta_optimizer.py`](code/imta_optimizer.py) | Scheduling over a 48-hour horizon, including the integer LP variant that enforces the battery floor hour by hour. |
| [`code/lstm_baseline.py`](code/lstm_baseline.py) | LSTM solar forecaster. Best verified performer at 0.93 W mean absolute error. |
| [`code/prophet_baseline.py`](code/prophet_baseline.py) | Prophet forecaster, for comparison. 3.58 W. |
| [`code/validate_optimizer_inputs.py`](code/validate_optimizer_inputs.py) | Input validation against real telemetry before anything reaches the optimiser. |

## Three findings

**Data composition beat model choice.** Eight different model families landed within
0.95 to 1.23 W of each other. One change to the train/test split moved the result further
than switching model did.

**The floor held for 41 days.** Every schedule the optimiser produced was simulated forward
hour by hour against a 20% safety floor. None crossed it.

**The diagnostic method transferred.** Built on one deployment, then reproduced on a second
site running different hardware, owned and operated by someone else.

## Scope, stated plainly

This work was telemetry-only by necessity. The buoy came out of the water partway through the
fellowship and I never had hands on either system. Every diagnosis here was made at a distance
and then confirmed by someone who could see the hardware.

That turned out to be the interesting constraint rather than a limiting one. It is the same
position anyone is in when an instrument is two hundred miles offshore, and it is where the
actual finding came from: **remote diagnosis gets you a short list of candidates, not an
answer.** Knowing precisely where that list ends is the useful part.

## Notes

- Figures are real telemetry unless a caption says otherwise.
- Scripts expect their input CSV under `data/`. The buoy's device identifier has been replaced
  with `DEVICE_ID`, and the telemetry itself is not included here.
- Two data-collection scripts (Firestore and Copernicus ERA5 pulls) are omitted, as they carry
  internal project identifiers and are plumbing rather than analysis.
