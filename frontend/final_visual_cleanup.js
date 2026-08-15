/* Final live-site QA behavior overrides.
   Loaded after showcase_exec.js so the existing initialization flow calls these
   refined renderers without duplicating the full component implementation. */

renderUpsetMatrix = function(parentElement, data) {
  const container = parentElement.querySelector('#abiq-upset-matrix');
  container.replaceChildren();
  const forecasts = (data.weekly_rankings ?? []).map(forecastFromRanking);
  const width = 620;
  const height = 350;
  const pad = {left: 64, right: 28, top: 36, bottom: 62};
  const xMin = 60;
  const xMax = 85;
  const yMin = 30;
  const yMax = 80;
  const x = (value) => pad.left + ((value - xMin) / (xMax - xMin)) * (width - pad.left - pad.right);
  const y = (value) => height - pad.bottom - ((value - yMin) / (yMax - yMin)) * (height - pad.top - pad.bottom);

  const svg = svgElement('svg', {
    viewBox: `0 0 ${width} ${height}`,
    role: 'img',
    'aria-label': 'Upset risk matrix comparing favorite win probability and relative upset pressure'
  });
  svg.classList.add('abiq-upset-svg');

  const backgroundLayer = svgElement('g');
  const markerLayer = svgElement('g');
  const leaderLayer = svgElement('g');
  const labelLayer = svgElement('g');

  const zone = svgElement('rect', {
    x: x(60),
    y: y(80),
    width: x(68) - x(60),
    height: y(60) - y(80),
    rx: 10
  });
  zone.classList.add('abiq-upset-zone');
  backgroundLayer.appendChild(zone);

  [40, 50, 60, 70, 80].forEach((tick) => {
    const line = svgElement('line', {
      x1: pad.left,
      x2: width - pad.right,
      y1: y(tick),
      y2: y(tick)
    });
    line.classList.add('abiq-chart-grid');
    backgroundLayer.appendChild(line);

    const label = svgElement('text', {
      x: pad.left - 12,
      y: y(tick) + 4,
      'text-anchor': 'end'
    });
    label.classList.add('abiq-chart-tick');
    label.textContent = String(tick);
    backgroundLayer.appendChild(label);
  });

  [60, 65, 70, 75, 80, 85].forEach((tick) => {
    const line = svgElement('line', {
      x1: x(tick),
      x2: x(tick),
      y1: pad.top,
      y2: height - pad.bottom
    });
    line.classList.add('abiq-chart-grid');
    backgroundLayer.appendChild(line);

    const label = svgElement('text', {
      x: x(tick),
      y: height - 34,
      'text-anchor': 'middle'
    });
    label.classList.add('abiq-chart-tick');
    label.textContent = `${tick}%`;
    backgroundLayer.appendChild(label);
  });

  const xLabel = svgElement('text', {
    x: (pad.left + width - pad.right) / 2,
    y: height - 8,
    'text-anchor': 'middle'
  });
  xLabel.classList.add('abiq-chart-axis-label');
  xLabel.textContent = 'Favorite win probability →';
  backgroundLayer.appendChild(xLabel);

  const yLabel = svgElement('text', {
    x: 18,
    y: height / 2,
    transform: `rotate(-90 18 ${height / 2})`,
    'text-anchor': 'middle'
  });
  yLabel.classList.add('abiq-chart-axis-label');
  yLabel.textContent = 'Upset pressure →';
  backgroundLayer.appendChild(yLabel);

  const zoneLabel = svgElement('text', {x: x(60) + 12, y: y(77)});
  zoneLabel.classList.add('abiq-upset-zone-label');
  zoneLabel.textContent = 'UPSET ALERT ZONE';
  labelLayer.appendChild(zoneLabel);

  /* Labels remain below their markers. Short leader lines make the point-to-label
     relationship explicit; the two closest points are pushed apart horizontally
     and vertically so PHI–WAS and CIN–TB cannot be confused. */
  const labelLayout = [
    {dx: 0, dy: 25},
    {dx: 0, dy: 25},
    {dx: 0, dy: 25},
    {dx: 40, dy: 31},
    {dx: -40, dy: 57}
  ];

  forecasts.forEach((forecast, index) => {
    const tier = forecast.upsetPressure >= 72 ? 'high' : forecast.upsetPressure >= 55 ? 'medium' : 'low';
    const markerX = x(forecast.probability);
    const markerY = y(forecast.upsetPressure);
    const circle = svgElement('circle', {
      cx: markerX,
      cy: markerY,
      r: 7
    });
    circle.classList.add('abiq-upset-dot', tier);
    const title = svgElement('title');
    title.textContent = `${forecast.underdog} upset watch vs ${forecast.favorite}: favorite ${forecast.display}, pressure ${forecast.upsetPressure}`;
    circle.appendChild(title);
    markerLayer.appendChild(circle);

    const layout = labelLayout[index] ?? {dx: 0, dy: 25};
    const labelX = markerX + layout.dx;
    const labelY = markerY + layout.dy;
    const leaderY = labelY - 13;
    const leader = svgElement('polyline', {
      points: `${markerX},${markerY + 8} ${markerX},${leaderY} ${labelX},${leaderY}`
    });
    leader.classList.add('abiq-upset-leader');
    leaderLayer.appendChild(leader);

    const label = svgElement('text', {
      x: labelX,
      y: labelY,
      'text-anchor': 'middle'
    });
    label.classList.add('abiq-upset-label');
    label.textContent = `${forecast.favorite}–${forecast.underdog}`;
    labelLayer.appendChild(label);
  });

  svg.append(backgroundLayer, markerLayer, leaderLayer, labelLayer);
  container.appendChild(svg);
};

