#!/usr/bin/env python3
"""Inspect HTML structure of target sites to find correct CSS selectors."""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

sites = [
    ("leiphone_ai", "https://www.leiphone.com/category/aihealth"),
    ("36kr_health", "https://36kr.com/information/healthcare"),
    ("36kr_ai", "https://36kr.com/information/AI"),
    ("huxiu", "https://www.huxiu.com"),
    ("pharmcube", "https://www.pharmcube.com"),
    ("nmpa", "https://www.nmpa.gov.cn"),
    ("cdstic", "https://www.cde.org.cn"),
]

for name, url in sites:
    print(f"\n{'='*60}")
    print(f"SITE: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        print(f"Status: {resp.status_code}")
        print(f"Final URL: {resp.url}")
        
        soup = BeautifulSoup(resp.text, "lxml")
        
        # Find common article containers
        selectors_to_try = [
            "article", ".article-item", ".article", ".news-item", ".item",
            ".information-item", ".post", ".feed-item", ".list-item",
            "[class*='article']", "[class*='news']", "[class*='item']",
        ]
        
        for sel in selectors_to_try:
            items = soup.select(sel)
            if items:
                print(f"\n  Selector '{sel}' found {len(items)} items")
                # Show first item's structure
                first = items[0]
                # Find title and link within first item
                title_el = first.find(["h1","h2","h3","h4","a"])
                if title_el:
                    print(f"    First item title: {title_el.get_text(strip=True)[:80]}")
                    link = title_el.get("href") or title_el.find("a", href=True)
                    if link:
                        if isinstance(link, str):
                            print(f"    Link: {link[:100]}")
                        else:
                            print(f"    Link: {link.get('href','')[:100]}")
                break
        else:
            print("  No article containers found with common selectors")
            # Show body structure hints
            body = soup.find("body")
            if body:
                classes = [c for c in body.get("class", []) if c]
                print(f"  Body classes: {classes[:5]}")
                
    except Exception as e:
        print(f"ERROR: {e}")
