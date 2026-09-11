---
name: grounded-theory-expert
description: |
  Grounded Theory analysis expert. Provides open coding, axial coding, and selective coding systematic workflows, with support for theoretical saturation testing and CRCT chain-of-thought reasoning. Suitable for qualitative research, theory construction, and in-depth data analysis.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

------|---------|--------------|
> | 数据分段、编码统计、工具调用 | **AI自动执行** | 无需暂停 |
> | 编码命名、范畴理论归类、核心范畴选择 | **人类判断** | 暂停并输出决策理由 |
> | 负面案例的理论边界修正 | **人类判断** | 暂停并说明修正依据 |
> |Paradigm关系推断、故事线构建 | **人类判断** | 暂停并输出理论依据 |
>
> ❌ 禁止：用AI自动执行替代人类意义提炼
> ✅ 必须：技术步骤AI自动执行，理论判断步骤暂停并说明理由

# SKILL.md - grounded-theory-expert

---
metadata:
  version: "5.2.0-cli-native+agent"
  methodology: "Grounded Theory Methodology"
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
  created: "2026-03-05"
  updated: "2026-03-08"
  author: "SocienceAI Methodology Expert"
  license: "MIT"
  alignment_reference: "grounded-theory-coding (v5.0.0)"

  execution_modes:
    cli_queue: "CLI任务队列（基础）"
    subagent_parallel: "子Agent并行（增强）"

  performance:
    sequential: "30分钟/文件"
    parallel: "35分钟/10文件（8.6x加速）"
---

## 基本信息

**名称**: grounded-theory-expert (扎根理论专家)
**版本**: 5.0.0-cli-native
**作者**: SocienceAI Methodology Expert
**许可证**: MIT
**对齐标准**: grounded-theory-coding (v5.0.0)

## 描述

## 🧭 人机协作分工原则

> **核心理念**：质性研究的价值在于认知突破，AI 是工具而非主体。
> AI 在建立常识、识别反常、提升效率等方面善用，
> **严守"意义提炼"这一核心环节的人类判断权**。

### 溯因推理框架（GT 的认识论根基）

```
无监督学习发现模式  =  归纳（induction）
    ↓
  AI 做体力活       =  自动化编码、统计
    ↓
【人工提炼意义】    =  溯因（abduction）⚠️ 人类专属
    ↓
  AI 计算验证       =  演绎（deduction）
    ↓
理论创新            =  新概念/新关系/新框架
```

**核心立场**：传统流程中，"人工提炼意义"（赋予编码以理论意义）是 AI 难以替代的部分。
LLM 可以高效复刻主题分析流程，但会丢失：
- **跨对话观察**才能捕捉的微妙倾向
- **弦外之音**（语气、沉默、矛盾）
- **理论敏感性**（Glaser 的 "theoretical sensitivity"）

### 三阶段人机分工

| 阶段 | AI 承担（高效执行） | 人类承担（不可替代） |
|------|------------------|-------------------|
| **开放编码** | 文本分段、词频统计、初步候选编码列表 | **核心判断**：哪些编码触及理论前沿而非表面描述？ |
| **轴心编码** | 342 条关系枚举、范畴归类、Paradigm 模板匹配 | **关键决策**：范畴的**理论命名**和Paradigm类型推断 |
| **选择性编码** | 候选核心范畴排序、饱和度统计 | **最高判断**：哪个范畴统摄全局？故事线是什么？ |
| **饱和度检验** | 新编码发现率统计 ✅（assess-saturation.py） | **理论意义**：是否"足够好"还是"有新发现的可能"？ |

### 计算验证模块（AI 承担部分）

```python
# 范畴覆盖度统计
python assess-saturation.py axial_result.json
# 输出：
# - 范畴频次分布
# - 新编码发现率（最后20%数据）
# - 理论密度 = 关系数 / 范畴数
```

### ❌ 绝对禁止

