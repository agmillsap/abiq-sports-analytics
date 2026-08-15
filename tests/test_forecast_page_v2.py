from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = ROOT / "showcase_v3.py"
BASE_JS = ROOT / "frontend" / "showcase_exec.js"
FINAL_JS = ROOT / "frontend" / "final_visual_cleanup.js"
PROFILE_JS = ROOT / "frontend" / "slate_confidence_profile.js"
V2_JS = ROOT / "frontend" / "forecast_page_v2.js"
V2_CSS = ROOT / "frontend" / "forecast_page_v2.css"


def _slate_rows() -> list[tuple[str, str, float, float, str]]:
    source = SHOWCASE.read_text(encoding="utf-8")
    rows = re.findall(
        r'_slate_forecast\("([A-Z]+)", "([A-Z]+)", ([0-9.]+), ([0-9.]+), "([^"]+)"\)',
        source,
    )
    return [
        (favorite, underdog, float(probability), float(close_game), kickoff)
        for favorite, underdog, probability, close_game, kickoff in rows
    ]


def test_full_week_one_slate_contains_16_unique_games_and_32_teams() -> None:
    rows = _slate_rows()
    assert len(rows) == 16
    assert len({(favorite, underdog) for favorite, underdog, *_ in rows}) == 16
    teams = [team for favorite, underdog, *_ in rows for team in (favorite, underdog)]
    assert len(teams) == 32
    assert len(set(teams)) == 32


def test_full_slate_is_ranked_and_summary_counts_are_consistent() -> None:
    rows = _slate_rows()
    probabilities = [probability for _, _, probability, _, _ in rows]
    close_game = [risk for _, _, _, risk, _ in rows]

    assert probabilities == sorted(probabilities, reverse=True)
    assert sum(probability >= 0.70 for probability in probabilities) == 3
    assert sum(risk >= 0.80 for risk in close_game) == 10

    tightest = min(rows, key=lambda row: row[2])
    assert tightest[0:2] == ("MIN", "GB")
    assert round(tightest[2] * 100, 1) == 51.2


def test_forecasts_v2_replaces_redundant_surfaces_with_distinct_questions() -> None:
    js = V2_JS.read_text(encoding="utf-8")
    css = V2_CSS.read_text(encoding="utf-8")

    for text in (
        "PRE-SNAP READ",
        "What the slate is telling us before kickoff.",
        "THE BOARD",
        "Every Week 1 matchup, ranked by forecast confidence.",
        "PRESSURE MAP",
        "Where confidence and game tension collide.",
        "UPSET WATCH",
    ):
        assert text in js

    assert "data.forecast_slate" in js
    assert "close_game_probability" in js
    assert "Close-game risk is a separate matchup-context signal" in js
    assert "renderForecasts = function(parentElement, data)" in js
    assert "200 - 2 * probability" not in js
    assert "SLATE CONFIDENCE PROFILE" not in js
    assert ".abiq-full-slate-columns" in css
    assert ".abiq-pressure-layout" in css


def test_forecasts_v2_is_loaded_after_prior_overrides() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert 'forecast_page_v2.css' in source
    assert 'forecast_page_v2.js' in source
    assert source.index('slate_confidence_profile.css') < source.index('forecast_page_v2.css')
    assert source.index('slate_confidence_profile.js') < source.index('forecast_page_v2.js')


def test_forecasts_v2_does_not_expose_private_runtime_state() -> None:
    source = V2_JS.read_text(encoding="utf-8") + V2_CSS.read_text(encoding="utf-8")
    forbidden = (
        "SUPABASE_",
        "st.secrets",
        "survivor_state",
        "pool_pick",
        "pick_popularity",
        "nfl-survivor-command-center",
    )
    for token in forbidden:
        assert token not in source


def test_combined_showcase_javascript_parses_with_forecasts_v2(tmp_path: Path) -> None:
    bundle = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (BASE_JS, FINAL_JS, PROFILE_JS, V2_JS)
    )
    bundle_path = tmp_path / "showcase_bundle_v2.mjs"
    bundle_path.write_text(bundle, encoding="utf-8")
    subprocess.run(
        ["node", "--check", str(bundle_path)],
        check=True,
        capture_output=True,
        text=True,
    )
