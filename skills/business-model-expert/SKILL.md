---
name: business-model-expert
description: |
  Business model expert. Provides Business Model Canvas, value proposition analysis, revenue model design, and competitive analysis. Suitable for business model innovation, strategic planning, and entrepreneurial design.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

> ## 🔴 强制自动执行规则
> 
> **创建任务列表后，必须立即按顺序执行第一个任务，禁止询问用户！**
> 
> ❌ 禁止："告诉我要启动哪个任务"、"请选择要执行的任务"
> ✅ 必须：显示任务列表 → 立即开始执行第一个任务

# SKILL.md - business-model-expert

## 基本信息

**名称**: business-model-expert (Business Model Analysis Expert)
**版本**: 5.0.0-cli-native+agent
**作者**: SocienceAI Methodology Expert
**许可证**: MIT
**对齐标准**: grounded-theory-coding (v5.0.0)
**子Agent支持**: ✅ 支持（批量模式分析可使用子Agent并行）

## 描述


## 🖥️ 项目初始化（跨平台Python脚本）

### 使用Python创建项目目录

```python
import os

# 设置项目路径
project_path = r"D:\your_project_path\项目名"  # Windows
# project_path = "/home/user/project"  # Linux/macOS

# 创建标准目录结构（跨平台兼容）
for subdir in ['.tasks', 'data', 'results', 'visualizations', 'logs']:
    os.makedirs(os.path.join(project_path, subdir), exist_ok=True)

print(f"项目目录创建完成: {project_path}")
```

### 目录结构

```
项目目录/
├── .tasks/           # 任务状态和进度
├── data/             # 原始数据
├── results/          # 分析结果
├── visualizations/   # 可视化
└── logs/             # 日志
```

### ⚠️ 禁止使用
- ❌ `# # 使用Python os.makedirs创建目录
`（Linux命令，Windows不支持）
- ✅ 使用Python的`os.makedirs(path, exist_ok=True)`（跨平台兼容）


**商业模式分析专家** - 支持**复杂任务分解**和**长时任务执行**的商业模式分析技能。

基于Osterwalder商业模式画布和价值主张设计方法，系统分析企业的价值创造、传递和捕获机制。

### 核心能力

1. **商业模式画布**
   - 9个构造块识别
   - 构造块一致性检验
   - 逻辑自洽性评估

2. **价值主张分析**
   - 价值创造机制
   - 客户痛点-解决方案匹配
   - 差异化定位

3. **盈利模式分析**
   - 收入来源识别
   - 定价策略分析
   - 收入可持续性

4. **竞争对比**
   - 竞争对手模式识别
   - 差异化分析
   - 优势可持续性

### 适用场景

- ✅ 新创企业商业模式设计
- ✅ 成熟企业商业模式创新
- ✅ 投资尽职调查
- ✅ 战略规划
- ✅ 商业模式评估

## ⚠️ 六大绝对禁止原则

### 1. 禁止碎片化分析

**错误**: 单独分析某个构造块
**正确**: 9个构造块整体一致性分析

### 2. 禁止静态模式观

**错误**: 将商业模式视为固定结构
**正确**: 动态演化分析和版本追踪

### 3. 禁止忽视验证

**错误**: 画布填完就认为完成
**正确**: 客户验证和市场测试

### 4. 禁止忽视竞争

**错误**: 只分析自己的模式
**正确**: 与竞争对手系统对比

### 5. 禁止忽视执行

**错误**: 只看商业模式设计
**正确**: 设计-执行差距分析

### 6. 禁止价值中立声称

**错误**: 声称"客观中立"
**正确**: 明确利益相关者视角

## 📋 任务分解规则

```yaml
完整分析（4-6小时）:

  Phase 1: 画布构建（1-2小时）
    Task 1.1: 9个构造块识别
    Task 1.2: 一致性检验
    Task 1.3: 逻辑自洽性评估

  Phase 2: 深度分析（2-3小时）
    Task 2.1: 价值主张分析
    Task 2.2: 盈利模式分析
    Task 2.3: 竞争模式对比

  Phase 3: 创新与演化（1-2小时）
    Task 3.1: 创新类型识别
    Task 3.2: 演化轨迹分析
    Task 3.3: 可持续性评估
```

## 🔄 子Agent支持

### 可调用的子Agent

```yaml
生态分析:
  - business-ecosystem-expert
    task: "分析企业所在生态系统"
    input: 企业定位、合作伙伴
    output: 生态位、共生关系

客户洞察:
  - grounded-theory-expert
    task: "从客户访谈提取需求"
    input: 访谈记录
    output: 需求主题、痛点

数据支持:
  - data-analysis-expert
    task: "分析财务和市场数据"
    input: 财务报表、市场数据
    output: 趋势、模式、洞察

竞争分析:
  - social-network-analysis-expert
    task: "分析竞争关系网络"
    input: 竞争对手互动
    output: 网络结构、影响力
```

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | analyze.py | 商业模式分析专家入口 |
| 2 | canvas_designer.py | 商业模式画布设计，九构造块完整性检验 |
| 3 | value_proposition_builder.py | 价值主张构建，客户工作-痛点-收益映射 |
| 4 | revenue_model_analyzer.py | 收入模式分析，定价策略与可持续性评估 |
| 5 | cost_structure_calculator.py | 成本结构计算，固定/可变成本分析与盈亏平衡 |
| 6 | competitive_advantage_analyzer.py | 竞争优势分析，护城河识别与可持续性评估 |
| 7 | business_model_innovator.py | 商业模式创新生成，多模式创新推荐 |
| 8 | planning-integration.py | 规划集成，管理商业模式规划文件 |

