from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TYPOGRAPHY = ROOT / "frontend" / "typography.css"
FINAL_CSS = ROOT / "frontend" / "final_visual_cleanup.css"
FINAL_JS = ROOT / "frontend" / "final_visual_cleanup.js"
SHOWCASE = ROOT / "showcase_v3.py"


def test_performance_visuals_use_only_locked_public_metrics() -> None:
    css = TYPOGRAPHY.read_text(encoding="utf-8")
    source = SHOWCASE.read_text(encoding="utf-8")

    assert "conic-gradient(#dc8d5e 0 66.05%" in css
    assert "left: 21.44%" in css
    assert 'content: "18 WEEKS"' in css
    assert 'content: "37 FEATURES"' in css

    assert '"value": "66.05%"' in source
    assert '"value": "0.2144"' in source
    assert '"value": "272 games"' in source
    assert '"value": "0 violations"' in source


def test_performance_visuals_preserve_mobile_readability() -> None:
    css = TYPOGRAPHY.read_text(encoding="utf-8")
    final_css = FINAL_CSS.read_text(encoding="utf-8")

    assert ".abiq-page-performance #abiq-performance-metrics" in css
    assert "@media (max-width: 860px)" in css
    assert "@media (max-width: 560px)" in css
    assert "grid-template-columns: 1fr" in css
    assert "font-size: 10px" in css
    assert ".abiq-reliability-svg" in final_css


def test_performance_visuals_do_not_add_chart_dependencies() -> None:
    public_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            ROOT / "showcase_v3.py",
            ROOT / "frontend" / "showcase_exec.html",
            ROOT / "frontend" / "showcase_exec.js",
            ROOT / "frontend" / "showcase_exec.css",
            ROOT / "frontend" / "typography.css",
            FINAL_CSS,
            FINAL_JS,
        )
    ).casefold()

    for dependency in ("plotly", "chart.js", "highcharts", "d3.js"):
        assert dependency not in public_source
