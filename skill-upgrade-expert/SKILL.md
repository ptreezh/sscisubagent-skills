---
name: skill-upgrade-expert
description: |
  技能升级专家。提供技能诊断、优化建议、子Agent集成、性能评估功能。适用于AI技能开发、技能标准化、质量提升场景。
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



# 技能升级专家 (Skill Upgrade Expert)

**版本**: 5.0.0-cli-native+agent
**方法**: "提升技能的技能" (The Skill of Upgrading Skills)
**最后更新**: 2026-03-14

---

## 技能概述

本技能提供系统化的方法论，用于将AI CLI技能从任意版本升级到v5.0.0-cli-native标准。该方法论已在14个研究方法技能上验证成功，实现100%完成率和5/5平均质量。

支持两种执行模式：
- **CLI任务队列模式**：单技能升级，串行处理，稳定可靠
- **子Agent并行模式**：批量升级，5-10x加速，自动降级保证

---

## 元数据

```yaml
metadata:
  version: "5.0.0-cli-native+agent"
  methodology: "提升技能的技能"
  domain: "技能开发/元技能"
  category: "meta-skill"
  subagent-support: true
  graceful-fallback: true
  ai-cli-native: true

  capabilities:
    - 系统化技能升级
    - 四级升级路径
    - CLI原生集成
    - 自迭代机制
    - 质量保证
    - 批量并行处理

  validated: true
  success_rate: "100%"
  case_count: 14
  avg_quality: "5/5"

  dependencies:
    - agentskills-io: true
    - task-queue-support: true
    - state-persistence: true
```

---

## 核心方法论

### 四级升级路径

#### Level 1: 基础升级 (Basic Upgrade)

**目标**: 建立质量基线

**核心内容**:
1. **6大绝对禁止原则** - 针对每个技能的特定化
2. **任务分解规则** - 系统化的任务拆解方法
3. **完成度验证清单** - 质量保证机制

**交付物**:
- SKILL.md (包含6大禁止)
- 基础目录结构

**时间**: 30分钟/技能

**质量门**:
- [ ] 6大禁止原则已定制化并文档化
- [ ] 任务分解规则已定义
- [ ] SKILL.md基础结构完整
- [ ] 目录结构符合标准

#### Level 2: 学术对齐 (Academic Alignment)

**目标**: 建立学术权威性

**核心内容**:
1. **经典文献** - 该领域权威文献
2. **权威定义** - 核心概念的学术定义
3. **应用范围** - 方法论的适用边界
4. **案例支撑** - 真实案例验证

**交付物**:
- references/classic-literature.md
- references/concepts.md (如需要)
- cases/positive/ (至少1个完整案例)

**时间**: 1小时/技能

**质量门**:
- [ ] 经典文献已引用（至少3篇）
- [ ] 核心概念已定义
- [ ] 至少1个成功案例
- [ ] 应用范围已明确

#### Level 3: CLI原生集成 (CLI-Native Integration)

**目标**: 深度集成CLI环境

**核心内容**:
1. **任务队列自动执行** - CLI任务队列支持
2. **状态持久化** - 三层持久化机制
3. **模型驱动执行** - 不是脚本生成，而是模型直接调用

**交付物**:
- skill.yaml (完整配置)
- SKILL.md (添加Level 3章节)
- tools/ (如需要)
- templates/task_plan.md.template
- subagents.yaml (可选)

**时间**: 30分钟/技能

**质量门**:
- [ ] CLI任务队列支持已添加
- [ ] 状态持久化机制已实现
- [ ] 模型驱动执行已配置
- [ ] 工具集成已完成

#### Level 3+: 子Agent增强（可选）

**目标**: 支持复杂任务的并行处理

**何时需要**:
- 批量处理（>5个独立任务）
- 大规模分析（总时间>1小时）
- 需要显著加速（5-10x）

**核心原则**（重要）:
1. **渐进式信息披露** - 用户通常不需要知道子Agent的存在
2. **向后完全兼容** - 不破坏现有CLI队列功能
3. **按需自动加载** - 仅在必要时启用子Agent
4. **友好用户体验** - 批量任务时友好提示加速
5. **优雅降级保证** - 子Agent不可用时自动降级到CLI队列

**两种模式**:

| 模式 | 适用场景 | 版本标识 | 性能 |
|------|----------|----------|------|
| CLI任务队列 | 1-5个任务，有依赖关系 | v5.0.0-cli-native | 基准 |
| 子Agent并行 | >5个独立任务 | v5.0.0-cli-native+agent | 5-10x加速 |

