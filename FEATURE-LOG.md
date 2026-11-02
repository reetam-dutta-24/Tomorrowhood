# Tomorrowhood: Confirmed Feature Catalog (v0.3, 2 Nov 2026)

Single source of truth linking **what the user cares about → what data measures it → what the form asks → what the report shows.** Built from the founder's 47-item list plus every addition accepted on 31 Oct 2026.

**Status: v1 feature list frozen.** All items below are accepted. New ideas go to `FEATURE-LOG.md` as V2 unless they replace something here. Roughly 84 data features (79 plus the five investor-mode features Q1 to Q5), 18 decision tools (O1 to O18) and one pathway-planner module. v0.3 adds O17 Future Timeline mode, O18 Investor mode, group Q, and the amenity taxonomy notes.

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
| A8 | Temporary stay options for the arrival period (hotels, hostels, motels, guesthouses, serviced apartments, co-living, short-term rentals): density, proximity to transit and airport, typical price band per type | new | N | Weight / Info (arrival plan) | Accommodation points of interest from OSM and Overture (tourism and lodging tags; completeness varies ❓); typical nightly and monthly price bands from official tourism statistics or curated ranges ❓. **No live prices, availability or guest ratings**: booking-platform data is licensed or restricted, and we do not scrape it. Short-term-rental datasets for some cities exist but licences and legitimacy vary ❓. The app links out to booking sites | 🟡 | V1.5 |

## B. Daily convenience and amenities

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| B1 | **Amenity density** (umbrella over B2 to B5, G1 to G4, D3) | 2 | N | Weight | OSM, Overture | 🟢 | MVP |
| B2 | Basic services (grocery, pharmacy, salon, laundry, food stalls, shops, banks and ATMs) | 46 | N | Weight | OSM | 🟢 | MVP |
| B3 | Restaurants and cafes with cuisine preference | 5 | N | Weight | OSM cuisine tag, Overture | 🟢 | MVP |
| B4 | Healthy food and meal-delivery access | 13 | N | Weight | OSM diet and delivery tags only; no platform scraping | 🟡 | V1.5 |
| B5 | Walkability: share of key services within a 15-minute walk | new | N | Derived (headline) | Routing on OSM | 🟢 | MVP |
| B6 | Pedestrian and cycling infrastructure | 12 | N | Weight | OSM footways and cycleways (mapping conventions differ by city; Tokyo cycleways under-tagged) | 🟡 | MVP |
| B7 | Car-free feasibility ("do I need a car?") | new | N | Derived | B5 + C1 + B2 | 🟢 | V1 |
| B8 | Accessibility (step-free transit, wheelchair-tagged venues) | new | N | Filter / Weight | GTFS wheelchair fields, OSM wheelchair tags ❓ | 🟡 | V1.5 |
| B9 | Online delivery coverage: food, grocery, quick commerce, parcels and e-commerce delivery speed | new | N/Ci | Weight | Per-address platform coverage is not open and we do not scrape platforms. Use: city-level platform presence (curated ❓), OSM delivery tags on restaurants and shops, parcel lockers and post offices, dark-store-style shops where tagged ❓. Neighbourhood-level coverage is weak, so it is shown with a low-confidence flag | 🟡 (neighbourhood level 🔴) | V1.5 |

