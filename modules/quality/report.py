#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Agregasi Data Quality Report.
"""

import json
from datetime import datetime
from typing import Any

import pandas as pd

from config.constants import (
    NON_NEGATIVE_NUMERIC_COLUMNS,
    QUALITY_SCORE_WEIGHTS,
)

from config.settings import OUTPUT_REPORTS_DIR
from modules.quality.consistency import check_consistency
from modules.quality.coordinate import check_coordinates
from modules.quality.duplicate import check_full_row_duplicates, check_key_duplicates
from modules.quality.missing import check_missing
from modules.utils.helper import ensure_dir, safe_percentage
from modules.utils.logger import get_logger

logger = get_logger(__name__)


def _check_temporal_validity(df: pd.DataFrame) -> dict[str, Any]:
    """Validasi tanggal kejadian tidak boleh setelah tanggal pelaporan."""

    required = {"tanggal_kejadian", "tanggal_pelaporan"}
    if not required.issubset(df.columns):
        return {"error": "missing_temporal_columns"}

    kejadian = pd.to_datetime(df["tanggal_kejadian"], errors="coerce")
    pelaporan = pd.to_datetime(df["tanggal_pelaporan"], errors="coerce")

    unparseable = int(kejadian.isna().sum() + pelaporan.isna().sum())
    invalid_order_mask = kejadian > pelaporan
    n_invalid_order = int(invalid_order_mask.sum())

    n_rows = len(df)
    n_valid = n_rows - n_invalid_order

    return {
        "n_valid": n_valid,
        "n_invalid_order": n_invalid_order,
        "n_unparseable": unparseable,
        "valid_percentage": safe_percentage(n_valid, n_rows),
        "invalid_row_indices": df[invalid_order_mask].index.tolist(),
    }


def _check_numeric_validity(df: pd.DataFrame) -> dict[str, Any]:
    """Validasi kolom numerik dampak tidak boleh bernilai negatif.
    """
    result: dict[str, Any] = {}
    n_rows = len(df)

    for col in NON_NEGATIVE_NUMERIC_COLUMNS:
        if col not in df.columns:
            continue

        numeric_series = pd.to_numeric(df[col], errors="coerce")
        non_numeric_mask = numeric_series.isna() & df[col].notna()
        n_non_numeric = int(non_numeric_mask.sum())

        negative_mask = numeric_series < 0
        n_negative = int(negative_mask.sum())

        result[col] = {
            "n_negative": n_negative,
            "n_non_numeric": n_non_numeric,
            "negative_row_indices": df[negative_mask].index.tolist(),
            "non_numeric_row_indices": df[non_numeric_mask].index.tolist(),
            "valid_percentage": safe_percentage(
                n_rows - n_negative - n_non_numeric, n_rows
            ),
        }

    return result

def _compute_quality_score(
    missing_result: dict[str, Any],
    consistency_result: dict[str, Any],
    coordinate_result: dict[str, Any],
    temporal_result: dict[str, Any],
    numeric_result: dict[str, Any],
    n_rows: int,
) -> dict[str, Any]:
    """Hitung Data Quality Score tertimbang (0-100) per komponen."""
    w = QUALITY_SCORE_WEIGHTS

    n_missing_problematic = sum(
        v["missing_count"]
        for v in missing_result["per_column"].values()
        if not v["acceptable"]
    )
    
    n_missing_problematic = min(n_missing_problematic, n_rows)
    completeness_score = w["completeness"] * (
        safe_percentage(n_rows - n_missing_problematic, n_rows) / 100
    )

    n_inconsistent = sum(
        len(v["inconsistent_groups"]) for v in consistency_result.values()
    )
    consistency_score = w["consistency"] * max(0, 1 - n_inconsistent / max(n_rows, 1))

    coordinate_score = w["coordinate_validity"] * (
        coordinate_result.get("valid_percentage", 0) / 100
    )

    temporal_score = w["temporal_validity"] * (
        temporal_result.get("valid_percentage", 0) / 100
    )

    numeric_pct_values = [v["valid_percentage"] for v in numeric_result.values()]
    numeric_avg_pct = (
        sum(numeric_pct_values) / len(numeric_pct_values) if numeric_pct_values else 100
    )
    numeric_score = w["numeric_validity"] * (numeric_avg_pct / 100)

    total = round(
        completeness_score
        + consistency_score
        + coordinate_score
        + temporal_score
        + numeric_score,
        2,
    )

    return {
        "total_score": total,
        "breakdown": {
            "completeness": round(completeness_score, 2),
            "consistency": round(consistency_score, 2),
            "coordinate_validity": round(coordinate_score, 2),
            "temporal_validity": round(temporal_score, 2),
            "numeric_validity": round(numeric_score, 2),
        },
    }

def _build_recommendations(
    missing_result: dict[str, Any],
    duplicate_key_result: dict[str, Any],
    consistency_result: dict[str, Any],
    coordinate_result: dict[str, Any],
    temporal_result: dict[str, Any],
    numeric_result: dict[str, Any],
) -> list[str]:
    """Susun rekomendasi tindak lanjut berbasis hasil pemeriksaan."""
    recommendations: list[str] = []

    if missing_result["problematic_columns"]:
        recommendations.append(
            f"Tinjau missing value pada kolom: {missing_result['problematic_columns']}"
        )

    for col, info in duplicate_key_result.items():
        if info["n_repeated_values"] > 0:
            recommendations.append(
                f"Verifikasi {info['n_repeated_values']} nilai berulang pada kolom kunci '{col}' "
                "sebelum memutuskan dedup"
            )

    for col, info in consistency_result.items():
        if info["inconsistent_groups"]:
            recommendations.append(
                f"Standarkan penulisan kategori pada kolom '{col}': "
                f"{list(info['inconsistent_groups'].values())}"
            )

    if coordinate_result.get("n_missing", 0) or coordinate_result.get("n_out_of_bbox", 0):
        recommendations.append(
            "Verifikasi koordinat yang kosong atau berada di luar wilayah Kabupaten Nganjuk"
        )

    if temporal_result.get("n_invalid_order", 0):
        recommendations.append(
            "Periksa baris dengan tanggal kejadian setelah tanggal pelaporan"
        )

    for col, info in numeric_result.items():
        if info["n_negative"] > 0:
            recommendations.append(f"Periksa nilai negatif pada kolom '{col}'")

    if not recommendations:
        recommendations.append("Tidak ditemukan isu kualitas data signifikan")

    return recommendations


def generate_quality_report(df: pd.DataFrame) -> dict[str, Any]:
    """Jalankan seluruh pemeriksaan kualitas dan susun laporan lengkap."""
    logger.info("Memulai Data Quality Assessment")

    missing_result = check_missing(df)
    full_dup_result = check_full_row_duplicates(df)
    key_dup_result = check_key_duplicates(df)
    consistency_result = check_consistency(df)
    coordinate_result = check_coordinates(df)
    temporal_result = _check_temporal_validity(df)
    numeric_result = _check_numeric_validity(df)

    score = _compute_quality_score(
        missing_result,
        consistency_result,
        coordinate_result,
        temporal_result,
        numeric_result,
        n_rows=len(df),
    )

    recommendations = _build_recommendations(
        missing_result,
        key_dup_result,
        consistency_result,
        coordinate_result,
        temporal_result,
        numeric_result,
    )

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dataset_summary": {
            "n_rows": len(df),
            "n_columns": len(df.columns),
        },
        "missing_value": missing_result,
        "duplicate": {
            "full_row": full_dup_result,
            "by_key": key_dup_result,
        },
        "consistency": consistency_result,
        "coordinate_validity": coordinate_result,
        "temporal_validity": temporal_result,
        "numeric_validity": numeric_result,
        "quality_score": score,
        "recommendations": recommendations,
    }

    logger.info(f"Data Quality Score: {score['total_score']}/100")
    return report


def export_report(report: dict[str, Any], filename: str = "data_quality_report.json") -> None:
    """Ekspor laporan ke outputs/reports sebagai JSON."""
    ensure_dir(OUTPUT_REPORTS_DIR)
    path = OUTPUT_REPORTS_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    logger.info(f"Data Quality Report disimpan: {path}")
