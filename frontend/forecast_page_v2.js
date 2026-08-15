/* Forecasts v2: full-slate decision surface.
   Loaded after the prior visual overrides so this renderer becomes the single
   active Forecasts implementation without disturbing Dashboard or Performance. */

function forecastV2Slate(data) {
  return [...(data.forecast_slate ?? [])]
    .map((item) => ({
      favorite: String(item.favorite ?? ''),
      underdog: String(item.underdog ?? ''),
      probability: Number(item.probability ?? 0),
      display: String(item.display ?? ''),
      closeGameProbability: Number(item.close_game_probability ?? 0),
      closeGameDisplay: String(item.close_game_display ?? ''),
      kickoff: String(item.kickoff ?? '')
    }))
    .filter((item) => item.favorite && item.underdog)
    .sort((left, right) => right.probability - left.probability);
}

function forecastV2Tier(probability) {
  if (probability >= 70) return {label: 'High', className: 'high'};
  if (probability >= 60) return {label: 'Medium', className: 'medium'};
  return {label: 'Tight', className: 'tight'};
}

function forecastV2MatchupLabel(item) {
  return `${item.favorite}–${item.underdog}`;
}

function forecastV2Heading(eyebrowText, titleText, metaText = '') {
  const heading = document.createElement('div');
  heading.className = 'abiq-visual-heading abiq-v2-heading';
  const copy = document.createElement('div');
  const eyebrow = document.createElement('div');
  eyebrow.className = 'abiq-eyebrow';
  eyebrow.textContent = eyebrowText;
  const title = document.createElement('h3');
  title.textContent = titleText;
  copy.append(eyebrow, title);
  heading.appendChild(copy);
  if (metaText) {
    const meta = document.createElement('span');
    meta.textContent = metaText;
    heading.appendChild(meta);
  }
  return heading;
}

function renderPreSnapRead(parentElement, slate) {
  const takeaway = parentElement.querySelector('#page-forecasts .abiq-takeaway');
  if (!takeaway) return;

  takeaway.className = 'abiq-pre-snap abiq-surface';
  takeaway.replaceChildren();

  const strongCount = slate.filter((item) => item.probability >= 70).length;
  const highTensionCount = slate.filter((item) => item.closeGameProbability >= 80).length;
  const tightest = [...slate].sort((left, right) => left.probability - right.probability)[0];

  const heading = document.createElement('div');
  heading.className = 'abiq-pre-snap-heading';
  const copy = document.createElement('div');
  const eyebrow = document.createElement('div');
  eyebrow.className = 'abiq-eyebrow';
  eyebrow.textContent = 'PRE-SNAP READ';
  const title = document.createElement('h3');
  title.textContent = 'What the slate is telling us before kickoff.';
  const sub = document.createElement('p');
  sub.textContent = 'A quick read on separation, tension and where Week 1 is least settled.';
  copy.append(eyebrow, title, sub);
  heading.appendChild(copy);
  takeaway.appendChild(heading);

  const insights = [
    {
      label: 'CLEAR FAVORITES',
      value: String(strongCount),
      detail: `of ${slate.length} teams clear a 70% win forecast.`
    },
    {
      label: 'HIGH-TENSION GAMES',
      value: String(highTensionCount),
      detail: `of ${slate.length} carry 80%+ close-game risk.`
    },
    {
      label: 'CLOSEST CALL',
      value: tightest?.display ?? '—',
      detail: tightest ? `${forecastV2MatchupLabel(tightest)} sits nearest to a coin flip.` : 'No slate data available.'
    }
  ];

  const grid = document.createElement('div');
  grid.className = 'abiq-pre-snap-grid';
  insights.forEach((item) => {
    const card = document.createElement('article');
    card.className = 'abiq-pre-snap-card';
    const label = document.createElement('span');
    label.textContent = item.label;
    const value = document.createElement('strong');
    value.textContent = item.value;
    const detail = document.createElement('p');
    detail.textContent = item.detail;
    card.append(label, value, detail);
    grid.appendChild(card);
  });
  takeaway.appendChild(grid);
}

