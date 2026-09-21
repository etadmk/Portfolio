# Résumé Concepts — Deep Study

Everything on your résumé except MarineSitu, rebuilt from first principles. Assume no prior knowledge; each concept is explained, then given a governing equation, then the question a panel actually asks about it.

**⚑ = high probability. If you're short on time, study only the ⚑ items.**

**The through-line, before you start.** Every project on this résumé is the *same* problem: **a liquid supplying heat to or from a hot surface, and what happens when the supply fails.** Pool boiling — the surface dries out and you hit CHF. Falling film — dry patches form below a minimum wetting rate. Capillary wicks — the meniscus recedes and you dry out. Fouling — the surface gets insulated by scale. Porous tungsten — the wick can't resupply the lithium. You have spent five years on one problem in five different fluids. **Say that sentence in the interview.**

---

# PART A — Zap Energy: Alloys and Porous Refractories

## A1. Phase diagrams and eutectics ⚑

*This is the single most likely deep-dive area, because it's your work and it's now their core competency.*

**What a binary phase diagram is.** Composition on the x-axis, temperature on the y. It maps which phases exist at equilibrium. Two lines matter:

- **Liquidus** — above it, everything is liquid. Cooling through it, the first solid appears.
- **Solidus** — below it, everything is solid. The gap between them is the **freezing range**, where liquid and solid coexist as a slurry (the "mushy zone").

**The eutectic point** is where the liquidus lines from both sides meet at a minimum, and liquidus and solidus touch. At that one composition:

```
L  →  α + β        at a single, fixed temperature
```

Liquid transforms directly into two solid phases with **no freezing range at all**. It's an *invariant* reaction — temperature is pinned while it happens.

**⚑ Why you wanted a eutectic (the answer that connects to their hardware).** Two reasons, and give both:

1. **Lowest melting point in the system.** The eutectic is the minimum of the liquidus surface. If your job is to keep a liquid metal molten in a loop, you want the lowest possible melting point, because every pipe, valve and cold leg in that loop must be held above it, forever.
2. **No mushy zone.** An off-eutectic alloy freezes *gradually* over a temperature range — you get solid crystals suspended in liquid, i.e. a slurry that can plug a line or a valve seat. A eutectic goes liquid-to-solid at one temperature. Freeze protection becomes a single setpoint rather than a margin against partial solidification.

Zap's public description of liquid-metal operations says the cardinal rule is keeping the metal hotter than its melting point so nothing solidifies in the pipes. **Your eutectic measurement is the number that sets that setpoint.** That's the sentence to land.

**Ternary phase diagrams** (your résumé says ternary). Three components, so composition needs two dimensions — hence the **Gibbs triangle**: each corner is a pure component, each point inside is a unique three-component composition, and the three coordinates always sum to 100%. Temperature becomes the third dimension, so you either draw a 3D liquidus surface or take horizontal slices (**isotherms**) or vertical slices (**isopleths**).

Structure to know: three binary eutectics sit on the three edges. From each, a **eutectic valley** runs down the liquidus surface into the interior. Where all three valleys meet is the **ternary eutectic** — the lowest melting point anywhere in the system. *That's what "investigating the eutectic composition of a novel alloy family" means: you were hunting the bottom of that surface.*

**Vocabulary that gets tested:**

| Reaction | What happens | Mnemonic |
|---|---|---|
| **Eutectic** | L → α + β | one liquid, two solids, on cooling |
| **Eutectoid** | γ → α + β | all solid; no liquid involved |
| **Peritectic** | L + α → β | liquid *plus* a solid make a new solid |
| **Congruent melting** | α → L, same composition | a pure-compound-like melting point |

- **Hypoeutectic / hypereutectic** — composition below / above the eutectic. Both freeze with a primary phase first, then the remaining liquid hits the eutectic and solidifies eutectically.
- **Lever rule** — in a two-phase region, the fraction of each phase: `f_α = (C_β − C_0)/(C_β − C_α)`. Weights on a lever about the overall composition.
- **Gibbs phase rule** — `F = C − P + 2`, or at constant pressure `F = C − P + 1`. For a binary at constant pressure with three phases present, F = 0: zero degrees of freedom, which is *why* the eutectic occurs at one fixed temperature and composition. **If you can say that, you've explained eutectics from thermodynamics rather than from a picture.**

**"Thermodynamic modelling"** on your résumé means CALPHAD-style work: you build or use Gibbs free energy models for each phase, then let software minimise total G to predict which phases are stable at a given composition and temperature (Thermo-Calc, FactSage, Pandat). You model first so you know *where to look* before you spend a week melting samples. Be honest about how much of this you did versus consumed.

> **Q. Why not just pick the lowest-melting pure metal?**
> Because you're also constrained by boiling point / vapour pressure at operating temperature, by chemical compatibility with the structural material, by thermal conductivity and heat capacity, and by neutronics. The eutectic is how you buy a low melting point without giving up the other properties — you're optimising a multi-property vector, not one number.

## A2. Thermal analysis — STA, DSC, TGA ⚑

**DSC (differential scanning calorimetry)** measures the *difference in heat flow* between your sample and an inert reference as both are ramped in temperature. When the sample undergoes a transformation, it absorbs or releases heat that the reference doesn't, and that shows up as a peak.

- **Melting is endothermic** → a peak in the absorbing direction on heating.
- **Peak area = enthalpy of the transformation** (ΔH_fusion), after calibration.
- **Onset temperature** (extrapolated, where the leading edge departs baseline) is the physically meaningful transition temperature. The *peak maximum* lags it and depends on heating rate.

