# AiMedbrief UI 全面调整 — 2026-06-02 19:05

## 背景
用户要求对 AiMedbrief 首页和文章详情页进行 5 项 UI 调整。

## 执行内容

### 1. 卡片增加图片占位区（左侧）
- 卡片改为 `display:flex` 双栏布局
- 左侧 280px 渐变色背景 + "Image" 占位文字（`.card-img` / `.img-placeholder`）
- 右侧为标题、摘要、标签、Key Takeaways 折叠区
- 响应式：窄屏下图片区缩放/堆叠

### 2. 移除 Weekly Digest 订阅模块
- 完全从侧边栏删除

### 3. 今日内容上方 2 个广告位
- 侧边栏 Today's Coverage 上方插入两个 `.ad-slot`
- 样式：占位卡片，虚线边框，180px 高度，标签 "Advertisement"
- 内容："Your brand here" + "advertise@aimedbrief.com"

### 4. 全站去中文
- index.html：所有标签、文案替换为英文
- 4 篇详情页：`lang="zh-CN"` → `"en"`，删除 `<h2>中文报道</h2>` 及中文摘要
- data.json：source 从"动脉网"改为 "VCBeat / VBData"
- build 脚本全部改用纯字符串拼接（避免 f-string 内嵌 CSS 花括号冲突）

### 5. 顶部导航放大 1.5 倍
- `.top-bar-inner` padding: 8px→14px 24px→28px
- `.top-bar-brand h1` font-size: 14px→20px
- `.top-bar-brand span` font-size: 13px→15px
- `.top-bar-links` font-size: 12px→14px, gap: 16px→20px

## 关键文件
| 文件 | 变化 |
|------|------|
| `backend/build_index.py` | 完全重写（字符串拼接替代 f-string） |
| `backend/rebuild_articles.py` | 新建，生成纯英文详情页 |
| `backend/fix_sources.py` | 新建，修复 data.json source 中文 |
| `index.html` | 重生成，21KB |
| `articles/2026-06-02-*.html` | 4篇全英文重建 |
| `articles/data.json` | source 英文化 |

## 构建脚本
```bash
python backend/build_index.py      # 生成首页
python backend/rebuild_articles.py # 生成文章详情页
```

## 验证结果
- 公共页面（index.html + 4 篇详情页）零中文字符 ✅
- 卡片结构：flex 双栏 + 图片占位 ✅
- 广告位数量：2 ✅
- Weekly Digest：已删除 ✅
- 导航栏：padding/font-size 已放大 ✅
