#!/usr/bin/env python3
"""Debug Playwright selectors by dumping actual page HTML."""
from playwright.sync_api import sync_playwright

sites = [
    ("36kr_health", "https://36kr.com/information/healthcare"),
    ("36kr_ai", "https://36kr.com/information/AI"),
    ("huxiu", "https://www.huxiu.com"),
    ("leiphone_ai", "https://www.leiphone.com/category/aihealth"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for name, url in sites:
        print(f"\n{'='*60}")
        print(f"SITE: {name}")
        print(f"URL: {url}")
        print(f"{'='*60}")
        
        page = browser.new_page()
        page.set_default_timeout(30000)
        
        try:
            page.goto(url, wait_until="networkidle")
            
            # Get page title
            title = page.title()
            print(f"Page title: {title}")
            
            # Try to find article containers by common patterns
            selectors_to_try = [
                "article",
                "[class*='item']",
                "[class*='article']",
                "[class*='news']",
                "[class*='list']",
                "[class*='card']",
                "[class*='post']",
                "[class*='feed']",
                "h3",
                "h2",
            ]
            
            for sel in selectors_to_try:
                items = page.query_selector_all(sel)
                if items and len(items) > 0 and len(items) < 200:
                    print(f"\n  Selector '{sel}' found {len(items)} items")
                    # Show first item's text content
                    first = items[0]
                    text = first.inner_text()[:200].replace('\n', ' ')
                    print(f"    First: {text}")
                    break
            else:
                print("  No article containers found")
                # Dump a snippet of body HTML
                body_html = page.inner_html("body")
                print(f"  Body HTML snippet (first 1000 chars):")
                print(f"  {body_html[:1000]}")
                
        except Exception as e:
            print(f"  ERROR: {e}")
        finally:
            page.close()
    
    browser.close()
