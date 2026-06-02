import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/candidates/candidates_2026-05-31.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

medical_keywords = ['医疗','医学','药','诊断','手术','影像','基因','蛋白','临床','患者','医院','器械','内镜','机器人','医','健康','CMEF','NMPA','脑','细胞','肿瘤','呼吸机','AI中','智能医','联影','安顿','阿里健康','丁香园']

med_articles = []
non_med = []
for item in data:
    title = item['title']
    summary = item.get('summary', '')
    text = title + summary
    if any(kw in text for kw in medical_keywords):
        med_articles.append(item)
    else:
        non_med.append(item)

print('=== 医疗AI相关文章 ===')
print()
for i, item in enumerate(med_articles, 1):
    print(f'{i}. [{item["source"]}] QS={item["quality_score"]} {item["title"]}')
    s = item.get('summary', '')[:120]
    print(f'   摘要: {s}')
    print(f'   URL: {item["url"]}')
    print()

print(f'=== 非医疗文章（共{len(non_med)}篇）===')
for i, item in enumerate(non_med, 1):
    print(f'{i}. [{item["source"]}] {item["title"]}')