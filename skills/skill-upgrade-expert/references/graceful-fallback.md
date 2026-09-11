# 子Agent优雅降级机制

**当子Agent不可用时，自动降级到CLI队列，保证核心功能不受影响**

---

## 🎯 核心原则

```yaml
降级原则:
  1. 子Agent是增强功能，非必需
  2. CLI队列是基础保证，必须可靠
  3. 降级应该透明，对用户影响最小
  4. 功能完整性不受影响
  5. 清晰的用户通知

用户体验目标:
  ✅ 即使子Agent不可用，核心功能仍正常工作
  ✅ 用户不知道发生了降级（除非需要长时间等待）
  ✅ 所有功能都能完成，只是速度可能慢一些
```

---

## 🔍 检测子Agent可用性

### 检测逻辑

```python
def check_subagent_availability():
    """检测子Agent是否可用"""

    availability = {
        "available": False,
        "reason": None,
        "fallback_mode": "cli_queue"
    }

    # 检查1: Agent tool是否存在
    if not has_agent_tool():
        availability["reason"] = "Agent tool不可用"
        return availability

    # 检查2: 是否有子Agent类型
    if not has_required_subagent_type():
        availability["reason"] = "所需子Agent类型不存在"
        return availability

    # 检查3: 是否有权限调用
    if not has_permission_to_call_subagent():
        availability["reason"] = "无子Agent调用权限"
        return availability

    # 检查4: 资源是否充足
    if not enough_resources_for_subagent():
        availability["reason"] = "资源不足（内存/CPU）"
        return availability

    # 检查5: 配置是否允许
    if not is_subagent_enabled_in_config():
        availability["reason"] = "配置中禁用了子Agent"
        return availability

    # 所有检查通过
    availability["available"] = True
    return availability


def has_agent_tool():
    """检查Agent tool是否可用"""
    try:
        # 尝试访问Agent tool
        import inspect
        frame = inspect.currentframe()
        # 检查是否有Agent函数可用
        return 'Agent' in globals() or 'Agent' in locals()
    except:
        return False


def has_required_subagent_type(subagent_type="general-purpose"):
    """检查所需子Agent类型是否存在"""
    # 这里可以列出可用的子Agent类型
    available_types = [
        "general-purpose",
        "grounded-theory-coder",
        "sna-analyzer",
        "data-analyzer"
    ]
    return subagent_type in available_types


def has_permission_to_call_subagent():
    """检查是否有权限调用子Agent"""
    # 检查配置文件
    config = load_skill_config()
    if config.get("allow_subagents", True) is False:
        return False
    return True


def enough_resources_for_subagent():
    """检查资源是否充足"""
    import psutil

    # 检查内存（需要至少2GB可用）
    available_memory_gb = psutil.virtual_memory().available / (1024**3)
    if available_memory_gb < 2:
        return False

    # 检查CPU（需要至少2个核心）
    cpu_count = psutil.cpu_count()
    if cpu_count < 2:
        return False

    return True


def is_subagent_enabled_in_config():
    """检查配置是否启用子Agent"""
    config = load_skill_config()
    return config.get("enable_subagents", True)
```

---

## 🔄 降级策略

### 策略1: 预防性降级（执行前）

```python
def execute_with_preemptive_fallback(tasks):
    """预防性降级：执行前检查可用性"""

    # 第一步：检查子Agent可用性
    availability = check_subagent_availability()

    if not availability["available"]:
        # 子Agent不可用，直接使用CLI队列
        logger.info(f"子Agent不可用: {availability['reason']}")
        logger.info("降级到CLI队列模式")

        # 通知用户（仅在批量任务时）
        if len(tasks) > 5:
            show_friendly_message(
                f"子Agent不可用（{availability['reason']}），",
                "将使用CLI队列处理任务",
                "预计时间较长..."
            )

        return execute_with_cli_queue(tasks)

    # 第二步：子Agent可用，尝试使用
    try:
        return execute_with_subagents(tasks)

    except SubagentError as e:
        # 子Agent执行失败，降级到CLI队列
        logger.error(f"子Agent执行失败: {e}")
        logger.info("降级到CLI队列模式")

        show_friendly_message(
            "子Agent执行遇到问题，",
            "自动切换到CLI队列模式"
        )

        return execute_with_cli_queue(tasks)
```

### 策略2: 反应性降级（执行中）

