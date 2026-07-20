#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Pembuatan chart interaktif dari Statistical Report dan Insight Report."""

from typing import Any

import plotly.graph_objects as go

from modules.utils.logger import get_logger

logger = get_logger(__name__)


def _bar_chart_from_distribution(
    distribution: dict[str, Any] | None, title: str, x_title: str, y_title: str
) -> go.Figure | None:
    """Bar chart generik dari dict distribusi {kategori: jumlah}."""
    if not distribution:
        return None

    sorted_items = sorted(distribution.items(), key=lambda kv: kv[1], reverse=True)
    labels, values = zip(*sorted_items)

    fig = go.Figure(data=go.Bar(x=labels, y=values))
    fig.update_layout(title=title, xaxis_title=x_title, yaxis_title=y_title)
    return fig


def _line_chart_from_series(
    series: dict[str, Any] | None, title: str, x_title: str, y_title: str
) -> go.Figure | None:
    """Line chart generik dari dict tren {periode: nilai}, urut berdasarkan key."""
    if not series:
        return None

    sorted_items = sorted(series.items(), key=lambda kv: kv[0])
    labels, values = zip(*sorted_items)

    fig = go.Figure(data=go.Scatter(x=labels, y=values, mode="lines+markers"))
    fig.update_layout(title=title, xaxis_title=x_title, yaxis_title=y_title)
    return fig


def _heatmap_from_correlation(correlation: dict[str, dict[str, float]] | None) -> go.Figure | None:
    """Heatmap korelasi dari matriks korelasi bentuk nested dict."""
    if not correlation:
        return None

    labels = list(correlation.keys())
    z = [[correlation[row].get(col) for col in labels] for row in labels]

    fig = go.Figure(data=go.Heatmap(z=z, x=labels, y=labels, colorscale="RdBu", zmid=0))
    fig.update_layout(title="Korelasi Antar Variabel Numerik")
    return fig


def _table_from_insights(insights: list[dict[str, Any]] | None) -> go.Figure | None:
    """Tabel ringkasan insight (kategori + temuan)."""
    if not insights:
        return None

    categories = [item.get("category", "-") for item in insights]
    findings = [item.get("finding", "-") for item in insights]

    fig = go.Figure(
        data=go.Table(
            header={"values": ["Kategori", "Temuan"], "align": "left"},
            cells={"values": [categories, findings], "align": "left"},
        )
    )
    fig.update_layout(title="Ringkasan Insight")
    return fig


def chart_jenis_bencana(statistical_report: dict[str, Any]) -> go.Figure | None:
    """Bar chart distribusi jenis bencana."""
    return _bar_chart_from_distribution(
        statistical_report.get("distribution_jenis_bencana"),
        title="Distribusi Jenis Bencana",
        x_title="Jenis Bencana",
        y_title="Jumlah Kejadian",
    )


def chart_kecamatan(statistical_report: dict[str, Any]) -> go.Figure | None:
    """Bar chart distribusi kejadian per kecamatan."""
    return _bar_chart_from_distribution(
        statistical_report.get("distribution_kecamatan"),
        title="Distribusi Kejadian per Kecamatan",
        x_title="Kecamatan",
        y_title="Jumlah Kejadian",
    )


def chart_yearly_trend(statistical_report: dict[str, Any]) -> go.Figure | None:
    """Line chart tren kejadian per tahun."""
    yearly = statistical_report.get("temporal_distribution", {}).get("yearly_trend")
    return _line_chart_from_series(
        yearly, title="Tren Kejadian per Tahun", x_title="Tahun", y_title="Jumlah Kejadian"
    )


def chart_monthly_trend(statistical_report: dict[str, Any]) -> go.Figure | None:
    """Line chart tren kejadian per bulan."""
    monthly = statistical_report.get("temporal_distribution", {}).get("monthly_trend")
    return _line_chart_from_series(
        monthly, title="Tren Kejadian per Bulan", x_title="Periode", y_title="Jumlah Kejadian"
    )


def chart_correlation_heatmap(statistical_report: dict[str, Any]) -> go.Figure | None:
    """Heatmap korelasi antar variabel numerik."""
    return _heatmap_from_correlation(statistical_report.get("correlation"))


def chart_insight_summary(insight_report: dict[str, Any]) -> go.Figure | None:
    """Tabel visual ringkasan insight hasil Phase 6."""
    return _table_from_insights(insight_report.get("insights"))


def generate_charts(
    statistical_report: dict[str, Any], insight_report: dict[str, Any]
) -> dict[str, go.Figure]:
    """Bangun seluruh chart interaktif dari Statistical Report dan Insight Report."""
    logger.info("Memulai pembuatan chart")

    candidates = {
        "chart_jenis_bencana": chart_jenis_bencana(statistical_report),
        "chart_kecamatan": chart_kecamatan(statistical_report),
        "chart_yearly_trend": chart_yearly_trend(statistical_report),
        "chart_monthly_trend": chart_monthly_trend(statistical_report),
        "chart_correlation_heatmap": chart_correlation_heatmap(statistical_report),
        "chart_insight_summary": chart_insight_summary(insight_report),
    }

    charts = {name: fig for name, fig in candidates.items() if fig is not None}
    skipped = set(candidates) - set(charts)
    if skipped:
        logger.warning(f"Chart dilewati karena data tidak tersedia: {skipped}")

    logger.info(f"Pembuatan chart selesai: {len(charts)} chart dihasilkan")
    return charts