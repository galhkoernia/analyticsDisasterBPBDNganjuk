#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Ekspor chart dan peta interaktif ke outputs/figures."""

import folium
import plotly.graph_objects as go

from config.settings import OUTPUT_FIGURES_DIR
from modules.utils.helper import ensure_dir
from modules.utils.logger import get_logger

logger = get_logger(__name__)


def export_charts(charts: dict[str, go.Figure]) -> None:
    """Simpan seluruh chart sebagai file HTML interaktif."""
    ensure_dir(OUTPUT_FIGURES_DIR)
    for name, fig in charts.items():
        path = OUTPUT_FIGURES_DIR / f"{name}.html"
        fig.write_html(str(path))
        logger.info(f"Chart '{name}' disimpan: {path}")


def export_map(disaster_map: folium.Map, filename: str = "disaster_map.html") -> None:
    """Simpan peta sebagai file HTML interaktif."""
    ensure_dir(OUTPUT_FIGURES_DIR)
    path = OUTPUT_FIGURES_DIR / filename
    disaster_map.save(str(path))
    logger.info(f"Peta kejadian disimpan: {path}")


def export_visualizations(charts: dict[str, go.Figure], disaster_map: folium.Map | None) -> None:
    """Ekspor seluruh chart dan peta hasil Visualization Engine."""
    export_charts(charts)
    if disaster_map is not None:
        export_map(disaster_map)
    else:
        logger.warning("Peta kejadian tidak tersedia, export peta dilewati")