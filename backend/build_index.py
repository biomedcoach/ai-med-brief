import json

with open(r'D:\Qclaw\AiMedbrief\articles\data.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

cat_map = {'创新药': 'Innovative Drug', '创新医疗器械': 'Medical Device', 'AI+医药': 'AI + Pharma', '居家检测': 'Home Testing'}

cards_html = ''
sidebar_trending = ''

for i, a in enumerate(articles):
    cat_en = cat_map.get(a['category'], a['category'])
    tag_cls = 'tag-drug' if a['category'] == '创新药' else 'tag-ai'

    cards_html += (
        '<article class="card" data-id="' + a['id'] + '">\n'
        '  <div class="card-img"><img src="images/2026-06-02-' + a['id'] + '.jpg" alt="' + a['title_en'] + '" loading="lazy"></div>\n'
        '  <div class="card-body">\n'
        '    <div class="card-top">\n'
        '      <span class="card-tag ' + tag_cls + '">' + cat_en + '</span>\n'
        '      <span class="card-date">June 2, Beijing Time</span>\n'
        '    </div>\n'
        '    <h3 class="card-title"><a href="articles/2026-06-02-' + a['id'] + '.html">' + a['title_en'] + '</a></h3>\n'
        '    <p class="card-summary">' + a['summary_en'] + '</p>\n'
        '    <div class="card-meta-row">\n'
        '      <span class="meta-source">Source: ' + a['source'] + '</span>\n'
        '    </div>\n'
        '  </div>\n'
        '</article>\n'
    )

    sidebar_trending += (
        '<div class="sb-item" onclick="location.href=\'articles/2026-06-02-' + a['id'] + '.html\'">\n'
        '  <div class="sb-item-title">' + a['title_en'][:72] + '...</div>\n'
        '  <div class="sb-item-tag">' + cat_en + '</div>\n'
        '</div>\n'
    )

counts = {}
for a in articles:
    c = cat_map.get(a['category'], a['category'])
    counts[c] = counts.get(c, 0) + 1
count_str = ' \u00b7 '.join(str(v) + ' ' + k for k, v in counts.items())

html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="ab-page" content="index.html">
<title>AiMedbrief &mdash; China Biopharma Intelligence Daily</title>
<link rel="icon" type="image/png" href="images/logo.png">
<meta name="description" content="Daily intelligence on innovative drugs, medical devices, and AI-enabled medicine from China &mdash; curated and translated for a global audience.">
<style>''')

css = r'''
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#fafafa;--bg-card:#fff;--text:#1d1d1f;--text-secondary:#6e6e73;--text-tertiary:#86868b;--border:#e5e5ea;--border-light:#f0f0f5;--accent:#0071e3;--accent-bg:#f5f9ff;--sidebar-w:340px;--max-w:1280px;--radius:16px;--drug-color:#5856d6;--ai-color:#ff6b35}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text','Helvetica Neue','Segoe UI',sans-serif;-webkit-font-smoothing:antialiased;line-height:1.47059}

/* Top Bar - 1.5x larger */
.top-bar{background:rgba(255,255,255,0.85);backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid var(--border-light);position:sticky;top:0;z-index:100}
.top-bar-inner{max-width:var(--max-w);margin:0 auto;padding:21px 42px;display:flex;justify-content:space-between;align-items:center}
.top-bar-brand{display:flex;align-items:center;gap:18px}
.top-bar-brand img{height:36px;width:auto;display:block}
.top-bar-brand span{font-size:22px;color:var(--text-secondary);font-weight:400;padding-left:18px;border-left:2px solid var(--border)}
.top-bar-links{display:flex;gap:30px;font-size:21px}
.top-bar-links a{color:var(--text-secondary);text-decoration:none;transition:color .2s;font-weight:500}
.top-bar-links a:hover{color:var(--accent)}

/* Hero - flex row with ads on right */
.hero{max-width:var(--max-w);margin:0 auto;padding:48px 24px 0;display:flex;gap:48px;align-items:flex-start}
.hero-text{flex:1;min-width:0}
.hero-ads{width:340px;flex-shrink:0;display:flex;flex-direction:column;gap:16px}
.hero h1{font-size:38px;font-weight:700;letter-spacing:-0.8px;line-height:1.1;margin-bottom:10px}
.hero p{font-size:17px;color:var(--text-secondary);max-width:650px;line-height:1.55}
.hero .stats{display:flex;gap:36px;margin-top:22px;font-size:14px;color:var(--text-tertiary)}
.hero .stats strong{font-size:17px;color:var(--text);font-weight:600}
.tag-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:28px}
.tag-btn{padding:8px 20px;border-radius:22px;font-size:13px;font-weight:500;cursor:pointer;background:transparent;border:1px solid var(--border);color:var(--text-secondary);font-family:inherit;transition:all .2s}
.tag-btn:hover,.tag-btn.active{background:var(--text);border-color:var(--text);color:#fff}

/* Layout */
.main-layout{max-width:var(--max-w);margin:0 auto;padding:0 24px 80px;display:flex;gap:40px;align-items:flex-start}
.feed{flex:1;min-width:0;margin-top:-190px}
.feed-header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:20px;padding-bottom:14px;border-bottom:1px solid var(--border-light)}
.feed-header h2{font-size:15px;font-weight:600}
.feed-header span{font-size:12px;color:var(--text-tertiary)}

