import json

with open(r'D:\Qclaw\AiMedbrief\articles\data.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for a in articles:
    pts_html = '\n'.join('<li>' + p + '</li>' for p in a['points'])

    html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>''' + a['title_en'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') + r'''</title>
<meta name="description" content="''' + a['summary_en'][:160] + r'''">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',sans-serif;background:#fafafa;color:#1d1d1f;line-height:1.6;-webkit-font-smoothing:antialiased}
.top-bar{background:rgba(255,255,255,.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid #f0f0f5;position:sticky;top:0;z-index:100;padding:10px 24px}
.top-bar-inner{max-width:860px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}
.top-bar-brand{font-weight:600;color:#1d1d1f;font-size:14px}
.top-bar a{color:#0071e3;text-decoration:none;font-weight:500;font-size:13px}
.container{max-width:860px;margin:0 auto;padding:48px 24px 80px}
.back-link{display:inline-flex;align-items:center;gap:6px;color:#0071e3;text-decoration:none;font-size:13px;margin-bottom:28px}
.back-link:hover{text-decoration:underline}
.category{display:inline-block;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;padding:3px 10px;border-radius:6px;margin-bottom:14px;background:rgba(88,86,214,.08);color:#5856d6}
.date{font-size:13px;color:#86868b;margin-bottom:8px}
h1{font-size:32px;font-weight:700;letter-spacing:-.5px;line-height:1.2;margin-bottom:24px}
h2{font-size:20px;font-weight:600;margin-top:36px;margin-bottom:12px}
.lede{font-size:17px;color:#424245;line-height:1.7;margin-bottom:36px;padding:24px 28px;background:#fff;border-radius:14px;border:1px solid #e5e5ea}
.key-points{list-style:none;margin-top:30px}
.key-points li{font-size:15px;color:#1d1d1f;padding:10px 0 10px 22px;position:relative;line-height:1.55;border-bottom:1px solid #f0f0f5}
.key-points li::before{content:'';width:7px;height:7px;background:#0071e3;border-radius:50%;position:absolute;left:0;top:16px}
.meta-section{font-size:12px;color:#86868b;margin-top:40px;padding-top:20px;border-top:1px solid #e5e5ea}
.meta-section a{color:#0071e3}
@media(max-width:640px){.container{padding:24px 16px}h1{font-size:24px}.lede{font-size:15px;padding:18px}}
</style>
<meta name="ab-page" content="2026-06-02-''' + a['id'] + r'''.html">
<meta name="ab-article-id" content="''' + a['id'] + r'''">
</head>
<body>
<nav class="top-bar"><div class="top-bar-inner">
<a href="../index.html" class="top-bar-brand">AiMedbrief</a>
<a href="../index.html">&#8592; Back to Home</a>
</div></nav>
<div class="container">
<a href="../index.html" class="back-link">&#8592; Back</a>
<p class="category">''' + a['cat_en'] + r'''</p>
<p class="date">June 2, 2026</p>
<h1>''' + a['title_en'] + r'''</h1>
<div class="lede">''' + a['summary_en'] + r'''</div>
<h2>Key Takeaways</h2>
<ul class="key-points">''' + pts_html + r'''</ul>
<div class="meta-section">
  Source: ''' + a['source'] + r'''
  &nbsp;&middot;&nbsp; <a href="''' + a['url'] + r'''" target="_blank" rel="noopener">Original source</a>
  &nbsp;&middot;&nbsp; Published June 2, 2026 &middot; Beijing Time (GMT+8)
</div>
</div>
<script src="../analytics.js"></script>
</body>
</html>'''

    path = r'D:\Qclaw\AiMedbrief\articles\2026-06-02-' + a['id'] + '.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Built: {path} ({len(html):,} bytes)')

print('\nDone building all article pages.')