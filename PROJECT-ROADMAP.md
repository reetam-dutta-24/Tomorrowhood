# Neighbourhood Advisor — Product Thesis & Master Roadmap (v2, working title)

**Status:** planning · **Region v1:** Asia-Pacific · **Cities v1:** Tokyo, Osaka, Seoul, Taipei, Singapore, Hong Kong, Kuala Lumpur, Bangkok, Ho Chi Minh City (last in the build queue)

Status legend: ✅ Done · 🟡 In progress · ⬜ Not started · ❓ Unverified (needs the Phase 0 scorecard)

---

## 1. Headline and thesis

**Headline (working):** *Choose where to live for the world of 2035, not 2025.*

Relocation is an **investment decision under uncertainty** whose payoff arrives over 3–10 years. Most tools describe places as they are today, at country or city level. People rarely regret the country; they regret the **neighbourhood**. And almost nobody weighs **climate, sustainability and geopolitics** when choosing where to live, although these shape how a place will be in ten years.

This product recommends **neighbourhoods and urban areas**, ranked by what is most convenient for the user *given where each area is heading*, and stress-tested against several possible futures. The result is a mixed shortlist that can interleave areas from different cities. Users refine it with a critique loop and see forecasts with honest uncertainty, backed by charts and statistics.

**Five pillars (do not drop these):**
1. **Future investment** — trajectory over 3–10 years, with uncertainty, not a snapshot. *(main USP)*
2. **Climate resilience** — heat, flood, typhoon, seismic, subsidence, water and power security, adaptation capacity, insurability, under climate scenarios.
3. **Sustainability** — transit, air quality trend, green space, energy mix, walkability, and the personal carbon footprint of living there.
4. **Geopolitical exposure** — shown as scenario stress tests and risk flags, **not** predictions (the weakest-forecastable pillar; be honest about it).
5. **Personal fit** — "most convenient for me", not "best": a user-weighted utility under constraints, with regret minimisation across futures.

**Two meanings of "investment" (keep separate in UI and write-up):** *livability trajectory* (will quality of life hold up?) and *financial trajectory* (property and rent). Prices are mainly a backtest proxy and an affordability input, not the objective.

---

## 2. Competitive landscape (searched 30 Oct 2026)

I searched for products that already do this and found **adjacent tools, not the full combination**. English-language web only; absence of evidence is not proof, so re-check periodically and check local-language products.

