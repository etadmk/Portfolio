# Fluid Systems Engineer Interview Prep — Form Energy

*Companion to your technical primer. This one is about performing under interview conditions: what they ask, how to structure answers, and what to signal.*

---

## 1. The process — what to expect

Based on recent candidate reports, Form runs a thorough but conventional engineering loop:

1. **Recruiter phone screen** — role fit, motivation, logistics, compensation range.
2. **Hiring-manager screen** — your background, why Form, high-level technical fit.
3. **Technical presentation (~30 min) + Q&A** — you present a past project; they probe your depth. This is the single most important stage. Often followed by 1:1 (sometimes 2:1) breakout interviews the same day. A full interview day runs ~4–5 hours, often remote first.
4. **Onsite + site tour** — meet several team members in person.

Total timeline averages about a month. Difficulty is moderate (~3/5). Culture signals from reviewers: fast-paced, aggressive timelines, "self-driven and OK with rapidly changing dynamics." Interpret that as: they want people who can own ambiguity, not just execute a spec.

**The two things that decide the loop:** (1) how crisply you present and defend your own past work, and (2) whether your fundamentals are *reflexive* — you can reason from first principles out loud, not just recall formulas.

---

## 2. Your technical presentation — prep this hardest

Pick a project where **you personally owned a fluid/thermal problem end to end**. Structure it as a story, not a report:

- **Problem & constraints** (30 sec) — what was hard, what were the limits (cost, space, temperature, flow rate).
- **Approach** — the physics you reasoned from, the assumptions you made and *why*, the tradeoffs you weighed.
- **Analysis/tooling** — hand calcs first, then CFD/simulation. Interviewers love seeing that you sanity-checked simulation against a back-of-envelope estimate.
- **Result & validation** — did it match prediction? What did you learn when it didn't?
- **What you'd do differently** — signals maturity.

**Rehearse the Q&A more than the talk.** Expect: "Why did you assume X?" "What if the flow were turbulent instead?" "How sensitive is your result to that boundary condition?" "What would you have done with half the budget?" Prepare to defend every assumption and to gracefully say "I don't know, here's how I'd find out" when cornered — that answer scores well.

**Tie it to Form if you can:** end with one sentence connecting your project's lesson to LDES challenges (flow distribution, thermal uniformity, two-phase handling, corrosion).

---

## 3. Core fluids questions — answer frameworks

These are the fundamentals most likely to come up in breakouts. Don't memorize paragraphs; internalize the *structure* of a good answer.

**"Walk me through how you'd size a pump for a coolant/electrolyte loop."**
Frame it as finding the operating point: build the **system curve** (static head + kQ² friction/minor losses via Darcy-Weisbach), overlay the **pump curve**, and pick a pump whose Best Efficiency Point sits near the intersection at design flow. Then check **NPSH available > NPSH required** with margin to avoid cavitation — flag that hot electrolyte raises vapor pressure and shrinks NPSHA. Mention you'd budget parasitic pumping power because at low current density it eats into round-trip efficiency.

**"Laminar or turbulent — how do you know, and why do you care?"**
Reynolds number, Re = ρVD/μ; transition ~2300 in pipes. Why it matters: sets friction factor (f = 64/Re laminar vs. Moody/Colebrook turbulent), heat-transfer coefficient, and mixing/mass-transfer behavior. Add the nuance that battery channels often run laminar or transitional, so you'd watch entrance-length effects — fully-developed correlations under-predict Δp in short channels.

**"How do you calculate pressure drop across [a manifold / a packed bed / a channel]?"**
- Pipe/channel: Darcy-Weisbach for major losses + K-factors for minor losses (in compact skids, minor losses often dominate — say this).
- Packed bed of iron pellets: **Ergun equation** (viscous Kozeny-Carman term + inertial Burke-Plummer term); Darcy's law alone only holds at low Re.
- Manifold/network: mass balance at nodes, head balance around loops.

**"You have 100 parallel cells and flow isn't even across them. What do you do?"**
This is *the* iron-air-relevant question. Answer: it's a header-vs-channel resistance problem. Increasing channel resistance relative to manifold resistance improves uniformity; widening the header lowers overall Δp and improves distribution; lower feed rates distribute more evenly; inlet geometry matters (vortices/separation); U- vs. Z-type headers differ. Quantify with a non-uniformity factor (std dev of per-channel flow). Note the tradeoff: more uniform distribution usually costs more pumping power.

