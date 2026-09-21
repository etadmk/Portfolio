# Machine Learning for Rookies — Taught Through a Solar Buoy
**A from-zero ML course built on the IMTA deployment data**
*No experience assumed. If you can copy-paste and read English, you can do this.*

---

## Before You Start — Read This Once

This course teaches machine learning using **one real thing**: a solar-powered buoy floating off the Gulf Coast, measuring sunlight and battery power every few seconds. We use its actual data the whole way through.

**The golden rule of this course:** you never meet a piece of jargon before you meet the idea behind it in plain English. Every lesson goes *idea → analogy → then code*. If a code block looks scary, that's fine — read it like a recipe, not like math. You are allowed to not understand everything yet.

**What you'll be able to do by the end:**
- Explain what machine learning actually is, without hand-waving
- Load real sensor data and look at it
- Predict tomorrow's solar power from past data
- Understand *why* a dumb model sometimes beats a fancy one
- Know which model to reach for and why

**How long it takes:** about 30–45 minutes per lesson. Don't skip ahead. Each lesson leans on the one before it.

---

## Lesson 0 — What Even Is Machine Learning?

Forget the buzzwords. Here is the entire idea in one sentence:

> **Machine learning is writing a program by showing it examples instead of writing the rules yourself.**

That's it. Compare two ways to predict tomorrow's weather:

- **Normal programming:** *You* write every rule. "If pressure drops AND humidity is high, predict rain." You have to know all the rules in advance.
- **Machine learning:** You show a program thousands of past days (weather + what happened next), and it figures out the rules *itself*. You never wrote "if pressure drops."

Three words you'll hear constantly, defined simply:

| Word | Plain meaning |
|---|---|
| **Model** | The "program" that ML produces. A box you put inputs into and get a prediction out of. |
| **Training** | The process of showing the model examples so it can learn. Also called "fitting." |
| **Prediction / forecast** | What the model spits out for a situation it hasn't seen. |

**Our task in this course:** build a model that looks at the buoy's past solar power and predicts the *next 48 hours* of solar power. That's a **forecast**.

> 🧠 **Checkpoint:** If a friend asks "what's machine learning?", can you answer in one sentence without saying "AI" or "neural network"? If yes, continue.

---

## Lesson 1 — Meet the Buoy (and Why We Care)

Out in the water off Alabama (30.2°N, 88.0°W — the Gulf Coast) sits an **IMTA buoy**. IMTA stands for Integrated Multi-Trophic Aquaculture, but you don't need the biology. Here's what matters:

- A **solar panel** charges a **battery** during the day.
- The battery powers **underwater cameras**.
- At night and on cloudy days, the panel makes nothing, so the battery drains.

**The real-world problem:** if we run the cameras too much, the battery dies and *everything* shuts off. If we run them too little, we waste uptime. The buoy needs to decide **when to run the cameras** — and that decision depends on **how much sun is coming tomorrow**.

So everything in this course serves one goal:

```
Predict tomorrow's solar power  →  decide when to run the cameras
```

The buoy logs its sensors every few seconds into a file. Ours is named:

```
imta_0a10aced202194944a071780_20260624_130203.csv
```

That ugly name is just `imta_` + the device ID + the date it was pulled. It holds **114,000+ rows** covering about **35 days** (mid-May to late June 2026).

The two measurements we'll forecast:
- **`panel_w`** — solar panel power, in **watts (W)**. Peaks around **100 W** at noon, drops to **0 W** at night.
- **`batt_v`** — battery voltage, in **volts (V)**. The real control signal — cameras live and die by this.

---

## Lesson 2 — What Does "Data" Actually Look Like?

People say "data" like it's mysterious. It isn't. It's a table — rows and columns, like a spreadsheet.

- Each **row** = one moment in time (one reading from the buoy).
- Each **column** = one thing that was measured (`panel_w`, `batt_v`, `timestamp`, …).

The buoy logs many *kinds* of events mixed together. We only want the solar readings, so we filter to rows where `event_type` is `"solar_data"`.

### The setup (do this once)

You need Python and a few free libraries. Open a terminal and run:

