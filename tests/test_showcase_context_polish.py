from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "frontend" / "showcase_exec.html"
TYPOGRAPHY = ROOT / "frontend" / "typography.css"


def test_dashboard_exposes_static_weather_and_injury_context() -> None:
    html = HTML.read_text(encoding="utf-8")
    assert "STATIC FORECAST CONTEXT" in html
    assert "ILLUSTRATIVE SNAPSHOT" in html
    assert html.count("WEATHER") == 3
    assert html.count("INJURIES") == 3
    assert "Clear · 78° · 6 mph wind" in html
    assert "Rain chance · 12 mph wind" in html
    assert "Dome · conditions stable" in html


def test_mobile_hero_iq_moves_left_and_down() -> None:
    css = TYPOGRAPHY.read_text(encoding="utf-8")
    assert "right: 9% !important" in css
    assert "top: 60% !important" in css
    assert "right: 8% !important" in css
    assert "top: 66% !important" in css


def test_playbook_visibility_is_strengthened_without_layout_change() -> None:
    css = TYPOGRAPHY.read_text(encoding="utf-8")
    assert "opacity: .78 !important" in css
    assert "opacity: .55 !important" in css
    assert "opacity: .50 !important" in css
    assert ".play-primary" in css
    assert ".play-soft" in css
