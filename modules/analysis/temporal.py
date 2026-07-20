#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Analisis temporal: tren kejadian berdasarkan waktu."""

from typing import Any

import pandas as pd

from modules.utils.logger import get_logger

logger = get_logger(__name__)


def _yearly_trend(df: pd.DataFrame) -> pd.Series:
    """Jumlah kejadian per tahun."""
    return df["tahun"].value_counts().sort_index()


def _monthly_trend(df: pd.DataFrame) -> pd.Series:
    """Jumlah kejadian per kombinasi tahun-bulan."""
    period = df["datetime_kejadian"].dt.to_period("M")
    return period.value_counts().sort_index()


def _quarterly_distribution(df: pd.DataFrame) -> pd.Series:
    """Distribusi kejadian per triwulan."""
    return df["triwulan"].value_counts().sort_index()


def _semester_distribution(df: pd.DataFrame) -> pd.Series:
    """Distribusi kejadian per semester."""
    return df["semester"].value_counts().sort_index()


def temporal_analysis(df: pd.DataFrame) -> dict[str, Any]:
    """Jalankan seluruh analisis temporal.

    Membutuhkan kolom hasil feature engineering: tahun, triwulan,
    semester, datetime_kejadian.
    """
    required_cols = {"tahun", "triwulan", "semester", "datetime_kejadian"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        logger.warning(
            f"Kolom temporal tidak lengkap, analisis dilewati: {missing_cols}"
        )
        return {}

    result = {
        "yearly_trend": _yearly_trend(df),
        "monthly_trend": _monthly_trend(df),
        "quarterly_distribution": _quarterly_distribution(df),
        "semester_distribution": _semester_distribution(df),
    }
    logger.info(f"Analisis temporal selesai: {len(result)} ringkasan dihasilkan")
    return result