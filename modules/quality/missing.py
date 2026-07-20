#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Pemeriksaan missing value."""

from typing import Any

import pandas as pd

from config.constants import ACCEPTABLE_MISSING_COLUMNS
from modules.utils.helper import safe_percentage
from modules.utils.logger import get_logger

logger = get_logger(__name__)


def check_missing(df: pd.DataFrame) -> dict[str, Any]:
    """Hitung jumlah dan persentase missing value per kolom.
    """
    n_rows = len(df)
    missing_counts = df.isna().sum()
    missing_counts = missing_counts[missing_counts > 0]

    per_column = {}
    problematic_columns = []

    for col, count in missing_counts.items():
        pct = safe_percentage(int(count), n_rows)
        is_acceptable = col in ACCEPTABLE_MISSING_COLUMNS
        per_column[col] = {
            "missing_count": int(count),
            "missing_percentage": pct,
            "acceptable": is_acceptable,
        }
        if not is_acceptable:
            problematic_columns.append(col)

    logger.info(
        f"Missing value: {len(per_column)} kolom terdampak, "
        f"{len(problematic_columns)} dianggap bermasalah"
    )

    return {
        "per_column": per_column,
        "problematic_columns": problematic_columns,
    }