function renderFullSlateBoard(parentElement, slate) {
  const host = parentElement.querySelector('#page-forecasts .abiq-forecast-visual-grid');
  if (!host) return;

  host.className = 'abiq-forecast-v2-stack';
  host.replaceChildren();

  const board = document.createElement('article');
  board.className = 'abiq-full-slate-board abiq-surface';
  board.appendChild(forecastV2Heading('THE BOARD', 'Every Week 1 matchup, ranked by forecast confidence.', `${slate.length} GAMES`));

  const columns = document.createElement('div');
  columns.className = 'abiq-full-slate-columns';
  const splitIndex = Math.ceil(slate.length / 2);
  [slate.slice(0, splitIndex), slate.slice(splitIndex)].forEach((group, columnIndex) => {
    const column = document.createElement('div');
    column.className = `abiq-full-slate-column column-${columnIndex + 1}`;
    group.forEach((item, localIndex) => {
      const overallIndex = columnIndex === 0 ? localIndex : splitIndex + localIndex;
      const tier = forecastV2Tier(item.probability);
      const row = document.createElement('div');
      row.className = 'abiq-full-slate-row';

      const rank = document.createElement('span');
      rank.className = 'abiq-full-slate-rank';
      rank.textContent = String(overallIndex + 1).padStart(2, '0');

      const matchup = document.createElement('div');
      matchup.className = 'abiq-full-slate-matchup';
      const logos = document.createElement('div');
      logos.className = 'abiq-full-slate-logos';
      const favoriteLogo = document.createElement('img');
      favoriteLogo.src = teamLogo(item.favorite);
      favoriteLogo.alt = `${item.favorite} logo`;
      const underdogLogo = document.createElement('img');
      underdogLogo.src = teamLogo(item.underdog);
      underdogLogo.alt = `${item.underdog} logo`;
      logos.append(favoriteLogo, underdogLogo);

      const matchupCopy = document.createElement('div');
      const favorite = document.createElement('strong');
      favorite.textContent = item.favorite;
      const opponent = document.createElement('span');
      opponent.textContent = `over ${item.underdog}`;
      const kickoff = document.createElement('small');
      kickoff.textContent = item.kickoff;
      matchupCopy.append(favorite, opponent, kickoff);
      matchup.append(logos, matchupCopy);

      const signal = document.createElement('div');
      signal.className = 'abiq-full-slate-signal';
      const signalTop = document.createElement('div');
      signalTop.className = 'abiq-full-slate-signal-top';
      const probability = document.createElement('strong');
      probability.textContent = item.display;
      const signalLabel = document.createElement('span');
      signalLabel.textContent = 'win forecast';
      signalTop.append(probability, signalLabel);
      const track = document.createElement('div');
      track.className = 'abiq-full-slate-track';
      const fill = document.createElement('div');
      fill.className = 'abiq-full-slate-fill';
      fill.style.width = `${Math.max(0, Math.min(100, item.probability))}%`;
      track.appendChild(fill);
      signal.append(signalTop, track);

      const badge = document.createElement('span');
      badge.className = `abiq-full-slate-tier ${tier.className}`;
      badge.textContent = tier.label;

      row.append(rank, matchup, signal, badge);
      column.appendChild(row);
    });
    columns.appendChild(column);
  });

  board.appendChild(columns);
  host.appendChild(board);
  host.appendChild(renderPressureMap(slate));
}

