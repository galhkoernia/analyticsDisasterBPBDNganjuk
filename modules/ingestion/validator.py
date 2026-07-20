#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Validasi skema dan profil dasar dataset."""

from typing import Any

import pandas as pd

from config.constants import RAW_COLUMN_MAP
from modules.utils.logger import get_logger

logger = get_logger(__name__)


def validate_schema(df: pd.DataFrame) -> dict[str, list[str]]:
    """Cek kolom yang diharapkan (RAW_COLUMN_MAP) terhadap kolom aktual.
    """
    expected = set(RAW_COLUMN_MAP.values())
    actual = set(df.columns)

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)

    if missing:
        logger.warning(f"Kolom hilang dari RAW_COLUMN_MAP: {missing}")
    if extra:
        logger.info(f"Kolom di dataset tapi belum dipetakan: {extra}")

    return {"missing_columns": missing, "unmapped_columns": extra}


def rename_to_logical(df: pd.DataFrame) -> pd.DataFrame:
    """Ganti nama kolom raw menjadi nama logis sesuai RAW_COLUMN_MAP
    """
    reverse_map = {raw: logical for logical, raw in RAW_COLUMN_MAP.items()}
    return df.rename(columns=reverse_map)


def profile_dataset(df: pd.DataFrame) -> dict[str, Any]:
    """Hasilkan profil dasar dataset: dimensi, tipe data, statistik ringkas."""
    dtype_counts = df.dtypes.astype(str).value_counts().to_dict()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    basic_stats = (
        df[numeric_cols].describe().to_dict() if numeric_cols else {}
    )

    profile = {
        "n_rows": int(df.shape[0]),
        "n_columns": int(df.shape[1]),
        "dtype_breakdown": dtype_counts,
        "numeric_columns": numeric_cols,
        "basic_statistics": basic_stats,
    }

    logger.info(
        f"Profil dataset: {profile['n_rows']} baris, "
        f"{profile['n_columns']} kolom, dtype={dtype_counts}"
    )
    return profile
