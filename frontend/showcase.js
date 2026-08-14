const ICONS = {
  home: `<svg viewBox="0 0 24 24"><path d="M3 11.5 12 4l9 7.5"></path><path d="M5.5 10v10h13V10"></path><path d="M9.5 20v-6h5v6"></path></svg>`,
  calendar: `<svg viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15" rx="2"></rect><path d="M7 3v4M17 3v4M3.5 9h17"></path></svg>`,
  chart: `<svg viewBox="0 0 24 24"><path d="M5 20V12h3v8M11 20V7h3v13M17 20V3h3v17"></path></svg>`,
  layers: `<svg viewBox="0 0 24 24"><path d="m12 3 9 5-9 5-9-5 9-5z"></path><path d="m3 12 9 5 9-5M3 16l9 5 9-5"></path></svg>`
};

const NAV_ITEMS = [
  ["Dashboard", "home"],
  ["Weekly Outlook", "calendar"],
  ["Model Performance", "chart"],
  ["Platform", "layers"]
];

const KPI_ICONS = {
  trend: `<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="17"></circle><path d="M9 27l8-11 6 7 8-12"></path></svg>`,
  shield: `<svg viewBox="0 0 40 40"><path d="M20 4l14 5v9c0 9-5 14-14 18C11 32 6 27 6 18V9l14-5z"></path></svg>`,
  check: `<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="17"></circle><path d="M11 20l6 6 13-14"></path></svg>`,
  target: `<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="16"></circle><circle cx="20" cy="20" r="10"></circle><circle cx="20" cy="20" r="3"></circle></svg>`,
  bars: `<svg viewBox="0 0 40 40"><rect x="6" y="24" width="6" height="11"></rect><rect x="17" y="16" width="6" height="19"></rect><rect x="28" y="7" width="6" height="28"></rect></svg>`
};

function hideStreamlitChrome() {
  const saved = [];
  const set = (el, prop, value) => {
    if (!el) return;
    saved.push([el, prop, el.style[prop]]);
    el.style[prop] = value;
  };
  set(document.querySelector('[data-testid="stSidebar"]'), "display", "none");
  set(document.querySelector('[data-testid="stHeader"]'), "display", "none");
  set(document.querySelector('[data-testid="stToolbar"]'), "display", "none");
  set(document.querySelector('[data-testid="stStatusWidget"]'), "display", "none");
  const block = document.querySelector('[data-testid="stMainBlockContainer"]') || document.querySelector('.block-container');
  set(block, "maxWidth", "none");
  set(block, "width", "100%");
  set(block, "padding", "0");
  set(block, "margin", "0");
  const main = document.querySelector('[data-testid="stMain"]');
  set(main, "background", "#111313");
  return () => saved.reverse().forEach(([el, prop, value]) => { el.style[prop] = value; });
}

function setPage(parentElement, pageName) {
  parentElement.querySelectorAll('.abiq-page').forEach((page) => {
    page.classList.toggle('active', page.dataset.page === pageName);
  });
  parentElement.querySelectorAll('.abiq-nav-item').forEach((button) => {
    button.classList.toggle('active', button.dataset.page === pageName);
  });
  const toggle = parentElement.querySelector('#abiq-mobile-nav-toggle');
  if (toggle) toggle.checked = false;
  parentElement.querySelector('.abiq-main')?.scrollIntoView({behavior: 'instant', block: 'start'});
}

function renderNav(parentElement) {
  const nav = parentElement.querySelector('#abiq-nav');
  nav.replaceChildren();
  for (const [label, icon] of NAV_ITEMS) {
    const button = document.createElement('button');
    button.type = 'button';
    button.dataset.page = label;
    button.className = 'abiq-nav-item' + (label === 'Dashboard' ? ' active' : '');
    const iconWrap = document.createElement('span');
    iconWrap.className = 'abiq-nav-icon';
    iconWrap.innerHTML = ICONS[icon];
    const text = document.createElement('span');
    text.textContent = label;
    button.append(iconWrap, text);
    button.onclick = () => setPage(parentElement, label);
    nav.appendChild(button);
  }
  parentElement.querySelectorAll('[data-page-target]').forEach((button) => {
    button.onclick = () => setPage(parentElement, button.dataset.pageTarget);
  });
  const preview = parentElement.querySelector('#abiq-preview-button');
  if (preview) preview.onclick = () => setPage(parentElement, 'Weekly Outlook');
}

function renderWeeks(parentElement, data) {
  const select = parentElement.querySelector('#abiq-week-select');
  select.replaceChildren();
  for (const item of data.weeks ?? []) {
    const option = document.createElement('option');
    option.value = String(item.week);
    option.textContent = item.label;
    if (Number(item.week) === Number(data.current_week)) option.selected = true;
    select.appendChild(option);
  }
}

