// Port scanner UI logic
(function () {
  const runBtn = document.getElementById('sc-run');
  if (!runBtn) return;

  let lastReport = null;

  runBtn.addEventListener('click', async () => {
    const body = {
      target: document.getElementById('sc-target').value.trim(),
      start_port: +document.getElementById('sc-start').value,
      end_port: +document.getElementById('sc-end').value,
      timeout: +document.getElementById('sc-timeout').value,
      threads: +document.getElementById('sc-threads').value,
    };
    if (!body.target) return CT.toast('Enter a target', 'warning');

    const progress = document.getElementById('sc-progress');
    const results = document.getElementById('sc-results');
    progress.classList.remove('d-none');
    results.classList.add('empty-state');
    results.innerHTML = '<div class="spinner-border text-accent"></div><p>Scanning…</p>';
    runBtn.disabled = true;

    const r = await CT.api('/scanner/api', body);
    progress.classList.add('d-none');
    runBtn.disabled = false;

    if (!r.ok) {
      results.innerHTML = `<i class="bi bi-x-circle"></i><p>${r.error}</p>`;
      return;
    }
    lastReport = r.report;
    document.getElementById('sc-stats').style.display = '';
    document.getElementById('st-target').textContent = r.report.ip;
    document.getElementById('st-total').textContent = r.report.total;
    document.getElementById('st-open').textContent = r.report.open_count;
    document.getElementById('st-time').textContent = r.report.duration + 's';

    const open = r.report.results.filter(x => x.status === 'open');
    if (open.length === 0) {
      results.classList.add('empty-state');
      results.innerHTML = '<i class="bi bi-shield-check"></i><p>No open ports found in range.</p>';
    } else {
      results.classList.remove('empty-state');
      results.innerHTML = `<div class="table-responsive"><table class="table table-dark table-hover align-middle mb-0">
        <thead><tr><th>Port</th><th>Status</th><th>Service</th></tr></thead>
        <tbody>${open.map(p => `<tr>
          <td class="fw-bold text-accent">${p.port}</td>
          <td><span class="badge bg-success">${p.status}</span></td>
          <td class="text-muted">${p.service}</td>
        </tr>`).join('')}</tbody></table></div>`;
    }
    document.getElementById('sc-json').disabled = false;
    document.getElementById('sc-csv').disabled = false;
  });

  async function exportAs(fmt) {
    if (!lastReport) return;
    const r = await fetch(`/scanner/export/${fmt}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(lastReport),
    });
    const blob = await r.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `scan.${fmt}`;
    a.click();
  }
  document.getElementById('sc-json').addEventListener('click', () => exportAs('json'));
  document.getElementById('sc-csv').addEventListener('click', () => exportAs('csv'));
})();
