from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)7s] %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