```bash
source /home/marinesitu/.venv/bin/activate     # turn on the project's Python environment
pip install darts scikit-learn matplotlib pandas
```

What those libraries are, in one line each:
- **pandas** — handles tables of data (think: Excel for Python).
- **matplotlib** — draws charts.
- **scikit-learn** — the classic toolbox of ML models.
- **darts** — a library made specifically for *forecasting over time*. It'll be our main tool.

### Loading and peeking at the data

```python
import pandas as pd

# Read the file into a table called df ("dataframe")
df = pd.read_csv("imta_0a10aced202194944a071780_20260624_130203.csv", low_memory=False)

# Keep only the solar readings
df = df[df["event_type"] == "solar_data"]

# Turn the text timestamps into real date-times the computer understands
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

print(df.shape)                    # how many rows and columns?
print(df[["timestamp", "panel_w"]].head())   # show the first 5 rows
```

Don't overthink `df`. It's just the nickname everyone gives their data table.

> 🧠 **Checkpoint:** In your own words, what is one *row* in this dataset? (Answer: one moment when the buoy recorded its sensors.)

---

## Lesson 3 — Time Series: Why "When" Changes Everything

Here's the single most important idea for our whole problem:

> **When data has a time order, the order itself carries information.**

A normal ML problem treats every row as independent — like predicting house prices, where house #5 tells you nothing special about house #6. But solar power is different: **noon today tells you a lot about noon tomorrow.** The sequence matters. Data like this is called a **time series**.

Every time series is a mix of three ingredients:

| Ingredient | What it means | In our buoy |
|---|---|---|
| **Seasonality** | A pattern that repeats | The daily sun cycle: zero at night, peak at noon — every day |
| **Trend** | A slow drift up or down | A gentle rise as summer days get longer |
| **Noise** | Random jitter you can't predict | A passing cloud, a sensor hiccup |

### See it for yourself

First we **resample** the data to hourly averages. Raw readings come every few seconds, which is too noisy and too much — averaging into one value per hour smooths it and makes patterns visible.

```python
import matplotlib.pyplot as plt

# Average everything into one row per hour, keep only panel_w
hourly = df.set_index("timestamp")[["panel_w"]].resample("h").mean().dropna()

hourly.plot(figsize=(14, 4), title="IMTA panel_w — hourly solar power")
plt.savefig("all_data.png")   # save the chart to a file you can open
```

You'll see a **repeating wave** — up every day, down every night, over and over. That repeating wave *is* the seasonality.

```python
# Now zoom into a single week — the daily rhythm is unmistakable
one_week = hourly["2026-06-01":"2026-06-07"]
one_week.plot(figsize=(12, 3), title="panel_w — June 1 to 7")
plt.savefig("one_week.png")
```

