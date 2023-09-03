from __future__ import annotations

import logging


def setup_root_logger(module_name: str, log_level: int) -> None:
    logger = logging.getLogger(module_name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(levelname)7s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(log_level)
