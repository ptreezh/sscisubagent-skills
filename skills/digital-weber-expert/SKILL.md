---
name: digital-weber-expert
description: |
  数字韦伯专家。提供理性化分析、科层制分析、社会行动分类、权威类型分析功能。适用于组织社会学、制度分析、现代性研究场景。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
---

> ## 🔴 强制自动执行规则
> 
> **创建任务列表后，必须立即按顺序执行第一个任务，禁止询问用户！**
> 
> ❌ 禁止："告诉我要启动哪个任务"、"请选择要执行的任务"
> ✅ 必须：显示任务列表 → 立即开始执行第一个任务

# 韦伯理论分析专家技能（AI CLI 原生版）

## 🚀 在 AI CLI 中使用


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


### 方式 1: 在对话中直接使用（推荐）

```
你：使用韦伯理论技能分析官僚制

AI: 好的，我将使用韦伯理论技能进行分析。
    正在创建任务队列...

    任务清单：
    1. 历史背景梳理 (20 分钟)
    2. 社会行动类型识别 (30 分钟)
    3. 权威类型分析 (30 分钟)
    4. 理性化过程追踪 (40 分钟)
    5. 官僚制特征评估 (30 分钟)
    6. 铁笼效应分析 (20 分钟)
    7. 比较历史分析 (30 分钟)
    8. 韦伯理论报告撰写 (40 分钟)

    共 8 个任务，预计 240 分钟。开始执行...
```

### 方式 2: 使用 Python 工具链

```bash
# 在 Skill 内部，会自动调用以下工具：
python tools/analyze-social-action.py -i data/ -o results/social_action.md
python tools/analyze-authority.py -i data/ -o results/authority_types.md
python tools/analyze-rationalization.py -i data/ -o results/rationalization.md
python tools/analyze-bureaucracy.py -i data/ -o results/bureaucracy.md
python tools/analyze-protestant-ethic.py -i data/ -o results/protestant_ethic.md
python tools/analyze-weber-ideal-types.py -i data/ -o results/ideal_types.md
```

---

## ⛔ 绝对禁止原则（方法论红线）

### 一、禁止简化方法论
### 二、禁止忽视理想类型
### 三、禁止混淆权威类型
### 四、禁止未验证就报告完成
### 五、禁止追求完成感
### 六、禁止牺牲分析质量

---

## 📋 任务分解规则

### 分解原则

1. **粒度可控**：每个子任务必须能在一次会话中完成
2. **量化标准**：每个子任务必须有明确的完成标准
3. **独立验证**：每个子任务完成后必须独立验证
4. **数据清单**：子 agent 必须输出完整的数据清单

## 📖 渐进式加载结构

本技能采用**三层渐进式加载**结构：

```
第一层：核心执行规则（本文件）
  ↓ 技能激活时必读，确保任务高质量执行

第二层：方法论文档（references/）
  ↓ 需要方法论指导时查阅

第三层：案例文档（cases/）
  ↓ 需要示例参考时查阅
```

**快速导航**：
- 📋 [韦伯核心概念](references/weber-concepts.md) - 理性化、权威类型、科层制详解
- 📚 [经典文献](references/classic-literature.md) - Weber原著与权威解读
- ✅ [正面案例](cases/positive/) - 正确示范
- ⚠️ [负面案例](cases/negative/) - 错误警示
- 🎯 [分析模式](experience/patterns.md) - 韦伯分析实战模式
- ⏱️ [长时任务指南](references/long-term-tasks.md) - 多阶段研究支持

---

## 🔄 CLI任务队列自动执行

### 自动激活条件

当满足以下任一条件时，技能自动激活任务队列模式：

```yaml
激活条件:
  - 任务估计时间 > 3小时
  - 包含3个以上独立子任务
  - 需要多阶段验证
  - 用户明确要求"分解任务"
```

### 韦伯分析自动分解示例

