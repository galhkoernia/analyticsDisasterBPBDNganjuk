#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Dashboard Integration.
"""

import json
from pathlib import Path
from typing import Any

import pandas as pd

from config.settings import (
    DATA_PROCESSED_DIR,
    OUTPUT_DASHBOARD_DIR,
    OUTPUT_REPORTS_DIR,
)
from modules.utils.helper import ensure_dir
from modules.utils.logger import get_logger

logger = get_logger(__name__)

_MAP_POINT_COLUMNS = [
    "latitude", "longitude", "jenis_bencana", "kecamatan", "koordinat_parse_status",
]


def _load_json_report(filename: str) -> dict[str, Any]:
    """Baca satu file report JSON dari outputs/reports. Kosong jika tidak ditemukan."""
    path = OUTPUT_REPORTS_DIR / filename
    if not path.exists():
        logger.warning(f"Report tidak ditemukan, dashboard menampilkan data kosong: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_map_points(filename: str = "clean_dataset.csv") -> list[dict[str, Any]]:
    """Baca titik koordinat valid dari Clean Dataset untuk peta interaktif."""
    path = DATA_PROCESSED_DIR / filename
    if not path.exists():
        logger.warning(f"Clean Dataset tidak ditemukan, peta akan kosong: {path}")
        return []

    df = pd.read_csv(path, usecols=lambda c: c in _MAP_POINT_COLUMNS)
    if "koordinat_parse_status" not in df.columns:
        return []

    valid = df[df["koordinat_parse_status"].astype(str).str.startswith("ok", na=False)]
    valid = valid.dropna(subset=["latitude", "longitude"])
    return valid[["latitude", "longitude", "jenis_bencana", "kecamatan"]].to_dict(orient="records")


def _collect_dashboard_data() -> dict[str, Any]:
    """Kumpulkan seluruh data siap-pakai dari output Analytics Engine yang sudah ada."""
    return {
        "quality": _load_json_report("data_quality_report.json"),
        "statistics": _load_json_report("statistical_report.json"),
        "insights": _load_json_report("insight_report.json"),
        "eda": _load_json_report("eda_report.json"),
        "map_points": _load_map_points(),
    }


def _write_asset(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_dashboard() -> None:
    """Bangun Dashboard Integration (Phase 8) dari output Analytics Engine yang sudah ada."""
    logger.info("Memulai Dashboard Integration")

    dashboard_data = _collect_dashboard_data()

    css_path = OUTPUT_DASHBOARD_DIR / "assets" / "css" / "style.css"
    js_path = OUTPUT_DASHBOARD_DIR / "assets" / "js" / "dashboard.js"
    index_path = OUTPUT_DASHBOARD_DIR / "index.html"

    ensure_dir(OUTPUT_DASHBOARD_DIR / "assets" / "icons")
    ensure_dir(OUTPUT_DASHBOARD_DIR / "assets" / "images")

    _write_asset(css_path, _CSS_CONTENT)
    _write_asset(js_path, _JS_CONTENT)

    data_json = json.dumps(dashboard_data, ensure_ascii=False, default=str)
    html_content = _HTML_TEMPLATE.replace("__DASHBOARD_DATA_JSON__", data_json)
    _write_asset(index_path, html_content)

    logger.info(f"Dashboard disimpan: {index_path}")


_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Disaster Analytics Dashboard</title>
<link rel="stylesheet" href="assets/css/style.css">
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-name">Disaster Analytics</span>
      </div>
      <nav class="nav">
        <a class="nav-item active" data-target="executive" href="#executive">Executive Summary</a>
        <a class="nav-item" data-target="temporal" href="#temporal">Temporal Analytics</a>
        <a class="nav-item" data-target="spatial" href="#spatial">Spatial Analytics</a>
        <a class="nav-item" data-target="disaster" href="#disaster">Disaster Analytics</a>
        <a class="nav-item" data-target="impact" href="#impact">Impact Analytics</a>
        <a class="nav-item" data-target="operational" href="#operational">Operational Analytics</a>
        <a class="nav-item" data-target="insight" href="#insight">Insight Panel</a>
      </nav>
      <div class="sidebar-footer">Disaster Analytics Engine</div>
    </aside>

    <main class="main">
      <section id="executive" class="section hero">
        <div class="hero-text">
          <span class="eyebrow">Ringkasan</span>
          <h1>Executive Summary</h1>
          <p id="generated-at" class="hero-meta"></p>
        </div>
        <div class="cards" id="executive-cards"></div>
      </section>

      <section id="temporal" class="section">
        <h2 class="section-title">Temporal Analytics</h2>
        <div class="card-row">
          <div class="chart-card"><div id="chart-yearly-trend"></div></div>
          <div class="chart-card"><div id="chart-monthly-trend"></div></div>
        </div>
      </section>

      <section id="spatial" class="section">
        <h2 class="section-title">Spatial Analytics</h2>
        <div class="card-row">
          <div class="chart-card"><div id="chart-kecamatan-rank"></div></div>
          <div class="chart-card"><div id="chart-map"></div></div>
        </div>
      </section>

      <section id="disaster" class="section">
        <h2 class="section-title">Disaster Analytics</h2>
        <div class="card-row">
          <div class="chart-card"><div id="chart-jenis-bencana-pie"></div></div>
          <div class="chart-card"><div id="chart-jenis-bencana-bar"></div></div>
        </div>
      </section>

      <section id="impact" class="section">
        <h2 class="section-title">Impact Analytics</h2>
        <div class="cards" id="impact-cards"></div>
        <div class="card-row">
          <div class="chart-card"><div id="chart-top-korban"></div></div>
          <div class="chart-card"><div id="chart-top-kerugian"></div></div>
        </div>
      </section>

      <section id="operational" class="section">
        <h2 class="section-title">Operational Analytics</h2>
        <div class="cards" id="operational-cards"></div>
        <div class="card-row">
          <div class="chart-card"><div id="chart-status-penanganan"></div></div>
        </div>
      </section>

      <section id="insight" class="section section-last">
        <h2 class="section-title">Insight Panel</h2>
        <div class="insight-list" id="insight-list"></div>
      </section>
    </main>
  </div>

  <script>window.__DASHBOARD_DATA__ = __DASHBOARD_DATA_JSON__;</script>
  <script src="assets/js/dashboard.js"></script>
</body>
</html>
"""

