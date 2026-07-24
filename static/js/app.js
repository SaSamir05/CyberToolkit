// Shared client-side helpers for CyberToolkit
window.CT = {
  async api(url, body) {
    try {
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body || {}),
      });
      return await r.json();
    } catch (e) {
      return { ok: false, error: e.message };
    }
  },
  toast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return alert(message);
    const el = document.createElement('div');
    el.className = `toast align-items-center text-bg-${type} border-0 fade-in`;
    el.setAttribute('role', 'alert');
    el.innerHTML = `<div class="d-flex"><div class="toast-body">${message}</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>`;
    container.appendChild(el);
    const t = new bootstrap.Toast(el, { delay: 3000 });
    t.show();
    el.addEventListener('hidden.bs.toast', () => el.remove());
  },
  async copy(text) {
    try {
      await navigator.clipboard.writeText(text);
      this.toast('Copied to clipboard', 'success');
    } catch { this.toast('Copy failed', 'danger'); }
  },
  bindCopy(scope) {
    scope.querySelectorAll('[data-copy]').forEach(btn => {
      btn.addEventListener('click', () => this.copy(btn.dataset.copy));
    });
  },
  download(filename, content, type = 'text/plain') {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
  },
};

// Keyboard shortcut: Ctrl/Cmd+K focuses first input on the page
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    const f = document.querySelector('input, textarea');
    if (f) f.focus();
  }
});
