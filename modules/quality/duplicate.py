#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Pemeriksaan duplikasi data."""

from typing import Any

import pandas as pd

from config.constants import DUPLICATE_KEY_COLUMNS
from modules.utils.logger import get_logger

logger = get_logger(__name__)


def check_full_row_duplicates(df: pd.DataFrame) -> dict[str, Any]:
    """Deteksi baris yang identik sepenuhnya di seluruh kolom."""
    duplicate_mask = df.duplicated(keep=False)
    n_duplicates = int(duplicate_mask.sum())

    logger.info(f"Duplikasi baris penuh: {n_duplicates} baris")
    return {
        "count": n_duplicates,
        "row_indices": df[duplicate_mask].index.tolist(),
    }


def check_key_duplicates(df: pd.DataFrame) -> dict[str, Any]:
    """Deteksi nilai berulang pada kolom kunci administratif.
    """
    result: dict[str, Any] = {}

    for col in DUPLICATE_KEY_COLUMNS:
        if col not in df.columns:
            logger.warning(f"Kolom kunci '{col}' tidak ditemukan, dilewati")
            continue

        value_counts = df[col].value_counts()
        repeated = value_counts[value_counts > 1]

        result[col] = {
            "n_repeated_values": int(len(repeated)),
            "n_affected_rows": int(repeated.sum()),
            "repeated_values": repeated.to_dict(),
        }

    return result
