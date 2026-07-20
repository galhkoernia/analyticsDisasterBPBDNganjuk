#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#


"""Pembuatan fitur turunan dari clean/transformed dataset.
"""

import re

import pandas as pd

from modules.utils.logger import get_logger

logger = get_logger(__name__)

_NIHIL_TOKENS = {"-", "--", "nihil", ""}
_LEADING_NUMBER = re.compile(r"^\D{0,10}?(\d+)")


def _extract_count(value: object) -> float:
    """Ekstrak angka pertama dari nilai narasi. NaN jika tidak dapat diekstrak."""
    if pd.isna(value):
        return float("nan")
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if text.lower() in _NIHIL_TOKENS:
        return 0.0

    match = _LEADING_NUMBER.match(text)
    if match:
        return float(match.group(1))

    return float("nan")


def _add_extracted_counts_with_log(df: pd.DataFrame, source_cols: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in source_cols:
        if col not in df.columns:
            continue
        extracted_col = f"_extracted_{col}"
        df[extracted_col] = df[col].apply(_extract_count)
        n_failed = int(df[extracted_col].isna().sum())
        if n_failed > 0:
            logger.warning(
                f"Ekstraksi angka gagal pada {n_failed}/{len(df)} baris kolom '{col}' "
                "(narasi tidak diawali angka) -- diperlakukan sebagai NaN, bukan 0"
            )
    return df


def add_victim_totals(df: pd.DataFrame) -> pd.DataFrame:
    """total_korban = korban_meninggal + korban_luka + korban_hilang (estimasi).
    """
    source_cols = ["korban_meninggal", "korban_luka", "korban_hilang"]
    df = _add_extracted_counts_with_log(df, source_cols)

    extracted_cols = [f"_extracted_{c}" for c in source_cols if c in df.columns]
    if extracted_cols:
        df["total_korban"] = df[extracted_cols].sum(axis=1, skipna=True, min_count=1)
        df = df.drop(columns=extracted_cols)

    return df


def add_rumah_totals(df: pd.DataFrame) -> pd.DataFrame:
    """total_rumah_terdampak = rumah_rusak_berat + sedang + ringan (estimasi)."""
    source_cols = ["rumah_rusak_berat", "rumah_rusak_sedang", "rumah_rusak_ringan"]
    df = _add_extracted_counts_with_log(df, source_cols)

    extracted_cols = [f"_extracted_{c}" for c in source_cols if c in df.columns]
    if extracted_cols:
        df["total_rumah_terdampak"] = df[extracted_cols].sum(axis=1, skipna=True, min_count=1)
        df = df.drop(columns=extracted_cols)

    return df


def add_pengungsi_totals(df: pd.DataFrame) -> pd.DataFrame:
    """total_pengungsi diekstrak dari kolom narasi 'pengungsi' (estimasi)."""
    source_cols = ["pengungsi"]
    df = _add_extracted_counts_with_log(df, source_cols)

    if "_extracted_pengungsi" in df.columns:
        df["total_pengungsi"] = df["_extracted_pengungsi"]
        df = df.drop(columns=["_extracted_pengungsi"])

    return df


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Turunkan tahun, bulan, triwulan, semester dari datetime_kejadian."""
    if "datetime_kejadian" not in df.columns:
        logger.warning("Kolom 'datetime_kejadian' tidak ditemukan, atribut waktu dilewati")
        return df

    df = df.copy()
    dt = df["datetime_kejadian"]
    df["tahun"] = dt.dt.year
    df["bulan"] = dt.dt.month
    df["nama_bulan"] = dt.dt.month_name()
    df["triwulan"] = dt.dt.quarter
    df["semester"] = dt.dt.month.apply(lambda m: 1 if pd.notna(m) and m <= 6 else (2 if pd.notna(m) else None))
    return df


def add_operational_features(df: pd.DataFrame) -> pd.DataFrame:
    """is_penanganan_selesai berdasarkan substring 'selesai' (case-insensitive).
    """
    if "status_penanganan" not in df.columns:
        return df

    df = df.copy()
    df["is_penanganan_selesai"] = (
        df["status_penanganan"].astype(str).str.contains("selesai", case=False, na=False)
    )
    return df


def feature_engineering_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Jalankan seluruh tahap feature engineering secara berurutan."""
    logger.info("Memulai Feature Engineering")
    df = add_victim_totals(df)
    df = add_rumah_totals(df)
    df = add_pengungsi_totals(df)
    df = add_temporal_features(df)
    df = add_operational_features(df)
    logger.info("Feature Engineering selesai")
    return df