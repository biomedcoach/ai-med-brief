import json

with open(r'D:\Qclaw\AiMedbrief\articles\data.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Translate source names to English
source_map = {
    '动脉网 / vbdata.cn': 'VCBeat / VBData',
    '动脉网': 'VCBeat / VBData',
    '生物谷': 'Bioon',
    '生物谷 / bioon.com': 'Bioon',
    '雷锋网': 'Leiphone',
    '36氪': '36Kr',
}

for a in articles:
    src = a['source']
    if src in source_map:
        a['source'] = source_map[src]
    # Also translate any Chinese in url description
    if '动脉网' in a.get('url', ''):
        a['url'] = a['url'].replace('动脉网', 'VCBeat')

with open(r'D:\Qclaw\AiMedbrief\articles\data.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print('Updated sources:')
for a in articles:
    print(f"  {a['id']}: source={a['source']}, url={a['url'][:60]}")

# Rebuild index and articles
print('done')