**交付物**:
- subagents.yaml (子Agent定义)
- examples/with-subagents.md (并行处理示例)
- references/graceful-fallback.md (降级机制)

**时间**: +1小时/技能（可选增强）

#### Level 4: 自迭代学习 (Self-Iteration)

**目标**: 持续学习和优化

**核心内容**:
1. **经验记录机制** - lesson-memory.md
2. **模式识别** - experience/patterns.md
3. **知识提取** - 自动从项目中提取知识
4. **持续优化** - 基于经验的自我改进

**交付物**:
- experience/patterns.md
- lesson-memory.md
- cases/positive/ (多个案例)

**时间**: 1小时/技能

**质量门**:
- [ ] experience/patterns.md已创建
- [ ] lesson-memory.md机制已建立
- [ ] 多个成功案例已添加
- [ ] 自迭代流程已定义

---

## 6大绝对禁止原则

每个技能需要定制化的6大禁止原则。以下是技能升级专家的定制版本：

```yaml
1. 禁止脱离数据/证据 - 所有升级结论必须有实际验证数据支撑
2. 禁止预设结论 - 不假设升级一定能成功，必须验证
3. 禁止方法误用 - 严格按照四级升级路径执行
4. 禁止忽视边界 - 明确技能适用范围和限制
5. 禁止质量妥协 - 不追求速度而牺牲质量评分
6. 禁止文档缺失 - 完整记录升级过程和决策
```

### 定制化示例

**扎根理论 (Grounded Theory)**:
```yaml
禁止编码前预设结论
禁止脱离原始数据编码
禁止编码无理论依据
禁止忽视负面案例
禁止追求编码数量
禁止编码标准不一致
```

**社会网络分析 (SNA)**:
```yaml
禁止节点定义模糊
禁止忽视关系权重
禁止过度简化网络
禁止可视化误导
禁止忽视网络动态性
禁止忽视社区结构
```

---

## 任务分解规则

### 三层分解法

```yaml
第一层: 主要阶段
  - 阶段1: 准备评估
  - 阶段2: Level升级
  - 阶段3: 质量验证
  - 阶段4: 文档完善

第二层: 每阶段的子任务
  - 任务1.1: 版本评估
  - 任务1.2: 需求分析
  - 任务2.1: Level 1升级
  - 任务2.2: Level 2升级
  ...

第三层: 可执行原子任务
  - 读取skill.yaml
  - 更新SKILL.md
  - 创建references文件
  ...
```

### 任务创建规则

```yaml
规则1: 每个任务必须独立可执行
规则2: 任务之间明确依赖关系
规则3: 每个任务有明确的验收标准
规则4: 任务粒度适中（0.5-2小时完成）
规则5: 自动化任务优先
```

---

## 目录结构标准

```yaml
技能目录结构:
  skill-name/
    SKILL.md                    # 核心技能定义（必须）
    README.md                   # 快速入门指南（推荐）
    soul.md                     # 技能灵魂/哲学（可选）
    skill.yaml                  # 技能配置文件（必须）
    subagents.yaml              # 子Agent定义（可选）
    lesson-memory.md            # 经验记录（Level 4）

    references/                 # 方法论文献（Level 2）
      classic-literature.md     # 经典文献（必须）
      concepts.md               # 核心概念（可选）
      tools.md                  # 工具文档（可选）
      graceful-fallback.md      # 优雅降级（Level 3+）

    experience/                 # 经验模式（Level 4）
      patterns.md               # 识别的模式（必须）

    cases/                      # 案例库（Level 2/4）
      positive/                 # 成功案例（至少1个）
      negative/                 # 失败案例（推荐）

    templates/                  # 模板文件（Level 3）
      task_plan.md.template     # 任务计划模板（推荐）

    tools/                      # 工具脚本（可选）

    prompts/                    # 提示词（必须）
      system-prompt.md          # 系统提示词

    examples/                   # 使用示例（推荐）
```

---

## CLI原生集成

### 任务队列支持

```yaml
task-queue:
  自动创建: true
  持久化: true
  依赖追踪: true

  task-types:
    - level-assessment
    - level-upgrade
    - quality-validation
    - report-generation

  execution:
    model-driven: true       # 模型直接执行，不生成脚本
    tool-first: true         # 优先使用专用工具
    state-persistence: true  # 状态持久化
```

### 三层持久化

