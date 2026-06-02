#!/usr/bin/env python3
"""
China AI Health — AI Translation Module
==========================================
Reads candidates_YYYY-MM-DD.json, sends each article to SiliconFlow API
for English translation + summary + key points extraction (JSON output).
Processed results saved to processed_YYYY-MM-DD.json.
"""

import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone

import requests
import yaml

# Fix Windows console encoding for Chinese/emoji output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as cfg

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("translate")

CST = timezone(timedelta(hours=8))
TODAY = datetime.now(CST).strftime("%Y-%m-%d")


# ════════════════════════════════════════════════════
#  SiliconFlow API Call
# ════════════════════════════════════════════════════

SYSTEM_PROMPT = cfg.TRANSLATION_SYSTEM_PROMPT
USER_PROMPT_TPL = cfg.TRANSLATION_USER_PROMPT_TEMPLATE


def call_siliconflow(cn_title, cn_content):
    """Call SiliconFlow API, return parsed JSON dict or None."""
    prompt = USER_PROMPT_TPL.format(
        cn_title=cn_title,
        cn_content=cn_content[:3000],  # cap content length
    )

    payload = {
        "model": cfg.SILICONFLOW_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 800,
    }

    headers = {
        "Authorization": f"Bearer {cfg.SILICONFLOW_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            cfg.SILICONFLOW_BASE_URL,
            json=payload,
            headers=headers,
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()

        # Strip markdown code fences if present
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        return json.loads(content)

    except Exception as e:
        log.warning(f"API call failed: {e}")
        return None


# ════════════════════════════════════════════════════
#  Main
# ════════════════════════════════════════════════════

def translate_all():
    in_path = os.path.join(cfg.CANDIDATES_DIR, f"candidates_{TODAY}.json")
    out_path = os.path.join(cfg.PROCESSED_DIR, f"processed_{TODAY}.json")

    if not os.path.exists(in_path):
        log.error(f"Candidates file not found: {in_path}")
        log.error("Run crawl.py first!")
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    log.info(f"Loaded {len(candidates)} candidates from {in_path}")

    results = []
    failed = 0

    # Load existing progress if any
    if os.path.exists(out_path):
        try:
            with open(out_path, "r", encoding="utf-8") as f:
                results = json.load(f)
            log.info(f"Resuming from {len(results)} already translated")
        except Exception:
            pass

    already_done = {a.get("url") for a in results}

    for i, art in enumerate(candidates, 1):
        # Skip already translated
        if art.get("url") in already_done:
            continue

        title = art.get("title", "")[:80]
        log.info(f"[{i}/{len(candidates)}] Translating: {title}...")

        cn_content = art.get("summary", "")
        if not cn_content or len(cn_content) < 50:
            # Fetch full content if summary is too short
            cn_content = fetch_full_content(art.get("url", ""))

        result = call_siliconflow(art.get("title", ""), cn_content)

        if result:
            merged = {**art, **result}
            results.append(merged)
            log.info(f"  ✓ en_title: {result.get('en_title', '')[:60]}...")
        else:
            failed += 1
            art["en_title"] = art.get("title", "")
            art["en_summary"] = ""
            art["en_key_points"] = []
            art["tags"] = []
            results.append(art)
            log.warning(f"  ✗ Failed — kept original title")

        # Save after each article (incremental)
        os.makedirs(cfg.PROCESSED_DIR, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # Rate limit: SiliconFlow free tier ~10 req/min
        if i % 8 == 0:
            log.info("  (rate limit pause 6s)")
            time.sleep(6)
        else:
            time.sleep(1)

    log.info("=" * 50)
    log.info(f"Done. Success: {len(results) - failed} | Failed: {failed}")
    log.info(f"Saved → {out_path}")


def fetch_full_content(url):
    """Best-effort: fetch full article text (fallback for short summaries)."""
    try:
        import requests as r
        resp = r.get(url, timeout=10, headers={"User-Agent": cfg.USER_AGENT})
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "lxml")
        # Remove scripts/styles
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        # Try common content selectors
        content_el = (
            soup.select_one("article")
            or soup.select_one(".article-content")
            or soup.select_one(".content")
            or soup.select_one("main")
        )
        if content_el:
            return content_el.get_text(" ", strip=True)[:4000]
        return soup.get_text(" ", strip=True)[:4000]
    except Exception:
        return ""


if __name__ == "__main__":
    translate_all()