**⚑ How DSC identifies a eutectic.** Two signatures, and knowing both is the good answer:

1. **A single sharp peak instead of two events.** An off-eutectic composition shows a solidus event followed by a broad melting range up to the liquidus. At the eutectic, solidus and liquidus coincide — one narrow peak, no tail.
2. **The eutectic arrest is isothermal and its area is maximised at the eutectic composition.** So you scan composition: the eutectic peak area grows as you approach the eutectic and the primary-phase liquidus tail shrinks to nothing. Where the tail vanishes is your eutectic.

**TGA (thermogravimetric analysis)** measures **mass** versus temperature. For reactive metals: mass *gain* means oxidation or nitridation (contamination), mass *loss* means volatilisation or decomposition.

**⚑ STA (simultaneous thermal analysis) = DSC + TGA on the same sample in the same run.** Why that matters, and this is the answer that shows you understand the instrument rather than just operating it:

> "A DSC peak alone is ambiguous — an endotherm could be melting, or it could be a reaction or evaporation. Because STA gives you mass simultaneously on the identical thermal history, you can separate them: a thermal event with **no** mass change is a genuine phase transformation; a thermal event **with** mass change is oxidation or volatilisation, i.e. a contamination artefact. For a reactive alloy system that distinction is the whole ballgame."

**Practical details they may probe:**

- **Heating rate.** Faster ramps shift peaks to higher temperature and broaden them (thermal lag and kinetics). You use slow rates for accurate transition temperatures, faster for sensitivity to weak events. Report the rate.
- **Calibration** against pure-metal melting standards — indium (156.6 °C), tin (231.9 °C), zinc (419.5 °C), aluminium (660.3 °C).
- **Use the heating curve, not cooling, for equilibrium temperatures**, because cooling curves show **supercooling** — the liquid persists below its true freezing point until nucleation happens, so cooling onsets read low and scatter.
- **Crucible choice** matters enormously for reactive metals: alumina, graphite, tungsten, BN — you need one that doesn't react with or wet your alloy, or you've measured the crucible.
- **Inert purge gas** (Ar) throughout, and even then trace O₂ shows up in the TGA trace.

## A3. Microstructure — SEM, EDX, optical ⚑

**SEM.** A focused electron beam is rastered over the sample; detectors collect what comes back.

- **Secondary electrons (SE)** — low energy, escape only from the top few nanometres → **topographic contrast**. Great depth of field, this is your "what does the surface look like" image.
- **Backscattered electrons (BSE)** — elastically scattered, intensity rises with atomic number → **compositional (Z) contrast**. Heavier phases appear brighter. **This is how you tell two phases apart in a eutectic without doing chemistry.**
- Knobs: accelerating voltage (higher = deeper penetration, more signal, more charging risk), working distance, spot size, and conductive coating for non-conductors.

**EDX / EDS.** The beam knocks out inner-shell electrons; refilling emits X-rays at energies characteristic of each element. Gives elemental identification and semi-quantitative composition.

**⚑ Its limitations are what get asked:**

- **Spatial resolution is set by the interaction volume (~1 µm³), not by the image resolution.** So on a fine lamellar eutectic with sub-micron spacing, your "point scan on the α phase" is averaging both phases. Know this — it's the classic trap.
- **Light elements are poor to impossible.** **EDX cannot detect lithium at all** (and H, He are out; Be, B, C are unreliable). If lithium was anywhere in your system, EDX was blind to it and you'd need something else. Volunteering this limitation is a strong credibility signal.
- **Peak overlaps** between elements with nearby line energies.
- Quantification requires standards and ZAF/matrix correction; treat unstandardised numbers as semi-quantitative.

**What you were actually looking for in the microstructure:**

- **Lamellar or rod eutectic morphology** — alternating fine plates or fibres of the two phases, formed by coupled growth. This is the visual fingerprint of a eutectic.
- **Primary dendrites** — tree-like crystals of one phase in a eutectic matrix means you were **off** eutectic; the primary phase grew first out of the liquid. Their presence and volume fraction tells you which side of the eutectic you're on.
- **Interlamellar spacing** scales inversely with the square root of growth rate — faster solidification gives finer eutectic.

**Optical microscopy** is the complement: no vacuum, much larger field of view, fast, and colour/etch contrast. Requires grinding, polishing and etching. For reactive alloys, prep under inert atmosphere or with non-aqueous polishing media, or you oxidise the surface you're trying to image.

## A4. Porous media — porosity and permeability ⚑

**Porosity ε** = void volume / total volume. Critical distinction:

- **Total porosity** includes closed, isolated voids.
- **Open (effective) porosity** is the connected network.

**Only open porosity does anything for you.** A structure can be 40% porous and completely useless as a wick if the pores don't connect.

**⚑ Archimedes' method.** Weigh the sample dry (m_dry), then suspended in a wetting liquid of known density (m_susp). Buoyancy gives you the true solid-plus-closed-pore volume, so:

```
ρ_bulk = m_dry ρ_liquid / (m_dry − m_susp)
ε_total = 1 − ρ_bulk / ρ_theoretical
```

Advantages: no geometry assumption, works on irregular shapes, includes closed porosity. **The limitation, which is the question:** it tells you *how much* void there is, and nothing about whether it's **connected**. Connectivity needs a transport measurement — permeability by flow, or mercury/gas intrusion porosimetry for the pore size distribution. (If you saturate the sample first you can get open porosity by the difference between dry, saturated and suspended masses — worth knowing as the refinement.)

**Permeability k** [units: m², sometimes darcy] is the material's conductance to viscous flow:

```
u = −(k/µ) ∇p                (Darcy's law)
```

