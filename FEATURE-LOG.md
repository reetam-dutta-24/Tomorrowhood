# Tomorrowhood: Confirmed Feature Catalog (v0.2, 31 Oct 2026)

Single source of truth linking **what the user cares about → what data measures it → what the form asks → what the report shows.** Built from the founder's 47-item list plus every addition accepted on 31 Oct 2026.

**Status: v1 feature list frozen.** All items below are accepted. New ideas go to `FEATURE-LOG.md` as V2 unless they replace something here. Roughly 71 data features, 15 decision tools and one pathway-planner module.

## How to read this

- **Your #**: the number in the original 47-item list. "new" = added later (all accepted).
- **Level**: Co = country, Ci = city, N = neighbourhood (H3 cell).
- **Role**: *Weight* (user-weighted preference), *Floor* (hard minimum, excludes areas), *Filter* (hard constraint set by the user, e.g. budget), *Info* (shown, not scored), *Target* (forecast target), *Derived* (computed from other features).
- **Readiness** (my estimate from memory and partial searches; ❓ until the Phase 0 scorecard measures it): 🟢 open data likely, 🟡 partial or needs a proxy, 🔴 no good open source found.
- **Wave**: MVP = London, NYC, Tokyo, Singapore. V1 = all 10 cities. V1.5, V2 = later.
- **Rule:** a feature enters a wave only if at least 3 of that wave's cities have it. Otherwise the app shows "not available here", never a silent zero.
- **Structure:** raw measures roll up into dimensions the user weights. The preference form asks about dimensions and hard floors, not every raw feature.

## Decisions applied to the original list

| Your # | Decision | Why |
|---|---|---|
| 2, 5, 6, 7, 15, 16, 46 | Merged under one amenity engine (B1) with a category taxonomy | All are counts of points of interest by category |
| 10, 11 | Coordinates are the foundation (A1, not user-facing); price is A2 | Coordinates generate many derived features |
| 34, 35, 36, 37 | Merged into a context-index layer (L1 to L3) built from open indicators | Many famous rankings are proprietary |
| 44 | **Dropped** (stock markets) | Short-term, not neighbourhood-relevant, not forecastable |
| 7 | Renamed "nightlife and social scene" | Same data, better for a public product |
| 17, 19 | Moved to V2 (image-based) | Needs deep learning, deferred |
| 18, 45 | Proxy only | No open traffic or job-location data |
| 38 | Venue counts first, event counts later | Event data is behind APIs with licence limits |

## A. Housing and cost

| ID | Feature | Your # | Level | Role | Data candidates (❓ unverified) | Ready | Wave |
|---|---|---|---|---|---|---|---|
| A1 | Spatial context: distance to centre, coast, rail, airport, elevation | 10 | N | Derived (foundation) | H3 index, OSM, elevation model | 🟢 | MVP |
| A2 | House price level and trend | 11 | N | Filter, Target | National transaction registers (Berlin, Toronto have gaps) | 🟡 | MVP |
| A3 | Rent level, rent vs buy | new | N/Ci | Filter, Target | Mostly aggregates; some official rental stats | 🟡 | V1 |
| A4 | Cost of living (groceries, transport, utilities) | 42 | Ci | Filter | Official CPI and price stats; do not redistribute proprietary cost indices | 🟡 | MVP (city level) |
| A5 | Preferred home type (flat, house, gated, high-rise, premium) | 43 | N | Filter | OSM building types and levels; "gated society" mapped to generic classes | 🟡 | V1 |
| A6 | Student and bachelor-friendly housing | 27 | N | Weight | Proxies: small-unit share, university proximity, shared-housing tags; no listing scraping | 🟡 | V1.5 |
| A7 | Newcomer rental friction (deposits, key money, guarantor, credit history, lease length) | new | Co/Ci | Info + flag | Hand-curated per country, dated | 🟡 | V1 |

