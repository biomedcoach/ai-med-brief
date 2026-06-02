#!/usr/bin/env python3
"""
China AI Health — Humanizer
=============================
Applies humanizer-zh rules to translated English text to remove
AI writing patterns and make content sound more natural.
"""

import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as cfg

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("humanize")

CST = timezone(timedelta(hours=8))
TODAY = datetime.now(CST).strftime("%Y-%m-%d")

SYSTEM_PROMPT = """You are a professional English editor specializing in removing AI-generated text patterns. Your task is to rewrite the provided English text to make it sound more natural and human-written.

## Rules to follow:

1. **Remove filler phrases** - Delete opening fillers and emphasis crutch words
2. **Break formulaic structures** - Avoid binary comparisons, dramatic paragraphing, rhetorical setups
3. **Vary rhythm** - Mix sentence lengths. Two items better than three. End paragraphs differently.
4. **Trust the reader** - State facts directly, skip softening, apologizing, and hand-holding
5. **Delete quotable quotes** - Rewrite anything that sounds like a pullquote
6. **Remove AI vocabulary** - Avoid: moreover, furthermore, however, it is worth noting that, it is important to, it is essential to, crucial, pivotal, landscape, testament, underscores, underscores the, highlights, demonstrates, exhibits, as well as, in addition, ultimately, leveraged, cutting-edge, innovative, groundbreaking, revolutionary, transformative
7. **Avoid "not only...but also" structures** - Use simpler constructions
8. **Delete vague attributions** - Don't say "experts say" or "industry observers note" without specific sources
9. **Remove dash overuse** - AI uses dashes more frequently than humans do
10. **Delete emoji** - Remove any emoji decorations
11. **Remove hedging phrases** - Instead of "it is believed that" or "it appears that", just state the fact
12. **Keep technical accuracy** - Don't change facts, numbers, or technical claims

## Quality criteria (1-10 each, target 45+/50):
- Directness: State facts plainly (10) vs. roundabout (1)
- Rhythm: Varied sentence length (10) vs. mechanical repetition (1)
- Trust: Respects reader intelligence (10) vs. over-explains (1)
- Authenticity: Sounds human (10) vs. robotic (1)
- Conciseness: No fluff (10) vs. padded (1)

## Output format:
Return ONLY the rewritten text. No explanations, no notes, no "here's the rewritten version". Just the text.

## Example:

INPUT: "Moreover, the new AI system represents a groundbreaking innovation that is set to revolutionize the healthcare industry. It is worth noting that this technology demonstrates remarkable capabilities in medical imaging analysis. Furthermore, experts believe it could have transformative implications for patient care."

OUTPUT: "The new AI system can analyze medical images with impressive accuracy. Early tests show promise for faster diagnoses. But questions remain about how it will perform in real clinical settings."
"""

USER_PROMPT_TPL = """Rewrite the following English text to remove AI writing patterns. Keep all facts, numbers, and technical information exactly as-is. Only change the writing style.

--- TEXT START ---
{en_text}
--- TEXT END ---

Return ONLY the rewritten text, nothing else:"""


def call_siliconflow(prompt, max_tokens=600):
    """Call SiliconFlow API for humanization."""
    payload = {
        "model": cfg.SILICONFLOW_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
        "max_tokens": max_tokens,
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
            timeout=90,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
        return content
    except Exception as e:
        log.warning(f"API call failed: {e}")
        return None


def humanize_text(en_title, en_summary, en_key_points):
    """Humanize all three text fields."""
    # Humanize title
    title_prompt = USER_PROMPT_TPL.format(en_text=en_title)
    new_title = call_siliconflow(title_prompt, max_tokens=100)
    if new_title:
        log.info(f"  Title: {new_title[:60]}...")
    else:
        new_title = en_title

    # Humanize summary
    summary_prompt = USER_PROMPT_TPL.format(en_text=en_summary)
    new_summary = call_siliconflow(summary_prompt, max_tokens=500)
    if new_summary:
        log.info(f"  Summary: {new_summary[:80]}...")
    else:
        new_summary = en_summary

    # Humanize key points
    new_key_points = []
    for kp in (en_key_points or []):
        kp_prompt = USER_PROMPT_TPL.format(en_text=kp)
        new_kp = call_siliconflow(kp_prompt, max_tokens=150)
        if new_kp:
            new_key_points.append(new_kp)
            log.info(f"  Point: {new_kp[:60]}...")
        else:
            new_key_points.append(kp)

    return new_title, new_summary, new_key_points


def humanize_all():
    """Load processed articles, humanize each, save."""
    in_path = os.path.join(cfg.PROCESSED_DIR, f"processed_{TODAY}.json")
    out_path = os.path.join(cfg.PROCESSED_DIR, f"humanized_{TODAY}.json")

    if not os.path.exists(in_path):
        log.error(f"Processed file not found: {in_path}")
        log.error("Run translate.py first!")
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    log.info(f"Loaded {len(articles)} processed articles for humanization")

    # Load existing humanized progress if any
    humanized = []
    if os.path.exists(out_path):
        try:
            with open(out_path, "r", encoding="utf-8") as f:
                humanized = json.load(f)
            log.info(f"Resuming from {len(humanized)} already humanized")
        except Exception:
            pass

    already_done = {a.get("url") for a in humanized}

    for i, art in enumerate(articles, 1):
        if art.get("url") in already_done:
            continue

        en_title = art.get("en_title", "")
        en_summary = art.get("en_summary", "")
        en_key_points = art.get("en_key_points", [])

        log.info(f"[{i}/{len(articles)}] Humanizing: {en_title[:50]}...")

        new_title, new_summary, new_key_points = humanize_text(
            en_title, en_summary, en_key_points
        )

        art["en_title"] = new_title
        art["en_summary"] = new_summary
        art["en_key_points"] = new_key_points
        humanized.append(art)

        # Save incrementally
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(humanized, f, ensure_ascii=False, indent=2)

        # Rate limit
        time.sleep(3)

    log.info("=" * 50)
    log.info(f"Done. Humanized {len(humanized)} articles")
    log.info(f"Saved → {out_path}")


if __name__ == "__main__":
    humanize_all()
