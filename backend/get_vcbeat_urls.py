import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

articles = [
    "ASCO 2026：中国ADC全面炸场！一线突破+双抗迭代+多靶点齐爆发",
    "ASCO 2026：α核素引爆！从β到α，中国核药抢占全球风口",
    "2.1亿C1轮融资落地！睿健医药加速打造全球化平台型细胞治疗Biotech",
    "血霁生物完成B轮近3亿元增资，用于血小板减少和抗衰老药物开发",
    "博凡格鲁肽，全球首个进入肥胖/超重临床III期的长效GLP-1 RA双周制剂",
    "ASCO2026 LBA | 君赛生物GC101 TIL关键Ⅱ期成功，疗效与安全性优异",
    "复宏汉霖联合创始人创办：汉康获得OrbiMed投资，在台湾创新板挂牌",
    "美的，拟全资收购，再加码医疗影像",
    "多场景激光医疗技术平台企业密尔医疗完成亿元B轮融资",
    "Presbia如何用一枚15微米透镜挑战老视矫正",
    "Space Pharm受邀香港—瑞士生物技术圆桌会议，共推AI多肽创新药跨境合作",
    "AI蛋白质设计如何重塑止痛药的未来",
    "数因智科完成Pre-A轮融资，AI+RNA双轮驱动医药消费赛道提速",
]

p = sync_playwright().start()
browser = p.chromium.launch(headless=True)
page = browser.new_page()
page.goto("https://www.vcbeat.top/", timeout=30000, wait_until="networkidle")
page.wait_for_timeout(3000)

content = page.content()
page.close()
browser.close()
p.stop()

# Extract all article links
from bs4 import BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Find all article elements
all_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    text = a.get_text(strip=True)
    if text and len(text) > 10:
        all_links.append({'text': text, 'href': href})

# Try to match our target articles
for target in articles:
    target_short = target[:30]
    found = []
    for link in all_links:
        # Check if link text contains any significant part of the target title
        if len(target_short) >= 10 and target_short[:10] in link['text']:
            found.append(link)
    if found:
        print(f"✓ {target[:50]}")
        for f in found:
            print(f"  → {f['href']} | {f['text'][:80]}")
    else:
        # Try fuzzy match
        for link in all_links:
            text = link['text']
            # Check character overlap
            common = set(target) & set(text)
            if len(common) / max(len(set(target)), 1) > 0.3 and len(text) > 15:
                found.append(link)
        if found:
            print(f"~ {target[:50]}")
            for f in found[:3]:
                print(f"  → {f['href']} | {f['text'][:80]}")
        else:
            print(f"✗ {target[:50]} (not found)")

# Also dump all article-like elements
print("\n=== All potential article links ===")
seen = set()
for link in all_links:
    if len(link['text']) > 20 and link['text'] not in seen:
        seen.add(link['text'])
        print(f"  {link['text'][:100]} → {link['href'][:80]}")
