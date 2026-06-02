import sys, io, json, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(headless=True)
page = browser.new_page()
page.goto("https://www.vcbeat.top/", timeout=60000, wait_until="networkidle")
time.sleep(3)

# Scroll to load lazy content
for i in range(3):
    page.evaluate("window.scrollBy(0, 800)")
    time.sleep(1.5)

# Get all links
links = page.evaluate("""
    () => {
        const results = [];
        const allLinks = document.querySelectorAll('a[href]');
        allLinks.forEach(a => {
            const href = a.href;
            const text = a.textContent.trim();
            if (text.length > 15 && href && !href.includes('javascript') && !href.includes('beian')) {
                results.push({text: text.substring(0, 120), href: href});
            }
        });
        return results;
    }
""")

page.close()
browser.close()
p.stop()

# Filter to likely article links
article_links = [l for l in links if '/article/' in l['href'] or '/news/' in l['href'] or '/detail/' in l['href'] or '/p/' in l['href']]

if not article_links:
    # Just show all meaningful links
    article_links = [l for l in links if 'vcbeat.top' in l['href'] or 'vbdata.cn' in l['href']]

print(f"Total links found: {len(links)}")
print(f"Article-like links: {len(article_links)}")
print()
for link in article_links[:30]:
    print(f"  {link['text'][:100]}")
    print(f"  → {link['href']}")
    print()

# If still no article links, dump all
if len(article_links) < 5:
    print("=== All links ===")
    for link in links[:30]:
        print(f"  {link['text'][:80]} → {link['href']}")