## B. Daily convenience and amenities

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| B1 | **Amenity density** (umbrella over B2 to B5, G1 to G4, D3) | 2 | N | Weight | OSM, Overture | 🟢 | MVP |
| B2 | Basic services (grocery, pharmacy, salon, laundry, food stalls, shops) | 46 | N | Weight | OSM | 🟢 | MVP |
| B3 | Restaurants and cafes with cuisine preference | 5 | N | Weight | OSM cuisine tag, Overture | 🟢 | MVP |
| B4 | Healthy food and meal-delivery access | 13 | N | Weight | OSM diet and delivery tags only; no platform scraping | 🟡 | V1.5 |
| B5 | Walkability: share of key services within a 15-minute walk | new | N | Derived (headline) | Routing on OSM | 🟢 | MVP |
| B6 | Pedestrian and cycling infrastructure | 12 | N | Weight | OSM footways and cycleways (mapping conventions differ by city; Tokyo cycleways under-tagged) | 🟡 | MVP |
| B7 | Car-free feasibility ("do I need a car?") | new | N | Derived | B5 + C1 + B2 | 🟢 | V1 |
| B8 | Accessibility (step-free transit, wheelchair-tagged venues) | new | N | Filter / Weight | GTFS wheelchair fields, OSM wheelchair tags ❓ | 🟡 | V1.5 |

## C. Mobility and work

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| C1 | Public transit access and frequency (bus, metro, rail, tram) | 9 | N | Weight, Target (planned lines) | GTFS feeds, OSM; taxis and ride-hailing have no open data | 🟢 | MVP |
| C2 | Traffic density and congestion | 18 | N | Weight / Floor | No open global source; proxy from road class and junctions | 🔴 | V1.5 (proxy) |
| C3 | Commute to workplace | 40 | N | Filter | Routing from user's address or area | 🟢 | MVP |
| C4 | Part-time job proximity | 45 | N | Weight | No open job locations; proxy: retail and hospitality density | 🔴 | V1.5 (proxy) |
| C5 | Airport and international connectivity (direct flights to home country) | new | Ci | Info | OurAirports and OpenFlights ❓ | 🟢 | V1 |
| C6 | Time-zone overlap with home | new | Ci | Info | Trivial calculation | 🟢 | V1 |

## D. Education

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| D1 | Schools and universities: count and proximity (quality later) | 1 | N | Weight | OSM for count. Quality rankings are not comparable across countries; use only where a standardised source exists | 🟢 count, 🔴 quality | MVP count, V1.5 quality |
| D2 | International schools and childcare | new | N | Filter | OSM plus curated | 🟡 | V1.5 |
| D3 | Workshops, classes, clubs, community spaces (yoga, music, zumba) | 16 | N | Weight | OSM community centres and leisure tags; Meetup-style data has licence limits ❓ | 🟡 | V1.5 |

## E. Health and environment

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| E1 | Healthcare access (hospitals, clinics, pharmacies) | 8 | N | Weight / Floor | OSM | 🟢 | MVP |
| E2 | Healthcare system quality | 8 | Co/Ci | Info | WHO and OECD indicators ❓ | 🟡 | V1 |
| E3 | Healthcare access for foreigners (insurance rules, English-speaking care) | new | Co | Info | Curated | 🟡 | V1.5 |
| E4 | Air quality (AQI) and trend | 21 | N/Ci | Weight / Floor, Target | OpenAQ stations, satellite air data ❓ | 🟡 | MVP |
| E5 | Water quality and access | 22 | Ci | Info (flag) | National data; hard to compare | 🔴 | V1.5 (flag) |
| E6 | Noise (roads, rail, flights, nightlife) | new | N | Weight / Floor | EU noise maps for London, Paris, Berlin ❓; proxies elsewhere | 🟡 | V1.5 |

## F. Safety, cleanliness and look-and-feel

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| F1 | Crime rate | 14 | N | Floor | Police open data; definitions differ across countries, so compare within a city and flag across cities | 🟡 | MVP |
| F2 | Cleanliness and hygiene from imagery | 17 | N | Floor (experimental) | Street imagery + segmentation model | 🔴 | V2 |
| F3 | Aesthetics and visual character | 19 | N | Weight (experimental, flagged as culturally biased) | Street imagery + model | 🔴 | V2 |
| F4 | Views (sunset, skyline, water) | 19 | N | Weight | Viewshed from elevation model plus building heights | 🟡 | V1.5 |
| F5 | Pedestrian road safety (crash data) | new | N | Info | Some city crash datasets ❓ | 🟡 | V2 |

