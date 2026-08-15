const ICONS = {
  home: `<svg viewBox="0 0 24 24"><path d="M3 11.5 12 4l9 7.5"></path><path d="M5.5 10v10h13V10"></path><path d="M9.5 20v-6h5v6"></path></svg>`,
  forecast: `<svg viewBox="0 0 24 24"><path d="M3 18l5-6 4 3 6-9"></path><path d="M15 6h3v3"></path><path d="M4 21h16"></path></svg>`,
  chart: `<svg viewBox="0 0 24 24"><path d="M5 20V12h3v8M11 20V7h3v13M17 20V3h3v17"></path></svg>`
};

const NAV_ITEMS = [
  ["Dashboard", "home"],
  ["Forecasts", "forecast"],
  ["Performance", "chart"]
];

const TEAM_LOGO_SLUGS = {
  ARI: "ari", CIN: "cin", CLE: "cle", DET: "det", JAX: "jax",
  LAC: "lac", NO: "no", PHI: "phi", TB: "tb", WAS: "wsh"
};

const FORECAST_READS = {
  LAC: "Clear top-line favorite in the static weekly view.",
  JAX: "Strong favorite signal with less uncertainty than the middle tier.",
  DET: "Detroit leads while a meaningful underdog path remains visible.",
  PHI: "Tighter forecast with more upset pressure than the leading favorites.",
  CIN: "Closest featured favorite and the slate's strongest upset-watch candidate."
};

const UPSET_READS = {
  TB: "The narrowest featured favorite keeps Tampa live in the representative weekly slate.",
  WAS: "A relatively tight forecast makes Washington worth monitoring behind the headline pick.",
  NO: "Detroit remains favored, but the gap is small enough to keep New Orleans on the watch list."
};

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
  if (preview) preview.onclick = () => setPage(parentElement, 'Forecasts');
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
    const icon = document.createElement('div'); icon.className = 'abiq-kpi-icon'; icon.innerHTML = KPI_ICONS[item.icon] ?? '';
    const title = document.createElement('div'); title.className = 'abiq-kpi-title'; title.textContent = item.title;
    const value = document.createElement('div'); value.className = 'abiq-kpi-value'; value.textContent = item.value;
    const sub = document.createElement('div'); sub.className = 'abiq-kpi-sub'; sub.textContent = item.subtext;
    card.append(icon, title, value, sub); container.appendChild(card);
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
    row.append(left, kickoff, right, chevron); container.appendChild(row);
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
    row.append(check, team, probability, confidence); container.appendChild(row);
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

function teamLogo(team) {
  const slug = TEAM_LOGO_SLUGS[team] ?? team.toLowerCase();
  return `https://a.espncdn.com/i/teamlogos/nfl/500/${slug}.png`;
}

function forecastFromRanking(item) {
  const [favorite, underdog] = String(item.label ?? '').split('·').map((part) => part.trim());
  const probability = Number(item.value ?? 0);
  const upsetPressure = Math.max(0, Math.min(100, Math.round(200 - 2 * probability)));
  return {
    favorite,
    underdog,
    probability,
    display: item.display ?? `${probability.toFixed(1)}%`,
    confidence: probability >= 70 ? 'High' : 'Medium',
    upsetPressure,
    read: FORECAST_READS[favorite] ?? 'Representative forecast signal for the static weekly slate.'
  };
}

function renderForecastBoard(parentElement, data) {
  const board = parentElement.querySelector('#abiq-forecast-board');
  board.replaceChildren();
  (data.weekly_rankings ?? []).forEach((item, index) => {
    const forecast = forecastFromRanking(item);
    const row = document.createElement('div'); row.className = 'abiq-forecast-row';
    const rank = document.createElement('div'); rank.className = 'abiq-forecast-rank'; rank.textContent = String(index + 1).padStart(2, '0');

    const matchup = document.createElement('div'); matchup.className = 'abiq-forecast-matchup';
    const logos = document.createElement('div'); logos.className = 'abiq-logo-pair';
    const favoriteLogo = document.createElement('img'); favoriteLogo.src = teamLogo(forecast.favorite); favoriteLogo.alt = `${forecast.favorite} logo`;
    const underdogLogo = document.createElement('img'); underdogLogo.src = teamLogo(forecast.underdog); underdogLogo.alt = `${forecast.underdog} logo`;
    logos.append(favoriteLogo, underdogLogo);
    const matchupCopy = document.createElement('div');
    const favorite = document.createElement('strong'); favorite.textContent = forecast.favorite;
    const opponent = document.createElement('span'); opponent.textContent = `over ${forecast.underdog}`;
    matchupCopy.append(favorite, opponent); matchup.append(logos, matchupCopy);

    const signal = document.createElement('div'); signal.className = 'abiq-forecast-signal';
    const signalTop = document.createElement('div'); signalTop.className = 'abiq-forecast-signal-top';
    const probability = document.createElement('strong'); probability.textContent = forecast.display;
    const probabilityLabel = document.createElement('span'); probabilityLabel.textContent = 'win forecast';
    signalTop.append(probability, probabilityLabel);
    const track = document.createElement('div'); track.className = 'abiq-forecast-track';
    const fill = document.createElement('div'); fill.className = 'abiq-forecast-fill'; fill.style.width = `${forecast.probability}%`; track.appendChild(fill);
    signal.append(signalTop, track);

    const confidence = document.createElement('div');
    confidence.className = `abiq-forecast-confidence ${forecast.confidence.toLowerCase()}`;
    confidence.textContent = forecast.confidence;

    const read = document.createElement('div'); read.className = 'abiq-forecast-read'; read.textContent = forecast.read;
    row.append(rank, matchup, signal, confidence, read); board.appendChild(row);
  });
}

