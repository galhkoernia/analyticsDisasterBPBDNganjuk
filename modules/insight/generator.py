#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Insight Generator: sintesis insight rule-based dari hasil Data Quality
Assessment, Exploratory Data Analysis, dan Statistical Analysis.
"""

import json
from datetime import datetime
from typing import Any

from config.constants import QUALITY_SCORE_WEIGHTS
from config.settings import OUTPUT_REPORTS_DIR
from modules.utils.helper import ensure_dir
from modules.utils.logger import get_logger

logger = get_logger(__name__)


def _insight_top_kecamatan_frekuensi(statistical_report: dict[str, Any]) -> dict[str, Any] | None:
    """Kecamatan dengan frekuensi kejadian tertinggi."""
    distribution = statistical_report.get("distribution_kecamatan")
    if not distribution:
        return None
    top_kecamatan = max(distribution, key=distribution.get)
    return {
        "category": "spatial",
        "finding": f"Kecamatan dengan frekuensi kejadian tertinggi adalah '{top_kecamatan}'",
        "value": {"kecamatan": top_kecamatan, "jumlah_kejadian": distribution[top_kecamatan]},
    }


def _insight_dominant_jenis_bencana(statistical_report: dict[str, Any]) -> dict[str, Any] | None:
    """Jenis bencana paling dominan."""
    distribution = statistical_report.get("distribution_jenis_bencana")
    if not distribution:
        return None
    top_jenis = max(distribution, key=distribution.get)
    return {
        "category": "disaster",
        "finding": f"Jenis bencana paling dominan adalah '{top_jenis}'",
        "value": {"jenis_bencana": top_jenis, "jumlah_kejadian": distribution[top_jenis]},
    }


def _insight_periode_terbanyak(statistical_report: dict[str, Any]) -> dict[str, Any] | None:
    """Periode (bulan) dengan kejadian terbanyak."""
    monthly = statistical_report.get("temporal_distribution", {}).get("monthly_trend")
    if not monthly:
        return None
    top_period = max(monthly, key=monthly.get)
    return {
        "category": "temporal",
        "finding": f"Periode dengan kejadian terbanyak adalah '{top_period}'",
        "value": {"periode": top_period, "jumlah_kejadian": monthly[top_period]},
    }


def _insight_trend(statistical_report: dict[str, Any]) -> dict[str, Any] | None:
    """Tren peningkatan atau penurunan kejadian antar tahun."""
    trend = statistical_report.get("trend_analysis")
    if not trend:
        return None
    return {
        "category": "temporal",
        "finding": (
            f"Jumlah kejadian {trend['direction']} dari {trend['first_year']} "
            f"({trend['first_value']}) ke {trend['last_year']} ({trend['last_value']})"
        ),
        "value": trend,
    }


def _insight_dampak_terbesar(eda_result: dict[str, Any]) -> list[dict[str, Any]]:
    """Dampak terbesar berdasarkan korban dan kerugian material."""
    impact = eda_result.get("impact", {}) or {}
    insights: list[dict[str, Any]] = []

    korban_summary = impact.get("korban_summary")
    if korban_summary:
        insights.append({
            "category": "impact",
            "finding": f"Total korban terbanyak dalam satu kejadian mencapai {korban_summary['max']:.0f} orang",
            "value": korban_summary,
        })

    kerugian_summary = impact.get("kerugian_summary")
    if kerugian_summary:
        insights.append({
            "category": "impact",
            "finding": f"Kerugian material terbesar dalam satu kejadian mencapai {kerugian_summary['max']:,.0f}",
            "value": kerugian_summary,
        })

    return insights


def _insight_kecamatan_dampak_tertinggi(eda_result: dict[str, Any]) -> list[dict[str, Any]]:
    """Kecamatan dengan dampak tertinggi berdasarkan korban dan kerugian."""
    impact = eda_result.get("impact", {}) or {}
    insights: list[dict[str, Any]] = []

    top_korban = impact.get("top_kecamatan_by_korban")
    if top_korban is not None and not top_korban.empty:
        kecamatan = str(top_korban.index[0])
        insights.append({
            "category": "impact",
            "finding": f"Kecamatan dengan total korban tertinggi adalah '{kecamatan}'",
            "value": {"kecamatan": kecamatan, "total_korban": float(top_korban.iloc[0])},
        })

    top_kerugian = impact.get("top_kecamatan_by_kerugian")
    if top_kerugian is not None and not top_kerugian.empty:
        kecamatan = str(top_kerugian.index[0])
        insights.append({
            "category": "impact",
            "finding": f"Kecamatan dengan kerugian material tertinggi adalah '{kecamatan}'",
            "value": {"kecamatan": kecamatan, "total_kerugian": float(top_kerugian.iloc[0])},
        })

    return insights


def _insight_kelengkapan_data(quality_report: dict[str, Any]) -> dict[str, Any] | None:
    """Tingkat kelengkapan data, reuse dari Data Quality Report (Phase 2)."""
    score = quality_report.get("quality_score")
    if not score:
        return None
    completeness = score["breakdown"].get("completeness")
    max_completeness = QUALITY_SCORE_WEIGHTS["completeness"]
    return {
        "category": "data_quality",
        "finding": (
            f"Skor kualitas data keseluruhan {score['total_score']}/100, "
            f"komponen completeness {completeness}/{max_completeness}"
        ),
        "value": score,
    }


def _insight_temuan_kualitas(quality_report: dict[str, Any]) -> dict[str, Any] | None:
    """Temuan kualitas data yang perlu ditindaklanjuti, reuse rekomendasi Phase 2."""
    recommendations = quality_report.get("recommendations")
    if not recommendations:
        return None
    return {
        "category": "data_quality",
        "finding": "Terdapat temuan kualitas data yang perlu ditindaklanjuti",
        "value": recommendations,
    }


def _insight_operasional(eda_result: dict[str, Any]) -> dict[str, Any] | None:
    """Insight operasional: rasio penyelesaian dan kecepatan pelaporan."""
    operational = eda_result.get("operational", {}) or {}
    if not operational:
        return None

    completion_ratio = operational.get("completion_ratio")
    duration_stats = operational.get("reporting_duration_stats", {})

    if completion_ratio is not None:
        finding = f"Rasio penanganan selesai sebesar {completion_ratio:.2%}"
    else:
        finding = "Data status penanganan tidak lengkap"

    if duration_stats:
        finding += f", rata-rata durasi pelaporan {duration_stats['mean_jam']:.1f} jam"

    return {
        "category": "operational",
        "finding": finding,
        "value": {"completion_ratio": completion_ratio, "reporting_duration_stats": duration_stats},
    }


def generate_insight_report(
    eda_result: dict[str, Any],
    statistical_report: dict[str, Any],
    quality_report: dict[str, Any],
) -> dict[str, Any]:
    """Susun insight rule-based dari hasil Phase 2, 4, dan 5.

    Tidak melakukan komputasi statistik ulang -- seluruh insight disintesis
    dari output yang sudah tersedia.
    """
    logger.info("Memulai Insight Generation")

    single_insights = [
        _insight_top_kecamatan_frekuensi(statistical_report),
        _insight_dominant_jenis_bencana(statistical_report),
        _insight_periode_terbanyak(statistical_report),
        _insight_trend(statistical_report),
        _insight_kelengkapan_data(quality_report),
        _insight_temuan_kualitas(quality_report),
        _insight_operasional(eda_result),
    ]

    insights: list[dict[str, Any]] = [item for item in single_insights if item is not None]
    insights.extend(_insight_dampak_terbesar(eda_result))
    insights.extend(_insight_kecamatan_dampak_tertinggi(eda_result))

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_insights": len(insights),
        "insights": insights,
    }

    logger.info(f"Insight Generation selesai: {len(insights)} insight dihasilkan")
    return report


def export_insight_report(report: dict[str, Any], filename: str = "insight_report.json") -> None:
    """Ekspor laporan insight ke outputs/reports sebagai JSON."""
    ensure_dir(OUTPUT_REPORTS_DIR)
    path = OUTPUT_REPORTS_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    logger.info(f"Insight Report disimpan: {path}")