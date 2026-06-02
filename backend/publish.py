#!/usr/bin/env python3
"""
China AI Health — Publisher
==============================
Reads selected_YYYY-MM-DD.json, generates the static index.html
using Jinja2 templates, writes individual article MD files,
and optionally does git commit + push.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

# Fix Windows console encoding for Chinese/emoji output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as cfg

CST = timezone(timedelta(hours=8))
TODAY = datetime.now(CST).strftime("%Y-%m-%d")
DATE_STR = datetime.now(CST).strftime("%B %d, %Y")


# ════════════════════════════════════════════════════
#  Tag CSS class mapping
# ════════════════════════════════════════════════════

TAG_CLASS_MAP = {
    "AI-diagnosis": "tag-diagnosis",
    "AI-drug-discovery": "tag-drug",
    "AI-medical-device": "tag-device",
    "Regulation": "tag-regulation",
    "Funding": "tag-funding",
    "Exhibition": "tag-exhibition",
    "AI-genomics": "tag-drug",
    "AI-robotics": "tag-device",
    "Digital-health": "tag-diagnosis",
    "Policy": "tag-regulation",
}

TAG_LABEL_MAP = {
    "AI-diagnosis": "AI Diagnosis",
    "AI-drug-discovery": "AI Drug Discovery",
    "AI-medical-device": "AI Medical Device",
    "Regulation": "Regulation",
    "Funding": "Funding",
    "Exhibition": "Exhibition",
    "AI-genomics": "AI Genomics",
    "AI-robotics": "AI Robotics",
    "Digital-health": "Digital Health",
    "Policy": "Policy",
}

# HTML template for the index page
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>China AI Health — {date_str}</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --bg: #fafafa; --bg-card: #ffffff; --text: #1d1d1f;
  --text-secondary: #6e6e73; --text-tertiary: #86868b;
  --border: #e5e5ea; --border-light: #f0f0f5; --accent: #0071e3;
  --accent-bg: #f5f9ff; --sidebar-width: 320px; --max-width: 1280px;
  --radius: 16px;
}}

body {{
  background: var(--bg); color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', 'Segoe UI', sans-serif;
  -webkit-font-smoothing: antialiased; line-height: 1.47059;
}}

.top-bar {{
  background: rgba(255,255,255,0.8); backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--border-light); font-size: 12px;
  color: var(--text-tertiary); position: sticky; top: 0; z-index: 100;
}}
.top-bar-inner {{
  max-width: var(--max-width); margin: 0 auto; padding: 8px 24px;
  display: flex; justify-content: space-between; align-items: center;
}}
.top-bar-links {{ display: flex; gap: 24px; }}
.top-bar-links a {{ color: var(--text-tertiary); text-decoration: none; font-size: 12px; transition: color 0.2s; }}
.top-bar-links a:hover {{ color: var(--accent); }}

.site-header {{ max-width: var(--max-width); margin: 0 auto; padding: 48px 24px 32px; }}
.header-top {{ display: flex; align-items: flex-end; justify-content: space-between; }}
.brand h1 {{ font-size: 32px; font-weight: 700; letter-spacing: -0.5px; color: var(--text); }}
.brand p {{ font-size: 14px; color: var(--text-tertiary); margin-top: 4px; }}
.btn {{
  padding: 9px 18px; border-radius: 20px; font-size: 13px; font-weight: 500;
  cursor: pointer; transition: all 0.2s; text-decoration: none;
  display: inline-flex; align-items: center; gap: 6px;
}}
.btn-outline {{ background: transparent; color: var(--accent); border: 1px solid var(--accent); }}
.btn-outline:hover {{ background: var(--accent-bg); }}

.tag-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 28px; }}
.tag-btn {{
  padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 500;
  cursor: pointer; background: transparent; border: none; color: var(--text-secondary);
  transition: all 0.2s;
}}
.tag-btn.active {{ background: var(--text); color: #fff; }}

.main-layout {{
  max-width: var(--max-width); margin: 0 auto; padding: 0 24px 80px;
  display: flex; gap: 40px; align-items: flex-start;
}}
.article-feed {{ flex: 1; min-width: 0; }}
.feed-header {{
  display: flex; justify-content: space-between; align-items: baseline;
  margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light);
}}
.feed-header h2 {{ font-size: 14px; font-weight: 600; color: var(--text); }}
.feed-meta {{ font-size: 12px; color: var(--text-tertiary); }}

.article-card {{
  background: var(--bg-card); border-radius: var(--radius); padding: 28px 32px;
  margin-bottom: 16px; cursor: pointer; transition: box-shadow 0.25s, transform 0.25s;
  border: 1px solid transparent;
}}
.article-card:hover {{
  box-shadow: 0 8px 40px rgba(0,0,0,0.06); transform: translateY(-1px);
  border-color: var(--border-light);
}}
.card-top {{ display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }}
.card-tag {{
  font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
  padding: 3px 10px; border-radius: 6px;
}}
.tag-diagnosis {{ color: #0071e3; background: rgba(0,113,227,0.08); }}
.tag-drug {{ color: #5856d6; background: rgba(88,86,214,0.08); }}
.tag-device {{ color: #ff6b35; background: rgba(255,107,53,0.08); }}
.tag-regulation {{ color: #34c759; background: rgba(52,199,89,0.08); }}
.tag-funding {{ color: #af52de; background: rgba(175,82,222,0.08); }}
.tag-exhibition {{ color: #ff9500; background: rgba(255,149,0,0.08); }}
.card-date {{ font-size: 12px; color: var(--text-tertiary); }}
.card-title {{
  font-size: 21px; font-weight: 600; letter-spacing: -0.3px; line-height: 1.2;
  margin-bottom: 10px; color: var(--text); transition: color 0.2s;
}}
.article-card:hover .card-title {{ color: var(--accent); }}
.card-summary {{
  font-size: 15px; color: var(--text-secondary); line-height: 1.55; margin-bottom: 16px;
}}
.card-points {{ display: flex; flex-direction: column; gap: 6px; }}
.card-point {{ font-size: 13px; color: var(--text-secondary); padding-left: 16px; position: relative; }}
.card-point::before {{
  content: ''; width: 5px; height: 5px; background: var(--accent);
  border-radius: 50%; position: absolute; left: 0; top: 8px;
}}

.sidebar {{ width: var(--sidebar-width); flex-shrink: 0; position: sticky; top: 60px; }}
.ad-slot {{
  background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 28px 24px; text-align: center; margin-bottom: 28px;
}}
.ad-slot-label {{
  font-size: 10px; font-weight: 600; color: var(--text-tertiary);
  text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 14px;
}}
.ad-slot-placeholder {{
  height: 200px; display: flex; flex-direction: column; align-items: center;
  justify-content: center; color: var(--text-tertiary); border: 1px dashed var(--border);
  border-radius: 12px; font-size: 14px; line-height: 1.6;
}}
.ad-slot-placeholder span {{ font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }}
.ad-slot-placeholder small {{ font-size: 12px; margin-top: 8px; color: var(--accent); }}

.sb-section {{ margin-bottom: 28px; }}
.sb-heading {{
  font-size: 11px; font-weight: 700; color: var(--text-tertiary);
  text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 16px;
}}
.sb-item {{ padding: 10px 0; border-bottom: 1px solid var(--border-light); cursor: pointer; }}
.sb-item:hover {{ color: var(--accent); }}
.sb-item-title {{ font-size: 14px; font-weight: 500; color: var(--text); line-height: 1.35; }}
.sb-item:hover .sb-item-title {{ color: var(--accent); }}
.sb-item-tag {{ font-size: 10px; color: var(--accent); font-weight: 600; margin-top: 3px; }}

.nl-box {{
  background: var(--accent-bg); border-radius: var(--radius); padding: 24px; margin-bottom: 28px;
}}
.nl-box h3 {{ font-size: 15px; font-weight: 600; margin-bottom: 4px; }}
.nl-box p {{ font-size: 13px; color: var(--text-secondary); margin-bottom: 14px; }}
.nl-input {{
  width: 100%; padding: 10px 14px; border: 1px solid var(--border); border-radius: 10px;
  font-size: 13px; outline: none; font-family: inherit; background: var(--bg-card);
  margin-bottom: 8px; transition: border-color 0.2s;
}}
.nl-input:focus {{ border-color: var(--accent); }}
.nl-btn {{
  width: 100%; padding: 10px; background: var(--accent); color: #fff;
  border: none; border-radius: 10px; font-size: 13px; font-weight: 500;
  cursor: pointer; font-family: inherit; transition: background 0.2s;
}}
.nl-btn:hover {{ background: #0077ed; }}

.pagination {{
  display: flex; align-items: center; justify-content: center; gap: 6px; margin-top: 32px;
}}
.page-btn {{
  width: 36px; height: 36px; border-radius: 8px; border: 1px solid transparent;
  background: transparent; color: var(--text-secondary); font-size: 13px;
  font-weight: 500; cursor: pointer; transition: all 0.2s;
  display: flex; align-items: center; justify-content: center; font-family: inherit;
}}
.page-btn.active {{ background: var(--text); color: #fff; }}

.site-footer {{ border-top: 1px solid var(--border-light); padding: 40px 24px; }}
.footer-inner {{
  max-width: var(--max-width); margin: 0 auto; display: flex;
  justify-content: space-between; align-items: center; font-size: 12px; color: var(--text-tertiary);
}}
.footer-links {{ display: flex; gap: 24px; }}
.footer-links a {{ color: var(--text-tertiary); text-decoration: none; transition: color 0.2s; }}
.footer-links a:hover {{ color: var(--text); }}

@media (max-width: 1024px) {{ .main-layout {{ flex-direction: column; }} .sidebar {{ width: 100%; position: static; }} }}
@media (max-width: 640px) {{
  .site-header {{ padding: 32px 16px 24px; }} .main-layout {{ padding: 0 16px 60px; gap: 32px; }}
  .article-card {{ padding: 20px; }} .card-title {{ font-size: 18px; }}
}}
</style>
</head>
<body>

<nav class="top-bar">
  <div class="top-bar-inner">
    <span style="font-weight:600;color:var(--text);">China AI Health</span>
    <div class="top-bar-links">
      <a href="#">Today</a> <a href="archive/">Archive</a> <a href="#">Topics</a> <a href="#">About</a>
    </div>
  </div>
</nav>

<header class="site-header">
  <div class="header-top">
    <div class="brand">
      <h1>China AI Health</h1>
      <p>Daily intelligence on AI-enabled medical products from China &mdash; curated and translated for a global audience.</p>
    </div>
    <a href="rss.xml" class="btn btn-outline">RSS</a>
  </div>
  <div class="tag-row">
    <button class="tag-btn active">All</button>
    <button class="tag-btn">AI Diagnosis</button>
    <button class="tag-btn">AI Drug Discovery</button>
    <button class="tag-btn">AI Medical Devices</button>
    <button class="tag-btn">Regulation</button>
    <button class="tag-btn">Funding</button>
    <button class="tag-btn">Exhibitions</button>
  </div>
</header>

<div class="main-layout">

  <main class="article-feed">
    <div class="feed-header">
      <h2>{date_str} &mdash; Today's Selection</h2>
      <span class="feed-meta">{count} articles</span>
    </div>

{articles_html}

  </main>

  <aside class="sidebar">
    <div class="ad-slot">
      <div class="ad-slot-label">Advertisement</div>
      <div class="ad-slot-placeholder">
        <span>Your brand here</span>
        Reach 5,000+ monthly readers tracking China's AI healthcare market.
        <small>advertise@cnai-health.com</small>
      </div>
    </div>

    <div class="sb-section">
      <div class="sb-heading">Trending</div>
      {trending_html}
    </div>

    <div class="nl-box">
      <h3>Weekly Digest</h3>
      <p>Top stories from China's AI health frontier. Every Monday. No spam.</p>
      <input type="email" class="nl-input" placeholder="you@email.com">
      <button class="nl-btn">Subscribe</button>
    </div>

    <div class="sb-section">
      <div class="sb-heading">Sources Monitored</div>
      <div style="font-size:12px;color:var(--text-tertiary);line-height:1.8;">
        vcbeat.top · bioon.com · leiphone.com<br>
        36kr.com · huxiu.com · yigoonet.com<br>
        medicaldevice.cn · cn-healthcare.com<br>
        pharmcube.com · NMPA.gov.cn · 15+ more
      </div>
    </div>
  </aside>

</div>

<footer class="site-footer">
  <div class="footer-inner">
    <div>China AI Health &copy; 2026 — Curated, translated, daily.</div>
    <div class="footer-links">
      <a href="#">About</a> <a href="#">Archive</a> <a href="#">RSS</a> <a href="#">GitHub</a> <a href="#">Privacy</a>
    </div>
  </div>
</footer>

</body>
</html>"""


