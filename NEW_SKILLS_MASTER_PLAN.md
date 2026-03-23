# 新研究方法论技能创建总计划

**创建时间**: 2026-03-15
**状态**: 进行中
**总技能数**: 21个新技能

---

## 执行状态概览

### 第一批 - 核心技能 (5个) ⭐⭐⭐
| 编号 | 技能名称 | 状态 | 完成度 |
|------|----------|------|--------|
| 1 | thematic-analysis-expert | ✅ complete | 100% |
| 2 | meta-analysis-expert | ✅ complete | 100% |
| 3 | sem-analysis-expert | ✅ complete | 100% |
| 4 | regression-analysis-expert | ✅ complete | 100% |
| 5 | content-analysis-expert | ✅ complete | 100% |

### 第二批 - 高频技能 (6个) ⭐⭐
| 编号 | 技能名称 | 状态 | 完成度 |
|------|----------|------|--------|
| 6 | rct-experimental-design-expert | ✅ complete | 100% |
| 7 | discourse-analysis-expert | ✅ complete | 100% |
| 8 | ethnography-expert | pending | 0% |
| 9 | factor-analysis-expert | pending | 0% |
| 10 | mixed-methods-expert | pending | 0% |
| 11 | case-study-expert | pending | 0% |

### 第三批 - 常用技能 (6个) ⭐
| 编号 | 技能名称 | 状态 | 完成度 |
|------|----------|------|--------|
| 12 | ipa-analysis-expert | pending | 0% |
| 13 | narrative-analysis-expert | pending | 0% |
| 14 | phenomenology-expert | pending | 0% |
| 15 | multilevel-modeling-expert | pending | 0% |
| 16 | longitudinal-analysis-expert | pending | 0% |
| 17 | action-research-expert | pending | 0% |

### 第四批 - 新兴方法 (4个)
| 编号 | 技能名称 | 状态 | 完成度 |
|------|----------|------|--------|
| 18 | nlp-text-mining-expert | pending | 0% |
| 19 | machine-learning-research-expert | pending | 0% |
| 20 | bibliometric-analysis-expert | pending | 0% |
| 21 | social-sequence-analysis-expert | pending | 0% |

---

## 单技能创建流程 (6步骤)

每个技能必须完成以下6个步骤：

### Step 1: 目录结构创建
- [ ] 创建技能目录 `agentskills/{skill-name}/`
- [ ] 创建子目录: `prompts/`, `tools/`, `references/`, `test_data/`

### Step 2: 核心文件创建
- [ ] 创建 `SKILL.md` (agentskills.io规范)
- [ ] 创建 `skill.yaml` (技能配置)
- [ ] 创建 `subagents.yaml` (子智能体配置)

### Step 3: 提示词系统
- [ ] 创建 `prompts/system-prompt.md` (系统提示词)
- [ ] 创建专业分析提示词文件

### Step 4: 工具函数
- [ ] 创建 `tools/` 下的Python工具
- [ ] 确保跨平台兼容性

### Step 5: 测试数据
- [ ] 创建 `test_data/` 示例数据
- [ ] 创建测试脚本

### Step 6: 验证与对齐
- [ ] 运行 `validate_skill_spec.py` 验证
- [ ] 与现有16个技能对齐
- [ ] 更新 `agentskills-index.json`

---

## 错误日志

| 时间 | 技能 | 错误 | 解决方案 |
|------|------|------|----------|
| - | - | - | - |

---

## 会话恢复指令

下次会话继续时，执行：
```
读取此文件 → 找到第一个pending技能 → 从Step 1继续
```

---

## 当前进度

**当前批次**: 第一批
**已完成技能**: thematic-analysis-expert, meta-analysis-expert, sem-analysis-expert
**当前技能**: regression-analysis-expert
**当前步骤**: Step 1 - 目录结构创建
**下一步行动**: 创建regression-analysis-expert目录结构

---

## 已完成技能详情

### thematic-analysis-expert ✅
- 完成时间: 2026-03-15
- 包含: SKILL.md, skill.yaml, subagents.yaml, system-prompt.md, 4个工具, 详细指南

### meta-analysis-expert ✅
- 完成时间: 2026-03-15
- 包含: SKILL.md, skill.yaml, subagents.yaml, system-prompt.md, 3个工具, skill_manifest.json
- 特点: Level I证据等级，PRISMA流程支持

### sem-analysis-expert ✅
- 完成时间: 2026-03-15
- 包含: SKILL.md, skill.yaml, system-prompt.md
- 特点: SEM全流程支持，模型拟合标准完整
