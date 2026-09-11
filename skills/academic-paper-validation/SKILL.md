---
name: academic-paper-validation
description: |
  Academic paper validation expert. Provides systematic peer review, methodology assessment, statistical verification, citation analysis, and publication readiness evaluation. Suitable for academic research, journal submission, and quality assurance.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

metadata:
  version: "1.0.0-cli-native+agent"
  methodology: "Academic Paper Validation Protocol"
  absolute-prohibitions: true
  task-decomposition-rules: true
  ai-cli-native: true
  task-queue-support: true
  agentskills-io: true
  cross-platform: true
  state-persistence: true
  self-iteration: true
  academic-alignment: true
  subagent-support: true
  graceful-fallback: true
  created: "2026-03-23"
  updated: "2026-03-23"
  author: "SocienceAI Academic Expert"
  license: "MIT"

  execution_modes:
    cli_queue: "CLI任务队列（基础）"
    subagent_parallel: "子Agent并行（增强）"

  performance:
    sequential: "20-40分钟/论文"
    parallel: "45分钟/论文（含多专家评审）"
---

## 基本信息

**名称**: academic-paper-validation (学术论文验证专家)
**版本**: 1.0.0
**作者**: SocienceAI Academic Expert
**许可证**: MIT

## 描述

**学术论文验证专家** - 支持**多专家评审**和**投稿前核验**的论文质量保障技能。

## 🖥️ 项目初始化（跨平台Python脚本）

### 使用Python创建项目目录

```python
import os

# 设置项目路径
project_path = r"D:\your_project_path\论文验证"  # Windows
# project_path = "/home/user/paper_validation"  # Linux/macOS

# 创建标准目录结构（跨平台兼容）
for subdir in ['.tasks', 'manuscript', 'reviews', 'reports', 'logs']:
    os.makedirs(os.path.join(project_path, subdir), exist_ok=True)

print(f"项目目录创建完成: {project_path}")
```

### 目录结构

```
论文验证/
├── .tasks/           # 验证任务状态
├── manuscript/       # 稿件文件
├── reviews/          # 评审记录
├── reports/          # 验证报告
└── logs/             # 日志
```

## 核心能力

### 1. 参考文献验证 (Reference Validation)
- 引用准确性检查
- 引用格式合规检查
- 引用完整性检查
- 原文对照验证

### 2. 数据可重复性检查 (Reproducibility Check)
- 数据可用性声明检查
- 代码/数据共享检查
- 方法描述完整性检查
- 统计分析可验证性检查

### 3. 格式合规检查 (Format Compliance)
- 期刊格式要求对照
- 字数/页数限制检查
- 图表格式检查
- 参考文献格式检查

### 4. 学术伦理检查 (Ethics Check)
- 抄袭检测准备
- 作者贡献声明检查
- 利益冲突声明检查
- 伦理审批检查

### 5. 多专家评审 (Multi-Expert Review)
- 文献专家评审
- 方法论专家评审
- 领域专家评审
- 评审意见整合

## ⚠️ 六大绝对禁止原则

### 1. 禁止忽视引用验证

**错误做法**:
```yaml
引用问题:
  - 假设引用准确无误
  - 不核对原文内容
  - 忽略引用格式错误
  - 遗漏必要引用

后果:
  - 学术不端风险
  - 论文被拒
  - 撤稿风险
```

**正确做法**:
```yaml
引用验证:
  Step 1: 逐条核对原文
    - 确认引用内容准确
    - 确认页码/年份正确
    - 确认作者姓名正确

  Step 2: 格式合规检查
    - 符合期刊引用格式
    - 信息完整无遗漏
    - 排序正确

  Step 3: 完整性检查
    - 文中引用与文献列表一致
    - 无遗漏必要引用
    - 无过度自引
```

### 2. 禁止跳过数据核验

**错误做法**:
```yaml
数据问题:
  - 假设数据准确
  - 不检查计算可重复性
  - 忽略数据来源说明
  - 缺失数据可用性声明

后果:
  - 可重复性危机
  - 论文可信度受损
  - 撤稿风险
```

**正确做法**:
```yaml
数据核验:
  Step 1: 原始数据核查
    - 数据来源可追溯
    - 数据处理步骤清晰
    - 异常值处理合理

  Step 2: 分析可重复性
    - 统计方法正确
    - 计算步骤可重现
    - 结果与数据一致

  Step 3: 数据可用性声明
    - 数据公开位置明确
    - 访问方式清晰
    - 符合期刊要求
```

### 3. 禁止无证据的完成声明

**错误做法**:
```yaml
草率完成:
  - 声称"验证完成"但无记录
  - 未实际执行检查
  - 无验证报告输出
  - 跳过必要步骤

后果:
  - 隐藏问题未发现
  - 投稿后被拒
  - 浪费时间和资源
```

**正确做法**:
```yaml
验证完成标准:
  Step 1: 执行所有检查项
    - 每项检查有记录
    - 问题有标注
    - 修复有验证

  Step 2: 生成验证报告
    - 检查项清单
    - 通过/未通过状态
    - 问题修复建议

  Step 3: 完成确认
    - 所有Critical问题已解决
    - 报告已完成
    - 可追溯记录存在
```

### 4. 禁止声称"超越"某理论而不了解其贡献

**错误做法**:
```yaml
理论声称:
  - 声称"超越Bourdieu"
  - 但不了解Bourdieu理论
  - 声称"改进ANT"
  - 但不了解ANT贡献

后果:
  - 理论漏洞明显
  - 被审稿人质疑
  - 学术声誉受损
```

