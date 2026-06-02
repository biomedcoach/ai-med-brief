# 🏥 China AI Health

**Daily intelligence on AI-enabled medical products from China — curated and translated for a global audience.**

## What is this?

A static website that aggregates, translates, and publishes the latest news about AI-powered medical products, drugs, devices, and diagnostics from China.

**Live site:** [cnai-health.github.io](https://cnai-health.github.io)

## How it works

```
Chinese news sources → Crawler (Playwright) → AI Translation → Quality Scoring → Static HTML → GitHub Pages
```

### Pipeline

1. **Crawl** (`crawl.py`) — Fetches articles from 36kr, Leiphone, and CDE
2. **Translate** (`translate.py`) — AI-powered English translation via SiliconFlow
3. **Select** (`select.py`) — Auto-selects top articles by quality score
4. **Publish** (`publish.py`) — Generates static HTML site
5. **Deploy** — GitHub Actions → GitHub Pages

### Schedule

| Time (CST) | Action |
|-------------|--------|
| 12:00 | Crawl + Translate |
| 17:00 | Crawl + Translate |
| 20:00 | Crawl + Translate |
| 01:00 | Select + Publish |

## Tech Stack

- **Crawler:** Python + Playwright (headless Chromium)
- **Translation:** SiliconFlow API (DeepSeek-R1 model)
- **Frontend:** Static HTML + CSS (vanilla, no frameworks)
- **Hosting:** GitHub Pages
- **Automation:** GitHub Actions

## Content Focus

- 🏥 AI diagnosis and medical imaging
- 💊 AI drug discovery
- 🤖 Medical robotics
- 🧬 AI genomics
- 📋 NMPA/FDA regulatory updates
- 💰 Funding and M&A in health AI
- 🎪 Major industry exhibitions

## License

Content is curated from public sources for educational and informational purposes.
