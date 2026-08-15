from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
SHOWCASE = ROOT / "showcase_v3.py"
README = ROOT / "README.md"
BASE_CSS = ROOT / "frontend" / "showcase.css"
HTML = ROOT / "frontend" / "showcase_exec.html"
CSS = ROOT / "frontend" / "showcase_exec.css"
TYPOGRAPHY = ROOT / "frontend" / "typography.css"
JS = ROOT / "frontend" / "showcase_exec.js"
WORDMARK = ROOT / "assets" / "brand" / "abiq_wordmark.webp"
IQ_MARK = ROOT / "assets" / "brand" / "abiq_iq_hero.webp"
BASE_TEXTURE = ROOT / "assets" / "textures" / "abiq_texture_base.webp"
ACCENT_TEXTURE = ROOT / "assets" / "textures" / "abiq_texture_accent.webp"


def _public_source() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in (APP, SHOWCASE, HTML, BASE_CSS, CSS, TYPOGRAPHY, JS)
    )


def test_public_app_contains_no_private_runtime_hooks() -> None:
    source = _public_source()
    forbidden = (
        "st.secrets",
        "SUPABASE_",
        "StateStore",
        "st.login",
        "st.logout",
        "ACCESS_CODE",
        "survivor.storage",
        "survivor.state",
        "nfl-survivor-command-center",
    )
    for token in forbidden:
        assert token not in source


def test_public_app_compiles_and_runs() -> None:
    compile(APP.read_text(encoding="utf-8"), "app.py", "exec")
    compile(SHOWCASE.read_text(encoding="utf-8"), "showcase_v3.py", "exec")
    app = AppTest.from_file(APP, default_timeout=20).run()
    assert not app.exception


def test_showcase_uses_streamlit_v2_component_contract() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert "st.components.v2.component(" in source
    assert 'name="abiq_public_showcase_v6"' in source
    assert 'key="abiq_public_showcase_v6"' in source
    assert 'showcase_exec.html' in source
    assert 'showcase_exec.css' in source
    assert 'typography.css' in source
    assert 'showcase_exec.js' in source
    assert "isolate_styles=True" in source
    assert 'height="content"' in source
    assert 'base_texture_data_uri' in source
    assert 'accent_texture_data_uri' in source


def test_component_reuses_abiq_material_runtime() -> None:
    base_css = BASE_CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    assert 'id="abiq-dashboard-root" class="abiq-app"' in html
    assert "--base-texture:none" in base_css
    assert "--accent-texture:none" in base_css
    assert "var(--base-texture)" in base_css
    assert "var(--accent-texture)" in base_css
    assert "setProperty('--base-texture'" in js
    assert "setProperty('--accent-texture'" in js
    assert ".abiq-kpi:last-child{grid-column:1/-1}" in base_css


def test_high_fidelity_assets_and_material_textures_are_packaged() -> None:
    assert WORDMARK.exists() and WORDMARK.stat().st_size > 5000
    assert IQ_MARK.exists() and IQ_MARK.stat().st_size > 5000
    assert BASE_TEXTURE.exists() and BASE_TEXTURE.stat().st_size > 4000
    assert ACCENT_TEXTURE.exists() and ACCENT_TEXTURE.stat().st_size > 4000


def test_static_team_logo_treatment_matches_private_product_pattern() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert "https://a.espncdn.com/i/teamlogos/nfl/500/" in source
    for team in ("ARI", "CIN", "CLE", "DET", "JAX", "LAC", "NO", "PHI", "TB", "WAS"):
        assert f'"{team}"' in source
    js = JS.read_text(encoding="utf-8")
    assert "abiq-team-cell" in js
    assert "abiq-rec-team" in js
    assert "abiq-logo-pair" in js


def test_showcase_is_exactly_three_executive_pages() -> None:
    html = HTML.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    for page in ("Dashboard", "Forecasts", "Performance"):
        assert f'data-page="{page}"' in html
        assert f'["{page}",' in js
    for retired_page in ("Weekly Outlook", "Model Performance", "Platform"):
        assert f'data-page="{retired_page}"' not in html
        assert f'["{retired_page}",' not in js


def test_secondary_page_headers_use_iq_watermark_treatment() -> None:
    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    assert html.count('class="abiq-page-watermark"') == 2
    assert ".abiq-page-watermark" in css
    assert "opacity: .12" in css
    assert "width: min(46%, 430px)" in css
    assert "@media (max-width: 860px)" in css
    assert "opacity: .10" in css


