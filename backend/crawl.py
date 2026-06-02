#!/usr/bin/env python3
"""
China AI Health — Crawler (Playwright version)
===============================================
Uses Playwright to render JS-heavy sites, then extracts articles.
Falls back to requests for simple HTML sites.
"""

import argparse
import difflib
import hashlib
import json
import logging
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

import requests
import yaml
from bs4 import BeautifulSoup

# Playwright
from playwright.sync_api import sync_playwright

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
log = logging.getLogger("crawl")

CST = timezone(timedelta(hours=8))
TODAY = datetime.now(CST).strftime("%Y-%m-%d")
NOW = datetime.now(CST)


# ══════════════════════════════════════════════════════
#  Database (SQLite: dedup history)
# ══════════════════════════════════════════════════════

def init_db():
    conn = sqlite3.connect(cfg.DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_hash TEXT UNIQUE,
            title TEXT,
            url TEXT,
            source TEXT,
            crawled_at TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_history_hash ON history(url_hash)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_history_crawled ON history(crawled_at)")
    conn.commit()
    return conn


def is_duplicate(conn, url, title):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    row = conn.execute("SELECT id FROM history WHERE url_hash = ?", (url_hash,)).fetchone()
    if row:
        return True

    cutoff = (NOW - timedelta(days=cfg.DEDUP_DAYS)).isoformat()
    rows = conn.execute("SELECT title FROM history WHERE crawled_at >= ?", (cutoff,)).fetchall()
    for (old_title,) in rows:
        if old_title and title:
            sim = difflib.SequenceMatcher(None, title.strip(), old_title.strip()).ratio()
            if sim >= cfg.DEDUP_SIMILARITY:
                return True
    return False


def mark_crawled(conn, url, title, source):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    conn.execute(
        "INSERT OR IGNORE INTO history(url_hash, title, url, source, crawled_at) VALUES (?,?,?,?,?)",
        (url_hash, title, url, source, NOW.isoformat()),
    )
    conn.commit()


# ══════════════════════════════════════════════════════
#  Playwright-based scraping
# ══════════════════════════════════════════════════════

def crawl_with_playwright(src, browser):
    """Use Playwright to scrape JS-rendered pages."""
    articles = []
    page = browser.new_page()
    page.set_default_timeout(20000)

    try:
        log.info(f"  [Playwright] Navigating {src['url']}...")
        page.goto(src["url"], wait_until="networkidle")

        # Wait for content to load
        list_sel = src.get("list_selector", "article")
        try:
            page.wait_for_selector(list_sel, timeout=10000)
        except Exception:
            log.warning(f"  Timeout waiting for {list_sel}, trying anyway...")

        # Extract items
        items = page.query_selector_all(list_sel)
        log.info(f"  Found {len(items)} items with selector '{list_sel}'")

        for item in items[:cfg.MAX_ARTICLES_PER_SOURCE]:
            # Title
            title_el = item.query_selector(src.get("title_selector", "h3 a, h2 a, a"))
            if not title_el:
                continue
            title = title_el.inner_text().strip()

            # Link
            link = title_el.get_attribute("href") or ""
            if not link:
                continue
            link = urljoin(src["url"], link)

            # Summary
            summary = ""
            if src.get("summary_selector"):
                sum_el = item.query_selector(src["summary_selector"])
                if sum_el:
                    summary = sum_el.inner_text().strip()

            # Date
            date_str = ""
            if src.get("date_selector"):
                date_el = item.query_selector(src["date_selector"])
                if date_el:
                    date_str = date_el.inner_text().strip()

            articles.append({
                "title": title,
                "url": link,
                "summary": summary,
                "published": NOW.isoformat(),
                "source": src["name"],
                "source_authority": src.get("authority", 5),
            })

    except Exception as e:
        log.warning(f"  Playwright error: {e}")
    finally:
        page.close()

    return articles


# ══════════════════════════════════════════════════════
#  Simple HTTP scraping (fallback)
# ══════════════════════════════════════════════════════

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": cfg.USER_AGENT})


def crawl_with_requests(src):
    """Simple HTTP scraping for non-JS sites."""
    articles = []
    try:
        resp = SESSION.get(src["url"], timeout=cfg.REQUEST_TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        log.warning(f"  HTTP error: {e}")
        return articles

    soup = BeautifulSoup(resp.text, "lxml")
    items = soup.select(src.get("list_selector", "article"))
    log.info(f"  Found {len(items)} items with selector '{src.get('list_selector')}'")

    for item in items[:cfg.MAX_ARTICLES_PER_SOURCE]:
        title_el = item.select_one(src.get("title_selector", "h3 a"))
        if not title_el:
            continue
        title = title_el.get_text(" ", strip=True)

        link_el = item.select_one(src.get("link_selector", src.get("title_selector", "h3 a")))
        if not link_el:
            continue
        link = link_el.get("href", "").strip()
        if not link:
            continue
        link = urljoin(src["url"], link)

        summary = ""
        if src.get("summary_selector"):
            sel = item.select_one(src["summary_selector"])
            if sel:
                summary = sel.get_text(" ", strip=True)

        articles.append({
            "title": title,
            "url": link,
            "summary": summary,
            "published": NOW.isoformat(),
            "source": src["name"],
            "source_authority": src.get("authority", 5),
        })

    return articles


# ══════════════════════════════════════════════════════
#  Quality Scoring
# ══════════════════════════════════════════════════════

with open(cfg.SOURCES_FILE, "r", encoding="utf-8") as f:
    _yaml = yaml.safe_load(f)
SCORING = _yaml.get("scoring", {})
WEIGHTS = SCORING.get("weights", cfg.SCORE_WEIGHTS)
RELEVANCE_KW = SCORING.get("relevance_keywords", {})
PRIMARY_KW = RELEVANCE_KW.get("primary", [])
SECONDARY_KW = RELEVANCE_KW.get("secondary", [])
HOUR_DECAY = SCORING.get("hour_decay_rate", 0.05)


def score_article(art):
    title = art["title"]
    summary = art.get("summary", "")
    text = (title + " " + summary).lower()

    # Freshness
    age_hours = 24
    art_pub = art.get("published")
    if art_pub:
        try:
            pub = datetime.fromisoformat(art_pub)
            age_hours = max(1, (NOW - pub).total_seconds() / 3600)
        except Exception:
            pass
    freshness_raw = max(0, 1 - HOUR_DECAY * age_hours)
    freshness = freshness_raw * 30

    # Authority
    auth = art.get("source_authority", 5)
    authority = (auth / 10) * 25

    # Relevance
    primary_count = sum(1 for kw in PRIMARY_KW if kw.lower() in text)
    if primary_count == 0:
        relevance = 0
    else:
        secondary_count = sum(1 for kw in SECONDARY_KW if kw.lower() in text)
        relevance = (min(primary_count, 3) / 3 * 12) + (min(secondary_count, 5) / 5 * 8)

    # Density
    text_len = len(text)
    if text_len < cfg.MIN_CONTENT_LENGTH:
        density = 1
    elif text_len > 5000:
        density = 15
    else:
        density = min(15, (text_len / 5000) * 15)

    # Rarity
    rarity = 8

    total = freshness + authority + relevance + density + rarity
    return round(min(100, total), 1)


# ══════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════

def crawl_all():
    with open(cfg.SOURCES_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    sources = config["sources"]
    conn = init_db()

    all_articles = []
    stats = {"total_fetched": 0, "duplicates": 0, "filtered": 0}

    # Launch Playwright browser once
    use_playwright = any(s.get("render") == "playwright" for s in sources)
    browser = None
    if use_playwright:
        log.info("Launching Playwright browser...")
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=True)

    try:
        for src in sources:
            name = src["name"]
            log.info(f"Crawling {name} ({src['type']})...")

            if src.get("render") == "playwright":
                articles = crawl_with_playwright(src, browser)
            else:
                articles = crawl_with_requests(src)

            for art in articles:
                stats["total_fetched"] += 1

                if is_duplicate(conn, art["url"], art["title"]):
                    stats["duplicates"] += 1
                    continue

                if any(b in art["title"] for b in cfg.TITLE_BLACKLIST):
                    stats["filtered"] += 1
                    continue

                score = score_article(art)
                if score < 20:
                    stats["filtered"] += 1
                    continue

                art["quality_score"] = score
                art["crawled_at"] = NOW.isoformat()
                all_articles.append(art)
                mark_crawled(conn, art["url"], art["title"], name)

            time.sleep(cfg.REQUEST_DELAY)

    finally:
        if browser:
            browser.close()
            p.stop()

    all_articles.sort(key=lambda a: a["quality_score"], reverse=True)

    os.makedirs(cfg.CANDIDATES_DIR, exist_ok=True)
    out_path = os.path.join(cfg.CANDIDATES_DIR, f"candidates_{TODAY}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    conn.close()

    log.info("=" * 50)
    log.info(f"Done. Fetched: {stats['total_fetched']} | Duplicates: {stats['duplicates']} | "
             f"Filtered: {stats['filtered']} | Candidates: {len(all_articles)}")
    log.info(f"Saved → {out_path}")

    print("\n Top 10 by Quality Score:")
    print("-" * 70)
    for i, a in enumerate(all_articles[:10], 1):
        print(f"  {i:2}. [QS {a['quality_score']:5.1f}] {a['title'][:60]}")
        print(f"      {a['source']:12s}")
    print()

    return all_articles


if __name__ == "__main__":
    crawl_all()