function renderKpis(parentElement, data) {
  const container = parentElement.querySelector('#abiq-kpis');
  container.replaceChildren();
  for (const item of data.kpis ?? []) {
    const card = document.createElement('article');
    card.className = 'abiq-kpi abiq-surface';
    const icon = document.createElement('div');
    icon.className = 'abiq-kpi-icon';
    icon.innerHTML = KPI_ICONS[item.icon] ?? '';
    const title = document.createElement('div'); title.className = 'abiq-kpi-title'; title.textContent = item.title;
    const value = document.createElement('div'); value.className = 'abiq-kpi-value'; value.textContent = item.value;
    const sub = document.createElement('div'); sub.className = 'abiq-kpi-sub'; sub.textContent = item.subtext;
    card.append(icon, title, value, sub);
    container.appendChild(card);
  }
}

function renderGames(parentElement, data) {
  const container = parentElement.querySelector('#abiq-games');
  container.replaceChildren();
  for (const item of data.games ?? []) {
    const row = document.createElement('div'); row.className = 'abiq-game-row';
    const left = document.createElement('div'); left.className = 'abiq-team-cell';
    const leftLogo = document.createElement('img'); leftLogo.src = item.left.logo; leftLogo.alt = '';
    const leftCopy = document.createElement('div');
    const leftCode = document.createElement('div'); leftCode.className = 'abiq-team-code'; leftCode.textContent = item.left.team;
    const leftProb = document.createElement('div'); leftProb.className = 'abiq-team-prob'; leftProb.textContent = item.left.probability;
    leftCopy.append(leftCode, leftProb); left.append(leftLogo, leftCopy);
    const kickoff = document.createElement('div'); kickoff.className = 'abiq-kickoff'; kickoff.innerHTML = `${item.date}<br>${item.time}`;
    const right = document.createElement('div'); right.className = 'abiq-team-cell right';
    const rightCopy = document.createElement('div'); rightCopy.style.textAlign = 'right';
    const rightCode = document.createElement('div'); rightCode.className = 'abiq-team-code'; rightCode.textContent = item.right.team;
    const rightProb = document.createElement('div'); rightProb.className = 'abiq-team-prob'; rightProb.textContent = item.right.probability;
    rightCopy.append(rightCode, rightProb);
    const rightLogo = document.createElement('img'); rightLogo.src = item.right.logo; rightLogo.alt = '';
    right.append(rightCopy, rightLogo);
    const chevron = document.createElement('span'); chevron.className = 'abiq-row-chevron'; chevron.textContent = '›';
    row.append(left, kickoff, right, chevron);
    container.appendChild(row);
  }
}

function renderRecommendations(parentElement, data) {
  const container = parentElement.querySelector('#abiq-recommendations');
  container.replaceChildren();
  for (const item of data.recommendations ?? []) {
    const row = document.createElement('div'); row.className = 'abiq-rec-row';
    const check = document.createElement('div'); check.className = 'abiq-rec-check'; check.textContent = '✓';
    const team = document.createElement('div'); team.className = 'abiq-rec-team';
    const logo = document.createElement('img'); logo.src = item.logo; logo.alt = '';
    const teamCopy = document.createElement('div');
    const name = document.createElement('div'); name.className = 'abiq-rec-name'; name.textContent = item.team;
    const sub = document.createElement('div'); sub.className = 'abiq-rec-sub'; sub.textContent = `vs ${item.opponent}`;
    teamCopy.append(name, sub); team.append(logo, teamCopy);
    const probability = document.createElement('div'); probability.className = 'abiq-rec-probability'; probability.textContent = item.probability;
    const probabilitySub = document.createElement('span'); probabilitySub.textContent = 'Win Probability'; probability.appendChild(probabilitySub);
    const confidence = document.createElement('div'); confidence.className = 'abiq-confidence'; confidence.textContent = item.confidence;
    const confidenceSub = document.createElement('span'); confidenceSub.textContent = 'Confidence'; confidence.appendChild(confidenceSub);
    row.append(check, team, probability, confidence);
    container.appendChild(row);
  }
}

function renderBars(container, rows) {
  container.replaceChildren();
  for (const item of rows ?? []) {
    const row = document.createElement('div'); row.className = 'abiq-bar-row';
    const label = document.createElement('span'); label.textContent = item.label;
    const track = document.createElement('div'); track.className = 'abiq-bar-track';
    const fill = document.createElement('div'); fill.className = 'abiq-bar-fill'; fill.style.width = `${item.value}%`; track.appendChild(fill);
    const value = document.createElement('strong'); value.textContent = item.display;
    row.append(label, track, value); container.appendChild(row);
  }
}

