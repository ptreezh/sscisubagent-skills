# 社会科学方法论 Skill 改进计划

**核查日期**: 2026-03-05  
**核查结果**: 13 个技能全部需要改进  
**平均分**: 53.5/100

---

## 📊 核查结果汇总

### 维度得分统计

| 维度 | 平均分 | 最高 | 最低 | 状态 |
|------|--------|------|------|------|
| agentskills.io 规范符合性 | 92% | 100% | 80% | ✅ 优秀 |
| 复杂任务分解支持 | 60% | 60% | 60% | ⚠️ 需改进 |
| 持久化任务计划运行 | 44% | 64% | 0% | ❌ 不足 |
| 信息渐进式披露优化 | 28% | 36% | 0% | ❌ 严重不足 |

### 技能分类

**第一组**: 65 分 (7 个技能)
- grounded-theory-expert
- social-network-analysis-expert
- actor-network-analysis-expert
- digital-marx-expert
- digital-durkheim-expert
- digital-weber-expert
- data-analysis-expert
- survey-design-expert

**第二组**: 35 分 (5 个技能)
- bourdieu-field-analysis-expert
- msqca-analysis-expert
- did-analysis-expert
- business-ecosystem-analysis-expert
- business-model-analysis-expert

---

## 🔧 改进措施

### 问题 1: 复杂任务分解支持 (60%)

**问题描述**:
- 部分技能缺少明确的多阶段分析流程
- 子任务管理逻辑不完善

**改进措施**:
1. 在每个 skill 的 SKILL.md 中明确添加 Phase 1-6 分析流程
2. 在 analyze.py 中添加阶段管理代码
3. 添加子任务分解和调度逻辑

**优先级**: 🔴 高

### 问题 2: 持久化任务计划运行 (44%)

**问题描述**:
- 部分技能缺少 task_plan 模板
- 状态持久化代码不完整
- 缺少会话恢复机制

**改进措施**:
1. 为每个 skill 创建完整的 templates/task_plan.md.template
2. 在 analyze.py 中添加状态保存/加载代码
3. 添加 recover_session() 方法

**优先级**: 🔴 高

### 问题 3: 信息渐进式披露优化 (28%)

**问题描述**:
- 缺少分阶段输出设计
- 没有摘要 + 详情模式
- 缺少披露级别控制

**改进措施**:
1. 在 SKILL.md 中添加"分阶段输出"说明
2. 在 analyze.py 中添加 summary 和 detail 两种输出模式
3. 添加 detail_level 参数控制披露级别

**优先级**: 🟡 中

---

## 📅 改进时间表

### 第 1 周：持久化任务计划运行
- [ ] 为所有 13 个技能创建 task_plan 模板
- [ ] 添加状态持久化代码
- [ ] 实现会话恢复功能

### 第 2 周：复杂任务分解
- [ ] 完善 SKILL.md 中的多阶段流程
- [ ] 添加子任务管理代码
- [ ] 测试任务分解逻辑

### 第 3 周：信息渐进式披露
- [ ] 添加分阶段输出设计
- [ ] 实现摘要 + 详情模式
- [ ] 添加披露级别控制参数

### 第 4 周：测试和验证
- [ ] 运行核查系统复测
- [ ] 确保所有技能≥80 分
- [ ] 生成最终报告

---

## 🚀 自动化改进脚本

使用自动化脚本批量改进：

```bash
# 运行改进脚本
python auto-improve.py --dimension persistent_planning
python auto-improve.py --dimension task_decomposition
python auto-improve.py --dimension progressive_disclosure
```

---

## ✅ 验收标准

所有技能必须达到：
- ✅ agentskills.io 规范符合性 ≥ 100%
- ✅ 复杂任务分解支持 ≥ 80%
- ✅ 持久化任务计划运行 ≥ 80%
- ✅ 信息渐进式披露优化 ≥ 80%
- ✅ 总分 ≥ 80/100

---

**改进计划制定完成**

*制定日期*: 2026-03-05  
*预计完成*: 2026-03-26  
*负责人*: SocienceAI Team
