# Tomorrowhood

**Where to live in 2035, not 2025.**
A neighbourhood-level, climate-aware recommendation platform for Asia-Pacific. It ranks areas by where they are *heading*, not just how they look today, and shows its forecasts with honest uncertainty.

> *Tomorrowhood is a working title (tomorrow + neighbourhood). A quick search found no obvious conflicts, but check domain, GitHub handle and trademark before committing.*

---

## Summary

Choosing where to live is a long-term investment, yet most tools rank countries or cities by today's conditions. People rarely regret the country; they regret the **neighbourhood**. And almost nobody weighs **climate, sustainability and geopolitics**, although these decide how a place will feel in ten years.

Tomorrowhood takes a short profile (budget, work, priorities, environment, time horizon, risk tolerance) and returns a **mixed shortlist of neighbourhoods across nine Asia-Pacific cities**. Each area is scored on forecast trajectories and stress-tested against several possible futures. Users refine the list with a feedback loop ("remove this city", "I need a park within ten minutes") and see every score with its source and confidence.

**Cities (v1):** Tokyo, Osaka, Seoul, Taipei, Singapore, Hong Kong, Kuala Lumpur, Bangkok, Ho Chi Minh City.

---

## The problem

- Rankings hide huge within-city differences; two districts in the same city can be worlds apart.
- Climate hazards (heat, floods, typhoons, subsidence, earthquakes), sustainability and geopolitical exposure are rarely part of the decision, and where they are, they appear as a snapshot or a single score.
- Existing "AI relocation advisors" are mostly city-level, with undisclosed data and no stated forecasting. Property-level climate-risk tools exist, but mainly for the US.
- Most people have no way to compare a Tokyo ward with a Seoul district against their own priorities.

---

## What it does

1. **Short profile first, depth later.** A five-minute core profile gives a first shortlist immediately. Optional modules (personality, interests, values, household, finances, future worldview) refine it, each showing what it changes.
2. **Forward-looking scores.** 3–10 year trajectories per dimension, with uncertainty bands, not only today's values.
3. **Scenario stress tests.** Shortlists are checked under climate, policy, economic and geopolitical scenarios; the **regret view** shows which areas stay good in all of them.
4. **Hard floors.** Safety, cleanliness, aesthetics and traffic are minimum thresholds, not weights. Areas below them are excluded, and the app says why.
5. **Feedback loop.** Quick critiques re-rank instantly with a "what changed" diff and learn the user's preferences.
6. **Glass-box scoring.** Every number expands to its data source and confidence; data richness is shown as confidence, never as quality.
7. **Decision tools.** Side-by-side comparison, sensitivity notes ("this flips if you weigh safety 20% more"), a net-worth and cost simulation, and a scouting plan for visiting the top areas.

---

## Five pillars

| Pillar | What it covers |
|---|---|
| **Future investment** | 3–10 year trajectories; livability and financial trends kept separate |
| **Climate resilience** | Heat, flood, typhoon, sea level, subsidence, seismic risk; adaptation capacity; insurability |
| **Sustainability** | Transit, air-quality trend, green space, energy mix, walkability, personal carbon footprint |
| **Geopolitical exposure** | Stability, conflict proximity, energy and food dependence, policy risk; shown as flags and stress tests, never predictions |
| **Personal fit** | A user-weighted utility under constraints, with regret minimisation across futures |

---

## How it works (technical)

**Pipeline:** open data sources → standardised H3 hexagonal-grid features → trajectory models with uncertainty → scenario engine → user-weighted, floor-filtered ranking → regret-minimising shortlist → critique loop.

**Layers:** country (policy and eligibility, geopolitics) → city (economy, macro and climate context) → neighbourhood (all dimensions and trajectories).

**Planned stack**
- **Web:** Next.js, TypeScript, Tailwind CSS, Auth.js, Prisma with PostgreSQL/PostGIS, MapLibre GL, Recharts
- **ML and data service:** Python, FastAPI, GeoPandas, H3, OpenStreetMap, GTFS ingestion, an open-source routing engine, scikit-learn and gradient boosting, conformal prediction for uncertainty, statsmodels
- **Ops:** Docker, GitHub Actions CI, tests (unit and end to end)

**Data:** national transaction and statistics portals, OpenStreetMap, GHSL and WorldPop, Sentinel and VIIRS satellite data, Overture, Mapillary, transit feeds, and published climate-scenario datasets. A **data-licence register** records the licence and commercial-use terms of every source.

---

## Evaluation (the credibility core)

- **Temporal backtests:** train on the past, predict the future; no random splits for forward-looking targets.
- **Per-dimension backtests** against each dimension's own history (population, built-up growth, air quality, transit access, flood events).
- **Leave-one-city-out validation** (for example train on Tokyo, predict Osaka), with domain shift reported openly.
- **Ablation and rank stability** using only globally uniform features versus the full set.
- **Calibration** of every uncertainty interval, with failures reported.
- **User study** (20–30 people): do the deeper questionnaires improve perceived fit?

---

## Honest limits and ethics

- Covers the **measurable half** of the decision. Community, language and personal ties are only partly visible to data.
- Geopolitics is the weakest-forecastable pillar; it is shown as exposure flags and scenarios.
- No ethnicity or demographic-composition features; displacement and gentrification risk are shown openly.
- Perception and aesthetic scores are experimental and flagged as culturally biased.
- Sensitive profile data (personality, finances) is consented, minimised and deletable.
- Not legal, immigration, financial or insurance advice.

---

## Roadmap (summary)

| Stage | Focus |
|---|---|
| **MVP** | Accounts, short profile, 4 strong-data cities, a few dimensions plus climate hazards, one real backtest, map UI, critique loop |
| **v1** | All nine cities, scenario engine, questionnaires, regret view, scouting plan, street-view indicators |
| **v2** | Community matching, monitoring alerts, nature and remote-destination mode, more regions |

The full plan, decisions and open items are in the master roadmap.

---

## Status

Planning. Earlier work in this repository family (a badminton pose-analysis prototype) is parked and documented as a research prototype.

---

## Resume blurbs

**One line:** Built a climate-aware, forward-looking neighbourhood recommender across nine Asia-Pacific cities, with temporal backtests, calibrated uncertainty and scenario stress tests.

**Three lines:**
- Designed a pipeline that turns open geospatial, transit, statistics and climate-scenario data into 3–10 year neighbourhood trajectories on an H3 grid.
- Validated with temporal backtests and leave-one-city-out transfer tests, reporting calibration and failure cases openly.
- Shipped a map-based web app with personalised shortlists, regret-minimising rankings and a feedback loop.

*(Fill in the real numbers and results once built; do not publish these claims before the evaluation exists.)*

---

## GitHub repository text

**Repository name (suggestion):** `tomorrowhood`

**Description (268 characters, limit 350):**
Climate-aware, forward-looking neighbourhood recommender for Asia-Pacific. Ranks areas across 9 cities by where they're heading (2035, not 2025): climate hazards, sustainability, geopolitical exposure and personal fit, with backtested forecasts and honest uncertainty.

**Shorter alternative (151 characters):**
Where to live in 2035, not 2025: neighbourhood-level, climate-aware recommendations for Asia-Pacific, with backtested forecasts and honest uncertainty.

**Suggested topics:** `machine-learning`, `geospatial`, `time-series-forecasting`, `climate-risk`, `urban-analytics`, `recommender-system`, `nextjs`, `fastapi`, `h3`, `openstreetmap`, `relocation`, `sustainability`

**Website field:** leave empty until a stable demo is deployed.