renderReliability = function(parentElement, data) {
  const container = parentElement.querySelector('#abiq-reliability-chart');
  container.replaceChildren();

  const points = (data.confidence_reliability ?? []).map((item) => ({
    threshold: Number(String(item.threshold).replace(/[^0-9.]/g, '')),
    thresholdLabel: item.threshold,
    observed: Number(item.observed)
  }));
  if (!points.length) return;

  const width = 720;
  const height = 380;
  const pad = {left: 82, right: 74, top: 48, bottom: 86};
  const xMin = 53;
  const xMax = 72;
  const yMin = 64;
  const yMax = 81.5;
  const x = (value) => pad.left + ((value - xMin) / (xMax - xMin)) * (width - pad.left - pad.right);
  const y = (value) => height - pad.bottom - ((value - yMin) / (yMax - yMin)) * (height - pad.top - pad.bottom);

  const svg = svgElement('svg', {
    viewBox: `0 0 ${width} ${height}`,
    role: 'img',
    'aria-label': 'Observed win accuracy rises as ABIQ forecast confidence increases'
  });
  svg.classList.add('abiq-reliability-svg');

  [65, 70, 75, 80].forEach((tick) => {
    const grid = svgElement('line', {
      x1: pad.left,
      x2: width - pad.right,
      y1: y(tick),
      y2: y(tick)
    });
    grid.classList.add('abiq-reliability-grid');
    svg.appendChild(grid);

    const label = svgElement('text', {
      x: pad.left - 14,
      y: y(tick) + 4,
      'text-anchor': 'end'
    });
    label.classList.add('abiq-reliability-tick');
    label.textContent = `${tick}%`;
    svg.appendChild(label);
  });

  const xAxis = svgElement('line', {
    x1: pad.left,
    x2: width - pad.right,
    y1: height - pad.bottom,
    y2: height - pad.bottom
  });
  xAxis.classList.add('abiq-reliability-axis');
  svg.appendChild(xAxis);

  const yAxis = svgElement('line', {
    x1: pad.left,
    x2: pad.left,
    y1: pad.top,
    y2: height - pad.bottom
  });
  yAxis.classList.add('abiq-reliability-axis');
  svg.appendChild(yAxis);

  points.forEach((point) => {
    const tick = svgElement('line', {
      x1: x(point.threshold),
      x2: x(point.threshold),
      y1: height - pad.bottom,
      y2: height - pad.bottom + 7
    });
    tick.classList.add('abiq-reliability-axis');
    svg.appendChild(tick);

    const label = svgElement('text', {
      x: x(point.threshold),
      y: height - pad.bottom + 27,
      'text-anchor': 'middle'
    });
    label.classList.add('abiq-reliability-tick');
    label.textContent = point.thresholdLabel;
    svg.appendChild(label);
  });

  const polyline = svgElement('polyline', {
    points: points.map((point) => `${x(point.threshold)},${y(point.observed)}`).join(' ')
  });
  polyline.classList.add('abiq-reliability-line');
  svg.appendChild(polyline);

  points.forEach((point) => {
    const marker = svgElement('circle', {
      cx: x(point.threshold),
      cy: y(point.observed),
      r: 4.5
    });
    marker.classList.add('abiq-reliability-point');
    svg.appendChild(marker);

    const value = svgElement('text', {
      x: x(point.threshold),
      y: y(point.observed) - 13,
      'text-anchor': 'middle'
    });
    value.classList.add('abiq-reliability-value');
    value.textContent = `${point.observed.toFixed(1)}%`;
    svg.appendChild(value);
  });

  const xTitle = svgElement('text', {
    x: (pad.left + width - pad.right) / 2,
    y: height - 15,
    'text-anchor': 'middle'
  });
  xTitle.classList.add('abiq-reliability-axis-title');
  xTitle.textContent = 'Forecast confidence threshold →';
  svg.appendChild(xTitle);

  const yTitle = svgElement('text', {
    x: 22,
    y: (pad.top + height - pad.bottom) / 2,
    transform: `rotate(-90 22 ${(pad.top + height - pad.bottom) / 2})`,
    'text-anchor': 'middle'
  });
  yTitle.classList.add('abiq-reliability-axis-title');
  yTitle.textContent = 'Observed win % →';
  svg.appendChild(yTitle);

  container.appendChild(svg);
};