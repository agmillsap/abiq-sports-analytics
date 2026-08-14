from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

COPPER = "#C97A50"
COPPER_BRIGHT = "#D99067"
TEXT = "#F4F0EA"
MUTED = "#9B958D"
PANEL = "#121414"
BORDER = "#292B2B"

WEEK1_SIGNALS = (
    ("LAC", "ARI", 0.8105, 1, "Sun · 4:25 PM ET"),
    ("JAX", "CLE", 0.7584, 2, "Sun · 1:00 PM ET"),
    ("DET", "NO", 0.7174, 3, "Sun · 1:00 PM ET"),
    ("PHI", "WAS", 0.6499, 4, "Sun · 4:25 PM ET"),
    ("CIN", "TB", 0.6377, 5, "Sun · 1:00 PM ET"),
)

NFL_METRICS = {
    "games": 272,
    "weeks": 18,
    "features": 37,
    "winner_accuracy": 0.6605,
    "brier": 0.214355,
    "log_loss": 0.617029,
    "temporal_violations": 0,
}

FANTASY_METRICS = {
    "population": 589,
    "standard_mae_reduction": 44.8580,
    "half_ppr_mae_reduction": 45.4352,
    "ppr_mae_reduction": 45.7589,
    "standard_spearman": 0.7216,
    "half_ppr_spearman": 0.7336,
    "ppr_spearman": 0.7413,
    "temporal_violations": 0,
}

