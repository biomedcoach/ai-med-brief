#!/usr/bin/env python3
"""Debug leiphone article structure."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.leiphone.com/category/aihealth", wait_until="networkidle")
    
    print("Page title:", page.title())
    
    # Try .list
    lists = page.query_selector_all(".list")
    print(f"\n.list found: {len(lists)}")
    for i, lst in enumerate(lists[:2]):
        print(f"\n  List {i+1}:")
        # Get all links inside
        links = lst.query_selector_all("a")
        for j, link in enumerate(links[:5]):
            href = link.get_attribute("href") or ""
            text = link.inner_text()[:80].replace('\n', ' ')
            print(f"    [{j+1}] {text} -> {href}")
    
    # Try .sub_a
    subs = page.query_selector_all(".sub_a")
    print(f"\n.sub_a found: {len(subs)}")
    for i, sub in enumerate(subs[:3]):
        text = sub.inner_text()[:80].replace('\n', ' ')
        href = sub.get_attribute("href") or ""
        print(f"  [{i+1}] {text} -> {href}")
    
    # Try looking for article cards with images
    cards = page.query_selector_all(".word, .headTit")
    print(f"\n.word found: {len(cards)}")
    for i, card in enumerate(cards[:3]):
        text = card.inner_text()[:80].replace('\n', ' ')
        print(f"  [{i+1}] {text}")
    
    browser.close()