# ════════════════════════════════════════════════════
#  Article card HTML generation
# ════════════════════════════════════════════════════

def article_card_html(art, idx=None):
    """Generate HTML for a single article card."""
    tags = art.get("tags", ["AI-diagnosis"])
    main_tag = tags[0] if tags else "AI-diagnosis"

    tag_class = TAG_CLASS_MAP.get(main_tag, "tag-diagnosis")
    tag_label = TAG_LABEL_MAP.get(main_tag, "AI Diagnosis")
    date = art.get("published", "Today")
    # Shorten date if ISO format
    if "T" in date:
        try:
            dt = datetime.fromisoformat(date)
            date = dt.strftime("%B %d")
        except Exception:
            date = "Today"

    title = art.get("en_title", art.get("title", ""))
    summary = art.get("en_summary", "")

    # Sanitize HTML content in title/summary
    title = title.replace("<", "&lt;").replace(">", "&gt;")
    summary = summary.replace("<", "&lt;").replace(">", "&gt;")

    kp_html = ""
    kps = art.get("en_key_points", []) or []
    if kps:
        points = "".join(
            f'<div class="card-point">{p.replace("<", "&lt;").replace(">", "&gt;")}</div>'
            for p in kps[:3]
        )
        kp_html = f'<div class="card-points">{points}</div>'

    url = art.get("url", "#")
    article_id = idx or ""

    return f"""
    <article class="article-card" data-id="{article_id}">
      <div class="card-top">
        <span class="card-tag {tag_class}">{tag_label}</span>
        <span class="card-date">{date}</span>
      </div>
      <h3 class="card-title"><a href="{url}" style="color:inherit;text-decoration:none;">{title}</a></h3>
      <p class="card-summary">{summary}</p>
      {kp_html}
    </article>"""


