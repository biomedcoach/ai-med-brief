#!/usr/bin/env python3
"""Test translation with 1 article."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as cfg
from translate import call_siliconflow

# Load candidates
with open(r'D:\Qclaw\AiMedbrief\backend\data\candidates\candidates_2026-05-31.json', 'r', encoding='utf-8') as f:
    candidates = json.load(f)

# Test with first article
art = candidates[0]
print(f"Testing translation for:")
print(f"  Title: {art['title']}")
print(f"  Summary: {art.get('summary', 'N/A')[:100]}...")
print(f"\nCalling API...")

result = call_siliconflow(art['title'], art.get('summary', ''))

if result:
    print(f"\n✓ Success!")
    print(f"  EN Title: {result.get('en_title', 'N/A')}")
    print(f"  Tags: {result.get('tags', [])}")
    print(f"  Key Points: {result.get('en_key_points', [])}")
else:
    print(f"\n✗ Failed")
