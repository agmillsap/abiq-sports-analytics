/* Static full-slate context for the public Week 1 Showcase.
   These matchup probabilities mirror the frozen Week 1 values already used by
   the Showcase. They contain no pool selections, user state, or private strategy. */

const ABIQ_SLATE_CONFIDENCE = [
  {label: 'MIN–GB', value: 51.2, featured: false},
  {label: 'BUF–HOU', value: 51.5, featured: false},
  {label: 'CHI–CAR', value: 56.5, featured: false},
  {label: 'DAL–NYG', value: 56.6, featured: false},
  {label: 'TEN–NYJ', value: 56.7, featured: false},
  {label: 'KC–DEN', value: 57.6, featured: false},
  {label: 'PIT–ATL', value: 60.9, featured: false},
  {label: 'BAL–IND', value: 60.9, featured: false},
  {label: 'LAR–SF', value: 62.4, featured: false},
  {label: 'SEA–NE', value: 62.5, featured: false},
  {label: 'LV–MIA', value: 63.1, featured: false},
  {label: 'CIN–TB', value: 63.8, featured: true},
  {label: 'PHI–WAS', value: 65.0, featured: true},
  {label: 'DET–NO', value: 71.7, featured: true},
  {label: 'JAX–CLE', value: 75.8, featured: true},
  {label: 'LAC–ARI', value: 81.1, featured: true}
];

function ensureSlateConfidenceCard(parentElement) {
  const grid = parentElement.querySelector('#page-forecasts .abiq-forecast-visual-grid');
  const upsetPanel = parentElement.querySelector('#page-forecasts .abiq-upset-panel');
  if (!grid || !upsetPanel) return null;

  let stack = grid.querySelector('.abiq-forecast-side-stack');
  if (!stack) {
    stack = document.createElement('div');
    stack.className = 'abiq-forecast-side-stack';
    grid.insertBefore(stack, upsetPanel);
    stack.appendChild(upsetPanel);
  } else if (upsetPanel.parentElement !== stack) {
    stack.prepend(upsetPanel);
  }

  let card = stack.querySelector('.abiq-slate-profile');
  if (!card) {
    card = document.createElement('article');
    card.className = 'abiq-slate-profile abiq-surface abiq-secondary-surface';
    card.innerHTML = `
      <div class="abiq-visual-heading abiq-slate-heading">
        <div><div class="abiq-eyebrow">SLATE CONFIDENCE PROFILE</div><h3>How concentrated is confidence across the full week?</h3></div>
        <span>16 GAMES</span>
      </div>
      <div class="abiq-slate-summary" aria-label="Week 1 favorite confidence distribution">
        <div class="abiq-slate-summary-card"><span>TIGHT</span><strong>6</strong><small>50–59.9%</small></div>
        <div class="abiq-slate-summary-card"><span>MODERATE</span><strong>7</strong><small>60–69.9%</small></div>
        <div class="abiq-slate-summary-card"><span>STRONG</span><strong>3</strong><small>70%+</small></div>
      </div>
      <div class="abiq-slate-chart" aria-label="Week 1 favorite win probability spectrum"></div>
      <div class="abiq-slate-legend"><span><i class="featured"></i>Featured board</span><span><i></i>Remaining slate</span></div>
      <p class="abiq-chart-note abiq-slate-note">Only 3 of 16 static favorites clear 70%, showing how concentrated the strongest weekly signals are.</p>
    `;
    stack.appendChild(card);
  }
  return card;
}

function renderSlateConfidenceProfile(parentElement) {
  const card = ensureSlateConfidenceCard(parentElement);
  if (!card) return;
  const container = card.querySelector('.abiq-slate-chart');
  if (!container) return;
  container.replaceChildren();

  const width = 620;
  const height = 230;
  const pad = {left: 34, right: 24, top: 32, bottom: 48};
  const xMin = 50;
  const xMax = 85;
  const x = (value) => pad.left + ((value - xMin) / (xMax - xMin)) * (width - pad.left - pad.right);
  const plotTop = pad.top;
  const plotBottom = height - pad.bottom;

  const svg = svgElement('svg', {
    viewBox: `0 0 ${width} ${height}`,
    role: 'img',
    'aria-label': 'Distribution of favorite win probabilities across all 16 static Week 1 Showcase games'
  });
  svg.classList.add('abiq-slate-svg');

  [
    {from: 50, to: 60, tier: 'tight'},
    {from: 60, to: 70, tier: 'moderate'},
    {from: 70, to: 85, tier: 'strong'}
  ].forEach((band) => {
    const rect = svgElement('rect', {
      x: x(band.from), y: plotTop,
      width: x(band.to) - x(band.from),
      height: plotBottom - plotTop,
      rx: 4
    });
    rect.classList.add('abiq-slate-band', band.tier);
    svg.appendChild(rect);
  });

  [50, 60, 70, 80, 85].forEach((tick) => {
    const line = svgElement('line', {x1: x(tick), x2: x(tick), y1: plotTop, y2: plotBottom});
    line.classList.add('abiq-slate-grid');
    svg.appendChild(line);
    const label = svgElement('text', {x: x(tick), y: height - 18, 'text-anchor': 'middle'});
    label.classList.add('abiq-slate-tick');
    label.textContent = `${tick}%`;
    svg.appendChild(label);
  });

  const lanes = [62, 91, 120, 149];
  const lastX = [-999, -999, -999, -999];
  const sorted = [...ABIQ_SLATE_CONFIDENCE].sort((a, b) => a.value - b.value || a.label.localeCompare(b.label));

  sorted.forEach((point) => {
    const pointX = x(point.value);
    let lane = lastX.findIndex((previous) => pointX - previous >= 30);
    if (lane < 0) {
      lane = lastX.reduce((best, previous, index, values) => previous < values[best] ? index : best, 0);
    }
    lastX[lane] = pointX;

    const marker = svgElement('circle', {cx: pointX, cy: lanes[lane], r: point.featured ? 7.5 : 5.5});
    marker.classList.add('abiq-slate-dot', point.featured ? 'featured' : 'context');
    const title = svgElement('title');
    title.textContent = `${point.label}: ${point.value.toFixed(1)}% favorite win probability${point.featured ? ' · featured above' : ''}`;
    marker.appendChild(title);
    svg.appendChild(marker);
  });

  container.appendChild(svg);
}

const renderForecastsBeforeSlateProfile = renderForecasts;
renderForecasts = function(parentElement, data) {
  renderForecastsBeforeSlateProfile(parentElement, data);
  renderSlateConfidenceProfile(parentElement);
};