## G. Leisure, fitness, social and culture

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| G1 | Entertainment venues (arcades, bowling, theme parks, casinos, gaming) | 6 | N | Weight | OSM tags | 🟢 | V1 |
| G2 | Nightlife and social scene (bars, pubs, clubs) | 7 | N | Weight | OSM | 🟢 | V1 |
| G3 | Sports facilities (pools, pitches, courts, turfs, indoor halls) | 15 | N | Weight | OSM sport and leisure tags | 🟢 | V1 |
| G4 | Gyms and fitness centres | 4 | N | Weight | OSM | 🟢 | MVP |
| G5 | Parks, green and open space (with satellite greenness) | 3 | N | Weight | OSM, satellite vegetation index | 🟢 | MVP |
| G6 | History, culture, art (museums, galleries, heritage sites) | 33 | N/Ci | Weight | OSM, Wikidata ❓ | 🟢 | V1 |
| G7 | Live music and concerts | 38 | Ci | Weight (niche) | Venue counts from OSM first; event counts need APIs with licence limits ❓ | 🟡 | V1.5 venues, V2 events |

## H. Nature and travel (the "escape and nature proximity" dimension)

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| H1 | Nearby destinations by type (mountains, beaches, forests, islands, historic) with travel time | 31 | N | Weight | OSM natural features, protected-area data (licence ❓), routing | 🟢 | V1 |
| H2 | Nearby adventure activities (trekking, skydiving, zip-lining) | 32 | N | Weight | OSM; rare activities are sparsely mapped | 🟡 | V1.5 |

## I. People and community

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| I1 | Population density and growth | 25 | N | Weight, Target | GHSL, WorldPop, census | 🟢 | MVP |
| I2 | Neighbourhood affluence (price tier, income level) | 26 | N | Weight / Filter | Small-area census income where available | 🟡 | MVP |
| I3 | Home-culture presence: cuisine, places of worship, halal, vegetarian | 5 | N | Weight | OSM points of interest only. No ethnicity, race or religion composition features (the aggregate exceptions are I9 and I10) | 🟡 | V1 |
| I4 | Language environment (English friendliness) and readiness to learn a language | 41 | Co/Ci | Weight | Curated; some proficiency indices are proprietary ❓ | 🟡 | V1 |
| I5 | Immigrant welfare and integration support | 23 | Co | Info | Hand-curated policy layer, dated and sourced | 🟡 | V1 |
| I6 | LGBTQ+ legal protections and acceptance (opt-in) | new | Co | Flag (opt-in) | Legal-rights indices ❓ licences | 🟡 | V1.5 |
| I7 | Gentrification and displacement risk | roadmap | N | Info | Derived from price trends | 🟡 | V1.5 |
| I8 | Language difficulty from the user's native language | new | Co | Info | Published difficulty categories; coverage for non-English native languages to verify ❓ | 🟡 | V1 (if a source exists) |
| I9 | International and expat community presence. The user chooses: **prefer more international / no preference / prefer more local immersion** | new | N | Weight (opt-in, three-way) | Small-area foreign-born or foreign-national share from national statistics (UK census, US ACS, Japan e-Stat, Korean district foreign-resident counts, Statistics Canada, ABS, INSEE, Berlin residents register ❓; Singapore likely resident vs non-resident only ❓), plus service proxies from OSM: international schools, embassies and consulates, coworking, English-language venues. **Aggregate share only; no breakdown by nationality, ethnicity or religion** | 🟡 | V1 |
| I10 | Home-community presence: areas with an established community of the user's own nationality or language. Opt-in, **positive-only** ("find areas with my community"), never "avoid areas with group X" | new | N | Weight (opt-in) | Officially published country-of-birth or nationality aggregates with minimum cell sizes where available ❓ (this is the one feature that needs a per-nationality breakdown); fallback proxies from OSM: cultural centres, places of worship, specialist grocers, language schools, community organisations | 🟡 | V1.5 |

Note on I9: this is where we first use population composition, so it has guardrails. It is opt-in, uses only the total foreign-resident share (never a breakdown by group), is shown with context and a data-confidence flag, and is framed as "international community vs local immersion" (a language learner may reasonably want the second). Census counts update every few years, so this is a snapshot, not a forecast target. The roadmap's ethics section is updated to match.

