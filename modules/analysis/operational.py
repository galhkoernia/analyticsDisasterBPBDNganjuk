#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Analisis operasional: status penanganan dan kecepatan respons."""

from typing import Any

import pandas as pd

from modules.utils.logger import get_logger

logger = get_logger(__name__)


def _status_distribution(df: pd.DataFrame) -> pd.Series:
    """Distribusi status penanganan."""
    return df["status_penanganan"].value_counts()


def _completion_ratio(df: pd.DataFrame) -> float:
    """Rasio kejadian dengan penanganan selesai."""
    return float(df["is_penanganan_selesai"].mean())


def _reporting_duration_stats(df: pd.DataFrame) -> dict[str, float]:
    """Statistik durasi pelaporan (jam) sebagai indikator kecepatan respons."""
    valid = df["durasi_pelaporan_jam"].dropna()
    if valid.empty:
        return {}
    return {
        "mean_jam": float(valid.mean()),
        "median_jam": float(valid.median()),
        "min_jam": float(valid.min()),
        "max_jam": float(valid.max()),
    }


def operational_analysis(df: pd.DataFrame) -> dict[str, Any]:
    """Jalankan seluruh analisis operasional.

    Membutuhkan kolom: status_penanganan, is_penanganan_selesai,
    durasi_pelaporan_jam.
    """
    required_cols = {"status_penanganan", "is_penanganan_selesai", "durasi_pelaporan_jam"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        logger.warning(
            f"Kolom operasional tidak lengkap, analisis dilewati: {missing_cols}"
        )
        return {}

    result = {
        "status_distribution": _status_distribution(df),
        "completion_ratio": _completion_ratio(df),
        "reporting_duration_stats": _reporting_duration_stats(df),
    }
    logger.info(
        f"Analisis operasional selesai: completion_ratio={result['completion_ratio']:.2%}"
    )
    return result