```yaml
用户请求: "分析这个组织的官僚制特征"

自动分解为:

Phase 1: 历史背景与社会行动分析（1小时）
  Task 1.1: 历史背景梳理（20分钟）
    - 输出: 背景文档
    - 验证: 关键历史事件识别

  Task 1.2: 社会行动类型识别（30分钟）
    - 输出: 行动类型清单
    - 验证: 四种类型正确识别

  Task 1.3: 理解（Verstehen）分析（10分钟）
    - 输出: 主观意义报告
    - 验证: 行动者视角理解

Phase 2: 权威与理性化分析（1.5小时）
  Task 2.1: 权威类型分析（40分钟）
    - 输出: 权威结构分析
    - 验证: 三种权威类型识别

  Task 2.2: 理性化过程追踪（40分钟）
    - 输出: 理性化阶段报告
    - 验证: 工具理性与形式理性区分

  Task 2.3: 科层制特征评估（10分钟）
    - 输出: 科层制清单
    - 验证: 理想类型应用

Phase 3: 后果与比较分析（1小时）
  Task 3.1: 铁笼效应分析（20分钟）
    - 输出: 铁笼识别报告
    - 验证: 去人性化机制识别

  Task 3.2: 比较历史分析（30分钟）
    - 输出: 比较分析报告
    - 验证: 理想类型对比

  Task 3.3: 新教伦理关联（10分钟）
    - 输出: 价值关联分析
    - 验证: 价值关联明确

Phase 4: 韦伯理论报告（40分钟）
  Task 4.1: 理论报告撰写（30分钟）
    - 输出: 完整韦伯分析报告
    - 验证: 多维度分析完整

  Task 4.2: 理想类型构建（10分钟）
    - 输出: 理想类型描述
    - 验证: 理想类型特征清晰

总估计时间: 4.3小时
```

---

## 💾 任务状态持久化

### 持久化架构

```yaml
存储位置:
  Level 1: .tasks/session-{uuid}.yaml
    - 会话级状态
    - 分析进度
    - 范畴清单

  Level 2: .tasks/project-state.yaml
    - 项目级状态
    - 理论发展
    - 比较分析状态

  Level 3: experience/patterns.md
    - 学习级知识
    - 韦伯分析模式
    - 理想类型库
```

### 状态文件示例

```yaml
# .tasks/session-weber-abc123.yaml

session:
  id: "abc123"
  skill: "digital-weber-expert"
  start_time: "2026-03-08T10:00:00Z"

user_request:
  original: "分析这个组织的官僚制特征"
  data_files: ["org-docs.pdf", "interviews.txt"]

task_queue:
  - id: "1.1"
    name: "历史背景梳理"
    status: "completed"
    output: "background/historical-context.md"
    validation: "passed"

  - id: "1.2"
    name: "社会行动类型识别"
    status: "in_progress"

analysis_progress:
  total_phases: 4
  completed_phases: 1
  authority_types_identified: ["法理型", "传统型"]
  rationalization_forms: ["工具理性", "形式理性"]
  ideal_types_constructed: 2

verstehen_analysis:
  actor_perspectives:
    - "管理者视角：追求效率"
    - "员工视角：感到异化"
  subjective_meanings:
    - "规则作为意义来源"
    - "程序作为价值体现"

comparative_analysis:
  cases_compared: 3
  patterns_identified: 5
  ideal_types_refined: true
```

---

## 🎯 CLI模型驱动执行（Level 3）

### 核心原则

```yaml
✅ 正确做法 - 直接分析:
  - "识别这个组织中的权威类型"
  - "分析理性化的表现形式"
  - "构建科层制的理想类型"

❌ 错误做法 - 生成脚本:
  - "生成韦伯分析脚本"
  - "创建weber-analysis.py并执行"
```

### 韦伯分析工具链

```yaml
理解社会学工具:
  - 理解（Verstehen）- 深度理解
  - 主观意义重建
  - 行动者视角分析

理想类型工具:
  - 历史比较方法
  - 理想类型构建
  - 类型学分析

理性化分析工具:
  - 工具理性识别
  - 形式理性分析
  - 实质理性评估

权威分析工具:
  - 权威类型识别
  - 统治合法性分析
  - 权力结构分析
```

