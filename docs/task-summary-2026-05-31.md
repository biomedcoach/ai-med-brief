# AiMedbrief 项目状态 — 2026-05-31

## 完成情况

### 核心代码
| 文件 | 状态 | 说明 |
|------|------|------|
| `crawl.py` | ✅ 完成 | Playwright 无头浏览器爬虫，5 个新闻源 |
| `translate.py` | ✅ 完成 | SiliconFlow API 翻译，含技术翻译专家规则 |
| `humanize.py` | ✅ 创建 | 润色步骤（暂跳过，太慢，见下方说明）|
| `select.py` | ✅ 完成 | 自动选择 top 10，质量评分系统 |
| `publish.py` | ✅ 完成 | 生成静态 index.html + articles/*.md |
| `curation_ui.py` | ✅ 完成 | 人工精选 GUI 工具 |
| `config.py` | ✅ 完成 | 含技术翻译专家规则 |
| `sources.yaml` | ✅ 完成 | 5 个新闻源配置 |
| `requirements.txt` | ✅ 完成 | Python 依赖 |

### GitHub Actions
| 文件 | 状态 | 说明 |
|------|------|------|
| `.github/workflows/crawl-publish.yml` | ✅ 完成 | 定时爬取/翻译/发布，3个时间点 |

### 生成的网站
| 文件 | 大小 | 说明 |
|------|------|------|
| `index.html` | 31 KB | 静态首页（Apple风格，科技感） |
| `articles/01-10.md` | 各 1.4-1.7 KB | 10 篇英文文章 |

---

## 当前数据（2026-05-31）

**爬取结果：** 16 篇候选文章
**翻译结果：** 16/16 完成
**精选结果：** 10 篇 top 文章（质量评分 58-67）

**精选前 3 篇：**
1. LinuTech Intelligence Launches AI Brain Imaging Systems — 67分
2. DeepSeek AI Limits Re-generation and Modification — 63分
3. Foshan Nanhai AI Medical System Achieves 20% Error Reduction — 63分

---

## humanize.py 说明

**已创建** `humanize.py`，集成 humanizer-zh 规则（去除 AI 写作痕迹）。
**当前跳过** — 每篇文章需 3 次 API 调用（标题/摘要/要点），16篇 × 3 × 90秒 ≈ 72分钟，太慢。

**优化方案（待实施）：**
- 方案 A：只润色标题（1 次/篇，16 分钟）
- 方案 B：离线处理，GitHub Actions 单独步骤，凌晨空闲运行
- 方案 C：集成到 translate.py 同一个 prompt 里（不额外 API 调用）

---

## 待完成

1. **创建 GitHub 仓库**（当前未初始化 Git）
2. **配置 GitHub Pages**（设置 Source: gh-pages branch 或 docs/）
3. **添加 SILICONFLOW_API_KEY** 到 GitHub Secrets
4. **测试 GitHub Actions** 定时任务
5. **humanize 优化**（选择上述方案之一实施）

---

## 文件路径

- 项目根目录：`D:\Qclaw\AiMedbrief`
- 源码目录：`D:\Qclaw\AiMedbrief\backend`
- 生成的网站：`D:\Qclaw\AiMedbrief\index.html` + `articles/`
- 备份数据：`D:\Qclaw\AiMedbrief\backend\data\candidates/` + `processed/` + `selected/`
