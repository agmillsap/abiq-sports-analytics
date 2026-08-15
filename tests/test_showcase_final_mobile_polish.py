from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = ROOT / "showcase_v3.py"
HTML = ROOT / "frontend" / "showcase_exec.html"
FINAL_CSS = ROOT / "frontend" / "final_visual_cleanup.css"
FINAL_JS = ROOT / "frontend" / "final_visual_cleanup.js"


def test_final_mobile_polish_layers_are_mounted() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert 'mobile_polish.css' in source
    assert 'final_visual_cleanup.css' in source
    assert 'final_visual_cleanup.js' in source


def test_recruiter_performance_view_replaces_fantasy_with_reliability() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    js = FINAL_JS.read_text(encoding="utf-8")

    assert "Fantasy challenger materially beat its frozen baseline." not in html
    assert 'id="abiq-reliability-chart"' in html
    assert "CONFIDENCE RELIABILITY" in html
    assert "renderReliability = function" in js

    for expected in (
        '"threshold": "55%+", "games": 213, "predicted": 68.16, "observed": 69.48',
        '"threshold": "60%+", "games": 172, "predicted": 70.79, "observed": 71.51',
        '"threshold": "65%+", "games": 130, "predicted": 73.42, "observed": 74.62',
        '"threshold": "70%+", "games": 82, "predicted": 76.91, "observed": 78.05',
    ):
        assert expected in source


def test_mobile_playbook_is_shifted_left_without_changing_copy_layer() -> None:
    css = FINAL_CSS.read_text(encoding="utf-8")
    assert "@media (max-width: 860px)" in css
    assert ".abiq-playbook" in css
    assert "right: -2% !important" in css
    assert "right: 2% !important" in css
    assert "width: 92% !important" in css


def test_forecast_team_marks_are_separated_on_mobile() -> None:
    css = FINAL_CSS.read_text(encoding="utf-8")
    assert ".abiq-logo-pair" in css
    assert "gap: 10px !important" in css
    assert "gap: 9px !important" in css
    assert ".abiq-upset-teams img + img" in css
    assert "margin-left: 0 !important" in css


def test_confidence_reliability_is_single_observed_line_visual() -> None:
    css = FINAL_CSS.read_text(encoding="utf-8")
    js = FINAL_JS.read_text(encoding="utf-8")
    assert ".abiq-reliability-line" in css
    assert "renderReliability = function" in js
    assert "Forecast confidence threshold →" in js
    assert "Observed win % →" in js
    assert "point.observed" in js
