from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL_CSS = ROOT / "frontend" / "final_visual_cleanup.css"


def test_desktop_forecast_read_moves_below_signal_and_confidence() -> None:
    css = FINAL_CSS.read_text(encoding="utf-8")
    assert '"rank matchup signal confidence"' in css
    assert '"rank matchup read read" !important' in css
    assert ".abiq-forecast-read" in css
    assert "grid-area: read !important" in css
    assert "overflow: visible !important" in css
    assert "text-overflow: clip !important" in css


def test_confidence_is_centered_against_probability_signal_block() -> None:
    css = FINAL_CSS.read_text(encoding="utf-8")
    assert ".abiq-forecast-signal" in css
    assert "grid-area: signal !important" in css
    assert ".abiq-forecast-confidence" in css
    assert "grid-area: confidence !important" in css
    assert "align-self: center !important" in css
    assert "justify-self: center !important" in css
