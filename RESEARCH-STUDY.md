# Skill 设计概念研究报告

**研究日期**: 2026-03-03  
**研究者**: SocienceAI  
**状态**: ✅ 概念理解完成

---

## 📚 核心概念理解

### 1. 什么是 agentskills.io Skill？

**Skill 的本质**:
- Skill 是一个**标准化的分析工具包**，不是简单的 Node.js 模块
- 它是**独立可调用**的分析服务，可以被 AI agent 或人类用户调用
- 它遵循**统一的配置规范**（skill.yaml, schema.json）
- 它内置**planning-with-files 机制**支持长时间复杂任务

**Skill 的应用场景**:
1. **AI Agent 调用**: AI agent 通过标准接口调用 skill 执行专业分析
2. **人类用户使用**: 研究人员通过命令行或 API 使用 skill
3. **系统集成**: skill 可以集成到更大的分析平台中

---

### 2. Skill 的标准结构

根据审核文档，一个完整的 skill 应该包含：

```
skill-name/
├── skill.yaml                    # Skill 元数据和配置
│   - name, version, description
│   - inputs/outputs Schema 定义
│   - prompts 配置
│   - tools 配置
│   - planning_files 配置
├── schema.json                   # 输入输出验证 Schema
├── README.md                     # 使用说明
├── prompts/                      # 提示词模板目录
│   ├── system-prompt.md          # 系统提示词
│   ├── analysis-prompt.md        # 分析提示词
│   └── validation-prompt.md      # 验证提示词
├── tools/                        # 工具函数目录
│   ├── analysis-tool.py          # Python 工具
│   ├── visualization.js          # JavaScript 工具
│   └── planning-integration.py   # planning-with-files 集成
├── templates/                    # planning-with-files 模板
│   ├── task_plan.md              # 任务计划模板
│   ├── findings.md               # 发现记录模板
│   └── progress.md               # 进度日志模板
├── examples/                     # 示例输入输出
│   ├── input-example.json
│   └── output-example.json
└── tests/                        # 测试目录
    ├── unit-tests/
    └── integration-tests/
```

---

### 3. planning-with-files 机制

**核心理念**:
- 将**易失的上下文**（Context Window = RAM）保存到**持久的文件系统**（Disk）
- 支持**跨会话继续**执行长时间任务
- 提供**可追溯的分析过程**记录

**三个核心文件**:

#### task_plan.md - 任务计划
```markdown
# 任务计划

**任务 ID**: xxx
**研究问题**: xxx
**分析类型**: xxx

## 阶段规划
### Phase 1: 数据准备
- [ ] 数据匿名化
- [ ] 数据分段
- 状态：pending/in_progress/complete

### Phase 2: 分析执行
- [ ] 步骤 1
- [ ] 步骤 2

## 质量检查点
- [ ] Phase 1 完成：检查点 1
- [ ] Phase 2 完成：检查点 2

## 错误日志
| 错误 | 尝试次数 | 解决方案 |
|------|----------|----------|
```

#### findings.md - 发现记录
```markdown
# 研究发现

## Phase 1 发现
### 关键发现 1
{{discovery_1}}

### 关键发现 2
{{discovery_2}}

## Phase 2 发现
### 分析结果
{{results}}

## 数据引用
| 编号 | 原始数据 | 来源 |
|------|----------|------|
| D1 | "{{quote}}" | {{source}} |
```

#### progress.md - 进度日志
```markdown
# 进度日志

## Session 1 (2026-03-03)
**目标**:
- {{goal_1}}
- {{goal_2}}

**完成的工作**:
- [x] {{completed_1}}
- [x] {{completed_2}}

**下一步计划**:
- {{next_step}}

**会话时长**: {{duration}} 分钟
```

---

### 4. Skill 配置详解 (skill.yaml)