`u` here is the **superficial** (Darcy) velocity — flow rate over total cross-section, not over the pore area. Pore velocity = u/ε. Getting that distinction right is a cheap point.

**Darcy is valid at low pore Reynolds number** (roughly Re_p < 1–10). Above that, inertial losses add a quadratic term — the **Forchheimer** correction. Wick flows are deeply Darcy; you're at Re ≪ 1, Stokes flow.

**Kozeny–Carman**, the standard estimate:

```
k ≈ ε³ d² / [180 (1−ε)²]
```

For ε = 0.4 and d = 10 µm this gives k ~ 10⁻¹³ m². **Say "order of magnitude" out loud when you quote it** — it assumes near-spherical, monodisperse particles and a well-connected network, and it degrades badly for broad size distributions, plate-like particles, or low porosity. **Tortuosity** (the ratio of actual path length to straight-line length) is the fudge that absorbs some of this.

**⚑ Sintering and why a real wick has a pore size *distribution*.** Porous tungsten is made by powder metallurgy: press tungsten powder, then partially sinter — heat below full densification so particles bond at contact points but voids remain. Pore size scales with powder size and sintering time/temperature. So there is no single r_c:

> **The largest pores set the capillary pressure limit** (the meniscus breaks through the weakest, biggest pore first, and Δp ∝ 1/r). **The mean pore size sets the permeability** (k ∝ r²). So the ideal wick has a narrow distribution, and a broad distribution gives you the permeability of the mean with the capillary limit of the largest. That's a genuinely good thing to say.

**COMSOL porous media.** Know which physics interface does what:

- **Darcy's Law** interface — for low-velocity flow in porous media, solves pressure with Darcy's relation. What you'd use for a wick.
- **Brinkman equations** — adds viscous shear terms; use when porosity is high or you need to resolve the transition from porous medium to free flow.
- **Free and Porous Media Flow** — couples Navier–Stokes in the open region to Darcy/Brinkman in the porous region.
- If asked how you'd validate: compare a simulated pressure drop against a measured one on a known sample at known flow rate, then check mesh independence.

**Effective thermal conductivity of a porous solid.** Porosity always *reduces* k below the dense value. Rough bounds are the series and parallel limits of solid and pore fluid; Maxwell–Eucken-type models sit between. Filling the pores with liquid metal helps (liquid Li ~45 W/m·K vs gas ~0.03) but doesn't recover dense tungsten (~170 W/m·K). **This is why a porous wick is a thermal penalty you accept in exchange for capillary supply.**

## A5. Glovebox and vacuum operations

**Why inert atmosphere.** Alkali and alkaline-earth metals and many refractory alloys react with O₂, H₂O and (for Li) N₂ at or near room temperature. A glovebox holds O₂ and H₂O at single-digit ppm or below via a purification train — copper catalyst beds to getter oxygen, molecular sieve to trap water, periodically regenerated with H₂/N₂ forming gas. Material enters through an **antechamber** that you pump and backfill several times to avoid dumping air into the main box.

**Why you should care beyond "I followed procedure":** oxygen is the enemy of two separate things. It contaminates your alloy (showing up as a mass gain in TGA and as oxide inclusions in SEM), and **it destroys wetting** — an oxide layer on a metal surface prevents liquid metal from wetting it, and wetting is what capillary action depends on. Oxygen control isn't housekeeping, it's a functional requirement.

**Vacuum basics.**

- Pressure regimes: rough (atm → ~10⁻³ mbar), high (to ~10⁻⁸), ultra-high (below that).
- Pumps: rotary vane or scroll for roughing; **turbomolecular** or diffusion for high vacuum; ion/getter for UHV. Turbos need a backing pump and can't be started at atmosphere.
- **Mean free path** grows as pressure falls; when it exceeds the vessel dimension you're in molecular flow (Knudsen number > 1) and conductance, not pumping speed, limits you.
- What limits your base pressure in practice: **outgassing** from surfaces, **virtual leaks** (trapped volumes like blind bolt holes slowly bleeding out), and real leaks. Found with a helium mass-spectrometer leak detector.
- **Why full-penetration welds** on liquid metal systems, which Zap says explicitly: a partial-penetration weld leaves a crevice that is both a virtual leak and a stress concentrator, and with a metal that reacts with air you cannot tolerate either direction of leakage.

---

# PART B — UCSD: Capillary Evaporation and CHF

## B1. Surface tension and capillarity ⚑

**Surface tension σ** [N/m] exists because a molecule at a liquid surface has fewer neighbours than one in the bulk, so creating surface area costs energy. σ is equivalently energy per unit area [J/m²].

**Young–Laplace equation** — a curved interface sustains a pressure difference:

```
Δp = σ (1/R₁ + 1/R₂)      →   2σ/R for a sphere
```

In a circular capillary of radius r with contact angle θ, the meniscus radius is r/cos θ, so:

```
Δp_cap = 2σ cos θ / r
```