_CSS_CONTENT = """
:root {
  --bg: #f5f6fb;
  --sidebar-bg: #12142e;
  --card-bg: #ffffff;
  --text-main: #1c1f2e;
  --text-muted: #868aa3;
  --accent: #4f46e5;
  --accent-soft: #eef0ff;
  --accent-2: #f97316;
  --border: #edeef4;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }

body {
  margin: 0;
  font-family: "Inter", "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--text-main);
}

.layout { display: flex; min-height: 100vh; }

.sidebar {
  width: 250px;
  background: var(--sidebar-bg);
  color: #fff;
  padding: 28px 18px;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.brand { display: flex; align-items: center; gap: 10px; margin-bottom: 36px; }
.brand-icon {
  width: 38px; height: 38px; border-radius: 11px;
  background: linear-gradient(135deg, var(--accent), #7c3aed);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 14px;
}
.brand-name { font-weight: 600; font-size: 15px; letter-spacing: 0.2px; }

.nav { display: flex; flex-direction: column; gap: 4px; flex: 1; }
.nav-item {
  text-decoration: none;
  text-align: left;
  background: none;
  border: none;
  color: #a6a9c2;
  padding: 11px 14px;
  border-radius: 9px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.15s, color 0.15s;
}
.nav-item:hover { background: rgba(255,255,255,0.06); color: #fff; }
.nav-item.active { background: var(--accent); color: #fff; }

.sidebar-footer { font-size: 11px; color: #5c5f7a; padding-top: 16px; }

.main { flex: 1; padding: 0 40px 60px; max-width: 1200px; }

.section { padding: 56px 0; border-bottom: 1px solid var(--border); scroll-margin-top: 24px; }
.section-last { border-bottom: none; }
.section-title { font-size: 20px; font-weight: 700; margin: 0 0 22px; }

.hero { padding-top: 48px; }
.hero-text { margin-bottom: 26px; }
.eyebrow {
  display: inline-block; font-size: 12px; font-weight: 600; letter-spacing: 0.4px;
  color: var(--accent); text-transform: uppercase; margin-bottom: 6px;
}
.hero h1 { font-size: 28px; margin: 0 0 6px; }
.hero-meta { color: var(--text-muted); font-size: 13px; margin: 0; }

.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-top: 8px; }
.stat-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px 22px;
  box-shadow: 0 1px 2px rgba(20,20,50,0.03);
}
.stat-label { font-size: 13px; color: var(--text-muted); margin-bottom: 8px; }
.stat-value { font-size: 26px; font-weight: 700; }
.stat-sub { font-size: 12px; color: var(--text-muted); margin-top: 4px; }

.card-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 18px; }
.chart-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 14px;
  min-height: 380px;
  box-shadow: 0 1px 2px rgba(20,20,50,0.03);
}

.insight-list { display: flex; flex-direction: column; gap: 10px; }
.insight-item {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 13px;
  padding: 15px 18px;
  display: flex;
  gap: 14px;
  align-items: flex-start;
}
.insight-tag {
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  padding: 4px 9px;
  border-radius: 7px;
  flex-shrink: 0;
  margin-top: 2px;
}
.insight-item p { margin: 0; font-size: 14px; line-height: 1.5; }

.empty-state {
  color: var(--text-muted);
  font-size: 13px;
  padding: 40px;
  text-align: center;
}
"""

