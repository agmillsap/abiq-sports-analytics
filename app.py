from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent

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

WEEK1_SIGNALS = (
    ("LAC", "ARI", 0.8105, 0.1812, 1, "Sun · 4:25 PM ET"),
    ("JAX", "CLE", 0.7584, 0.2318, 2, "Sun · 1:00 PM ET"),
    ("DET", "NO", 0.7174, 0.2711, 3, "Sun · 1:00 PM ET"),
    ("PHI", "WAS", 0.6499, 0.3386, 4, "Sun · 4:25 PM ET"),
    ("CIN", "TB", 0.6377, 0.3514, 5, "Sun · 1:00 PM ET"),
)


def _asset_data_uri(name: str) -> str:
    path = ROOT / "assets" / name
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


WORDMARK_URI = _asset_data_uri("abiq_wordmark.svg")
IQ_URI = _asset_data_uri("abiq_iq.svg")

st.set_page_config(
    page_title="ABIQ | Sports Decision Intelligence",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      [data-testid="stSidebar"], [data-testid="stHeader"], #MainMenu, footer {display:none !important;}
      .stApp {background:#050606 !important;}
      .block-container {max-width:none !important; padding:0 !important; margin:0 !important;}
      iframe {display:block; border:0 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{
  --copper:#c6784c;
  --copper-bright:#dc8d5e;
  --copper-soft:#a75c39;
  --copper-deep:#704027;
  --black:#070808;
  --panel:#131515;
  --panel-2:#181a1a;
  --border:#353737;
  --border-soft:#262828;
  --text:#e3ddd5;
  --muted:#9b958e;
  --dim:#716c66;
  --noise:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.74' numOctaves='4' seed='29' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.36'/%3E%3C/svg%3E");
}}
*{{box-sizing:border-box}}
html,body{{margin:0;min-height:100%;background:#050606;color:var(--text);font-family:"Avenir Next",Avenir,"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}}
button,select{{font:inherit}}
button{{cursor:pointer}}
.shell{{min-height:1010px;display:grid;grid-template-columns:252px minmax(0,1fr);gap:11px;padding:10px;background:radial-gradient(ellipse at 78% 3%,rgba(198,120,76,.075),transparent 31%),radial-gradient(ellipse at 12% 75%,rgba(255,255,255,.028),transparent 28%),var(--noise),linear-gradient(145deg,#060707,#0b0c0c 52%,#060707)}}
.sidebar,.main{{border:1px solid #303232;background:radial-gradient(ellipse at 30% 5%,rgba(255,255,255,.04),transparent 27%),var(--noise),linear-gradient(160deg,rgba(17,19,19,.98),rgba(8,9,9,.98));box-shadow:0 22px 60px rgba(0,0,0,.22)}}
.sidebar{{border-radius:11px;min-height:990px;display:flex;flex-direction:column;overflow:hidden}}
.brand{{padding:27px 24px 21px;border-bottom:1px solid var(--border-soft)}}
.brand img{{width:100%;max-width:172px;display:block;margin:0 auto}}
.brand-meaning{{margin:9px auto 0;display:flex;flex-wrap:wrap;justify-content:center;gap:4px 7px;color:#89847d;font-size:7.2px;line-height:1.35;letter-spacing:.17em;font-weight:650}}
.brand-meaning b{{color:var(--copper);font-weight:400}}
.nav{{padding:15px 13px;display:grid;gap:4px}}
.nav-button{{height:55px;width:100%;display:flex;align-items:center;gap:13px;padding:0 14px;border:1px solid transparent;border-left:3px solid transparent;border-radius:7px;background:transparent;color:#bbb5ae;text-align:left;font-size:12px;letter-spacing:.01em;transition:.18s ease}}
.nav-button:hover{{background:rgba(255,255,255,.025);color:#e0dad2}}
.nav-button.active{{border-color:rgba(198,120,76,.36);border-left-color:var(--copper-bright);background:linear-gradient(90deg,rgba(198,120,76,.11),rgba(255,255,255,.025));color:#e8e1d8}}
.nav-icon{{width:25px;height:25px;display:grid;place-items:center;color:#aaa49d;font-size:17px}}
.nav-button.active .nav-icon{{color:var(--copper-bright)}}
.profile{{margin:auto 20px 18px;padding-top:17px;border-top:1px solid var(--border-soft);display:grid;grid-template-columns:38px 1fr;gap:10px;align-items:center}}
.avatar{{width:38px;height:38px;border:1px solid var(--copper);border-radius:50%;display:grid;place-items:center;color:var(--copper-bright);font-size:11px;letter-spacing:.06em}}
.profile-name{{font-size:12px;color:#b6b0a8}}
.profile-sub{{margin-top:3px;color:#6f6b65;font-size:9px;letter-spacing:.08em;text-transform:uppercase}}
.main{{border-radius:11px;min-width:0;padding:0 22px 23px;overflow:hidden}}
.header{{min-height:96px;display:flex;align-items:center;justify-content:space-between;gap:18px;padding:0 10px}}
.greeting{{font-family:Georgia,"Times New Roman",serif;font-size:20px;color:#ded8d0;letter-spacing:-.018em}}
.greeting-sub{{margin-top:5px;color:#8e8982;font-size:11px}}
.header-actions{{display:flex;align-items:center;gap:9px}}
.showcase-pill{{height:31px;padding:0 11px;display:flex;align-items:center;border:1px solid rgba(198,120,76,.4);border-radius:999px;color:#c87a4d;background:rgba(198,120,76,.055);font-size:8px;letter-spacing:.14em;font-weight:700;text-transform:uppercase}}
.week-control{{position:relative;min-width:225px;height:42px;display:flex;align-items:center;border:1px solid #313434;border-radius:6px;background:linear-gradient(145deg,rgba(22,24,24,.96),rgba(11,12,12,.96))}}
.week-control select{{width:100%;height:100%;padding:0 34px 0 15px;appearance:none;border:0;outline:0;background:transparent;color:#c7c1b9;font-size:11px}}
.chev{{position:absolute;right:12px;color:#8e8982;pointer-events:none}}
.page{{display:none;animation:fade .2s ease}}
.page.active{{display:block}}
@keyframes fade{{from{{opacity:.55;transform:translateY(3px)}}to{{opacity:1;transform:none}}}}
.surface{{position:relative;overflow:hidden;border:1px solid var(--border);background:radial-gradient(ellipse at 12% 7%,rgba(255,255,255,.05),transparent 30%),radial-gradient(ellipse at 88% 83%,rgba(198,120,76,.04),transparent 31%),var(--noise),linear-gradient(145deg,#181a1a,#111313 49%,#171919);box-shadow:inset 0 1px 0 rgba(255,255,255,.015),0 14px 34px rgba(0,0,0,.15)}}
.hero{{height:252px;border-radius:13px;display:flex;align-items:center;padding:28px 34px;background:radial-gradient(ellipse at 82% 16%,rgba(198,120,76,.145),transparent 31%),radial-gradient(ellipse at 63% 91%,rgba(255,255,255,.04),transparent 29%),var(--noise),linear-gradient(106deg,#111313,#171818 48%,#2a231f)}}
.hero-copy{{position:relative;z-index:5;width:52%}}
.eyebrow{{color:var(--copper-bright);font-size:8.5px;letter-spacing:.19em;font-weight:750;text-transform:uppercase}}
.hero h1,.page-title{{font-family:Georgia,"Times New Roman",serif;font-weight:400;color:#e5dfd6;letter-spacing:-.028em}}
.hero h1{{margin:10px 0 0;font-size:33px;line-height:1.08}}
.hero p{{max-width:500px;margin:13px 0 0;color:#aba59e;font-size:11.5px;line-height:1.58}}
.outline-button{{margin-top:16px;height:37px;padding:0 14px;display:inline-flex;align-items:center;gap:18px;border:1px solid #8d4f31;border-radius:5px;background:rgba(11,12,12,.38);color:var(--copper-bright);font-size:8px;letter-spacing:.15em;font-weight:700}}
.playbook{{position:absolute;z-index:1;right:5px;top:4px;width:56%;height:245px;opacity:.55;mix-blend-mode:screen}}
.playbook svg{{width:100%;height:100%}}
.play-line,.play-circle,.play-x path{{stroke:#8d8982;fill:none;stroke-width:1.5;opacity:.42}}
.play-soft{{opacity:.23}} .play-copper{{stroke:#aa6540;opacity:.64}}
.hero-iq{{position:absolute;z-index:4;right:10%;top:50%;transform:translateY(-50%);width:192px;opacity:.94;filter:drop-shadow(0 5px 8px rgba(0,0,0,.28))}}
.kpi-grid{{margin-top:12px;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}}
.kpi{{min-height:112px;border-radius:11px;padding:14px 14px 12px;display:grid;grid-template-columns:38px 1fr;grid-template-rows:auto 1fr auto;column-gap:9px;align-items:center}}
.kpi-icon{{grid-row:1/4;width:34px;height:34px;border:1px solid rgba(198,120,76,.34);border-radius:9px;display:grid;place-items:center;color:var(--copper-bright);font-size:15px;background:rgba(198,120,76,.035)}}
.kpi-label{{color:#aaa49d;font-size:7.7px;letter-spacing:.14em;font-weight:700;text-transform:uppercase}}
.kpi-value{{align-self:end;color:#cf7f51;font-family:Georgia,"Times New Roman",serif;font-size:21px;line-height:1.05;white-space:nowrap}}
.kpi-sub{{color:#7f7a74;font-size:8.7px;line-height:1.25}}
.lower-grid{{margin-top:11px;display:grid;grid-template-columns:.88fr 1.12fr;gap:11px}}
.panel{{min-height:340px;border-radius:11px;padding:0 15px 5px}}
.panel-head{{height:48px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border-soft);color:#d2ccc4;font-size:8.3px;letter-spacing:.15em;font-weight:700;text-transform:uppercase}}
.panel-head button{{border:0;background:transparent;color:var(--copper-bright);font-size:8px;letter-spacing:.08em}}
.game-row{{min-height:70px;display:grid;grid-template-columns:minmax(0,1fr) 92px minmax(0,1fr);align-items:center;gap:7px;border-bottom:1px solid var(--border-soft)}}
.game-row:last-child,.rec-row:last-child{{border-bottom:0}}
.team{{display:flex;align-items:center;gap:9px;min-width:0}} .team.right{{justify-content:flex-end;text-align:right}}
.team-badge{{width:37px;height:37px;border:1px solid #454747;border-radius:50%;display:grid;place-items:center;color:#d5cfc7;font-family:Georgia,"Times New Roman",serif;font-size:11px;background:#101212}}
.team-code{{font-size:11px;color:#d5cfc7;font-weight:600}} .team-prob{{margin-top:2px;color:var(--copper-bright);font-size:9px}}
.kickoff{{text-align:center;color:#8e8982;font-size:8.5px;line-height:1.45}}
.rec-row{{min-height:70px;display:grid;grid-template-columns:25px minmax(0,1fr) 82px 74px;align-items:center;gap:8px;border-bottom:1px solid var(--border-soft)}}
.rec-check{{width:22px;height:22px;border:1px solid var(--copper-bright);border-radius:50%;display:grid;place-items:center;color:var(--copper-bright);font-size:9px}}
.rec-title{{font-size:11px;color:#d7d1c9}} .rec-sub{{margin-top:3px;color:#817c76;font-size:8.5px}}
.rec-prob{{font-family:Georgia,"Times New Roman",serif;color:#d0c9c1;font-size:14px}} .rec-prob span{{display:block;margin-top:2px;font-family:inherit;color:#77736d;font-size:8px}}
.conf{{justify-self:end;width:69px;padding:6px 2px;border:1px solid #69402c;border-radius:5px;text-align:center;color:var(--copper-bright);font-size:9px}} .conf span{{display:block;margin-top:2px;color:#918b84;font-size:7.5px}}
.disclosure{{margin:11px 0 0;padding:9px 12px;border:1px solid #2b2d2d;border-radius:8px;background:rgba(9,10,10,.72);color:#807b75;font-size:8.7px;line-height:1.45}} .disclosure strong{{color:#ad6b47;font-weight:650}}
.page-head{{min-height:130px;padding:22px 25px;border-radius:12px;margin-bottom:11px;display:flex;align-items:flex-end;justify-content:space-between;gap:24px}}
.page-title{{margin:7px 0 0;font-size:31px;line-height:1.08}}
.page-copy{{max-width:620px;margin-top:10px;color:#9d978f;font-size:11px;line-height:1.6}}
.page-mark{{width:118px;opacity:.72}}
.feature-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:11px}}
.metric-card{{border-radius:11px;padding:15px;min-height:112px}}
.metric-label{{color:#9d978f;font-size:7.8px;letter-spacing:.13em;font-weight:700;text-transform:uppercase}}
.metric-value{{margin-top:8px;color:#cf7f51;font-family:Georgia,"Times New Roman",serif;font-size:23px}}
.metric-detail{{margin-top:5px;color:#77726c;font-size:8.8px;line-height:1.4}}
.story-grid{{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-top:11px}}
.story{{border-radius:11px;padding:18px;min-height:175px}} .story h3{{margin:6px 0 8px;font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:20px;color:#ddd6ce}} .story p{{margin:0;color:#918b84;font-size:10.5px;line-height:1.6}}
.rank-board{{border-radius:11px;padding:15px 16px;margin-top:11px}}
.rank-row{{display:grid;grid-template-columns:28px 105px minmax(0,1fr) 58px;gap:10px;align-items:center;min-height:47px;border-bottom:1px solid #262828}} .rank-row:last-child{{border-bottom:0}}
.rank-num{{color:#6f6b65;font-family:Georgia,"Times New Roman",serif;font-size:14px}} .rank-match{{font-size:10px;color:#d2ccc4}} .rank-bar{{height:6px;background:#202222;border-radius:999px;overflow:hidden}} .rank-fill{{height:100%;background:linear-gradient(90deg,#8a4d31,#dc8d5e);border-radius:999px}} .rank-pct{{text-align:right;color:#cf7f51;font-family:Georgia,"Times New Roman",serif;font-size:14px}}
.pipeline{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:11px}} .pipe{{position:relative;min-height:150px;padding:16px;border:1px solid #333535;border-radius:10px;background:linear-gradient(145deg,#161818,#0f1111)}} .pipe:not(:last-child):after{{content:'›';position:absolute;right:-9px;top:56px;color:#8c5134;font-size:25px;z-index:3}} .pipe-num{{color:#815038;font-size:8px;letter-spacing:.15em}} .pipe-title{{margin-top:18px;font-family:Georgia,"Times New Roman",serif;font-size:18px;color:#ddd7cf}} .pipe-copy{{margin-top:8px;color:#7d7872;font-size:9px;line-height:1.5}}
.validation-band{{margin-top:11px;border-radius:11px;padding:17px;display:grid;grid-template-columns:1.1fr 1fr;gap:18px;align-items:center}} .validation-band h3{{margin:4px 0 7px;font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:21px}} .validation-band p{{margin:0;color:#8d8780;font-size:9.8px;line-height:1.55}} .holdout-bars{{display:grid;gap:8px}} .holdout-row{{display:grid;grid-template-columns:67px 1fr 52px;gap:8px;align-items:center;font-size:8.5px;color:#8d8780}} .holdout-track{{height:5px;background:#222424;border-radius:999px;overflow:hidden}} .holdout-fill{{height:100%;background:#c6784c;border-radius:999px}}
.mobile-menu{{display:none}}
@media(max-width:1120px){{.shell{{grid-template-columns:220px minmax(0,1fr)}}.kpi-grid{{grid-template-columns:repeat(3,1fr)}}.feature-grid{{grid-template-columns:repeat(2,1fr)}}.hero-iq{{width:158px;right:4%}}.hero-copy{{width:62%}}}}
@media(max-width:780px){{.shell{{display:block;padding:0;min-height:100vh}}.sidebar{{display:none}}.main{{border:0;border-radius:0;padding:0 11px 18px;min-height:100vh}}.header{{min-height:84px;padding-left:48px}}.greeting{{font-size:17px}}.showcase-pill{{display:none}}.week-control{{min-width:155px}}.mobile-menu{{display:grid;position:absolute;z-index:40;top:24px;left:14px;width:30px;height:30px;place-items:center;border:1px solid rgba(198,120,76,.48);border-radius:6px;background:#101212;color:#dc8d5e}}.mobile-drawer{{display:none;position:absolute;z-index:50;top:61px;left:11px;width:238px;padding:10px;border:1px solid #343636;border-radius:9px;background:#0e1010;box-shadow:0 18px 45px rgba(0,0,0,.5)}}.mobile-drawer.open{{display:grid}}.mobile-drawer button{{height:41px;border:0;border-bottom:1px solid #242626;background:transparent;color:#bbb5ae;text-align:left;padding:0 11px;font-size:10px}}.hero{{height:auto;min-height:255px;padding:24px 20px}}.hero-copy{{width:74%}}.hero h1{{font-size:27px}}.hero-iq{{width:125px;right:-5%;opacity:.62}}.playbook{{opacity:.33;width:68%}}.kpi-grid{{grid-template-columns:repeat(2,1fr)}}.lower-grid,.story-grid,.validation-band{{grid-template-columns:1fr}}.feature-grid{{grid-template-columns:repeat(2,1fr)}}.pipeline{{grid-template-columns:1fr}}.pipe:not(:last-child):after{{display:none}}.game-row{{grid-template-columns:1fr 75px 1fr}}.rec-row{{grid-template-columns:22px 1fr 64px}}.conf{{display:none}}.page-head{{min-height:120px;padding:18px}}.page-mark{{display:none}}}}
</style>
</head>
<body>
<div class="shell">
  <aside class="sidebar">
    <div class="brand">
      <img src="{WORDMARK_URI}" alt="ABIQ">
      <div class="brand-meaning"><span>ANALYTICS</span><b>•</b><span>BALANCE</span><b>•</b><span>INTELLIGENCE</span><b>•</b><span>QUALITY</span></div>
    </div>
    <nav class="nav">
      <button class="nav-button active" data-page="dashboard"><span class="nav-icon">⌂</span>Dashboard</button>
      <button class="nav-button" data-page="weekly"><span class="nav-icon">⌁</span>Weekly Outlook</button>
      <button class="nav-button" data-page="performance"><span class="nav-icon">▥</span>Model Performance</button>
      <button class="nav-button" data-page="platform"><span class="nav-icon">◇</span>Platform</button>
    </nav>
    <div class="profile"><div class="avatar">AM</div><div><div class="profile-name">Abigail Millsap</div><div class="profile-sub">Portfolio Showcase</div></div></div>
  </aside>

  <main class="main">
    <button class="mobile-menu" aria-label="Open navigation">☰</button>
    <div class="mobile-drawer">
      <button data-page="dashboard">Dashboard</button><button data-page="weekly">Weekly Outlook</button><button data-page="performance">Model Performance</button><button data-page="platform">Platform</button>
    </div>
    <header class="header">
      <div><div class="greeting">Welcome to ABIQ.</div><div class="greeting-sub">Smarter decisions through analytics.</div></div>
      <div class="header-actions"><div class="showcase-pill">Static Showcase</div><label class="week-control"><select aria-label="Showcase week"><option>2026 · Week 1</option></select><span class="chev">⌄</span></label></div>
    </header>

    <section id="dashboard" class="page active">
      <section class="hero surface">
        <div class="hero-copy"><div class="eyebrow">Weekly Outlook</div><h1>Edge comes from<br>process, not predictions.</h1><p>ABIQ turns probability, uncertainty, matchup context and future value into a decision-ready football experience. This public opening view mirrors the private dashboard with sanitized static data.</p><button class="outline-button" data-page="weekly">VIEW WEEKLY PREVIEW <span>›</span></button></div>
        <div class="playbook" aria-hidden="true"><svg viewBox="0 0 760 280"><defs><marker id="ag" markerWidth="10" markerHeight="10" refX="8" refY="4.5" orient="auto"><path d="M0,0 L0,9 L9,4.5 z" fill="#8b8780" opacity=".48"/></marker><marker id="ac" markerWidth="10" markerHeight="10" refX="8" refY="4.5" orient="auto"><path d="M0,0 L0,9 L9,4.5 z" fill="#aa6540" opacity=".65"/></marker></defs><path class="play-line" d="M716 69 C620 27 514 22 423 33 C334 44 269 68 209 111" marker-end="url(#ag)"/><path class="play-line play-soft" d="M695 212 C608 244 507 247 419 229 C347 214 284 185 231 151" marker-end="url(#ag)"/><path class="play-line play-soft" d="M189 92 C279 125 367 142 452 140 C543 138 619 113 686 82"/><path class="play-line play-copper" d="M682 119 C624 135 586 158 553 192 C535 211 517 223 493 233" marker-end="url(#ac)"/><circle class="play-circle" cx="196" cy="162" r="14"/><circle class="play-circle" cx="327" cy="198" r="12"/><circle class="play-circle play-copper" cx="647" cy="174" r="14"/><g class="play-x" transform="translate(242 91)"><path d="M-9 -9 L9 9 M9 -9 L-9 9"/></g><g class="play-x" transform="translate(470 93)"><path d="M-9 -9 L9 9 M9 -9 L-9 9"/></g><g class="play-x" transform="translate(612 226)"><path d="M-9 -9 L9 9 M9 -9 L-9 9"/></g></svg></div>
        <img class="hero-iq" src="{IQ_URI}" alt="">
      </section>

      <section class="kpi-grid">
        <article class="kpi surface"><div class="kpi-icon">↗</div><div class="kpi-label">Best win signal</div><div class="kpi-value">81.1%</div><div class="kpi-sub">LAC vs ARI</div></article>
        <article class="kpi surface"><div class="kpi-icon">✓</div><div class="kpi-label">Top confidence</div><div class="kpi-value">LAC</div><div class="kpi-sub">Rank #1 this slate</div></article>
        <article class="kpi surface"><div class="kpi-icon">◎</div><div class="kpi-label">Historical accuracy</div><div class="kpi-value">66.05%</div><div class="kpi-sub">2025 point-in-time replay</div></article>
        <article class="kpi surface"><div class="kpi-icon">◇</div><div class="kpi-label">Signal integrity</div><div class="kpi-value">0</div><div class="kpi-sub">Temporal cutoff violations</div></article>
        <article class="kpi surface"><div class="kpi-icon">ƒ</div><div class="kpi-label">Fantasy holdout</div><div class="kpi-value">−45.4%</div><div class="kpi-sub">Approx. MAE vs baseline</div></article>
      </section>

      <section class="lower-grid">
        <article class="panel surface"><div class="panel-head"><span>Upcoming Games</span><button data-page="weekly">VIEW ALL ›</button></div>
          <div class="game-row"><div class="team"><div class="team-badge">ARI</div><div><div class="team-code">Arizona</div><div class="team-prob">18.1%</div></div></div><div class="kickoff">SUN<br>4:25 PM ET</div><div class="team right"><div><div class="team-code">Los Angeles</div><div class="team-prob">81.1%</div></div><div class="team-badge">LAC</div></div></div>
          <div class="game-row"><div class="team"><div class="team-badge">CLE</div><div><div class="team-code">Cleveland</div><div class="team-prob">23.2%</div></div></div><div class="kickoff">SUN<br>1:00 PM ET</div><div class="team right"><div><div class="team-code">Jacksonville</div><div class="team-prob">75.8%</div></div><div class="team-badge">JAX</div></div></div>
          <div class="game-row"><div class="team"><div class="team-badge">NO</div><div><div class="team-code">New Orleans</div><div class="team-prob">27.1%</div></div></div><div class="kickoff">SUN<br>1:00 PM ET</div><div class="team right"><div><div class="team-code">Detroit</div><div class="team-prob">71.7%</div></div><div class="team-badge">DET</div></div></div>
          <div class="game-row"><div class="team"><div class="team-badge">WAS</div><div><div class="team-code">Washington</div><div class="team-prob">33.9%</div></div></div><div class="kickoff">SUN<br>4:25 PM ET</div><div class="team right"><div><div class="team-code">Philadelphia</div><div class="team-prob">65.0%</div></div><div class="team-badge">PHI</div></div></div>
        </article>
        <article class="panel surface"><div class="panel-head"><span>Model Recommendations</span><button data-page="weekly">VIEW ALL ›</button></div>
          <div class="rec-row"><div class="rec-check">✓</div><div><div class="rec-title">Los Angeles Chargers</div><div class="rec-sub">vs ARI · strongest planning signal</div></div><div class="rec-prob">81.1%<span>WIN SIGNAL</span></div><div class="conf">VERY HIGH<span>CONFIDENCE</span></div></div>
          <div class="rec-row"><div class="rec-check">✓</div><div><div class="rec-title">Jacksonville Jaguars</div><div class="rec-sub">vs CLE · strong separation</div></div><div class="rec-prob">75.8%<span>WIN SIGNAL</span></div><div class="conf">HIGH<span>CONFIDENCE</span></div></div>
          <div class="rec-row"><div class="rec-check">✓</div><div><div class="rec-title">Detroit Lions</div><div class="rec-sub">vs NO · credible alternative</div></div><div class="rec-prob">71.7%<span>WIN SIGNAL</span></div><div class="conf">HIGH<span>CONFIDENCE</span></div></div>
          <div class="rec-row"><div class="rec-check">✓</div><div><div class="rec-title">Philadelphia Eagles</div><div class="rec-sub">vs WAS · secondary option</div></div><div class="rec-prob">65.0%<span>WIN SIGNAL</span></div><div class="conf">MEDIUM<span>CONFIDENCE</span></div></div>
        </article>
      </section>
      <div class="disclosure"><strong>Static portfolio example.</strong> The dashboard above uses sanitized preseason planning data to demonstrate the real ABIQ product experience; it is not a live Week 1 issuance. Validated historical performance is separated on the Model Performance view.</div>
    </section>

    <section id="weekly" class="page">
      <section class="page-head surface"><div><div class="eyebrow">Opening Line · Decision Surface</div><div class="page-title">Weekly Outlook</div><div class="page-copy">A fan-first example of how ABIQ reduces a full NFL slate to the handful of choices worth comparing, while keeping uncertainty and data quality visible.</div></div><img class="page-mark" src="{IQ_URI}" alt=""></section>
      <section class="validation-band surface"><div><div class="eyebrow">Quick Takeaway</div><h3>LAC leads the static Week 1 planning board.</h3><p>Its 81.1% planning signal creates the clearest separation in this sanitized example. The interface deliberately focuses the viewer on the strongest alternatives instead of forcing a scan of every available statistic.</p></div><div class="holdout-bars"><div class="holdout-row"><span>LAC · ARI</span><div class="holdout-track"><div class="holdout-fill" style="width:81.1%"></div></div><strong>81.1%</strong></div><div class="holdout-row"><span>JAX · CLE</span><div class="holdout-track"><div class="holdout-fill" style="width:75.8%"></div></div><strong>75.8%</strong></div><div class="holdout-row"><span>DET · NO</span><div class="holdout-track"><div class="holdout-fill" style="width:71.7%"></div></div><strong>71.7%</strong></div></div></section>
      <section class="rank-board surface"><div class="panel-head"><span>Week 1 · Ranked Planning Signals</span><span style="color:#756f69">STATIC EXAMPLE</span></div><div class="rank-row"><div class="rank-num">01</div><div class="rank-match">LAC vs ARI</div><div class="rank-bar"><div class="rank-fill" style="width:81.1%"></div></div><div class="rank-pct">81.1%</div></div><div class="rank-row"><div class="rank-num">02</div><div class="rank-match">JAX vs CLE</div><div class="rank-bar"><div class="rank-fill" style="width:75.8%"></div></div><div class="rank-pct">75.8%</div></div><div class="rank-row"><div class="rank-num">03</div><div class="rank-match">DET vs NO</div><div class="rank-bar"><div class="rank-fill" style="width:71.7%"></div></div><div class="rank-pct">71.7%</div></div><div class="rank-row"><div class="rank-num">04</div><div class="rank-match">PHI vs WAS</div><div class="rank-bar"><div class="rank-fill" style="width:65%"></div></div><div class="rank-pct">65.0%</div></div><div class="rank-row"><div class="rank-num">05</div><div class="rank-match">CIN vs TB</div><div class="rank-bar"><div class="rank-fill" style="width:63.8%"></div></div><div class="rank-pct">63.8%</div></div></section>
      <section class="story-grid"><article class="story surface"><div class="eyebrow">How to read it</div><h3>Decision first. Evidence second.</h3><p>The recommendation surface prioritizes the action a fan is trying to take, then layers probability, context and confidence behind it. Deeper analytics remain available without dominating the first screen.</p></article><article class="story surface"><div class="eyebrow">Data governance</div><h3>Planning is not prediction history.</h3><p>This current-season surface is intentionally labeled as an example. Historical validation claims remain separate so preseason product design cannot be mistaken for verified live performance.</p></article></section>
    </section>

    <section id="performance" class="page">
      <section class="page-head surface"><div><div class="eyebrow">Validation & Trust</div><div class="page-title">Evidence before confidence.</div><div class="page-copy">ABIQ uses point-in-time replay, frozen baselines and explicit leakage controls so model claims reflect information that could actually have been available when a decision was made.</div></div><img class="page-mark" src="{IQ_URI}" alt=""></section>
      <section class="feature-grid"><article class="metric-card surface"><div class="metric-label">NFL replay</div><div class="metric-value">272 games</div><div class="metric-detail">18-week expanding 2025 regular-season replay</div></article><article class="metric-card surface"><div class="metric-label">Winner accuracy</div><div class="metric-value">66.05%</div><div class="metric-detail">179 of 271 non-tie winners</div></article><article class="metric-card surface"><div class="metric-label">Probability quality</div><div class="metric-value">0.2144</div><div class="metric-detail">Brier score · market-free logistic model</div></article><article class="metric-card surface"><div class="metric-label">Temporal integrity</div><div class="metric-value">0 violations</div><div class="metric-detail">37 prediction-time football features</div></article></section>
      <section class="validation-band surface"><div><div class="eyebrow">Fantasy · Protected Holdout</div><h3>Frozen Ridge challenger beat the frozen baseline.</h3><p>The 2025 reveal compared the exact same 589 established-player population across Standard, Half-PPR and PPR. The candidate was frozen before the holdout was scored and 2025 is not reused for post-reveal tuning.</p></div><div class="holdout-bars"><div class="holdout-row"><span>Standard</span><div class="holdout-track"><div class="holdout-fill" style="width:44.858%"></div></div><strong>−44.86%</strong></div><div class="holdout-row"><span>Half-PPR</span><div class="holdout-track"><div class="holdout-fill" style="width:45.4352%"></div></div><strong>−45.44%</strong></div><div class="holdout-row"><span>PPR</span><div class="holdout-track"><div class="holdout-fill" style="width:45.7589%"></div></div><strong>−45.76%</strong></div></div></section>
      <section class="story-grid"><article class="story surface"><div class="eyebrow">Point-in-time design</div><h3>The model never gets to know the future.</h3><p>Each replay is constrained to information available before the prediction cutoff. Future outcomes, later weekly results and unavailable-at-decision-time signals are explicitly excluded.</p></article><article class="story surface"><div class="eyebrow">Scope discipline</div><h3>A pass is not the end of validation.</h3><p>Fantasy established-player preseason research passed this gate, while rookies/new entrants and weekly start/sit remain separate research tracks. NFL challenger work follows the same frozen-control discipline.</p></article></section>
    </section>

    <section id="platform" class="page">
      <section class="page-head surface"><div><div class="eyebrow">Built End to End</div><div class="page-title">Analytics engineered into a product.</div><div class="page-copy">The private ABIQ system combines reproducible data pipelines, model governance, automated operations, persistence and decision-focused UX. This public repository exposes the product story without exposing production state.</div></div><img class="page-mark" src="{IQ_URI}" alt=""></section>
      <section class="pipeline"><article class="pipe"><div class="pipe-num">01 · OBSERVE</div><div class="pipe-title">Data</div><div class="pipe-copy">Open and governed football sources normalized into reproducible inputs.</div></article><article class="pipe"><div class="pipe-num">02 · TRANSFORM</div><div class="pipe-title">Features</div><div class="pipe-copy">Prediction-time transforms with explicit temporal cutoffs and provenance.</div></article><article class="pipe"><div class="pipe-num">03 · ESTIMATE</div><div class="pipe-title">Models</div><div class="pipe-copy">Frozen champion / challenger evaluation with probabilistic metrics.</div></article><article class="pipe"><div class="pipe-num">04 · DECIDE</div><div class="pipe-title">Optimization</div><div class="pipe-copy">Rankings and strategy built around the actual user decision objective.</div></article><article class="pipe"><div class="pipe-num">05 · EXPLAIN</div><div class="pipe-title">Product</div><div class="pipe-copy">Fan-first Streamlit experiences with safe degraded-mode behavior.</div></article></section>
      <section class="story-grid"><article class="story surface"><div class="eyebrow">Automation</div><h3>Designed to operate without a notebook open.</h3><p>Scheduled GitHub Actions orchestrate data refreshes, validation checks, semantic audits and fail-safe operating paths. Routine tests use fixtures and cached data rather than spending limited live-provider credits.</p></article><article class="story surface"><div class="eyebrow">Trust boundary</div><h3>Public Showcase. Private production.</h3><p>The recruiter app contains no user persistence, credentials, private picks or provider secrets. Its static evidence and visual shell are deliberately separated from the production application.</p></article></section>
    </section>
  </main>
</div>
<script>
const buttons=[...document.querySelectorAll('[data-page]')];
const pages=[...document.querySelectorAll('.page')];
const drawer=document.querySelector('.mobile-drawer');
function go(page){{pages.forEach(p=>p.classList.toggle('active',p.id===page));document.querySelectorAll('.nav-button').forEach(b=>b.classList.toggle('active',b.dataset.page===page));if(drawer)drawer.classList.remove('open');window.scrollTo(0,0)}}
buttons.forEach(b=>b.addEventListener('click',()=>go(b.dataset.page)));
document.querySelector('.mobile-menu').addEventListener('click',()=>drawer.classList.toggle('open'));
</script>
</body>
</html>
"""

components.html(html, height=1030, scrolling=True)
