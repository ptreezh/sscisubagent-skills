---
name: pest-analysis-expert
description: |
  PEST/PESTEL environmental analysis expert. Provides six-dimensional macro-environment analysis, factor identification, impact assessment, and trend prediction. Suitable for strategic planning, market analysis, and environmental scanning.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

## 概述

PEST/PESTEL分析是最广泛使用的宏观环境分析工具，通过系统识别政治(Political)、经济(Economic)、社会(Social)、技术(Technological)、环境(Environmental)、法律(Legal)六大维度的环境因素，为战略决策提供外部环境洞察。

---

## 6大绝对禁止原则

```yaml
1. 禁止维度遗漏 - 必须分析所有六个维度（P/E/S/T/E/L）
2. 禁止因素空泛 - 每个因素必须具体、可描述
3. 禁止无证据 - 所有因素必须有数据或证据支撑
4. 禁止静态分析 - 必须考虑时间维度和趋势
5. 禁止忽视关联 - 必须分析维度间的交叉影响
6. 禁止脱离战略 - 因素必须与战略决策相关
```

---

## CRCT思维链（强制执行）

### C - Constant Comparison（持续比较）
比较不同维度因素的关联性和影响方向

### R - Record（记录）
记录因素名称、维度、描述、证据来源、影响评估

### C - Chain（链条）
建立因素间的关联链条，识别系统性风险和机会

### T - Trace（追踪）
追踪因素的历史变化和未来趋势

---

## PESTEL六维度框架

```
┌─────────────────────────────────────────────────────────────┐
│                     PESTEL分析框架                           │
├───────────────┬───────────────┬─────────────────────────────┤
│ P - Political │ E - Economic  │ 政策法规、宏观经济          │
│ 政治因素      │ 经济因素      │                              │
├───────────────┼───────────────┼─────────────────────────────┤
│ S - Social    │ T - Techno.   │ 人口文化、技术创新          │
│ 社会因素      │ 技术因素      │                              │
├───────────────┼───────────────┼─────────────────────────────┤
│ E - Environ.  │ L - Legal     │ 气候环境、法律合规          │
│ 环境因素      │ 法律因素      │                              │
└───────────────┴───────────────┴─────────────────────────────┘
```

---

## 分析流程

### 第一阶段：维度扫描
- 六维度系统扫描
- 使用标准检查清单
- 每维度至少3个因素

### 第二阶段：因素识别
- 具体化因素描述
- 收集证据支撑
- 确认因素分类

### 第三阶段：影响评估
- 影响程度评分（1-5）
- 发生概率评分（1-5）
- 时间紧迫性评估

### 第四阶段：交叉分析
- 维度间关联识别
- 关键关联链分析
- 系统性风险识别

### 第五阶段：战略启示
- 机会识别
- 威胁识别
- 战略建议提炼

---

## Planning-With-Files支持

自动创建：task_plan.md、progress.md、findings.md

## CLI原生集成

- 任务队列支持
- 三层状态持久化
- 子Agent并行支持

---

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | pestel_identifier.py | PESTEL六维度因素识别与评估 |

### CLI用法

```bash
python tools/pestel_identifier.py --input data.txt --output pestel_factors.json
python tools/pestel_identifier.py --help
```

## 参考资料

- [经典文献](references/classic-literature.md)
- [详细指南](references/detailed-guide.md)
- [成功案例](cases/positive/)
- [失败案例](cases/negative/)
- [经验模式](experience/patterns.md)

---

## 参考文献

1. Aguilar, F.J. (1967). *Scanning the Business Environment*. Macmillan.
2. Johnson, G., & Scholes, K. (1989). *Exploring Corporate Strategy*. Prentice Hall.
3. Fahey, L., & Narayanan, V.K. (1986). *Macroenvironmental Analysis for Strategic Management*. West Publishing.

---

**技能版本**: 5.0.0-cli-native+agent
**方法论严谨性**: 0%妥协
**创建时间**: 2026-03-15