function renderPressureMap(slate) {
  const panel = document.createElement('article');
  panel.className = 'abiq-pressure-panel abiq-surface abiq-secondary-surface';
  panel.appendChild(forecastV2Heading('PRESSURE MAP', 'Where confidence and game tension collide.', 'WIN PROBABILITY × CLOSE-GAME RISK'));

  const layout = document.createElement('div');
  layout.className = 'abiq-pressure-layout';
  const chart = document.createElement('div');
  chart.className = 'abiq-pressure-chart';

  const width = 900;
  const height = 430;
  const pad = {left: 72, right: 28, top: 34, bottom: 72};
  const xMin = 50;
  const xMax = 85;
  const yMin = 45;
  const yMax = 100;
  const x = (value) => pad.left + ((value - xMin) / (xMax - xMin)) * (width - pad.left - pad.right);
  const y = (value) => height - pad.bottom - ((value - yMin) / (yMax - yMin)) * (height - pad.top - pad.bottom);

  const svg = svgElement('svg', {
    viewBox: `0 0 ${width} ${height}`,
    role: 'img',
    'aria-label': 'Pressure Map comparing favorite win probability with close-game risk for all sixteen Week 1 games'
  });
  svg.classList.add('abiq-pressure-svg');

  const tensionZone = svgElement('rect', {
    x: pad.left,
    y: y(100),
    width: width - pad.left - pad.right,
    height: y(80) - y(100),
    rx: 12
  });
  tensionZone.classList.add('abiq-pressure-zone');
  svg.appendChild(tensionZone);

  [50, 60, 70, 80, 90, 100].forEach((tick) => {
    const grid = svgElement('line', {x1: pad.left, x2: width - pad.right, y1: y(tick), y2: y(tick)});
    grid.classList.add('abiq-pressure-grid');
    svg.appendChild(grid);
    const label = svgElement('text', {x: pad.left - 14, y: y(tick) + 4, 'text-anchor': 'end'});
    label.classList.add('abiq-pressure-tick');
    label.textContent = `${tick}%`;
    svg.appendChild(label);
  });

  [50, 55, 60, 65, 70, 75, 80, 85].forEach((tick) => {
    const grid = svgElement('line', {x1: x(tick), x2: x(tick), y1: pad.top, y2: height - pad.bottom});
    grid.classList.add('abiq-pressure-grid');
    svg.appendChild(grid);
    const label = svgElement('text', {x: x(tick), y: height - 40, 'text-anchor': 'middle'});
    label.classList.add('abiq-pressure-tick');
    label.textContent = `${tick}%`;
    svg.appendChild(label);
  });

  const zoneLabel = svgElement('text', {x: pad.left + 14, y: y(96)});
  zoneLabel.classList.add('abiq-pressure-zone-label');
  zoneLabel.textContent = 'HIGH-TENSION ZONE';
  svg.appendChild(zoneLabel);

  const xTitle = svgElement('text', {x: (pad.left + width - pad.right) / 2, y: height - 10, 'text-anchor': 'middle'});
  xTitle.classList.add('abiq-pressure-axis');
  xTitle.textContent = 'Favorite win probability →';
  svg.appendChild(xTitle);
  const yTitle = svgElement('text', {x: 22, y: height / 2, transform: `rotate(-90 22 ${height / 2})`, 'text-anchor': 'middle'});
  yTitle.classList.add('abiq-pressure-axis');
  yTitle.textContent = 'Close-game risk →';
  svg.appendChild(yTitle);

  const labeledGames = new Set(['LAC–ARI', 'JAX–CLE', 'DET–NO', 'BUF–HOU', 'MIN–GB']);
  const labelOffsets = {
    'LAC–ARI': {dx: -12, dy: -15, anchor: 'end'},
    'JAX–CLE': {dx: 12, dy: -13, anchor: 'start'},
    'DET–NO': {dx: 12, dy: -13, anchor: 'start'},
    'BUF–HOU': {dx: 14, dy: -12, anchor: 'start'},
    'MIN–GB': {dx: 14, dy: 22, anchor: 'start'}
  };

  slate.forEach((item) => {
    const labelText = forecastV2MatchupLabel(item);
    const marker = svgElement('circle', {
      cx: x(item.probability),
      cy: y(item.closeGameProbability),
      r: item.probability >= 70 ? 7 : 5.5
    });
    const markerClass = item.probability >= 70 ? 'strong' : item.closeGameProbability >= 80 ? 'tension' : 'standard';
    marker.classList.add('abiq-pressure-dot', markerClass);
    const title = svgElement('title');
    title.textContent = `${labelText}: ${item.display} favorite win forecast, ${item.closeGameDisplay} close-game risk`;
    marker.appendChild(title);
    svg.appendChild(marker);

    if (labeledGames.has(labelText)) {
      const offset = labelOffsets[labelText] ?? {dx: 10, dy: -10, anchor: 'start'};
      const label = svgElement('text', {
        x: x(item.probability) + offset.dx,
        y: y(item.closeGameProbability) + offset.dy,
        'text-anchor': offset.anchor
      });
      label.classList.add('abiq-pressure-label');
      label.textContent = labelText;
      svg.appendChild(label);
    }
  });

  chart.appendChild(svg);

  const reads = document.createElement('aside');
  reads.className = 'abiq-pressure-reads';
  const cleanest = [...slate].sort((left, right) => (right.probability - right.closeGameProbability * 0.12) - (left.probability - left.closeGameProbability * 0.12))[0];
  const strongTension = [...slate]
    .filter((item) => item.probability >= 70)
    .sort((left, right) => right.closeGameProbability - left.closeGameProbability)[0];
  const tossup = [...slate].sort((left, right) => left.probability - right.probability)[0];

  const readItems = [
    {
      label: 'CLEANEST FAVORITE',
      title: cleanest ? forecastV2MatchupLabel(cleanest) : '—',
      copy: cleanest ? `${cleanest.display} win forecast with ${cleanest.closeGameDisplay} close-game risk.` : ''
    },
    {
      label: 'STRONG, BUT VOLATILE',
      title: strongTension ? forecastV2MatchupLabel(strongTension) : '—',
      copy: strongTension ? `${strongTension.display} win forecast, but ${strongTension.closeGameDisplay} close-game risk.` : ''
    },
    {
      label: 'TRUE TOSS-UP',
      title: tossup ? forecastV2MatchupLabel(tossup) : '—',
      copy: tossup ? `${tossup.display} leaves almost no separation between the two sides.` : ''
    }
  ];

  readItems.forEach((item) => {
    const card = document.createElement('div');
    card.className = 'abiq-pressure-read';
    const label = document.createElement('span');
    label.textContent = item.label;
    const title = document.createElement('strong');
    title.textContent = item.title;
    const copy = document.createElement('p');
    copy.textContent = item.copy;
    card.append(label, title, copy);
    reads.appendChild(card);
  });

  layout.append(chart, reads);
  panel.appendChild(layout);

  const note = document.createElement('p');
  note.className = 'abiq-chart-note abiq-pressure-note';
  note.textContent = 'Close-game risk is a separate matchup-context signal from win probability. Higher values indicate a profile more consistent with a one-score game; it is not an upset probability.';
  panel.appendChild(note);
  return panel;
}

