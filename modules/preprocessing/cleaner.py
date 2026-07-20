#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#


"""Pembersihan data mentah menjadi dataset siap transformasi.
"""

import re
from typing import Any

import pandas as pd

from config.constants import CATEGORICAL_CONSISTENCY_COLUMNS, NON_NEGATIVE_NUMERIC_COLUMNS
from modules.utils.helper import normalize_text
from modules.utils.logger import get_logger

logger = get_logger(__name__)

GENERIC_MISSING_TOKENS = {"", "n/a", "na", "null", "none", "nan", "-nan"}

_BULLET_CHARS_PATTERN = re.compile(r"^[\s•\uf0d8\u2022\-]+")


def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Hapus leading/trailing whitespace pada seluruh kolom object."""
    df = df.copy()
    object_cols = df.select_dtypes(include="object").columns
    for col in object_cols:
        df[col] = df[col].apply(lambda v: v.strip() if isinstance(v, str) else v)
    logger.info(f"Trim whitespace diterapkan pada {len(object_cols)} kolom object")
    return df


def normalize_missing_tokens(df: pd.DataFrame) -> pd.DataFrame:
    """Konversi token missing generik menjadi NaN sesungguhnya.
    """
    df = df.copy()
    narrative_exempt = {
        "korban_meninggal", "korban_luka", "korban_hilang",
        "rumah_rusak_berat", "rumah_rusak_sedang", "rumah_rusak_ringan",
        "pengungsi",
    }
    n_converted = 0

    for col in df.select_dtypes(include="object").columns:
        if col in narrative_exempt:
            continue
        mask = df[col].apply(
            lambda v: isinstance(v, str) and v.strip().lower() in GENERIC_MISSING_TOKENS
        )
        n_converted += int(mask.sum())
        df.loc[mask, col] = pd.NA

    logger.info(f"Missing token generik dikonversi ke NaN: {n_converted} sel")
    return df


def standardize_categorical(
    df: pd.DataFrame, consistency_result: dict[str, Any] | None = None
) -> pd.DataFrame:
    """Standarkan kolom kategorikal ke satu representasi kanonik.
    """
    df = df.copy()

    for col in CATEGORICAL_CONSISTENCY_COLUMNS:
        if col not in df.columns:
            continue

        if consistency_result and col in consistency_result:
            inconsistent = consistency_result[col].get("inconsistent_groups", {})
            value_counts = df[col].value_counts()
            canonical_map: dict[str, str] = {}

            for variants in inconsistent.values():
                canonical = max(variants, key=lambda v: value_counts.get(v, 0))
                for variant in variants:
                    canonical_map[variant] = canonical

            if canonical_map:
                df[col] = df[col].replace(canonical_map)
                logger.info(
                    f"Kolom '{col}': {len(canonical_map)} variant dipetakan ke bentuk kanonik"
                )
        else:
            df[col] = df[col].apply(
                lambda v: normalize_text(str(v)) if pd.notna(v) else v
            )

    return df


def clean_kerugian(df: pd.DataFrame) -> pd.DataFrame:
    """Koersi kolom kerugian ke numerik, sentinel '-' menjadi NaN (belum dihitung)."""
    df = df.copy()
    for col in NON_NEGATIVE_NUMERIC_COLUMNS:
        if col not in df.columns:
            continue
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def remove_unwanted_characters(df: pd.DataFrame) -> pd.DataFrame:
    """Hapus bullet/karakter noise di awal string pada kolom narasi.
    """
    df = df.copy()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(
            lambda v: _BULLET_CHARS_PATTERN.sub("", v).strip() if isinstance(v, str) else v
        )
    return df


def clean_pipeline(
    df: pd.DataFrame, consistency_result: dict[str, Any] | None = None
) -> pd.DataFrame:
    """Jalankan seluruh tahap cleaning secara berurutan."""
    logger.info("Memulai Data Cleaning")
    df = trim_whitespace(df)
    df = remove_unwanted_characters(df)
    df = normalize_missing_tokens(df)
    df = standardize_categorical(df, consistency_result)
    df = clean_kerugian(df)
    logger.info("Data Cleaning selesai")
    return df