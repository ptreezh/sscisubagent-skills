---
name: grounded-theory-expert
description: |
  扎根理论分析专家。提供开放编码、主轴编码、选择性编码的系统化流程，支持理论饱和度检验和CRCT思维链。适用于质性研究、理论建构、数据深度分析场景。
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

# SKILL.md - grounded-theory-expert

---
metadata:
  version: "5.1.0-cli-native+agent"
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

PZ|
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

VS|### 核心能力
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

## ⚠️ 六大绝对禁止原则

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


## 详细指南

完整的使用指南请参考: [详细指南](references/detailed-guide.md)