function renderWeekly(parentElement, data) {
  renderBars(parentElement.querySelector('#abiq-weekly-bars'), data.weekly_rankings?.slice(0,3));
  const board = parentElement.querySelector('#abiq-weekly-rankings');
  board.replaceChildren();
  const head = document.createElement('div'); head.className = 'abiq-panel-heading'; head.innerHTML = '<span>WEEK 1 · RANKED PLANNING SIGNALS</span><span style="color:#756f69">STATIC EXAMPLE</span>';
  board.appendChild(head);
  (data.weekly_rankings ?? []).forEach((item, index) => {
    const row = document.createElement('div'); row.className = 'abiq-rank-row';
    const rank = document.createElement('div'); rank.className = 'abiq-rank-num'; rank.textContent = String(index + 1).padStart(2,'0');
    const matchup = document.createElement('div'); matchup.className = 'abiq-rank-match'; matchup.textContent = item.label;
    const track = document.createElement('div'); track.className = 'abiq-bar-track';
    const fill = document.createElement('div'); fill.className = 'abiq-bar-fill'; fill.style.width = `${item.value}%`; track.appendChild(fill);
    const pct = document.createElement('div'); pct.className = 'abiq-rank-pct'; pct.textContent = item.display;
    row.append(rank, matchup, track, pct); board.appendChild(row);
  });
}

function renderPerformance(parentElement, data) {
  const grid = parentElement.querySelector('#abiq-performance-metrics');
  grid.replaceChildren();
  for (const item of data.performance_metrics ?? []) {
    const card = document.createElement('article'); card.className = 'abiq-metric-card abiq-surface';
    const label = document.createElement('div'); label.className = 'abiq-metric-label'; label.textContent = item.label;
    const value = document.createElement('div'); value.className = 'abiq-metric-value'; value.textContent = item.value;
    const detail = document.createElement('div'); detail.className = 'abiq-metric-detail'; detail.textContent = item.detail;
    card.append(label, value, detail); grid.appendChild(card);
  }
  renderBars(parentElement.querySelector('#abiq-fantasy-bars'), data.fantasy_holdout);
}

function renderPlatform(parentElement, data) {
  const pipeline = parentElement.querySelector('#abiq-platform-pipeline');
  pipeline.replaceChildren();
  (data.platform_pipeline ?? []).forEach((item, index) => {
    const card = document.createElement('article'); card.className = 'abiq-pipe';
    const num = document.createElement('div'); num.className = 'abiq-pipe-num'; num.textContent = `${String(index+1).padStart(2,'0')} · ${item.verb}`;
    const title = document.createElement('div'); title.className = 'abiq-pipe-title'; title.textContent = item.title;
    const copy = document.createElement('div'); copy.className = 'abiq-pipe-copy'; copy.textContent = item.copy;
    card.append(num, title, copy); pipeline.appendChild(card);
  });
}

function initialize(component) {
  const { parentElement, data } = component;
  const root = parentElement.querySelector('#abiq-dashboard-root');
  if (!root) return;
  if (data.base_texture_data_uri) root.style.setProperty('--base-texture', `url("${data.base_texture_data_uri}")`);
  if (data.accent_texture_data_uri) root.style.setProperty('--accent-texture', `url("${data.accent_texture_data_uri}")`);
  parentElement.querySelector('#abiq-brand-logo').src = data.logo_data_uri ?? '';
  parentElement.querySelector('#abiq-hero-iq').src = data.iq_data_uri ?? '';
  parentElement.querySelectorAll('[data-iq]').forEach((img) => { img.src = data.iq_data_uri ?? ''; });
  parentElement.querySelector('#abiq-profile-avatar').textContent = data.initials ?? 'AM';
  parentElement.querySelector('#abiq-profile-name').textContent = data.display_name ?? 'Abigail Millsap';
  parentElement.querySelector('#abiq-hero-description').textContent = data.hero_description ?? '';
  renderNav(parentElement);
  renderWeeks(parentElement, data);
  renderKpis(parentElement, data);
  renderGames(parentElement, data);
  renderRecommendations(parentElement, data);
  renderWeekly(parentElement, data);
  renderPerformance(parentElement, data);
  renderPlatform(parentElement, data);
}

export default function(component) {
  let cancelled = false;
  let frameId = null;
  let cleanupChrome = null;
  let attempts = 0;
  const mount = () => {
    if (cancelled) return;
    if (component.parentElement.querySelector('#abiq-dashboard-root')) {
      cleanupChrome = hideStreamlitChrome();
      initialize(component);
      return;
    }
    attempts += 1;
    if (attempts < 30) frameId = requestAnimationFrame(mount);
  };
  frameId = requestAnimationFrame(mount);
  return () => {
    cancelled = true;
    if (frameId !== null) cancelAnimationFrame(frameId);
    if (cleanupChrome) cleanupChrome();
  };
}
