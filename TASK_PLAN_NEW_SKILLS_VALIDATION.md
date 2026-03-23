# 新增研究方法论技能核验任务计划

## 任务概述

**任务ID**: NEW_SKILLS_VALIDATION_001
**创建时间**: 2026-03-15
**优先级**: 高
**预计工作量**: 21技能 × 12缺失文件 = ~252文件

## 任务目标

按照v5.0.0-cli-native+agent标准，逐个核查并补全21个新增研究方法论技能。

## 核验标准（每技能15文件）

```
agentskills/[skill-name]/
├── SKILL.md                    # 主技能文档
├── skill.yaml                  # 技能配置
├── subagents.yaml              # 子Agent定义
├── skill-hooks.yaml            # 三层持久化hooks
├── lesson-memory.md            # 经验记忆库
├── prompts/
│   └── system-prompt.md        # 系统提示词
├── references/
│   └── detailed-guide.md       # 详细方法论指南
├── cases/
│   ├── positive/               # 成功案例
│   └── negative/               # 失败案例
├── templates/
│   └── [method]-template.md    # 方法模板
├── tools/
│   └── [tool].py               # Python工具脚本
└── experience/
    └── best-practices.md       # 最佳实践
```

## 分批执行计划

### 批次1: 质性研究方法（8个技能）

| # | 技能名称 | 当前状态 | 目标状态 |
|---|----------|----------|----------|
| 1.1 | action-research-expert | 3文件 ❌ | 15文件 ✅ |
| 1.2 | case-study-expert | 3文件 ❌ | 15文件 ✅ |
| 1.3 | ethnography-expert | 3文件 ❌ | 15文件 ✅ |
| 1.4 | phenomenology-expert | 3文件 ❌ | 15文件 ✅ |
| 1.5 | narrative-analysis-expert | 3文件 ❌ | 15文件 ✅ |
| 1.6 | ipa-analysis-expert | 3文件 ❌ | 15文件 ✅ |
| 1.7 | discourse-analysis-expert | 3文件 ❌ | 15文件 ✅ |
| 1.8 | thematic-analysis-expert | 10文件 ⚠️ | 15文件 ✅ |

**批次1预计文件数**: 8 × 15 = 120文件

### 批次2: 定量研究方法（7个技能）

| # | 技能名称 | 当前状态 | 目标状态 |
|---|----------|----------|----------|
| 2.1 | regression-analysis-expert | 8文件 ⚠️ | 15文件 ✅ |
| 2.2 | factor-analysis-expert | 3文件 ❌ | 15文件 ✅ |
| 2.3 | sem-analysis-expert | 3文件 ❌ | 15文件 ✅ |
| 2.4 | meta-analysis-expert | 8文件 ⚠️ | 15文件 ✅ |
| 2.5 | rct-experimental-design-expert | 4文件 ⚠️ | 15文件 ✅ |
| 2.6 | longitudinal-analysis-expert | 3文件 ❌ | 15文件 ✅ |
| 2.7 | multilevel-modeling-expert | 3文件 ❌ | 15文件 ✅ |

**批次2预计文件数**: 7 × 15 = 105文件

### 批次3: 混合方法+新兴方法（6个技能）

| # | 技能名称 | 当前状态 | 目标状态 |
|---|----------|----------|----------|
| 3.1 | mixed-methods-expert | 3文件 ❌ | 15文件 ✅ |
| 3.2 | content-analysis-expert | 6文件 ⚠️ | 15文件 ✅ |
| 3.3 | nlp-text-mining-expert | 3文件 ❌ | 15文件 ✅ |
| 3.4 | machine-learning-research-expert | 3文件 ❌ | 15文件 ✅ |
| 3.5 | bibliometric-analysis-expert | 3文件 ❌ | 15文件 ✅ |
| 3.6 | social-sequence-analysis-expert | 3文件 ❌ | 15文件 ✅ |

**批次3预计文件数**: 6 × 15 = 90文件

## 核验流程（每技能）

```
1. 文件完整性检查
   ├── 统计现有文件数
   ├── 对比标准15文件
   └── 识别缺失文件

2. 内容质量检查
   ├── SKILL.md内容完整性
   ├── 6大禁止原则定制化
   ├── CRCT思维链实现
   └── 方法论对齐验证

3. 真实场景可用性检查
   ├── 子Agent调用测试
   ├── Python工具可用性
   ├── 三层持久化测试
   └── 跨CLI兼容性测试

4. 补全缺失内容
   ├── 创建缺失文件
   ├── 填充内容
   └── 质量验证
```

## 进度追踪

### 当前会话进度
- [x] 批次1.1: action-research-expert ✅ 完成 (15/15)
- [x] 批次1.2: case-study-expert ✅ 完成 (15/15)
- [x] 批次1.3: ethnography-expert ✅ 完成 (15/15)
- [ ] 批次1.4: phenomenology-expert
- [ ] ...

### 历史会话记录
| 会话日期 | 完成技能 | 备注 |
|----------|----------|------|
| 2026-03-15 | action-research-expert, case-study-expert | 任务计划创建，完成2个技能核验 |

## 质量检查清单

每技能完成时需确认：
- [x] 15个文件全部存在
- [x] SKILL.md包含完整方法论
- [x] 6大禁止原则已定制
- [x] CRCT思维链已实现
- [x] prompts/system-prompt.md完整
- [x] references/detailed-guide.md完整
- [x] cases/包含正负面案例
- [x] templates/包含方法模板
- [x] tools/包含Python工具
- [x] experience/best-practices.md完整
- [x] skill-hooks.yaml配置正确
- [x] lesson-memory.md包含经验
- [x] subagents.yaml子Agent定义清晰

---

**任务状态**: 进行中
**当前进度**: 2/21 (9.5%)
**最后更新**: 2026-03-15
