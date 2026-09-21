# Check-In

**DOE/ORISE Marine Energy Fellow · MarineSitu**
**Focus:** Blue Robotics solar installation — curtailment analysis & fault investigation

---

## This week at a glance

- Diagnosed a second deployment site (Hawaii Island) using the same curtailment-vs-fault method built for the primary buoy.
- Found the daily harvest pattern was **curtailment**, not weather-limited — confirmed directly by the site's hardware contact.
- Traced a two-day total power loss event to a **specific physical cause**, starting from a small anomaly in a weather chart.
- Corrected a mislabeled power-draw figure across five internal scripts and a portfolio document, based on an earlier hardware review.
- Identified a related second system (near-identical hardware) as the next candidate for the same analysis.

---

## 1. Curtailment finding — Hawaii Island site

Daily solar harvest stayed flat (~180–240 Wh/day) regardless of cloud cover ranging from 26% to 93%. That pattern — harvest decoupled from weather — is the signature of a charge controller **curtailing** power once the battery reaches a full/float state, not a system that's actually weather-limited.

This was later confirmed directly: the system is sized with **more solar generation capacity than its load needs**, so it hits float most days independent of conditions.

*Artifact: dashboard comparing this finding against the primary buoy's own confirmed curtailment case.*

---

## 2. Fault investigation — two-day power collapse

A separate, two-day event showed total power collection dropping to near-zero, with battery voltage sagging low. Investigation steps:

1. Flagged the event and initially set it aside as a separate open question rather than folding it into the curtailment story.
2. While comparing charts side by side, noticed a small **wind-speed uptick** lining up with the timing of the power collapse — flagged as an unconfirmed lead.
3. Sent targeted questions to the site's hardware contact: battery capacity, minute-level telemetry availability, and a sanity check on the wind correlation.
4. **Confirmed:** the solar panel had physically detached from its mounting in high wind. The wind uptick was the actual cause, not a coincidence.

**Why it matters:** this was a mechanical/mounting failure, not an electrical or battery fault — a materially different (and simpler) fix than the alternative explanations would have required.

---

## 3. Battery specification — a caveat worth flagging

The site's battery was identified as a repurposed consumer power station (512 Wh nameplate rating). However, its original built-in safety electronics were damaged in an unrelated prior incident and are now bypassed — the cell pack runs directly through a generic cell balancer and the site's charge controller instead.

**Open item:** the nameplate capacity assumes the original electronics were still in the loop. The real usable capacity and safe voltage floor should be derived from the underlying cell specifications, not the nameplate figure, before it's used in any safe-operating-floor calculation.

---

## 4. Power-draw correction (primary buoy)

Following an earlier hardware review, corrected a mislabeled power figure that had been attributed to a single camera when it actually represented the whole system's draw (base load + underwater camera + surviving top-side camera). Updated across the optimizer, input-validation script, a modeling notebook, and a portfolio document — five files total.

---

## Next steps

- [ ] Resolve the battery's real usable capacity from cell specs rather than nameplate rating.
- [ ] Apply the same curtailment-vs-fault method to the related second system once its data comes through — same charge controller and battery model, so the method should transfer directly.
- [ ] Fold the confirmed Hawaii Island findings into the broader cross-site comparison work.
