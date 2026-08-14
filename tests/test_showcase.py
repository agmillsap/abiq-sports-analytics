from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
SHOWCASE = ROOT / "showcase_v3.py"
BASE_CSS = ROOT / "frontend" / "showcase.css"
HTML = ROOT / "frontend" / "showcase_exec.html"
CSS = ROOT / "frontend" / "showcase_exec.css"
JS = ROOT / "frontend" / "showcase_exec.js"
WORDMARK = ROOT / "assets" / "brand" / "abiq_wordmark.webp"
IQ_MARK = ROOT / "assets" / "brand" / "abiq_iq_hero.webp"
BASE_TEXTURE = ROOT / "assets" / "textures" / "abiq_texture_base.webp"
ACCENT_TEXTURE = ROOT / "assets" / "textures" / "abiq_texture_accent.webp"


def _public_source() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in (APP, SHOWCASE, HTML, BASE_CSS, CSS, JS)
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
    assert 'name="abiq_public_showcase_v4"' in source
    assert 'showcase_exec.html' in source
    assert 'showcase_exec.css' in source
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
    for team in ("ARI", "CLE", "DET", "JAX", "LAC", "NO", "PHI", "WAS"):
        assert f'"{team}"' in source
    js = JS.read_text(encoding="utf-8")
    assert "abiq-team-cell" in js
    assert "abiq-rec-team" in js


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
    assert "UPSET WATCH" in source
    assert '"GAMES FORECAST"' in source
    assert '"Risk"' in source
    assert "survivor entries" not in source.casefold()


def test_performance_combines_validation_and_platform_story() -> None:
    html = HTML.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    assert "VALIDATION · ENGINEERING · TRUST" in html
    assert "HOW ABIQ WORKS" in html
    assert 'id="abiq-platform-pipeline"' in html
    assert "renderPipeline(parentElement, data)" in js
    assert "renderPerformance(parentElement, data)" in js


def test_validation_claims_are_locked_in_source() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert '"games": 272' in source
    assert '"winner_accuracy": 0.6605' in source
    assert '"population": 589' in source
    assert '"standard_mae_reduction": 44.8580' in source
    assert '"half_ppr_mae_reduction": 45.4352' in source
    assert '"ppr_mae_reduction": 45.7589' in source
    assert source.count('"temporal_violations": 0') == 2
