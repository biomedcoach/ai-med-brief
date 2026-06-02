# China AI Health — Backend Configuration
import os

# ── Paths ───────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")
CANDIDATES_DIR = os.path.join(DATA_DIR, "candidates")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
SELECTED_DIR = os.path.join(DATA_DIR, "selected")
DB_PATH = os.path.join(DATA_DIR, "history.db")
SOURCES_FILE = os.path.join(ROOT, "sources.yaml")
TEMPLATE_FILE = os.path.join(os.path.dirname(ROOT), "index.html")

# ── API ─────────────────────────────────────────────
SILICONFLOW_API_KEY = os.environ.get("SILICONFLOW_API_KEY", "sk-uejmkcsbiwamfjcykymcjwlobubbxyvpvwzwbvlndcpfmtph")
SILICONFLOW_MODEL = "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"
SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"

# ── Crawling ────────────────────────────────────────
REQUEST_TIMEOUT = 15
REQUEST_DELAY = 1.5  # seconds between requests (be polite)
USER_AGENT = "ChinaAIHealth/1.0 (bot; medical-news-indexing; contact@cnai-health.com)"
MAX_ARTICLES_PER_SOURCE = 8

# ── Quality Scoring Weights ─────────────────────────
SCORE_WEIGHTS = {
    "freshness": 0.30,
    "authority": 0.25,
    "relevance": 0.20,
    "density": 0.15,
    "rarity": 0.10,
}

# ── Filters ─────────────────────────────────────────
TITLE_BLACKLIST = ["招聘", "招人", "求职", "广告", "推广", "活动报名", "培训班", "实习生"]
MIN_CONTENT_LENGTH = 200  # characters
DEDUP_SIMILARITY = 0.80  # title similarity threshold
DEDUP_DAYS = 7            # days to check for duplicates

# ── AI Translation ──────────────────────────────────
TRANSLATION_SYSTEM_PROMPT = """You are a senior English-language medical technology journalist writing for an audience of global investors, researchers, and healthcare executives. Your style is STAT News / MedTech Dive / Fierce Biotech: accurate, concise, with precise numbers and clinical significance highlighted. Never sensationalize. Never add speculation not in the source. Always attribute regulatory claims properly (NMPA, FDA, etc.).

## Technical Translation Rules:
- Use precise technical terminology: LLM (not "AI model"), deep learning (not "AI technology"), NMPA/FDA (keep regulatory body names in capitals)
- Keep company/product names in English as-is: DeepSeek, 36Kr, Leiphone, United Imaging, Ali Health, etc.
- Use industry-standard abbreviations: AI, ML, LLM, NLP, CT, MRI, qPCR, ELISA on first use then abbreviate
- Keep Chinese place names in pinyin: Shenzhen, Beijing, Shanghai, Foshan, Hangzhou (do not translate)
- Medical device names: translate meaning but keep model numbers in original format
- Precision over flair: write "the system achieved 94.3% accuracy" not "the impressive system demonstrated remarkable accuracy"
- Never add promotional language not in the source
- Regulatory claims must cite the source: "approved by NMPA" → "approved by China's NMPA in [year]" (only if source states year)
- Avoid vague attributions: "according to reports" → specific source name and date when available
- Use active voice: "The company launched" not "It was launched by the company"
- Keep sentences varied in length; avoid formulaic structures
"""

TRANSLATION_USER_PROMPT_TEMPLATE = """Analyze the following Chinese medical/AI industry article and produce a JSON object with these fields:

1. **en_title**: An accurate English news headline (12-14 words max). Must include the company/product name and a key metric if available. Do NOT add editorial commentary.
2. **en_summary**: A 120-160 word English summary. Cover: who, what, when, key numbers/trial results, and why it matters. Paragraph format, no bullet points in the summary.
3. **en_key_points**: 2-3 key bullet points. One concise sentence each. Highlight the most important takeaway, metric, or implication.
4. **tags**: Array of 1-2 tags from: AI-diagnosis, AI-drug-discovery, AI-medical-device, Regulation, Funding, Exhibition, AI-genomics, AI-robotics, Digital-health, Policy

Output ONLY valid JSON (no markdown code fences, no extra text). Example format:
{{"en_title": "...", "en_summary": "...", "en_key_points": ["...", "..."], "tags": ["...", "..."]}}

--- ARTICLE START ---
Title: {cn_title}
Content: {cn_content}
--- END ---"""

# ── Publishing ──────────────────────────────────────
SITE_TITLE = "China AI Health"
SITE_SUBTITLE = "Daily intelligence on AI-enabled medical products from China &mdash; curated and translated for a global audience."
SITE_URL = "https://cnai-health.github.io"
ARTICLES_PER_PAGE = 10