st.set_page_config(
    page_title="ABIQ | Sports Decision Intelligence",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
    .stApp {{ background: #080909; color: {TEXT}; }}
    [data-testid="stSidebar"] {{ background: #0D0F0F; border-right: 1px solid {BORDER}; }}
    [data-testid="stSidebar"] * {{ color: {TEXT}; }}
    .block-container {{ max-width: 1220px; padding-top: 2.2rem; padding-bottom: 3rem; }}
    .abiq-wordmark {{ font-family: Georgia, 'Times New Roman', serif; font-size: 2.15rem; letter-spacing: .12em; font-weight: 600; color: {TEXT}; }}
    .abiq-wordmark span {{ color: {COPPER_BRIGHT}; }}
    .eyebrow {{ color: {COPPER_BRIGHT}; text-transform: uppercase; letter-spacing: .18em; font-size: .66rem; font-weight: 700; }}
    .hero {{ font-family: Georgia, 'Times New Roman', serif; font-size: clamp(2.3rem, 5vw, 4.6rem); line-height: 1.03; letter-spacing: -.035em; color: {TEXT}; margin: .45rem 0 1rem; }}
    .subhead {{ color: {MUTED}; font-size: 1rem; line-height: 1.7; max-width: 800px; }}
    .card {{ background: {PANEL}; border: 1px solid {BORDER}; border-radius: 16px; padding: 20px; min-height: 152px; }}
    .card-label {{ color: {COPPER_BRIGHT}; text-transform: uppercase; letter-spacing: .12em; font-size: .62rem; font-weight: 700; }}
    .card-title {{ font-family: Georgia, 'Times New Roman', serif; font-size: 1.3rem; color: {TEXT}; margin: .48rem 0 .6rem; }}
    .card-body {{ color: {MUTED}; font-size: .78rem; line-height: 1.6; }}
    .metric {{ background: {PANEL}; border: 1px solid {BORDER}; border-radius: 14px; padding: 18px; min-height: 118px; }}
    .metric-value {{ font-family: Georgia, 'Times New Roman', serif; color: {COPPER_BRIGHT}; font-size: 1.65rem; margin-top: .4rem; }}
    .metric-detail {{ color: {MUTED}; font-size: .68rem; line-height: 1.45; margin-top: .35rem; }}
    .section-title {{ font-family: Georgia, 'Times New Roman', serif; font-size: 2rem; color: {TEXT}; margin: .15rem 0 .5rem; }}
    .section-copy {{ color: {MUTED}; line-height: 1.65; max-width: 850px; }}
    .rule {{ height: 1px; background: {BORDER}; margin: 2.1rem 0; }}
    div[data-testid="stAlert"] {{ background: #121414; border-color: #3A302B; }}
    .stRadio label, .stSelectbox label {{ color: {MUTED} !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def wordmark() -> None:
    st.markdown('<div class="abiq-wordmark">AB<span>IQ</span></div>', unsafe_allow_html=True)
    st.caption("Analytics · Balance · Intelligence · Quality")


def header(section: str, title: str, copy: str) -> None:
    st.markdown(f'<div class="eyebrow">{section}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subhead">{copy}</div>', unsafe_allow_html=True)


def section(kicker: str, title: str, copy: str) -> None:
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="eyebrow">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-copy">{copy}</div>', unsafe_allow_html=True)


def card(label: str, title: str, body: str) -> None:
    st.markdown(
        f'<div class="card"><div class="card-label">{label}</div><div class="card-title">{title}</div><div class="card-body">{body}</div></div>',
        unsafe_allow_html=True,
    )


def metric(label: str, value: str, detail: str) -> None:
    st.markdown(
        f'<div class="metric"><div class="card-label">{label}</div><div class="metric-value">{value}</div><div class="metric-detail">{detail}</div></div>',
        unsafe_allow_html=True,
    )


wordmark()
st.sidebar.markdown("---")
st.sidebar.caption("PUBLIC PORTFOLIO SHOWCASE")
page = st.sidebar.radio(
    "Navigation",
    ("Overview", "Weekly Outlook", "Model Performance", "Platform"),
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.caption("Built independently by Abigail Millsap")
st.sidebar.caption("Public view intentionally excludes private user state, credentials, provider secrets, and production operator controls.")

if page == "Overview":
    header(
        "Sports Decision Intelligence",
        "Sports decisions, made clearer.",
        "ABIQ is a football analytics platform that combines predictive modeling, decision optimization, risk context, and product design to turn complex data into understandable choices.",
    )

    cols = st.columns(3)
    with cols[0]:
        card("Decision intelligence", "Survivor", "Balances win probability, uncertainty, multi-entry strategy, and future team value rather than treating each week as an isolated pick.")
    with cols[1]:
        card("Weekly rankings", "Pick'em", "Transforms game probabilities and matchup context into a ranked confidence board designed for fast weekly decisions.")
    with cols[2]:
        card("Validated preseason research", "Fantasy", "A frozen Ridge challenger materially beat a frozen baseline on a protected 2025 established-player holdout across Standard, Half-PPR, and PPR scoring.")

    section(
        "From data to decision",
        "A product system, not a notebook model.",
        "The private ABIQ platform separates collection, point-in-time feature engineering, modeling, optimization, persistence, and presentation. This public repository is a sanitized Showcase boundary rather than a copy of production source code.",
    )
    flow = st.columns(4)
    for col, item in zip(
        flow,
        (
            ("Observe", "Open and governed football data are normalized into reproducible inputs."),
            ("Predict", "Leakage-aware models estimate probabilities and player outcomes while preserving uncertainty."),
            ("Decide", "Decision engines rank choices around the actual product objective, not raw accuracy alone."),
            ("Explain", "Fan-first interfaces show the takeaway first and deeper analytical evidence on demand."),
        ),
    ):
        with col:
            card("Architecture", item[0], item[1])

elif page == "Weekly Outlook":
    header(
        "Decision Surface",
        "Weekly Outlook",
        "A public-safe example of how ABIQ reduces a full NFL slate to a short comparison a fan can act on quickly.",
    )
    st.info("Preseason planning example — not a final Week 1 production issuance. The displayed probability signals use preseason/prior-season context and include historical market-derived inputs whose live decision-horizon timing has not been production-validated.")

    teams = [row[0] for row in WEEK1_SIGNALS]
    probabilities = [row[2] * 100 for row in WEEK1_SIGNALS]
    opponents = [row[1] for row in WEEK1_SIGNALS]
    fig = go.Figure(
        go.Bar(
            x=list(reversed(probabilities)),
            y=[f"{team} vs {opp}" for team, opp in reversed(list(zip(teams, opponents)))],
            orientation="h",
            text=[f"{p:.1f}%" for p in reversed(probabilities)],
            textposition="outside",
            marker_color=COPPER_BRIGHT,
            hovertemplate="%{y}<br>Planning signal: %{x:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        height=360,
        margin=dict(l=10, r=60, t=20, b=35),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT),
        xaxis=dict(title="Current preseason planning signal", ticksuffix="%", range=[0, 100], gridcolor="rgba(255,255,255,.08)"),
        yaxis=dict(title="", gridcolor="rgba(0,0,0,0)"),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    cols = st.columns(5)
    for col, (team, opponent, probability, rank, kickoff) in zip(cols, WEEK1_SIGNALS):
        with col:
            card(f"Rank #{rank}", f"{team} vs {opponent}", f"{probability:.1%} planning signal · {kickoff}")

    with st.expander("Why this is labeled a planning example"):
        st.write("The Showcase separates product-design examples from validated historical model claims. Current preseason rankings demonstrate the interface and decision workflow; the Model Performance page contains the evidence used for model-validation claims.")

elif page == "Model Performance":
    header(
        "Validation & Trust",
        "Evidence before confidence.",
        "ABIQ uses point-in-time replay, frozen baselines, and explicit leakage controls so model claims reflect information that could actually have been available when a prediction was made.",
    )

    st.markdown("### NFL game model · 2025 point-in-time replay")
    cols = st.columns(4)
    with cols[0]:
        metric("Regular season", "272 games", "18-week expanding historical replay")
    with cols[1]:
        metric("Winner accuracy", "66.05%", "179 of 271 non-tie game winners")
    with cols[2]:
        metric("Probability quality", "0.2144 Brier", "Market-free frozen logistic champion")
    with cols[3]:
        metric("Temporal integrity", "0 violations", "37 prediction-time football features")

    section(
        "Fantasy holdout",
        "The challenger had to beat a frozen baseline.",
        "Before 2025 results were revealed, ABIQ froze a position-specific StandardScaler + Ridge(alpha=10) challenger and a separate baseline. The single-shot holdout compared the same 589 established-player population across all three scoring formats.",
    )
    cols = st.columns(3)
    with cols[0]:
        metric("Standard", "44.86% lower MAE", "Ridge rank correlation: 0.722")
    with cols[1]:
        metric("Half-PPR", "45.44% lower MAE", "Ridge rank correlation: 0.734")
    with cols[2]:
        metric("PPR", "45.76% lower MAE", "Ridge rank correlation: 0.741")

    st.success("The frozen Ridge challenger passed the established-player preseason challenger gate with zero temporal violations across Standard, Half-PPR, and PPR.")
    st.caption("Scope matters: this does not declare the full Fantasy product production-ready. Rookies/new entrants and weekly start/sit validation remain separate research tracks, and 2025 is not reused for post-reveal hyperparameter tuning.")

elif page == "Platform":
    header(
        "Built End to End",
        "Analytics engineered into a product.",
        "The private ABIQ system combines data pipelines, model governance, automated operations, persistence, and decision-focused UX. The public Showcase exposes the engineering story without exposing the private production boundary.",
    )

    cols = st.columns(2)
    pillars = (
        ("Point-in-time modeling", "Historical replays enforce prediction cutoffs so future outcomes and later information do not leak into model inputs."),
        ("Champion / challenger governance", "New approaches are tested against frozen baselines and require explicit promotion instead of silently replacing a working model."),
        ("Automated operations", "GitHub Actions orchestrate data refreshes, validation checks, semantic audits, and fail-safe operating paths."),
        ("Resilient product architecture", "Prediction generation, decision optimization, persistence, and UI presentation are separated so failures can degrade safely."),
        ("Cost-aware data engineering", "Routine tests use fixtures, mocks, and cached data rather than consuming limited live provider credits."),
        ("Fan-first product design", "Interfaces prioritize the decision and its supporting evidence instead of exposing every available statistic by default."),
    )
    for index, (title, body) in enumerate(pillars):
        with cols[index % 2]:
            card("Engineering principle", title, body)

    section(
        "Technology",
        "Python · Streamlit · scikit-learn · GitHub Actions · Supabase",
        "The production platform also uses persistent cloud state, scheduled workflows, point-in-time feature generation, champion/challenger model controls, caching, and explicit degraded-mode behavior. Private implementation details and credentials are intentionally excluded from this public repository.",
    )

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.caption("ABIQ · Analytics. Balance. Intelligence. Quality. · Smarter decisions through analytics.")
st.caption("Portfolio Showcase built by Abigail Millsap. Historical performance does not guarantee future results.")
