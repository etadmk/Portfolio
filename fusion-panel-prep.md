# Fusion ME Panel — Night-Before Prep

**Premise:** you have done all of this work. You have just lost the index to it. This document rebuilds the index, in the order a technical panel will pull on it.

---

## 00 — How to use tonight

| Time | Read | Why |
|---|---|---|
| 25 min | §1 Your own résumé, re-learned | The single highest-risk failure mode is fumbling *your own* project. Panels forgive not knowing their machine. They do not forgive not knowing your data. |
| 30 min | §2 The five equations + §3 The one-paragraph mental model | This is what you write on a whiteboard. Do it on paper twice. |
| 30 min | §4 Likely questions | Read the question, answer out loud *before* reading the model answer. |
| 15 min | §5 Fundamentals rapid-fire | Cheap points. They always ask two or three. |
| 10 min | §6 How to sound like a peer | Three things to volunteer unprompted. |
| 5 min | §9 Cheat card | Re-read this in the car / before the call. Nothing else. |

**Do not** try to memorise §5 exhaustively. Two forgotten correlations cost you nothing. One fumbled explanation of your own CHF number costs you the interview.

---

## 01 — Your background, re-learned

Read each project's **30-second pitch** out loud. That's the version you actually say. Everything below it is ammunition for follow-ups.

### Zap Energy — Advanced Materials Group, 2024
*Porous refractory metal structures + liquid-metal-blanket alloy development.*

**30-second pitch:**
> "At Zap I worked on two threads in the advanced materials group. One was thermophysical characterisation of candidate liquid-metal blanket alloys — preparing research alloys in an inert glovebox, finding the eutectic composition of a novel alloy family by STA, DSC and TGA, and checking microstructure by SEM/EDX and optical. The other was porous tungsten: COMSOL porous-media modelling for porosity and permeability, with density measured by Archimedes' method as the experimental cross-check."

**This is the most directly relevant thing on your résumé.** Lead with it if the role is PFC/blanket. Follow-ups they will ask:

- *Why a eutectic?* Lowest melting point in the system — for a liquid metal you want the melting point safely below the coldest point in the loop so you never freeze a duct. Eutectic also solidifies at a single temperature rather than through a mushy two-phase range.
- *How does DSC find a eutectic?* You ramp composition. The eutectic composition is the one where the solidus and liquidus merge into a single sharp endothermic peak on the heating trace — no separate solidus-then-liquidus pair, no long freezing range. Off-eutectic compositions show two thermal events.
- *Why Archimedes for density?* It measures bulk density including closed porosity, with no geometry assumption. Compare against theoretical full density → total porosity fraction. It does *not* tell you whether the porosity is connected, which is the property that actually matters for wicking — that needs permeability (flow) measurement or mercury/gas intrusion.
- *What did COMSOL give you?* Effective permeability and porosity of the sintered structure — i.e. the `k` in Darcy's law that you then feed into a capillary-limit calculation.
- **Proprietary boundary:** state it once, up front, calmly: *"Some of the compositions are proprietary, so I'll describe methods and the reasoning rather than the specific alloy system — happy to go as deep as you like on the technique side."* Say it before they have to ask. It reads as trustworthy, not evasive. Never volunteer a composition to seem impressive.

### UCSD TEMP Lab, 2023
*Capillary-fed thin-film evaporation; CHF characterisation.*

**30-second pitch:**
> "At UCSD I ran thin-film evaporation experiments on capillary wicks — anodic alumina, glass fibre membranes, and hydrogels — measuring capillary pressure, permeability and thin-film spreading. The design framework was Young–Laplace for the driving pressure and Darcy's law for the resistance, and the figure of merit was critical heat flux: how much flux you can push before the wick can't resupply the evaporating surface and it dries out. We characterised up to 600 W/cm² on the GB-140 glass-fibre samples."