**"Explain the dimensionless numbers you'd use and what each tells you."**
Re (inertial/viscous → flow regime), Pr (momentum vs. thermal diffusivity → boundary-layer ratio), Nu (dimensionless convective heat transfer → output of h correlations), Sc (momentum vs. mass diffusivity → mass-transfer analog of Pr), Sh (dimensionless mass transfer → analog of Nu), Pe (advective vs. diffusive transport = Re·Pr or Re·Sc). Bonus: Gr/Ra for natural convection, Bi for internal-vs-surface conduction resistance.

**"How does fluid flow couple to heat transfer in a battery?"**
Flow rate sets h (via Nu correlations), h sets cell temperature, temperature sets reaction kinetics, gas solubility, and evaporation — a two-way coupling. Emphasize temperature *uniformity*, not just peak temperature: non-uniformity drives cell-to-cell voltage spread. For iron-air add that the heat load *changes sign* (exothermic discharge, endothermic charge), so you may need heating as well as cooling.

**"Bernoulli — when can you use it and when can't you?"**
It's an inviscid, incompressible, steady, along-a-streamline integral of momentum with negligible losses. Most real battery plumbing violates the no-loss assumption, so treat it as a quick sanity check, not a design tool. Naming its limits is what they're testing.

---

## 4. Applied iron-air systems questions

Here they test whether you understand *their* system, not just textbook fluids.

**"Why is the air electrode the hard part?"**
It's a gas-diffusion electrode that must admit O₂ while keeping electrolyte in, survive thousands of wetting/drying cycles without flooding or drying, and run bifunctionally (ORR on discharge, OER on charge) with sluggish kinetics that cost voltage efficiency. Three failure modes to name: **CO₂ carbonation** (atmospheric CO₂ + KOH → carbonate crystals that clog pores), **flooding/drying balance**, and **oxygen-evolution overpotential** on charge.

**"Why manage CO₂ and humidity in the intake air?"**
CO₂ forms carbonates that degrade the KOH electrolyte and clog electrode pores; humidity shifts the electrolyte water balance (water is a reactant here). So air-flow rate, humidity, and CO₂ are coupled control variables — you'd scrub CO₂ and/or actively manage electrolyte carbonate.

**"Iron-air is only ~40–50% round-trip efficient. Why is that acceptable?"**
Because it buys ~10× lower cost, and the economics work when you charge from otherwise-curtailed, near-zero-cost renewables over multi-day windows. The main efficiency drains are parasitic hydrogen evolution at the iron electrode (hurts coulombic efficiency + a localized safety issue) and ORR/OER overpotentials (hurt voltage efficiency). Connecting the physics to the *business case* is a strong signal.

**"How does gas evolution affect the fluid system?"**
Parasitic H₂ (on charge) and O₂ handling make parts of the system two-phase. Bubbles do two opposing things: they displace conductive electrolyte (raising ohmic resistance and reducing active area) but also stir the boundary layer (enhancing mass transfer, lowering concentration overpotential). You'd design gas-liquid separation and venting so H₂ never reaches hazardous concentrations.

**"How does mass transport couple to the flow you design?"**
Three mechanisms move species: migration (potential gradient), diffusion (concentration gradient), convection (bulk motion — the part you engineer). When reaction outruns transport you hit a limiting current and concentration overpotential spikes. Convection thins the diffusion boundary layer and raises the limiting current — which is exactly why electrolyte circulation and bubble stirring matter.

**"What worries you about materials in this system?"**
Hot concentrated KOH is aggressive. Compatible: many fluoropolymers (PTFE, PVDF), polyolefins (HDPE, PP), nickel, some stainless. Attacked: aluminum, glass, many elastomers. You'd verify every wetted material, seal, and gasket at *actual* concentration and temperature, avoid galvanic couples, and design against iron-electrode passivation and seal creep over long cycles.

---

## 5. Show you know the company (recent context)

Dropping current, accurate facts signals genuine interest. As of early–mid 2026:

