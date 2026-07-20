#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Pembuatan peta interaktif persebaran kejadian bencana."""

import zlib

import folium
import pandas as pd

from modules.utils.logger import get_logger

logger = get_logger(__name__)

_MARKER_COLORS: list[str] = [
    "red", "blue", "green", "purple", "orange", "darkred",
    "cadetblue", "darkgreen", "darkpurple", "pink", "gray",
]


def _marker_color(jenis_bencana: str) -> str:
    """Warna marker deterministik berdasarkan jenis bencana (hash stabil, bukan hash() bawaan)."""
    idx = zlib.crc32(jenis_bencana.encode("utf-8")) % len(_MARKER_COLORS)
    return _MARKER_COLORS[idx]


def _build_popup_html(row: pd.Series) -> str:
    """Susun konten popup marker dari satu baris dataset."""
    lines = [
        f"<b>Jenis Bencana:</b> {row.get('jenis_bencana', '-')}",
        f"<b>Kecamatan:</b> {row.get('kecamatan', '-')}",
    ]
    if "total_korban" in row and pd.notna(row["total_korban"]):
        lines.append(f"<b>Total Korban:</b> {row['total_korban']:.0f}")
    if "kerugian" in row and pd.notna(row["kerugian"]):
        lines.append(f"<b>Kerugian:</b> {row['kerugian']:,.0f}")
    return "<br>".join(lines)


def build_disaster_map(df: pd.DataFrame) -> folium.Map | None:
    """Bangun peta persebaran kejadian dari koordinat yang berhasil diparsing.
    """
    required_cols = {"latitude", "longitude", "koordinat_parse_status", "jenis_bencana", "kecamatan"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        logger.warning(f"Kolom peta tidak lengkap, pembuatan peta dilewati: {missing_cols}")
        return None

    valid = df[df["koordinat_parse_status"].str.startswith("ok", na=False)]
    if valid.empty:
        logger.warning("Tidak ada koordinat valid, pembuatan peta dilewati")
        return None

    disaster_map = folium.Map(
        location=[valid["latitude"].mean(), valid["longitude"].mean()], zoom_start=11
    )

    for _, row in valid.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(_build_popup_html(row), max_width=300),
            icon=folium.Icon(color=_marker_color(str(row["jenis_bencana"]))),
        ).add_to(disaster_map)

    logger.info(f"Peta kejadian dibuat: {len(valid)}/{len(df)} baris memiliki koordinat valid")
    return disaster_map