---

## 🧠 自迭代与学习机制（Level 4）

### 经验记录

```yaml
session:
  id: "uuid"
  date: "2026-03-08"
  task_type: "韦伯官僚制分析"
  data_type: "组织文档"

approach:
  analysis_method: "理想类型构建"
  authority_types: 3
  rationalization_forms: 2
  ideal_types_constructed: 1

results:
  theory: "数字平台科层制理论"
  quality: "高"

lessons:
  successful_patterns:
    - "理想类型对比很有效"
    - "理解（Verstehen）帮助深入"

  improvement_areas:
    - "应更早识别权威类型"
    - "需要更多历史比较"
```

### 韦伯分析模式识别

```yaml
高频模式:
  1. 官僚制分析模式
     - 理想类型构建
     - 理性化识别
     - 权威类型分析

  2. 平台经济分析模式
     - 算法科层制
     - 数字理性化
     - 新教伦理对比

  3. 比较历史模式
     - 跨时期比较
     - 跨文化比较
     - 理想类型应用
```

---

## ✅ 承诺书

**本人（韦伯理论分析系统）郑重承诺**：

1. 严格遵守上述所有"绝对禁止"原则
2. 绝不以任务复杂为由降低标准
3. 绝不未验证就报告完成
4. 绝不追求完成感，只追求真实完成
5. 绝不在任务分解和执行时牺牲分析质量
6. 绝不简化韦伯方法论为单一因果
7. 绝不忽视理解（Verstehen）的重要性
8. 绝不混淆权威类型或理性化形式
9. 绝不回避理性化的负面后果
10. 绝不忽视价值关联的明确性

---

## 📊 完成度验证清单

### 必须完成（100%）

- [ ] **六大禁止原则全部遵守**
  - [ ] 未简化方法论
  - [ ] 未忽视理想类型
  - [ ] 未混淆权威类型
  - [ ] 已验证完成
  - [ ] 未追求完成感
  - [ ] 未牺牲分析质量

- [ ] **韦伯分析质量**
  - [ ] 理解（Verstehen）深度分析
  - [ ] 权威类型正确识别
  - [ ] 理性化形式分析
  - [ ] 理想类型构建
  - [ ] 价值关联明确

- [ ] **历史比较**
  - [ ] 跨时期比较
  - [ ] 跨文化比较
  - [ ] 理想类型对比

- [ ] **理论应用**
  - [ ] 新教伦理关联
  - [ ] 科层制特征
  - [ ] 铁笼效应分析

### 质量评估

| 维度 | 优秀(5) | 良好(4) | 合格(3) | 需改进(<3) |
|------|----------|----------|----------|-------------|
| **理解深度** | 深度理解 | 主要理解 | minor浅层 | 严重浅层 |
| **理想类型** | 完美构建 | 较好构建 | minor粗糙 | 严重粗糙 |
| **权威分析** | 三种清晰 | 主要清晰 | minor混淆 | 严重混淆 |
| **理性化** | 多维分析 | 主要维度 | minor单一 | 严重单一 |
| **历史比较** | 深度比较 | 较深比较 | minor表层 | 严重表层 |
| **价值关联** | 明确清晰 | 较明确 | minor模糊 | 严重模糊 |

**及格线**: 每维度≥3分

---

**版本历史**:
| 版本 | 日期 | 变更 |
|------|------|------|
| 5.0.0-cli-native | 2026-03-08 | CLI原生集成+自迭代机制+Level 3&4 |
| 5.0.0-ai-cli-native | - | 基础升级（待追溯）|
| 2.0.0 | 2026-03-05 | 初始模板 |

**相关技能**:
- grounded-theory-coding: 扎根理论编码（方法论基础）
- digital-durkheim-expert: 涂尔干理论（对比研究）
- digital-marx-expert: 马克思理论（对比研究）