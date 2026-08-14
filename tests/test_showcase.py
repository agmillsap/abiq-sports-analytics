from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"


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
    )
    for token in forbidden:
        assert token not in source


def test_public_app_compiles() -> None:
    compile(APP.read_text(encoding="utf-8"), "app.py", "exec")


def test_public_app_runtime_and_navigation() -> None:
    app = AppTest.from_file(APP, default_timeout=20).run()
    assert not app.exception
    assert app.radio

    for page in ("Weekly Outlook", "Model Performance", "Platform"):
        app.radio[0].set_value(page)
        app.run(timeout=20)
        assert not app.exception


def test_validation_claims_are_locked_in_source() -> None:
    source = APP.read_text(encoding="utf-8")
    assert '"games": 272' in source
    assert '"winner_accuracy": 0.6605' in source
    assert '"population": 589' in source
    assert '"standard_mae_reduction": 44.8580' in source
    assert '"half_ppr_mae_reduction": 45.4352' in source
    assert '"ppr_mae_reduction": 45.7589' in source
    assert '"temporal_violations": 0' in source