def trending_html(articles):
    """Generate trending sidebar items from top articles."""
    items = []
    for i, art in enumerate(articles[:5]):
        title = (art.get("en_title") or art.get("title", ""))[:80]
        title = title.replace("<", "&lt;").replace(">", "&gt;")
        tags = art.get("tags", [])
        tag = TAG_LABEL_MAP.get(tags[0], "") if tags else ""
        tag_class = TAG_CLASS_MAP.get(tags[0], "tag-diagnosis") if tags else ""
        items.append(f"""
      <div class="sb-item">
        <div class="sb-item-title">{title}</div>
        <div class="sb-item-tag" style="color:#0071e3">{tag}</div>
      </div>""")

    return "".join(items)


# ════════════════════════════════════════════════════
#  Main
# ════════════════════════════════════════════════════

def publish(dry_run=False):
    selected_file = os.path.join(cfg.SELECTED_DIR, f"selected_{TODAY}.json")

    if not os.path.exists(selected_file):
        print(f"ERROR: No selected file for {TODAY}")
        print(f"Expected: {selected_file}")
        print("Run curation_ui.py first to select articles.")
        sys.exit(1)

    with open(selected_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    count = len(articles)
    print(f"Loaded {count} selected articles for {TODAY}")

    # Generate article cards
    cards = [article_card_html(art, i + 1) for i, art in enumerate(articles)]
    articles_html = "".join(cards)

    # Generate trending
    trending = trending_html(articles)

    # Fill template
    html = HTML_TEMPLATE.format(
        date_str=DATE_STR,
        count=count,
        articles_html=articles_html,
        trending_html=trending,
    )

    # Write index.html
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(root, "index.html")

    if dry_run:
        print(f"\nDRY RUN — would write to: {out_path}")
        print(f"Generated {len(html)} bytes of HTML")
        preview = html[:800]
        print("\n--- PREVIEW (first 800 chars) ---")
        print(preview)
        print("--- END PREVIEW ---")
        return

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Written {out_path} ({len(html)} bytes)")

    # Generate individual article MD files
    articles_dir = os.path.join(root, "articles")
    os.makedirs(articles_dir, exist_ok=True)

    for i, art in enumerate(articles, 1):
        art_file = os.path.join(articles_dir, f"{TODAY}-{i:02d}.md")
        en_title = art.get("en_title", art.get("title", ""))
        en_summary = art.get("en_summary", "")
        kps = art.get("en_key_points", [])

        kp_md = "\n".join(f"- {p}" for p in kps) if kps else ""
        content = f"""# {en_title}

> Published {DATE_STR} | Source: {art.get('source', 'Unknown')}

{en_summary}

## Key Points

{kp_md}

---

*Source: [{art.get('title', 'Original Article')}]({art.get('url', '#')})*
"""
        with open(art_file, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"✓ Written {count} article MD files to {articles_dir}/")


def git_push():
    """Git add, commit, push."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        subprocess.run(["git", "add", "index.html", "articles/"], cwd=root, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Daily update: {TODAY}"],
            cwd=root,
            check=False,  # may fail if no changes
        )
        subprocess.run(["git", "push"], cwd=root, check=True)
        print(f"✓ Git push complete for {TODAY}")
        return True
    except Exception as e:
        print(f"✗ Git push failed: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="China AI Health Publisher")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no file write")
    parser.add_argument("--date", type=str, help="Publish for a specific date (YYYY-MM-DD)")
    parser.add_argument("--push", action="store_true", help="Git push after publishing")
    args = parser.parse_args()

    if args.date:
        TODAY = args.date
        try:
            dt = datetime.fromisoformat(args.date)
            DATE_STR = dt.strftime("%B %d, %Y")
        except Exception:
            pass

    publish(dry_run=args.dry_run)

    if args.push and not args.dry_run:
        git_push()