## C. Mobility and work

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| C1 | Public transit access and frequency (bus, metro, rail, tram) | 9 | N | Weight, Target (planned lines) | GTFS feeds, OSM; taxis and ride-hailing have no open data | 🟢 | MVP |
| C2 | Traffic density and congestion | 18 | N | Weight / Floor | No open global source; proxy from road class and junctions | 🔴 | V1.5 (proxy) |
| C3 | Commute to workplace | 40 | N | Filter | Routing from user's address or area | 🟢 | MVP |
| C4 | Part-time job proximity | 45 | N | Weight | No open job locations; proxy: retail and hospitality density | 🔴 | V1.5 (proxy) |
| C5 | Airport and international connectivity (direct flights to home country) | new | Ci | Info | OurAirports and OpenFlights ❓ | 🟢 | V1 |
| C6 | Time-zone overlap with home | new | Ci | Info | Trivial calculation | 🟢 | V1 |
| C7 | Proximity to an international airport (travel time by transit and by road to the nearest international airport). The user chooses: **close / no preference / not too close** (the last links to noise, E6) | new | N | Weight (opt-in, two-sided) | OSM aerodromes and OurAirports (airport type and IATA code ❓), routing on OSM and GTFS | 🟢 | V1 |

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
| F6 | **Women's safety** (own feature; opt-in hard floor): night-time environment (street lighting, venues open late and footfall, night transit service, distance to police and hospitals) plus city and country context (legal protections, published survey indices ❓) | new | N/Ci/Co | Floor (opt-in) / Weight | OSM lighting tags, opening hours, GTFS night services; police open data by offence type only where published. **Recorded sexual-offence rates are not comparable across countries**: they reflect legal definitions and reporting as much as danger, so a higher number can mean more reporting. Used only within a city, flagged as such, never as a "safe/unsafe" label | 🟡 | V1 (environmental proxies), V1.5 (surveys and indices) |

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
| J1 | Career-fit city and area for the profession the user enters (job-cluster match: tech, design, finance, etc.) | 39 | Ci/N | Weight | No open job-posting data; start with curated industry-cluster profiles and employment statistics, plus area-level proximity to employer clusters from OSM office and industrial land use | 🟡 | V1 |
| J2 | Income level by profession, per city | 28 | Ci | Info | National wage statistics; job classifications differ by country, needs a crosswalk ❓ | 🟡 | V1 |
| J3 | **Savings potential** (income by profession vs cost of living) | new | Ci | Derived (headline) | J2 + A4 | 🟡 | V1 |
| J4 | Taxes for foreigners, banking and remittance ease | new | Co | Info | Curated | 🟡 | V1.5 |
| J5 | ~~Stock market conditions~~ | 44 | | | | | **Dropped** |
| J6 | Student-loan and education-finance access for international students and newcomers (eligibility by nationality and status, lenders, typical terms), plus banking and credit access without local credit history | new | Co | Info | Curated from official and lender pages, dated ❓. **Physical proximity to loan offices is a weak signal** (most lending is online or national), so branch and ATM proximity sits in B2 instead | 🟡 | V1.5 |
| J7 | Business, startup and investment friendliness for foreigners, now and outlook (company set-up ease, foreign-ownership limits, startup and investor visa routes, tax incentives, funding ecosystem, talent pool, coworking and office supply) | new | Co/Ci | Weight (opt-in module) | Our own composite from open indicators (for example World Bank business-regulation data ❓, open company registries where available ❓, OSM coworking and offices) plus curated rules; proprietary startup-ecosystem rankings are not redistributed. Outlook from dated policy changes (L4) and published trends ❓ | 🟡 | V1.5 |
| J8 | Career growth outlook for the user's profession: demand trend, salary trend, employer density, by city | new | Ci | Weight, Target (where published) | National occupation projections and wage series where published ❓ (formats differ by country, needs a job-classification crosswalk); OSM office and industrial clusters for employer density | 🟡 | V1.5 |

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
| M3 | Digital and tech modernity: cashless and mobile-payment acceptance, vending and automated retail, parcel lockers, EV charging, bike-share, e-government services, 5G and fibre availability | new | N/Ci | Weight | OSM vending, charging, bike-share and locker tags (neighbourhood level); city-level indicators from central-bank payment statistics ❓, e-government indices ❓, coverage maps ❓ (licences to check). A transparent composite, not a single black-box score | 🟡 | V1 (OSM proxies), V1.5 (city indicators) |

