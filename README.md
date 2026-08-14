# ABIQ | Sports Decision Intelligence

**Analytics. Balance. Intelligence. Quality.**  
*Smarter decisions through analytics.*

ABIQ is an independently built football decision-intelligence platform that combines predictive analytics, model governance, optimization, automated data operations, and fan-first product design.

This repository contains the **public portfolio Showcase only**. The private production codebase, user state, credentials, provider configuration, and operator controls are intentionally excluded.

## What opens first

The Showcase now opens on a **static, sanitized version of the real ABIQ Dashboard experience** rather than a generic portfolio landing page. The visual hierarchy, navigation shell, weekly decision framing, recommendation panels, and ABIQ brand language mirror the private product while all displayed current-season data remain static examples.

A subtle `Static Showcase` indicator and disclosure distinguish exemplary current-season data from validated historical performance.

## What this Showcase demonstrates

- **NFL predictive modeling:** point-in-time historical replay with explicit leakage controls and probabilistic evaluation.
- **Fantasy model research:** frozen baseline/challenger testing on a protected 2025 holdout before production use.
- **Decision product design:** analytics translated into short, understandable weekly decision surfaces.
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
