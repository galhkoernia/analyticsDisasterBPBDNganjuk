#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Analisis spasial: distribusi kejadian berdasarkan lokasi."""

from typing import Any

import pandas as pd

from modules.utils.logger import get_logger

logger = get_logger(__name__)


def _valid_coordinate_ratio(df: pd.DataFrame) -> float:
    """Rasio baris dengan koordinat berhasil diparsing (status diawali 'ok')."""
    valid = df["koordinat_parse_status"].str.startswith("ok").sum()
    return valid / len(df) if len(df) else 0.0


def _distribution_by_kecamatan(df: pd.DataFrame) -> pd.Series:
    """Jumlah kejadian per kecamatan."""
    return df["kecamatan"].value_counts()


def _distribution_by_desa(df: pd.DataFrame) -> pd.Series:
    """Jumlah kejadian per desa."""
    return df["desa"].value_counts()


def _coordinate_bounds_summary(df: pd.DataFrame) -> dict[str, float]:
    """Ringkasan rentang latitude/longitude yang valid."""
    valid = df[["latitude", "longitude"]].dropna()
    if valid.empty:
        return {}
    return {
        "lat_min": float(valid["latitude"].min()),
        "lat_max": float(valid["latitude"].max()),
        "lon_min": float(valid["longitude"].min()),
        "lon_max": float(valid["longitude"].max()),
    }


def spatial_analysis(df: pd.DataFrame) -> dict[str, Any]:
    """Jalankan seluruh analisis spasial.

    Membutuhkan kolom hasil transformasi: latitude, longitude,
    koordinat_parse_status, kecamatan, desa.
    """
    required_cols = {"latitude", "longitude", "koordinat_parse_status", "kecamatan", "desa"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        logger.warning(
            f"Kolom spasial tidak lengkap, analisis dilewati: {missing_cols}"
        )
        return {}

    result = {
        "valid_coordinate_ratio": _valid_coordinate_ratio(df),
        "distribution_by_kecamatan": _distribution_by_kecamatan(df),
        "distribution_by_desa": _distribution_by_desa(df),
        "coordinate_bounds": _coordinate_bounds_summary(df),
    }
    logger.info(
        f"Analisis spasial selesai: valid_coordinate_ratio="
        f"{result['valid_coordinate_ratio']:.2%}"
    )
    return result