## P. Growth and trajectory signals (from the roadmap; missing from the original 47)

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| P1 | Development momentum (built-up growth, night lights, new construction) | roadmap | N | Target | GHSL, VIIRS night lights, Overture | 🟢 | MVP |
| P2 | Planned infrastructure pipeline (announced transit lines, large projects) | roadmap | N | Target / Scenario input | Curated from official plans, dated | 🟡 | V1.5 |

## Q. Investment inputs (support O18; opt-in)

| ID | Feature | Your # | Level | Role | Data candidates | Ready | Wave |
|---|---|---|---|---|---|---|---|
| Q1 | Rental yield (rent vs price) | new | N/Ci | Target / Derived | A2 with official rental statistics ❓; only aggregates, no listing scraping | 🟡 | V1.5 |
| Q2 | Foreign-buyer rules and costs (ownership limits, stamp duties/surcharges, taxes, restrictions) | new | Co/Ci | Info + filter | Hand-curated, dated, sourced | 🟡 | V1.5 |
| Q3 | Market liquidity (transaction volume, time to sell where published) | new | N/Ci | Info / Weight | Transaction registers (sales counts) | 🟡 | V1.5 |
| Q4 | Financing access for foreigners (mortgage availability, deposit rules, typical rates) | new | Co | Info | Curated, dated ❓ | 🟡 | V2 |
| Q5 | Risk adjustments (climate loss exposure, policy and currency risk, insurability) | new | N/Ci | Derived | K2, L4, roadmap risk-adjusted cost | 🟡 | V2 |

Guardrails: investor mode is a separate objective the user turns on; it never recommends individual properties; every output carries "not financial advice", uncertainty and stress tests.

## Amenity taxonomy (implementation notes, London pipeline)

- Each OSM (class, subtype) pair maps to exactly one group, kept as editable data (`ml/pipeline/taxonomy.py`) with a duplicate guard.
- Groups: daily_services, healthcare, education, food_drink, nightlife, culture_leisure, wellness_fitness, green_outdoor, modern_tech, upscale_retail, upscale_leisure, everyday_retail, worship, transport, stay, trees, street_furniture.
- **Street furniture** (parking, benches, bins, bicycle racks) is separate and never counted as amenity richness; it was about 70% of raw amenity points.
- Composites: `everyday_services` (daily_services, healthcare, education, food_drink, everyday_retail) and `leisure_modern_upscale` (culture_leisure, nightlife, wellness_fitness, modern_tech, upscale_retail, upscale_leisure, upscale hotels). The second is a headline user preference (feeds B1, G2, G4, M3).
- "Upscale" is a proxy (4+ star hotels; jewellery, art, wine and deli shops; spas, golf, marinas), to be validated against price tier (I2) once housing data exists. Scale with percentiles or logs, not max.
- Ring access features (k1 about 300 m, k4 about 1.2 km straight-line) feed B5 until routing exists; the presence-based essentials proxy saturates in inner London.

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
| O6 | Landing area vs settling area | Recommends a short-stay landing area (transit, services, newcomer-friendly, easy from the airport) separately from the long-term one, with stay types and typical price bands; shows how long the user plans to stay temporarily | A8, C7, OSM accommodation tags, B2, C1, A7, I9 | V1.5 |
| O7 | Pre-mortem ("why you might regret this") | Top three risks for this user and area, from rules over the data; no LLM | All dimensions, sensitivity analysis | V1 |
| O8 | Couples and household mode | Two workplaces and two preference sets; finds areas that balance both and shows fairness | C3, ranking engine | V1.5 |
| O9 | Before/after comparison | User enters where they live now; report shows change in commute, savings, climate, hazards, amenities | O1, J3, K1, K2 | V1.5 |
| O10 | Arrival kit | Nearest immigration office, embassy, banks, SIM shops and familiar-food grocery per area | OSM office and diplomatic tags (completeness to check ❓), B2, I3 | V1.5 |
| O11 | Break-even horizon | Years until savings potential covers the one-off cost of relocating | J3, O14 | V1.5 |
| O12 | Time-machine map | Slider showing an area's past and forecast with uncertainty bands | Trajectory models | V1.5 |
| O13 | "A year here" view | Month-by-month climate, daylight and seasonal conditions per area | K1, K5 | V1.5 |
| O14 | Landing cost calculator | Total first-year cost: visa fees, temporary stay, deposits, flights, furniture, first months of rent | A7, J4, pathway module | V1.5 |
| O15 | Remote-worker mode | Coworking spaces, internet quality, time-zone overlap, remote-work visas | M1, C6, OSM, pathway module | V1.5 |
| O16 | Grounded AI assistant (RAG chatbot) | Answers questions about results, methodology, policy cards and pathway routes using retrieval over our curated documents plus calls to the structured ranking and data services, with citations and "last verified" dates. It **explains** results; it never generates or changes the scores. Declines to give legal or immigration advice | Curated corpus (pathway module, policy layer, data and model cards), ranking API, vector index | V1.5 (after the curated corpus exists) |

