#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Pemeriksaan konsistensi nilai kategorikal."""

from typing import Any

import pandas as pd

from config.constants import CATEGORICAL_CONSISTENCY_COLUMNS
from modules.utils.helper import normalize_text
from modules.utils.logger import get_logger

logger = get_logger(__name__)


def check_consistency(df: pd.DataFrame) -> dict[str, Any]:
    """Deteksi variasi penulisan pada kolom kategorikal.
    """
    result: dict[str, Any] = {}

    for col in CATEGORICAL_CONSISTENCY_COLUMNS:
        if col not in df.columns:
            logger.warning(f"Kolom kategorikal '{col}' tidak ditemukan, dilewati")
            continue

        raw_values = df[col].dropna().unique().tolist()
        normalized_groups: dict[str, list[str]] = {}

        for value in raw_values:
            key = normalize_text(str(value)).lower()
            normalized_groups.setdefault(key, []).append(value)

        inconsistent = {
            key: variants
            for key, variants in normalized_groups.items()
            if len(variants) > 1
        }

        result[col] = {
            "n_unique_raw": len(raw_values),
            "n_unique_normalized": len(normalized_groups),
            "inconsistent_groups": inconsistent,
        }

        if inconsistent:
            logger.warning(
                f"Kolom '{col}': {len(inconsistent)} grup nilai tidak konsisten"
            )

    return result
