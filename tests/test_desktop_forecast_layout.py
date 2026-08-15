from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_HTML = ROOT / "frontend" / "showcase_exec.html"


def test_standard_desktop_forecasts_stack_to_prevent_clipping() -> None:
    html = SHOWCASE_HTML.read_text(encoding="utf-8")
    assert "@media (min-width: 861px) and (max-width: 1680px)" in html
    assert "#page-forecasts .abiq-forecast-visual-grid" in html
    assert "grid-template-columns: 1fr !important" in html


def test_ultrawide_forecasts_keep_weighted_two_column_layout() -> None:
    html = SHOWCASE_HTML.read_text(encoding="utf-8")
    assert "@media (min-width: 1681px)" in html
    assert "minmax(0, 1.3fr) minmax(420px, .7fr)" in html


def test_performance_disclosure_is_evenly_spaced_between_panels() -> None:
    html = SHOWCASE_HTML.read_text(encoding="utf-8")
    assert ".abiq-page-performance > .abiq-page-head" in html
    assert "margin-bottom: 0 !important" in html
    assert ".abiq-performance-disclosure" in html
    assert "margin: 12px auto !important" in html


def test_mobile_forecast_structure_is_not_overridden() -> None:
    html = SHOWCASE_HTML.read_text(encoding="utf-8")
    mobile_block = html.split("@media (max-width: 860px)", 1)[1].split("</style>", 1)[0]
    assert ".abiq-forecast" not in mobile_block