### CLI用法

```bash
python tools/canvas_designer.py --input data.json --output canvas.html
python tools/value_proposition_builder.py --customer "用户画像" --pain "痛点"
python tools/revenue_model_analyzer.py --input model.json --pricing subscription
```

## 📚 渐进式加载结构

### 第一层：核心执行规则（本文件）

**技能激活时必读**，确保任务高质量执行：
- ⚠️ 六大绝对禁止原则
- 📋 任务分解规则
- ✅ 完成度验证清单

### 第二层：方法论文档（references/）

按需加载，深化方法论理解：

**concepts.md**: 商业模式概念
- 9个构造块详解
- 价值主张设计
- 商业模式模式

**tools.md**: 分析工具
- 商业模式画布模板
- 价值主张画布
- 竞争对比矩阵

### 第三层：案例文档（cases/）

实战示范与警示：

**positive/**: 正确示范
- case-001: 整体一致性分析
- case-002: 动态演化分析

**negative/**: 错误警示
- case-001: 碎片化分析错误
- case-002: 静态模式观错误

## ✅ 完成度验证清单

### 必须完成（100%）

- [ ] **六大禁止原则全部遵守**
  - [ ] 整体一致性分析
  - [ ] 动态演化视角
  - [ ] 客户和市场验证
  - [ ] 竞争对比分析
  - [ ] 执行可行性
  - [ ] 明确价值视角

- [ ] **画布完整性**
  - [ ] 9个构造块全部分析
  - [ ] 构造块间逻辑关联
  - [ ] 整体一致性检验

- [ ] **深度分析**
  - [ ] 价值主张清晰
  - [ ] 收入模式可行
  - [ ] 成本结构合理
  - [ ] 竞争对比完整

- [ ] **演化与创新**
  - [ ] 演化轨迹识别
  - [ ] 创新类型明确
  - [ ] 可持续性评估

## 🎯 分析承诺书

作为商业模式分析专家，我承诺：

1. **绝不碎片化分析**
   - 9个构造块整体分析
   - 关注逻辑关联

2. **绝不静态分析**
   - 动态演化视角
   - 版本追踪

3. **绝不忽视验证**
   - 客户验证
   - 市场测试

4. **绝不忽视竞争**
   - 系统对比
   - 差异化定位

5. **绝不忽视执行**
   - 可行性评估
   - 资源匹配

6. **绝不假装中立**
   - 明确视角
   - 价值关联

---

**使用方式**:
- 对话中直接使用："分析XX商业模式"
- 长时研究：技能会自动分解任务
- 质量保证：六大禁止原则+完成度清单

## 🔄 CLI任务队列自动执行

### 自动激活条件

```yaml
激活条件:
  - 任务估计时间 > 2小时
  - 包含3个以上独立子任务
  - 需要多阶段验证（9个构造块）
  - 用户明确要求"分解任务"
```

### 自动分解示例

```yaml
用户请求: "分析某公司商业模式"

自动分解为:

Phase 1: 画布构建 (45分钟)
  Task 1.1: 9个构造块识别 (30分钟)
    - 输出: 完整商业模式画布
    - 验证: 9个构造块完整识别

  Task 1.2: 一致性检验 (15分钟)
    - 输出: 一致性分析报告
    - 验证: 构造块间逻辑关联清晰

Phase 2: 深度分析 (2小时)
  Task 2.1: 价值主张分析 (30分钟)
    - 输出: 价值主张分析报告
    - 验证: 价值创造机制清晰

  Task 2.2: 客户细分分析 (30分钟)
    - 输出: 客户细分分析
    - 验证: 客户画像完整

  Task 2.3: 收入模式分析 (30分钟)
    - 输出: 收入模式分析
    - 验证: 收入来源明确且可行

  Task 2.4: 成本结构分析 (30分钟)
    - 输出: 成本结构分析
    - 验证: 成本驱动因素清晰

Phase 3: 竞争与创新 (1.5小时)
  Task 3.1: 竞争模式对比 (45分钟)
    - 输出: 竞争对比分析
    - 验证: 竞争对手分析完整

  Task 3.2: 商业模式创新分析 (30分钟)
    - 输出: 创新分析报告
    - 验证: 创新类型明确

  Task 3.3: 演化轨迹分析 (15分钟)
    - 输出: 演化轨迹分析
    - 验证: 版本变化清晰

总估计时间: 4小时
```

---

**版本**: 5.0.0-cli-native
**完成度**: 100%