def test_public_framing_centers_forecasting_not_survivor_strategy() -> None:
    source = _public_source()
    assert "WEEKLY FORECAST · RISK INTELLIGENCE" in source
    assert "UPSET ALERTS" in source
    assert '"GAMES FORECAST"' in source
    assert '"Risk"' in source
    assert "survivor entries" not in source.casefold()


def test_forecasts_page_uses_visual_decision_surfaces() -> None:
    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    for element_id in ("abiq-forecast-board", "abiq-upset-matrix", "abiq-upset-alerts"):
        assert f'id="{element_id}"' in html
    assert "renderForecastBoard(parentElement, data)" in js
    assert "renderUpsetMatrix(parentElement, data)" in js
    assert "renderUpsetAlerts(parentElement, data)" in js
    assert "200 - 2 * probability" in js
    assert "createElementNS" in js
    assert ".abiq-forecast-visual-grid" in css
    assert ".abiq-upset-alert-grid" in css
    assert ".abiq-upset-dot.high" in css
    assert "not a betting edge or a separate live model" in html
    assert "plotly" not in _public_source().casefold()


def test_new_forecast_visual_text_respects_readability_floor() -> None:
    css = CSS.read_text(encoding="utf-8")
    for selector in (
        ".abiq-visual-heading > span",
        ".abiq-forecast-matchup span",
        ".abiq-forecast-signal-top span",
        ".abiq-forecast-confidence",
        ".abiq-chart-tick",
        ".abiq-chart-note",
        ".abiq-upset-tier",
        ".abiq-upset-meta",
    ):
        assert selector in css
    assert "font-size: 10px" in css
    assert "font-size: 10.5px" in css


def test_public_showcase_weekly_football_data_is_frozen() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    assert '"current_week": 1' in source
    assert '"weeks": [{"week": 1, "label": "2026 · Week 1"}]' in source
    assert "football/team content is intentionally frozen" in source
    assert "not a weekly data feed" in readme
    assert "Only accepted historical model-performance evidence may be updated" in readme

    workflow_files = list((ROOT / ".github" / "workflows").glob("*.yml"))
    workflow_files += list((ROOT / ".github" / "workflows").glob("*.yaml"))
    for workflow_file in workflow_files:
        workflow_text = workflow_file.read_text(encoding="utf-8").casefold()
        assert "schedule:" not in workflow_text
        assert "cron:" not in workflow_text


def test_performance_combines_validation_and_platform_story() -> None:
    html = HTML.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    assert "VALIDATION · ENGINEERING · TRUST" in html
    assert "HOW ABIQ WORKS" in html
    assert 'id="abiq-platform-pipeline"' in html
    assert "renderPipeline(parentElement, data)" in js
    assert "renderPerformance(parentElement, data)" in js


def test_showcase_typography_has_10px_readability_floor() -> None:
    css = TYPOGRAPHY.read_text(encoding="utf-8")
    assert "font-size: 10px !important" in css
    for selector in (
        ".abiq-kpi-title",
        ".abiq-kpi-sub",
        ".abiq-panel-heading",
        ".abiq-team-prob",
        ".abiq-kickoff",
        ".abiq-rec-sub",
        ".abiq-confidence span",
        ".abiq-page-head p",
        ".abiq-metric-label",
        ".abiq-metric-detail",
    ):
        assert selector in css


def test_performance_workflow_headers_have_stronger_hierarchy() -> None:
    css = TYPOGRAPHY.read_text(encoding="utf-8")
    assert ".abiq-pipe-num" in css
    assert "font-size: 11.5px !important" in css
    assert "font-weight: 650" in css
    assert ".abiq-pipe-copy" in css
    assert "font-size: 11px !important" in css


def test_dashboard_uses_interpretable_brier_probability_quality_kpi() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert '"title": "PROBABILITY QUALITY", "value": "0.2144"' in source
    assert '"subtext": "Brier score · 0 perfect / 1 maximum inaccuracy"' in source
    assert "Brier score measures how accurate the model's predicted probabilities are." in source
    assert "0 is perfect and 1 represents maximum inaccuracy" in source
    assert "Confidently wrong forecasts are penalized more severely than cautious misses." in source


def test_validation_claims_are_locked_in_source() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert '"games": 272' in source
    assert '"winner_accuracy": 0.6605' in source
    assert '"population": 589' in source
    assert '"standard_mae_reduction": 44.8580' in source
    assert '"half_ppr_mae_reduction": 45.4352' in source
    assert '"ppr_mae_reduction": 45.7589' in source
    assert source.count('"temporal_violations": 0') == 2
