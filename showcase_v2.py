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

TEAM_LOGO_SLUGS = {
    "ARI": "ari",
    "CIN": "cin",
    "CLE": "cle",
    "DET": "det",
    "JAX": "jax",
    "LAC": "lac",
    "NO": "no",
    "PHI": "phi",
    "TB": "tb",
    "WAS": "wsh",
}


def _asset_data_uri(relative_path: str) -> str:
    path = ROOT / relative_path
    mime_by_suffix = {
        ".webp": "image/webp",
        ".png": "image/png",
        ".svg": "image/svg+xml",
    }
    mime = mime_by_suffix[path.suffix.lower()]
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _team_logo(team: str) -> str:
    slug = TEAM_LOGO_SLUGS[team]
    return f"https://a.espncdn.com/i/teamlogos/nfl/500/{slug}.png"


def _render() -> None:
    wordmark_uri = _asset_data_uri("assets/brand/abiq_wordmark.webp")
    iq_uri = _asset_data_uri("assets/brand/abiq_iq_hero.webp")
    stone_uri = _asset_data_uri("assets/textures/abiq_stone_smooth.webp")

    logos = {team: _team_logo(team) for team in TEAM_LOGO_SLUGS}

    st.set_page_config(
        page_title="ABIQ | Sports Decision Intelligence",
        page_icon="◼",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(
        """
        <style>
          [data-testid="stSidebar"],
          [data-testid="stHeader"],
          [data-testid="stToolbar"],
          [data-testid="stDecoration"],
          [data-testid="stStatusWidget"],
          [data-testid="stAppDeployButton"],
          [data-testid="manage-app-button"],
          .stDeployButton,
          #MainMenu,
          footer {display:none !important; visibility:hidden !important;}
          .stApp {background:#050606 !important;}
          .block-container {max-width:none !important; padding:0 !important; margin:0 !important;}
          iframe {display:block; border:0 !important; width:100% !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    template = r'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
:root {
  --copper:#c6784c;
  --copper-bright:#dc8d5e;
  --copper-deep:#704027;
  --black:#070808;
  --panel:#131515;
  --panel-2:#181a1a;
  --border:#353737;
  --border-soft:#262828;
  --text:#ddd7cf;
  --muted:#9b958e;
  --dim:#716c66;
  --stone:url("__STONE__");
}
*{box-sizing:border-box}
html,body{margin:0;min-height:100%;background:#050606;color:var(--text);font-family:"Avenir Next",Avenir,"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
button,select{font:inherit} button{cursor:pointer}
.shell{width:100%;min-height:1010px;display:grid;grid-template-columns:273px minmax(0,1fr);gap:12px;padding:11px;background-color:var(--black);background-image:radial-gradient(ellipse at 77% 3%,rgba(198,120,76,.06),transparent 30%),radial-gradient(ellipse at 14% 71%,rgba(255,255,255,.025),transparent 27%),var(--stone),linear-gradient(145deg,#070808 0%,#0a0b0b 50%,#070808 100%);background-size:auto,auto,512px 512px,auto;background-blend-mode:normal,normal,soft-light,normal}
.sidebar,.main{border:1px solid #303232;background-color:rgba(12,14,14,.97);background-image:radial-gradient(ellipse at 30% 4%,rgba(255,255,255,.035),transparent 28%),radial-gradient(ellipse at 75% 72%,rgba(198,120,76,.025),transparent 28%),var(--stone),linear-gradient(160deg,rgba(17,19,19,.98),rgba(9,10,10,.98));background-size:auto,auto,512px 512px,auto;background-blend-mode:normal,normal,soft-light,normal;box-shadow:0 18px 42px rgba(0,0,0,.18)}
.sidebar{min-height:988px;border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
.brand{padding:31px 27px 24px;border-bottom:1px solid var(--border-soft)}
.brand img{display:block;width:100%;max-width:178px;height:auto;margin:0 auto}
.brand-meaning{margin:13px auto 0;max-width:190px;display:flex;flex-wrap:wrap;justify-content:center;gap:4px 7px;color:#8e8881;font-size:7.6px;line-height:1.35;letter-spacing:.16em;font-weight:600}.brand-meaning b{color:var(--copper);font-weight:500}
.nav{padding:16px 14px 12px;display:grid;gap:4px}.nav-button{width:100%;height:58px;display:flex;align-items:center;gap:15px;padding:0 16px;border:1px solid transparent;border-left:3px solid transparent;border-radius:6px;background:transparent;color:#c4beb6;text-align:left;font-size:13px;font-weight:450}.nav-button:hover{background:rgba(255,255,255,.03)}.nav-button.active{border-color:rgba(198,120,76,.42);border-left-color:var(--copper-bright);background:linear-gradient(90deg,rgba(198,120,76,.10),rgba(255,255,255,.03));color:#e3ddd5}.nav-icon{width:25px;height:25px;display:grid;place-items:center;color:#bdb7af;font-size:17px}.nav-button.active .nav-icon{color:var(--copper-bright)}
.profile{margin:auto 23px 20px;padding-top:18px;border-top:1px solid var(--border-soft);display:grid;grid-template-columns:39px 1fr;align-items:center;gap:11px}.avatar{width:39px;height:39px;border:1px solid var(--copper);border-radius:50%;display:grid;place-items:center;color:var(--copper-bright);font-size:12px}.profile-name{color:#a9a49d;font-size:13px}.profile-sub{margin-top:2px;color:#6f6c67;font-size:9px;letter-spacing:.08em;text-transform:uppercase}
.main{min-width:0;border-radius:10px;padding:0 24px 24px;overflow:hidden}.header{height:111px;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:0 12px}.greeting{font-family:Georgia,"Times New Roman",serif;font-size:20px;letter-spacing:-.018em;font-weight:400;color:#d9d3cb}.greeting-sub{margin-top:5px;color:#918b84;font-size:11.5px}.header-actions{display:flex;align-items:center;gap:12px}.showcase-pill{height:31px;padding:0 11px;display:flex;align-items:center;border:1px solid rgba(198,120,76,.42);border-radius:999px;color:#c87a4d;background:rgba(198,120,76,.055);font-size:8px;letter-spacing:.14em;font-weight:700;text-transform:uppercase}.week-control{position:relative;min-width:260px;height:45px;display:flex;align-items:center;border:1px solid #313434;border-radius:6px;background:linear-gradient(145deg,rgba(22,24,24,.96),rgba(11,12,12,.96))}.week-control select{width:100%;height:100%;padding:0 38px 0 16px;appearance:none;-webkit-appearance:none;border:0;outline:0;background:transparent;color:#c7c1b9;font-size:13px}.chev{position:absolute;right:13px;color:#8e8982;pointer-events:none}
.page{display:none;animation:fade .18s ease}.page.active{display:block}@keyframes fade{from{opacity:.6;transform:translateY(2px)}to{opacity:1;transform:none}}
.surface{position:relative;overflow:hidden;border:1px solid var(--border);background-color:var(--panel);background-image:radial-gradient(ellipse at 12% 7%,rgba(255,255,255,.045),transparent 30%),radial-gradient(ellipse at 87% 83%,rgba(198,120,76,.035),transparent 31%),var(--stone),linear-gradient(145deg,#191b1b 0%,#111313 49%,#181919 100%);background-size:auto,auto,512px 512px,auto;background-blend-mode:normal,normal,soft-light,normal;box-shadow:inset 0 1px 0 rgba(255,255,255,.012),0 15px 36px rgba(0,0,0,.16)}
.surface-alt{position:relative;overflow:hidden;border:1px solid #303333;background:radial-gradient(ellipse at 82% 16%,rgba(198,120,76,.05),transparent 33%),var(--stone),linear-gradient(145deg,#161818,#0e1010);background-size:auto,512px 512px,auto;background-blend-mode:normal,soft-light,normal;box-shadow:0 12px 30px rgba(0,0,0,.14)}
.hero{height:262px;border-radius:13px;display:flex;align-items:center;padding:29px 35px;background-image:radial-gradient(ellipse at 82% 16%,rgba(198,120,76,.12),transparent 31%),radial-gradient(ellipse at 63% 91%,rgba(255,255,255,.035),transparent 29%),var(--stone),linear-gradient(106deg,#111313 0%,#171818 48%,#2a231f 100%);background-size:auto,auto,512px 512px,auto;background-blend-mode:normal,normal,soft-light,normal}.hero-copy{position:relative;z-index:6;width:48%}.eyebrow{margin-bottom:11px;color:var(--copper-bright);font-size:9.5px;letter-spacing:.18em;font-weight:700;text-transform:uppercase}.hero h1,.page-title{font-family:Georgia,"Times New Roman",serif;font-weight:400;color:var(--text);letter-spacing:-.025em}.hero h1{margin:0;font-size:34px;line-height:1.10}.hero p{margin:14px 0 0;max-width:475px;color:#b1aca5;font-size:12.5px;line-height:1.58}.outline-button{margin-top:17px;height:39px;padding:0 15px;display:inline-flex;align-items:center;gap:20px;border:1px solid #8d4f31;border-radius:5px;background:rgba(11,12,12,.42);color:var(--copper-bright);font-size:9px;letter-spacing:.15em;font-weight:650}.playbook{position:absolute;z-index:2;right:13px;top:6px;width:55%;height:250px;pointer-events:none;opacity:.58;mix-blend-mode:screen}.playbook svg{width:100%;height:100%}.play-line,.play-circle,.play-x path{stroke:#8f8b84;fill:none;stroke-width:1.55;opacity:.42}.play-soft{opacity:.25}.play-copper{stroke:#aa6540;opacity:.58}.hero-iq{position:absolute;z-index:5;right:13%;top:50%;transform:translateY(-50%);width:235px;height:auto;filter:drop-shadow(0 4px 6px rgba(0,0,0,.26))}
.kpi-grid{margin-top:14px;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:11px}.kpi{height:118px;display:grid;grid-template-columns:48px minmax(0,1fr);grid-template-rows:24px 42px 20px;align-items:center;column-gap:10px;padding:16px 15px 14px;border-radius:11px}.kpi-icon{grid-column:1;grid-row:1/span 3;width:39px;height:39px;border:1px solid rgba(198,120,76,.36);border-radius:9px;display:grid;place-items:center;color:var(--copper-bright);font-size:16px;background:rgba(198,120,76,.03)}.kpi-label{color:#aaa49d;font-size:8.8px;line-height:1.2;letter-spacing:.13em;font-weight:650;text-transform:uppercase}.kpi-value{color:#cf7f51;font-family:Georgia,"Times New Roman",serif;font-size:23px;line-height:1.02;font-weight:400;white-space:nowrap}.kpi-sub{color:#858079;font-size:9.6px;line-height:1.25}
.lower-grid{margin-top:12px;display:grid;grid-template-columns:.86fr 1.14fr;gap:12px}.panel{min-height:352px;border-radius:11px;padding:0 16px 5px}.panel-head{height:49px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border-soft);color:#d5cfc7;font-size:9.5px;letter-spacing:.15em;font-weight:650;text-transform:uppercase}.panel-head button{border:0;background:transparent;color:var(--copper-bright);font-size:9px;letter-spacing:.06em}.game-row{min-height:73px;display:grid;grid-template-columns:minmax(0,1fr) 112px minmax(0,1fr);align-items:center;gap:7px;border-bottom:1px solid var(--border-soft)}.game-row:last-child,.rec-row:last-child{border-bottom:0}.team{display:flex;align-items:center;gap:10px;min-width:0}.team.right{justify-content:flex-end;text-align:right}.team-logo,.rec-logo{width:43px;height:43px;object-fit:contain;filter:drop-shadow(0 2px 4px rgba(0,0,0,.32))}.team-code{color:#d9d3cb;font-size:12.5px;font-weight:550}.team-prob{margin-top:2px;color:var(--copper-bright);font-size:11px}.kickoff{color:#c0bbb4;text-align:center;font-size:9.5px;line-height:1.45}.rec-row{min-height:73px;display:grid;grid-template-columns:29px minmax(0,1fr) 115px 95px;align-items:center;gap:9px;border-bottom:1px solid var(--border-soft)}.rec-check{width:24px;height:24px;display:grid;place-items:center;border:1px solid var(--copper-bright);border-radius:50%;color:var(--copper-bright);font-size:11px}.rec-team{display:flex;align-items:center;gap:10px;min-width:0}.rec-name{color:#d8d2ca;font-size:12.5px;font-weight:500}.rec-sub{margin-top:2px;color:#99948d;font-size:10px}.rec-prob{color:#d7d1c9;font-size:12.5px}.rec-prob span{display:block;margin-top:3px;color:#9e9992;font-size:9px}.conf{justify-self:end;width:78px;padding:7px 3px 6px;border:1px solid #6f422d;border-radius:5px;color:var(--copper-bright);text-align:center;font-size:10px}.conf span{display:block;margin-top:2px;color:#a49f98;font-size:8px}.disclosure{margin:12px 0 0;padding:10px 13px;border:1px solid #2b2d2d;border-radius:8px;background:rgba(8,9,9,.82);color:#817c76;font-size:9px;line-height:1.5}.disclosure strong{color:#b16e49;font-weight:650}
.page-head{min-height:148px;padding:24px 28px;border-radius:12px;margin-bottom:12px;display:flex;align-items:flex-end;justify-content:space-between;gap:24px;background-image:radial-gradient(ellipse at 88% 15%,rgba(198,120,76,.10),transparent 30%),var(--stone),linear-gradient(120deg,#151717,#111313 55%,#211a17);background-size:auto,512px 512px,auto;background-blend-mode:normal,soft-light,normal}.page-title{margin:6px 0 0;font-size:31px;line-height:1.08}.page-copy{max-width:650px;margin-top:10px;color:#9d978f;font-size:11px;line-height:1.6}.page-mark{width:138px;opacity:.66}.feature-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:11px}.metric-card{border-radius:11px;padding:17px;min-height:120px}.metric-label{color:#9d978f;font-size:7.8px;letter-spacing:.13em;font-weight:700;text-transform:uppercase}.metric-value{margin-top:9px;color:#cf7f51;font-family:Georgia,"Times New Roman",serif;font-size:23px}.metric-detail{margin-top:6px;color:#77726c;font-size:8.8px;line-height:1.45}.story-grid{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-top:11px}.story{border-radius:11px;padding:19px;min-height:175px}.story h3{margin:6px 0 8px;font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:20px;color:#ddd6ce}.story p{margin:0;color:#918b84;font-size:10.5px;line-height:1.6}.rank-board{border-radius:11px;padding:15px 16px;margin-top:11px}.rank-row{display:grid;grid-template-columns:28px 105px minmax(0,1fr) 58px;gap:10px;align-items:center;min-height:47px;border-bottom:1px solid #262828}.rank-row:last-child{border-bottom:0}.rank-num{color:#6f6b65;font-family:Georgia,"Times New Roman",serif;font-size:14px}.rank-match{font-size:10px;color:#d2ccc4}.rank-bar{height:6px;background:#202222;border-radius:999px;overflow:hidden}.rank-fill{height:100%;background:linear-gradient(90deg,#8a4d31,#dc8d5e);border-radius:999px}.rank-pct{text-align:right;color:#cf7f51;font-family:Georgia,"Times New Roman",serif;font-size:14px}.validation-band{margin-top:11px;border-radius:11px;padding:18px;display:grid;grid-template-columns:1.1fr 1fr;gap:18px;align-items:center}.validation-band h3{margin:4px 0 7px;font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:21px}.validation-band p{margin:0;color:#8d8780;font-size:9.8px;line-height:1.55}.holdout-bars{display:grid;gap:9px}.holdout-row{display:grid;grid-template-columns:67px 1fr 56px;gap:8px;align-items:center;font-size:8.5px;color:#8d8780}.holdout-track{height:5px;background:#222424;border-radius:999px;overflow:hidden}.holdout-fill{height:100%;background:#c6784c;border-radius:999px}
.pipeline{display:grid;grid-template-columns:repeat(5,1fr);gap:9px;margin-top:11px}.pipe{position:relative;min-height:158px;padding:17px;border:1px solid #333535;border-radius:10px;background:radial-gradient(ellipse at 85% 12%,rgba(198,120,76,.055),transparent 34%),var(--stone),linear-gradient(145deg,#171919,#0f1111);background-size:auto,512px 512px,auto;background-blend-mode:normal,soft-light,normal;box-shadow:inset 0 2px 0 rgba(198,120,76,.15),0 10px 28px rgba(0,0,0,.12)}.pipe:nth-child(even){background:radial-gradient(ellipse at 20% 85%,rgba(255,255,255,.025),transparent 33%),var(--stone),linear-gradient(145deg,#121515,#0a0c0c);background-size:auto,512px 512px,auto;background-blend-mode:normal,soft-light,normal}.pipe:not(:last-child):after{content:'›';position:absolute;right:-10px;top:58px;color:#8c5134;font-size:25px;z-index:3}.pipe-num{color:#9b5b3b;font-size:8px;letter-spacing:.15em}.pipe-title{margin-top:18px;font-family:Georgia,"Times New Roman",serif;font-size:18px;color:#ddd7cf}.pipe-copy{margin-top:8px;color:#7d7872;font-size:9px;line-height:1.5}
.mobile-menu,.mobile-drawer{display:none}
@media(max-width:1180px){.shell{grid-template-columns:235px minmax(0,1fr)}.main{padding-left:16px;padding-right:16px}.hero h1{font-size:32px}.hero-iq{width:190px;right:8%}.kpi-grid{grid-template-columns:repeat(5,minmax(145px,1fr));overflow-x:auto}.feature-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:860px){.shell{display:block;padding:0;min-height:100vh}.sidebar{display:none}.main{border:0;border-radius:0;padding:0 12px 24px;min-height:100vh}.header{height:auto;min-height:92px;align-items:flex-start;padding:16px 0 12px 48px}.greeting{font-size:18px}.greeting-sub{max-width:190px;line-height:1.45}.header-actions{gap:4px}.showcase-pill{display:none}.week-control{min-width:215px;height:43px}.mobile-menu{display:grid;position:absolute;z-index:60;top:19px;left:14px;width:34px;height:34px;place-items:center;border:1px solid rgba(198,120,76,.56);border-radius:7px;background:rgba(14,16,16,.96);box-shadow:0 7px 20px rgba(0,0,0,.30);color:#dc8d5e;font-size:17px}.mobile-drawer{position:absolute;z-index:70;top:60px;left:12px;width:min(82vw,300px);max-height:78vh;overflow:auto;padding:12px;border:1px solid #343636;border-radius:10px;background:linear-gradient(160deg,#151717,#0b0d0d);box-shadow:18px 18px 44px rgba(0,0,0,.42)}.mobile-drawer.open{display:block}.drawer-brand{padding:10px 12px 16px;border-bottom:1px solid var(--border-soft);margin-bottom:8px}.drawer-brand img{display:block;width:150px;height:auto}.mobile-drawer button{width:100%;height:44px;border:0;border-bottom:1px solid #242626;background:transparent;color:#bbb5ae;text-align:left;padding:0 11px;font-size:10px}.hero{height:auto;min-height:265px;padding:25px 22px}.hero-copy{width:72%}.hero h1{font-size:29px;line-height:1.08}.hero p{font-size:11.2px;line-height:1.58}.playbook{width:62%;opacity:.42}.hero-iq{width:155px;right:2%;opacity:.74}.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr));overflow:visible;gap:10px}.kpi{height:126px;grid-template-columns:42px minmax(0,1fr);grid-template-rows:25px 43px 27px;padding:15px 13px 13px;column-gap:8px}.kpi-icon{width:35px;height:35px}.kpi-label{font-size:8px}.kpi-value{font-size:22px}.kpi-sub{font-size:8.8px}.kpi:last-child{grid-column:1/-1}.lower-grid,.story-grid,.validation-band{grid-template-columns:1fr}.feature-grid{grid-template-columns:repeat(2,1fr)}.pipeline{grid-template-columns:1fr}.pipe:not(:last-child):after{display:none}.game-row{grid-template-columns:minmax(0,1fr) 72px minmax(0,1fr);gap:5px}.team-logo{width:36px;height:36px}.team-code{font-size:10.5px}.team-prob{font-size:9.5px}.kickoff{font-size:8px}.rec-row{grid-template-columns:23px minmax(0,1fr) 64px}.rec-logo{width:34px;height:34px}.rec-name{font-size:10.5px}.rec-sub{font-size:8.5px}.rec-prob{font-size:11px}.conf{display:none}.page-head{min-height:132px;padding:19px}.page-title{font-size:27px}.page-mark{display:none}.rank-row{grid-template-columns:24px 76px minmax(0,1fr) 48px}.rank-match{font-size:8.5px}.metric-card{min-height:116px;padding:14px}.metric-value{font-size:20px}}
@media(max-width:480px){.header{padding-left:48px}.week-control{min-width:155px}.hero-copy{width:76%}.hero-iq{width:138px;right:1%;opacity:.68}.kpi{height:124px}.feature-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.metric-card{padding:13px;min-height:120px}.metric-detail{font-size:8px}.team-code{display:none}}
</style>
</head>
<body>
<div class="shell">
  <aside class="sidebar">
    <div class="brand"><img src="__WORDMARK__" alt="ABIQ"><div class="brand-meaning"><span>ANALYTICS</span><b>•</b><span>BALANCE</span><b>•</b><span>INTELLIGENCE</span><b>•</b><span>QUALITY</span></div></div>
    <nav class="nav">
      <button class="nav-button active" data-page="dashboard"><span class="nav-icon">⌂</span>Dashboard</button>
      <button class="nav-button" data-page="weekly"><span class="nav-icon">⌁</span>Weekly Outlook</button>
      <button class="nav-button" data-page="performance"><span class="nav-icon">▥</span>Model Performance</button>
      <button class="nav-button" data-page="platform"><span class="nav-icon">◇</span>Platform</button>
    </nav>
    <div class="profile"><div class="avatar">AM</div><div><div class="profile-name">Abigail Millsap</div><div class="profile-sub">Portfolio Showcase</div></div></div>
  </aside>

  <main class="main">
    <button class="mobile-menu" aria-label="Open ABIQ navigation">☰</button>
    <div class="mobile-drawer"><div class="drawer-brand"><img src="__WORDMARK__" alt="ABIQ"></div><button data-page="dashboard">Dashboard</button><button data-page="weekly">Weekly Outlook</button><button data-page="performance">Model Performance</button><button data-page="platform">Platform</button></div>
    <header class="header"><div><div class="greeting">Welcome to ABIQ.</div><div class="greeting-sub">Smarter decisions through analytics.</div></div><div class="header-actions"><div class="showcase-pill">Static Showcase</div><label class="week-control"><select aria-label="Showcase week"><option>2026 · Week 1</option></select><span class="chev">⌄</span></label></div></header>

    <section id="dashboard" class="page active">
      <section class="hero surface"><div class="hero-copy"><div class="eyebrow">Weekly Outlook</div><h1>Edge comes from<br>process, not predictions.</h1><p>ABIQ turns probability, uncertainty, matchup context and future value into a decision-ready football experience. This public opening view mirrors the private dashboard with sanitized static data.</p><button class="outline-button" data-page="weekly">VIEW WEEKLY PREVIEW <span>›</span></button></div><div class="playbook" aria-hidden="true"><svg viewBox="0 0 760 280"><defs><marker id="ag" markerWidth="10" markerHeight="10" refX="8" refY="4.5" orient="auto"><path d="M0,0 L0,9 L9,4.5 z" fill="#8b8780" opacity=".48"/></marker><marker id="ac" markerWidth="10" markerHeight="10" refX="8" refY="4.5" orient="auto"><path d="M0,0 L0,9 L9,4.5 z" fill="#aa6540" opacity=".65"/></marker></defs><path class="play-line" d="M716 69 C620 27 514 22 423 33 C334 44 269 68 209 111" marker-end="url(#ag)"/><path class="play-line play-soft" d="M695 212 C608 244 507 247 419 229 C347 214 284 185 231 151" marker-end="url(#ag)"/><path class="play-line play-soft" d="M189 92 C279 125 367 142 452 140 C543 138 619 113 686 82"/><path class="play-line play-copper" d="M682 119 C624 135 586 158 553 192 C535 211 517 223 493 233" marker-end="url(#ac)"/><circle class="play-circle" cx="196" cy="162" r="14"/><circle class="play-circle" cx="327" cy="198" r="12"/><circle class="play-circle play-copper" cx="647" cy="174" r="14"/><g class="play-x" transform="translate(242 91)"><path d="M-9 -9 L9 9 M9 -9 L-9 9"/></g><g class="play-x" transform="translate(470 93)"><path d="M-9 -9 L9 9 M9 -9 L-9 9"/></g><g class="play-x" transform="translate(612 226)"><path d="M-9 -9 L9 9 M9 -9 L-9 9"/></g></svg></div><img class="hero-iq" src="__IQ__" alt=""></section>

      <section class="kpi-grid">
        <article class="kpi surface"><div class="kpi-icon">↗</div><div class="kpi-label">Top win probability</div><div class="kpi-value">81.1%</div><div class="kpi-sub">Highest current signal</div></article>
        <article class="kpi surface"><div class="kpi-icon">◈</div><div class="kpi-label">Confidence level</div><div class="kpi-value">High</div><div class="kpi-sub">Strongest weekly tier</div></article>
        <article class="kpi surface"><div class="kpi-icon">✓</div><div class="kpi-label">Weekly picks</div><div class="kpi-value">16</div><div class="kpi-sub">Across 16 games</div></article>
        <article class="kpi surface"><div class="kpi-icon">◎</div><div class="kpi-label">Replay accuracy</div><div class="kpi-value">66.05%</div><div class="kpi-sub">2025 point-in-time replay</div></article>
        <article class="kpi surface"><div class="kpi-icon">ƒ</div><div class="kpi-label">Fantasy holdout</div><div class="kpi-value">−45.4%</div><div class="kpi-sub">Approx. MAE vs baseline</div></article>
      </section>

      <section class="lower-grid">
        <article class="panel surface"><div class="panel-head"><span>Upcoming Games</span><button data-page="weekly">VIEW ALL ›</button></div>
          <div class="game-row"><div class="team"><img class="team-logo" src="__ARI__" alt="ARI"><div><div class="team-code">ARI</div><div class="team-prob">18.1%</div></div></div><div class="kickoff">SUN<br>4:25 PM ET</div><div class="team right"><div><div class="team-code">LAC</div><div class="team-prob">81.1%</div></div><img class="team-logo" src="__LAC__" alt="LAC"></div></div>
          <div class="game-row"><div class="team"><img class="team-logo" src="__CLE__" alt="CLE"><div><div class="team-code">CLE</div><div class="team-prob">23.2%</div></div></div><div class="kickoff">SUN<br>1:00 PM ET</div><div class="team right"><div><div class="team-code">JAX</div><div class="team-prob">75.8%</div></div><img class="team-logo" src="__JAX__" alt="JAX"></div></div>
          <div class="game-row"><div class="team"><img class="team-logo" src="__NO__" alt="NO"><div><div class="team-code">NO</div><div class="team-prob">27.1%</div></div></div><div class="kickoff">SUN<br>1:00 PM ET</div><div class="team right"><div><div class="team-code">DET</div><div class="team-prob">71.7%</div></div><img class="team-logo" src="__DET__" alt="DET"></div></div>
          <div class="game-row"><div class="team"><img class="team-logo" src="__WAS__" alt="WAS"><div><div class="team-code">WAS</div><div class="team-prob">33.9%</div></div></div><div class="kickoff">SUN<br>4:25 PM ET</div><div class="team right"><div><div class="team-code">PHI</div><div class="team-prob">65.0%</div></div><img class="team-logo" src="__PHI__" alt="PHI"></div></div>
        </article>
        <article class="panel surface"><div class="panel-head"><span>Model Recommendations</span><button data-page="weekly">VIEW ALL ›</button></div>
          <div class="rec-row"><div class="rec-check">✓</div><div class="rec-team"><img class="rec-logo" src="__LAC__" alt="LAC"><div><div class="rec-name">Los Angeles Chargers</div><div class="rec-sub">vs ARI · strongest planning signal</div></div></div><div class="rec-prob">81.1%<span>WIN SIGNAL</span></div><div class="conf">VERY HIGH<span>CONFIDENCE</span></div></div>
          <div class="rec-row"><div class="rec-check">✓</div><div class="rec-team"><img class="rec-logo" src="__JAX__" alt="JAX"><div><div class="rec-name">Jacksonville Jaguars</div><div class="rec-sub">vs CLE · strong separation</div></div></div><div class="rec-prob">75.8%<span>WIN SIGNAL</span></div><div class="conf">HIGH<span>CONFIDENCE</span></div></div>
          <div class="rec-row"><div class="rec-check">✓</div><div class="rec-team"><img class="rec-logo" src="__DET__" alt="DET"><div><div class="rec-name">Detroit Lions</div><div class="rec-sub">vs NO · credible alternative</div></div></div><div class="rec-prob">71.7%<span>WIN SIGNAL</span></div><div class="conf">HIGH<span>CONFIDENCE</span></div></div>
          <div class="rec-row"><div class="rec-check">✓</div><div class="rec-team"><img class="rec-logo" src="__PHI__" alt="PHI"><div><div class="rec-name">Philadelphia Eagles</div><div class="rec-sub">vs WAS · secondary option</div></div></div><div class="rec-prob">65.0%<span>WIN SIGNAL</span></div><div class="conf">MEDIUM<span>CONFIDENCE</span></div></div>
        </article>
      </section>
      <div class="disclosure"><strong>Static portfolio example.</strong> This opening dashboard uses sanitized preseason planning data to demonstrate the real ABIQ product experience; it is not a live Week 1 issuance. Validated historical performance is separated on Model Performance.</div>
    </section>

    <section id="weekly" class="page">
      <section class="page-head surface"><div><div class="eyebrow">Opening Line · Decision Surface</div><div class="page-title">Weekly Outlook</div><div class="page-copy">ABIQ reduces a full NFL slate to the handful of choices worth comparing, while keeping uncertainty, context and data quality visible.</div></div><img class="page-mark" src="__IQ__" alt=""></section>
      <section class="validation-band surface-alt"><div><div class="eyebrow">Quick Takeaway</div><h3>LAC leads the static Week 1 planning board.</h3><p>Its 81.1% planning signal creates the clearest separation in this sanitized example. The interface deliberately focuses the viewer on the strongest alternatives instead of forcing a scan of every available statistic.</p></div><div class="holdout-bars"><div class="holdout-row"><span>LAC · ARI</span><div class="holdout-track"><div class="holdout-fill" style="width:81.1%"></div></div><strong>81.1%</strong></div><div class="holdout-row"><span>JAX · CLE</span><div class="holdout-track"><div class="holdout-fill" style="width:75.8%"></div></div><strong>75.8%</strong></div><div class="holdout-row"><span>DET · NO</span><div class="holdout-track"><div class="holdout-fill" style="width:71.7%"></div></div><strong>71.7%</strong></div></div></section>
      <section class="rank-board surface"><div class="panel-head"><span>Week 1 · Ranked Planning Signals</span><span style="color:#756f69">STATIC EXAMPLE</span></div><div class="rank-row"><div class="rank-num">01</div><div class="rank-match">LAC vs ARI</div><div class="rank-bar"><div class="rank-fill" style="width:81.1%"></div></div><div class="rank-pct">81.1%</div></div><div class="rank-row"><div class="rank-num">02</div><div class="rank-match">JAX vs CLE</div><div class="rank-bar"><div class="rank-fill" style="width:75.8%"></div></div><div class="rank-pct">75.8%</div></div><div class="rank-row"><div class="rank-num">03</div><div class="rank-match">DET vs NO</div><div class="rank-bar"><div class="rank-fill" style="width:71.7%"></div></div><div class="rank-pct">71.7%</div></div><div class="rank-row"><div class="rank-num">04</div><div class="rank-match">PHI vs WAS</div><div class="rank-bar"><div class="rank-fill" style="width:65%"></div></div><div class="rank-pct">65.0%</div></div><div class="rank-row"><div class="rank-num">05</div><div class="rank-match">CIN vs TB</div><div class="rank-bar"><div class="rank-fill" style="width:63.8%"></div></div><div class="rank-pct">63.8%</div></div></section>
      <section class="story-grid"><article class="story surface-alt"><div class="eyebrow">How to read it</div><h3>Decision first. Evidence second.</h3><p>The recommendation surface prioritizes the action a fan is trying to take, then layers probability, context and confidence behind it.</p></article><article class="story surface"><div class="eyebrow">Data governance</div><h3>Planning is not prediction history.</h3><p>Current-season surfaces are intentionally labeled as examples. Historical validation claims remain separate so product design cannot be mistaken for verified live performance.</p></article></section>
    </section>

    <section id="performance" class="page">
      <section class="page-head surface"><div><div class="eyebrow">Validation & Trust</div><div class="page-title">Evidence before confidence.</div><div class="page-copy">ABIQ uses point-in-time replay, frozen baselines and explicit leakage controls so model claims reflect information that could actually have been available when a decision was made.</div></div><img class="page-mark" src="__IQ__" alt=""></section>
      <section class="feature-grid"><article class="metric-card surface-alt"><div class="metric-label">NFL replay</div><div class="metric-value">272 games</div><div class="metric-detail">18-week expanding 2025 regular-season replay</div></article><article class="metric-card surface"><div class="metric-label">Winner accuracy</div><div class="metric-value">66.05%</div><div class="metric-detail">179 of 271 non-tie winners</div></article><article class="metric-card surface-alt"><div class="metric-label">Probability quality</div><div class="metric-value">0.2144</div><div class="metric-detail">Brier score · market-free logistic model</div></article><article class="metric-card surface"><div class="metric-label">Temporal integrity</div><div class="metric-value">0 violations</div><div class="metric-detail">37 prediction-time football features</div></article></section>
      <section class="validation-band surface"><div><div class="eyebrow">Fantasy · Protected Holdout</div><h3>Frozen Ridge challenger beat the frozen baseline.</h3><p>The 2025 reveal compared the same 589 established-player population across Standard, Half-PPR and PPR. The candidate was frozen before the holdout was scored and 2025 is not reused for post-reveal tuning.</p></div><div class="holdout-bars"><div class="holdout-row"><span>Standard</span><div class="holdout-track"><div class="holdout-fill" style="width:44.858%"></div></div><strong>−44.86%</strong></div><div class="holdout-row"><span>Half-PPR</span><div class="holdout-track"><div class="holdout-fill" style="width:45.4352%"></div></div><strong>−45.44%</strong></div><div class="holdout-row"><span>PPR</span><div class="holdout-track"><div class="holdout-fill" style="width:45.7589%"></div></div><strong>−45.76%</strong></div></div></section>
      <section class="story-grid"><article class="story surface"><div class="eyebrow">Point-in-time design</div><h3>The model never gets to know the future.</h3><p>Each replay is constrained to information available before the prediction cutoff. Future outcomes, later weekly results and unavailable-at-decision-time signals are explicitly excluded.</p></article><article class="story surface-alt"><div class="eyebrow">Scope discipline</div><h3>A pass is not the end of validation.</h3><p>Fantasy established-player preseason research passed this gate, while rookies/new entrants and weekly start/sit remain separate research tracks.</p></article></section>
    </section>

    <section id="platform" class="page">
      <section class="page-head surface"><div><div class="eyebrow">Built End to End</div><div class="page-title">Analytics engineered into a product.</div><div class="page-copy">The private ABIQ system combines reproducible data pipelines, model governance, automated operations, persistence and decision-focused UX. This public repository exposes the product story without exposing production state.</div></div><img class="page-mark" src="__IQ__" alt=""></section>
      <section class="pipeline"><article class="pipe"><div class="pipe-num">01 · OBSERVE</div><div class="pipe-title">Data</div><div class="pipe-copy">Open and governed football sources normalized into reproducible inputs.</div></article><article class="pipe"><div class="pipe-num">02 · TRANSFORM</div><div class="pipe-title">Features</div><div class="pipe-copy">Prediction-time transforms with explicit temporal cutoffs and provenance.</div></article><article class="pipe"><div class="pipe-num">03 · ESTIMATE</div><div class="pipe-title">Models</div><div class="pipe-copy">Frozen champion / challenger evaluation with probabilistic metrics.</div></article><article class="pipe"><div class="pipe-num">04 · DECIDE</div><div class="pipe-title">Optimization</div><div class="pipe-copy">Rankings and strategy built around the actual user decision objective.</div></article><article class="pipe"><div class="pipe-num">05 · EXPLAIN</div><div class="pipe-title">Product</div><div class="pipe-copy">Fan-first Streamlit experiences with safe degraded-mode behavior.</div></article></section>
      <section class="story-grid"><article class="story surface"><div class="eyebrow">Automation</div><h3>Designed to operate without a notebook open.</h3><p>Scheduled GitHub Actions orchestrate data refreshes, validation checks, semantic audits and fail-safe operating paths. Routine tests use fixtures and cached data rather than spending limited live-provider credits.</p></article><article class="story surface-alt"><div class="eyebrow">Trust boundary</div><h3>Public Showcase. Private production.</h3><p>The recruiter app contains no user persistence, credentials, private picks or provider secrets. Static evidence and the product shell remain deliberately separated from production.</p></article></section>
    </section>
  </main>
</div>
<script>
const buttons=[...document.querySelectorAll('[data-page]')];
const pages=[...document.querySelectorAll('.page')];
const drawer=document.querySelector('.mobile-drawer');
function go(page){pages.forEach(p=>p.classList.toggle('active',p.id===page));document.querySelectorAll('.nav-button').forEach(b=>b.classList.toggle('active',b.dataset.page===page));if(drawer)drawer.classList.remove('open');window.scrollTo(0,0)}
buttons.forEach(b=>b.addEventListener('click',()=>go(b.dataset.page)));
document.querySelector('.mobile-menu').addEventListener('click',()=>drawer.classList.toggle('open'));
</script>
</body>
</html>'''

    replacements = {
        "__WORDMARK__": wordmark_uri,
        "__IQ__": iq_uri,
        "__STONE__": stone_uri,
    }
    replacements.update({f"__{team}__": url for team, url in logos.items()})
    html = template
    for token, value in replacements.items():
        html = html.replace(token, value)

    components.html(html, height=1240, scrolling=True)


def run() -> None:
    _render()
