from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TYPOGRAPHY = ROOT / "frontend" / "typography.css"


def test_performance_supporting_copy_uses_larger_desktop_readability_floor() -> None:
    css = TYPOGRAPHY.read_text(encoding="utf-8")
    assert ".abiq-page-performance .abiq-exec-head p" in css
    assert "font-size: 13px !important" in css
    assert ".abiq-page-performance .abiq-performance-disclosure" in css
    assert "font-size: 12.5px !important" in css
    assert ".abiq-page-performance .abiq-metric-detail" in css
    assert ".abiq-page-performance .abiq-metric-label" in css
    assert "font-size: 12px !important" in css


def test_performance_metric_cards_can_grow_instead_of_clipping_larger_copy() -> None:
    css = TYPOGRAPHY.read_text(encoding="utf-8")
    assert "height: auto !important" in css
    assert "min-height: 190px !important" in css
    assert "padding-bottom: 70px !important" in css
    assert "padding-right: 130px !important" in css


def test_performance_charts_and_supporting_sections_are_not_left_at_ten_px() -> None:
    css = TYPOGRAPHY.read_text(encoding="utf-8")
    assert ".abiq-page-performance .abiq-reliability-tick" in css
    assert ".abiq-page-performance .abiq-reliability-value" in css
    assert "font-size: 13.5px !important" in css
    assert ".abiq-page-performance .abiq-chart-note" in css
    assert ".abiq-page-performance .abiq-pipe-copy" in css
    assert ".abiq-page-performance .abiq-story p" in css


def test_mobile_performance_readability_is_raised_without_using_desktop_sizes() -> None:
    css = TYPOGRAPHY.read_text(encoding="utf-8")
    assert "@media (max-width: 860px)" in css
    assert "font-size: 11.5px !important" in css
    assert "min-height: 170px !important" in css
    assert "@media (max-width: 560px)" in css
    assert "min-height: 156px !important" in css
