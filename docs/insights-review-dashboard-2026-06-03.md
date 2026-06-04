# 产品洞察仪表盘 + 输出审阅台开发

## 日期
2026-06-03 15:13 ~ 16:00

## 目标
基于 review_notes 表，开发两大管理后台页面：产品洞察仪表盘和输出审阅台，实现 AI 输出质量的系统化管理。

## 完成内容

### 1. API 层（3 个新端点）

**`/api/admin/insights?days=30`** — 聚合所有洞察数据：
- 工具使用排行榜、各工具评审均分
- 用户转化漏斗（报告表→工具使用）
- 四象限分析（热度×质量 → 明星/修复/埋没/低优先）
- 每日评审趋势、问题标签统计
- 自动建议生成（低质高频→优先修复，优质低频→增加曝光）

**`/api/admin/review/samples`** — 样本列表（支持 tool_type/status 筛选，分页）
- LEFT JOIN review_notes 获取已有评审状态

**`/api/admin/review/notes`** — 审阅记录 CRUD（POST upsert / GET / DELETE）

### 2. 前端页面

**`/admin/insights`** — 产品洞察仪表盘：
- 概览卡片（工具总输出/整体均分/优秀案例/待审阅）
- 四象限分析矩阵
- 用户转化漏斗 + 问题标签
- 自动建议面板
- 工具使用排名表
- 审阅趋势柱状图
- 快捷跳转审阅台

**`/admin/review`** — 输出审阅台：
- 左侧样本列表（工具/状态筛选 + 分页）
- 右侧分屏审阅面板（输入↔输出并排）
- 四维度 1-5★ 评分（相关性/准确度/完整度/文笔）
- 自动综合分 + 优秀案例勾选
- 问题标签（预设+自定义）
- 管理员备注 + 即时保存

### 3. 管理后台入口
在 `/admin` 快捷入口中新增"产品洞察"和"输出审阅"链接。

## 踩坑记录

1. **MySQL 5.7 prepared statement 兼容性**：`pool.query(sql, [days])` 的 `?` 占位符在复杂子查询中不被 MySQL 5.7 接受。改用模板字符串直接插值。

2. **表名不一致**：本地数据库的诊断表叫 `reports`（非 `diagnosis_reports`），修正 SQL 查询中的表名。

3. **MySQL 5.7 LEFT JOIN 子查询限制**：`LEFT JOIN (SELECT ...) t` 需要显式 `ON 1=1`，否则报语法错误。

4. **MySQL 5.7 utf8mb4_0900_ai_ci → utf8mb4_general_ci**：导入数据时的排序规则降级已在前置步骤处理。

## 测试结果
- Insights API: ✅ 200, 数据聚合正常
- Samples API: ✅ 200, 分页筛选正常
- /admin/insights 页面: ✅ 200
- /admin/review 页面: ✅ 200
- /admin 入口: ✅ 200

## 文件清单
| 文件 | 说明 |
|------|------|
| `app/api/admin/insights/route.ts` | 洞察聚合 API |
| `app/api/admin/review/samples/route.ts` | 样本列表 API |
| `app/api/admin/review/notes/route.ts` | 审阅记录 CRUD API |
| `app/admin/insights/page.tsx` | 洞察仪表盘页面 |
| `app/admin/review/page.tsx` | 审阅台页面 |
| `app/admin/page.tsx` | 添加快捷入口 |
