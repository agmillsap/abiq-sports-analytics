from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = ROOT / "showcase_v3.py"
MOBILE = ROOT / "frontend" / "mobile_polish.css"


def test_final_mobile_polish_layer_is_mounted() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert 'mobile_polish.css' in source


def test_recruiter_performance_view_hides_fantasy_holdout() -> None:
    css = MOBILE.read_text(encoding="utf-8")
    assert ".abiq-page-performance > .abiq-takeaway" in css
    assert "display: none !important" in css


def test_mobile_playbook_and_recommendation_spacing_are_strengthened() -> None:
    css = MOBILE.read_text(encoding="utf-8")
    assert "@media (max-width: 860px)" in css
    assert ".abiq-playbook" in css
    assert "opacity: .84 !important" in css
    assert ".abiq-rec-row" in css
    assert "104px !important" in css
    assert ".abiq-confidence" in css
    assert "width: 100px !important" in css


def test_forecast_team_marks_get_more_mobile_breathing_room() -> None:
    css = MOBILE.read_text(encoding="utf-8")
    assert ".abiq-logo-pair" in css
    assert "width: 64px !important" in css
    assert ".abiq-forecast-matchup" in css
    assert "gap: 12px !important" in css
    assert ".abiq-upset-teams img + img" in css
