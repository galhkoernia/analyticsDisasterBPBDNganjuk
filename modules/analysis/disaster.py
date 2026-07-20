#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Analisis karakteristik bencana: jenis, penyebab, dan persebarannya."""

from typing import Any

import pandas as pd

from modules.utils.logger import get_logger

logger = get_logger(__name__)


def _distribution_jenis_bencana(df: pd.DataFrame) -> pd.Series:
    """Jumlah kejadian per jenis bencana."""
    return df["jenis_bencana"].value_counts()


def _distribution_penyebab(df: pd.DataFrame) -> pd.Series:
    """Jumlah kejadian per penyebab."""
    return df["penyebab"].value_counts()


def _crosstab_jenis_bencana_kecamatan(df: pd.DataFrame) -> pd.DataFrame:
    """Tabulasi silang jenis bencana terhadap kecamatan."""
    return pd.crosstab(df["jenis_bencana"], df["kecamatan"])


def disaster_analysis(df: pd.DataFrame) -> dict[str, Any]:
    """Jalankan seluruh analisis karakteristik bencana.

    Membutuhkan kolom: jenis_bencana, penyebab, kecamatan.
    """
    required_cols = {"jenis_bencana", "penyebab", "kecamatan"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        logger.warning(
            f"Kolom karakteristik bencana tidak lengkap, analisis dilewati: {missing_cols}"
        )
        return {}

    result = {
        "distribution_jenis_bencana": _distribution_jenis_bencana(df),
        "distribution_penyebab": _distribution_penyebab(df),
        "crosstab_jenis_bencana_kecamatan": _crosstab_jenis_bencana_kecamatan(df),
    }
    dominant = result["distribution_jenis_bencana"].idxmax()
    logger.info(f"Analisis bencana selesai: jenis dominan = '{dominant}'")
    return result