| O17 | **Future Timeline mode** (working name; "manifesting" mode) | Forward simulation: from the user's profile and chosen city/area/route, a 2026 to 2036 slider shows money (savings, costs, break-even), time (commute, hours), risks (climate, policy) and immigration milestones year by year as base, good and bad scenarios. Goal-backward sub-mode: the user states a goal ("own a flat by 2032", "permanent residency by year 5") and sees which cities, areas and routes make it realistic and what must be true. A simulation under stated assumptions, never a prediction of a person's life; every assumption is editable | J3, O11, O14, A2/A3 trends, K2, pathway module (N), L4, trajectory models | V1.5 |
| O18 | **Investor mode ("best place to invest")** | A separate, opt-in mode with its own objective (risk-adjusted property outcome) and its own ranking, never mixed into livability scores. Uses price outlook, rental yield, foreign-buyer rules and costs, liquidity, financing access, and climate and policy risk, with uncertainty and stress tests. Shows areas and cities, never individual properties. Not financial advice | A2, A3, Q1 to Q5, K2, L4, I7, trajectory models | V1.5 (basic), V2 (full) |

Product features from the roadmap that are not data features (scenario stress tests, regret view, climate analogue cities, risk-adjusted cost, shock simulator, reversibility score, glass-box scoring) remain in `PROJECT-ROADMAP.md`, Section 7.

## Which features carry the forecast (important)

The forward-looking claim rests on features that have **history** to train on or **scenario projections** to use. Most other features are snapshots shown as they are today.

| Forecast basis | Features |
|---|---|
| Historical time series (backtestable) | A2 price, A3 rent, Q1 rental yield, Q3 liquidity, I1 population, P1 development momentum, E4 air quality trend, K4 heat and green-cover trend, C1 transit access (opening dates), J8 profession demand and salary trend (where published) |
| Published scenario projections | K2 climate hazards, K1 climate shifts |
| Curated, dated plans | P2 planned infrastructure, L4 policy tightening |
| Snapshot only (shown, not forecast) | Most amenity, safety, education and leisure features |

Where a feature is a snapshot, the report says so. The backtests in the evaluation plan cover the first group.

## How the preference form falls out of this catalog

- **Core form (about 5 minutes):** life-stage preset (O3), budget and home type (A2, A4, A5), commute (C3), climate preference (K1), top priorities as sliders (one per group: daily convenience, fitness and nature, leisure and culture, education, health, mobility), and hard floors (safety, women's safety (opt-in, F6), noise, air quality, hazards).
- **Optional modules:** career (J1, J8), business or investor interest (J7), student finance (J6), delivery needs (B9), language (I4, I8), origin-culture presence (I3), international or local-immersion preference (I9), home-community presence (I10), family (D2), student or bachelor needs (A6), nightlife and social scene (G2), accessibility (B8), arrival plan and airport proximity (A8, C7), household mode (O8), opt-in flags (I6), investor mode (O18, Q1 to Q5), and the future-timeline goal inputs (O17).
- **Report:** the same groups appear as sections, each showing the raw measures behind the score and their data confidence.