| Product | What it does | Gap vs this project |
|---|---|---|
| [CanHelp Move](https://canhelpmove.com/) | AI relocation advisor; 320+ cities, 42 countries; neighbourhood suggestions only in a paid report | City-level, data sources undisclosed, climate = seasons and air quality, no stated forecasting or geopolitics |
| [ExpatLife.ai](https://expatlife.ai/cities) | 122 countries, 351 city guides, 1,800+ neighbourhood comparisons, quiz, calculators | Editorial and guide-style, no forecasting, light climate |
| [DISTRIQ](https://distriq.ai/) | "Neighbourhood intelligence" for 200+ neighbourhoods in 12+ countries (schools, commute, hidden costs) | No forecasting, climate or geopolitics on the page I could read |
| [Rumavi Global Relocation Index](https://rumavi.com/en/global-relocation-index/methodology) | 192 countries, 24 metrics, six personas, includes climate risk (ND-GAIN) and conflict risk (Global Peace Index); published methodology | **Country-level, annual snapshot**, no neighbourhoods, no forecasts. A good model for methodology transparency |
| [Neighbourhood matcher for China](https://chinavisitguide.com/tools/neighbourhood-matcher) | Neighbourhood matches in 5 mainland cities | Editorial rents, no forecasts or climate |
| [NextMove AI](https://nextmove-ai.com/), CityMatch.ai, Where Do I Move To, SettleSavvy | AI "where should I move" matchers | Crowded, mostly US or city-level, undisclosed data (this is the cliché zone) |
| [First Street](https://firststreet.org/pricing/home-buyers), RiskBeforeBuy, Redfin climate | Property-level flood, wildfire, hurricane, heat risk | **US only** |
| [Climate Central coastal screening](https://www.climatecentral.org/climate-services/coastal-flood-layers) | Global sea-level and coastal flood layers | Hazard layer, not a personalised relocation tool |
| XDI, MSCI, ICE climate analytics | Asset-level physical climate risk for APAC real estate | Institutional, not consumer |
| [Henley GIRRI](https://www.henleyglobal.com/publications/global-investment-risk-and-resilience-index/may-2026-update/global-risk-rankings-post-shock-re-ranking) | Country investment risk and resilience ranking | Country-level, investor-oriented |
| [Urban liveability time-series paper (NL)](https://ar5iv.labs.arxiv.org/html/2309.00594) | Research: tracking neighbourhood liveability over time from aerial images | Research only; shows **domain shift is a real problem** (rankings degraded over time and across cities) |
| Local hazard portals (e.g. Japan's official hazard maps ❓) | Per-country official risk maps | Fragmented per country; none unify, forecast and personalise |

**Conclusion:** the novelty is the *combination*: neighbourhood-level × forward-looking × climate, sustainability and geopolitics scenarios × personalised profile × Asia-Pacific × regret minimisation × critique loop, with disclosed methods and backtests. Each piece exists somewhere; the combination, as built here, was not found. **Threat:** the "AI relocation advisor" category is crowded with thin wrappers, and incumbents could add climate layers. The defence is real data pipelines, validation and transparency.

---

## 3. Users and problem

- **Who:** students, professionals, families choosing where to live in Asia-Pacific; later relocation firms, employers' mobility teams, universities.
- **Problem:** choices come from social media, rankings and agents with conflicts of interest; country and city rankings hide huge within-city variation; climate and geopolitical exposure are ignored or treated as "weather."

---

## 4. Product flow

### 4.1 Progressive profiling (not one giant form)
1. **Account** (reuse existing auth).
2. **Core profile, about 5 minutes:** budget, work location or remote status, commute tolerance, priorities (sliders), environment (gated community, nature, downtown), time horizon (3 / 5 / 10 years), risk tolerance. → first shortlist immediately.
3. **Optional deeper modules,** each showing how it will refine results ("this adjusts 3 of your 10 weights"); progress is always saved:
   - Personality (Big Five short form), interests/career (RIASEC; skip if the user already knows their career), values, risk tolerance.
   - Affinities and aversions ("biases"): cities or countries liked or avoided.
   - Household and life stage: partner, children and schools, ageing parents, pets, accessibility needs.
   - Cultural infrastructure: food (vegetarian, halal), places of worship, language support, expat communities (partly measures the "community" half via OSM proxies).
   - Health needs: hospitals, English-speaking care.
   - Finance: income, savings, currency, buy vs rent, affordability stress test, taxes, relocation cost.
   - Visa and policy: dependants' work rights, residency path, stability.
   - Future-worldview form (see 4.4).

### 4.2 Instruments (valid, free, and must change results)
- **Big Five** via the public-domain IPIP item pool (short form). **Not MBTI** (proprietary, weak science).
- **Career interests:** RIASEC / Holland via the free O*NET Interest Profiler ❓ (verify terms).
- **Values:** a short Schwartz-style instrument ❓ (verify licence). **Risk tolerance:** a short validated scale.
- Instruments map to **soft priors, always user-overridable** (e.g. extraversion → social density and third places; noise sensitivity → quiet; risk tolerance → how much forecast uncertainty the user accepts). Effect sizes in the personality–place literature are small. Never present results as verdicts or diagnoses.

### 4.3 Hard floors (not weights)
Safety, cleanliness, aesthetics and traffic are **minimum thresholds** that exclude areas regardless of preference. Show what was excluded and why, with data confidence. Avoid binary "safe/unsafe" labels. Perception and aesthetic scores are experimental and flagged.

### 4.4 Future-worldview form → scenarios
Climate sensitivity, sustainability priority, geopolitical concern and growth expectation become **scenario weights**. The shortlist is stress-tested under combinations (e.g. high-warming vs moderate; tighter vs looser migration policy; energy-price shock) and shows which areas stay good in all of them. Geopolitics appears as exposure flags and scenario stress tests only.

### 4.5 Dashboard output
- Mixed shortlist with map pins and confidence badges.
- Per-area page: fit breakdown by dimension, trajectory **fan charts**, scenario comparison, "why this area / why not", climate and sustainability panel, commute and transit isochrones, street imagery (v1.5), cost and net-worth simulation.
- Side-by-side comparison; **regret view** (robust vs fragile areas); **sensitivity note** ("ranking flips if you weigh safety +20%"); **counterfactual advice** ("change these two preferences to unlock a better match").
- Shareable report (privacy-controlled) and PDF export.

### 4.6 Feedback loop
Quick controls ("remove this city", "raise greenery", "add a constraint", "I dislike this area"), instant re-rank and a **"what changed" diff**. Critiques train a lightweight preference model.

### 4.7 Monitoring and scouting
- **Alerts** when an area's forecast changes (new transit line, hazard update, policy change).
- **Scouting plan:** auto-generated 3-day visit itinerary to test the top 3 areas on the ground.

### 4.8 Community matching (v2)
Opt-in, pseudonymous, verified, in-app messaging only, reporting and moderation, per-field consent (test results never exposed). Needs users to work. v1 designs the data model; may show anonymised cohort insights once there are users.

---

## 5. Scope v1

### 5.1 Cities
| Tier | Cities | Role |
|---|---|---|
| Strong data | Tokyo, Osaka, Seoul, Taipei, Singapore, Hong Kong | Train, backtest, leave-one-city-out |
| Application (thin data) | Kuala Lumpur, Bangkok, Ho Chi Minh City | Wider uncertainty, data-confidence flags; HCMC built last |

Notes: Osaka is a within-country transfer test for Tokyo. Out for now: Dubai (not Asia-Pacific), mainland China (restricted geodata; possible v2 satellite-only experiment after a legal check), Manila and Jakarta (thin data), Istanbul (inflation-distorted prices). Asia-Pacific is also strongly climate-exposed (typhoons, floods, heat, subsidence, earthquakes), which strengthens the thesis.

### 5.2 Unit of analysis
H3 hexagonal grid at neighbourhood scale, aggregated to named districts for display; city extents from functional urban areas.

### 5.3 Dimensions (user-weighted)
| # | Dimension | Sources (candidates) |
|---|---|---|
| 1 | Housing cost and trend | National transaction registers |
| 2 | Transit and mobility | GTFS, OSM, planned lines |
| 3 | Daily-life amenities | OSM + routing |
| 4 | Environment: air, heat, green space | Satellite, stations |
| 5 | Safety ❓ | Police open data |
| 6 | People and economy | National statistics offices |
| 7 | Growth signals | GHSL, VIIRS, Overture |
| 8 | Street appearance (v1.5) | Mapillary + segmentation |
| 9 | Escape and nature proximity | OSM, protected areas, terrain, routing |
| 10 | Work and commute | OSM, census commuting |
| 11 | **Climate hazards:** heat stress, pluvial/coastal/river flood, typhoon, sea level, subsidence, seismic and tsunami | CMIP6 downscaled data (NEX-GDDP) ❓, ISIMIP ❓, WRI Aqueduct ❓, JRC flood maps ❓, hazard catalogues ❓ |
| 12 | **Adaptation and resilience:** drainage and flood defences, building codes, grid reliability, water security, insurability | Mostly curated ❓ |
| 13 | **Sustainability:** transit share, air-quality trend, green space, grid emissions, walkability, personal carbon footprint | Mixed |
| 14 | **Geopolitical exposure:** stability, rule of law, conflict proximity, energy and food import dependence, capital controls, currency stability | Global Peace Index ❓, World Bank governance ❓, GDELT ❓ (flags and scenarios only) |
| 15 | Policy layer (national): eligibility, tightening risk | Hand-curated, dated |

Dimension 9: user picks which categories count (coast, mountains, trails, protected areas, hot springs, islands) and "off-beat" is defined by measurable proxies. Check protected-area dataset licences before commercial use.

---

## 6. Architecture

Layers: **country** (policy, eligibility, geopolitics, tightening risk) → **city** (jobs, economy, macro and climate context) → **neighbourhood** (all dimensions with 3–10 year trajectories).

**Pipeline:** raw sources → standardised H3 feature tables → trajectory models with uncertainty → **scenario engine** (climate, policy, economy, geopolitics) → user-weighted, floor-filtered ranking → regret-minimising shortlist → critique loop.

**Modelling notes:** panel forecasting per dimension, with naive baselines that must be beaten or honestly reported; conformal or equivalent uncertainty with calibration reported; imputation inside CV folds with "was imputed" flags; data richness feeds a confidence score, never a quality score; climate trajectories use published scenario ensembles (do not invent climate physics), downscaled and combined with local exposure; preference modelling from profile and critiques.

**Web app:** reuse the existing shell (Next.js, Auth.js, themes, onboarding wizard, dashboard, CI); map-first UI; every score expandable to its source and confidence ("glass box").

---

## 7. Out-of-the-box features (backlog, ordered by value)
1. **Glass-box scoring:** model and data cards, per-score sources and confidence (the answer to black-box AI advisors).
2. **Climate analogue cities:** "this area in 2040 feels like X today."
3. **Risk-adjusted cost:** price vs expected climate loss ("12% cheaper but higher expected flood exposure").
4. **Micro-advice:** floor-level and block-level guidance from elevation data.
5. **Insurability and financing reality check** for foreigners.
6. **Time-horizon slider:** rankings change between 3 and 10 years.
7. **Shock simulator:** typhoon season, energy-price spike, visa cap, currency drop, with personal impact.
8. **Reversibility score:** how costly it is to leave.
9. **Personal carbon footprint** of living in each area.
10. **Bias audit:** where stated preferences differ from evidence.
11. **Group relocation optimiser** (B2B): balance several employees' preferences.
12. **Aggregated demand signals** (anonymised) as a longer-term data moat.

---

## 8. Data register (mandatory before any monetisation)

Table per source: URL, licence, commercial use?, attribution or share-alike duties, coverage years, last checked. Found so far (existence confirmed, quality ❓):

| Area | Source | Notes |
|---|---|---|
| Japan housing | MLIT transaction prices | Anonymised to district level ❓ |
| Korea housing | MOLIT actual sale prices (data.go.kr), Seoul dataset | API key and terms |
| Taiwan housing | Actual price registration (data.gov.tw) | Coverage from about 2013 ❓ |
| Singapore housing | HDB resale (data.gov.sg) | Public housing only |
| Hong Kong housing | RVD price indices | Indices, not sales |
| KL, Bangkok, HCMC housing | Aggregators or asking prices only | Official open data ❓; **do not scrape listing portals** |
| Transit | GTFS-JP and community Tokyo feeds, Seoul TOPIS, Taiwan TDX, Hong Kong Transport Dept, Singapore transport open data, Malaysia GTFS | Bangkok, HCMC ❓ |
| Small-area stats | Japan e-Stat, Korea SGIS, Hong Kong planning units | Others ❓ |
| Global layers | OSM (ODbL: attribution and share-alike), GHSL, WorldPop, Sentinel, VIIRS, Overture, Mapillary (CC BY-SA) | Google Earth Engine free tier is non-commercial |
| Climate | CMIP6 downscaled, ISIMIP, WRI Aqueduct, JRC flood, seismic catalogues, Climate Central | Licences ❓ |

---

## 9. Evaluation plan
1. **Temporal backtests** (train to year T, predict T+5 to T+10); no random splits for forward-looking targets.
2. **Per-dimension backtests** on each dimension's own history (population, built-up, air quality, transit access, flood events).
3. **Price proxy** in strong-data cities, labelled as a desirability proxy.
4. **Leave-one-city-out** (Tokyo → Osaka cleanest). Expect domain shift (see the NL liveability paper) and report it.
5. **Ablation and rank stability:** global-only features vs full set.
6. **Natural experiments:** transit openings with known dates.
7. **Calibration** of all uncertainty intervals; failures reported openly.
8. **User study (20–30 people):** do the deeper questionnaires improve perceived fit versus a minimal profile? Do users return and refine?

---

## 10. Ethics, privacy and limits
- Personality, values, affinities and finances are sensitive: consent, encryption, minimisation, easy deletion (India's DPDP Act, GDPR).
- No ethnicity or demographic-composition features; show displacement and gentrification risk openly.
- Geopolitics presented neutrally as evidence-based exposure flags, never as political advocacy; not predictions.
- Perception and aesthetic scores are experimental and culturally biased.
- Data richness means confidence, not quality.
- Community, language and personal ties are only partly measurable; say so.
- Not legal, immigration, financial or insurance advice. Community matching needs safety design before launch.

---

## 11. Phased roadmap

**Time (part-time, honest):** an MVP cut in about 8–10 weeks; full v1 about 14–18 weeks.

| Phase | Work | Status |
|---|---|---|
| **0** | Decisions, repo, **data-richness scorecard script** (fills every ❓), licence register | ⬜ |
| **1** | Spatial foundation: H3 grid, city extents, OSM, routing, GTFS. **Tokyo end to end first** | ⬜ |
| **2** | Feature layers: accessibility, environment, growth, transit, stats, nature proximity, housing, **climate hazard layers** | ⬜ |
| **3** | Trajectory models, uncertainty, backtests, leave-one-city-out, ablations (**MVP cut line**) | ⬜ |
| **4** | Core profile, floors, shortlist, critique loop, **scenario engine** (climate and policy first) | ⬜ |
| **5** | Web app: map UI, area pages, charts, confidence display, reuse of shell | ⬜ |
| **6 (v1.5)** | Personality and interest instruments, affinities and bias audit, future-worldview form, scouting plan, street-view indicators, geopolitical flags, tightening-risk predictor | ⬜ |
| **7** | Evaluation write-up, deployment, demo video, user study | ⬜ |
| **v2** | Community matching, monitoring alerts, nature and remote mode (Bali, Caribbean-style destinations), more regions, mainland China satellite-only tier after legal check, B2B group relocation | ⬜ |

**MVP = accounts, a short core profile, 4 strong-data cities, 3–4 dimensions plus climate hazards, one real backtest, map UI, critique loop.** Everything else is bonus.

**Cut line (drop in order):** street view → geopolitical flags and tightening predictor → personality instruments → Ho Chi Minh City → Bangkok and KL → critique-loop learning (keep simple re-ranking).

---

## 12. Decision log
- **Why this project, not CourtKinetics:** CourtKinetics was blocked by compute (0.878 s/frame on CPU, about 120 hours for the footage), manual labelling and multi-person tracking. This project has large structured open data and no GPU dependency. CourtKinetics stays in the repo as a documented research prototype (MediaPipe baseline, YOLO-Pose + ByteTrack findings, Kaggle GPU experiment).
- **Neighbourhood, not country or city.**
- **Asia-Pacific first, 9 cities,** chosen on data richness across dimensions, not property data alone; HCMC last.
- **Headline pillars:** future investment, climate, sustainability, geopolitics, personal fit. Geopolitics is scenario-based only.
- **"Most convenient for me", not "best";** regret minimisation over point-score ranking.
- **Progressive profiling** instead of one long form; instruments must change the output; Big Five and RIASEC, not MBTI.
- **Safety, cleanliness, aesthetics, traffic = hard floors,** with transparency about exclusions.
- **Property data's role:** backtest proxy and affordability input.
- **No scraping of listing portals;** data-licence register mandatory.
- **China excluded in v1** (geodata restrictions).
- **Competitive check (30 Oct 2026):** adjacent tools exist; the full combination was not found; the "AI relocation advisor" category is crowded with thin wrappers, so rigour and transparency are the differentiators.

---

## 13. Open items
- [ ] Project name and repo layout (new repo with web shell copied, vs reuse monorepo)
- [ ] Phase 0 scorecard script: OSM completeness, Mapillary coverage, transit feeds, air-quality, small-area stats, climate layer coverage, per city
- [ ] Licences and commercial-use terms for every source (including instruments: O*NET, values scales)
- [ ] Housing backtest definition per city; functional urban area boundaries
- [ ] Decide which climate scenarios (e.g. moderate vs high warming) the MVP supports
- [ ] CourtKinetics cleanup: add `*.pt` to `.gitignore`, commit remaining scripts, document the Kaggle GPU run, mark repo as a parked prototype
- [ ] Re-run the competitor search quarterly; check local-language products

---

## 14. How to use this document
At the start of each session read Sections 11 and 13. At the end, update status markers and open items. Record non-obvious decisions in Section 12 so the reasoning survives.