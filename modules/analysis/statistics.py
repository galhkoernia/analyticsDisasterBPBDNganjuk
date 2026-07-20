#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Analisis statistik deskriptif dan korelasi antar variabel numerik.

Distribusi frekuensi, tren, dan crosstab memanfaatkan kembali output
Phase 4 (eda_result) tanpa komputasi ulang.
"""

import json
from datetime import datetime
from typing import Any

import pandas as pd

from config.settings import OUTPUT_REPORTS_DIR
from modules.utils.helper import ensure_dir, to_json_safe
from modules.utils.logger import get_logger

logger = get_logger(__name__)

NUMERIC_COLUMNS_OF_INTEREST: list[str] = [
    "total_korban",
    "total_rumah_terdampak",
    "kerugian",
    "durasi_pelaporan_jam",
]

MIN_ROWS_FOR_CORRELATION = 3


def _descriptive_stats(df: pd.DataFrame) -> dict[str, Any]:
    """Statistik deskriptif (count, mean, std, quartile, max, missing_ratio) per kolom numerik."""
    result: dict[str, Any] = {}
    available_cols = [c for c in NUMERIC_COLUMNS_OF_INTEREST if c in df.columns]

    if not available_cols:
        logger.warning("Tidak ada kolom numerik yang dikenali untuk statistik deskriptif")
        return result

    for col in available_cols:
        series = pd.to_numeric(df[col], errors="coerce")
        valid = series.dropna()
        if valid.empty:
            continue
        result[col] = {
            "count": int(valid.count()),
            "mean": float(valid.mean()),
            "std": float(valid.std()) if len(valid) > 1 else 0.0,
            "min": float(valid.min()),
            "q1": float(valid.quantile(0.25)),
            "median": float(valid.median()),
            "q3": float(valid.quantile(0.75)),
            "max": float(valid.max()),
            "missing_ratio": float(series.isna().mean()),
        }

    return result


def _correlation_matrix(df: pd.DataFrame) -> dict[str, Any]:
    """Korelasi Pearson antar variabel numerik, jika data memenuhi syarat minimum."""
    available_cols = [c for c in NUMERIC_COLUMNS_OF_INTEREST if c in df.columns]
    if len(available_cols) < 2:
        logger.warning("Korelasi dilewati: kurang dari 2 kolom numerik tersedia")
        return {}

    numeric_df = df[available_cols].apply(pd.to_numeric, errors="coerce")
    valid_rows = numeric_df.dropna()
    if len(valid_rows) < MIN_ROWS_FOR_CORRELATION:
        logger.warning(
            f"Korelasi dilewati: hanya {len(valid_rows)} baris valid "
            f"(minimum {MIN_ROWS_FOR_CORRELATION})"
        )
        return {}

    corr = valid_rows.corr(method="pearson")
    return to_json_safe(corr)


def _trend_analysis(temporal_result: dict[str, Any]) -> dict[str, Any]:
    """Ringkas arah tren tahunan (naik/turun/stabil) dari yearly_trend (Phase 4)."""
    yearly = temporal_result.get("yearly_trend")
    if yearly is None or len(yearly) < 2:
        return {}

    first_year, last_year = int(yearly.index[0]), int(yearly.index[-1])
    first_value, last_value = int(yearly.iloc[0]), int(yearly.iloc[-1])
    delta = last_value - first_value

    if delta > 0:
        direction = "meningkat"
    elif delta < 0:
        direction = "menurun"
    else:
        direction = "stabil"

    return {
        "first_year": first_year,
        "last_year": last_year,
        "first_value": first_value,
        "last_value": last_value,
        "delta": delta,
        "direction": direction,
    }


def generate_statistical_report(df: pd.DataFrame, eda_result: dict[str, Any]) -> dict[str, Any]:
    """Jalankan analisis statistik deskriptif dan korelasi, digabung dengan
    distribusi/tren/crosstab yang direuse dari Phase 4 (eda_result).
    """
    logger.info("Memulai Statistical Analysis")

    temporal_result = eda_result.get("temporal", {}) or {}
    spatial_result = eda_result.get("spatial", {}) or {}
    disaster_result = eda_result.get("disaster", {}) or {}

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "descriptive_stats": _descriptive_stats(df),
        "distribution_jenis_bencana": to_json_safe(
            disaster_result.get("distribution_jenis_bencana")
        ),
        "distribution_kecamatan": to_json_safe(
            spatial_result.get("distribution_by_kecamatan")
        ),
        "temporal_distribution": {
            "yearly_trend": to_json_safe(temporal_result.get("yearly_trend")),
            "monthly_trend": to_json_safe(temporal_result.get("monthly_trend")),
        },
        "trend_analysis": _trend_analysis(temporal_result),
        "crosstab_jenis_bencana_kecamatan": to_json_safe(
            disaster_result.get("crosstab_jenis_bencana_kecamatan")
        ),
        "correlation": _correlation_matrix(df),
    }

    logger.info("Statistical Analysis selesai")
    return report


def export_statistical_report(
    report: dict[str, Any], filename: str = "statistical_report.json"
) -> None:
    """Ekspor laporan statistik ke outputs/reports sebagai JSON."""
    ensure_dir(OUTPUT_REPORTS_DIR)
    path = OUTPUT_REPORTS_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    logger.info(f"Statistical Report disimpan: {path}")