**⚠️ Fix this before tomorrow:** your résumé says "sustain heat loads up to **600 W**" in one bullet and "CHF characterised up to **600 W/cm²**" in another. Those are different claims by a factor of the sample area. Decide which you can defend and know the sample footprint. If the heated area was ~1 cm², both are true and you say so. If it was larger, say the *flux* number and the *area*. A panel that catches an undefended order of magnitude will discount everything else you say. (Sanity check that helps you: the group's published glass-fibre membrane work reports ~486 W/cm² at ΔT ≈ 7 °C, so a ~600 W/cm² claim is in-family for that rig.)

**Why this project is your strongest card in a fusion PFC interview:** it *is* the CPS problem with water instead of lithium. Same driving equation, same resistance equation, same failure mode. Dryout in your rig = film loss exposing bare substrate in a divertor. Say that explicitly:
> "The capillary-porous-structure divertor is the same design problem I worked on at UCSD — capillary-fed thin-film evaporation with a dryout limit — with three things changed: the working fluid is a liquid metal, the substrate is refractory instead of alumina or glass, and there's a magnetic field. The Young–Laplace and Darcy framing transfers directly."

- *What actually sets CHF in a wick?* The capillary pressure budget. Available driving pressure `2σcosθ/r_c` must cover viscous liquid resistance (Darcy), vapour-side pressure drop, and gravity. When required exceeds available, the meniscus recedes into the wick, dry spots form, local temperature runs away.
- *The pore-size tension:* smaller pores → more capillary pressure (∝ 1/r) but lower permeability (∝ r²), so more viscous resistance. There's an optimum, and graded/hierarchical wicks exist precisely to break the trade (big channels for transport, fine pores at the surface for pressure).
- *Troubleshooting story lives here* — water transport inconsistencies, CHF deviations, multimeter inaccuracy. See §8.

### UIUC Energy & Multiphase Flow Lab, 2021–22
*Pool boiling nucleation; falling-film evaporation and crystallisation fouling.*

**30-second pitch:**
> "Two projects. Pool boiling: I tested stainless samples with different micron-scale groove densities and correlated nucleation-site density and spacing with boiling heat-transfer performance, using an automated DAQ rig with heater control and high-speed imaging. Falling-film: saltwater evaporation on steel and 3D-printed polymer tubes with wettability-patterned surfaces, quantifying fouling growth by OpenCV image processing and wave-velocity analysis, plus SEM of the CaCO₃ scale. Co-authored papers in ASME Journal of Heat and Mass Transfer and Desalination."

**The result to remember, because it's a genuinely good one:** hydrophobic bands confine scale to the hydrophilic zones — a 1.6 mm band stayed clean, while a 0.8 mm band got bridged and mineralised anyway. Geometry mattered as much as surface chemistry, and there's a minimum stripe width below which the benefit disappears.

**Why this is relevant to fusion, and it's a non-obvious bridge worth making yourself:** §08 of your primer lists *pore clogging over life* as an unsolved failure mode. That is crystallisation fouling. Say:
> "The closest thing I've studied to the pore-clogging failure mode is crystallisation fouling on desalination tubes — a transport-limited deposition process slowly destroying a heat-transfer surface, where the surface's wetting state governs where deposits nucleate. I don't want to over-claim the analogy, but the experimental approach transfers: you characterise the deposit morphology at the wetting boundary and you learn that pattern geometry has a threshold."

### MarineSitu — DOE/ORISE WPTO Marine Energy Fellow, 2025–present
*Virtual twin + duty-cycle optimisation for off-grid subsea platforms.*

**30-second pitch:**
> "I built a Python virtual twin for solar-powered off-grid underwater monitoring platforms — coupling ERA5 solar irradiance reanalysis, battery state of charge, and per-sensor power draw for cameras, sonar, UV-C antifouling and acoustics across multi-day deployments. Then three solvers on top of it: a greedy heuristic, a MILP, and an LP, producing sampling schedules that respect battery, duty-cycle and safety-floor constraints. Validated against ERA5 across five sites from Hawaii to Anchorage, and the output tells you which deployment scenarios are actually feasible by site and season."

**How to make this land with a fusion panel** (it isn't thermal, so frame it as the skill, not the subject): *"It's the same reasoning as defining an operating window — you have a physical model, hard constraints, and you're mapping the feasible envelope rather than optimising a single point. That's how I'd approach a surface-temperature window bounded by evaporative capacity on one side and core impurity influx on the other."* That sentence connects your newest project to §08 of the primer, which is exactly what a good candidate does.

- *Why three solvers?* Greedy for speed and a baseline; MILP when you need genuine optimality with integer on/off decisions per sensor per interval; LP as the relaxation — fast, gives a bound on how much the heuristic is leaving on the table.

### Personal — Transient 2D heat conduction solver
**30-second pitch:**
> "Explicit finite-difference FTCS solve of the 2D transient heat equation on a 20×20 grid — embedded constant-temperature source, Dirichlet on three sides, convective Robin on the fourth, with a Fourier-number stability check and the inner loop vectorised in NumPy."

- *Stability?* Explicit FTCS in 2D requires `Fo = αΔt/Δx² ≤ 1/4` (1/2 in 1D). The convective boundary node is *more* restrictive: `Fo(1 + Bi_Δx) ≤ 1/2` in 1D form, where `Bi_Δx = hΔx/k`. Know this — it's the classic follow-up.
- *Why not implicit?* Implicit (or Crank–Nicolson) is unconditionally stable and lets you take large time steps, at the cost of solving a linear system each step. For a small grid and a transient you want resolved anyway, explicit is simpler and fine.
- *Fusion relevance:* this is the tool you'd reach for to get the transient temperature field through a wick during an ELM — see the ΔT calculation in §2.3.

---

## 02 — The five equations you must be able to write cold

Write each one by hand, twice, before bed.

### 2.1 Young–Laplace — the driving pressure

```
Δp_cap,max = 2σ cos θ / r_c
```

Liquid Li at ~500 K: σ ≈ 0.40 N/m, pore radius r_c ≈ 5 µm, conditioned W surface θ ≈ 0°:

```
Δp = 2(0.40)/(5×10⁻⁶) = 1.6×10⁵ Pa = 160 kPa
```

**The comparison that makes the point:** ammonia at the same pore size gives ~3.3 kPa. Lithium's surface tension is ~15–20× a conventional heat-pipe fluid, so you get **~50× the capillary "engine."** That's the one-line reason liquid-metal CPS is credible at MW/m² flux and an ammonia heat pipe isn't in the conversation.

> Say it as: *"Same governing equation as any heat-pipe wick. Only the fluid properties change — and they change by more than an order of magnitude in the direction you want."*

### 2.2 Darcy — the resistance

```
u = -(k/µ) dp/dx        →      ṁ = ρ k A Δp / (µ L_eff)
```

Capillary pressure is a *ceiling*, not a rate. Darcy converts it into a flow. The design check is the pressure budget:

```
Δp_cap,available  ≥  Δp_liquid (Darcy) + Δp_vapour + Δp_gravity
```

Permeability estimate if pushed (Kozeny–Carman): `k ≈ ε³d²/[180(1-ε)²]`. For ε = 0.4, d = 10 µm → k ~ 10⁻¹³ m². Flag it as an order-of-magnitude.

### 2.3 Conduction across the wick — the coupling nobody expects you to name

```
ΔT = q″ · t / k_eff
```

10 MW/m² through a 1 mm wick with k_eff ≈ 50 W/m·K:

```
ΔT = (1×10⁷)(1×10⁻³)/50 = 200 K
```

**Why this matters more than it looks:** the wick ΔT sets the lithium *surface* temperature. Surface temperature sets Li vapour pressure — which climbs roughly exponentially. Vapour pressure sets lithium influx to the core plasma. So *wick thickness and effective conductivity are core-plasma-impurity parameters*, not just thermal ones. Note also that porosity **reduces** k_eff below dense tungsten, and lithium in the pores (k ≈ 45 W/m·K liquid) only partly compensates. Thin wick good for temperature, bad for supply margin. Real trade.

### 2.4 Hartmann — the MHD term heat pipes don't have

```
Ha = B L √(σ_e / µ)          Δp_MHD ~ Ha²  at large Ha
```

Lithium: σ_e ≈ 3.3×10⁶ S/m, µ ≈ 5.6×10⁻⁴ Pa·s → `√(σ_e/µ) ≈ 7.7×10⁴`.

| Case | B | L | Ha |
|---|---|---|---|
| Thin capillary film | 2 T | 100 µm | **≈ 15** — tractable |
| Bulk blanket duct | 5 T | 1 cm | **≈ 3,800** → Ha² ≈ 1.5×10⁷ |

**Same fluid, same field, only the length scale changed.** That single comparison is the whole argument for passive capillary supply at the plasma-facing surface, and the standard justification for **flow channel inserts** (electrically insulating duct liners) if you must pump a bulk loop.

> If asked *"how do you move the lithium?"* — the answer is **"at the surface, mostly you don't. Capillarity does it passively, and MHD is the reason you want it that way."**

### 2.5 Evaporation — and the order-of-magnitude that separates you from a memoriser

Lithium latent heat of vaporisation ≈ **21 MJ/kg** (145.9 kJ/mol ÷ 6.94 g/mol).

To reject 10 MW/m² *purely* by evaporation:
```
ṁ″ = q″/h_fg = 10⁷/(21×10⁶) ≈ 0.48 kg/m²·s
```
That is roughly half a kilogram of lithium per square metre per second. Nobody can supply that, and long before you failed to supply it you would have poisoned the core with lithium vapour.

**Therefore — and this is the insight to volunteer:**
> "Evaporation isn't the steady-state heat-removal path. Run the numbers and you'd need ~0.5 kg/m²·s of lithium at 10 MW/m², which is unsupportable and would violate the core impurity limit by a wide margin. Bulk heat removal is conduction through the film and wick into the actively cooled backplate. What the liquid buys you is a self-healing low-Z surface, wall conditioning, and a vapour-shielding buffer during transients — plus, in principle, breeding real estate. Evaporation matters as a transient mechanism and as the thing that sets the upper temperature limit, not as the cooling budget."

Some concepts (vapour-box style divertors) *do* deliberately lean on lithium vapour to dissipate power — worth one clause of acknowledgement so you don't sound absolutist.

**Also worth a sentence if evaporation comes up:** Hertz–Knudsen gives the free-molecular evaporative flux, `ṁ″ ≈ P_sat(T)/√(2πR_specific T)`, with P_sat from Clausius–Clapeyron. You don't need the constants — you need to say *"vapour pressure is exponential in temperature, so the impurity penalty for surface temperature is steep and the window is narrow."*

---

## 03 — The whole component in one paragraph

Memorise the **chain**, not the facts. If you can recite this, you can reconstruct almost any answer.

> Heat and particles arrive from the scrape-off layer. The heat conducts through the thin lithium film and the porous W–Re wick into an actively cooled backplate — that's the real cooling path. The temperature drop across the wick sets the lithium surface temperature; surface temperature sets lithium vapour pressure exponentially; vapour pressure sets lithium influx to the core, which is tolerable mainly because lithium is Z=3 and radiates roughly as Z² (a stray tungsten atom, Z=74, is vastly worse). Meanwhile the surface loses mass to evaporation and sputtering, and capillary pressure (Young–Laplace, ~160 kPa) must drive Darcy flow through the wick fast enough to replace that mass. If it can't, the film thins to dryout, bare tungsten faces the plasma, you get a local hot spot and high-Z sputtering. All of this sits in a multi-tesla field, so any conducting flow induces retarding Lorentz forces — at film scale Ha ≈ 15 and it's fine, at duct scale Ha ≈ 3,800 and it's a different problem entirely, which is why the surface is fed passively and why pumped loops need insulating flow channel inserts. On a slower clock, 14 MeV neutrons accumulate displacement damage in dpa and transmute W → Re → Os, both pushing the ductile-to-brittle transition temperature up over life; that bulk-material clock, not the liquid surface, is what eventually ends the component.

### Why lithium — name three reasons separately, they're testing whether you conflate them
1. **Low-Z / low core contamination.** Radiated power from a core impurity scales roughly as Z². Li (Z=3) vs W (Z=74).
2. **Self-healing.** A solid tile that erodes or melts leaves a permanent divot — a stress riser and a future hot spot. A thinned liquid film just gets rewetted.
3. **Wall conditioning / recycling control.** *This is the plasma-physics one and the one to volunteer.* Lithium getters deuterium at the wall, suppressing hydrogen recycling and measurably improving edge confinement (NSTX, LTX and related). The PFC isn't just surviving the plasma — it's improving it.
4. **(Bonus, reactor-relevant)** Lithium is the breeder: `⁶Li + n → T + ⁴He`. So the component is potentially breeding blanket real estate as well as armour. Note `⁷Li + n → T + ⁴He + n′` is endothermic, hence ⁶Li enrichment and neutron multipliers in real blanket designs, and TBR > 1 is the requirement for fuel self-sufficiency.

### Why porous W–Re — three jobs, in tension
- **Refractory host:** if the film locally dries out, bare substrate faces the plasma. Highest practical melting point wins. W ≈ 3,422 °C.
- **Re for irradiation:** pure W under 14 MeV neutrons suffers transmutation (W→Re→Os) and defect accumulation, both raising DBTT — a component that started ductile can be brittle at operating temperature after enough fluence. Pre-alloying with Re is a deliberate hedge, and W–Re retains better post-irradiation ductility than pure W in several irradiation studies. **That's the actual engineering argument, not "Re is a better metal."**
- **Porosity is non-negotiable:** no connected pore network, no capillary path, and you've built a solid tile with *worse* thermal conductivity than a dense one.

---

## 04 — Likely panel questions, with answers

**Q. Walk me through the concept.**
Recite §3. Then stop talking. Let them pick the thread.

**Q. Why do you need porosity? Why not just flow a film over a solid surface?**
Capillary action requires connected pore channels — it's what generates the pressure that resupplies the surface passively. Flowing a film over a solid means pumping a conducting liquid across a magnetic field, which is the Ha ≈ 3,800 problem. Passive capillary supply keeps the length scale at ~100 µm and Ha at ~15. Porosity is what lets you avoid MHD.

**Q. What's the binding constraint on this design?**
Not the capillary pressure ceiling — 160 kPa is a lot. It's the **mass balance**: whether replenishment flow through the wick matches combined evaporation plus sputtering mass loss at the target heat flux without thinning to bare substrate. Then say: *"and second, the surface temperature window, which is bounded below by wetting and above by lithium influx to the core."*

**Q. Order-of-magnitude the mass balance for me.**
This is the question that separates candidates. Have this ready and **state every assumption as you go**:

> Take a 0.1 m tall tile, 1 mm wick, k ≈ 10⁻¹³ m², Δp = 160 kPa, µ_Li ≈ 5.6×10⁻⁴ Pa·s, ρ_Li ≈ 500 kg/m³.
> Darcy velocity: u = kΔp/(µL) = (10⁻¹³)(1.6×10⁵)/[(5.6×10⁻⁴)(0.1)] ≈ 3×10⁻⁴ m/s.
> Mass supplied per unit surface area: ρ·u·(t/L) = 500 × 3×10⁻⁴ × 10⁻² ≈ 1.5×10⁻³ kg/m²·s.
> Loss side: divertor ion flux ~10²³–10²⁴ m⁻²s⁻¹, Li sputter yield ~0.1–1. At 10²³ and Y = 0.1 that's ~10⁻⁴ kg/m²·s — about a decade of margin. At 10²⁴ and Y near 1 it's ~10⁻² — a deficit of nearly an order of magnitude, and you dry out.
> So the answer is "it depends on flux and yield, and the design lives inside roughly one order of magnitude either side of failure." That's why this is the live question rather than a solved one.

Then add the caveat honestly: *"Those are order-of-magnitude numbers to show the structure of the calculation, not design values — permeability especially I'd want measured, not estimated from Kozeny–Carman."* Saying that **raises** your credibility.

**Q. Why not just use tungsten monoblocks like ITER?**
They're the mature answer and for good reason — water-cooled W monoblocks on CuCrZr are the demonstrated technology at ~10 MW/m². The liquid-metal case is about what happens beyond that: erosion is permanent on a solid, transient melting leaves permanent damage, and a solid surface does nothing for you plasma-side. Liquid lithium trades a well-understood engineering problem for a self-healing surface, recycling control, and higher transient tolerance — and takes on new problems (splashing, tritium retention, MHD, wetting) in exchange. It's a bet on a different risk portfolio, not a strict improvement.

**Q. What kills this component?**
Four clocks running at once:
1. **dpa** — displacement damage from 14 MeV neutrons, driving hardening and DBTT shift. A bulk-material clock independent of anything at the surface.
2. **Transmutation** — W→Re→Os drifts the alloy composition over life, so "W–xRe" is a moving target, not a one-time selection.
3. **Tritium retention** in the lithium and in the porous structure — a fuel-cycle and safety-inventory problem. Bred tritium trapped in the wick doesn't help TBR and does count against in-vessel inventory limits.
4. **Transients** — ELMs and disruptions, ms-scale loads far above steady SOL flux. For a liquid surface the open question isn't melting (nothing solid to melt) — it's **splashing and droplet ejection**, which wastes inventory and injects droplets as an uncontrolled impurity source.

**Q. How would you test whether the wick can keep up?**
This is *your* question — answer from experience, not theory:
> "The same way I characterised CHF at UCSD. Instrument a sample with a known heated area, ramp flux, and watch for the signature of incipient dryout — a departure from the linear q″ vs ΔT trend and a rise in surface temperature at fixed power. Independently measure permeability and pore-size distribution rather than inferring them, because that's the term I'd trust least. For lithium specifically, the hard parts are that you need vacuum and inert handling — which I did at Zap in glovebox and vacuum ops — and that diagnosing a moving liquid surface non-invasively is genuinely harder than a solid tile, so I'd want to be explicit up front about what's measured versus inferred."

**Q. How do you know the lithium wets the tungsten?**
You don't, for free. θ ≈ 0° is a *conditioned-surface* assumption. Oxide layers on tungsten block wetting, and you generally need elevated temperature plus a clean, oxide-free surface before lithium wets. Since capillary pressure goes as cos θ, loss of wetting is a direct loss of driving pressure — it's arguably the first thing to fail in practice and the assumption I'd interrogate first. (Then bridge: *"my UIUC work was on exactly this class of question — patterned wettability and how it governs where deposition happens."*)

**Q. What's the operating temperature window, and what sets it?**
Lower bound: lithium melting point (180.5 °C) plus enough margin to wet reliably and never freeze a feed path. Upper bound: lithium vapour pressure and hence core influx — commonly placed somewhere in the ~400–500 °C range for tokamak-relevant conditions, but concept-dependent and genuinely contested, which is why higher surface temperature giving more evaporative capacity is a *trade*, not a free win. **Hedge the upper number out loud** — "commonly quoted around 400–500 °C, but I'd treat it as machine-specific" — rather than asserting a precise value you can't source.

**Q. If you had one experiment and six months, what would you run?**
A defensible answer: measured permeability and pore-size distribution on the actual sintered W–Re structure, then a lithium-wetted capillary-limit test at relevant flux to find dryout, with the surface temperature and the mass-loss rate both instrumented. Rationale: the mass balance is the binding constraint (see above), permeability is the term with the widest uncertainty, and everything downstream — temperature window, impurity influx, lifetime — is conditional on it. State the reasoning; the specific choice matters less than showing you pick experiments by which uncertainty dominates the answer.

**Q. You've worked with water and ammonia wicks. What actually changes with lithium?**
Good, concrete list — this is a gift of a question:
- σ up ~15–20× → far more capillary pressure at the same pore size.
- Electrical conductivity → MHD exists at all. New physics, no analogue in your prior rigs.
- Prandtl number is ~0.01–0.05 instead of ~7 → thermal boundary layer much thicker than momentum layer, so standard Nu correlations don't apply; you'd use a liquid-metal correlation of the Lyon–Martinelli form (Nu as a function of Péclet).
- Chemical reactivity → glovebox/vacuum handling, oxide-driven wetting problems, compound formation that can clog pores.
- The fluid is now also nuclear fuel (breeding) and a tritium inventory site.
- The substrate is refractory and irradiated, so material properties drift over life.

**Q. What's the difference between a heat pipe and this?**
A heat pipe is a closed two-phase loop: evaporator, wick return, condenser. Here the "condenser" is the plasma chamber and the vapour is lost, not returned — it's an open system with an impurity budget instead of a closed cycle, and the wick is resupplying against mass *loss*, not just circulating. Plus MHD, plus irradiation.

**Q. What do you not know?**
Answer it straight. See §7.

---

## 05 — Fundamentals rapid-fire

Panels sprinkle these in. One or two sentences each is the right length.

**Heat transfer**
- **Biot number** `Bi = hL/k`: internal vs external resistance. Bi ≪ 1 → lumped capacitance is valid.
- **Fourier number** `Fo = αt/L²`: dimensionless time for conduction. Also the explicit-FD stability parameter.
- **Nusselt** `Nu = hL/k`: convective vs conductive. **Prandtl** `Pr = ν/α`: momentum vs thermal diffusivity — ~0.7 air, ~7 water, ~0.01–0.05 liquid metals.
- **Péclet** `Pe = Re·Pr`: advection vs diffusion. The relevant one for liquid metals.
- **Radiation** goes as T⁴ — dominant at PFC temperatures for anything with a view factor to a cold surface, negligible in your water rigs. Worth remembering the regime changes.
- **Thermal contact resistance** across bonded joints (e.g. wick to cooled backplate) is often the largest single ΔT in a real stack, and the hardest to predict. Good thing to raise unprompted about the backplate bond.

**Fluids**
- **Reynolds** `Re = ρuL/µ`. Wick flow is deeply laminar — Re ≪ 1, Darcy regime, Stokes flow.
- **Capillary number** `Ca = µu/σ`: viscous vs surface tension. **Bond number** `Bo = ρgL²/σ`: gravity vs surface tension — small Bo means capillarity wins, which is why fine pores work regardless of orientation.
- **Weber** `We = ρu²L/σ`: inertia vs surface tension — the number that governs **droplet ejection/splashing** during a transient. If splashing comes up, reach for We.
- **Marangoni / thermocapillary flow:** σ decreases with temperature, so surface tension gradients drag liquid from hot to cold — meaning the hottest spot is where the film *thins*, exactly the wrong direction. This is a real thin-film mechanism and naming it signals depth.

**Materials**
- **DBTT** and why irradiation raises it (defect accumulation impeding dislocation motion + transmutation-driven composition change).
- **Recrystallisation** of W is a separate degradation path from irradiation embrittlement — grain growth and loss of the worked microstructure above roughly 1,200–1,400 °C.
- **The honest counterpoint on W–Re** (see §6).
- **Sputtering:** physical sputtering yield rises with incident ion energy above a threshold and depends on mass ratio; lithium's yield is high, and there's additional temperature-dependent enhancement — which is precisely why the mass-loss side of the balance is uncertain.

**Mechanical**
- **Thermal stress** `σ ≈ EαΔT/(1-ν)` for a constrained plate — the reason CTE mismatch across a W-to-backplate joint is a design driver, and why "just braze it" is never the answer.
- **Thermal fatigue**: cyclic ΔT over thousands of pulses, not a single static load case. Divertor components are qualified by cycling.

---

## 06 — Three things to volunteer that make you sound like a peer

Deploy at most two. Volunteering all of them looks rehearsed.

**1. Evaporation isn't the cooling budget.** The 0.5 kg/m²·s calculation from §2.5. This is the single most effective thing in this document, because most people repeat "evaporative cooling" without ever dividing by the latent heat.

**2. Re alloying is a hedge, not a free win.** W–Re retains better post-irradiation ductility than pure W — but under irradiation W–Re also tends to form Re-rich precipitates (σ and χ phases) that produce their own hardening and embrittlement, and transmutation is moving the composition anyway. So the Re fraction is a life-averaged optimisation against two competing degradation mechanisms, not a one-time material selection. *Mark this as your understanding of the literature, not a measurement you made.*

**3. Thermoelectric MHD (TEMHD).** A temperature gradient across a liquid-metal/solid interface in a magnetic field drives thermoelectric currents, and those currents in the field drive flow you didn't design. It can be exploited — some concepts deliberately use TEMHD to drive lithium along trenches — or it can move your film in ways you didn't intend and cause local dryout. Mentioning TEMHD unprompted is a strong signal you've actually read the liquid-lithium PFC literature rather than a heat-pipe textbook.

---

## 07 — When you don't know

You will be asked something you can't answer. This is expected and is *not* the failure mode. Bluffing is.

**Use this structure:**
> "I haven't worked with that directly. The closest thing in my experience is ___, and here's how I'd reason about it: ___. What I'd want to know before committing to an answer is ___."

**Never** invent a number. If pressed for one you don't have: *"I'd be guessing — let me give you the order of magnitude and the assumption behind it, and flag that I'd want to check it."* Then do exactly that.

**If you blank on your own project detail** (entirely possible, it's been a year or more): *"I'd want to look at my notes for the exact value rather than misquote it — what I can tell you is the method and what the result drove."* Panels read this as integrity. They read a wrong confident number as a red flag about everything else.

**Numbers I'd defend vs. numbers I'd hedge:**

| Defend | Hedge out loud |
|---|---|
| 2σcosθ/r_c = 160 kPa (you can derive it) | Li operating temperature upper bound (~400–500 °C, concept-dependent) |
| Ha ≈ 15 vs ≈ 3,800 (you can derive it) | Permeability estimates from Kozeny–Carman |
| h_fg,Li ≈ 21 MJ/kg → 0.48 kg/m²·s at 10 MW/m² | Sputter yields and divertor ion flux (range, not value) |
| W melting point ~3,422 °C | dpa lifetime limits (design- and code-dependent) |
| Your own CHF number **once you've reconciled W vs W/cm²** | Anything from Zap that's proprietary |

---

## 08 — Behavioural, mapped to work you actually did

Pick **one** story for each and rehearse it out loud once. Structure: situation → what you did → what changed because of it.

**"Tell me about a time you debugged something hard."**
Your UCSD troubleshooting: water transport inconsistencies, CHF deviations, and multimeter inaccuracy. Fill in from memory: what was the symptom, what did you suspect first and why was it wrong, how did you isolate the instrumentation error from the physical one, what changed afterward. **The point of this story is that you distinguished a measurement artefact from a real physical effect** — that's the skill a panel is buying. If you only remember one thread, use the multimeter one: an instrumentation fault masquerading as physics is the most relatable debugging story in experimental engineering.

**"Tell me about working across disciplines."**
The UIUC falling-film work: experiments plus OpenCV image processing plus CFD validation support plus manuscript editing, landing in ASME JHMT and Desalination. Or Zap: materials, thermal analysis, characterisation, and simulation in one group.

**"Tell me about owning something end to end."**
MarineSitu: you built the model, wrote three solvers, validated against ERA5 across five sites, and the output is directly informing field deployment planning.

**"Tell me about a time you were wrong."**
Have one. The 0.8 mm vs 1.6 mm hydrophobic band result is a good frame if it fits your memory — a hypothesis about surface chemistry being sufficient, corrected by data showing geometry had a threshold. Only tell it if it's true; if not, use whatever real one you remember.

**"Why fusion / why us?"** Have a two-sentence answer ready. Something true: your last four projects have all been capillary-fed evaporation and porous-media heat transfer at high flux, and fusion PFCs are where that problem is hardest and matters most. Do not oversell — panels of engineers are allergic to it.

---

## 09 — Cheat card (this is all you read tomorrow morning)

**The chain:** SOL flux → conduction through film + wick → backplate coolant. Wick ΔT → surface T → Li vapour pressure (exponential) → core influx (tolerable because Z=3, radiates ~Z²). Mass loss (evap + sputter) must be replaced by Young–Laplace pressure driving Darcy flow. Fail → dryout → bare W → hot spot + high-Z sputtering. All in a B field → Ha ≈ 15 at film scale (fine), ≈ 3,800 at duct scale (not fine) → passive capillary at the surface, FCIs if you must pump. Slow clock: dpa + W→Re→Os transmutation → DBTT up → that's what ends it.

**Five numbers:**
- Δp_cap = 2σcosθ/r_c = 2(0.40)/(5×10⁻⁶) = **160 kPa** (vs ~3.3 kPa ammonia, ~50×)
- Ha = BL√(σ_e/µ), √(3.3×10⁶/5.6×10⁻⁴) ≈ 7.7×10⁴ → **15** (2 T, 100 µm) vs **3,800** (5 T, 1 cm)
- ΔT = q″t/k_eff = 10⁷ × 10⁻³/50 = **200 K** across a 1 mm wick at 10 MW/m²
- h_fg,Li ≈ **21 MJ/kg** → 10 MW/m² all-evaporative = **0.48 kg/m²·s** = impossible
- W melts at **3,422 °C**; Li melts at **180.5 °C**; Li Z=3, W Z=74

**Three reasons for Li:** low-Z core contamination · self-healing surface · deuterium gettering / recycling control (volunteer this one). Bonus: ⁶Li + n → T + ⁴He, breeding.

**Three jobs for porous W–Re:** refractory backstop on dryout · Re hedges transmutation-driven DBTT shift · connected porosity or there's no capillary path at all.

**Volunteer:** evaporation isn't the cooling budget · Re is a hedge with its own precipitate-embrittlement counterpoint · TEMHD.

**Your bridge sentence:** *"CPS is the capillary-fed thin-film evaporation problem I worked on at UCSD, with a liquid metal, a refractory substrate, and a magnetic field added — and the porous tungsten permeability side of it is what I did at Zap."*

**Before you walk in:** reconcile 600 W vs 600 W/cm² and know the heated area. State the Zap proprietary boundary early and calmly. Hedge the numbers in the right-hand column of §7. Don't invent numbers.
