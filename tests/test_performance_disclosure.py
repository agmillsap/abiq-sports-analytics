from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_HTML = ROOT / "frontend" / "showcase_exec.html"


def test_performance_tab_identifies_real_weekly_model_results() -> None:
    html = SHOWCASE_HTML.read_text(encoding="utf-8")
    assert "abiq-performance-disclosure" in html
    assert "Verified performance data." in html
    assert "real, graded ABIQ model outcomes" in html
    assert "refreshed weekly" in html
    assert "actual model performance" in html
