import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(headless=True)
page = browser.new_page()

# Monitor XHR/API calls
api_calls = []
def log_request(request):
    url = request.url
    if 'api' in url or 'article' in url or 'data' in url or 'list' in url or 'news' in url:
        api_calls.append({'url': url, 'method': request.method})

page.on('request', log_request)

page.goto("https://www.vcbeat.top/", timeout=60000, wait_until="domcontentloaded")
page.wait_for_timeout(5000)

# Check page source for article URL patterns  
html = page.content()
# Look for article links in raw HTML
import re
urls = re.findall(r'https?://[^\s"<>]+(?:article|news|detail|p/)[^\s"<>]+', html)
urls2 = re.findall(r'https?://(?:www\.)?vcbeat\.top[^\s"<>]*', html)
urls3 = re.findall(r'https?://(?:www\.)?vbdata\.cn[^\s"<>]*', html)

page.close()
browser.close()
p.stop()

print(f"API calls captured: {len(api_calls)}")
for call in api_calls[:20]:
    print(f"  {call['method']} {call['url'][:120]}")

print(f"\nArticle-like URLs in HTML: {len(urls)}")
for u in urls[:10]:
    print(f"  {u[:120]}")

print(f"\nvcbeat.top URLs: {len(urls2)}")
for u in urls2[:10]:
    print(f"  {u[:120]}")

print(f"\nvbdata.cn URLs: {len(urls3)}")
for u in urls3[:10]:
    print(f"  {u[:120]}")

# Also try clicking on a section first approach
print("\n=== Article-like text in HTML ===")
texts = re.findall(r'(?:ASCO|核药|ADC|GLP-1|细胞治疗|激光医疗|百胜|AI多肽|RNA|止痛药|透镜)[^<]{10,200}', html)
for t in texts[:15]:
    print(f"  {t[:150]}")