**正确做法**:
```yaml
理论定位:
  Step 1: 深入了解已有理论
    - 阅读核心文献
    - 理解关键概念
    - 明确理论边界

  Step 2: 明确差异点
    - 列出具体差异
    - 说明创新之处
    - 承认继承关系

  Step 3: 精确表述
    - 使用"扩展"而非"超越"
    - 说明具体贡献
    - 提供证据支持
```

### 5. 禁止不满足语言要求就声称可投稿

**错误做法**:
```yaml
语言问题:
  - 中文论文声称可投英文期刊
  - 未检查语言质量
  - 忽略翻译准确性
  - 无母语润色

后果:
  - 立即被拒
  - 审稿人负面印象
  - 浪费投稿机会
```

**正确做法**:
```yaml
语言准备:
  Step 1: 确认目标期刊语言要求
    - 英文期刊需英文稿件
    - 中文期刊需中文稿件
    - 双语期刊需确认

  Step 2: 语言质量检查
    - 语法检查
    - 术语准确性
    - 表达清晰度

  Step 3: 完成确认
    - 语言版本已准备
    - 质量已验证
    - 方可声称"可投稿"
```

### 6. 禁止不调用领域专家而声称全面验证

**错误做法**:
```yaml
验证问题:
  - 仅依赖通用验证工具
  - 不调用领域专家
  - 声称"通用AI可以验证所有学科论文"
  - 忽视学科特殊规范

后果:
  - 方法论错误未被发现
  - 领域知识错误被忽略
  - 论文可信度受损
```

**正确做法**:
```yaml
全面验证:
  Step 1: 通用验证
    - 引用格式检查
    - 数据可重复性检查
    - 格式合规检查

  Step 2: 领域专家验证
    - 调用对应方法论专家
    - 调用领域知识专家
    - 双重验证

  Step 3: 综合评估
    - 整合所有专家意见
    - 区分Critical/Major/Minor问题
    - 所有Critical问题解决后方可声称"全面验证"
```

## 验证流程

### Phase 1: 预检查 (Pre-Check)
- 目标期刊确认
- 格式要求对照
- 必备材料清单

### Phase 2: 引用验证 (Reference Validation)
- 逐条核对原文
- 格式合规检查
- 完整性检查

### Phase 3: 数据核验 (Data Verification)
- 数据来源核查
- 分析可重复性
- 可用性声明检查

### Phase 4: 多专家评审 (Multi-Expert Review)
- 文献专家评审
- 方法论专家评审
- 领域专家评审
- 评审意见整合

### Phase 5: 修复验证 (Fix Verification)
- Critical问题修复确认
- Major问题修复确认
- 最终质量评分

### Phase 6: 完成确认 (Completion Confirmation)
- 验证报告生成
- 投稿建议
- 风险提示

## 适用场景

- ✅ 学术论文投稿前核验
- ✅ 参考文献准确性检查
- ✅ 数据可重复性验证
- ✅ 多专家评审组织
- ✅ 期刊格式合规检查
- ✅ 学术伦理合规检查

## 质量标准

| 维度 | 标准 | 检查方法 |
|------|------|----------|
| 引用准确性 | 100% | 逐条核对原文 |
| 数据可重复性 | ≥90% | 独立重现分析 |
| 格式合规性 | 100% | 期刊模板对照 |
| 专家评审通过率 | ≥80% | 多专家独立评审 |
| Critical问题解决率 | 100% | 修复后验证 |

## 使用示例

### 快速核验
```
用户: 帮我验证这篇论文的引用
技能: 执行引用验证流程
  1. 提取所有引用
  2. 逐条核对原文
  3. 检查格式合规
  4. 生成验证报告
```

### 完整验证
```
用户: 这篇论文准备投稿，请进行全面验证
技能: 执行完整验证流程
  Phase 1: 预检查
  Phase 2: 引用验证
  Phase 3: 数据核验
  Phase 4: 多专家评审
  Phase 5: 修复验证
  Phase 6: 完成确认
```

## 与其他技能的协作

- **grounded-theory-expert**: 扎根理论论文的方法论验证
- **actor-network-analysis-expert**: ANT论文的理论准确性验证
- **bourdieu-field-analysis-expert**: 布迪厄理论论文的概念验证

## 🖥️ Python 工具

> 当前版本暂无独立的Python工具文件。学术验证功能在AI CLI中通过结构化分析流程实现。

## 核心教训（来自GFT论文投稿案例）

1. **绝不声称"准备完成"或"可以投稿"**，除非完成全部核验
2. **必须调用领域专家**进行深度评审
3. **核心概念必须与原著精确对齐**，不能想当然
4. **目标期刊语言要求必须首先满足**
5. **声称"超越"某理论时必须精确说明差异点**
6. **任何"完成"声明前必须回答：如果我是最严苛的审稿人，会给出什么致命批评？**

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | paper_validator.py | 学术论文结构验证（摘要/引言/方法/结果/讨论） |
| 2 | citation_checker.py | 引用格式检查（APA/GB/T 7714） |
| 3 | format_normalizer.py | 格式标准化（字体/行距/图表规范） |

### CLI用法

```bash
# 验证论文结构
python tools/paper_validator.py --file paper.pdf

# 检查引用格式
python tools/citation_checker.py --ref-file references.bib

# 标准化格式
python tools/format_normalizer.py --input draft.docx --style gbt7714
```