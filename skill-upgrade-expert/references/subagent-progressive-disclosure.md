# 渐进式信息披露 - 子Agent增强版

**核心原则：不破坏现有功能，按需加载子Agent**

---

## 🎯 核心设计原则

### 1. 渐进式信息披露

```yaml
原则: 用户/系统只在需要时才知道子Agent的存在

用户体验:
  Level 1: 基础使用
    - 用户只是说"对数据进行编码"
    - 系统自动选择最佳方式
    - 用户不需要知道背后是CLI队列还是子Agent

  Level 2: 高级使用（可选）
    - 用户可以明确指定模式
    - "使用子Agent并行处理"
    - "使用CLI队列串行处理"

  Level 3: 开发者（可选）
    - 查看详细的执行日志
    - 了解为什么选择某种模式
    - 性能对比数据
```

### 2. 向后兼容保证

```yaml
承诺:
  ✅ 现有功能完全保留
  ✅ CLI任务队列仍然是默认
  ✅ 不破坏任何现有代码
  ✅ 不改变基础API

实现:
  - 子Agent作为可选增强
  - 自动决策逻辑透明
  - 用户可以覆盖
  - 降级机制完善
```

### 3. 按需加载

```yaml
触发条件（必须全部满足）:
  1. 任务数量 > 5个
  2. 任务相互独立
  3. 预估时间 > 1小时
  4. 用户没有明确禁止

默认行为:
  - CLI任务队列（安全、可靠）
  - 子Agent并行（仅在必要时）

用户控制:
  - 可以强制使用CLI队列
  - 可以强制使用子Agent
  - 可以设置触发阈值
```

---

## 📋 实现方案

### 架构设计

```yaml
三层架构:

第一层: 基础层（必需）
  - CLI任务队列
  - TaskCreate/TaskUpdate/TaskGet
  - 状态持久化
  - 模型驱动执行

第二层: 决策层（自动）
  - 分析任务特征
  - 评估性能需求
  - 选择执行模式
  - 透明决策日志

第三层: 增强层（可选）
  - 子Agent并行
  - 仅在必要时启用
  - 可手动覆盖
  - 完善的错误处理
```

### 决策流程（渐进式）

```python
def execute_task_progressive(tasks, user_preference=None):
    """
    渐进式任务执行

    用户不会看到这个复杂性，
    只会看到"正在处理..."
    """

    # 第一层：基础检查（对用户透明）
    if user_preference == "cli_queue":
        # 用户明确要求使用CLI队列
        return execute_with_cli_queue(tasks)

    if user_preference == "subagent_parallel":
        # 用户明确要求使用子Agent
        return execute_with_subagents(tasks)

    # 第二层：自动决策（对用户透明）
    mode = auto_decide_mode(tasks)

    if mode == "CLI_QUEUE":
        # 不需要告诉用户选择了什么
        # 只执行即可
        logger.info("使用CLI队列模式")  # 开发日志
        return execute_with_cli_queue(tasks)

    else:  # SUBAGENT_PARALLEL
        # 第一次使用子Agent时，友好提示
        if not has_used_subagents_before():
            show_friendly_message(
                "检测到批量任务，将使用并行处理以提升效率"
            )

        logger.info("使用子Agent并行模式")  # 开发日志
        return execute_with_subagents(tasks)


def auto_decide_mode(tasks):
    """自动决策（完全对用户透明）"""

    # 判断1: 任务数量
    if len(tasks) <= 5:
        return "CLI_QUEUE"

    # 判断2: 独立性
    if has_dependencies(tasks):
        return "CLI_QUEUE"

    # 判断3: 数据量
    if estimate_data_size(tasks) < 100_000:
        return "CLI_QUEUE"

    # 判断4: 时间估算
    if estimate_time(tasks) < 60:
        return "CLI_QUEUE"

    # 其他情况：使用子Agent
    return "SUBAGENT_PARALLEL"


def show_friendly_message(message):
    """友好的进度提示（渐进式信息披露）"""

    # 只在第一次使用时显示
    # 之后不再打扰用户

    print(f"ℹ️  {message}")
    print("   这将加快处理速度...")
```

