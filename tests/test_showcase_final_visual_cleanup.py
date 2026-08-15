from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOBILE = ROOT / "frontend" / "mobile_polish.css"
SHOWCASE = ROOT / "showcase_v3.py"


def test_mobile_playbook_is_centered_behind_iq_and_kept_faint() -> None:
    css = MOBILE.read_text(encoding="utf-8")
    assert "right: -16% !important" in css
    assert "top: 64% !important" in css
    assert "width: 84% !important" in css
    assert "opacity: .54 !important" in css


def test_mobile_logo_pairs_are_separated_not_overlapped() -> None:
    css = MOBILE.read_text(encoding="utf-8")
    assert ".abiq-logo-pair" in css
    assert "gap: 8px !important" in css
    assert "margin: 0 !important" in css
    assert ".abiq-upset-teams" in css
    assert "margin-left: 0 !important" in css


def test_upset_matrix_labels_get_top_layer_halo() -> None:
    css = MOBILE.read_text(encoding="utf-8")
    assert ".abiq-upset-label" in css
    assert "paint-order: stroke fill !important" in css
    assert "stroke-width: 4px !important" in css


def test_performance_uses_observed_win_rate_line_visual_only() -> None:
    css = MOBILE.read_text(encoding="utf-8")
    assert ".abiq-reliability-legend" in css
    assert "display: none !important" in css
    assert "Forecast confidence threshold" in css
    assert "Observed win %" in css
    for value in ("69.5%25", "71.5%25", "74.6%25", "78.0%25"):
        assert value in css


def test_component_identity_is_bumped_for_fresh_deploy() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert 'name="abiq_public_showcase_v7"' in source
    assert 'key="abiq_public_showcase_v7"' in source