```yaml
持久化层次:
  第一层: 会话持久化
    - 当前任务状态
    - 临时数据
    - 位置: .claude/session/

  第二层: 项目持久化
    - 任务历史
    - 分析结果
    - 位置: project/tasks/

  第三层: 学习持久化
    - 经验模式
    - 案例库
    - 位置: experience/ & cases/
```

---

## 质量保证

### 完成度验证清单

```yaml
Level 1 检查:
  ☑ 6大禁止原则已定制化
  ☑ 任务分解规则已定义
  ☑ SKILL.md基础结构完整
  ☑ 目录结构符合标准

Level 2 检查:
  ☑ 经典文献已引用
  ☑ 核心概念已定义
  ☑ 至少1个成功案例
  ☑ 应用范围已明确

Level 3 检查:
  ☑ CLI任务队列支持
  ☑ 状态持久化机制
  ☑ 模型驱动执行
  ☑ 工具集成完成

Level 4 检查:
  ☑ experience/patterns.md已创建
  ☑ lesson-memory.md机制
  ☑ 多个成功案例
  ☑ 自迭代流程定义

质量评分:
  ☑ 内容完整性 (5/5)
  ☑ 方法论准确性 (5/5)
  ☑ 实用性 (5/5)
  ☑ CLI集成度 (5/5)
  ☑ 自迭代能力 (5/5)
```

---

## 跨平台兼容性规范

### 核心原则

**所有技能必须跨平台兼容（Windows/Linux/macOS）**

技能不应该假设用户的操作系统环境。所有命令和操作必须使用跨平台方式实现。

### 禁止使用的Linux特定命令

```yaml
禁止命令:
  文件操作:
    - # 使用Python os.makedirs创建目录
- rm -rf          # 使用 shutil.rmtree()
    - cp -r           # 使用 shutil.copytree()
    - mv              # 使用 shutil.move()
    - ln -s           # 使用 os.symlink()
    - touch           # 使用 open(f, 'a').close()
    
  进程操作:
    - nohup ... &     # 使用 subprocess.Popen()
    - kill $PID       # 使用 subprocess.run(['taskkill', ...]) 或 os.kill()
    - ps aux | grep   # 使用 psutil 库
    
  重定向:
    - > /dev/null     # 使用 subprocess.DEVNULL
    - 2>&1            # 使用 stderr=subprocess.STDOUT
    
  路径引用:
    - /tmp/           # 使用 tempfile.gettempdir()
    - $HOME           # 使用 Path.home()
    - $PWD            # 使用 os.getcwd()
    - ~               # 使用 Path.home()
    
  文件打开:
    - open file       # macOS特有，使用 webbrowser.open()
    - xdg-open        # Linux特有，使用 webbrowser.open()
    - start           # Windows特有，使用 os.startfile() 或 webbrowser.open()
```

### 跨平台替代方案

#### 1. 目录创建

```python
# 正确方式（跨平台）
import os
os.makedirs(path, exist_ok=True)

# 或使用共享工具
from _shared_tools.init_project import init_project
init_project(project_path)
```

#### 2. 临时文件

```python
# 正确方式（跨平台）
import tempfile
import os

# 获取临时目录
temp_dir = tempfile.gettempdir()

# 创建临时文件
temp_file = os.path.join(temp_dir, "output.html")

# 或使用
temp_path = tempfile.mktemp(suffix=".html")
```

#### 3. 文件复制

```python
# 正确方式（跨平台）
import shutil

# 复制目录
shutil.copytree(src_dir, dst_dir)

# 复制文件
shutil.copy2(src_file, dst_file)
```

#### 4. 打开文件/URL

```python
# 正确方式（跨平台）
import webbrowser
import os
import platform

def open_file(filepath):
    """跨平台打开文件"""
    if platform.system() == 'Windows':
        os.startfile(filepath)
    elif platform.system() == 'Darwin':  # macOS
        os.system(f'open "{filepath}"')
    else:  # Linux
        os.system(f'xdg-open "{filepath}"')

# 或简单使用
webbrowser.open(f"file://{os.path.abspath(filepath)}")
```

#### 5. 后台进程

```python
# 正确方式（跨平台）
import subprocess
import platform

def run_background(cmd_list, cwd=None):
    """跨平台后台运行"""
    kwargs = {
        'stdout': subprocess.DEVNULL,
        'stderr': subprocess.DEVNULL,
        'cwd': cwd
    }
    
    if platform.system() == 'Windows':
        kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
    
    return subprocess.Popen(cmd_list, **kwargs)
```

### 共享工具模块

位置: `agentskills/_shared_tools/`

