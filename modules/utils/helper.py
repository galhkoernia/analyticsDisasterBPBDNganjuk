#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Fungsi utilitas generik lintas modul."""

from pathlib import Path

from typing import Any

import numpy as np
import pandas as pd

def ensure_dir(path: Path) -> Path:
    """Pastikan direktori ada, buat jika belum."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_percentage(numerator: int, denominator: int) -> float:
    """Hitung persentase dengan aman terhadap pembagian nol."""
    if denominator == 0:
        return 0.0
    return round((numerator / denominator) * 100, 2)


def normalize_text(value: str) -> str:
    """Normalisasi teks kategorikal: trim, single space, lower-case-safe compare."""
    if not isinstance(value, str):
        return value
    return " ".join(value.strip().split())


def to_json_safe(value: Any) -> Any:
    """Konversi struktur pandas/numpy menjadi tipe native yang aman untuk JSON."""
    if isinstance(value, pd.Series):
        return {str(idx): to_json_safe(v) for idx, v in value.items()}
    if isinstance(value, pd.DataFrame):
        return {str(idx): to_json_safe(row.to_dict()) for idx, row in value.iterrows()}
    if isinstance(value, dict):
        return {str(k): to_json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_json_safe(v) for v in value]
    if isinstance(value, (pd.Timestamp, pd.Period)):
        return str(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if not isinstance(value, (str, int, float, bool)) and pd.isna(value):
        return None
    return value
