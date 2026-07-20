#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Analisis dampak: korban, rumah terdampak, dan kerugian material."""

from typing import Any

import pandas as pd

from modules.utils.logger import get_logger

logger = get_logger(__name__)


def _numeric_summary(series: pd.Series) -> dict[str, float]:
    """Ringkasan statistik dasar (sum, mean, median, max, missing_ratio)."""
    valid = series.dropna()
    if valid.empty:
        return {}
    return {
        "sum": float(valid.sum()),
        "mean": float(valid.mean()),
        "median": float(valid.median()),
        "max": float(valid.max()),
        "missing_ratio": float(series.isna().mean()),
    }


def _top_affected_kecamatan(df: pd.DataFrame, by: str, top_n: int = 5) -> pd.Series:
    """Kecamatan dengan dampak tertinggi berdasarkan kolom `by`."""
    return df.groupby("kecamatan")[by].sum().sort_values(ascending=False).head(top_n)


def impact_analysis(df: pd.DataFrame) -> dict[str, Any]:
    """Jalankan seluruh analisis dampak.
    """
    required_cols = {"total_korban", "total_rumah_terdampak", "kerugian", "kecamatan"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        logger.warning(
            f"Kolom dampak tidak lengkap, analisis dilewati: {missing_cols}"
        )
        return {}

    result = {
        "korban_summary": _numeric_summary(df["total_korban"]),
        "rumah_summary": _numeric_summary(df["total_rumah_terdampak"]),
        "kerugian_summary": _numeric_summary(df["kerugian"]),
        "top_kecamatan_by_korban": _top_affected_kecamatan(df, "total_korban"),
        "top_kecamatan_by_kerugian": _top_affected_kecamatan(df, "kerugian"),
    }

    if "total_pengungsi" in df.columns:
        result["pengungsi_summary"] = _numeric_summary(df["total_pengungsi"])
        result["top_kecamatan_by_pengungsi"] = _top_affected_kecamatan(df, "total_pengungsi")
    else:
        logger.warning("Kolom 'total_pengungsi' tidak ditemukan, metrik pengungsi dilewati")

    logger.info("Analisis dampak selesai")
    return result