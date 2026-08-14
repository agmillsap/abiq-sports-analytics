from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
WORDMARK = ROOT / "assets" / "abiq_wordmark.svg"
IQ_MARK = ROOT / "assets" / "abiq_iq.svg"


def test_public_app_contains_no_private_runtime_hooks() -> None:
    source = APP.read_text(encoding="utf-8")
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
    source = APP.read_text(encoding="utf-8")
    compile(source, "app.py", "exec")
    app = AppTest.from_file(APP, default_timeout=20).run()
    assert not app.exception


def test_showcase_uses_branded_custom_shell() -> None:
    source = APP.read_text(encoding="utf-8")
    assert 'id="dashboard" class="page active"' in source
    assert "Edge comes from process" in source
    assert "Model Recommendations" in source
    assert "Static portfolio example" in source
    assert "Model Performance" in source
    assert "Analytics engineered into a product" in source
    assert WORDMARK.exists()
    assert IQ_MARK.exists()


def test_brand_assets_are_original_public_safe_svg_assets() -> None:
    wordmark = WORDMARK.read_text(encoding="utf-8")
    iq_mark = IQ_MARK.read_text(encoding="utf-8")
    assert "ABIQ wordmark" in wordmark
    assert "linearGradient" in wordmark
    assert "ABIQ IQ mark" in iq_mark
    assert "linearGradient" in iq_mark


def test_validation_claims_are_locked_in_source() -> None:
    source = APP.read_text(encoding="utf-8")
    assert '"games": 272' in source
    assert '"winner_accuracy": 0.6605' in source
    assert '"population": 589' in source
    assert '"standard_mae_reduction": 44.8580' in source
    assert '"half_ppr_mae_reduction": 45.4352' in source
    assert '"ppr_mae_reduction": 45.7589' in source
    assert source.count('"temporal_violations": 0') == 2