---

## 📝 SKILL.md更新（渐进式版本）

### 更新CLI集成章节

```markdown
## CLI原生集成

### 智能执行模式

本技能会**自动选择**最佳执行方式，你无需关心细节。

#### 对于小任务（1-5个文件）

```yaml
行为: 自动使用CLI任务队列
特点: 简单、可靠、快速
你看到的: "正在处理..."
实际: 依次处理每个文件
```

#### 对于批量任务（>5个文件）

```yaml
行为: 自动使用子Agent并行
特点: 快速、高效、透明
你看到的: "检测到批量任务，使用并行处理..."
实际: 多个子Agent同时处理
性能: 5-10x加速
```

### 用户控制（可选）

如果你想手动控制模式，可以这样：

```
# 强制使用子Agent并行
"使用子Agent并行处理这些文件"

# 强制使用CLI队列
"使用CLI队列依次处理"

# 让系统自动选择（默认）
"处理这些文件"
```

### 性能对比

| 文件数 | CLI队列 | 子Agent并行 | 自动选择 |
|--------|---------|-----------|---------|
| 3个 | 1.5小时 | - | CLI队列 ✅ |
| 10个 | 5小时 | 35分钟 | 子Agent ⚡ |
| 50个 | 25小时 | 2.5小时 | 子Agent ⚡ |

**注意**: 系统会自动选择最优方式，你通常不需要手动指定。
```

---

## 🛡️ 向后兼容保证

### 现有功能完全保留

```yaml
保证1: CLI队列功能不变
  ✅ TaskCreate/TaskUpdate/TaskGet仍然可用
  ✅ 状态持久化不变
  ✅ 所有现有代码正常工作
  ✅ 不破坏任何现有流程

保证2: API兼容
  ✅ 现有调用方式不变
  ✅ 不需要修改任何代码
  ✅ 自动升级，无感知

保证3: 默认行为保守
  ✅ CLI队列是默认选择
  ✅ 只在明确有益时使用子Agent
  ✅ 不会突然改变行为

保证4: 可控性强
  ✅ 可以强制使用CLI队列
  ✅ 可以禁用子Agent
  ✅ 可以调整触发阈值
```

### 降级机制

```python
def execute_with_fallback(tasks):
    """带回退的执行"""

    try:
        # 尝试使用子Agent
        return execute_with_subagents(tasks)

    except SubagentNotAvailable:
        # 子Agent不可用，降级到CLI队列
        logger.warning("子Agent不可用，使用CLI队列")
        return execute_with_cli_queue(tasks)

    except SubagentError as e:
        # 子Agent执行出错，降级到CLI队列
        logger.error(f"子Agent出错: {e}，降级到CLI队列")
        return execute_with_cli_queue(tasks)

    # CLI队列也会出错？那才是真正的错误
```

---

## 🎯 用户体验设计

### 场景1: 小任务（完全透明）

```yaml
用户输入:
  "对这3个访谈进行编码"

系统行为:
  - 分析: 3个文件，使用CLI队列
  - 执行: 依次处理
  - 用户看到:
    ✅ 正在处理文件1...
    ✅ 正在处理文件2...
    ✅ 正在处理文件3...
    ✅ 完成！

用户不知道:
  - 系统选择了CLI队列
  - 没有使用子Agent
  - （也不需要知道）
```

### 场景2: 批量任务（友好提示）

```yaml
用户输入:
  "对data/目录下的所有访谈文件进行编码"

系统行为:
  - 分析: 发现20个文件
  - 决策: 使用子Agent并行
  - 友好提示（仅第一次）:
    ℹ️  检测到批量任务（20个文件）
    ℹ️  将使用并行处理以提升效率
    ℹ️  预计时间: 约35分钟（而非10小时）

  - 执行: 20个子Agent并行
  - 用户看到:
    ✅ 正在并行处理20个文件...
    ✅ 完成！总时间: 35分钟
    ✅ 加速: 17x ⚡

用户知道:
  - 使用了并行处理
  - 速度很快
  - （但不需要知道技术细节）
```