- **Manufacturing is live.** Form launched production at its first high-volume facility in **Weirton, West Virginia** and began delivering its first commercial pilot (Minnesota, with **Great River Energy**), with the full project expected online in 2026.
- **Massive commercial pipeline** — over **75 GWh** under agreement. Landmark deals include a **300 MW / 30 GWh** system with **Xcel Energy** in **Pine Island, Minnesota** tied to a **Google** data center (~$1B, described as among the largest battery projects by energy capacity announced globally).
- **AI-data-center demand is a new driver** — a **12 GWh** capacity agreement with **Crusoe** (announced at CERAWeek 2026) to power AI infrastructure starting 2027.
- **First international deployment** — a **10 MW / 1,000 MWh** project with **FuturEnergy Ireland** in northwest Ireland, targeted for 2029.
- **Safety story** — their iron-air cells passed UL 9540A testing with no thermal runaway or fire, a structural advantage over lithium-ion for siting.

**How to use this:** don't recite it. Weave one or two facts into a question or an answer — e.g., "With the Crusoe and Google-scale deployments moving from pilots to gigawatt-hour builds, I'd imagine flow-distribution and thermal uniformity across that many cells becomes a huge manufacturing-and-reliability problem — is that where this role sits?"

---

## 6. Behavioral & mission-fit

Form's own reviewers stress fast pace, aggressive timelines, and needing to be self-driven. Prepare STAR-format stories (Situation, Task, Action, Result) for:

- **Owning ambiguity** — a time you defined the problem yourself, not just solved a handed-down spec.
- **A failure / wrong assumption** — what broke, how you caught it, what you changed. (They *will* ask.)
- **Cross-functional friction** — working with people outside your discipline (electrochemists, manufacturing, controls). Iron-air is inherently multidisciplinary; show you can speak across boundaries.
- **Moving fast under uncertainty** — shipping a "good enough, validated" answer on a deadline vs. chasing perfection.
- **Why Form / why LDES** — have a genuine, specific answer. "Lithium can't cost-effectively do multi-day storage; iron-air can, and that's the piece the grid actually needs for deep decarbonization" is a solid spine. Make it yours.

For early-career specifically: they're hiring for **trajectory and reasoning**, not a finished expert. It's fine to say "I haven't done X, but here's how I'd approach it" — the reasoning is the signal.

---

## 7. Smart questions to ask them

Good questions double as competence signals:

- Which subsystem would I own first — air handling, electrolyte/water management, or thermal?
- How do you balance parasitic balance-of-plant power against round-trip efficiency at low current density?
- How much of the fluids work is CFD/simulation vs. hand calcs vs. hardware testing?
- As you scale from pilots to gigawatt-hour deployments, what's changing most in the fluid-systems challenges — is it manufacturability, flow uniformity at scale, or field reliability?
- What does the sim-to-test validation loop look like here?
- Where does this role sit relative to the electrochemistry and manufacturing teams?

---

## 8. Morning-of cheat sheet

**Equations to have cold**
- Re = ρVD/μ (transition ~2300)
- Darcy-Weisbach: Δp = f(L/D)(ρV²/2); f = 64/Re (laminar)
- Bernoulli (know its 4 assumptions)
- Darcy's law: v = −(κ/μ)∇p; Ergun for packed beds
- Newton's cooling: q″ = h(Ts − T∞); Nu = hL/k
- Nernst: E = E° − (RT/nF)ln Q
- Faraday: moles = It/nF (links current → reactant/gas rate)
- Pump: operating point = pump curve ∩ system curve; check NPSHA > NPSHR

**Dimensionless quick-recall**
Re (flow regime) · Pr (heat, ν/α) · Nu (conv. heat out) · Sc (mass, ν/D) · Sh (conv. mass out) · Pe (advection/diffusion)

**Iron-air one-liners**
- Reversible rusting: discharge breathes in O₂ (Fe → rust); charge breathes out O₂ (rust → Fe).
- ~1.28 V OCV, ~764 Wh/kg theoretical (iron-air literature, not Form-confirmed).
- ~40–50% RTE = the price of ~10× lower cost; works charging from curtailed renewables.
- Air electrode = the hard part (carbonation, flooding/drying, OER overpotential).
- Chemistry is simple; balance-of-plant (air/water/thermal) is where fluids engineers add value.

**Mindset:** reason out loud, sanity-check simulation with hand calcs, defend your assumptions, and say "I'd find out by…" instead of bluffing.
