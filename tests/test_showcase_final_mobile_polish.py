from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = ROOT / "showcase_v3.py"
HTML = ROOT / "frontend" / "showcase_exec.html"
JS = ROOT / "frontend" / "showcase_exec.js"
MOBILE = ROOT / "frontend" / "mobile_polish.css"


def test_final_mobile_polish_layer_is_mounted() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert 'mobile_polish.css' in source


def test_recruiter_performance_view_replaces_fantasy_with_reliability() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")

    assert "Fantasy challenger materially beat its frozen baseline." not in html
    assert 'id="abiq-reliability-chart"' in html
    assert "CONFIDENCE RELIABILITY" in html

    for expected in (
        '"threshold": "55%+", "games": 213, "predicted": 68.16, "observed": 69.48',
        '"threshold": "60%+", "games": 172, "predicted": 70.79, "observed": 71.51',
        '"threshold": "65%+", "games": 130, "predicted": 73.42, "observed": 74.62',
        '"threshold": "70%+", "games": 82, "predicted": 76.91, "observed": 78.05',
    ):
        assert expected in source


def test_mobile_playbook_and_recommendation_spacing_match_final_qa() -> None:
    css = MOBILE.read_text(encoding="utf-8")
    assert "@media (max-width: 860px)" in css
    assert ".abiq-playbook" in css
    assert "right: -16% !important" in css
    assert "top: 64% !important" in css
    assert "opacity: .54 !important" in css
    assert ".abiq-rec-row" in css
    assert "104px !important" in css
    assert ".abiq-confidence" in css
    assert "width: 100px !important" in css


def test_forecast_team_marks_use_separated_mobile_layout() -> None:
    css = MOBILE.read_text(encoding="utf-8")
    assert ".abiq-logo-pair" in css
    assert "width: 76px !important" in css
    assert "gap: 8px !important" in css
    assert ".abiq-forecast-matchup" in css
    assert "gap: 14px !important" in css
    assert ".abiq-upset-teams img + img" in css
    assert "margin-left: 0 !important" in css


def test_confidence_reliability_is_single_observed_line_visual() -> None:
    css = MOBILE.read_text(encoding="utf-8")
    assert ".abiq-reliability-panel" in css
    assert ".abiq-reliability-legend" in css
    assert "display: none !important" in css
    assert "Forecast confidence threshold" in css
    assert "Observed win %" in css
    assert ".abiq-reliability-chart > *" in css
    assert "display: none !important" in css
    for value in ("69.5%25", "71.5%25", "74.6%25", "78.0%25"):
        assert value in css
