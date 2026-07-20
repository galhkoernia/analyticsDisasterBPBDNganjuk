#
# Created on Sat Jul 04 2026
#
# Copyright (c) 2026 galhkoernia
#

"""Konfigurasi logging terpusat."""

import logging
from pathlib import Path

from config.settings import LOG_FILE


def get_logger(name: str) -> logging.Logger:
    """Buat logger dengan handler file dan console."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