### 场景3: 明确控制（高级用户）

```yaml
用户输入:
  "使用子Agent并行处理这10个文件"

系统行为:
  - 分析: 用户明确要求子Agent
  - 执行: 使用子Agent并行
  - 用户看到:
    ✅ 启动子Agent并行处理...
    ✅ 完成！

用户完全控制:
  - 明确知道使用了子Agent
  - 可以精确控制执行方式
```

---

## 📊 技术实现细节

### 配置文件（可选）

创建 `.claude/skill-config.yaml`:

```yaml
# grounded-theory-expert配置

execution:
  # 默认模式：auto
  mode: auto  # auto | cli_queue | subagent_parallel

  # 子Agent触发阈值
  thresholds:
    min_tasks: 5        # 最少任务数
    min_data_size: 100  # KB
    min_time: 60        # 分钟

  # 是否显示友好提示
  show_friendly_message: true

  # 是否使用过子Agent
  has_used_subagents: false

# 用户可以覆盖这些设置
```

### 日志策略

```yaml
用户日志（简洁）:
  ✅ 正在处理文件1...
  ✅ 正在处理文件2...
  ✅ 完成！

开发者日志（详细）:
  [INFO] 任务分析: 文件数=10, 独立=True
  [INFO] 决策结果: 使用子Agent并行
  [INFO] 启动10个子Agent
  [INFO] 子Agent1完成，耗时28秒
  [INFO] 子Agent2完成，耗时31秒
  ...
  [INFO] 所有子Agent完成，总耗时35秒
  [INFO] 整合结果中...
  [INFO] 完成！
```

---

## ✅ 验证清单

### 渐进式信息披露检查

```yaml
用户体验:
  ☑ 小任务完全透明
  ☑ 批量任务友好提示
  ☑ 不会打扰用户
  ☑ 只在第一次提示

向后兼容:
  ☑ 现有功能保留
  ☑ CLI队列默认
  ☑ API不变
  ☑ 可手动控制

按需加载:
  ☑ 自动决策逻辑
  ☑ 触发条件合理
  ☑ 降级机制完善
  ☑ 用户可控

性能:
  ☑ CLI队列性能不变
  ☑ 子Agent显著加速
  ☑ 不增加额外开销
  ☑ 资源使用合理
```

---

## 🎯 实施步骤

### 第一步: 保留现有功能

```yaml
不做任何破坏性改动:
  ✅ CLI队列代码完全保留
  ✅ 所有现有API不变
  ✅ 默认行为不变
```

### 第二步: 添加决策层

```yaml
添加自动决策逻辑:
  ✅ 分析任务特征
  ✅ 评估是否需要子Agent
  ✅ 对用户透明
```

### 第三步: 实现子Agent（可选）

```yaml
作为可选增强:
  ✅ 仅在必要时启用
  ✅ 友好提示
  ✅ 降级机制
```

### 第四步: 文档更新

```yaml
渐进式文档:
  ✅ 用户指南简洁
  ✅ 开发者文档详细
  ✅ 性能对比透明
```

---

## 🎉 总结

```yaml
核心原则:
  ✅ 不破坏现有功能
  ✅ 渐进式信息披露
  ✅ 按需加载子Agent
  ✅ 向后完全兼容

用户体验:
  - 小任务: 完全透明
  - 批量任务: 友好提示
  - 高级用户: 完全控制

技术实现:
  - CLI队列: 默认、安全
  - 子Agent: 增强、快速
  - 自动决策: 智能、透明

版本标识:
  - v5.0.0-cli-native: 基础版（CLI队列）
  - v5.0.0-cli-native+agent: 增强版（CLI队列 + 子Agent）
  - 两者完全兼容，后者是前者的超集
```

---

**关键点**: 用户通常不需要知道子Agent的存在，系统会自动选择最佳方式！