```python
def execute_with_reactive_fallback(tasks):
    """反应性降级：执行中失败时降级"""

    subagent_results = []
    failed_tasks = []

    # 尝试使用子Agent
    for task in tasks:
        try:
            result = execute_single_task_with_subagent(task)
            subagent_results.append(result)

        except SubagentNotAvailableError:
            # 子Agent突然不可用，全部降级
            logger.warning("子Agent突然不可用，全部任务降级到CLI队列")
            return execute_with_cli_queue(tasks)

        except SubagentExecutionError as e:
            # 单个任务失败，记录并继续
            logger.warning(f"任务{task['id']}在子Agent中失败: {e}")
            failed_tasks.append(task)
            continue

    # 如果有失败的任务，用CLI队列重试
    if failed_tasks:
        logger.info(f"{len(failed_tasks)}个任务失败，使用CLI队列重试")

        cli_results = execute_with_cli_queue(failed_tasks)
        subagent_results.extend(cli_results)

    return subagent_results
```

### 策略3: 渐进式降级（部分降级）

```python
def execute_with_gradual_fallback(tasks):
    """渐进式降级：部分任务用子Agent，部分用CLI队列"""

    # 分组：识别哪些可以用子Agent，哪些必须用CLI队列
    subagent_tasks = []
    cli_queue_tasks = []

    for task in tasks:
        if is_task_suitable_for_subagent(task):
            subagent_tasks.append(task)
        else:
            cli_queue_tasks.append(task)

    results = []

    # 第一批：用CLI队列处理必须串行的任务
    if cli_queue_tasks:
        logger.info(f"使用CLI队列处理{len(cli_queue_tasks)}个任务")
        cli_results = execute_with_cli_queue(cli_queue_tasks)
        results.extend(cli_results)

    # 第二批：尝试用子Agent处理并行任务
    if subagent_tasks:
        availability = check_subagent_availability()

        if availability["available"]:
            try:
                logger.info(f"使用子Agent处理{len(subagent_tasks)}个任务")
                subagent_results = execute_with_subagents(subagent_tasks)
                results.extend(subagent_results)

            except SubagentError as e:
                logger.warning(f"子Agent失败，降级到CLI队列: {e}")
                cli_results = execute_with_cli_queue(subagent_tasks)
                results.extend(cli_results)
        else:
            logger.info(f"子Agent不可用，使用CLI队列")
            cli_results = execute_with_cli_queue(subagent_tasks)
            results.extend(cli_results)

    return results
```

---

## 💬 用户通知策略

### 通知原则

```yaml
通知时机:
  ❌ 不通知: 小任务（<5个），快速完成
  ✅ 友好提示: 批量任务（>5个），需要较长时间
  ✅ 明确通知: 降级发生，用户需要知道
  ✅ 详细说明: 用户要求了解详情

通知内容:
  - 发生了什么（降级）
  - 为什么发生（原因）
  - 影响是什么（可能慢一些）
  - 保证什么（功能完整）
```

### 通知实现

```python
class FallbackNotifier:
    """降级通知管理器"""

    def __init__(self):
        self.has_notified = False
        self.config = load_skill_config()

    def notify_fallback(self, reason, task_count, estimated_time=None):
        """通知用户降级"""

        # 检查配置
        if not self.config.get("show_fallback_messages", True):
            return

        # 检查是否需要通知
        if not self.should_notify(task_count):
            return

        # 构建消息
        message = self.build_message(reason, task_count, estimated_time)

        # 显示消息
        self.show_message(message)

        self.has_notified = True

    def should_notify(self, task_count):
        """判断是否应该通知"""

        # 小任务不通知
        if task_count <= 3:
            return False

        # 已经通知过，不重复通知
        if self.has_notified:
            return False

        # 批量任务，需要通知
        return True

    def build_message(self, reason, task_count, estimated_time=None):
        """构建通知消息"""

        lines = []
        lines.append("ℹ️  执行模式调整")
        lines.append(f"   原因: {self.friendly_reason(reason)}")
        lines.append(f"   任务数: {task_count}个")

        if estimated_time:
            lines.append(f"   预计时间: {estimated_time}")

        lines.append("   所有功能将正常完成 ✓")

        return "\n".join(lines)

    def friendly_reason(self, technical_reason):
        """将技术原因转换为用户友好的说明"""

        reasons_map = {
            "Agent tool不可用": "当前环境不支持并行处理",
            "所需子Agent类型不存在": "所需的分析模块不可用",
            "无子Agent调用权限": "当前配置不支持并行处理",
            "资源不足（内存/CPU）": "系统资源有限，使用标准模式",
            "配置中禁用了子Agent": "当前配置使用标准模式",
            "子Agent执行失败": "并行处理遇到问题，切换到标准模式"
        }

        return reasons_map.get(
            technical_reason,
            "使用标准处理模式"
        )

    def show_message(self, message):
        """显示消息"""
        print(message)
        # 也可以记录到日志
        logger.info(f"用户通知: {message}")


# 使用示例
notifier = FallbackNotifier()

def execute_with_fallback_notification(tasks):
    """带通知的降级执行"""

    availability = check_subagent_availability()

    if not availability["available"]:
        # 子Agent不可用，通知并降级
        notifier.notify_fallback(
            reason=availability["reason"],
            task_count=len(tasks),
            estimated_time=estimate_cli_queue_time(tasks)
        )

        return execute_with_cli_queue(tasks)

    # 子Agent可用，正常执行
    return execute_with_subagents(tasks)
```

