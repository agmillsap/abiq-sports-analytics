from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_HTML = ROOT / "frontend" / "showcase_exec.html"
DESKTOP_CSS = ROOT / "frontend" / "desktop_forecast_balance.css"


def test_desktop_forecasts_use_weighted_side_by_side_layout() -> None:
    css = DESKTOP_CSS.read_text(encoding="utf-8")
    assert "@media (min-width: 1280px)" in css
    assert "#abiq-dashboard-root #page-forecasts .abiq-forecast-visual-grid" in css
    assert "minmax(0, 2fr) minmax(390px, .8fr)" in css
    assert "align-items: start !important" in css


def test_desktop_winner_rows_are_compacted_to_fit_inside_card() -> None:
    css = DESKTOP_CSS.read_text(encoding="utf-8")
    assert '"rank matchup signal confidence"' in css
    assert '"rank matchup read read"' in css
    assert "28px minmax(155px, .95fr) minmax(150px, 1.05fr) 72px" in css
    assert "width: 68px !important" in css
    assert "overflow-wrap: anywhere !important" in css


def test_narrower_matrix_avoids_tall_empty_panel_and_keeps_labels_readable() -> None:
    css = DESKTOP_CSS.read_text(encoding="utf-8")
    assert "min-height: 250px !important" in css
    assert ".abiq-chart-tick" in css
    assert "font-size: 15px !important" in css
    assert ".abiq-chart-axis-label" in css
    assert "font-size: 16px !important" in css


def test_performance_disclosure_is_evenly_spaced_between_panels() -> None:
    html = SHOWCASE_HTML.read_text(encoding="utf-8")
    assert ".abiq-page-performance > .abiq-page-head" in html
    assert "margin-bottom: 0 !important" in html
    assert ".abiq-performance-disclosure" in html
    assert "margin: 12px auto !important" in html


def test_new_desktop_balance_does_not_override_mobile_forecast_layout() -> None:
    css = DESKTOP_CSS.read_text(encoding="utf-8")
    assert "@media (max-width: 860px)" not in css
