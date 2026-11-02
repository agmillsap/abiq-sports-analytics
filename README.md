# ABIQ | Sports Decision Intelligence

**Analytics. Balance. Intelligence. Quality.**  
*Smarter decisions through analytics.*

ABIQ is an independently built football decision-intelligence platform that combines predictive analytics, model governance, optimization, automated data operations, and fan-first product design.

This repository contains the **public portfolio Showcase only**. The private production codebase, user state, credentials, provider configuration, and operator controls are intentionally excluded.

## What opens first

The Showcase now opens on a **static, sanitized version of the real ABIQ Dashboard experience** rather than a generic portfolio landing page. The visual hierarchy, navigation shell, weekly decision framing, recommendation panels, and ABIQ brand language mirror the private product while all displayed current-season data remain static examples.

A subtle `Static Showcase` indicator and disclosure distinguish exemplary current-season data from validated historical performance.

The NFL Week 1 forecast example is intentionally frozen. This public Showcase is **not a weekly data feed**: team, matchup, recommendation, odds, injury, weather, and other current-season football inputs are not refreshed on a schedule. The Dashboard's week selector changes the *local CFB scenario planning week* (Weeks 1–14); it never loads new NFL forecasts. NFL selections appear only for the frozen Week 1 public snapshot, while Weeks 2–14 explicitly show that no later NFL forecast is supplied. Only accepted historical model-performance evidence may be updated over time as new validation is completed.

### Combined weekly Dashboard and NFL Forecasts

The Dashboard now presents a **weekly NFL + CFB pick board** aligned with the ABIQ dark/copper design and team logos. At Week 1 it includes three frozen representative NFL forecasts alongside the current SEC and Big Ten illustrative Survivor path picks. Selecting Weeks 2–14 shows the two CFB picks with an explicit NFL unavailable state, **never invented later-week NFL projections**. Changes to the CFB scenario are reflected when returning to the Dashboard. The previous Forecasts destination is now visibly named **NFL Forecasts**, and the validated Performance page is unchanged.

CFB team marks are loaded as public CDN images from ESPN, with readable monogram fallback if the third-party asset is unavailable. These logos are presentation assets, not data collection or odds API calls. The combined board does not rank NFL forecasts against synthetic college probabilities, and the displayed planning week numbers do not imply NFL/CFB calendar alignment.

### CFB Survivor · Interactive Scenario Prototype

The **CFB Survivor** navigation page demonstrates a working, entirely local season-planning interaction:

- Switch between **SEC and Big Ten**, with separate what-if scenarios for each.
- Browse weekly ranked alternatives and a **14-week season path**.
- Inspect **every illustrated game and bye week** for every conference team.
- Override a recommended pick and immediately reoptimize the remaining season; see changed future picks.
- Enforce one selection per week and **no team reuse**; preserve earlier selections when editing later weeks.
- Reset to the default optimal path without mutating private picks or accounts.

The schedule is a **synthetic fixture** (12 illustrated games and two byes for every team), not the official NCAA 2026 schedule. Win percentages are **illustrative inputs**, not calibrated or live CFB predictions. The front-end uses a transparent, deterministic Hungarian assignment optimizer to maximize the product of example probabilities under the no-reuse rule. The display makes no claim about actual season survival, ownership projections, betting edge, or production CFB model validation.

Use `node tests/cfb_survivor.test.cjs` to verify fixture symmetry, complete 14-week plans, no repeated teams, locked-week behavior, and downstream reoptimization without contacting providers.

## What this Showcase demonstrates

- **NFL predictive modeling:** point-in-time historical replay with explicit leakage controls and probabilistic evaluation.
- **Fantasy model research:** frozen baseline/challenger testing on a protected 2025 holdout before production use.
- **Decision product design:** analytics translated into short, understandable weekly decision surfaces, including an interactive CFB Survivor what-if engine.
- **Engineering:** Python, Streamlit, custom HTML/CSS product surfaces, automated GitHub Actions testing, and a separate public/private trust boundary.
- **Model governance:** champion/challenger controls, no silent promotion, and no post-hoc tuning on protected holdouts.

## Selected validation evidence

### NFL game model
- 272 games across the 2025 regular season
- **66.05% winner accuracy** across 271 non-tie games
- Brier score **0.214355**
- 37 market-free football features
- **0 temporal-cutoff violations**

### Fantasy preseason challenger
On the same 589 established-player holdout, the frozen Ridge challenger reduced MAE versus the frozen baseline by:

- **44.86%** — Standard
- **45.44%** — Half-PPR
- **45.76%** — PPR

Ridge rank correlation ranged from **0.722 to 0.741**, with **0 temporal violations**.

See [VALIDATION.md](VALIDATION.md) for methodology, exact metrics, and limitations.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Public / private boundary

The Showcase is intentionally standalone. It does **not** import or connect to the private ABIQ application, production persistence, authentication, saved user picks, paid-provider adapters, or production operations.

The production platform remains private while this repository provides a recruiter-safe view of the product thinking, validation discipline, and user experience.

## Author

Built independently by **Abigail Millsap**.

Historical performance does not guarantee future results.
