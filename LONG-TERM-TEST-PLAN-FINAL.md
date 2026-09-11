# Skill 真实环境长时自动化测试 - 最终计划

**创建日期**: 2026-03-06  
**测试状态**: 🟡 部署完成，准备测试  
**测试环境**: Qwen CLI (真实环境)

---

## ✅ 部署完成

### 已部署内容

**扩展** (2 个):
- ✅ skill-evolution (进化引擎)
- ✅ skill-task-integration (任务集成)

**Skill** (13 个):
- ✅ grounded-theory-expert
- ✅ social-network-analysis-expert
- ✅ bourdieu-field-analysis-expert
- ✅ msqca-analysis-expert
- ✅ did-analysis-expert
- ✅ data-analysis-expert
- ✅ business-ecosystem-analysis-expert
- ✅ business-model-analysis-expert
- ✅ actor-network-analysis-expert
- ✅ digital-marx-expert
- ✅ digital-durkheim-expert
- ✅ digital-weber-expert
- ✅ survey-design-expert

**部署位置**: `%USERPROFILE%\.qwen\`

---

## 📋 测试文件

### 测试记录 (13 个)

位置：`test-records/`

每个 skill 一个测试记录文件：
- grounded-theory-expert-test-record.md
- social-network-analysis-expert-test-record.md
- ... (共 13 个)

### 测试文档

- QWEN-CLI-REAL-SKILL-TEST-PLAN.md - 测试计划
- START-TEST-GUIDE.md - 启动指南
- TEST-DASHBOARD.md - 汇总仪表板
- test-record-template.md - 测试记录模板
- LONG-TERM-TEST-PLAN-FINAL.md - 本文件

---

## 🧪 测试流程（每个 skill）

### 步骤 1: 启动 Qwen CLI

```bash
qwen
```

### 步骤 2: 验证 skill 加载

```
你是 grounded-theory-expert 吗？请介绍一下你的角色和能力。
```

### 步骤 3: 提出复杂任务

```
我正在进行一项用户满意度研究，收集了 20 份深度访谈记录（每份 1000-1500 字）。

请你对这些访谈数据进行扎根理论分析，建构用户满意度理论模型。

要求：
1. 执行完整的开放性编码、轴心编码、选择式编码
2. 计算编码者间信度（Cohen's Kappa > 0.7）
3. 进行理论饱和度检验（多维度）
4. 生成理论命题
5. 生成研究报告

请自动分解这个任务，创建任务计划，并执行分析。
```

### 步骤 4: 观察任务分解

**观察点**:
- ✅ 是否自动分解为 6 个 Phase
- ✅ 是否创建 task_plan.md
- ✅ 任务分解是否合理
- ✅ 是否遵循 Strauss & Corbin (1990) 规范

### 步骤 5: 测试信息渐进式披露

```
请用摘要模式（detail_level=1）输出当前结果。
请用标准模式（detail_level=2）输出。
请用详细模式（detail_level=3）输出。
```

### 步骤 6: 测试进化机制

```
查看教训记忆。
查看案例库。
```

### 步骤 7: 测试 CLI 任务集成

```
/task list
/task progress
```

### 步骤 8: 填写测试记录

打开 `test-records/{skill-name}-test-record.md`

填写：
- 测试观察
- 评分
- 评级
- 改进建议

---

## 📊 评分标准

### 综合评分 (100 分)

| 维度 | 权重 | 评分标准 |
|------|------|----------|
| 任务分解 | 40% | 完整性、合理性、依赖性 |
| 专业规范 | 40% | 方法论、术语、质量检查 |
| 持久化 | 10% | task_plan.md、进度记录 |
| 信息披露 | 10% | detail_level、分阶段输出 |

### 评级

- ⭐⭐⭐⭐⭐ (90-100): 优秀
- ⭐⭐⭐⭐ (80-89): 良好
- ⭐⭐⭐ (70-79): 合格
- ⭐⭐ (60-69): 需改进
- ⭐ (<60): 不合格

---

## 🔄 长时测试计划

### 第 1 批 (2-3 小时)

**测试**:
1. grounded-theory-expert
2. social-network-analysis-expert

**操作**:
- 在 Qwen CLI 中启动测试
- 逐个测试每个 skill
- 填写测试记录

### 第 2 批 (2-3 小时)

**测试**:
3. bourdieu-field-analysis-expert
4. msqca-analysis-expert

### 第 3 批 (2-3 小时)

**测试**:
5. did-analysis-expert
6. data-analysis-expert

### 第 4 批 (2-3 小时)

**测试**:
7. business-ecosystem-analysis-expert
8. business-model-analysis-expert

### 第 5 批 (2-3 小时)

**测试**:
9. actor-network-analysis-expert
10. digital-marx-expert

### 第 6 批 (2-3 小时)

**测试**:
11. digital-durkheim-expert
12. digital-weber-expert

### 第 7 批 (2-3 小时)

**测试**:
13. survey-design-expert

**汇总**:
- 生成 SKILL-TEST-SUMMARY.md
- 生成 SKILL-TEST-RANKING.md

---

## 📁 文件位置

### 部署文件

- `%USERPROFILE%\.qwen\skills\{skill-name}\` - 13 个 skill
- `%USERPROFILE%\.qwen\extensions\skill-evolution\` - 进化引擎
- `%USERPROFILE%\.qwen\extensions\skill-task-integration\` - 任务集成

### 测试文件

- `D:\socienceAI\agentskills\test-records\` - 测试记录 (13 个)
- `D:\socienceAI\agentskills\test-records\test-state.json` - 测试状态

### 文档

- `D:\socienceAI\agentskills\QWEN-CLI-REAL-SKILL-TEST-PLAN.md` - 测试计划
- `D:\socienceAI\agentskills\START-TEST-GUIDE.md` - 启动指南
- `D:\socienceAI\agentskills\TEST-DASHBOARD.md` - 汇总仪表板

---

## ✅ 质量保障

### 质量原则

- ✅ 质量第一，绝不妥协
- ✅ 真实 CLI 环境测试
- ✅ 严格评分
- ✅ 详细记录

### 质量检查点

- [ ] 每个 skill 都有测试记录
- [ ] 评分客观公正
- [ ] 改进建议具体
- [ ] 汇总报告完整

---

## 🔄 重启后继续

**如果重启 Qwen CLI**:

输入：
```
继续 Skill 真实环境测试计划。

当前测试进度：
- 已完成：{已测试的 skill}
- 当前测试：{当前 skill}
- 待测试：{待测试 skill}

请继续测试。
```

**系统会记住**:
- 已测试的 skill
- 当前测试进度
- 测试记录位置

---

## 🚀 开始测试

### 立即行动

**步骤 1**: 启动 Qwen CLI
```bash
qwen
```

**步骤 2**: 开始测试 grounded-theory-expert
```
你是 grounded-theory-expert 吗？请介绍一下你的角色和能力。
```

**步骤 3**: 提出复杂任务（见测试记录文件）

**步骤 4**: 观察并记录

**步骤 5**: 填写测试记录

---

## 📊 测试仪表板

查看实时进度：

```bash
notepad D:\socienceAI\agentskills\TEST-DASHBOARD.md
```

---

**测试准备就绪！**

**状态**: 🟡 部署完成，准备测试  
**下一步**: 启动 Qwen CLI，开始测试 grounded-theory-expert

*最后更新*: 2026-03-06