---

## 📊 降级场景分析

### 场景1: CLI环境不支持Agent tool

```yaml
环境: 纯命令行，无Agent tool

检测:
  has_agent_tool() → False

行为:
  ✅ 自动降级到CLI队列
  ✅ 通知用户（如果任务多）
  ℹ️  "当前环境不支持并行处理，使用标准模式"

结果:
  - 所有功能正常
  - 只是速度慢一些
  - 用户无感知（除非长时间等待）
```

### 场景2: 资源不足

```yaml
环境: 内存不足，CPU核心少

检测:
  enough_resources_for_subagent() → False
  原因: available_memory < 2GB

行为:
  ✅ 自动降级到CLI队列
  ✅ 通知用户
  ℹ️  "系统资源有限，使用标准模式"

结果:
  - 避免系统崩溃
  - 稳定完成所有任务
  - 用户理解资源限制
```

### 场景3: 子Agent执行失败

```yaml
环境: Agent tool可用，但执行出错

执行:
  execute_with_subagents(tasks)
  → SubagentError: "子进程崩溃"

行为:
  ✅ 捕获错误
  ✅ 自动降级到CLI队列
  ✅ 通知用户
  ℹ️  "并行处理遇到问题，切换到标准模式"

结果:
  - 任务不会丢失
  - 自动重试成功
  - 用户知道发生了什么
```

### 场景4: 用户配置禁用

```yaml
环境: 用户在配置中禁用子Agent

配置:
  config.yaml:
    enable_subagents: false

检测:
  is_subagent_enabled_in_config() → False

行为:
  ✅ 尊重用户配置
  ✅ 使用CLI队列
  ❌ 不通知（用户明确选择）

结果:
  - 按用户意愿执行
  - 无干扰
```

---

## 🛡️ 功能完整性保证

### 核心原则

```yaml
保证1: 所有功能必须完成
  - 降级不应导致功能缺失
  - 只是执行方式不同
  - 最终结果一致

保证2: 数据不丢失
  - 降级过程中的数据安全
  - 原子操作
  - 错误恢复

保证3: 状态一致性
  - 降级前后状态一致
  - 任务状态正确
  - 进度可追踪
```

### 实现示例

```python
def safe_execute_with_fallback(tasks):
    """安全的降级执行，保证功能完整性"""

    # 第一步：保存初始状态
    initial_state = save_state(tasks)

    try:
        # 第二步：尝试子Agent
        results = execute_with_subagents(tasks)

        # 验证结果完整性
        if validate_results(results, tasks):
            return results
        else:
            raise SubagentValidationError("结果验证失败")

    except (SubagentError, ValidationError) as e:
        logger.warning(f"子Agent执行失败: {e}")

        # 第三步：确保状态回滚
        restore_state(initial_state)

        # 第四步：降级到CLI队列
        logger.info("降级到CLI队列模式")

        results = execute_with_cli_queue(tasks)

        # 再次验证结果
        if not validate_results(results, tasks):
            raise CriticalError("CLI队列也无法完成，这是严重错误")

        return results


def validate_results(results, tasks):
    """验证结果的完整性"""

    # 检查1: 结果数量
    if len(results) != len(tasks):
        logger.error(f"结果数量不匹配: {len(results)} != {len(tasks)}")
        return False

    # 检查2: 每个任务都有结果
    for i, task in enumerate(tasks):
        if i >= len(results):
            logger.error(f"任务{i}缺少结果")
            return False

        if results[i] is None:
            logger.error(f"任务{i}结果为空")
            return False

    # 检查3: 结果格式正确
    for i, result in enumerate(results):
        if not is_valid_result_format(result):
            logger.error(f"任务{i}结果格式错误")
            return False

    return True
```