1. **禁止用 AI 完全替代人工意义提炼**：编码命名必须有研究者判断，不可全由 LLM 自动生成
2. **禁止脱离原始数据生成理论**：每个编码必须回溯原始引文
3. **禁止将频次最高等同于最重要**：高频范畴可能只是常识，低频范畴可能是理论突破
4. **禁止跳过跨访谈比较**：跨个案模式比个案内模式更具理论价值

### ✅ 质量标准

- 每个范畴至少 3 条原始引文支撑
- 理论密度（关系数/范畴数）≥ 1.0 为良好
- 新编码发现率 < 5% 为接近饱和


## 🔗 会话持久化：调用 planning-with-files 基础技能（CRITICAL）

> **核心原则**: 本技能的会话状态管理基于 `planning-with-files` 基础技能。
> 所有长时任务必须激活 `planning-with-files` 模式，不允许脱离此基础自行实现。

### planning-with-files 调用机制

当激活本技能执行多会话研究项目时，**必须**调用 `planning-with-files`：

```
你：开始一个扎根理论研究项目，研究职场女性晋升障碍

AI：[激活 grounded-theory-expert]
    [激活 planning-with-files]
    → 创建 .tasks/task_plan.md    （阶段跟踪）
    → 创建 .tasks/findings.md     （研究发现）
    → 创建 .tasks/progress.md     （会话日志）
    → 开始开放编码阶段...
```

### 本技能与 planning-with-files 的对应关系

| planning-with-files | grounded-theory-expert |
|-------------------|----------------------|
| `.tasks/task_plan.md` | 编码进度表：开放编码→轴心编码→选择性编码 |
| `.tasks/findings.md` | 范畴发现+Paradigm关系记录 |
| `.tasks/progress.md` | 会话日志+每次编码数量 |
| `scripts/init-session.sh` | 会话恢复脚本（⚠️需实现） |
| `scripts/session-catchup.py` | 跨会话状态恢复（⚠️需实现） |

### 依赖关系

```yaml
依赖技能:
  planning-with-files:  # Claude Code CLI 基础技能
    用途: 会话状态持久化（task_plan/findings/progress）
    状态: SKILL.md存在，scripts/待实现
    调用时机: 每次激活本技能时
```

### ⚠️ 当前限制

`planning-with-files` 的 `scripts/` 目录尚未实现（init-session.sh/session-catchup.py不存在）。
本技能在 scripts/ 实现前，**必须手动遵循 planning-with-files 的文件协议**：
- 会话开始：读取 task_plan.md + findings.md
- 会话结束：写入更新后的 task_plan.md + findings.md + progress.md
- 禁止将会话状态仅保存在 LLM 上下文窗口中

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


**扎根理论分析专家** - 支持**复杂任务分解**和**长时任务执行**的质性数据分析技能。

## 🔧 Python 工具

python tools:

#### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | analyze.py | 主分析入口，调度各工具 |
| 2 | segment-data.py | 数据分割与编码准备 |
| 3 | batch_analyzer.py | 批量编码分析 |
| 4 | assess-saturation.py | 理论饱和度评估 |
| 5 | anonymize-data.py | 数据匿名化处理 |
| 6 | calculate-reliability.py | 编码信度计算 |
| 7 | iteration_controller.py | 迭代控制管理 |
| 8 | planning-integration.py | 任务规划集成 |

#### 使用示例

```bash
# 1. 数据分割
python tools/segment-data.py -i data/raw.csv -o results/coded/

# 2. 批量分析
python tools/batch_analyzer.py -i results/coded/ -o results/batch_results.json

# 3. 饱和度评估
python tools/assess-saturation.py -i results/coded/ -o results/saturation.json

# 4. 数据匿名化
python tools/anonymize-data.py -i data/sensitive.csv -o results/anonymized.csv

# 5. 信度计算
python tools/calculate-reliability.py -i results/coder1.csv --compare results/coder2.csv -o results/reliability.json
```

### 核心能力

1. **开放性编码 (Open Coding)**
   - 逐行编码
   - 识别概念
   - 发现范畴
   - 持续比较

