import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'D:\Qclaw\AiMedbrief\backend\data\candidates\candidates_2026-06-02.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total candidates: {len(data)}')
print()
for i, item in enumerate(data, 1):
    title = item['title']
    url = item['url']
    qs = item['quality_score']
    summary = item['summary'][:100]
    src = item['source']
    print(f'{i}. [{src}] {title}')
    print(f'   {url}')
    print(f'   QS: {qs}')
    print()