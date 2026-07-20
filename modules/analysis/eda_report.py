#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Agregasi dan ekspor Exploratory Data Analysis Report (Phase 4)."""

import json
from datetime import datetime
from typing import Any

import pandas as pd

from config.settings import OUTPUT_REPORTS_DIR
from modules.analysis.disaster import disaster_analysis
from modules.analysis.impact import impact_analysis
from modules.analysis.operational import operational_analysis
from modules.analysis.spatial import spatial_analysis
from modules.analysis.temporal import temporal_analysis
from modules.utils.helper import ensure_dir, to_json_safe
from modules.utils.logger import get_logger

logger = get_logger(__name__)


def generate_eda_report(df: pd.DataFrame) -> dict[str, Any]:
    """Jalankan seluruh analisis EDA (temporal, spatial, disaster, impact,
    operational) dan gabungkan menjadi satu struktur report.
    """
    logger.info("Memulai Exploratory Data Analysis")

    eda_result = {
        "temporal": temporal_analysis(df),
        "spatial": spatial_analysis(df),
        "disaster": disaster_analysis(df),
        "impact": impact_analysis(df),
        "operational": operational_analysis(df),
    }

    logger.info("Exploratory Data Analysis selesai")
    return eda_result


def export_eda_report(eda_result: dict[str, Any], filename: str = "eda_report.json") -> None:
    """Ekspor EDA Report ke outputs/reports sebagai JSON (konversi JSON-safe)."""
    ensure_dir(OUTPUT_REPORTS_DIR)
    path = OUTPUT_REPORTS_DIR / filename

    safe_report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        **to_json_safe(eda_result),
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(safe_report, f, indent=2, ensure_ascii=False, default=str)
    logger.info(f"EDA Report disimpan: {path}")