function svgElement(name, attributes = {}) {
  const element = document.createElementNS('http://www.w3.org/2000/svg', name);
  Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, String(value)));
  return element;
}

function renderUpsetMatrix(parentElement, data) {
  const container = parentElement.querySelector('#abiq-upset-matrix');
  container.replaceChildren();
  const forecasts = (data.weekly_rankings ?? []).map(forecastFromRanking);
  const width = 620;
  const height = 330;
  const pad = {left: 58, right: 22, top: 30, bottom: 52};
  const xMin = 60;
  const xMax = 85;
  const yMin = 30;
  const yMax = 80;
  const x = (value) => pad.left + ((value - xMin) / (xMax - xMin)) * (width - pad.left - pad.right);
  const y = (value) => height - pad.bottom - ((value - yMin) / (yMax - yMin)) * (height - pad.top - pad.bottom);

  const svg = svgElement('svg', {viewBox: `0 0 ${width} ${height}`, role: 'img', 'aria-label': 'Upset risk matrix comparing favorite win probability and relative upset pressure'});
  svg.classList.add('abiq-upset-svg');

  const zone = svgElement('rect', {x: x(60), y: y(80), width: x(68) - x(60), height: y(60) - y(80), rx: 10});
  zone.classList.add('abiq-upset-zone'); svg.appendChild(zone);
  const zoneLabel = svgElement('text', {x: x(60) + 12, y: y(77)}); zoneLabel.classList.add('abiq-upset-zone-label'); zoneLabel.textContent = 'UPSET ALERT ZONE'; svg.appendChild(zoneLabel);

  [40, 50, 60, 70, 80].forEach((tick) => {
    const line = svgElement('line', {x1: pad.left, x2: width - pad.right, y1: y(tick), y2: y(tick)}); line.classList.add('abiq-chart-grid'); svg.appendChild(line);
    const label = svgElement('text', {x: pad.left - 12, y: y(tick) + 4, 'text-anchor': 'end'}); label.classList.add('abiq-chart-tick'); label.textContent = String(tick); svg.appendChild(label);
  });
  [60, 65, 70, 75, 80, 85].forEach((tick) => {
    const line = svgElement('line', {x1: x(tick), x2: x(tick), y1: pad.top, y2: height - pad.bottom}); line.classList.add('abiq-chart-grid'); svg.appendChild(line);
    const label = svgElement('text', {x: x(tick), y: height - 28, 'text-anchor': 'middle'}); label.classList.add('abiq-chart-tick'); label.textContent = `${tick}%`; svg.appendChild(label);
  });

  const xLabel = svgElement('text', {x: (pad.left + width - pad.right) / 2, y: height - 6, 'text-anchor': 'middle'}); xLabel.classList.add('abiq-chart-axis-label'); xLabel.textContent = 'Favorite win probability →'; svg.appendChild(xLabel);
  const yLabel = svgElement('text', {x: 15, y: height / 2, transform: `rotate(-90 15 ${height / 2})`, 'text-anchor': 'middle'}); yLabel.classList.add('abiq-chart-axis-label'); yLabel.textContent = 'Upset pressure →'; svg.appendChild(yLabel);

  const offsets = [
    {dx: 10, dy: -11}, {dx: 10, dy: 18}, {dx: 10, dy: -10}, {dx: -10, dy: -12, anchor: 'end'}, {dx: -10, dy: 18, anchor: 'end'}
  ];
  forecasts.forEach((forecast, index) => {
    const group = svgElement('g');
    const tier = forecast.upsetPressure >= 72 ? 'high' : forecast.upsetPressure >= 55 ? 'medium' : 'low';
    const circle = svgElement('circle', {cx: x(forecast.probability), cy: y(forecast.upsetPressure), r: 7}); circle.classList.add('abiq-upset-dot', tier);
    const title = svgElement('title'); title.textContent = `${forecast.underdog} upset watch vs ${forecast.favorite}: favorite ${forecast.display}, pressure ${forecast.upsetPressure}`; circle.appendChild(title);
    group.appendChild(circle);
    const offset = offsets[index] ?? {dx: 9, dy: -9};
    const label = svgElement('text', {x: x(forecast.probability) + offset.dx, y: y(forecast.upsetPressure) + offset.dy, 'text-anchor': offset.anchor ?? 'start'});
    label.classList.add('abiq-upset-label'); label.textContent = `${forecast.favorite}–${forecast.underdog}`; group.appendChild(label);
    svg.appendChild(group);
  });
  container.appendChild(svg);
}

