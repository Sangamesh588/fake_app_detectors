/* script.js — Frontend glue to Python Flask backend (drop-in replacement) */

document.addEventListener('DOMContentLoaded', () => {

    /* -------------------------
       Backend config
       ------------------------- */
    const BACKEND_ORIGIN = "http://localhost:8000"; // <-- change if backend hosted elsewhere
    const HEALTH_INTERVAL_MS = 10000; // refresh backend health every 10s

    /* -------------------------
       Helper utilities
       ------------------------- */
    function el(id) { return document.getElementById(id); }
    function setDisplay(id, visible) {
        const e = el(id);
        if (!e) return;
        e.style.display = visible ? '' : 'none';
    }

    async function checkBackendStatus() {
        const statusEl = el('backendStatus');
        if (!statusEl) return;
        try {
            const r = await fetch(`${BACKEND_ORIGIN}/health`, { method: 'GET' });
            if (!r.ok) throw new Error('status ' + r.status);
            const json = await r.json();
            const ts = json.timestamp ? (new Date(json.timestamp)).toLocaleString() : 'unknown';
            statusEl.textContent = `Backend: UP — ${json.service || 'scanner'} @ ${ts}`;
            statusEl.classList.remove('status-down');
            statusEl.classList.add('status-up');
        } catch (err) {
            statusEl.textContent = `Backend: DOWN — ${err.message}`;
            statusEl.classList.remove('status-up');
            statusEl.classList.add('status-down');
        }
    }

    async function fetchJson(url, opts = {}) {
        const res = await fetch(url, opts);
        if (!res.ok) {
            const txt = await res.text().catch(()=>null);
            throw new Error(`HTTP ${res.status} ${res.statusText} ${txt||''}`);
        }
        return await res.json();
    }

    function clearResultsTable() {
        const body = el('resultsBody');
        if (body) body.innerHTML = '';
    }

    function addResultRow(evidence) {
        const body = el('resultsBody');
        if (!body) return;
        const tr = document.createElement('tr');

        const name = evidence.appName || evidence.app || '';
        const pkg = evidence.package || evidence.packageId || '';
        const risk = (typeof evidence.risk !== 'undefined') ? evidence.risk : (evidence.score || '-');
        const reason = evidence.reason || evidence.description || '';

        const scoreClass = (risk >= 70) ? 'risk-high' : (risk >= 40 ? 'risk-medium' : 'risk-low');

        tr.innerHTML = `
            <td>${escapeHtml(name)}</td>
            <td>${escapeHtml(pkg)}</td>
            <td class="${scoreClass}">${escapeHtml(risk)}</td>
            <td>${escapeHtml(reason)}</td>
        `;

        body.appendChild(tr);
    }

    // basic HTML escaper for inserted text
    function escapeHtml(s) {
        if (s === null || s === undefined) return '';
        return String(s)
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#39;');
    }

    /* -------------------------
       UI references (used by this script)
       ------------------------- */
    const loadingEl = el('loading');
    const resultsTable = el('resultsTable');
    const backendRaw = el('backendRaw'); // optional debug pre element

    // Show/hide helpers
    function showLoading(show = true) {
        if (loadingEl) loadingEl.style.display = show ? 'block' : 'none';
    }
    function showTable(show = true) {
        if (resultsTable) resultsTable.style.display = show ? 'table' : 'none';
    }

    /* -------------------------
       Main scan function — posts to Python backend /scan
       ------------------------- */
    window.scanApps = async function () {
        const brandInput = el('brandInput');
        if (!brandInput) { alert('brandInput element missing'); return; }
        const brand = brandInput.value.trim();
        if (!brand) { alert('Please enter a brand or URL to scan.'); return; }

        showLoading(true);
        showTable(false);
        clearResultsTable();
        if (backendRaw) backendRaw.textContent = '';

        try {
            const payload = { brand, scope: { platform: 'android' } };
            const url = `${BACKEND_ORIGIN}/scan`;

            const data = await fetchJson(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            // Expect { ok: true, results: [ ... ] } per Flask example
            if (!data || !Array.isArray(data.results)) {
                throw new Error('Invalid response structure from backend');
            }

            // Optionally show raw returned JSON for debugging
            if (backendRaw) backendRaw.textContent = JSON.stringify(data, null, 2);

            // Render each candidate
            if (data.results.length === 0) {
                alert('No candidates returned by backend.');
            } else {
                for (const r of data.results) {
                    // The backend may not compute risk — we support both cases.
                    // If backend includes signals/risk, use them; otherwise, display placeholders.
                    // Map backend fields to the frontend display keys expected:
                    // prefer r.appName, fallback to r.app or r.name
                    // prefer r.package, fallback to r.packageId
                    // prefer r.risk or r.score (numeric)
                    const ev = {
                        appName: r.appName || r.name || r.app || '',
                        package: r.package || r.packageId || '',
                        risk: r.risk ?? r.score ?? '-',
                        reason: r.reason || r.description || ''
                    };
                    addResultRow(ev);
                }
            }

            showLoading(false);
            showTable(true);
        } catch (err) {
            showLoading(false);
            showTable(false);
            console.error('Scan failed', err);
            alert('Scan failed: ' + err.message + '\nMake sure your Python backend is running at ' + BACKEND_ORIGIN);
        }
    };

    /* -------------------------
       Navigation active-link on scroll (kept from your original)
       ------------------------- */
    const sections = document.querySelectorAll("section");
    const navLinks = document.querySelectorAll("header nav a");

    window.addEventListener("scroll", () => {
        let current = "";

        sections.forEach(sec => {
            const top = window.scrollY;
            const offset = sec.offsetTop - 150;
            const height = sec.offsetHeight;
            if (top >= offset && top < offset + height) {
                current = sec.getAttribute("id");
            }
        });

        navLinks.forEach(a => {
            a.classList.remove("active");
            if (a.getAttribute("href") === `#${current}`) {
                a.classList.add("active");
            }
        });
    });

    /* -------------------------
       Run an initial backend check and repeat periodically
       ------------------------- */
    checkBackendStatus();
    setInterval(checkBackendStatus, HEALTH_INTERVAL_MS);

    // Expose check function in case you want to call it manually
    window.checkBackendStatus = checkBackendStatus;

    /* -------------------------
       Small UX: hide loading initially if present
       ------------------------- */
    showLoading(false);
});