**Contact angle θ** is set by the three interfacial energies (**Young's equation**):

```
σ_sv = σ_sl + σ_lv cos θ
```

θ < 90° wetting, θ > 90° non-wetting, θ → 0° perfect wetting. **Contact angle hysteresis** is real: the advancing angle (liquid moving forward) exceeds the receding angle, because of roughness and chemical heterogeneity. It's why a single "θ" is an idealisation.

**Jurin's law** — capillary rise height, from balancing capillary pressure against hydrostatic head:

```
h = 2σ cos θ / (ρ g r)
```

**Bond number** `Bo = ρgL²/σ` — gravity versus surface tension. Small Bo means capillarity dominates and orientation doesn't matter, which is why fine wicks work upside down.

**⚑ The mechanism you must be able to narrate: how a wick self-regulates.** At low heat flux, the meniscus sits near the wick surface with gentle curvature, generating only the small pressure needed. As flux rises, more liquid must flow, viscous losses grow, so the meniscus curves more sharply to generate more pressure — it recedes into progressively smaller pores. This continues until it reaches the smallest available pore radius. **Beyond that the wick physically cannot generate more pressure, liquid supply falls short of evaporation, dry spots appear, and local temperature runs away. That is capillary-limited CHF.** If you can say that paragraph, you own this project.

## B2. Thin-film evaporation ⚑

**Why thin is the whole point.** Heat must conduct through the liquid before it can evaporate. That conduction resistance is `t/k` — proportional to film thickness. So the thinner the film, the higher the flux at a given superheat. Evaporation is therefore not uniform across a meniscus; it is dramatically concentrated where the film is thinnest.

**Three regions of an extended meniscus**, going from dry solid toward bulk liquid:

1. **Adsorbed (non-evaporating) film** — a few nanometres thick, held to the solid so strongly by **disjoining pressure** (van der Waals attraction to the substrate) that its effective saturation pressure is suppressed and it cannot evaporate at all.
2. **Thin-film / transition region** — thin enough for very low thermal resistance, but thick enough that disjoining pressure no longer suppresses evaporation. **The vast majority of the evaporative heat transfer happens in this narrow band.** Maximising its total length is what wick and surface design is really trying to do.
3. **Intrinsic meniscus** — bulk curvature, thick, high thermal resistance, contributes comparatively little.

**Heat transfer coefficient** `h = q″/ΔT`. Context for your own numbers: the UCSD group's published glass-fibre membrane work reports roughly 486 W/cm² at ΔT ≈ 7 °C — that's h of order 10⁶ W/m²·K, one to two orders above ordinary convective boiling. **That extraordinary h is the reason this field exists**, and it comes entirely from making the conduction path through the liquid as short as possible.

**Interfacial resistance.** Even with zero conduction resistance, evaporation is rate-limited at the interface itself. **Hertz–Knudsen / Schrage** relations give the net mass flux from the difference between saturation pressure at the liquid temperature and the actual vapour pressure. At extreme fluxes this becomes non-negligible. You don't need the constants — you need to know the resistance exists and that it, plus vapour-side pressure drop, is the ultimate ceiling once you've made the film thin enough.

## B3. CHF and the limits ⚑

**⚑ The distinction to have ready: capillary dryout is NOT the same mechanism as pool boiling CHF.** Same acronym, different physics, and panels test this.

- **Wick / capillary-limited dryout** — a **liquid supply** failure. The capillary pressure budget is exceeded, the meniscus recedes past the smallest pore, liquid stops arriving. Fixed by wick design.
- **Pool boiling CHF** — a **vapour removal** failure. Vapour generation is so vigorous that a vapour blanket forms and blocks liquid from reaching the surface (hydrodynamic instability of the vapour columns). Fixed by surface and geometry.

**The capillary pressure budget** — the design inequality:

```
Δp_cap,max  ≥  Δp_liquid + Δp_vapour + Δp_gravity
```
with `Δp_liquid` from Darcy, `Δp_vapour` from flow of vapour away, and gravity depending on orientation.

**⚑ The five classical heat-pipe limits.** Naming all five is a strong, cheap signal:

1. **Capillary limit** — wick can't supply the liquid. Usually the binding one.
2. **Boiling limit** — nucleation *inside* the wick blocks the liquid path with vapour.
3. **Entrainment limit** — high-velocity counterflowing vapour shears liquid off the wick surface and carries it back.
4. **Sonic limit** — vapour flow chokes at Mach 1 in the vapour core. Matters at startup and for liquid metals.
5. **Viscous limit** — at very low temperature the vapour pressure is so low that viscous forces in the vapour dominate and flow barely happens.

**How you actually detected incipient dryout in the lab** — this is your experimental answer:

- Departure from the previously linear `q″` vs `ΔT` trend.
- A temperature excursion at **fixed** power — the surface climbs with no change in input.
- Hysteresis on power-down: it doesn't recover along the same curve, because rewetting requires re-establishing the meniscus.

## B4. The wick materials, and why those three

Your résumé lists AAO, glass fibre and hydrogels. The reason to test all three is that they sit at different points of the same trade.

**The trade-off, stated cleanly:** capillary pressure scales as `1/r`, permeability as `r²`. Small pores give you pressure and cost you flow. There is an optimum, and the figure of merit for a wick is roughly `k/r_eff` (permeability per unit pore radius) — you want maximum flow per unit capillary pressure sacrificed.

- **AAO (anodic aluminium oxide)** — made by anodising aluminium in acid, which self-organises into a hexagonal array of straight, parallel, near-identical cylindrical pores. **Very tightly controlled r**, so it's the ideal model system for testing Young–Laplace quantitatively. But straight non-interconnected pores and modest porosity mean low permeability, so it dries out early despite high capillary pressure.
- **Glass fibre membranes** — a random interconnected fibrous network. **High permeability and pore interconnection**, so liquid can redistribute laterally to feed a locally starved spot. The cost is a broad pore size distribution, so the capillary limit is set by the largest pores. This is why interconnected fibre membranes win on flux — and it's the geometry that hit ~486 W/cm² in the group's published work.
- **Hydrogels** — a swollen crosslinked polymer network holding water within the polymer matrix. Transport is through a soft, deformable, partly diffusive medium rather than rigid pores — a different regime, and interesting for how much water can be held and released.

**⚑ The design lesson, which is the real answer to "what did you learn":** **pore interconnection matters more than pore size.** A network that lets liquid redistribute laterally tolerates local hot spots; an array of isolated straight pores can only feed each point from directly below. That insight transfers directly to sintered porous tungsten, where connectivity is exactly what Archimedes' method fails to measure.

## B5. Instrumentation, DAQ, and the troubleshooting story ⚑

**How you know your heat flux.** Typically a cartridge heater on a known area driven by a DC supply: `q″ = VI/A`. Every error in that expression is an error in your headline number:

- **Area** — is it the heater footprint, the wetted area, or the projected area? This is exactly your **600 W vs 600 W/cm²** problem. Nail it down.
- **Parasitic losses** — heat that leaves through insulation, leads and fixturing never reached the sample, so your reported flux is high. Guard heaters and insulation exist to make `VI` a true measure of the flux into the sample. Any credible CHF claim needs a heat-loss accounting.
- **Temperature** — thermocouples are typically ±1–2 K (type K, or type T for better low-temperature accuracy), require **cold junction compensation**, and read the *thermocouple bead*, not the surface. Extrapolating from embedded TCs to a surface temperature introduces its own error. RTDs are more accurate but slower and more fragile.

**⚑ Four-wire vs two-wire resistance measurement — learn this, because it's very likely the physics behind your multimeter story.** A two-wire measurement puts the lead and contact resistance in series with what you're trying to measure. A four-wire (Kelvin) measurement forces current through one pair and senses voltage through a separate pair carrying essentially no current, so lead resistance drops out. For low resistances — heaters, RTDs, shunts — two-wire can be wrong by a lot, and the error drifts with temperature and connector condition, so it *looks like* physics.

**⚑ Your troubleshooting story, structured.** The version of this story that impresses is the one where you distinguish an **instrumentation artefact** from a **real physical effect**:

> "I had CHF values that weren't reproducing between runs. The tempting conclusion is sample-to-sample variation in the wick. Before accepting that, I checked the measurement chain — and found the multimeter reading was the problem, not the sample. Once that was corrected the scatter collapsed. The lesson I took is to suspect the instrument before you believe a physical result, especially when the result is the one you were hoping for."

Fill in the real specifics from memory. Also have the **water transport inconsistency** version — degassing (dissolved air coming out of solution and blocking pores), inadequate priming/wetting of the wick, or an unstable reservoir level are the usual culprits, and every one of them mimics a real capillary limit.

**Uncertainty propagation.** For `q″ = VI/A`, relative uncertainties add in quadrature: `(δq/q)² = (δV/V)² + (δI/I)² + (δA/A)²`. Area is usually the dominant term, and it's the one people forget to quote. Saying that unprompted is a mark of an experimentalist.

---

# PART C — UIUC: Boiling, Falling Films, and Fouling

## C1. Pool boiling ⚑

**The boiling curve.** Wall heat flux `q″` (y-axis) versus **wall superheat** `ΔT = T_wall − T_sat` (x-axis). Five regimes, in order:

1. **Natural convection** — below the onset of nucleate boiling, no bubbles; heat moves by buoyant convection.
2. **Onset of nucleate boiling (ONB)** — the first bubbles appear at the most favourable cavities.
3. **Nucleate boiling** — the useful regime. Steeply rising `q″` with small ΔT because bubble growth and departure violently stir the boundary layer. This is where you want to operate.
4. **Critical heat flux (CHF)** — the peak. Vapour generation becomes so intense that vapour blankets the surface and liquid can no longer reach it.
5. **Transition boiling** (unstable, negative slope) then the **Leidenfrost minimum**, then **film boiling** — a stable vapour film, so heat transfer collapses and wall temperature soars.

**⚑ Why CHF is a safety limit, not just a performance number.** If you control **heat flux** (an electrical heater, a nuclear fuel rod) and you cross CHF, there is no stable operating point until film boiling — so wall temperature jumps by hundreds of degrees essentially instantly and the surface fails. That's *burnout*. If you control **wall temperature** instead you can traverse transition boiling stably. Same curve, completely different consequence.

**Nucleation physics.** A bubble of radius `r` must overcome its own surface tension, so it needs a minimum superheat:

```
ΔT_sat = 2 σ T_sat / (ρ_v h_fg r)
```

**Small cavities require large superheat; large cavities activate first and at low superheat.** So the **cavity size distribution on the surface controls ONB and the active nucleation site density** — which is precisely why you were testing samples with different micron-scale groove densities. Grooves are engineered cavities: they let you set nucleation site density deliberately instead of relying on whatever roughness the machining left.

**The three parameters that set nucleate boiling performance:** active **nucleation site density**, bubble **departure diameter**, and departure **frequency**. Heat transfer scales with their product — sites × volume per bubble × bubbles per second. Your groove-density study was a controlled experiment on the first one.

**⚑ The wettability trade, which is counterintuitive and gets asked:**

- **Hydrophobic** surfaces nucleate more easily — vapour is happy to sit on them — so ONB happens at lower superheat and low-flux performance improves. But that same reluctance to be wetted means the vapour doesn't clear, so bubbles merge into a blanket sooner and **CHF is lower**.
- **Hydrophilic** surfaces resist nucleation (higher ONB superheat) but **rewet aggressively**, pushing liquid back to the wall and delaying the blanket, so **CHF is higher**.
- Hence mixed-wettability and biphilic surfaces: hydrophobic islands for nucleation on a hydrophilic background for rewetting. Best of both. **Note this is a direct cousin of your falling-film patterned-wettability work — same idea, different objective.**

**Correlations, for naming only:** **Rohsenow** for nucleate boiling flux (with a surface-fluid empirical constant, which is the tell that boiling is surface-dependent); **Zuber** for CHF, `q_CHF ≈ 0.131 ρ_v h_fg [σ g (ρ_l − ρ_v)/ρ_v²]^(1/4)`, derived from hydrodynamic instability of the vapour columns.

**Your rig:** automated test system with DAQ, closed-loop heater control, and **high-speed imaging** so you can count sites, measure departure diameter and frequency directly, and correlate the optical record with the thermal data rather than inferring bubble behaviour from the boiling curve alone.

## C2. Falling-film evaporation ⚑

**The concept.** Liquid is distributed over the outside of a horizontal tube (or down a vertical surface) and flows as a thin film under gravity while being heated. Because the film is thin, the conduction resistance across it is small, so you get high `h` at very small ΔT — with a small liquid inventory. That's why it's the workhorse of **multi-effect distillation desalination** and of refrigeration evaporators.

**Nusselt falling-film theory** — the classic result. For a laminar film with mass flow per unit width Γ:

```
δ = (3 µ Γ / ρ² g)^(1/3)          h ≈ k / δ
```

So film thickness grows only as the cube root of flow rate, and `h` falls as flow rises. **The film Reynolds number** is conventionally `Re = 4Γ/µ`, and the regimes are smooth laminar → **wavy laminar** → turbulent. Real films are almost always wavy, and the waves *enhance* heat transfer above Nusselt theory by thinning the film in the troughs and mixing it.

**⚑ Why you were doing wave-velocity analysis.** Interfacial wave speed and frequency tell you the film's hydrodynamic state — flow distribution, liquid retention, and mixing — which is what actually sets local heat transfer and local film thinning. Measuring waves optically is how you get at film behaviour without inserting a probe that would disturb it.

**Intertube flow modes** on horizontal tube bundles, as flow rate rises: **droplet → jet (column) → sheet**. Which mode you're in controls how uniformly the next tube down gets wetted, and therefore whether it has dry patches.

**⚑ Dry patch formation and the minimum wetting rate.** Below a critical flow rate the film breaks up and dry patches form, held open by the balance of surface tension at the dry-patch rim against the inertia and hydrostatic force of the flow trying to close it. **This is the falling-film analogue of capillary dryout and pool-boiling CHF: a liquid supply failure exposing hot surface.** Dry patches are also where scale nucleates fastest, because the local solution concentrates as it evaporates. Connecting dry-patch formation to fouling is a genuinely good insight to have.

## C3. Crystallisation fouling ⚑

**⚑ The one counterintuitive fact.** CaCO₃ and CaSO₄ have **inverse (retrograde) solubility** — they become *less* soluble as temperature rises. So they precipitate preferentially on the **hottest surface**, which is exactly the heat transfer surface you were trying to keep clean. That's why scaling is a heat exchanger problem specifically and not just a plumbing problem.

**The chemistry:**

```
Ca²⁺ + 2HCO₃⁻  →  CaCO₃(s) + CO₂ + H₂O
```

Heating drives off CO₂, which shifts the carbonate equilibrium and drives precipitation right at the hot wall. Polymorphs: **calcite** (rhombohedral, thermodynamically stable — the dense layer you imaged), **aragonite** (needle-like, favoured at higher temperature), **vaterite** (metastable). Being able to name the morphology you saw and identify it as calcite is a nice specific.

**The fouling curve** — deposit thickness or fouling resistance versus time:

1. **Induction period** — nucleation is happening but there's no measurable deposit yet. Surface properties dominate here, which is exactly the lever your patterning was pulling.
2. **Growth** — linear, falling-rate, or asymptotic, depending on whether removal (shear, spalling) keeps pace with deposition.

Net rate = deposition − removal. Both terms are engineerable.

**Fouling resistance** is how it's quantified:

```
R_f = 1/U_fouled − 1/U_clean
```

Scale is a conduction resistance in series with everything else. Because CaCO₃ conductivity is low (order 1–3 W/m·K, roughly like glass), a very thin layer destroys `U`. That's the mechanism behind the 20–30% efficiency loss figure on your résumé.

**⚑ Why patterned wettability works** — the mechanism, and be careful to give the mechanism, not just the result:

- Heterogeneous nucleation is favoured where the surface energy is high and the liquid is in intimate contact. **Hydrophilic regions offer many favourable nucleation sites; hydrophobic regions offer few.**
- Adhesion also differs: the **work of adhesion** of a deposit to a low-energy hydrophobic surface is lower, so whatever does deposit is more easily removed by shear.
- **So the crystals go where you told them to go.** You've confined scale to defined sacrificial zones and left the rest clean — moving from "prevent all fouling" (impossible) to "control where fouling happens" (achievable).

**⚑ Your headline result and its mechanism.** A **1.6 mm** hydrophobic band stayed clean; a **0.8 mm** band was **bridged** and mineralised anyway. Mechanism: the liquid film maintains continuity across a sufficiently narrow non-wetting stripe — the film simply spans it rather than dewetting — so ions are transported across and deposition proceeds. **There is a threshold stripe width, set by the film's ability to bridge, below which the pattern stops working.**

**The design lesson, and it's a strong one to state:** **geometry mattered as much as surface chemistry.** You can have the right surface chemistry and still lose the benefit entirely by getting the feature size wrong. That's a transferable engineering conclusion, not a lab curiosity — and it's the same conclusion as "pore interconnection matters more than pore size" from UCSD. **You have found the same lesson twice in two different systems. Say so.**

## C4. Image processing and CFD

**OpenCV pipeline** — the operations behind "image processing and wave-velocity analysis":

- **Calibration** — pixels to millimetres from a known reference in frame. Everything quantitative depends on this.
- **Preprocessing** — greyscale, blur to suppress noise, contrast normalisation.
- **Thresholding / edge detection** (Canny) to find the liquid interface or the deposit boundary.
- **Background subtraction / frame differencing** to isolate what moved.
- **Contour detection** for areas, coverage fractions, and fouling-layer growth over time.
- **Wave velocity** — the clean way is a **space–time (x–t) diagram**: take a single line of pixels across the flow, stack it for every frame, and the waves appear as diagonal streaks whose slope *is* the velocity. Alternatively cross-correlate the signals from two positions and use the time lag. Mentioning the x–t method specifically sounds like someone who did it rather than read about it.

**Pandas** for the resulting time series, and for joining the optical data to the thermal DAQ record on timestamps.

**High-speed imaging trade-offs** — frame rate versus exposure versus resolution versus light. Short exposures freeze motion but need intense illumination; backlighting gives crisp interface silhouettes while diffuse front lighting shows surface texture. Insufficient light is the usual reason high-speed footage is unusable.

**⚑ CFD: verification versus validation.** This distinction gets asked and most candidates fumble it.

- **Verification** — "am I solving the equations correctly?" Grid refinement / mesh independence, time-step independence, comparison to analytical solutions, checking conservation. Purely internal to the simulation.
- **Validation** — "am I solving the correct equations?" Comparison against **experiment**. This is what you were doing: providing the experimental data the model was measured against.

Also worth knowing for a falling-film or boiling model: **VOF (volume of fluid)** is the standard method for tracking a sharp liquid–vapour interface; it advects a phase fraction field and reconstructs the interface. Interface-resolving simulations are mesh-hungry, which is why experimental validation matters so much.

---

# PART D — Personal: Transient 2D Conduction Solver

## D1. The equation and the discretisation ⚑

**The heat equation**, 2D, no generation:

```
∂T/∂t = α (∂²T/∂x² + ∂²T/∂y²)          α = k/(ρ c_p)
```

`α` is **thermal diffusivity** [m²/s] — how fast a temperature disturbance propagates, as opposed to `k`, which is how much steady heat flows. A material can have high `k` and low `α` if it also has high heat capacity.

**FTCS = Forward Time, Centred Space.** Forward Euler in time (first-order accurate), central differences in space (second-order accurate). On a uniform grid with Δx = Δy, the explicit update is:

```
T_ij^(n+1) = T_ij^n + Fo (T_E + T_W + T_N + T_S − 4 T_ij^n)
```

with the **Fourier number** `Fo = α Δt / Δx²` as the single dimensionless parameter. It's the same Fo as in transient conduction generally — dimensionless time — which is a nice unifying observation.

## D2. Stability ⚑

Rewrite the update grouping the centre node:

```
T_ij^(n+1) = Fo (T_E + T_W + T_N + T_S) + (1 − 4Fo) T_ij^n
```

**⚑ The physical stability argument, which is more impressive than quoting the number:** if the coefficient on the centre node `(1 − 4Fo)` goes negative, then a node being *hotter* now makes it *colder* next step — a physically absurd inversion that amplifies each step and produces oscillating, exploding garbage. Requiring it non-negative gives:

```
2D:  Fo ≤ 1/4          1D:  Fo ≤ 1/2
```

(The rigorous route is von Neumann analysis — substitute a Fourier mode and require the amplification factor's magnitude ≤ 1. Same answer. Mention it exists; use the coefficient-sign argument to explain it.)

**⚑ The convective boundary node is stricter.** Doing an energy balance on the half-control-volume at a surface with convection introduces the grid Biot number `Bi_Δx = h Δx / k`, and stability requires:

```
Fo (1 + Bi_Δx) ≤ 1/2        (1D surface node)
```

Because the surface node exchanges with both its neighbour and the fluid, it has a shorter effective time constant. **So the convective boundary, not the interior, is what limits your time step.** Knowing that the boundary condition sets the stability limit is the mark of someone who actually wrote the code.

## D3. Boundary conditions ⚑

| Type | Physical meaning | Math |
|---|---|---|
| **Dirichlet** (1st kind) | Fixed temperature | `T = T_s` |
| **Neumann** (2nd kind) | Fixed flux; `q″ = 0` is insulated / a symmetry plane | `−k ∂T/∂n = q″` |
| **Robin** (3rd kind) | Convection to a fluid | `−k ∂T/∂n = h (T_s − T_∞)` |

Your solver used Dirichlet on three sides and Robin on the fourth — a constant-temperature source embedded in the domain, cooled convectively on one boundary.

**Two ways to implement a flux or convective BC:**

- **Ghost node** — invent a node outside the domain whose value enforces the derivative condition, then use the standard interior stencil. Clean, keeps second-order accuracy.
- **Energy balance on a half control volume** — write conservation directly for the boundary cell. More physical, easier to get right, and it's the route that naturally produces the `Fo(1+Bi)` stability condition.

**Biot number** `Bi = hL/k` (the *physical* one, using the body's characteristic length, not Δx): internal conduction resistance versus external convection resistance. `Bi ≪ 1` means the body is nearly isothermal and lumped capacitance is valid — no need for a spatial solver at all. Worth knowing when your solver is overkill.

## D4. Alternatives and verification

**Explicit vs implicit.** Explicit is trivial to code, needs no linear solve, and is conditionally stable — the time step is capped regardless of what accuracy you need. **Implicit (backward Euler)** is unconditionally stable so you can take large steps, at the cost of solving a sparse linear system each step. **Crank–Nicolson** averages the two, giving second-order accuracy in time and unconditional stability, though it can oscillate on sharp transients. **ADI (alternating direction implicit)** was the classic way to get implicit stability in 2D while only ever solving tridiagonal systems.

**⚑ How you'd verify it — the question that follows "I wrote a solver."** Three things, and give all three:

1. **Compare to an analytical solution.** A semi-infinite solid with a step surface temperature has the exact `erfc` solution; a 1D slab has a known series solution. Run your code in that limit and check it reproduces them.
2. **Grid and time-step refinement.** Halve Δx and Δt; the solution should converge, and the error should shrink at the expected order (second in space, first in time for FTCS).
3. **Energy conservation.** Sum the energy in through the boundaries over time and check it against the change in stored energy `∫ρc_pT dV`. A bug in a boundary condition shows up here immediately and nowhere else.

**Vectorisation.** The NumPy version replaces nested Python loops over i and j with array slicing — `T[1:-1,1:-1] + Fo*(T[2:,1:-1] + T[:-2,1:-1] + T[1:-1,2:] + T[1:-1,:-2] - 4*T[1:-1,1:-1])`. Same arithmetic, executed in compiled code instead of the interpreter, typically one to two orders of magnitude faster. **Important detail:** you must compute the new field from the old one, so you need a separate output array (or a copy) — updating in place silently mixes time levels and gives you a different, wrong scheme.

---

# PART E — Cross-Cutting

## E1. Dimensionless numbers, all in one place ⚑

| Number | Definition | Ratio of | Where it showed up for you |
|---|---|---|---|
| Reynolds | ρuL/µ | inertia / viscous | falling films, wick flow (Re ≪ 1) |
| Prandtl | ν/α | momentum / thermal diffusivity | ~7 water, ~0.7 air, ~0.01 liquid metals |
| Nusselt | hL/k | convective / conductive | every heat transfer result you have |
| Péclet | Re·Pr | advection / diffusion | the relevant one for liquid metals |
| Biot | hL/k | internal / external resistance | your Robin boundary |
| Fourier | αt/L² | dimensionless time | your solver's stability parameter |
| Bond | ρgL²/σ | gravity / surface tension | why fine wicks beat gravity |
| Capillary | µu/σ | viscous / surface tension | meniscus dynamics under flow |
| Weber | ρu²L/σ | inertia / surface tension | droplet break-up, splashing |
| Marangoni | (dσ/dT)ΔT L/(µα) | thermocapillary / viscous | thin-film flow toward cold regions |
| Hartmann | BL√(σ_e/µ) | Lorentz / viscous | liquid metal MHD |

**⚑ Two you should be ready to volunteer as "what changes with liquid metals":**

- **Prandtl ~0.01 instead of ~7.** The thermal boundary layer becomes far *thicker* than the momentum boundary layer, so conduction competes with advection everywhere and ordinary Nusselt correlations don't apply. You use a liquid-metal correlation of the **Lyon–Martinelli** form, `Nu ≈ 7 + 0.025 Pe^0.8`, where Nu depends on Péclet rather than separately on Re and Pr. **This is directly relevant to sodium and lithium loops.**
- **Marangoni / thermocapillary flow.** σ falls with temperature, so surface tension gradients drag liquid **from hot toward cold** — meaning the hottest spot is where a thin film *thins further*. Exactly the wrong direction. A real thin-film mechanism and worth naming.

## E2. Numbers to have on the tip of your tongue

- Water σ ≈ 0.072 N/m; liquid Li σ ≈ 0.40 N/m (**~5× water, ~50× ammonia**); Li h_fg ≈ 21 MJ/kg; water h_fg ≈ 2.26 MJ/kg
- Li melts at 180.5 °C; Na at 97.8 °C; Bi at 271 °C; W at ~3,422 °C
- k: W ~170, liquid Li ~45, stainless ~15, CaCO₃ ~1–3, water ~0.6, air ~0.03 W/m·K
- Your CHF: 600 W/cm² = **6 MW/m²** — same order as divertor steady-state heat flux. **Good comparison to make.**
- Pure water pool boiling CHF on a flat plate at 1 atm ≈ 100–130 W/cm². **Your wick number is ~5× that**, which is the point of the whole field.
- Explicit FD stability: Fo ≤ 1/4 (2D), 1/2 (1D), Fo(1+Bi_Δx) ≤ 1/2 at a convective node

## E3. Things not to overclaim

Be precise about your role. "I ran the experiments and did the analysis" is different from "I designed the rig," and different again from "I assisted with CFD validation" — which your résumé accurately says, and which means you supplied and analysed the experimental data, not that you built the model. **Panels respect the person who draws that line themselves and get suspicious of the person who doesn't.**

Same for the thermodynamic modelling and the COMSOL work: know whether you built the model or ran an existing one, and say which.

## E4. The four sentences that tie it all together

Learn these. They're the answer to "walk us through your background" and to "why are you a fit."

1. "Every project I've done is a version of one problem: keeping a liquid supplied to a hot surface, and understanding what happens when the supply fails — CHF in wicks, dry patches in falling films, dryout in a capillary structure."
2. "The framework has been the same every time — Young–Laplace for the driving pressure, Darcy for the resistance, and a mass balance to find the limit — and the fluid and substrate are what changed."
3. "Twice now, in two unrelated systems, I've found that the geometry mattered as much as the chemistry: interconnection beat pore size in wicks, and stripe width beat surface treatment in fouling."
4. "The eutectic work is the piece I'd most want to pick back up, because the melting point of the loop fluid is what sets the freeze-protection requirement on every pipe and valve in the system."
