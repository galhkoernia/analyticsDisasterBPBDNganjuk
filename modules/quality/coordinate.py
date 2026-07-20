#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Validasi koordinat geografis."""

from typing import Any

import pandas as pd

from config.constants import NGANJUK_BBOX
from modules.utils.helper import safe_percentage
from modules.utils.logger import get_logger

logger = get_logger(__name__)


def check_coordinates(df: pd.DataFrame) -> dict[str, Any]:
    """Validasi kolom latitude/longitude.
    """
    
    if "latitude" not in df.columns or "longitude" not in df.columns:
        logger.warning("Kolom latitude/longitude tidak ditemukan")
        return {"error": "missing_coordinate_columns"}

    n_rows = len(df)
    lat, lon = df["latitude"], df["longitude"]

    missing_mask = lat.isna() | lon.isna()
    n_missing = int(missing_mask.sum())

    valid_range_mask = lat.between(-90, 90) & lon.between(-180, 180)
    out_of_range_mask = ~valid_range_mask & ~missing_mask
    n_out_of_range = int(out_of_range_mask.sum())

    in_bbox_mask = (
        lat.between(NGANJUK_BBOX["lat_min"], NGANJUK_BBOX["lat_max"])
        & lon.between(NGANJUK_BBOX["lon_min"], NGANJUK_BBOX["lon_max"])
    )
    out_of_bbox_mask = ~in_bbox_mask & valid_range_mask & ~missing_mask
    n_out_of_bbox = int(out_of_bbox_mask.sum())

    n_valid = n_rows - n_missing - n_out_of_range - n_out_of_bbox

    logger.info(
        f"Koordinat: {n_valid} valid, {n_missing} kosong, "
        f"{n_out_of_range} di luar range, {n_out_of_bbox} di luar bbox Nganjuk"
    )

    return {
        "n_valid": n_valid,
        "n_missing": n_missing,
        "n_out_of_range": n_out_of_range,
        "n_out_of_bbox": n_out_of_bbox,
        "valid_percentage": safe_percentage(n_valid, n_rows),
        "missing_row_indices": df[missing_mask].index.tolist(),
        "out_of_range_row_indices": df[out_of_range_mask].index.tolist(),
        "out_of_bbox_row_indices": df[out_of_bbox_mask].index.tolist(),
    }
