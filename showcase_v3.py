from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"

NFL_METRICS = {
    "games": 272,
    "weeks": 18,
    "features": 37,
    "winner_accuracy": 0.6605,
    "brier": 0.214355,
    "log_loss": 0.617029,
    "temporal_violations": 0,
}

FANTASY_METRICS = {
    "population": 589,
    "standard_mae_reduction": 44.8580,
    "half_ppr_mae_reduction": 45.4352,
    "ppr_mae_reduction": 45.7589,
    "standard_spearman": 0.7216,
    "half_ppr_spearman": 0.7336,
    "ppr_spearman": 0.7413,
    "temporal_violations": 0,
}

TEAM_LOGO_SLUGS = {
    "ARI": "ari",
    "CIN": "cin",
    "CLE": "cle",
    "DET": "det",
    "JAX": "jax",
    "LAC": "lac",
    "NO": "no",
    "PHI": "phi",
    "TB": "tb",
    "WAS": "wsh",
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _asset_data_uri(relative_path: str) -> str:
    path = ROOT / relative_path
    mime_by_suffix = {
        ".webp": "image/webp",
        ".png": "image/png",
        ".svg": "image/svg+xml",
    }
    mime = mime_by_suffix[path.suffix.lower()]
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _team_logo(team: str) -> str:
    slug = TEAM_LOGO_SLUGS[team]
    return f"https://a.espncdn.com/i/teamlogos/nfl/500/{slug}.png"


def _game(
    left: str,
    left_probability: float,
    right: str,
    right_probability: float,
    time: str,
) -> dict[str, object]:
    return {
        "left": {
            "team": left,
            "logo": _team_logo(left),
            "probability": f"{left_probability:.1%}",
        },
        "right": {
            "team": right,
            "logo": _team_logo(right),
            "probability": f"{right_probability:.1%}",
        },
        "date": "SUN",
        "time": time,
    }


def _recommendation(
    team: str,
    opponent: str,
    probability: float,
    confidence: str,
) -> dict[str, object]:
    return {
        "team": team,
        "opponent": opponent,
        "logo": _team_logo(team),
        "probability": f"{probability:.1%}",
        "confidence": confidence,
    }


def _rank(label: str, value: float) -> dict[str, object]:
    return {"label": label, "value": value * 100.0, "display": f"{value:.1%}"}


def _payload() -> dict[str, object]:
    # Public Showcase contract: football/team content is intentionally frozen.
    # Only accepted historical model-performance evidence may be refreshed over time.
    return {
        "display_name": "Abigail Millsap",
        "initials": "AM",
        "current_week": 1,
        "weeks": [{"week": 1, "label": "2026 · Week 1"}],
        "logo_data_uri": _asset_data_uri("assets/brand/abiq_wordmark.webp"),
        "iq_data_uri": _asset_data_uri("assets/brand/abiq_iq_hero.webp"),
        "base_texture_data_uri": _asset_data_uri("assets/textures/abiq_texture_base.webp"),
        "accent_texture_data_uri": _asset_data_uri("assets/textures/abiq_texture_accent.webp"),
        "hero_description": (
            "ABIQ turns probability, uncertainty, matchup context and upset risk "
            "into a decision-ready football forecasting experience. This public "
            "opening view uses sanitized static data while preserving the production design system."
        ),
        "kpis": [
            {"icon": "trend", "title": "TOP WIN PROBABILITY", "value": "81.1%", "subtext": "Highest current signal"},
            {"icon": "shield", "title": "CONFIDENCE LEVEL", "value": "High", "subtext": "Strongest weekly tier"},
            {"icon": "check", "title": "GAMES FORECAST", "value": "16", "subtext": "Full weekly slate"},
            {"icon": "target", "title": "REPLAY ACCURACY", "value": "66.05%", "subtext": "2025 point-in-time replay"},
            {"icon": "bars", "title": "PROBABILITY QUALITY", "value": "0.2144", "subtext": "Brier score · 0 perfect / 1 maximum inaccuracy"},
        ],
        "games": [
            _game("ARI", 0.1812, "LAC", 0.8105, "4:25 PM ET"),
            _game("CLE", 0.2318, "JAX", 0.7584, "1:00 PM ET"),
            _game("NO", 0.2711, "DET", 0.7174, "1:00 PM ET"),
            _game("WAS", 0.3386, "PHI", 0.6499, "4:25 PM ET"),
        ],
        "recommendations": [
            _recommendation("LAC", "ARI", 0.8105, "High"),
            _recommendation("JAX", "CLE", 0.7584, "High"),
            _recommendation("DET", "NO", 0.7174, "High"),
            _recommendation("PHI", "WAS", 0.6499, "Medium"),
        ],
        "weekly_rankings": [
            _rank("LAC · ARI", 0.8105),
            _rank("JAX · CLE", 0.7584),
            _rank("DET · NO", 0.7174),
            _rank("PHI · WAS", 0.6499),
            _rank("CIN · TB", 0.6377),
        ],
        "performance_metrics": [
            {"label": "NFL REPLAY", "value": "272 games", "detail": "18-week expanding 2025 regular-season replay"},
            {"label": "WINNER ACCURACY", "value": "66.05%", "detail": "179 of 271 non-tie winners"},
            {"label": "PROBABILITY QUALITY", "value": "0.2144", "detail": "Brier score measures how accurate the model's predicted probabilities are. It ranges from 0 to 1, where 0 is perfect and 1 represents maximum inaccuracy. Confidently wrong forecasts are penalized more severely than cautious misses."},
            {"label": "TEMPORAL INTEGRITY", "value": "0 violations", "detail": "37 prediction-time football features"},
        ],
        "fantasy_holdout": [
            {"label": "Standard", "value": FANTASY_METRICS["standard_mae_reduction"], "display": "−44.86%"},
            {"label": "Half-PPR", "value": FANTASY_METRICS["half_ppr_mae_reduction"], "display": "−45.44%"},
            {"label": "PPR", "value": FANTASY_METRICS["ppr_mae_reduction"], "display": "−45.76%"},
        ],
        "platform_pipeline": [
            {"verb": "OBSERVE", "title": "Data", "copy": "Open and governed football sources normalized into reproducible inputs."},
            {"verb": "TRANSFORM", "title": "Features", "copy": "Prediction-time transforms with explicit temporal cutoffs and provenance."},
            {"verb": "FORECAST", "title": "Models", "copy": "Frozen champion and challenger evaluation with probabilistic metrics."},
            {"verb": "ASSESS", "title": "Risk", "copy": "Win probability, uncertainty and upset exposure translated into comparable signals."},
            {"verb": "EXPLAIN", "title": "Product", "copy": "Fan-first interfaces that surface the decision and preserve analytical depth."},
        ],
    }


SHOWCASE_COMPONENT = st.components.v2.component(
    name="abiq_public_showcase_v5",
    html=_read_text(FRONTEND / "showcase_exec.html"),
    css=(
        _read_text(FRONTEND / "showcase.css")
        + "\n"
        + _read_text(FRONTEND / "showcase_exec.css")
        + "\n"
        + _read_text(FRONTEND / "typography.css")
        + "\n"
        + _read_text(FRONTEND / "mobile_polish.css")
    ),
    js=_read_text(FRONTEND / "showcase_exec.js"),
    isolate_styles=True,
)


def run() -> None:
    st.set_page_config(
        page_title="ABIQ | Sports Decision Intelligence",
        page_icon="◼",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
          [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"],
          [data-testid="stStatusWidget"], [data-testid="stAppDeployButton"], #MainMenu, footer {
            display:none !important;
          }
          .stApp { background:#111313 !important; }
          .block-container { max-width:none !important; padding:0 !important; margin:0 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    SHOWCASE_COMPONENT(
        data=_payload(),
        default={},
        key="abiq_public_showcase_v5",
        width="stretch",
        height="content",
    )