> 🧠 **Checkpoint:** Which of the three ingredients (seasonality / trend / noise) would a *cloud* be? (Answer: noise — it's unpredictable.)

---

## Lesson 4 — Your First Model Is the Dumbest One (On Purpose)

Beginners assume ML means "fancy." The pros do the opposite: **always try the dumbest possible model first.** It's your yardstick. If a fancy model can't beat the dumb one, the fancy one is worthless here.

Our dumb model is called **Naive Seasonal**, and its entire strategy is:

> "Tomorrow at noon will be exactly like *today* at noon."

It just copies the value from 24 hours ago. No learning, no math, no magic. The `K=24` below means "copy from 24 steps (hours) ago."

### A word on train / validation split

To test any model honestly, we hide some data from it:
- **Training set** — the data the model is allowed to learn from.
- **Validation set** — recent data we *hide*, then compare the model's guesses against. This is how we check if it actually works, instead of just memorizing.

We'll hide the **last 48 hours** and predict them.

```python
from darts import TimeSeries
from darts.models import NaiveSeasonal

# Convert our table into a darts "TimeSeries" object
series = TimeSeries.from_dataframe(hourly.reset_index(), time_col="timestamp", value_cols="panel_w")

train, val = series[:-48], series[-48:]   # hide the last 48 hours

model = NaiveSeasonal(K=24)   # "copy the value from 24 hours ago"
model.fit(train)              # "fit" = train. Here it just memorizes the cycle.
pred = model.predict(48)      # forecast the 48 hidden hours
```

### How do we know if it's good? Meet MAE

We need a number for "how wrong were we." The simplest one is **MAE — Mean Absolute Error**: on average, how many watts off was each prediction? Lower is better. `MAE = 3` means "off by 3 watts on average."

```python
from darts.metrics import mae
print("MAE:", mae(val, pred), "watts")
```

**The real result on June 14 data: MAE = 0.72 W.**

Read that again. The panel peaks at 100 W, and the dumb "copy yesterday" model was off by less than **one watt**. Why so good?

1. Only **35 days** of data exist — not enough for a fancy model to learn much.
2. **Gulf Coast summer** is boringly consistent — every day really does look like the last.
3. The **daily sun cycle is almost perfectly regular.**

**The analogy:** if someone asks "will it be sunny at noon tomorrow?", you can just look out the window at noon today. You don't need a weather model. That's Naive Seasonal.

> 🧠 **Checkpoint:** Why do we test the dumb model *first* and not last? (Answer: it sets the bar every other model has to clear.)

---

## Lesson 5 — Now the Actual Machine Learning

Naive Seasonal doesn't *learn* anything. Now we build models that do. The trick that lets a normal ML model handle time is called **lag features**.

### Lag features, explained with no math

A "lag" is just *a value from the past*. To predict the power **right now**, we hand the model the last 24 hours as clues:

```
To predict power at 12:00 today, the model sees:
   power 1 hour ago, power 2 hours ago, ... power 24 hours ago
```

`lag_24` is "the value 24 hours ago" — i.e. this time yesterday. The model learns a rule like: *"if it was sunny this time yesterday, it's probably sunny now."* We're turning a time problem into an ordinary "inputs → output" problem the model already knows how to handle.

### Linear Regression — the simplest learner

A **linear** model draws the best straight-line relationship between the past values and the answer. It literally learns weights like:

```
power_now = 0.82 × (power 24h ago) + 0.07 × (power 23h ago) + ...
```

```python
from darts.models import LinearRegressionModel

model = LinearRegressionModel(lags=24, output_chunk_length=48)
model.fit(train)
pred = model.predict(48)
```

**Result: MAE = 5.52 W.** Worse than the dumb model! Why? **A straight line can't trace a curve.** Solar power swoops up and down like a hill each day; a line can only approximate it. We need something that can bend.

### Random Forest — many simple models voting

This is where ML earns its keep. A **decision tree** asks yes/no questions:

```
Is the power 24h ago above 50 W?
   YES → is it before 2 pm? → guess 75 W
   NO  → guess 5 W
```

One tree is twitchy and **overfits** (it memorizes the training data and flops on anything new). The fix is wonderfully simple: **build 100 different trees and average their votes.** That's a **Random Forest**. The crowd is wiser than any single tree.

```python
from darts.models import RandomForestModel

model = RandomForestModel(lags=24, output_chunk_length=48,
                          n_estimators=100, random_state=42)
model.fit(train)
pred = model.predict(48)
```

**Result: MAE = 2.55 W — the best ML model.** Trees can bend with the daily curve, and the averaging stops them from overfitting. (`random_state=42` just makes the randomness repeatable so you get the same answer every run.)

### The scoreboard (June 14 data)

| Model | What it is | MAE (lower = better) |
|---|---|---|
| **Naive Seasonal** | Copy yesterday (dumb baseline) | **0.72 W** 🏆 |
| Random Forest | 100 trees voting | 2.55 W |
| SVR | Smooth-curve fitter | 3.43 W |
| Gradient Boosting | Trees fixing each other's mistakes | 3.00 W |
| Linear Regression | Straight-line fit | 5.52 W |
| AutoARIMA | Classic statistics model | 10.26 W |

> 🧠 **Checkpoint:** Why did the fancy Random Forest *lose* to the dumb baseline here? (Answer: too little data + extremely regular weather — the dumb rule was nearly perfect, leaving nothing for ML to improve on.)

---

## Lesson 6 — The Plot Twist: More Data Changes Who Wins

This is the most important lesson in the whole course, and most beginners miss it: **the "best model" is not fixed. It depends on how much data you have.**

The team ran the same models at three points in time as data accumulated:

| Model | June 4 (15 days) | June 14 (25 days) | June 24 (35 days) |
|---|---|---|---|
| Naive Seasonal | 5.06 W | **0.72 W** | 4.04 W |
| Random Forest | 6.24 W | 2.55 W | 5.27 W |
| SVR | 5.87 W | 3.43 W | **4.14 W** |

Read the story in those numbers:

1. **June 4 → 14:** everything got better. More data = more pattern to learn from.
2. **June 14:** a freak streak of identical days. "Copy yesterday" was nearly flawless (0.72 W).
3. **June 14 → 24:** the dumb model *collapsed* (0.72 → 4.04 W). The weather turned variable — and suddenly "yesterday" stopped predicting "today." Meanwhile SVR became the most robust.

**Why this is good news, not bad:** the moment the dumb baseline starts failing is the moment real ML becomes worth it. Variable weather is exactly when a model that *learns* beats a model that just *copies*.

The rough roadmap as data grows:

```
~15 days  → dumb baselines win (boring stable summer)
~60 days  → ML starts to compete (seasons begin shifting)
~90 days  → ML wins consistently (a full range of weather)
6 months  → deep learning (neural nets) becomes worth trying
```

> 🧠 **Checkpoint:** Your baseline suddenly gets much worse one week. Panic, or progress? (Answer: progress — it means the data got interesting enough for ML to matter.)

---

## Lesson 7 — Forecasting the Thing That Actually Matters: Battery

Solar power is nice, but the cameras don't care about sunlight directly — they care about the **battery voltage `batt_v`**. A full battery means cameras can run; an empty one means lights out no matter how sunny it is.

Good news: the **exact same pipeline** works on battery voltage. You just swap the column.

```python
hourly = (df.set_index("timestamp")[["batt_v"]]
            .resample("h").mean().dropna().reset_index())
# ...then run the same models as before
```

**Result:** Naive Seasonal scores **MAE = 0.009 V** — essentially perfect. ML models do 8–10× *worse*.

Why is the dumb model even more dominant here? Because battery voltage changes **slowly and smoothly** — it charges all day, drains all night, with very little surprise. The smoother and more regular something is, the harder it is to beat "just copy yesterday."

**The practical takeaway:** we can predict tomorrow's battery state with a one-line model. That's great news — it means the camera-scheduling decision rests on a prediction we can trust.

---

## Lesson 8 — Giving the Model a Weather Forecast (Covariates)

So far every model only looks at the buoy's *own past*. It has no idea whether *tomorrow* is forecast to be cloudy. A **covariate** fixes that — it's **extra outside information** you feed the model alongside the target's history.

For solar, the natural covariate is **how much sunlight is expected**. Two sources:

- **ERA5** — a giant historical weather dataset from the European weather agency. Its `ssrd` field is "surface solar radiation" — basically, how much sun hit that spot.
- **pvlib** — a physics library that computes the *theoretical* sunlight on a perfectly clear day for any location and time.

```python
import pvlib
location = pvlib.location.Location(30.201833, -87.965000, tz="US/Central")
times = pd.date_range("2026-05-20", "2026-06-24", freq="h", tz="US/Central")
clearsky = location.get_clearsky(times)   # ideal sun if zero clouds
```

Now the model can compare *ideal* sun to *actual* `panel_w`. The gap between them is, basically, the clouds.

### One rookie trap to remember

When you check how related two solar things are (their **correlation**), **only use daytime hours.** Nighttime is all zeros for both sun and power, and those matching zeros fake a strong relationship that isn't real.

```python
daytime = merged[merged["panel_w"] > 5]    # drop nighttime zeros
corr = daytime["panel_w"].corr(daytime["ssrd_w_m2"])
```

**Bonus diagnostic:** if actual power is far below the clear-sky ideal on a *cloudless* day, the panel might be dirty (salt spray!). The data can tell you the hardware needs cleaning.

---

## Lesson 9 — From Prediction to Decision

A forecast is useless until it *changes what you do*. Remember the whole point: **decide when to run the cameras.** This is a two-stage pipeline.

```
STAGE 1 — FORECAST
   predict next 48h of solar power and battery (Lessons 4–8)
        ↓
STAGE 2 — OPTIMIZE
   choose the camera schedule that maximizes uptime
   WITHOUT ever letting the battery drop too low
```

Stage 2 is an **optimizer** — a tool that searches every possible schedule and picks the best one that obeys your rules ("battery never below 20%"). A library called **CVXPY** solves this in milliseconds:

```python
import cvxpy as cp

x = cp.Variable(48, boolean=True)         # for each hour: cameras on (1) or off (0)
objective = cp.Maximize(cp.sum(x))        # goal: as many on-hours as possible
# constraints: battery must stay within safe limits all 48 hours
# (full code in the source materials)
```

You don't need to follow the syntax. The idea is what counts: **forecast → feed it to an optimizer → get a schedule.** The prediction work from Lessons 4–8 is what makes that schedule trustworthy.

Down the road, once 90+ days of data exist, a smarter approach called **reinforcement learning** can let the buoy *learn its own* scheduling policy by trial and error — but that's a sequel, not a rookie topic.

---

## Lesson 10 — Picking the Right Yardstick (Metrics)

You've used **MAE**. There are others, and choosing well matters:

| Metric | What it rewards | Use it when |
|---|---|---|
| **MAE** | Treats all errors equally | The default. Our solar forecasting. |
| **RMSE** | Punishes *big* misses extra hard | A huge miss is dangerous (e.g. could drain the battery) |
| **MdAPE** | Ignores weird outliers | Sensors sometimes log garbage (like `-1` errors) |

The lesson: don't blindly grab one number. Ask "**what kind of mistake hurts me most?**" — then pick the metric that punishes that mistake.

---

## You Did It — The Whole Picture

Here's everything you learned, as one flow:

```
Raw buoy data (114,000+ rows)
        ↓  filter to solar, average to hourly
Clean hourly time series (~700 rows)
        ↓  hide last 48h as a test
Train models & score with MAE
        ↓
Discover: dumb baseline wins... for now
        ↓
Add weather covariates (ERA5 / pvlib)
        ↓
Feed the forecast to an optimizer
        ↓
Decision: when to run the cameras
```

**What you can now honestly say you understand:**
- What ML is, and how it differs from normal programming
- What a time series is and its three ingredients
- Why you always benchmark against a dumb baseline
- What lag features, linear models, and random forests do
- Why "best model" depends on how much data you have
- How a forecast turns into a real-world decision

---

## Glossary (Bookmark This)

- **Model** — the thing that turns inputs into a prediction.
- **Training / fitting** — showing a model examples so it learns.
- **Forecast** — a prediction about the future.
- **Time series** — data where the time-order matters (like our solar readings).
- **Seasonality / trend / noise** — the repeating pattern / slow drift / random jitter in a time series.
- **Resampling** — squashing many readings into one per time bucket (e.g. per hour).
- **Train / validation split** — data the model learns from vs. hidden data we test it on.
- **Baseline** — the dumbest model, used as a yardstick.
- **Lag feature** — a past value used as an input ("value 24h ago").
- **Overfitting** — when a model memorizes training data and fails on new data.
- **Covariate** — extra outside information fed to the model (e.g. a weather forecast).
- **MAE / RMSE / MdAPE** — ways to measure how wrong predictions were.
- **Optimizer** — a tool that picks the best choice under a set of rules.

---

## Where to Go Next

1. **Re-run the benchmark on fresh data.** Is the dumb baseline still winning, or has ML caught up?
2. **Add ERA5 as a covariate** and see if cloudy-day forecasts improve.
3. **Wait for 90 days of data** (around mid-August 2026), then try neural-net models (CNN, GRU, TCN).
4. **Build the CVXPY optimizer** to close the loop from prediction to camera schedule.

*Built from the IMTA deployment materials: imta_forecast.ipynb, imta_batt_forecast.py, imta_cross_dataset_comparison.py, fetch_era5_comparison.py.*
