# CLI任务队列 vs 子智能体驱动 - 架构对比

**澄清两种不同的任务执行模式**

---

## 📊 两种架构对比

### 模式A: CLI任务队列（当前升级技能支持）

```yaml
架构:
  主Agent → CLI任务队列 → 模型直接执行

特点:
  - 任务在主Agent的TaskList中管理
  - 使用TaskCreate/TaskUpdate/TaskGet工具
  - 主Agent直接执行任务（或使用Bash/Read等工具）
  - 不调用子Agent

执行流程:
  1. 主Agent接收任务
  2. 分解为子任务（TaskCreate）
  3. 依次执行子任务（主Agent自己）
  4. 更新状态（TaskUpdate）
  5. 完成后标记完成（TaskUpdate completed）

优点:
  ✅ 简单直接
  ✅ 上下文保持
  ✅ 状态管理清晰
  ✅ 无子Agent通信开销

缺点:
  ❌ 无法并行处理独立任务
  ❌ 主Agent承担所有工作
  ❌ 大量任务时上下文压力大

适用场景:
  - 任务数量少（<10个）
  - 任务有依赖关系
  - 需要紧密协作
```

### 模式B: 子智能体驱动（双层架构）

```yaml
架构:
  主Agent → 子Agent集 → 每个子Agent独立执行子任务

特点:
  - 使用Agent tool调用specialized subagent
  - 子Agent有独立的上下文窗口
  - 可并行执行多个子Agent
  - 支持多层嵌套（主→子→子子）

执行流程:
  1. 主Agent接收任务
  2. 分解为独立子任务
  3. 为每个子任务启动子Agent（Agent tool）
  4. 子Agent独立执行（有独立context）
  5. 子Agent返回结果
  6. 主Agent整合结果

优点:
  ✅ 可并行处理独立任务
  ✅ 每个子Agent有完整上下文
  ✅ 适合CPU密集型或大量任务
  ✅ 可扩展到多层架构

缺点:
  ❌ 复杂度较高
  ❌ 子Agent间通信成本
  ❌ 状态管理复杂
  ❌ 需要careful orchestration

适用场景:
  - 任务数量多（>10个）
  - 有多个独立任务
  - 需要并行处理
  - 需要专门能力
```

---

## 🤔 当前升级技能支持什么？

### 当前实现（Level 3: CLI集成）

```yaml
升级后的技能支持:

✅ CLI任务队列（模式A）
  - TaskCreate/TaskUpdate/TaskGet
  - 任务状态持久化
  - 三层持久化架构
  - 模型直接执行

❌ 子智能体驱动（模式B）
  - 未在Level 3中明确要求
  - 未在SKILL.md模板中包含
  - 未在示例中展示
  - 不是必需标准
```

---

## 📋 实际案例对比

### 案例1: grounded-theory-expert（当前实现）

**架构**: CLI任务队列

```python
# 主Agent执行流程

# 1. 创建任务
TaskCreate("数据分段")
TaskCreate("开放编码")
TaskCreate("轴心编码")
TaskCreate("选择式编码")

# 2. 依次执行
for task in tasks:
    # 主Agent直接执行
    data = read_file(file_path)
    codes = perform_coding(data)  # 主Agent自己做
    save_results(codes)

# 3. 更新状态
TaskUpdate(task_id, status="completed")
```

**特点**:
- ✅ 任务在TaskList中管理
- ✅ 主Agent执行所有工作
- ❌ 无法并行编码多个数据段
- ❌ 大量数据时主Agent context压力大

---

### 案例2: 如果使用子智能体驱动

**架构**: 双层子Agent

```python
# 主Agent orchestrator

# 1. 分解任务
data_segments = split_data(data)  # 10个数据段

# 2. 并行启动子Agent
subagents = []
for segment in data_segments:
    subagent = Agent(
        subagent_type="grounded-theory-coder",
        prompt=f"对这个数据段进行开放编码: {segment}"
    )
    subagents.append(subagent)

# 3. 等待所有子Agent完成
results = []
for subagent in subagents:
    result = await subagent  # 每个子Agent独立执行
    results.append(result)

# 4. 整合结果
all_codes = merge_codes(results)
```

**特点**:
- ✅ 10个子Agent并行编码
- ✅ 每个子Agent有独立context
- ✅ 大幅提升速度
- ⚠️ 需要careful orchestration
- ⚠️ 结果整合复杂

