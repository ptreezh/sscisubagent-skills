# 主题分析专家技能创建计划

**技能名称**: thematic-analysis-expert
**中文名称**: 主题分析专家
**优先级**: ⭐⭐⭐ 最高
**使用频率**: 质性研究中最广泛使用的方法
**创建时间**: 2026-03-15

---

## 技能概述

### 学术背景
主题分析(Thematic Analysis)是由Braun & Clarke (2006)系统化的质性研究方法，是目前质性研究中使用最广泛的分析方法之一。相比扎根理论的复杂性，主题分析更加灵活、易学、适用范围广。

### 核心能力
1. **六步骤分析流程**: 熟悉数据 → 生成初始代码 → 搜索主题 → 审查主题 → 定义命名主题 → 撰写报告
2. **归纳与演绎模式**: 支持数据驱动的归纳分析和理论驱动的演绎分析
3. **主题质量评估**: 内部一致性、外部异质性、主题饱和度检验
4. **反思性实践**: 研究者位置性反思、分析过程透明化

### 适用场景
- 访谈数据分析
- 焦点小组讨论
- 开放式问卷回答
- 文本/文档分析
- 社交媒体内容分析
- 日记/叙事材料分析

---

## 详细创建步骤

### Step 1: 目录结构 ✅
```
agentskills/thematic-analysis-expert/
├── SKILL.md                    # 技能说明
├── skill.yaml                  # 配置文件
├── subagents.yaml              # 子智能体
├── prompts/
│   ├── system-prompt.md        # 系统提示词
│   ├── coding-prompt.md        # 编码提示词
│   ├── theme-development-prompt.md  # 主题发展提示词
│   └── report-writing-prompt.md     # 报告撰写提示词
├── tools/
│   ├── code_extractor.py       # 代码提取工具
│   ├── theme_cluster.py        # 主题聚类工具
│   ├── saturation_checker.py   # 饱和度检验工具
│   └── quality_assessor.py     # 质量评估工具
├── references/
│   ├── detailed-guide.md       # 详细指南
│   └── braun-clarke-2006.md    # 经典文献摘要
└── test_data/
    ├── interview_sample.json   # 访谈样本
    └── analysis_example.json   # 分析示例
```

### Step 2: SKILL.md 内容规划
- 遵循agentskills.io规范
- 包含name, description, license, compatibility, metadata
- 详细的技能能力说明

### Step 3: 系统提示词规划
- Braun & Clarke 六步骤方法论
- 反思性主题分析(Reflexive TA)
- 代码簿方法(Codebook TA)
- 编码可靠性方法(Coding Reliability TA)

### Step 4: 工具函数规划
- `code_extractor.py`: 从文本中提取初始代码
- `theme_cluster.py`: 将代码聚类为主题
- `saturation_checker.py`: 检验主题饱和度
- `quality_assessor.py`: 评估分析质量

### Step 5: 测试数据规划
- 使用真实访谈片段(匿名化)
- 包含不同领域的示例
- 提供完整的分析流程示例

### Step 6: 验证清单
- [ ] SKILL.md格式正确
- [ ] 所有工具跨平台兼容
- [ ] 提示词符合方法论规范
- [ ] 测试数据真实可用
- [ ] 与现有技能对齐

---

## 进度追踪

| 步骤 | 状态 | 完成时间 |
|------|------|----------|
| Step 1: 目录结构 | in_progress | - |
| Step 2: 核心文件 | pending | - |
| Step 3: 提示词系统 | pending | - |
| Step 4: 工具函数 | pending | - |
| Step 5: 测试数据 | pending | - |
| Step 6: 验证对齐 | pending | - |

---

## 错误记录

| 尝试 | 操作 | 错误 | 解决方案 |
|------|------|------|----------|
| - | - | - | - |
