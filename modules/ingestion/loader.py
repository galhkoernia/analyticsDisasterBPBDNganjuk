#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Pembacaan dataset mentah dari data/raw."""

from pathlib import Path

import pandas as pd

from config.settings import DATA_RAW_DIR, DEFAULT_SHEET_NAME, SUPPORTED_EXTENSIONS
from modules.utils.logger import get_logger

logger = get_logger(__name__)


def find_raw_file(filename: str | None = None) -> Path:
    if filename:
        path = DATA_RAW_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {path}")
        return path

    candidates = [
        p for p in DATA_RAW_DIR.iterdir()
        if p.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    if not candidates:
        raise FileNotFoundError(f"Tidak ada dataset di {DATA_RAW_DIR}")
    if len(candidates) > 1:
        raise ValueError(
            f"Lebih dari satu file ditemukan di {DATA_RAW_DIR}, "
            f"tentukan filename secara eksplisit: {[p.name for p in candidates]}"
        )
    return candidates[0]


def load_dataset(filename: str | None = None) -> pd.DataFrame:
    
    path = find_raw_file(filename)
    logger.info(f"Membaca dataset: {path.name}")

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path, sheet_name=DEFAULT_SHEET_NAME)

    logger.info(f"Dataset dimuat: {df.shape[0]} baris, {df.shape[1]} kolom")
    return df