function renderUpsetAlerts(parentElement, data) {
  const container = parentElement.querySelector('#abiq-upset-alerts');
  container.replaceChildren();
  const forecasts = (data.weekly_rankings ?? []).map(forecastFromRanking).sort((a, b) => b.upsetPressure - a.upsetPressure).slice(0, 3);
  forecasts.forEach((forecast) => {
    const tier = forecast.upsetPressure >= 72 ? 'High watch' : forecast.upsetPressure >= 62 ? 'Elevated' : 'Monitor';
    const card = document.createElement('article'); card.className = 'abiq-upset-alert abiq-surface';
    const top = document.createElement('div'); top.className = 'abiq-upset-alert-top';
    const teams = document.createElement('div'); teams.className = 'abiq-upset-teams';
    const underdogLogo = document.createElement('img'); underdogLogo.src = teamLogo(forecast.underdog); underdogLogo.alt = `${forecast.underdog} logo`;
    const favoriteLogo = document.createElement('img'); favoriteLogo.src = teamLogo(forecast.favorite); favoriteLogo.alt = `${forecast.favorite} logo`;
    teams.append(underdogLogo, favoriteLogo);
    const badge = document.createElement('span'); badge.className = 'abiq-upset-tier'; badge.textContent = tier;
    top.append(teams, badge);
    const title = document.createElement('h3'); title.textContent = `${forecast.underdog} over ${forecast.favorite}`;
    const meta = document.createElement('div'); meta.className = 'abiq-upset-meta'; meta.textContent = `${forecast.favorite} favorite ${forecast.display} · Upset pressure ${forecast.upsetPressure}`;
    const copy = document.createElement('p'); copy.textContent = UPSET_READS[forecast.underdog] ?? 'A closer forecast raises the representative underdog watch level.';
    card.append(top, title, meta, copy); container.appendChild(card);
  });
}

function renderForecasts(parentElement, data) {
  renderBars(parentElement.querySelector('#abiq-weekly-bars'), data.weekly_rankings?.slice(0, 3));
  renderForecastBoard(parentElement, data);
  renderUpsetMatrix(parentElement, data);
  renderUpsetAlerts(parentElement, data);
}

function renderReliability(parentElement, data) {
  const container = parentElement.querySelector('#abiq-reliability-chart');
  container.replaceChildren();
  for (const item of data.confidence_reliability ?? []) {
    const row = document.createElement('div');
    row.className = 'abiq-reliability-row';

    const label = document.createElement('div');
    label.className = 'abiq-reliability-label';
    const threshold = document.createElement('strong'); threshold.textContent = item.threshold;
    const games = document.createElement('span'); games.textContent = `${item.games} games`;
    label.append(threshold, games);

    const plot = document.createElement('div');
    plot.className = 'abiq-reliability-plot';

    const makeSeries = (kind, labelText, value) => {
      const series = document.createElement('div');
      series.className = `abiq-reliability-series ${kind}`;
      const seriesLabel = document.createElement('span'); seriesLabel.textContent = labelText;
      const track = document.createElement('div'); track.className = 'abiq-reliability-track';
      const fill = document.createElement('div'); fill.className = 'abiq-reliability-fill'; fill.style.width = `${value}%`; track.appendChild(fill);
      const display = document.createElement('strong'); display.textContent = `${value.toFixed(1)}%`;
      series.append(seriesLabel, track, display);
      return series;
    };

    plot.append(
      makeSeries('predicted', 'Model', Number(item.predicted)),
      makeSeries('observed', 'Actual', Number(item.observed))
    );
    row.append(label, plot);
    container.appendChild(row);
  }
}

function renderPipeline(parentElement, data) {
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
  renderReliability(parentElement, data);
  renderPipeline(parentElement, data);
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
  renderForecasts(parentElement, data);
  renderPerformance(parentElement, data);
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