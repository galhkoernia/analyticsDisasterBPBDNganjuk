#
# Created on Thu Jul 02 2026
#
# Copyright (c) 2026 galhkoernia
#


"""Entry point Disaster Analytics Engine.
"""
import pandas as pd

from modules.ingestion.loader import load_dataset
from modules.ingestion.validator import profile_dataset, rename_to_logical, validate_schema
from modules.quality.report import export_report, generate_quality_report
from modules.utils.logger import get_logger

from modules.preprocessing.cleaner import clean_pipeline
from modules.preprocessing.transformer import transform_pipeline
from modules.preprocessing.feature_engineering import feature_engineering_pipeline
from config.settings import DATA_PROCESSED_DIR
from modules.utils.helper import ensure_dir

from modules.analysis.eda_report import export_eda_report, generate_eda_report
from modules.visualization.dashboard import build_dashboard

from modules.analysis.statistics import export_statistical_report, generate_statistical_report
from modules.insight.generator import export_insight_report, generate_insight_report

from modules.visualization.charts import generate_charts
from modules.visualization.export import export_visualizations
from modules.visualization.maps import build_disaster_map


logger = get_logger(__name__)


def run_pipeline(filename: str | None = None) -> None:
    # Data Understanding
    df = pd.read_excel(filename) if filename else load_dataset()
    schema_check = validate_schema(df)
    if schema_check["missing_columns"]:
        logger.warning(
            "Sebagian kolom di RAW_COLUMN_MAP tidak ditemukan di dataset. "
        )

    logger.info("Tahap 1 (Data Understanding)")

    df = rename_to_logical(df)
    profile_dataset(df)

    # Data Quality Assessment
    report = generate_quality_report(df)
    export_report(report)

    logger.info("Tahap 2 (Data Quality Assessment)")

    # Data Preprocessing
    df_clean = clean_pipeline(df, consistency_result=report["consistency"])
    df_clean = transform_pipeline(df_clean)
    df_clean = feature_engineering_pipeline(df_clean)

    ensure_dir(DATA_PROCESSED_DIR)
    output_path = DATA_PROCESSED_DIR / "clean_dataset.csv"
    df_clean.to_csv(output_path, index=False)
    logger.info(f"Clean Dataset disimpan: {output_path}")
    logger.info("Tahap 3 (Data Preprocessing)")

    # Exploratory Data Analysis
    eda_result = generate_eda_report(df_clean)
    export_eda_report(eda_result)
    logger.info("Tahap 4 (Exploratory Data Analysis)")

    # Statistical Analysis
    statistical_report = generate_statistical_report(df_clean, eda_result)
    export_statistical_report(statistical_report)
    logger.info("Tahap 5 (Statistical Analysis)")

    # Insight Generator
    insight_report = generate_insight_report(
        eda_result=eda_result,
        statistical_report=statistical_report,
        quality_report=report,
    )
    export_insight_report(insight_report)
    logger.info("Tahap 6 (Insight Generator)")


    # Visualization Engine
    charts = generate_charts(statistical_report, insight_report)
    disaster_map = build_disaster_map(df_clean)
    export_visualizations(charts, disaster_map)
    logger.info("Tahap 7 (Visualization Engine)")

    # Dashboard Builder
    build_dashboard()
    logger.info("Tahap 8 (Dashboard Integration)")
if __name__ == "__main__":
    run_pipeline()