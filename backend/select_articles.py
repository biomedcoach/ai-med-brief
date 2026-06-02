#!/usr/bin/env python3
"""
China AI Health — Article Selection
====================================
Reads processed_YYYY-MM-DD.json, auto-selects top N articles by quality score.
Saves to selected_YYYY-MM-DD.json for publish.py.
"""

import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as cfg

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("select")

CST = timezone(timedelta(hours=8))
TODAY = datetime.now(CST).strftime("%Y-%m-%d")
MAX_SELECTED = 10  # articles to publish per day


def select_auto():
    """Auto-select top articles by quality score."""
    # Prefer humanized version if available
    humanized_path = os.path.join(cfg.PROCESSED_DIR, f"humanized_{TODAY}.json")
    in_path = os.path.join(cfg.PROCESSED_DIR, f"processed_{TODAY}.json")
    out_path = os.path.join(cfg.SELECTED_DIR, f"selected_{TODAY}.json")

    if os.path.exists(humanized_path):
        in_path = humanized_path
        log.info(f"Using humanized file: {in_path}")
    elif not os.path.exists(in_path):
        log.error(f"Processed file not found: {in_path}")
        log.error("Run translate.py first!")
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    log.info(f"Loaded {len(articles)} processed articles")

    # Filter: must have en_title and en_summary
    valid = [a for a in articles if a.get("en_title") and a.get("en_summary")]
    log.info(f"Valid articles (with translation): {len(valid)}")

    # Sort by quality_score descending
    valid.sort(key=lambda a: a.get("quality_score", 0), reverse=True)

    # Take top N
    selected = valid[:MAX_SELECTED]
    log.info(f"Selected top {len(selected)} articles")

    # Save
    os.makedirs(cfg.SELECTED_DIR, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(selected, f, ensure_ascii=False, indent=2)

    log.info(f"Saved → {out_path}")

    # Print summary
    log.info("=" * 50)
    for i, a in enumerate(selected, 1):
        log.info(f"  {i}. [{a.get('quality_score', 0):.0f}] {a.get('en_title', '')[:60]}")


if __name__ == "__main__":
    select_auto()