---

## 📝 配置文件

### 技能配置示例

创建 `config/skill-config.yaml`:

```yaml
# 技能执行配置

execution:
  # 子Agent配置
  subagent:
    # 是否启用子Agent
    enabled: true

    # 自动降级
    auto_fallback: true

    # 降级原因映射（用户友好）
    fallback_reasons:
      "Agent tool不可用": "当前环境不支持并行处理"
      "资源不足": "系统资源有限"
      "配置禁用": "当前配置使用标准模式"

  # 通知配置
  notification:
    # 是否显示降级通知
    show_fallback_message: true

    # 通知阈值（任务数）
    notify_threshold: 5

    # 是否显示技术细节
    show_technical_details: false

  # 性能配置
  performance:
    # 子Agent最小任务数
    min_tasks_for_subagent: 5

    # 资源要求
    min_memory_gb: 2
    min_cpu_cores: 2

    # 超时设置
    subagent_timeout: 3600  # 秒

# 日志配置
logging:
  level: INFO
  file: .claude/skill-execution.log

  # 关键事件
  key_events:
    - subagent_called
    - fallback_triggered
    - fallback_reason
    - execution_time
```

---

## 🧪 测试和验证

### 测试场景

```python
def test_fallback_mechanisms():
    """测试所有降级场景"""

    print("测试降级机制...")

    # 测试1: Agent tool不可用
    print("\n1. 测试Agent tool不可用")
    mock_agent_tool_unavailable()
    result = execute_with_fallback(test_tasks)
    assert result is not None
    assert len(result) == len(test_tasks)
    print("   ✅ 通过")

    # 测试2: 资源不足
    print("\n2. 测试资源不足")
    mock_low_resources()
    result = execute_with_fallback(test_tasks)
    assert result is not None
    print("   ✅ 通过")

    # 测试3: 子Agent执行失败
    print("\n3. 测试子Agent执行失败")
    mock_subagent_failure()
    result = execute_with_fallback(test_tasks)
    assert result is not None
    print("   ✅ 通过")

    # 测试4: 配置禁用
    print("\n4. 测试配置禁用")
    mock_config_disabled()
    result = execute_with_fallback(test_tasks)
    assert result is not None
    print("   ✅ 通过")

    print("\n✅ 所有降级测试通过！")
```

---

## 🎯 最佳实践总结

```yaml
DO (推荐做法):
  ✅ 总是检查子Agent可用性
  ✅ 提供完善的降级机制
  ✅ 保证功能完整性
  ✅ 友好的用户通知
  ✅ 详细的日志记录
  ✅ 测试所有降级场景

DON'T (避免做法):
  ❌ 假设子Agent总是可用
  ❌ 降级时丢失数据
  ❌ 让降级影响功能
  ❌ 技术错误直接暴露给用户
  ❌ 忽略降级场景
  ❌ 不测试降级逻辑
```

---

## 📋 降级检查清单

```yaml
实现检查:
  ☑ 检测子Agent可用性
  ☑ 预防性降级
  ☑ 反应性降级
  ☑ 渐进式降级
  ☑ 用户通知
  ☑ 功能完整性验证
  ☑ 状态持久化
  ☑ 错误处理
  ☑ 日志记录
  ☑ 配置支持

测试检查:
  ☑ Agent tool不可用
  ☑ 资源不足
  ☑ 子Agent执行失败
  ☑ 用户配置禁用
  ☑ 批量任务降级
  ☑ 小任务不通知
  ☑ 功能完整性
  ☑ 数据不丢失

文档检查:
  ☑ 降级策略说明
  ☑ 用户通知示例
  ☑ 配置文件说明
  ☑ 故障排除指南
```

---

**关键点**: 子Agent是增强功能，降级到CLI队列不应影响任何核心功能！
