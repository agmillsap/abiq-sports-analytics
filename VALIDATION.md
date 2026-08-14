# ABIQ Validation Evidence

This public document summarizes the historical evidence shown in the ABIQ Portfolio Showcase. It is intentionally narrower than the private production research record.

## NFL game model

The accepted 2025 regular-season replay used a point-in-time expanding-window design. Each target week was predicted using only completed earlier seasons plus earlier completed 2025 weeks.

- 272 regular-season games replayed across 18 weeks
- 271 non-tie outcomes for winner-accuracy scoring
- 179 / 271 winners correct = **66.05%**
- Brier score: **0.214355**
- Log loss: **0.617029**
- 37 market-free football features
- **0 temporal-cutoff violations**

Closing-market results are retained internally as a benchmark but are not presented here as equivalent production inputs because historical quote timing was not validated for ABIQ's live decision horizon.

## Fantasy preseason established-player holdout

Before the 2025 holdout was revealed, ABIQ froze a baseline and a position-specific `StandardScaler + Ridge(alpha=10)` challenger. The same 589 established-player population was evaluated across Standard, Half-PPR, and PPR scoring.

| Scoring | Frozen baseline MAE | Ridge MAE | MAE reduction | Ridge Spearman |
|---|---:|---:|---:|---:|
| Standard | 52.229 | 28.800 | **44.86%** | **0.722** |
| Half-PPR | 59.971 | 32.723 | **45.44%** | **0.734** |
| PPR | 67.795 | 36.773 | **45.76%** | **0.741** |

Temporal integrity passed with **0 violations** in all three formats.

### Scope limitations

- This validates the established-player preseason challenger, not the entire Fantasy product.
- Players without prior-season history, including rookies/new entrants, require separate handling.
- Weekly start/sit, waiver, and trade workflows require separate point-in-time weekly validation.
- The 2025 holdout is not reused for post-reveal hyperparameter tuning.
- Historical performance does not guarantee future results.
