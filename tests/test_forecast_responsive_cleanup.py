from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V2_JS = ROOT / "frontend" / "forecast_page_v2.js"
V2_CSS = ROOT / "frontend" / "forecast_page_v2.css"


def test_pre_snap_metrics_are_centered_between_label_and_detail() -> None:
    css = V2_CSS.read_text(encoding="utf-8")
    assert "grid-template-rows: auto minmax(38px, 1fr) auto" in css
    assert ".abiq-pre-snap-card > strong" in css
    assert "align-self: center" in css
    assert '"label value"' in css
    assert '"detail value"' in css


def test_full_slate_board_has_no_redundant_probability_meter() -> None:
    js = V2_JS.read_text(encoding="utf-8")
    css = V2_CSS.read_text(encoding="utf-8")
    assert "abiq-full-slate-track" not in js
    assert "abiq-full-slate-fill" not in js
    assert ".abiq-full-slate-track" not in css
    assert ".abiq-full-slate-fill" not in css
    assert "Projected winner" in js
    assert "Win %" in js


def test_board_rows_use_compact_prediction_columns() -> None:
    css = V2_CSS.read_text(encoding="utf-8")
    assert "grid-template-columns: 24px minmax(145px, 1.2fr) 78px 58px 62px" in css
    assert "min-height: 68px" in css
    assert ".abiq-full-slate-pick" in css
    assert ".abiq-full-slate-probability" in css


def test_pressure_map_uses_aligned_desktop_chart_and_read_row() -> None:
    css = V2_CSS.read_text(encoding="utf-8")
    js = V2_JS.read_text(encoding="utf-8")
    assert "grid-template-columns: minmax(0, 1fr)" in css
    assert ".abiq-pressure-reads" in css
    assert "grid-template-columns: repeat(3, minmax(0, 1fr))" in css
    assert "width: min(100%, 1180px)" in css
    assert "layout.appendChild(chart)" in js
    assert "layout.appendChild(renderPressureReads(readItems, 'abiq-pressure-reads'))" in js


def test_mobile_pressure_view_replaces_scatterplot_with_compact_reads() -> None:
    css = V2_CSS.read_text(encoding="utf-8")
    js = V2_JS.read_text(encoding="utf-8")
    assert ".abiq-pressure-mobile-list" in css
    assert "display: none" in css
    assert "#abiq-dashboard-root #page-forecasts .abiq-pressure-layout {\n    display: none;" in css
    assert "#abiq-dashboard-root #page-forecasts .abiq-pressure-mobile-list {\n    display: grid;" in css
    assert "renderPressureReads(readItems, 'abiq-pressure-mobile-list')" in js