function renderUpsetWatchV2(parentElement, slate) {
  const section = parentElement.querySelector('#page-forecasts .abiq-upset-watch');
  const container = parentElement.querySelector('#abiq-upset-alerts');
  if (!section || !container) return;

  const heading = section.querySelector('.abiq-flow-heading');
  if (heading) {
    heading.replaceChildren();
    const eyebrow = document.createElement('div');
    eyebrow.className = 'abiq-eyebrow';
    eyebrow.textContent = 'UPSET WATCH';
    const title = document.createElement('h3');
    title.textContent = 'The matchups with the least separation and the most tension.';
    heading.append(eyebrow, title);
  }

  const candidates = [...slate]
    .filter((item) => item.probability < 65 && item.closeGameProbability >= 80)
    .sort((left, right) => (left.probability - right.probability) || (right.closeGameProbability - left.closeGameProbability))
    .slice(0, 3);

  container.replaceChildren();
  candidates.forEach((item) => {
    const card = document.createElement('article');
    card.className = 'abiq-upset-alert abiq-surface abiq-upset-alert-v2';

    const top = document.createElement('div');
    top.className = 'abiq-upset-alert-top';
    const teams = document.createElement('div');
    teams.className = 'abiq-upset-teams';
    const underdogLogo = document.createElement('img');
    underdogLogo.src = teamLogo(item.underdog);
    underdogLogo.alt = `${item.underdog} logo`;
    const favoriteLogo = document.createElement('img');
    favoriteLogo.src = teamLogo(item.favorite);
    favoriteLogo.alt = `${item.favorite} logo`;
    teams.append(underdogLogo, favoriteLogo);
    const badge = document.createElement('span');
    badge.className = 'abiq-upset-tier';
    badge.textContent = 'Watch';
    top.append(teams, badge);

    const title = document.createElement('h3');
    title.textContent = `${item.underdog} vs ${item.favorite}`;
    const meta = document.createElement('div');
    meta.className = 'abiq-upset-meta';
    meta.textContent = `${item.favorite} forecast ${item.display} · Close-game risk ${item.closeGameDisplay}`;
    const copy = document.createElement('p');
    copy.textContent = 'Limited forecast separation plus elevated close-game risk makes this one of the slate’s least settled matchups.';
    card.append(top, title, meta, copy);
    container.appendChild(card);
  });
}

renderForecasts = function(parentElement, data) {
  const slate = forecastV2Slate(data);
  renderPreSnapRead(parentElement, slate);
  renderFullSlateBoard(parentElement, slate);
  renderUpsetWatchV2(parentElement, slate);
};
