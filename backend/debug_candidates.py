import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read the raw crawl data
with open(r'D:\Qclaw\AiMedbrief\backend\data\candidates\candidates_2026-06-02.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total articles fetched: {len(data)}')
print()
print('=== Source breakdown ===')
sources = {}
for item in data:
    src = item['source']
    if src not in sources:
        sources[src] = 0
    sources[src] += 1

for src, count in sources.items():
    print(f'  {src}: {count}')

# The crawl log said "Fetched: 16 | Duplicates: 8 | Filtered: 0 | Candidates: 8"
# So 16 total, 8 were duplicates, leaving 8. But 0 filtered means keyword filter passed.
# The leiphone articles might have been counted as duplicates? That's weird.

# Let me check if the crawler's dup detection is the issue
print()
print('=== All articles ===')
for i, item in enumerate(data, 1):
    print(f'{i}. [{item["source"]}] QS={item["quality_score"]} {item["title"]}')