```yaml
name: skill-name
version: 1.0.0
description: |
  技能描述，包括方法论基础
  基于 Author (Year) 理论框架

author: SocienceAI
license: MIT
category: category-name
tags:
  - tag1
  - tag2

# 输入规范
inputs:
  - name: input_name
    type: string|number|array|object
    required: true|false
    description: 输入描述
    examples:
      - "示例值"

# 输出规范
outputs:
  - name: output_name
    type: object
    description: 输出描述
    schema:
      field1: type
      field2: type

# 提示词模板
prompts:
  system: prompts/system-prompt.md
  analysis: prompts/analysis-prompt.md
  validation: prompts/validation-prompt.md

# 工具函数
tools:
  - name: tool_name
    file: tools/tool.py
    runtime: python3|node
    description: 工具描述

# planning-with-files 配置
planning_files:
  - task_plan.md
  - findings.md
  - progress.md
```

---

### 5. 方法论严谨性要求

每个 skill 必须：

1. **遵循权威理论框架**
   - 明确说明方法论基础（如：Strauss & Corbin, 1990）
   - 区分不同理论流派（如：glaserian vs straussian vs constructivist）
   - 包含核心构念的完整定义

2. **标准化操作流程**
   - 完整的分析步骤
   - 每步有质量检查点
   - 错误处理和恢复机制

3. **可验证的输出**
   - 标准化的输出格式
   - 包含完整的分析过程记录
   - 支持审核追踪

4. **与权威软件对齐**
   - 功能对比专业软件（如 NVivo, Gephi, fs/QCA）
   - 达到或超越专业软件的分析质量

---

### 6. 我之前理解的偏差

❌ **错误理解**:
- Skill 是简单的 Node.js 模块
- 只需要实现功能代码
- planning-with-files 只是简单的文件模板
- 不需要严格的 schema 定义

✅ **正确理解**:
- Skill 是标准化的分析工具包
- 需要完整的配置（skill.yaml, schema.json）
- planning-with-files 是核心机制，需要深度集成
- 需要严格的输入输出 Schema 验证
- 需要提示词工程（prompts/）
- 需要工具函数层（tools/）
- 需要示例和测试

---

### 7. 重新实现的关键点

#### 7.1 skill.yaml 配置
- 必须定义完整的 inputs/outputs Schema
- 必须配置 prompts 路径
- 必须配置 tools 列表
- 必须配置 planning_files

#### 7.2 提示词工程
- system-prompt.md: 定义角色和方法论基础
- analysis-prompt.md: 定义分析步骤
- validation-prompt.md: 定义质量检查

#### 7.3 工具函数层
- Python 工具：用于统计分析、数据处理
- JavaScript 工具：用于可视化、交互
- planning-integration: 集成 planning-with-files

#### 7.4 planning-with-files 深度集成
- 不是简单的模板文件
- 需要在代码中实际读写这些文件
- 需要支持会话恢复
- 需要记录完整的分析过程

---

## 📋 重新实现清单

### 需要重新实现的 Skills:

1. **grounded-theory-expert** ❌ 需要重构
   - 缺少 schema.json
   - prompts/ 不完整
   - tools/ 缺失
   - planning-with-files 集成不够深入

2. **social-network-analysis-expert** ❌ 需要重构
   - 缺少 schema.json
   - prompts/ 不完整
   - tools/ 缺失
   - planning-with-files 集成不够深入

### 正确的实现顺序:

1. 设计 skill.yaml（包含完整 Schema）
2. 编写 prompts/（系统提示词、分析提示词、验证提示词）
3. 实现 tools/（Python/JavaScript工具函数）
4. 实现 planning-with-files 深度集成
5. 创建 examples/（输入输出示例）
6. 编写 tests/（单元测试、集成测试）

---

## 🎯 下一步行动

1. **停止当前实现** - 当前实现不符合规范
2. **重新设计 skill 架构** - 按照正确的结构
3. **从第一个 skill 开始重构** - grounded-theory-expert
4. **确保每个组件都符合规范** - skill.yaml, schema.json, prompts/, tools/

---

**研究完成**: 2026-03-03  
**理解置信度**: 95%  
**准备重构**: ✅ 是