---

## 🎯 需求分析

### 你的问题：支持"双层子智能体驱动子任务"吗？

**答案**: 当前升级技能**不明确要求**，但**不禁止**添加。

```yaml
当前状态:
  Level 3标准中:
    - ✅ 要求: CLI任务队列支持
    - ✅ 要求: 状态持久化
    - ✅ 要求: 模型驱动执行
    - ❌ 未要求: 子智能体驱动

  意味着:
    - 达到5.0.0-cli-native标准 ✅
    - 不需要实现子Agent架构
    - 但可以选择性添加

如果需要子Agent支持:
  - 可以作为额外功能添加
  - 不影响v5.0.0-cli-native认证
  - 但需要文档说明
```

---

## 💡 建议的升级方案

### 方案A: 保持当前标准（推荐给大多数技能）

```yaml
适用情况:
  - 任务数量少（<10个）
  - 任务有依赖关系
  - 不需要大量并行

实现:
  - 使用CLI任务队列
  - TaskCreate/TaskUpdate/TaskGet
  - 主Agent执行

优势:
  - 简单
  - 可靠
  - 易维护

符合标准: ✅ v5.0.0-cli-native
```

### 方案B: 增强版（添加子Agent支持）

```yaml
适用情况:
  - 任务数量多（>10个）
  - 有多个独立任务
  - 需要并行加速

实现:
  - CLI任务队列 + Agent tool
  - 识别可并行任务
  - 启动子Agent并行执行
  - 整合子Agent结果

需要添加:
  1. SKILL.md中说明子Agent策略
  2. examples/中展示子Agent用法
  3. templates/中包含子Agent模板

符合标准: ✅ v5.0.0-cli-native (增强)
```

### 方案C: 混合模式（最灵活）

```yaml
策略:
  - 小任务: 主Agent直接执行（模式A）
  - 大量独立任务: 子Agent并行（模式B）

实现:
  1. 任务分析
     - 识别可并行任务
     - 评估任务数量

  2. 分支处理
     if task_count < threshold:
         # 模式A: CLI任务队列
         use_cli_queue()
     else:
         # 模式B: 子Agent并行
         use_subagents()

  3. 文档说明
     - 何时用哪种模式
     - 如何切换模式
     - 最佳实践

符合标准: ✅ v5.0.0-cli-native (高级)
```

---

## 🔄 升级技能本身需要更新吗？

### 如果要支持子Agent驱动

**需要添加的内容**:

```yaml
Level 3增强:

1. 子Agent策略
   - 何时使用子Agent
   - 如何选择子Agent类型
   - 如何orchestrate多个子Agent

2. 通信模式
   - 主Agent→子Agent
   - 子Agent→主Agent
   - 子Agent↔子Agent（如需要）

3. 状态管理
   - 子Agent状态追踪
   - 结果整合
   - 错误处理

4. 文档要求
   - 在SKILL.md中说明
   - 在examples/中展示
   - 在templates/中支持
```

---

## 🎯 实际建议

### 对于大多数技能

```yaml
推荐: CLI任务队列（模式A）

理由:
  1. 简单可靠
  2. 符合v5.0.0-cli-native标准
  3. 易于维护
  4. 适合大多数场景

示例:
  - grounded-theory-expert ✅
  - data-analysis-expert ✅
  - survey-design-expert ✅
```

### 对于需要并行的技能

```yaml
推荐: 添加子Agent支持（模式B）

适合场景:
  - 批量处理多个文件
  - 并行分析多个案例
  - 大量独立计算

示例:
  - 批量文献综述
  - 大规模数据清洗
  - 并行案例分析

实现:
  - 保持CLI任务队列作为基础
  - 添加子Agent并行能力
  - 文档说明何时使用
```

---

## 📝 总结

```yaml
当前v5.0.0-cli-native标准:
  ✅ 支持: CLI任务队列
  ❌ 不要求: 子智能体驱动
  ✅ 允许: 可选添加子Agent

双层子智能体驱动:
  - 不是当前标准的必需部分
  - 可以作为增强功能添加
  - 需要额外文档和示例

建议:
  1. 先实现CLI任务队列（必需）
  2. 评估是否需要子Agent（可选）
  3. 如需要，作为增强功能添加
  4. 保持向后兼容
```

---

**结论**: 当前升级技能专注于CLI任务队列，不强制要求子智能体驱动，但允许作为可选增强功能添加。