Note on I10 (for users who want to live near people from their own country): I9 deliberately avoids any breakdown by nationality. I10 needs one (the user's own nationality), so it is a separate and more guarded feature:
- **Opt-in and positive-only.** It finds areas with an established community of the user's nationality or language. There is no option to avoid or rank down areas because of who else lives there.
- **Nationality or country of birth only.** Never ethnicity, race or religion. Only officially published aggregates with minimum cell sizes, never individual-level data.
- **Presence, not majority.** True single-nationality majority areas are rare in these cities, so I10 measures how established a community is (share and community points of interest), not whether it is a majority.
- **Informational.** The report shows it as a layer ("an established Korean community is here") and, where relevant, notes the trade-off with local immersion. It never labels an area better or worse.
- **Uneven data.** Where no small-area nationality data exists, the app falls back to community points of interest and says which source it used.
- Reviewed against local anti-discrimination and data-protection rules (for example GDPR in Europe) before launch. This is a product decision, not legal advice.

## J. Economy and career

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| J1 | Career-fit city and area (job-cluster match: tech, design, finance, etc.) | 39 | Ci | Weight | No open job-posting data; start with curated industry-cluster profiles and employment statistics | 🟡 | V1 |
| J2 | Income level by profession, per city | 28 | Ci | Info | National wage statistics; job classifications differ by country, needs a crosswalk ❓ | 🟡 | V1 |
| J3 | **Savings potential** (income by profession vs cost of living) | new | Ci | Derived (headline) | J2 + A4 | 🟡 | V1 |
| J4 | Taxes for foreigners, banking and remittance ease | new | Co | Info | Curated | 🟡 | V1.5 |
| J5 | ~~Stock market conditions~~ | 44 | | | | | **Dropped** |

## K. Climate, sustainability and resilience

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| K1 | Climate preference (temperature, rainfall, humidity, sunshine, snow, seasons) | 20 | Ci | Weight | Climate normals and reanalysis data ❓ | 🟢 | MVP |
| K2 | Climate hazards and readiness (heat, flood, typhoon or hurricane, wildfire, sea level, earthquake), under scenarios | 29 | N/Ci | Floor / Weight, Target (scenario projections) | Hazard maps, climate-scenario data ❓ | 🟡 | MVP (1 to 2 hazards) |
| K3 | Sustainable development (city and country) | 30 | Ci/Co | Weight | Open SDG indicators ❓ | 🟡 | V1 |
| K4 | Urban heat island and green-cover trend | new | N | Weight, Target | Satellite land-surface temperature and vegetation | 🟡 | V1 |
| K5 | Daylight and winter darkness | new | Ci | Info | Astronomical calculation | 🟢 | V1 |

Note: climate (K1) is the same across a city but differs between cities. Heat and green cover (K4) vary inside a city.

## L. Country context and geopolitics

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| L1 | Passport strength and visa-free access | 34 | Co | Info | Open visa-requirement datasets ❓; the Henley and Passport Index rankings are proprietary | 🟡 | V1 |
| L2 | Country quality of life and development composite (HDI, GDP per capita, literacy, poverty, unemployment) | 35, 36 | Co | Info | Our own composite from open indicators (World Bank, UNDP, WHO, UNESCO) | 🟢 | V1 |
| L3 | City quality of life and rankings | 37 | Ci | Info | Own composite from open data; commercial city rankings are proprietary | 🟡 | V1 |
| L4 | Geopolitical condition, immigration rules and tightening risk | 47 | Co | Flag / Scenario | Curated policy tracker, conflict and stability indices ❓, event data ❓ | 🟡 | V1.5 |

## M. Infrastructure

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| M1 | Internet speed and connectivity | 24 | N/Ci | Weight | Open speed-test datasets exist; licences may be non-commercial ❓ | 🟡 | V1.5 |
| M2 | Utility reliability (power outages, water supply) | new | Ci | Info | National utility stats; weak comparability | 🔴 | V2 |

## P. Growth and trajectory signals (from the roadmap; missing from the original 47)

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| P1 | Development momentum (built-up growth, night lights, new construction) | roadmap | N | Target | GHSL, VIIRS night lights, Overture | 🟢 | MVP |
| P2 | Planned infrastructure pipeline (announced transit lines, large projects) | roadmap | N | Target / Scenario input | Curated from official plans, dated | 🟡 | V1.5 |

## N. Pathway planner (separate module)

A structured roadmap from the user's country to the target city.

**Contents**
- Input: origin country and passport, age, education, profession, finances, target city.
- Output: the main routes (study, skilled work, employer-sponsored, startup, investor, family, remote work, working holiday), each with required exams, documents, typical timeline, cost, and how often the rules change.
- Review and analysis: a comparison of routes by cost, time, difficulty and policy risk.

**Limits:** rules change often and differ per country, so this is curated work. We cannot estimate approval odds. It is not legal or immigration advice. Every card needs an official source link and a "last verified" date, with a stale warning when the date is old.

**Scope:** V1.5 starts with route cards for the top 3 to 4 routes per target country from official pages. Personalised route ranking and alerts: V2.

## O. Decision tools (products built on the features above)

| ID | Tool | What it does | Depends on | Wave |
|---|---|---|---|---|
| O1 | Neighbourhood twin finder | User names an area they know; we return the closest matches in other cities (vector similarity on feature tables) | All feature tables | V1 |
| O2 | Neighbourhood archetypes | Clustering plus plain-language labels (quiet family area, student district, nightlife core, business district) | All feature tables | V1 |
| O3 | Life-stage presets | Student, young professional, family, remote worker, retiree; each pre-fills the form with weights the user can override | Form | MVP |
| O4 | Life-routine simulator | User describes a typical week; we compute weekly travel hours and cost per shortlisted area | Routing, B1 to B3, C1, C3, G4 | V1 |
| O5 | Eligibility-aware shortlist | Cities with no realistic route for the user are excluded or penalised, with the reason shown | Pathway module (N), L1, L4 | V1.5 |
| O6 | Landing area vs settling area | Recommends a short-stay landing area (transit, services, newcomer-friendly) separately from the long-term one | OSM accommodation tags, B2, C1, A7, I9 | V1.5 |
| O7 | Pre-mortem ("why you might regret this") | Top three risks for this user and area, from rules over the data; no LLM | All dimensions, sensitivity analysis | V1 |
| O8 | Couples and household mode | Two workplaces and two preference sets; finds areas that balance both and shows fairness | C3, ranking engine | V1.5 |
| O9 | Before/after comparison | User enters where they live now; report shows change in commute, savings, climate, hazards, amenities | O1, J3, K1, K2 | V1.5 |
| O10 | Arrival kit | Nearest immigration office, embassy, banks, SIM shops and familiar-food grocery per area | OSM office and diplomatic tags (completeness to check ❓), B2, I3 | V1.5 |
| O11 | Break-even horizon | Years until savings potential covers the one-off cost of relocating | J3, O14 | V1.5 |
| O12 | Time-machine map | Slider showing an area's past and forecast with uncertainty bands | Trajectory models | V1.5 |
| O13 | "A year here" view | Month-by-month climate, daylight and seasonal conditions per area | K1, K5 | V1.5 |
| O14 | Landing cost calculator | Total first-year cost: visa fees, deposits, flights, furniture, first months of rent | A7, J4, pathway module | V1.5 |
| O15 | Remote-worker mode | Coworking spaces, internet quality, time-zone overlap, remote-work visas | M1, C6, OSM, pathway module | V1.5 |

Product features from the roadmap that are not data features (scenario stress tests, regret view, climate analogue cities, risk-adjusted cost, shock simulator, reversibility score, glass-box scoring) remain in `PROJECT-ROADMAP.md`, Section 7.

## Which features carry the forecast (important)

The forward-looking claim rests on features that have **history** to train on or **scenario projections** to use. Most other features are snapshots shown as they are today.

| Forecast basis | Features |
|---|---|
| Historical time series (backtestable) | A2 price, A3 rent, I1 population, P1 development momentum, E4 air quality trend, K4 heat and green-cover trend, C1 transit access (opening dates) |
| Published scenario projections | K2 climate hazards, K1 climate shifts |
| Curated, dated plans | P2 planned infrastructure, L4 policy tightening |
| Snapshot only (shown, not forecast) | Most amenity, safety, education and leisure features |

Where a feature is a snapshot, the report says so. The backtests in the evaluation plan cover the first group.

## How the preference form falls out of this catalog

- **Core form (about 5 minutes):** life-stage preset (O3), budget and home type (A2, A4, A5), commute (C3), climate preference (K1), top priorities as sliders (one per group: daily convenience, fitness and nature, leisure and culture, education, health, mobility), and hard floors (safety, noise, air quality, hazards).
- **Optional modules:** career (J1), language (I4, I8), origin-culture presence (I3), international or local-immersion preference (I9), home-community presence (I10), family (D2), student or bachelor needs (A6), nightlife and social scene (G2), accessibility (B8), household mode (O8), opt-in flags (I6).
- **Report:** the same groups appear as sections, each showing the raw measures behind the score and their data confidence.| 2026-10-31 | A8 Temporary stay options for the arrival period (no live prices or ratings) | Accepted (V1.5) | OSM lodging tags plus curated price bands; links out to booking sites |
| 2026-10-31 | C7 Proximity to an international airport (close / no preference / not too close) | Accepted (V1) | OSM, OurAirports and routing |
