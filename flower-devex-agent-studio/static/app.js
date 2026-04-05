const state = {
  demoIndex: 0,
  demos: [
    {
      team_name: 'Platform Squad',
      workflow: 'Review pull requests with an agent that suggests fixes and test updates',
      challenge: 'Developers spend too much time on repeated review comments, missing repo context, and manually validating AI-generated code.',
      constraints: 'Must work with GitHub based workflows, respect code ownership, and never bypass tests.',
      objective: 'Reduce review time while keeping correctness and trust high.'
    },
    {
      team_name: 'Developer Productivity',
      workflow: 'Generate release notes and deployment checks from merged pull requests',
      challenge: 'Release coordination is repetitive and error-prone. Engineers manually gather context from many tickets and commits.',
      constraints: 'Needs CI integration and an approval step before publication.',
      objective: 'Improve release confidence and save time during weekly deploys.'
    }
  ]
};

async function runAnalysis(payload) {
  const response = await fetch('/api/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return response.json();
}

function metricCard(label, value) {
  return `<div class="metric"><span>${label}</span><strong>${value}</strong></div>`;
}

function render(data) {
  document.getElementById('resultTitle').textContent = data.title;
  document.getElementById('recommendation').textContent = data.recommendation;
  document.getElementById('metrics').innerHTML = [
    metricCard('AI fit', `${data.metrics.ai_fit}%`),
    metricCard('Trust readiness', `${data.metrics.trust_readiness}%`),
    metricCard('Rollout readiness', `${data.metrics.rollout_readiness}%`),
    metricCard('Time saved', data.metrics.estimated_time_saved),
    metricCard('Pilot', data.metrics.suggested_pilot)
  ].join('');

  document.getElementById('agentCards').innerHTML = data.agent_cards.map(card => `
    <article class="agent-card">
      <div class="agent-top">
        <div class="agent-icon">${card.icon}</div>
        <div>
          <strong>${card.title}</strong>
        </div>
      </div>
      <p>${card.summary}</p>
      <ul>${card.signals.map(item => `<li>${item}</li>`).join('')}</ul>
    </article>
  `).join('');

  document.getElementById('qualityHarness').innerHTML = data.quality_harness.map(item => `
    <div class="list-item">
      <div class="list-head">
        <strong>${item.name}</strong>
        <span class="status">${item.status}</span>
      </div>
      <p>${item.detail}</p>
    </div>
  `).join('');

  document.getElementById('backlog').innerHTML = data.backlog.map(item => `<li>${item}</li>`).join('');
}

function readForm() {
  return {
    team_name: document.getElementById('team').value,
    workflow: document.getElementById('workflow').value,
    challenge: document.getElementById('challenge').value,
    constraints: document.getElementById('constraints').value,
    objective: document.getElementById('objective').value,
  };
}

async function bootstrap(payload = null) {
  const runBtn = document.getElementById('runBtn');
  runBtn.textContent = 'Running…';
  runBtn.disabled = true;
  try {
    const data = await runAnalysis(payload || readForm());
    render(data);
  } catch (error) {
    document.getElementById('recommendation').textContent = 'Something went wrong while running the local analysis. Please refresh and try again.';
    console.error(error);
  } finally {
    runBtn.textContent = 'Run agent studio';
    runBtn.disabled = false;
  }
}

document.getElementById('runBtn').addEventListener('click', () => bootstrap());
document.getElementById('demoBtn').addEventListener('click', () => {
  state.demoIndex = (state.demoIndex + 1) % state.demos.length;
  const demo = state.demos[state.demoIndex];
  document.getElementById('team').value = demo.team_name;
  document.getElementById('workflow').value = demo.workflow;
  document.getElementById('challenge').value = demo.challenge;
  document.getElementById('constraints').value = demo.constraints;
  document.getElementById('objective').value = demo.objective;
  bootstrap(demo);
});

bootstrap(state.demos[0]);
