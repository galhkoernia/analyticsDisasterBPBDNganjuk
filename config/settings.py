#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Konfigurasi path dan parameter global sistem."""

from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Data
DATA_DIR: Path = BASE_DIR / "data"
DATA_RAW_DIR: Path = DATA_DIR / "raw"
DATA_PROCESSED_DIR: Path = DATA_DIR / "processed"
DATA_REFERENCE_DIR: Path = DATA_DIR / "reference"

# Output
OUTPUTS_DIR: Path = BASE_DIR / "outputs"
OUTPUT_REPORTS_DIR: Path = OUTPUTS_DIR / "reports"
OUTPUT_FIGURES_DIR: Path = OUTPUTS_DIR / "figures"
OUTPUT_DASHBOARD_DIR: Path = OUTPUTS_DIR / "dashboard"

# Logging
LOG_DIR: Path = OUTPUTS_DIR / "reports"
LOG_FILE: Path = LOG_DIR / "pipeline.log"

# Ingestion
DEFAULT_SHEET_NAME: int | str = 0
DEFAULT_ENCODING: str = "utf-8"
SUPPORTED_EXTENSIONS: tuple[str, ...] = (".xlsx", ".xls", ".csv")
