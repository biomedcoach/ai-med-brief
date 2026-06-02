import sys, io, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from crawl import crawl_with_playwright, score_article, is_duplicate, init_db
from config import SOURCES, TITLE_BLACKLIST, NOW
from playwright.sync_api import sync_playwright

# Only leiphone
lp_src = [s for s in SOURCES if s['name'] == 'leiphone_ai'][0]
print(f'Source: {lp_src["name"]} → {lp_src["url"]}')

p = sync_playwright().start()
browser = p.chromium.launch(headless=True)
articles = crawl_with_playwright(lp_src, browser)
browser.close()
p.stop()

print(f'\nFetched {len(articles)} articles from leiphone_ai')
print()

conn = init_db()

for art in articles[:15]:
    title = art['title']
    url = art['url']
    score = score_article(art)
    dup = is_duplicate(conn, url, title)
    blacklisted = any(b in title for b in TITLE_BLACKLIST)
    
    verdict = 'PASS' if (not dup and score >= 20 and not blacklisted) else f'FAIL(dup={dup}, score={score}, bl={blacklisted})'
    print(f'  {verdict} | {title[:60]}')
    
conn.close()