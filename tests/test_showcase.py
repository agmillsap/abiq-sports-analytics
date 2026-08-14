from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
SHOWCASE = ROOT / "showcase_v2.py"
WORDMARK = ROOT / "assets" / "brand" / "abiq_wordmark.webp"
IQ_MARK = ROOT / "assets" / "brand" / "abiq_iq_hero.webp"
STONE = ROOT / "assets" / "textures" / "abiq_stone_smooth.webp"


def _public_source() -> str:
    return APP.read_text(encoding="utf-8") + SHOWCASE.read_text(encoding="utf-8")


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
    compile(SHOWCASE.read_text(encoding="utf-8"), "showcase_v2.py", "exec")
    app = AppTest.from_file(APP, default_timeout=20).run()
    assert not app.exception


def test_showcase_uses_abiq_parity_shell() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert 'id="dashboard" class="page active"' in source
    assert "Edge comes from<br>process, not predictions." in source
    assert "Model Recommendations" in source
    assert "Static portfolio example" in source
    assert "Analytics engineered into a product" in source
    assert 'class="hero-iq"' in source
    assert '.hero-iq{width:155px;right:2%;opacity:.74}' in source
    assert '.kpi:last-child{grid-column:1/-1}' in source


def test_high_fidelity_brand_assets_are_packaged() -> None:
    assert WORDMARK.exists() and WORDMARK.stat().st_size > 5000
    assert IQ_MARK.exists() and IQ_MARK.stat().st_size > 5000
    assert STONE.exists() and STONE.stat().st_size > 500


def test_static_team_logo_treatment_matches_private_product_pattern() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert "https://a.espncdn.com/i/teamlogos/nfl/500/" in source
    for team in ("ARI", "CLE", "DET", "JAX", "LAC", "NO", "PHI", "WAS"):
        assert f'"{team}"' in source
    assert 'class="team-logo"' in source
    assert 'class="rec-logo"' in source


def test_secondary_pages_have_explicit_backfill_and_contrast() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert ".surface-alt{" in source
    assert ".pipe{" in source
    assert ".pipe:nth-child(even)" in source
    assert "surface-alt" in source


def test_streamlit_chrome_is_suppressed_where_platform_allows() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert '[data-testid="stToolbar"]' in source
    assert '[data-testid="stStatusWidget"]' in source
    assert "stDeployButton" in source


def test_validation_claims_are_locked_in_source() -> None:
    source = SHOWCASE.read_text(encoding="utf-8")
    assert '"games": 272' in source
    assert '"winner_accuracy": 0.6605' in source
    assert '"population": 589' in source
    assert '"standard_mae_reduction": 44.8580' in source
    assert '"half_ppr_mae_reduction": 45.4352' in source
    assert '"ppr_mae_reduction": 45.7589' in source
    assert source.count('"temporal_violations": 0') == 2
