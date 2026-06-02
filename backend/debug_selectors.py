#!/usr/bin/env python3
"""Debug: find exact CSS selectors for article items."""
from playwright.sync_api import sync_playwright

def debug_site(page, name):
    print(f"\n{'='*60}")
    print(f"SITE: {name}")
    print(f"{'='*60}")
    
    # Get all elements with class attributes and show common patterns
    elements = page.query_selector_all("*")
    class_counts = {}
    for el in elements:
        cls = el.get_attribute("class")
        if cls:
            for c in cls.split():
                if len(c) > 3:
                    class_counts[c] = class_counts.get(c, 0) + 1
    
    # Show top class names
    print("Top class names:")
    for cls, count in sorted(class_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  .{cls} ({count})")
    
    # Try to find article-like elements
    print("\nTrying selectors:")
    test_selectors = [
        ".article-item",
        ".information-item", 
        ".item",
        ".feed-item",
        ".post-item",
        ".news-item",
        "[data-aid]",
        "[data-track]",
        ".article",
        ".post",
    ]
    
    for sel in test_selectors:
        items = page.query_selector_all(sel)
        if items and 0 < len(items) < 100:
            print(f"  {sel}: {len(items)} items")
            for i, item in enumerate(items[:2]):
                text = item.inner_text()[:100].replace('\n', ' ')
                print(f"    [{i+1}] {text}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 36kr AI
    page = browser.new_page()
    page.goto("https://36kr.com/information/AI", wait_until="networkidle")
    debug_site(page, "36kr_ai")
    page.close()
    
    # Leiphone
    page = browser.new_page()
    page.goto("https://www.leiphone.com/category/aihealth", wait_until="networkidle")
    debug_site(page, "leiphone_ai")
    page.close()
    
    browser.close()
