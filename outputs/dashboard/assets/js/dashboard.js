
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
