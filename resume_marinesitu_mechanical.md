# Aditi Kalle
**Marine / Mechanical Engineer — Renewable Energy & Power Systems**
aditi@marinesitu.com

---

## Professional Summary

Mechanical engineer specializing in **off-grid renewable power systems**, **energy modeling**, and **marine hardware**. Background in thermal systems and renewable energy. Built power-analysis and optimization tools that turn field telemetry into battery/solar sizing, power budgets, and operational scheduling decisions. DOE/ORISE Marine Energy Fellow.

---


## Experience

### Marine Energy Fellow (DOE/ORISE) — MarineSitu
*Sept 2025 – Present | Seattle, WA*

---

**AMEC System Analysis** *(Sept – Nov 2025)*
- Developed monitoring-selection and power-analysis tools for the AMEC marine system.
- Conducted and documented power measurements with repeatable measurement procedures.
- Compiled the full **AMEC power budget**.
- Produced **battery (7–18 Ah)** and **solar (30–109 W)** sizing recommendations across **7 operational profiles** using location-specific solar data.
- Built a Python **Marine System Power Analysis Tool** with time-series, phase-aware, component-level modeling.

**IMTA Power Analysis** *(Oct – Nov 2025)*
- Completed power modeling for a solar-powered marine monitoring system.
- Evaluated multiple operational scenarios and Jetson compute profiles.
- Generated daily energy estimates ranging **141–783 Wh/day**.
- Created a reusable modeling framework, later adapted for AMEC systems.
- Refined models iteratively based on team feedback.

**Hybrid Power Modeling & Optimization** *(Oct 2025 – Jan 2026)*
- Reviewed hybrid-economics models and led/participated in code walkthroughs.
- Designed and built the **MarineSitu Sampling Strategy** optimization tool.
- Implemented an object-oriented framework with YAML configuration and pipeline architecture.
- Developed the implementation roadmap for next-phase work.

**IMTA Energy-Aware Scheduling & Forecasting** *(May 2026 – Present)*
- Characterized the buoy's off-grid power system — **100W solar, 12V 100Ah (1200 Wh) LiFePO4, MPPT** — from 35 days of field telemetry; derived a **~230 Wh/day** energy budget.
- Extracted true loads from telemetry: **1.7W** always-on base load, **5.5W** underwater camera, and a corrected **34.5W total system draw** (identified and fixed a mislabeled figure that had attributed the whole system's draw to a single camera); established a realistic **23% duty cycle** as the governing power constraint.
- Defined safe battery envelope (**20–90% SoC**) and built a proportional power-allocation scheme that held the battery in-bounds with zero over-discharge across the deployment.
- Built solar-forecasting models (LSTM + baselines, **0.93W MAE**) and formulated camera scheduling as constrained optimization (integer LP, CVXPY) under battery and solar-availability limits.
- Ran a hardware-validation review with the system's technical contact that overturned an initial "panel degradation" diagnosis — isolated the true cause to charge-controller curtailment using raw charge-state telemetry, and separated a second anomaly to a distinct root cause using the same method.
- Presented findings and secured stakeholder approval for the forecasting + scheduling approach.

**Cross-Site Solar Diagnostics — Second Deployment** *(Aug 2026 – Present)*
- Applied the curtailment-vs-fault diagnostic method developed for the primary buoy to a second, independently-owned solar deployment, using only daily-summary telemetry and weather data.
- Identified a curtailment pattern (harvest decoupled from cloud cover) from indirect evidence, then confirmed it directly with the site's engineering contact.
- Diagnosed a multi-day total power-loss event by cross-referencing weather telemetry against harvest data, flagging a wind-speed anomaly that was later confirmed as the physical root cause (a solar panel mount failure) — resolving the issue without access to fault-level telemetry.
- Built a short-term solar production forecast (24-hour and 7-day) by calibrating open weather-API irradiance data against the site's own historical harvest, flagging a specific low-generation day ahead of time.
- Coordinated directly with external engineering stakeholders to close out battery specification and hardware questions, and scoped a follow-on analysis for a second related system with shared hardware.

---

## Technical Skills

- **Energy systems:** Off-grid solar/battery sizing, power budgeting, MPPT charge control, battery SoC management, duty-cycle & load analysis
- **Modeling & optimization:** Time-series and phase-aware power modeling, component-level energy modeling, constrained optimization (linear programming, CVXPY), forecasting
- **Marine/mechanical:** Marine-grade hardware selection, corrosion/biofouling failure analysis, field power measurement, repeatable test procedures
- **Software:** Python (NumPy, pandas, scikit-learn), object-oriented design, YAML-configured pipelines, cloud telemetry (GCP/Firestore)
- **Thermal & renewable:** Thermal systems, renewable energy integration

---

## Education

*[Degree, Institution, Year — fill in]*
