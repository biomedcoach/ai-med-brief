#!/usr/bin/env python3
"""Debug script: test each source individually to see what's happening."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as cfg
import yaml
import feedparser
import requests
from bs4 import BeautifulSoup

with open(cfg.SOURCES_FILE, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

print("=" * 70)
print("SOURCE DIAGNOSTIC")
print("=" * 70)

for src in config["sources"]:
    name = src["name"]
    print(f"\n--- {name} ({src['type']}) ---")
    
    if src["type"] == "rss":
        feed = feedparser.parse(src["rss_url"])
        print(f"  Entries found: {len(feed.entries)}")
        if feed.entries:
            for i, e in enumerate(feed.entries[:3]):
                title = e.get("title", "N/A")[:60]
                print(f"    {i+1}. {title}")
        else:
            print(f"  Feed status: {feed.get('status', 'unknown')}")
            print(f"  Feed bozo: {feed.get('bozo', 'N/A')}")
    
    elif src["type"] == "html":
        try:
            resp = requests.get(src["url"], timeout=15, headers={"User-Agent": cfg.USER_AGENT})
            print(f"  Status: {resp.status_code}")
            soup = BeautifulSoup(resp.text, "lxml")
            items = soup.select(src.get("list_selector", "article"))
            print(f"  Items found: {len(items)}")
            if items:
                for i, item in enumerate(items[:2]):
                    title_el = item.select_one(src["title_selector"])
                    title = title_el.get_text(strip=True)[:60] if title_el else "NO TITLE"
                    print(f"    {i+1}. {title}")
        except Exception as e:
            print(f"  ERROR: {e}")

print("\n" + "=" * 70)
