#!/usr/bin/env python3
"""Test Baidu News scraping."""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cookie": "BAIDUID=1234567890:FG=1",
}

url = "https://www.baidu.com/s?wd=AI医疗&tn=news&cl=2&rn=20"
print(f"Fetching: {url}")

try:
    resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
    print(f"Status: {resp.status_code}")
    print(f"Final URL: {resp.url}")
    print(f"Content length: {len(resp.text)} bytes")
    
    soup = BeautifulSoup(resp.text, "lxml")
    
    # Try different selectors
    selectors = [
        ".result",
        ".c-container",
        "[tpl]",
        ".news-list .result",
        ".result-op",
    ]
    
    for sel in selectors:
        items = soup.select(sel)
        if items:
            print(f"\nSelector '{sel}' found {len(items)} items")
            for i, item in enumerate(items[:3]):
                title_el = item.find("h3") or item.select_one("a")
                title = title_el.get_text(strip=True)[:80] if title_el else "NO TITLE"
                print(f"  {i+1}. {title}")
            break
    else:
        print("\nNo items found with common selectors")
        # Show a snippet of the HTML
        print(f"\nHTML snippet (first 2000 chars):")
        print(soup.get_text()[:2000])
        
except Exception as e:
    print(f"ERROR: {e}")