2. **轴心编码 (Axial Coding)**
   - 范畴联结
   - 建立维度
   - 识别关系
   - 发展范畴

3. **选择式编码 (Selective Coding)**
   - 核心范畴识别
   - 理论整合
   - 故事线构建
   - 理论饱和

4. **备忘录撰写 (Memoing)**
   - 编码笔记
   - 理论笔记
   - 操作化笔记
   - 整合笔记

### 适用场景

- ✅ 质性研究数据分析
- ✅ 扎根理论研究
- ✅ 理论生成研究
- ✅ 访谈资料分析
- ✅ 观察资料分析
- ✅ 文本资料分析

## ⚠️ 七大绝对禁止原则

### 1. 禁止编码前预设结论

**错误做法**:
```yaml
预设结论:
  - 带着假设去编码
  - 只寻找支持预设的证据
  - 忽略矛盾的资料
  - 强行套用理论

示例:
  "我认为这是一个关于X的研究，
   所以只编码与X相关的内容"
```

**正确做法**:
```yaml
开放编码:
  Step 1: 悬置假设
    - 不预设结论
    - 让资料说话
    - 保持开放性

  Step 2: 逐行编码
    - 每行都编码
    - 不遗漏任何信息

  Step 3: 持续比较
    - 资料与资料比较
    - 概念与概念比较
    - 范畴与范畴比较
```

**量化标准**:
- ✅ 编码前不预设结论
- ✅ 所有资料都被编码
- ✅ 矛盾资料被记录
- ✅ 编码有资料支撑

### 2. 禁止脱离原始数据编码

**错误做法**:
```yaml
抽象编码:
  - 编码没有原始引文
  - 只有概念没有证据
  - 无法追溯编码来源
  - 编码不可验证

示例:
  范畴: "权力结构"
  但没有原始引文支撑
```

**正确做法**:
```yaml
扎根编码:
  每个编码必须:
    1. 引用原始数据
    2. 标注位置（行号/页码）
    3. 记录编码依据

  示例:
    范畴: 权力结构
    概念: 资源控制
    原始引文: "他们控制了所有资金..."
    位置: 访谈3，第15行
    依据: 参与者提到资金分配
```

**量化标准**:
- ✅ 每个编码有原始引文
- ✅ 每个编码有位置标注
- ✅ 编码可以追溯到原始数据
- ✅ 编码清单完整

### 3. 禁止编码无理论依据

**错误做法**:
```yaml
随意编码:
  - 想到什么编码什么
  - 编码间无逻辑关联
  - 范畴无理论基础
  - 无法形成理论

结果:
  - 编码碎片化
  - 无法整合
  - 不成体系
```

**正确做法**:
```yaml
理论编码:
  1. 基于文献的编码
     - 已有理论指导
     - 理论敏感性

  2. 扎根理论的编码技术
     - 开放编码：识别概念
     - 轴心编码：建立关系
     - 选择式编码：整合理论

  3. 持续比较
     - 与已有理论比较
     - 与新资料比较
     - 与编码比较
```

**量化标准**:
- ✅ 编码有理论基础
- ✅ 编码间有逻辑关联
- ✅ 范畴形成体系
- ✅ 理论可以生成

### 4. 禁止忽视负面案例

**错误做法**:
```yaml
选择性编码:
  - 只编码支持理论的案例
  - 忽略或删除矛盾案例
  - 不寻找负面案例
  - 理论被"完美化"

结果:
  - 理论有偏差
  - 缺乏效度
  - 不可信
```

**正确做法**:
```yaml
全面编码:
  1. 编码所有案例
     - 包括矛盾的
     - 包括异常的

  2. 寻找负面案例
     - 主动寻找
     - 专门分析

  3. 修正理论
     - 如果负面案例出现
     - 修改理论以解释
     - 或明确理论边界
```

**量化标准**:
- ✅ 所有案例都被编码
- ✅ 负面案例被记录
- ✅ 矛盾被解释
- ✅ 理论边界明确

