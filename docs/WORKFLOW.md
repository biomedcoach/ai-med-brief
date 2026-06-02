# AiMedbrief 完整工作流程 & 备份清单

> 生成日期：2026-06-02 21:52 (Beijing Time)
> 备份文件：`C:\Users\eugenie\.qclaw\backups\AiMedbrief-full-2026-06-02-2152.zip` (1.41 MB)

---

## 📦 一、备份内容

| 模块 | 文件数 | 说明 |
|------|--------|------|
| 项目源码 | 全部 | `D:\Qclaw\AiMedbrief\` 完整打包 |
| 首页 | 1 | `index.html`（静态首页，Apple风格，5篇文章卡片+配图） |
| 文章详情 | 5 | `articles/2026-06-02-01~05.html`（英文详情页+封面图） |
| 元数据 | 1 | `articles/data.json`（结构化文章数据） |
| 配图 | 5 | `images/2026-06-02-01~05.jpg`（MiniMax image-01生成） |
| 后端脚本 | 20+ | `backend/*.py`（爬虫/翻译/精选/构建） |
| 爬虫配置 | 1 | `backend/sources.yaml`（4个新闻源：36kr/Leiphone/Huxiu/VCBeat） |
| 候选数据 | 4 | `backend/data/candidates/`（爬虫原始输出 JSON） |
| 翻译结果 | 2 | `backend/data/processed/`（翻译+润色输出） |
| GitHub Actions | 3 | `.github/workflows/*.yml`（部署+定时任务） |
| 文档 | 3 | `docs/` + README.md + 产品方案 |

### 额外备份（临时脚本）

| 脚本 | 位置 | 用途 |
|------|------|------|
| `test_minimax_image.py` | workspace/tmp/ | 测试 MiniMax 图像 API 端点 |
| `generate_images.py` | workspace/tmp/ | 批量生成5张配图 |
| `rebuild_detail_pages.py` | workspace/tmp/ | 重建文章详情页 |
| `fix_articles.py` | workspace/tmp/ | 统一 source + 删 keypoints |
| `fix_build_index.py` | workspace/tmp/ | 修改 build_index.py |
| `update_dates.py` | workspace/tmp/ | 加北京时间标注 |
| `fix_sources.py` | workspace/tmp/ | 数据来源英文化 |

---

## 🔄 二、完整工作流程（6步）

```
爬虫 → 提取 → 筛选 → 翻译 → 配图 → 建站 → 推送
```

### Step 1：爬虫抓取（`crawl.py`）

```
输入：backend/sources.yaml（新闻源配置）
输出：backend/data/candidates/candidates_YYYY-MM-DD.json
```

**技术栈：** Playwright 无头浏览器（Chromium）
- 36kr（信息流、健康频道）：双源，至今稳定
- Leiphone（AI 频道）：单源，更新慢
- Huxiu（首页）：验证码阻挡，已跳过
- 动脉网（VCBeat）：纯 SPA 渲染，Playwright 取不到直链 → 改为手动 web_fetch + 搜索

**运行：**
```bash
cd D:\Qclaw\AiMedbrief\backend
python crawl.py
```

**抓取逻辑（crawl.py 核心）：**
- 每个源配置 `type`（playwright/rss/html）、`url`、`list_selector`
- 提取标题、链接、时间、摘要
- 去重（标题相似度 > 0.80 丢弃）
- 关键词打分（primary 匹配 +10，secondary +5，排除关键词 -50）
- 最低分阈值 30 → 进入候选池

---

### Step 2：筛选与提取（`debug_candidates.py` / 手动）

```
输入：candidates_YYYY-MM-DD.json（爬虫原始输出）
输出：candidates_YYYY-MM-DD_manual.md（Markdown 格式候选清单）
```

**当前实际做法（动脉网文章无法自动爬取时）：**
1. `web_fetch` 抓取动脉网首页、VBData 站点内容
2. 手动筛选相关文章（创新药/创新器械/居家检测/AI+医药）
3. 排除融资/政策类文章
4. 写入 `backend/data/candidates_june2_v2.md`

**筛选标准：**
- ✅ 创新药研发 / 临床试验 / ASCO
- ✅ 创新医疗器械审批
- ✅ AI + 医药 / 蛋白质设计 / 医疗AI
- ❌ 纯融资新闻
- ❌ 政策法规
- ❌ 纯商业并购（无研发内容）

---

### Step 3：翻译（`translate.py`）

```
输入：backend/data/candidates/candidates_YYYY-MM-DD.json
      → 手动转为 candidates_june2_v2_translated20260602.md
输出：backend/data/processed/processed_YYYY-MM-DD.json（含英文摘要）
```

**技术栈：**
- **LLM**: SiliconFlow API → `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B`（免费）
- **System Prompt**: 医疗英译专家 + 术语规范（来自 `technical-translation-expert` 技能）
- **超时**: 120s/篇（大量医学术语需更长推理时间）
- **增量保存**: 每翻译一篇立即保存，断点续传

**翻译质量保证：**
- 原文标题 → 英文标题（保留核心信息）
- 中文摘要 → 英文摘要（≈250 words，保留医学专有名词首字母大写）
- 术语统一：ADC/PD-1/VEGF/TIL/CAR-T/ASCO → 保持不变
- 去中文化：网页和 data.json 全英文

**运行：**
```bash
cd D:\Qclaw\AiMedbrief\backend
python translate.py
```

---

### Step 4：配图生成（`generate_images.py`）

> ⚠️ 这步用 MiniMax 的 **图像模型**（image-01），不是文本模型 M2.7

```
输入：英文标题 + 摘要（自动拼 prompt）
输出：images/YYYY-MM-DD-ID.jpg（1024×576）
```

**API 信息：**
- 端点：`POST https://api.minimax.chat/v1/image_generation`
- 模型：`image-01`
- 尺寸：`1024×576`（16:9，适配卡片）
- API Key：`sk-cp-AIamgPrpWnA9PDBbTTTwtWv...`

**Prompt 模板：**
```
Scientific illustration of [article topic], clean modern style, 
medical/biotech themed, blue and white color scheme, 
professional journal quality, no text overlays
```

**每篇定制 prompt 示例：**
- ADC 出海 → "antibody-drug conjugate molecular structure, global pharmaceutical trade"
- 核药α核素 → "alpha particle radiopharmaceutical, nuclear medicine laboratory"
- TIL疗法 → "tumor infiltrating lymphocytes, immuno-oncology, cellular therapy"
- AI蛋白质 → "AI-driven protein structure prediction, computational biology"
- 出海交易 → "global pharmaceutical business, China biotech out-licensing"

**运行：**
```bash
python tmp/generate_images.py
```

---

### Step 5：建站（`build_index.py` + `rebuild_articles.py`）

```
输入：articles/data.json（文章元数据）+ images/（配图）
输出：index.html + articles/*.html
```

**build_index.py 核心逻辑：**
1. 读取 `articles/data.json`
2. 生成 Hero 区（标题 + 广告位 + 北京时间标注）
3. 生成首页文章卡片：
   - 左：配图 `<img>`（280px → 平板 200px → 手机全宽 160px）
   - 右：分类标签 + 日期 + 标题 + 摘要 + 来源
   - 无 Key Takeaways
4. 生成侧边栏：Today's Coverage（侧边栏导航）+ Topics + Contact
5. 响应式 CSS：1024px / 640px 断点
6. 全站英文，零中文字符

**rebuild_articles.py 核心逻辑：**
1. 每篇文章生成独立 HTML
2. 顶部毛玻璃导航（`AiMedbrief` logo + `← Back to Home`）
3. 分类标签 + 北京时间日期
4. 封面大图（全宽圆角 16px）
5. 英文标题 + 英文摘要
6. 底部 Source 行（动脉网 (VCBeat) + Original source 链接）

**运行：**
```bash
cd D:\Qclaw\AiMedbrief
python backend/build_index.py      # 生成 index.html
python backend/rebuild_articles.py # 生成 articles/*.html
```

---

### Step 6：本地预览 & GitHub 推送

**本地预览：**
```bash
cd D:\Qclaw\AiMedbrief
python -m http.server 8080
# 浏览器打开 http://localhost:8080
```

**GitHub 推送：**
```bash
cd D:\Qclaw\AiMedbrief
git add -A
git commit -m "YYYY-MM-DD: update — N articles"
git push origin main
```

**自动部署（GitHub Actions → Pages）：**
- Repository: `biomedcoach/ai-med-brief`（public）
- `.github/workflows/deploy.yml` → 推送后自动部署
- Pages URL: `https://biomedcoach.github.io/ai-med-brief/`
- Secret: `SILICONFLOW_API_KEY`（用于定时爬虫 cron job）

---

## 📋 三、关键配置速查

| 项目 | 值 |
|------|-----|
| **项目路径** | `D:\Qclaw\AiMedbrief\` |
| **Python** | `C:\Users\eugenie\AppData\Local\Programs\Python\Python312\python.exe` |
| **LLM API** | SiliconFlow `POST https://api.siliconflow.cn/v1/chat/completions` |
| **LLM 模型** | `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B`（免费） |
| **图像 API** | MiniMax `POST https://api.minimax.chat/v1/image_generation` |
| **图像模型** | `image-01` |
| **GitHub** | `biomedcoach/ai-med-brief` / PAT (stored in GitHub Secrets) |
| **Pages URL** | `https://biomedcoach.github.io/ai-med-brief/` |
| **编码** | Python 脚本 `.py` UTF-8 / PowerShell `$env:PYTHONIOENCODING='utf-8'` |

---

## ⚡ 四、快速恢复指南

**如项目完全丢失，按以下顺序恢复：**

```bash
# 1. 解压备份
Expand-Archive -Path "C:\Users\eugenie\.qclaw\backups\AiMedbrief-full-2026-06-02-2152.zip" -DestinationPath "D:\Qclaw\AiMedbrief"

# 2. 确保 Python 依赖
cd D:\Qclaw\AiMedbrief\backend
pip install playwright requests pyyaml # 如需爬虫
playwright install chromium

# 3. 验证文件完整性（必须有）
# - index.html
# - articles/data.json
# - images/*.jpg (5张)
# - backend/build_index.py

# 4. 本地预览
cd D:\Qclaw\AiMedbrief
python -m http.server 8080

# 5. 修改后推送
git add -A
git commit -m "update"
git push origin main
```

---

## ⚠️ 五、已知问题

1. **crawl-publish.yml GitHub Actions 失败** — 定时爬虫在 GitHub 上跑不通（403/验证码），当前由本地手动跑
2. **动脉网无直链** — SPA 渲染站点，所有文章链接指向 vbdata.cn 首页而非原文
3. **Huxiu 验证码** — Playwright 无法通过滑动验证码
4. **humanize.py 超时** — 润色环节耗时过长，5/31 被终止，当前未使用
5. **MiniMax API 端点 4 选 1** — 测试了 4 个候选 URL，最终确认 `api.minimax.chat` 可用
6. **build_index.py 不用 f-string** — 全用纯字符串拼接，避免 CSS 花括号冲突

---

## 📝 六、AI 配图 Prompt 记录（5篇）

| 文章 | Prompt关键词 |
|------|-------------|
| ADC 出海 | antibody-drug conjugate molecular structure, global pharmaceutical trade, clean scientific, blue gradient |
| 核药α核素 | alpha particle radiopharmaceutical, nuclear medicine laboratory, glowing isotopes, dark blue |
| TIL细胞疗法 | tumor infiltrating lymphocytes attacking cancer, immuno-oncology, cellular therapy, microscopic, vibrant |
| AI蛋白质设计 | AI-driven protein folding prediction, computational biology, helix structures, digital visualization |
| 中国创新药出海 | global pharmaceutical business, China biotech out-licensing, deal making, world map connections |

---

*文档由 QClaw 自动生成，记录 AiMedbrief 项目截至 2026-06-02 21:52 的完整工作流程备份。*