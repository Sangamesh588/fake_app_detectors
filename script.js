// script.js — Frontend for Fake App Detector (URL-based)

document.addEventListener("DOMContentLoaded", () => {
  /* -------------------------
     Backend config
     ------------------------- */
  const BACKEND_ORIGIN = "http://127.0.0.1:5000"; // Flask API base
  const HEALTH_INTERVAL_MS = 10000; // 10s health check

  /* -------------------------
     Helpers
     ------------------------- */
  const el = (id) => document.getElementById(id);

  function escapeHtml(s) {
    if (s === null || s === undefined) return "";
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function clearResultsTable() {
    const body = el("resultsBody");
    if (body) body.innerHTML = "";
  }

  function addResultRow(ev) {
    const body = el("resultsBody");
    if (!body) return;

    const tr = document.createElement("tr");

    const score = ev.risk;
    const scoreClass =
      typeof score === "number"
        ? score >= 70
          ? "risk-high"
          : score >= 40
          ? "risk-medium"
          : "risk-low"
        : "";

    tr.innerHTML = `
      <td>${escapeHtml(ev.appName)}</td>
      <td>${escapeHtml(ev.package)}</td>
      <td class="${scoreClass}">${escapeHtml(ev.risk)}</td>
      <td>${escapeHtml(ev.reason)}</td>
    `;

    body.appendChild(tr);
  }

  async function fetchJson(url, opts = {}) {
    const res = await fetch(url, opts);
    if (!res.ok) {
      const txt = await res.text().catch(() => null);
      throw new Error(`HTTP ${res.status} ${res.statusText} ${txt || ""}`);
    }
    return await res.json();
  }

  const loadingEl = el("loading");
  const resultsTable = el("resultsTable");
  const backendRaw = el("backendRaw");
  const backendStatus = el("backendStatus");

  function showLoading(show = true) {
    if (loadingEl) loadingEl.style.display = show ? "block" : "none";
  }

  function showTable(show = true) {
    if (resultsTable) resultsTable.style.display = show ? "table" : "none";
  }

  /* -------------------------
     Backend health check (optional)
     ------------------------- */
  async function checkBackendStatus() {
    if (!backendStatus) return;

    backendStatus.textContent = "Backend: checking...";

    try {
      const data = await fetchJson(`${BACKEND_ORIGIN}/health`);
      const ts = data.timestamp || new Date().toISOString();
      backendStatus.textContent = `Backend: UP — ${data.service || "scanner"} @ ${ts}`;
      backendStatus.classList.remove("status-down");
      backendStatus.classList.add("status-up");
    } catch (err) {
      backendStatus.textContent = `Backend: DOWN — ${err.message}`;
      backendStatus.classList.remove("status-up");
      backendStatus.classList.add("status-down");
    }
  }

  /* -------------------------
     MAIN: Scan a single URL using /api/check-url
     ------------------------- */
  window.scanApps = async function () {
    const input = el("brandInput"); // same input box in your HTML
    if (!input) {
      alert("brandInput element missing in HTML.");
      return;
    }

    const urlToCheck = input.value.trim();
    if (!urlToCheck) {
      alert("Please paste a Play Store URL to scan.");
      return;
    }

    showLoading(true);
    showTable(false);
    clearResultsTable();
    if (backendRaw) backendRaw.textContent = "";

    try {
      const data = await fetchJson(`${BACKEND_ORIGIN}/api/check-url`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: urlToCheck }),
      });

      // Optional: show raw backend response
      if (backendRaw) backendRaw.textContent = JSON.stringify(data, null, 2);

      if (!data.found) {
        alert(
          "This package is not in our sample dataset.\n" +
            "Remember: this is an academic demo with a fixed set of apps."
        );
        showLoading(false);
        showTable(false);
        return;
      }

      const ev = {
        appName: data.appName || "",
        package: data.packageId || "",
        risk: data.risk ?? "-",
        reason: Array.isArray(data.reason)
          ? data.reason.join("; ")
          : data.reason || "",
      };

      addResultRow(ev);

      showLoading(false);
      showTable(true);
    } catch (err) {
      console.error("URL scan failed", err);
      showLoading(false);
      showTable(false);
      alert(
        "Scan failed: " +
          err.message +
          "\nMake sure your Python backend is running at " +
          BACKEND_ORIGIN
      );
    }
  };

  /* -------------------------
     Section scroll highlight (your existing UX)
     ------------------------- */
  const sections = document.querySelectorAll("section");
  const navLinks = document.querySelectorAll("header nav a");

  window.addEventListener("scroll", () => {
    let current = "";

    sections.forEach((sec) => {
      const top = window.scrollY;
      const offset = sec.offsetTop - 150;
      const height = sec.offsetHeight;
      if (top >= offset && top < offset + height) {
        current = sec.getAttribute("id");
      }
    });

    navLinks.forEach((a) => {
      a.classList.remove("active");
      if (a.getAttribute("href") === `#${current}`) {
        a.classList.add("active");
      }
    });
  });

  /* -------------------------
     Init
     ------------------------- */
  checkBackendStatus();
  setInterval(checkBackendStatus, HEALTH_INTERVAL_MS);
  showLoading(false);
});
