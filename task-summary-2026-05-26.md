# Task Summary — 2026-05-26 中国 AI 医疗英文资讯站

## 背景
用户要做一个静态英文资讯站，汇总中国 AI 医疗产品/检测/器械/展会相关新闻。
每天爬30-40篇中文文章 → AI翻译成英文摘要 → 人工精选10篇 → 自动发布到 GitHub Pages。

## 今日产出

### 1. 静态首页 design
- **文件**: `index.html`
- **风格**: Apple 科技媒体风（浅灰底 + 纯白卡片 + SF 系统字体）
- 有右侧广告位（初期展示重要新闻，后期卖广告）
- 无 emoji、无来源标注（首页不标，详情页再标）
- 10篇示例文章：AI诊断/制药/器械/监管/融资/展会全覆盖

### 2. 翻译模型对比
- **文件**: `translation-model-comparison.md`
- **结论**: MVP用SiliconFlow（免费），精选文章用MiniMax精翻（$1.5/月）

### 3. 后端完整架构
- **文件**: `backend-design.html`
- 4模块流水线: crawl.py → translate.py → curation_ui.py → publish.py

### 4. 后端代码 (全部写完)
- `backend/config.py` — API密钥、路径、评分权重、翻译prompt
- `backend/sources.yaml` — 15个爬虫源（RSS+HTML），含评分规则和过滤
- `backend/crawl.py` — 爬虫（RSS/HTML二合一），SQLite去重，Quality Score 5维打分
- `backend/translate.py` — SiliconFlow API翻译，JSON结构化输出
- `backend/curation_ui.py` — Streamlit精选界面（你操作的地方）
- `backend/publish.py` — 静态页面生成器，基于HTML模板
- `backend/requirements.txt` — Python依赖
- `.github/workflows/daily.yml` — GitHub Actions定时任务

### 5. Quality Score 算法
5个维度加权: Freshness(30%) + Authority(25%) + Relevance(20%) + Density(15%) + Rarity(10%)

### 6. 用户操作流程
每天只需: `python curation_ui.py` → 浏览器勾选10篇 → 点确认。凌晨自动发布。

## 待做
- 用户终端 `pip install -r requirements.txt` 装依赖
- `python crawl.py` 首次试跑，看候选文章质量
- 调 sources.yaml 里的 authority 和 cat_filter
- 调 config.py 里的 SCORE_WEIGHTS 权重
- Streamlit curation UI 实际跑一次看交互
- 注册 GitHub repo，配置 Actions secrets