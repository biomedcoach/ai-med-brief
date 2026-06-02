#!/usr/bin/env python3
"""Test RSS feeds with requests + manual parsing to debug issues."""
import requests
import xml.etree.ElementTree as ET

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

feeds = [
    ("vcbeat", "https://vcbeat.top/feed"),
    ("bioon", "https://www.bioon.com/feed"),
    ("yigoo", "https://www.yigoonet.com/feed"),
    ("cn_healthcare", "https://www.cn-healthcare.com/rss"),
    ("medicaldevice", "https://www.innomd.org/feed"),
    ("yaozh", "https://www.yaozh.com/feed"),
    ("jiqizhixin", "https://www.jiqizhixin.com/rss"),
    ("gepresearch", "https://www.yyjjb.com.cn/feed"),
]

for name, url in feeds:
    print(f"\n{'='*60}")
    print(f"FEED: {name}")
    print(f"URL: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        print(f"Status: {resp.status_code}")
        print(f"Final URL: {resp.url}")
        print(f"Content-Type: {resp.headers.get('Content-Type', 'N/A')}")
        print(f"Content length: {len(resp.text)} bytes")
        
        if resp.status_code == 200:
            # Try to parse as XML
            try:
                root = ET.fromstring(resp.text[:50000])  # limit size
                # Find items/entries
                items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')
                print(f"Items found: {len(items)}")
                if items:
                    for i, item in enumerate(items[:3]):
                        title = item.find('title')
                        title_text = title.text[:80] if title is not None and title.text else "N/A"
                        print(f"  {i+1}. {title_text}")
            except ET.ParseError as e:
                print(f"XML Parse Error: {e}")
                # Show first 500 chars of content
                print(f"Content preview: {resp.text[:500]}")
        else:
            print(f"Failed with status {resp.status_code}")
            print(f"Response preview: {resp.text[:300]}")
            
    except Exception as e:
        print(f"ERROR: {e}")