```yaml
共享工具:
  init_project.py:
    功能: 跨平台项目初始化
    用法: |
      from _shared_tools.init_project import init_project
      init_project("/path/to/project")
      
  env_adapter.py:
    功能: 环境适配器（待创建）
    功能:
      - 自动检测操作系统
      - 提供统一的文件操作API
      - 处理路径分隔符差异
```

### 路径处理规范

```python
# 正确方式（跨平台）
import os
from pathlib import Path

# 路径连接
path = os.path.join(dir1, dir2, filename)

# 或使用Path
path = Path(dir1) / dir2 / filename

# 规范化路径
path = os.path.normpath(path)

# 获取绝对路径
abs_path = os.path.abspath(relative_path)
```

### 验证清单

升级/创建技能时必须验证：

```yaml
跨平台兼容性检查:
  ☑ SKILL.md中无Linux特定命令
  ☑ 无硬编码的 /tmp/ 路径
  ☑ 无 $变量 语法
  ☑ 文件操作使用Python标准库
  ☑ 目录创建使用 os.makedirs(exist_ok=True)
  ☑ 临时文件使用 tempfile 模块
  ☑ 路径连接使用 os.path.join() 或 Path
  ☑ 后台进程使用 subprocess.DEVNULL
```

### 常见问题修复

| 问题 | 修复方式 |
|------|----------|
| # 使用Python os.makedirs创建目录
不兼容Windows | 改用 `os.makedirs(path, exist_ok=True)` |
| `/tmp/` 路径不存在 | 改用 `tempfile.gettempdir()` |
| `cp -r` 命令失败 | 改用 `shutil.copytree()` |
| `kill $PID` 语法错误 | 改用 `subprocess.run(['taskkill', '/F', '/PID', str(pid)])` |
| `> /dev/null 2>&1 &` 失败 | 改用 `subprocess.DEVNULL` 和 `Popen` |
| `$HOME` 未定义 | 改用 `Path.home()` 或 `os.path.expanduser('~')` |

---

## 成功案例

### 已验证的14个技能

| 技能 | 原版本 | 目标版本 | 质量评分 |
|------|--------|----------|----------|
| grounded-theory-expert | 2.0.0 | 5.0.0-cli-native | 5/5 |
| social-network-analysis-expert | 5.0.0-ai-cli-native | 5.0.0-cli-native | 5/5 |
| digital-durkheim-expert | 5.0.0-ai-cli-native | 5.0.0-cli-native | 5/5 |
| digital-marx-expert | 5.0.0-ai-cli-native | 5.0.0-cli-native | 5/5 |
| digital-weber-expert | 5.0.0-ai-cli-native | 5.0.0-cli-native | 5/5 |
| bourdieu-field-analysis-expert | 5.0.0-ai-cli-native | 5.0.0-cli-native | 5/5 |
| actor-network-analysis-expert | 5.0.0-ai-cli-native | 5.0.0-cli-native | 5/5 |
| cas-simulation-expert | 5.0.0-cli-native | 5.0.0-cli-native | 5/5 |
| system-dynamics-expert | 5.0.0-cli-native | 5.0.0-cli-native | 5/5 |
| qca-analysis-expert | 5.0.0-cli-native | 5.0.0-cli-native | 5/5 |
| did-analysis-expert | 5.0.0-cli-native | 5.0.0-cli-native | 5/5 |
| survey-design-expert | 5.0.0-cli-native | 5.0.0-cli-native | 5/5 |
| business-ecosystem-expert | 5.0.0-cli-native | 5.0.0-cli-native | 5/5 |
| business-model-expert | 5.0.0-cli-native | 5.0.0-cli-native | 5/5 |

**成果统计**:
- 完成率: 100% (14/14)
- 平均质量: 5/5
- 总文档量: ~30,000行
- 验证状态: 已在生产环境使用

---

## 参考资料

- [详细指南](references/detailed-guide.md)
- [快速参考](references/quick-reference.md)
- [子Agent增强](references/subagent-enhancement.md)
- [优雅降级](references/graceful-fallback.md)
- [经验模式](experience/patterns.md)

---

## 版本历史

```yaml
5.0.0-cli-native+agent (2026-03-14):
  - 添加子Agent并行支持
  - 添加优雅降级机制
  - 添加CRCT思维链
  - 完善质量保证体系

1.0.0 (2026-03-08):
  - 初始版本
  - 14个技能验证成功
  - 100%完成率
  - 5/5平均质量
```

---

**使用本技能，您可以将任何AI CLI技能系统化地升级到v5.0.0-cli-native标准！**