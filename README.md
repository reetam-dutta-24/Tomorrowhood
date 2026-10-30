# Tomorrowhood

**Where to live in 2035, not 2026.**

A forward-looking, neighbourhood-level relocation advisor for ten of the world's most cosmopolitan, immigrant-receiving cities. It ranks areas by where they are *heading*, not just how they look today, stress-tests them against climate, policy and geopolitical scenarios, and shows every forecast with honest uncertainty.

> **Status: early development (Phase 0, data foundation).** Nothing here is a finished product yet. The plan, decisions and progress are public in this repository.

---

## Why this exists

Choosing where to live is a long-term investment, yet most tools rank countries or cities by today's conditions. People rarely regret the country; they regret the **neighbourhood**. And almost nobody weighs **climate, sustainability and geopolitics**, even though these decide how a place will feel in ten years.

Tomorrowhood takes a short profile (budget, work, priorities, environment, time horizon, risk tolerance) and returns a mixed shortlist of neighbourhoods across cities, refined by a feedback loop ("remove this city", "I need a park within ten minutes"). Every score expands to its data source and confidence.

## Cities (v1)

Tokyo · Singapore · Seoul · Melbourne · London · New York City · San Francisco · Paris · Berlin · Toronto

The pipeline is built on **London, New York City, Tokyo and Singapore** first. Berlin and Toronto come last because their open housing data is limited, which makes them a useful test of how the system behaves with less data.

## Five pillars

| Pillar | What it covers |
|---|---|
| **Future investment** | 3 to 10 year trajectories; livability and financial trends kept separate |
| **Climate resilience** | Heat, flood, storm, wildfire, sea level, seismic risk; adaptation capacity |
| **Sustainability** | Transit, air quality trend, green space, walkability, personal carbon footprint |
| **Geopolitical exposure** | Stability, policy and immigration-rule risk; shown as flags and stress tests, never predictions |
| **Personal fit** | A user-weighted utility under hard constraints, with regret minimisation across futures |

## What it will do

- **Short profile first, depth later.** A five-minute core profile gives a first shortlist; optional modules (career, language, family, finances, community) refine it.
- **Forward-looking scores** with uncertainty bands, not only today's values.
- **Scenario stress tests and a regret view:** which areas stay good across several possible futures.
- **Hard floors** for safety (including an opt-in women's-safety floor), noise, air quality and hazards. Areas below a floor are excluded, and the app says why.
- **Neighbourhood twin finder:** name an area you know, and get the closest matches in other cities.
- **Immigration pathway planner:** route cards (study, skilled work, startup, remote work) with official sources and "last verified" dates. Not legal advice.
- **Arrival tools:** a landing-area recommendation for the first weeks, airport access, and a first-year cost estimate.
- **Glass-box scoring:** every number links to its source, licence and confidence. Data richness is shown as confidence, never as quality.

The full list, grouped and prioritised, is in the [feature catalog](docs/feature-catalog.md). Decisions and rejected ideas are in the [feature log](FEATURE-LOG.md).

## How it works

```
open data → H3 hexagonal-grid feature tables → trajectory models with uncertainty
→ scenario engine → user-weighted, floor-filtered ranking
→ regret-minimising shortlist → critique loop
```

Layers: **country** (policy, eligibility, geopolitics) → **city** (economy, climate context) → **neighbourhood** (all dimensions and trajectories).

**Planned stack** (subject to change as phases complete)
- **Data and ML:** Python, pandas, GeoPandas, H3, DuckDB and Parquet, scikit-learn, LightGBM, statsmodels, conformal prediction for uncertainty
- **Service:** FastAPI for ranking and scenarios
- **Web:** Next.js, TypeScript, Tailwind CSS, Auth.js, PostgreSQL with PostGIS, MapLibre GL
- **Ops:** GitHub Actions CI, tests

Deep learning (for example street-imagery models) is deliberately deferred to v2.

## Evaluation (the credibility core)

- **Temporal backtests:** train on the past, predict the future; no random splits for forward-looking targets.
- **Leave-one-city-out validation** (for example London → Paris, Tokyo → Seoul), with domain shift reported openly.
- **Ablations and rank stability** across feature sets.
- **Calibration** of every uncertainty interval, with failures reported.
- **User study** (20 to 30 people) on whether deeper questionnaires improve perceived fit.

## Progress so far

**Phase 0: data-coverage scorecard.** Before choosing the build order, the project measures how much OpenStreetMap data each city actually has, on an equal 6 km × 6 km square around the centre.

First results (more cities running):

| City | Buildings / km² | Amenities / km² | Transit stops / km² | Buildings with floor count | Buildings with address |
|---|---|---|---|---|---|
| London | 1,045 | 455 | 37 | 49% | 58% |
| Tokyo | 1,766 | 472 | 43 | 17% | 7% |

These numbers show why raw tag completeness is not a quality score: Tokyo's low address rate reflects Japan's block-based addressing, not poor mapping. The project therefore treats data richness as a confidence signal, read against each city's own conventions.

## Repository layout

```
ml/                    data pipeline, scorecard and models (Python)
  scorecard/           OpenStreetMap coverage measurement
web/                   Next.js application
PROJECT-ROADMAP.md     product thesis, architecture, phases, decision log
FEATURE-LOG.md         every feature decision (accepted, deferred, rejected)
docs/feature-catalog.md  grouped feature catalog with data sources and waves
```

## Running the scorecard

```bash
cd ml
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1    macOS/Linux: source .venv/bin/activate
pip install requests pandas
python scorecard/osm_coverage.py --cities London Tokyo
```

Edit the contact address in the script's `User-Agent` before running; the public Overpass servers ask scripts to identify themselves. Results are cached and written to `ml/scorecard/results/`.

## Honest limits and ethics

- The product covers the **measurable half** of the decision. Community, language and personal ties are only partly visible to data.
- Geopolitics is the hardest pillar to forecast; it appears as exposure flags and scenarios, not predictions.
- No ethnicity or race features. Community-related features (international concentration, home-community presence) are **opt-in and positive-only**: there is never an option to avoid areas because of who lives there.
- Perception and aesthetic scores are experimental and flagged as culturally biased.
- Sensitive profile data (personality, finances) is consented, minimised and deletable.
- Not legal, immigration, financial or insurance advice.

## Data and licences

The project uses open data (OpenStreetMap under ODbL, national statistics, transit feeds, satellite and climate-scenario datasets) and records the licence and commercial-use terms of every source. Listing portals and booking platforms are not scraped. OpenStreetMap data © OpenStreetMap contributors.

## Roadmap

| Stage | Focus |
|---|---|
| **MVP** | Accounts, short profile, 4 cities (London, NYC, Tokyo, Singapore), core features plus climate hazards, one real backtest, map UI, critique loop |
| **v1** | All ten cities, scenario engine, questionnaires, regret view, twin finder, scouting plan |
| **v1.5** | Pathway planner, arrival tools, street-view indicators, geopolitical flags |
| **v2** | Community matching, monitoring alerts, deep-learning imagery features, more regions |

Details: [PROJECT-ROADMAP.md](PROJECT-ROADMAP.md).

## Prior work

An earlier badminton pose-analysis prototype (MediaPipe and YOLO-Pose experiments) is parked in this repository family as a documented research prototype.