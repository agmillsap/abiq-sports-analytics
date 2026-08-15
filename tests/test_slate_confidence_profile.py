from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_JS = ROOT / "frontend" / "showcase_exec.js"
FINAL_JS = ROOT / "frontend" / "final_visual_cleanup.js"
PROFILE_JS = ROOT / "frontend" / "slate_confidence_profile.js"
PROFILE_CSS = ROOT / "frontend" / "slate_confidence_profile.css"
SHOWCASE = ROOT / "showcase_v3.py"


def test_profile_contains_exactly_16_static_week_one_games() -> None:
    js = PROFILE_JS.read_text(encoding="utf-8")
    entries = re.findall(r"\{label: '([^']+)', value: ([0-9.]+), featured: (true|false)\}", js)
    assert len(entries) == 16
    assert len({label for label, _, _ in entries}) == 16


def test_profile_matches_featured_forecast_board_values() -> None:
    js = PROFILE_JS.read_text(encoding="utf-8")
    featured = {
        label: float(value)
        for label, value, is_featured in re.findall(
            r"\{label: '([^']+)', value: ([0-9.]+), featured: (true|false)\}", js
        )
        if is_featured == "true"
    }
    assert featured == {
        "CIN–TB": 63.8,
        "PHI–WAS": 65.0,
        "DET–NO": 71.7,
        "JAX–CLE": 75.8,
        "LAC–ARI": 81.1,
    }


def test_profile_summary_counts_match_probability_bands() -> None:
    js = PROFILE_JS.read_text(encoding="utf-8")
    values = [
        float(value)
        for _, value, _ in re.findall(
            r"\{label: '([^']+)', value: ([0-9.]+), featured: (true|false)\}", js
        )
    ]
    assert sum(50 <= value < 60 for value in values) == 6
    assert sum(60 <= value < 70 for value in values) == 7
    assert sum(value >= 70 for value in values) == 3
    assert "Only 3 of 16 static favorites clear 70%" in js


def test_profile_is_secondary_context_not_redundant_ranked_board() -> None:
    js = PROFILE_JS.read_text(encoding="utf-8")
    css = PROFILE_CSS.read_text(encoding="utf-8")
    assert "SLATE CONFIDENCE PROFILE" in js
    assert "Featured board" in js
    assert "Remaining slate" in js
    assert "abiq-forecast-side-stack" in js
    assert ".abiq-forecast-side-stack" in css
    assert "renderForecastsBeforeSlateProfile(parentElement, data)" in js


def test_profile_adds_no_private_runtime_or_pool_state() -> None:
    source = PROFILE_JS.read_text(encoding="utf-8") + PROFILE_CSS.read_text(encoding="utf-8")
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


def test_combined_showcase_javascript_parses(tmp_path: Path) -> None:
    bundle = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (BASE_JS, FINAL_JS, PROFILE_JS)
    )
    bundle_path = tmp_path / "showcase_bundle.mjs"
    bundle_path.write_text(bundle, encoding="utf-8")
    subprocess.run(["node", "--check", str(bundle_path)], check=True, capture_output=True, text=True)


def test_profile_assets_are_loaded_by_fresh_component_identity() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert 'name="abiq_public_showcase_v11"' in source
    assert 'key="abiq_public_showcase_v11"' in source
    assert 'slate_confidence_profile.css' in source
    assert 'slate_confidence_profile.js' in source
