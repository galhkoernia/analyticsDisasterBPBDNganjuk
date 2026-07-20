#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Transformasi tipe data, parsing koordinat, dan normalisasi datetime.
"""

import re
from datetime import datetime

import pandas as pd

from config.constants import NGANJUK_BBOX
from modules.utils.logger import get_logger

logger = get_logger(__name__)

_DECIMAL_TOKEN = re.compile(r"-?\s*\d+[.,]\d+")
_DMS_TOKEN = re.compile(
    r"(-?\d+)[°⁰]\s*(\d+)['’]\s*(\d+(?:[.,]\s*\d+)?)[\"”]\s*([NSEWnsew])"
)
_MISSING_COORD_SENTINELS = {"-", "--", ""}


def _parse_decimal_pair(text: str) -> tuple[float | None, float | None, str]:
    tokens = _DECIMAL_TOKEN.findall(text)
    if len(tokens) < 2:
        return None, None, "unparseable"

    try:
        lat = float(tokens[0].replace(" ", "").replace(",", "."))
        lon = float(tokens[1].replace(" ", "").replace(",", "."))
    except ValueError:
        return None, None, "unparseable"

    status = "ok_decimal" if len(tokens) == 2 else "multi_point_first_used"
    return lat, lon, status


def _parse_dms_pair(text: str) -> tuple[float | None, float | None, str]:
    matches = _DMS_TOKEN.findall(text)
    if len(matches) < 2:
        return None, None, "unparseable"

    lat, lon = None, None
    for deg_str, min_str, sec_str, hemi in matches[:2]:
        try:
            degrees = abs(float(deg_str))
            minutes = float(min_str)
            seconds = float(sec_str.replace(" ", "").replace(",", "."))
        except ValueError:
            return None, None, "unparseable"

        if not (0 <= minutes < 60) or not (0 <= seconds < 60):
            return None, None, "unparseable_invalid_range"

        decimal = degrees + minutes / 60 + seconds / 3600
        hemi_upper = hemi.upper()
        if hemi_upper in ("S", "W"):
            decimal = -decimal

        if hemi_upper in ("N", "S"):
            lat = decimal
        elif hemi_upper in ("E", "W"):
            lon = decimal

    if lat is None or lon is None:
        return None, None, "unparseable"

    status = "ok_dms" if len(matches) == 2 else "multi_point_first_used"
    return lat, lon, status


def _correct_latitude_sign(lat: float) -> tuple[float, bool]:
    """Balik tanda latitude positif yang seharusnya negatif (Nganjuk selalu di selatan)."""
    if lat > 0 and NGANJUK_BBOX["lat_min"] <= -lat <= NGANJUK_BBOX["lat_max"]:
        return -lat, True
    return lat, False


def _parse_single_coordinate(raw: object) -> tuple[float | None, float | None, str]:
    if pd.isna(raw):
        return None, None, "missing"

    text = str(raw).strip()
    if text.lower() in _MISSING_COORD_SENTINELS:
        return None, None, "missing"

    has_dms_symbol = bool(re.search(r"[°⁰]", text))
    lat, lon, status = (
        _parse_dms_pair(text) if has_dms_symbol else _parse_decimal_pair(text)
    )

    if lat is not None:
        lat, corrected = _correct_latitude_sign(lat)
        if corrected:
            status = f"{status}_sign_corrected"

    return lat, lon, status


def parse_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Parsing 'koordinat' menjadi kolom latitude/longitude + status audit."""
    if "koordinat" not in df.columns:
        logger.warning("Kolom 'koordinat' tidak ditemukan, parsing dilewati")
        return df

    df = df.copy()
    parsed = df["koordinat"].apply(_parse_single_coordinate)
    df["latitude"] = parsed.apply(lambda t: t[0])
    df["longitude"] = parsed.apply(lambda t: t[1])
    df["koordinat_parse_status"] = parsed.apply(lambda t: t[2])

    status_counts = df["koordinat_parse_status"].value_counts().to_dict()
    logger.info(f"Parsing koordinat selesai: {status_counts}")

    n_failed = df["koordinat_parse_status"].str.startswith("unparseable").sum()
    if n_failed > 0:
        logger.warning(
            f"{n_failed} baris koordinat gagal diparsing, perlu verifikasi manual"
        )

    return df


def combine_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Gabungkan kolom tanggal + waktu menjadi timestamp tunggal."""
    df = df.copy()

    def _combine(date_val, time_val):
        if pd.isna(date_val) or pd.isna(time_val):
            return pd.NaT
        return pd.Timestamp.combine(pd.Timestamp(date_val).date(), time_val)

    if {"tanggal_kejadian", "waktu_kejadian"}.issubset(df.columns):
        df["datetime_kejadian"] = df.apply(
            lambda r: _combine(r["tanggal_kejadian"], r["waktu_kejadian"]), axis=1
        )

    if {"tanggal_pelaporan", "waktu_pelaporan"}.issubset(df.columns):
        df["datetime_pelaporan"] = df.apply(
            lambda r: _combine(r["tanggal_pelaporan"], r["waktu_pelaporan"]), axis=1
        )

    if {"datetime_kejadian", "datetime_pelaporan"}.issubset(df.columns):
        df["durasi_pelaporan_jam"] = (
            df["datetime_pelaporan"] - df["datetime_kejadian"]
        ).dt.total_seconds() / 3600

    logger.info("Kombinasi datetime kejadian/pelaporan selesai")
    return df


def cast_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Tetapkan dtype eksplisit untuk kolom kategorikal ber-cardinality rendah."""
    df = df.copy()
    categorical_cols = ["kecamatan", "desa", "jenis_bencana", "status_penanganan"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")
    return df


def transform_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Jalankan seluruh tahap transformasi secara berurutan."""
    logger.info("Memulai Data Transformation")
    df = parse_coordinates(df)
    df = combine_datetime(df)
    df = cast_dtypes(df)
    logger.info("Data Transformation selesai")
    return df
