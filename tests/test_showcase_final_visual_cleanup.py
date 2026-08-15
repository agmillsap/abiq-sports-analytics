from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOBILE = ROOT / "frontend" / "mobile_polish.css"
FINAL_CSS = ROOT / "frontend" / "final_visual_cleanup.css"
FINAL_JS = ROOT / "frontend" / "final_visual_cleanup.js"
SHOWCASE = ROOT / "showcase_v3.py"


def test_mobile_playbook_is_shifted_left_behind_iq() -> None:
    css = FINAL_CSS.read_text(encoding="utf-8")
    assert "right: -2% !important" in css
    assert "right: 2% !important" in css
    assert "width: 92% !important" in css


def test_logo_pairs_are_separated_on_desktop_and_mobile() -> None:
    css = FINAL_CSS.read_text(encoding="utf-8")
    assert ".abiq-logo-pair" in css
    assert "gap: 10px !important" in css
    assert "position: static !important" in css
    assert ".abiq-upset-teams img + img" in css
    assert "margin-left: 0 !important" in css


def test_upset_matrix_labels_render_after_marker_layer() -> None:
    css = FINAL_CSS.read_text(encoding="utf-8")
    js = FINAL_JS.read_text(encoding="utf-8")
    assert "paint-order: stroke fill !important" in css
    assert "font-size: 13.5px !important" in css
    assert "const markerLayer = svgElement('g')" in js
    assert "const labelLayer = svgElement('g')" in js
    assert "svg.append(backgroundLayer, markerLayer, labelLayer)" in js


def test_performance_uses_spacious_observed_win_rate_line_graph() -> None:
    css = FINAL_CSS.read_text(encoding="utf-8")
    js = FINAL_JS.read_text(encoding="utf-8")
    assert ".abiq-reliability-line" in css
    assert "stroke-width: 2" in css
    assert "r: 4.5" in js
    assert "const width = 720" in js
    assert "const height = 380" in js
    assert "Forecast confidence threshold →" in js
    assert "Observed win % →" in js
    assert "predicted" not in js


def test_sidebar_and_temporal_metric_have_non_overlapping_overrides() -> None:
    css = FINAL_CSS.read_text(encoding="utf-8")
    assert ".abiq-brand-meaning" in css
    assert "max-width: none !important" in css
    assert ".abiq-metric-card:nth-child(4)::after" in css
    assert "bottom: 16px !important" in css


def test_lac_probability_uses_half_up_display_rounding() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert "ROUND_HALF_UP" in source
    assert "_display_probability(left_probability)" in source
    assert '"TOP WIN PROBABILITY", "value": "81.1%"' in source


def test_component_identity_is_bumped_for_fresh_deploy() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert 'name="abiq_public_showcase_v8"' in source
    assert 'key="abiq_public_showcase_v8"' in source
    assert 'final_visual_cleanup.css' in source
    assert 'final_visual_cleanup.js' in source
