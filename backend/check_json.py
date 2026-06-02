import json

with open(r'D:\Qclaw\AiMedbrief\backend\data\candidates\candidates_2026-05-31.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total articles: {len(data)}")
print("\nFirst 5 articles:")
for i, a in enumerate(data[:5], 1):
    print(f"{i}. [{a['quality_score']}] {a['title'][:60]}")
    print(f"   Source: {a['source']} | URL: {a['url'][:60]}")
