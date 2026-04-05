async function fetchJSON(path) {
  const res = await fetch(path);
  return await res.json();
}

function statCard(label, value) {
  return `<div class="stat glass"><label>${label}</label><strong>${value}</strong></div>`;
}

function drawChart(points) {
  const svg = document.getElementById('chart');
  const width = 820;
  const height = 300;
  const pad = 26;
  const values = points.slice(-24).map(p => p.price_eur_mwh);
  const min = Math.min(...values) - 2;
  const max = Math.max(...values) + 2;
  const toX = (i) => pad + (i * (width - pad * 2)) / (values.length - 1);
  const toY = (v) => height - pad - ((v - min) * (height - pad * 2)) / (max - min);
  const path = values.map((v, i) => `${i === 0 ? 'M' : 'L'} ${toX(i)} ${toY(v)}`).join(' ');
  const area = `${path} L ${toX(values.length - 1)} ${height - pad} L ${toX(0)} ${height - pad} Z`;
  const xLines = [0, 1, 2, 3, 4];
  const yLines = [0, .25, .5, .75, 1];

  svg.innerHTML = `
    ${xLines.map(i => `<line x1="${pad}" y1="${pad + i * (height - pad * 2) / 4}" x2="${width - pad}" y2="${pad + i * (height - pad * 2) / 4}" stroke="rgba(255,255,255,.08)" />`).join('')}
    ${yLines.map(i => `<line x1="${pad + i * (width - pad * 2)}" y1="${pad}" x2="${pad + i * (width - pad * 2)}" y2="${height - pad}" stroke="rgba(255,255,255,.05)" />`).join('')}
    <path d="${area}" fill="#74f3c1" class="area"></path>
    <path d="${path}" stroke="#74f3c1" class="line"></path>
    ${values.map((v, i) => `<circle cx="${toX(i)}" cy="${toY(v)}" r="3.5" fill="#7aa8ff" />`).join('')}
  `;
  const legend = document.createElement('div');
  legend.className = 'legend';
  legend.innerHTML = `<span style="--c:#74f3c1">Market Price</span>`;
  svg.parentElement.appendChild(legend);
  const style = document.createElement('style');
  style.textContent = `.legend span::before{background:var(--c);}`;
  document.head.appendChild(style);
}

async function load() {
  const [summary, series, runs, quality, assets, agents] = await Promise.all([
    fetchJSON('/api/summary'),
    fetchJSON('/api/timeseries'),
    fetchJSON('/api/pipeline-runs'),
    fetchJSON('/api/quality'),
    fetchJSON('/api/assets'),
    fetchJSON('/api/agents')
  ]);

  document.getElementById('stats').innerHTML = [
    statCard('Platform Uptime', summary.platform_uptime),
    statCard('Avg Price', `${summary.avg_price} €/MWh`),
    statCard('Quality Score', `${summary.avg_quality}%`),
    statCard('Demand', `${summary.avg_demand} MW`),
    statCard('Renewable Coverage', `${summary.renewable_coverage}%`),
    statCard('Daily Cost', `€${summary.daily_cost_eur}`),
  ].join('');

  drawChart(series);

  document.getElementById('pipelineRuns').innerHTML = runs.map(run => `
    <div class="item">
      <div class="item-top">
        <strong>${run.name}</strong>
        <span class="badge ${run.status}">${run.status}</span>
      </div>
      <small>${run.owner} · ${run.duration_sec}s · freshness ${run.freshness_min} min</small>
    </div>
  `).join('');

  document.getElementById('qualityChecks').innerHTML = quality.map(check => `
    <div class="item">
      <div class="item-top">
        <strong>${check.name}</strong>
        <span class="badge ${check.result === 'pass' ? 'success' : 'monitoring'}">${check.result}</span>
      </div>
      <small>${check.detail}</small>
    </div>
  `).join('');

  document.getElementById('agents').innerHTML = agents.map(agent => `
    <div class="item">
      <div class="item-top">
        <strong>${agent.name}</strong>
        <span class="badge ${agent.status}">${agent.status}</span>
      </div>
      <small>${agent.purpose}</small>
    </div>
  `).join('');

  document.getElementById('assets').innerHTML = `
    <table>
      <thead>
        <tr><th>Asset</th><th>Region</th><th>Capacity</th><th>Availability</th><th>Latency</th></tr>
      </thead>
      <tbody>
        ${assets.map(asset => `
          <tr>
            <td>${asset.id} · ${asset.type}</td>
            <td>${asset.region}</td>
            <td>${asset.capacity_mw} MW</td>
            <td>${asset.availability_pct}%</td>
            <td>${asset.data_latency_sec}s</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

document.getElementById('runPipelineBtn').addEventListener('click', async () => {
  const res = await fetch('/api/run-demo-pipeline', { method: 'POST' });
  await res.json();
  const toast = document.getElementById('toast');
  toast.classList.remove('hidden');
  setTimeout(() => toast.classList.add('hidden'), 2500);
  load();
});

load();
