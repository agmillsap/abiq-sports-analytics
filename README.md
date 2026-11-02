# ABIQ | Sports Decision Intelligence

**Analytics. Balance. Intelligence. Quality.**  
*Smarter decisions through analytics.*

ABIQ is an independently built football decision-intelligence platform that combines predictive analytics, model governance, optimization, automated data operations, and fan-first product design.

This repository contains the **public portfolio Showcase only**. The private production codebase, user state, credentials, provider configuration, and operator controls are intentionally excluded.

## What opens first

The Showcase now opens on a **static, sanitized version of the real ABIQ Dashboard experience** rather than a generic portfolio landing page. The visual hierarchy, navigation shell, weekly decision framing, recommendation panels, and ABIQ brand language mirror the private product while all displayed current-season data remain static examples.

A subtle `Static Showcase` indicator and disclosure distinguish exemplary current-season data from validated historical performance.

The NFL Week 1 forecast example is intentionally frozen. This public Showcase is **not a weekly data feed**: team, matchup, recommendation, odds, injury, weather, and other current-season football inputs are not refreshed on a schedule. The NFL header's week control does not trigger new weekly data. Only accepted historical model-performance evidence may be updated over time as new validation is completed.

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