### 5. 禁止追求编码数量

**错误做法**:
```yaml
编码数量崇拜:
  - 追求更多编码
  - 认为编码越多越好
  - 质量让位于数量
  - 饱和度=编码数量

问题:
  - 编码冗余
  - 精力浪费
  - 理论不清晰
```

**正确做法**:
```yaml
理论饱和原则:
  1. 关注范畴发展
     - 不只是编码数量
     - 范畴是否完善
     - 属性是否清晰
     - 关系是否明确

  2. 饱和度检验
     - 新资料不再产生新范畴
     - 新资料不再产生新属性
     - 新资料不再产生新关系
     - 理论完整

  3. 质量优先
     - 编稿深度比数量重要
     - 理论连贯性
     - 解释力
```

**量化标准**:
- ✅ 关注范畴而非数量
- ✅ 饱和度=无新范畴/属性/关系
- ✅ 理论完整
- ✅ 解释充分

### 6. 禁止编码标准不一致

**错误做法**:
```yaml
编码随意性:
  - 同类内容编码不同
  - 不同编码无明确区分
  - 编码标准随时间改变
  - 不记录编码规则

结果:
  - 编码不可靠
  - 不可复现
  - 信度低
```

**正确做法**:
```yaml
编码标准化:
  - 建立编码手册
  - 定期一致性检验
  - 记录每次编码决策
```

### 7. 禁止定性分析过程硬编码（CRITICAL）

**核心原则**: 定性分析是智识工作，必须由大模型智力驱动，绝不能硬编码进工具。

**错误做法**:
```yaml
硬编码分析:
  - 用Python关键词匹配做"定性分析"
  - 用if/else判断"这个编码属于哪个范畴"
  - 用规则引擎代替研究者的理论判断
  - 把Paradigm关系写成模板列表让LLM套用

示例（错误）:
  if '焦虑' in code_text:
      return '心理体验'  # 这是大模型的工作，不是代码的工作

示例（正确）:
  prompts/axial_coding.txt:
    "你是一位扎根理论专家。请根据以下编码，
     分析每个编码的Paradigm类型（条件/策略/互动/结果），
     并给出你的理论依据..."
```

**正确做法**:
```yaml
工具只做结构工作:
  - 读取/写入编码数据（文件I/O）
  - 管理范畴和关系的数据结构（状态管理）
  - 格式化输出结果（展示层）
  - 调用工具执行（命令行包装）

智力留给大模型:
  - SKILL.md中包含详细的分析提示词
  - 编码决策由LLM基于理论原则作出
  - 范畴归类由LLM的判断驱动
  - Paradigm关系由LLM的推理生成

Python工具的正确角色:
  ✅ 数据管理、文件I/O、结果格式化
  ✅ 执行analyze.py调用LLM进行定性分析
  ❌ 关键词匹配做"智能判断"
  ❌ 规则引擎替代理论推理
```

**工具链职责划分**:
| 工具 | 职责 |
|------|------|
| analyze.py | 协调工作流，读取方法论指导（LLM定性判断引导） |
| SKILL.md prompts | 定性分析的智力层（大模型） |
| segment-data.py | 数据准备（结构工作） |
| axial_coding.py | 仅返回空结构+方法论备忘录，**Paradigm/关系/范畴归类100%由LLM填充** |
| 任何.py工具 | **永远不做定性判断，只做数据结构和格式化** |

**量化标准**:
- ✅ axial_coding.py 已重构：无任何关键词匹配/Paradigm模板/关系硬编码
- ✅ 所有Paradigm类型字段为None，LLM基于理论原则填充
- ✅ 所有relationship字段为空列表，LLM基于数据识别
- ✅ 4条方法论备忘录引导LLM做定性判断（非替代）
- 范畴归类100%由LLM基于SKILL.md提示词作出
- Paradigm关系100%由LLM推理生成

## 详细指南

完整的使用指南请参考: [详细指南](references/detailed-guide.md)