/* Card with image on left */
.card{background:var(--bg-card);border-radius:var(--radius);margin-bottom:18px;transition:box-shadow .3s,transform .2s;border:1px solid transparent;display:flex;overflow:hidden;min-height:220px}
.card:hover{box-shadow:0 10px 48px rgba(0,0,0,.07);transform:translateY(-2px);border-color:var(--border-light)}
.card-img{width:280px;flex-shrink:0;overflow:hidden;border-radius:12px 0 0 12px}.card-img img{width:100%;height:100%;object-fit:cover;display:block}
.img-placeholder{font-size:13px;font-weight:500;color:var(--text-tertiary);letter-spacing:1px;text-transform:uppercase}
.card-body{padding:28px 32px 24px;flex:1;min-width:0;display:flex;flex-direction:column}
.card-top{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.card-tag{font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.7px;padding:4px 11px;border-radius:6px}
.tag-drug{color:var(--drug-color);background:rgba(88,86,214,.09)}
.tag-ai{color:var(--ai-color);background:rgba(255,107,53,.09)}
.card-date{font-size:12px;color:var(--text-tertiary)}
.card-title{font-size:19px;font-weight:600;letter-spacing:-.25px;line-height:1.25;margin-bottom:10px}
.card-title a{color:var(--text);text-decoration:none;transition:color .2s}
.card-title a:hover{color:var(--accent)}
.card-summary{font-size:14px;color:var(--text-secondary);line-height:1.6;flex:1;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.card-meta-row{display:flex;justify-content:space-between;align-items:center;margin-top:14px;padding-top:12px;border-top:1px solid var(--border-light)}
.meta-source{font-size:11.5px;color:var(--text-tertiary)}
.kp-toggle{background:none;border:none;color:var(--accent);font-size:12px;font-weight:600;cursor:pointer;font-family:inherit;padding:4px 0;transition:opacity .2s}
.kp-toggle:hover{opacity:.7}


/* Hero Ad Slots */
.hero-ads .ad-slot{margin-bottom:0}
.hero-ads .ad-slot-inner{height:180px}
.ad-slot{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden}
.ad-slot-label{font-size:10px;font-weight:700;color:var(--text-tertiary);text-transform:uppercase;letter-spacing:1.5px;padding:10px 18px 0}
.ad-slot-inner{display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--text-tertiary);border:1px dashed var(--border);border-radius:0 0 var(--radius) var(--radius);margin:10px 14px}
.ad-slot-inner span{font-weight:500;color:var(--text-secondary);margin-bottom:4px;font-size:14px}
.ad-slot-inner small{font-size:12px;color:var(--accent)}

/* Sidebar */
.sidebar{width:var(--sidebar-w);flex-shrink:0;position:sticky;top:76px;padding-top:20px}
.sb-section{margin-bottom:28px}
.sb-heading{font-size:11px;font-weight:700;color:var(--text-tertiary);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:14px}
.sb-item{padding:11px 0;border-bottom:1px solid var(--border-light);cursor:pointer;transition:color .2s}
.sb-item:hover .sb-item-title{color:var(--accent)}
.sb-item-title{font-size:13.5px;font-weight:500;color:var(--text);line-height:1.4}
.sb-item-tag{font-size:10px;font-weight:600;margin-top:3px;color:var(--drug-color)}
.sb-item:last-child .sb-item-tag{color:var(--ai-color)}
.source-list{font-size:12px;color:var(--text-tertiary);line-height:2}

/* Footer */
.site-footer{border-top:1px solid var(--border-light);padding:32px 24px;font-size:12px;color:var(--text-tertiary)}
.footer-inner{max-width:var(--max-w);margin:0 auto;display:flex;justify-content:space-between;align-items:center}
.footer-links{display:flex;gap:24px}
.footer-links a{color:var(--text-tertiary);text-decoration:none}
.footer-links a:hover{color:var(--text)}

@media(max-width:1024px){.hero{flex-direction:column;gap:24px}.hero-ads{width:100%;flex-direction:row;gap:16px}.hero-ads .ad-slot{flex:1}.hero-ads .ad-slot-inner{height:120px}.main-layout{flex-direction:column}.sidebar{width:100%;position:static}.card{flex-direction:row}.card-img{width:200px}}
@media(max-width:640px){.hero{padding:32px 16px 24px}.hero h1{font-size:26px}.hero-ads{flex-direction:column}.hero-ads .ad-slot-inner{height:100px}.main-layout{padding:0 16px 60px}.card{flex-direction:column;min-height:auto}.card-img{width:100%;height:160px}.top-bar-inner{padding:12px 16px}.top-bar-brand h1{font-size:18px}.top-bar-brand span{display:none}.top-bar-links{font-size:13px;gap:14px}}
'''
html_parts.append(css)
html_parts.append('</style></head><body>\n')

# Top bar
html_parts.append('''<nav class="top-bar"><div class="top-bar-inner">
<div class="top-bar-brand"><img src="images/logo.png" alt="AiMedbrief"><span>China Biopharma Intelligence Daily</span></div>
<div class="top-bar-links"><a href="#">Today</a><a href="#">Archive</a><a href="#">Topics</a><a href="#">About</a></div>
</div></nav>\n''')

# Hero with ads on the right
hero_stats = '<strong>' + str(len(articles)) + '</strong> articles today<div><strong>June 2</strong>, 2026 &middot; Beijing Time (GMT+8)</div>'
html_parts.append(
    '<header class="hero">\n'
    '<div class="hero-text">\n'
    '<h1>China Biopharma Intelligence</h1>\n'
    '<p>Innovative drugs, medical devices, and AI-enabled medicine from China &mdash; curated and translated daily for the global biopharma community.</p>\n'
    '<div class="stats">' + hero_stats + '</div>\n'
    '<div class="tag-row">\n'
    '  <button class="tag-btn active" onclick="filterAll()">All</button>\n'
    '  <button class="tag-btn" onclick="filterCat(\'Innovative Drug\')">Innovative Drugs</button>\n'
    '  <button class="tag-btn" onclick="filterCat(\'AI + Pharma\')">AI + Pharma</button>\n'
    '</div>\n'
    '</div>\n'
    '<div class="hero-ads">\n'
    '<div class="ad-slot"><div class="ad-slot-label">Advertisement</div>\n'
    '<div class="ad-slot-inner"><span>Your brand here</span></div></div>\n'
    '<div class="ad-slot"><div class="ad-slot-label">Advertisement</div>\n'
    '<div class="ad-slot-inner"><span>Your brand here</span></div></div>\n'
    '</div>\n'
    '</header>\n'
)

# Main layout (no ad slots in sidebar anymore)
feed_header = '<h2>Today\'s Selection</h2><span>June 2, 2026 &middot; Beijing Time (GMT+8) &mdash; ' + str(len(articles)) + ' articles</span>'
html_parts.append(
    '<div class="main-layout">\n<main class="feed">\n'
    '<div class="feed-header">' + feed_header + '</div>\n'
)
html_parts.append(cards_html)
html_parts.append('</main>\n\n<aside class="sidebar">\n')

# Today's coverage
html_parts.append('<div class="sb-section"><div class="sb-heading">Today\'s Coverage</div>\n')
html_parts.append(sidebar_trending)
html_parts.append('</div>\n')

html_parts.append('''</aside></div>\n''')

# Footer
html_parts.append('''<footer class="site-footer"><div class="footer-inner">
<span>AiMedbrief &copy; 2026 &mdash; Curated, translated, daily.</span>
<div class="footer-links"><a href="#">About</a><a href="#">Archive</a><a href="https://github.com/biomedcoach/ai-med-brief">GitHub</a><a href="#">Privacy</a></div>
</div></footer>

<script>
function filterAll(){document.querySelectorAll('.tag-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.card').forEach(c=>c.style.display='');event.target.classList.add('active')}
function filterCat(cat){document.querySelectorAll('.tag-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.card').forEach(c=>{var t=c.querySelector('.card-tag').textContent.trim();c.style.display=t===cat?'':'none'});event.target.classList.add('active')}

</script>
<script src="analytics.js"></script>
</body></html>''')

full_html = ''.join(html_parts)

with open(r'D:\Qclaw\AiMedbrief\index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'index.html rebuilt ({len(full_html):,} bytes)')