_JS_CONTENT = """
(function () {
  var data = window.__DASHBOARD_DATA__ || {};
  var quality = data.quality || {};
  var statistics = data.statistics || {};
  var insightsReport = data.insights || {};
  var eda = data.eda || {};
  var mapPoints = data.map_points || [];

  var COLORS = { primary: "#4f46e5", accent: "#f97316" };

  document.getElementById("generated-at").textContent =
    "Digenerate: " + (quality.generated_at || insightsReport.generated_at || "-");

  initScrollSpy();
  renderExecutiveSummary();
  renderTemporal();
  renderSpatial();
  renderDisaster();
  renderImpact();
  renderOperational();
  renderInsightPanel();

  function initScrollSpy() {
    var navItems = document.querySelectorAll(".nav-item");
    var sections = document.querySelectorAll(".section");

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          navItems.forEach(function (item) {
            item.classList.toggle("active", item.dataset.target === entry.target.id);
          });
        }
      });
    }, { rootMargin: "-40% 0px -55% 0px", threshold: 0 });

    sections.forEach(function (section) { observer.observe(section); });
  }

  function card(label, value, sublabel) {
    return (
      '<div class="stat-card"><div class="stat-label">' + label +
      '</div><div class="stat-value">' + value + "</div>" +
      (sublabel ? '<div class="stat-sub">' + sublabel + "</div>" : "") +
      "</div>"
    );
  }

  function findInsightValue(category, keyword) {
    var list = insightsReport.insights || [];
    for (var i = 0; i < list.length; i++) {
      var item = list[i];
      if (item.category === category && (!keyword || item.finding.toLowerCase().indexOf(keyword) !== -1)) {
        return item.value;
      }
    }
    return null;
  }

  function sortedEntries(obj) {
    return Object.entries(obj || {}).sort(function (a, b) { return b[1] - a[1]; });
  }

  function layoutFor(title) {
    return {
      title: title,
      margin: { t: 40, b: 40, l: 60, r: 20 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: { family: "Inter, sans-serif", size: 12 },
    };
  }

  function renderExecutiveSummary() {
    var totalKejadian = quality.dataset_summary ? quality.dataset_summary.n_rows : "-";
    var totalKecamatan = statistics.distribution_kecamatan
      ? Object.keys(statistics.distribution_kecamatan).length : "-";
    var jenisDominan = findInsightValue("disaster", "dominan");
    var korbanSummary = (eda.impact || {}).korban_summary || {};
    var qualityScore = quality.quality_score ? quality.quality_score.total_score : "-";

    document.getElementById("executive-cards").innerHTML =
      card("Total Kejadian", totalKejadian) +
      card("Total Kecamatan Terdampak", totalKecamatan) +
      card("Jenis Bencana Dominan", jenisDominan ? jenisDominan.jenis_bencana : "-") +
      card("Total Korban (estimasi)", korbanSummary.sum !== undefined ? Math.round(korbanSummary.sum) : "-") +
      card("Data Quality Score", qualityScore !== "-" ? qualityScore + " / 100" : "-");
  }

  function renderTemporal() {
    var yearly = (statistics.temporal_distribution || {}).yearly_trend || {};
    var monthly = (statistics.temporal_distribution || {}).monthly_trend || {};

    var yearlyKeys = Object.keys(yearly).sort();
    Plotly.newPlot("chart-yearly-trend",
      [{ x: yearlyKeys, y: yearlyKeys.map(function (k) { return yearly[k]; }),
         type: "scatter", mode: "lines+markers", line: { color: COLORS.primary } }],
      layoutFor("Tren Kejadian per Tahun"));

    var monthlyKeys = Object.keys(monthly).sort();
    Plotly.newPlot("chart-monthly-trend",
      [{ x: monthlyKeys, y: monthlyKeys.map(function (k) { return monthly[k]; }),
         type: "scatter", mode: "lines+markers", line: { color: COLORS.accent } }],
      layoutFor("Tren Kejadian per Bulan"));
  }

  function renderSpatial() {
    var kecamatan = sortedEntries(statistics.distribution_kecamatan).slice(0, 15);
    Plotly.newPlot("chart-kecamatan-rank",
      [{ x: kecamatan.map(function (e) { return e[1]; }),
         y: kecamatan.map(function (e) { return e[0]; }),
         type: "bar", orientation: "h", marker: { color: COLORS.primary } }],
      layoutFor("Ranking Kecamatan (Top 15)"));

    if (mapPoints.length > 0) {
      Plotly.newPlot("chart-map", [{
        type: "scattermapbox",
        lat: mapPoints.map(function (p) { return p.latitude; }),
        lon: mapPoints.map(function (p) { return p.longitude; }),
        text: mapPoints.map(function (p) { return p.jenis_bencana + " - " + p.kecamatan; }),
        mode: "markers",
        marker: { size: 8, color: COLORS.accent },
      }], {
        mapbox: { style: "open-street-map", center: { lat: mapPoints[0].latitude, lon: mapPoints[0].longitude }, zoom: 10 },
        margin: { t: 30, b: 0, l: 0, r: 0 },
        title: "Sebaran Kejadian",
      });
    } else {
      document.getElementById("chart-map").innerHTML =
        '<div class="empty-state">Data koordinat tidak tersedia</div>';
    }
  }

  function renderDisaster() {
    var jenis = sortedEntries(statistics.distribution_jenis_bencana);
    Plotly.newPlot("chart-jenis-bencana-pie",
      [{ labels: jenis.map(function (e) { return e[0]; }),
         values: jenis.map(function (e) { return e[1]; }), type: "pie", hole: 0.45 }],
      layoutFor("Persentase Jenis Bencana"));

    Plotly.newPlot("chart-jenis-bencana-bar",
      [{ x: jenis.map(function (e) { return e[0]; }),
         y: jenis.map(function (e) { return e[1]; }), type: "bar", marker: { color: COLORS.primary } }],
      layoutFor("Distribusi Jenis Bencana"));
  }

  function renderImpact() {
    var impact = eda.impact || {};
    var korban = impact.korban_summary || {};
    var rumah = impact.rumah_summary || {};
    var kerugian = impact.kerugian_summary || {};
    var pengungsi = impact.pengungsi_summary || null;

    document.getElementById("impact-cards").innerHTML =
      card("Total Korban", korban.sum !== undefined ? Math.round(korban.sum) : "-") +
      card("Total Rumah Terdampak", rumah.sum !== undefined ? Math.round(rumah.sum) : "-") +
      card("Total Pengungsi", pengungsi && pengungsi.sum !== undefined ? Math.round(pengungsi.sum) : "Data belum tersedia") +
      card("Total Kerugian Material", kerugian.sum !== undefined ? kerugian.sum.toLocaleString("id-ID") : "-");

    var topKorban = impact.top_kecamatan_by_korban || {};
    var topKerugian = impact.top_kecamatan_by_kerugian || {};

    Plotly.newPlot("chart-top-korban",
      [{ x: Object.values(topKorban), y: Object.keys(topKorban), type: "bar", orientation: "h", marker: { color: COLORS.accent } }],
      layoutFor("Top Kecamatan berdasarkan Korban"));

    Plotly.newPlot("chart-top-kerugian",
      [{ x: Object.values(topKerugian), y: Object.keys(topKerugian), type: "bar", orientation: "h", marker: { color: COLORS.primary } }],
      layoutFor("Top Kecamatan berdasarkan Kerugian"));
  }

  function renderOperational() {
    var operational = eda.operational || {};
    var status = operational.status_distribution || {};
    var completion = operational.completion_ratio;
    var duration = operational.reporting_duration_stats || {};
    var qualityScore = quality.quality_score ? quality.quality_score.total_score : "-";

    document.getElementById("operational-cards").innerHTML =
      card("Rasio Penanganan Selesai", (completion !== undefined && completion !== null) ? (completion * 100).toFixed(1) + "%" : "-") +
      card("Rata-rata Durasi Pelaporan", duration.mean_jam !== undefined ? duration.mean_jam.toFixed(1) + " jam" : "-") +
      card("Data Quality Score", qualityScore !== "-" ? qualityScore + " / 100" : "-");

    var statusEntries = Object.entries(status);
    if (statusEntries.length > 0) {
      Plotly.newPlot("chart-status-penanganan",
        [{ labels: statusEntries.map(function (e) { return e[0]; }),
           values: statusEntries.map(function (e) { return e[1]; }), type: "pie", hole: 0.4 }],
        layoutFor("Distribusi Status Penanganan"));
    } else {
      document.getElementById("chart-status-penanganan").innerHTML =
        '<div class="empty-state">Data status penanganan tidak tersedia</div>';
    }
  }

  function renderInsightPanel() {
    var list = insightsReport.insights || [];
    if (list.length === 0) {
      document.getElementById("insight-list").innerHTML =
        '<div class="empty-state">Belum ada insight yang dihasilkan</div>';
      return;
    }
    document.getElementById("insight-list").innerHTML = list.map(function (item) {
      return '<div class="insight-item"><span class="insight-tag">' + item.category +
        '</span><p>' + item.finding + '</p></div>';
    }).join("");
  }
})();
"""