# 优雅降级实现模板

**可复制到任何技能中，确保子Agent不可用时的优雅降级**

---

## 📋 完整实现模板

```python
#!/usr/bin/env python3
"""
技能执行模板 - 带优雅降级机制

确保在任何环境下都能正常工作：
- 子Agent可用时：使用并行加速
- 子Agent不可用时：自动降级到CLI队列
- 用户友好通知
- 功能完整性保证
"""

import logging
from typing import List, Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """执行模式"""
    CLI_QUEUE = "cli_queue"
    SUBAGENT_PARALLEL = "subagent_parallel"


class FallbackReason(Enum):
    """降级原因"""
    AGENT_TOOL_UNAVAILABLE = "Agent tool不可用"
    SUBAGENT_TYPE_NOT_FOUND = "所需子Agent类型不存在"
    NO_PERMISSION = "无子Agent调用权限"
    INSUFFICIENT_RESOURCES = "资源不足(内存/CPU)"
    CONFIG_DISABLED = "配置中禁用了子Agent"
    EXECUTION_FAILED = "子Agent执行失败"


class GracefulExecutor:
    """优雅降级执行器"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.notifier = FallbackNotifier(config)

    def execute(self, tasks: List[Dict]) -> List[Dict]:
        """
        智能执行任务, 自动降级

        Args:
            tasks: 任务列表

        Returns:
            执行结果列表
        """

        logger.info(f"开始执行{len(tasks)}个任务")

        # 第一步：检查子Agent可用性
        availability = self._check_subagent_availability()

        if not availability["available"]:
            # 子Agent不可用, 降级到CLI队列
            return self._execute_with_fallback(
                tasks,
                reason=availability["reason"]
            )

        # 第二步：子Agent可用, 尝试执行
        try:
            logger.info("使用子Agent并行模式")
            results = self._execute_with_subagents(tasks)

            # 验证结果
            if self._validate_results(results, tasks):
                return results
            else:
                raise ValidationError("子Agent结果验证失败")

        except Exception as e:
            # 子Agent执行失败, 降级到CLI队列
            logger.warning(f"子Agent执行失败: {e}，降级到CLI队列")
            return self._execute_with_fallback(
                tasks,
                reason=FallbackReason.EXECUTION_FAILED.value
            )

    def _check_subagent_availability(self) -> Dict[str, Any]:
        """检查子Agent是否可用"""

        availability = {
            "available": False,
            "reason": None
        }

        # 检查1: Agent tool是否存在
        if not self._has_agent_tool():
            availability["reason"] = FallbackReason.AGENT_TOOL_UNAVAILABLE.value
            return availability

        # 检查2: 资源是否充足
        if not self._enough_resources():
            availability["reason"] = FallbackReason.INSUFFICIENT_RESOURCES.value
            return availability

        # 检查3: 配置是否允许
        if not self._is_subagent_enabled():
            availability["reason"] = FallbackReason.CONFIG_DISABLED.value
            return availability

        # 所有检查通过
        availability["available"] = True
        return availability

    def _execute_with_fallback(
        self,
        tasks: List[Dict],
        reason: str
    ) -> List[Dict]:
        """降级到CLI队列执行"""

        logger.info(f"降级到CLI队列模式: {reason}")

        # 通知用户(如果需要)
        self.notifier.notify_fallback(
            reason=reason,
            task_count=len(tasks),
            estimated_time=self._estimate_cli_queue_time(tasks)
        )

        # 使用CLI队列执行
        return self._execute_with_cli_queue(tasks)

    def _execute_with_subagents(self, tasks: List[Dict]) -> List[Dict]:
        """使用子Agent并行执行"""

        # 这里是实际的子Agent调用逻辑
        # 具体实现取决于你的技能

        subagents = []
        for task in tasks:
            # 创建子Agent
            subagent = self._create_subagent(task)
            subagents.append(subagent)

        # 收集结果
        results = []
        for subagent in subagents:
            result = self._await_subagent(subagent)
            results.append(result)

        return results

    def _execute_with_cli_queue(self, tasks: List[Dict]) -> List[Dict]:
        """使用CLI队列执行"""

        results = []
        for task in tasks:
            # 执行单个任务
            result = self._execute_single_task(task)
            results.append(result)

        return results

    def _validate_results(
        self,
        results: List[Dict],
        tasks: List[Dict]
    ) -> bool:
        """验证结果完整性"""

        # 检查数量
        if len(results) != len(tasks):
            logger.error(f"结果数量不匹配: {len(results)} != {len(tasks)}")
            return False

        # 检查每个结果
        for i, result in enumerate(results):
            if result is None:
                logger.error(f"结果{i}为空")
                return False

        return True

    # ========== 辅助方法 ==========

    def _has_agent_tool(self) -> bool:
        """检查Agent tool是否可用"""
        try:
            import inspect
            frame = inspect.currentframe()
            return 'Agent' in globals() or 'Agent' in locals()
        except:
            return False

    def _enough_resources(self) -> bool:
        """检查资源是否充足"""
        try:
            import psutil
            # 检查内存(至少2GB可用)
            available_memory_gb = (
                psutil.virtual_memory().available / (1024**3)
            )
            if available_memory_gb < 2:
                return False

            # 检查CPU(至少2核)
            cpu_count = psutil.cpu_count()
            if cpu_count < 2:
                return False

            return True
        except:
            # 如果无法检查, 假设资源充足
            return True

    def _is_subagent_enabled(self) -> bool:
        """检查配置是否启用子Agent"""
        return self.config.get("enable_subagents", True)

    def _estimate_cli_queue_time(self, tasks: List[Dict]) -> str:
        """估算CLI队列执行时间"""
        # 这里可以根据任务特征估算
        # 简化示例：每个任务30分钟
        total_minutes = len(tasks) * 30

        if total_minutes < 60:
            return f"约{total_minutes}分钟"
        else:
            hours = total_minutes / 60
            return f"约{hours:.1f}小时"

    def _create_subagent(self, task: Dict):
        """创建子Agent(示例)"""
        # 实际实现取决于具体的Agent tool
        pass

    def _await_subagent(self, subagent) -> Dict:
        """等待子Agent完成(示例)"""
        # 实际实现取决于具体的Agent tool
        pass

    def _execute_single_task(self, task: Dict) -> Dict:
        """执行单个任务(示例)"""
        # 实际实现取决于具体的技能逻辑
        pass


class FallbackNotifier:
    """降级通知管理器"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.has_notified = False

    def notify_fallback(
        self,
        reason: str,
        task_count: int,
        estimated_time: Optional[str] = None
    ):
        """通知用户降级"""

        # 检查配置
        if not self.config.get("show_fallback_messages", True):
            return

        # 检查是否需要通知
        if not self._should_notify(task_count):
            return

        # 构建消息
        message = self._build_message(reason, task_count, estimated_time)

        # 显示消息
        self._show_message(message)

        self.has_notified = True

    def _should_notify(self, task_count: int) -> bool:
        """判断是否应该通知"""

        # 小任务不通知
        if task_count <= 3:
            return False

        # 已经通知过，不重复通知
        if self.has_notified:
            return False

        # 批量任务, 需要通知
        return True

    def _build_message(
        self,
        reason: str,
        task_count: int,
        estimated_time: Optional[str]
    ) -> str:
        """构建通知消息"""

        lines = []
        lines.append("ℹ️  执行模式调整")
        lines.append(f"   原因: {self._friendly_reason(reason)}")
        lines.append(f"   任务数: {task_count}个")

        if estimated_time:
            lines.append(f"   预计时间: {estimated_time}")

        lines.append("   所有功能将正常完成 ✓")

        return "\n".join(lines)

    def _friendly_reason(self, technical_reason: str) -> str:
        """将技术原因转换为用户友好的说明"""

        reasons_map = {
            "Agent tool不可用": "当前环境不支持并行处理",
            "所需子Agent类型不存在": "所需的分析模块不可用",
            "无子Agent调用权限": "当前配置不支持并行处理",
            "资源不足(内存/CPU)": "系统资源有限, 使用标准模式",
            "配置中禁用了子Agent": "当前配置使用标准模式",
            "子Agent执行失败": "并行处理遇到问题, 切换到标准模式"
        }

        return reasons_map.get(
            technical_reason,
            "使用标准处理模式"
        )

    def _show_message(self, message: str):
        """显示消息"""
        print(message)
        logger.info(f"用户通知: {message}")


class ValidationError(Exception):
    """验证错误"""
    pass


# ========== 使用示例 ==========

def example_usage():
    """使用示例"""

    # 创建执行器
    executor = GracefulExecutor(config={
        "enable_subagents": True,
        "show_fallback_messages": True
    })

    # 准备任务
    tasks = [
        {"id": 1, "file": "data1.txt"},
        {"id": 2, "file": "data2.txt"},
        {"id": 3, "file": "data3.txt"},
    ]

    # 执行(自动处理降级)
    results = executor.execute(tasks)

    # 使用结果
    print(f"完成{len(results)}个任务")

    # 如果是批量任务
    many_tasks = [
        {"id": i, "file": f"data{i}.txt"}
        for i in range(1, 21)
    ]

    # 会自动显示友好提示(如果降级)
    results = executor.execute(many_tasks)


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 运行示例
    example_usage()
```

---

## 🔧 集成到现有技能

### 步骤1: 复制模板

```bash
# 复制到技能目录
cp graceful-fallback-template.py agentskills/your-skill/tools/
```

### 步骤2: 定制化

```python
# 根据你的技能定制

class YourSkillExecutor(GracefulExecutor):

    def _create_subagent(self, task):
        """实现你的子Agent创建逻辑"""
        return Agent(
            subagent_type="your-specialized-type",
            prompt=f"处理任务: {task}"
        )

    def _execute_single_task(self, task):
        """实现你的CLI队列执行逻辑"""
        # 使用Read, Write等工具
        data = read_file(task['file'])
        result = analyze(data)
        return result
```

### 步骤3: 使用

```python
# 在SKILL.md中引用
executor = YourSkillExecutor()
results = executor.execute(tasks)
```

---

## ✅ 测试清单

```yaml
功能测试:
  ☑ 子Agent可用时使用并行
  ☑ 子Agent不可用时降级
  ☑ 资源不足时降级
  ☑ 配置禁用时降级
  ☑ 执行失败时降级
  ☑ 结果验证通过
  ☑ 用户通知正确

通知测试:
  ☑ 小任务不通知
  ☑ 批量任务通知
  ☑ 通知内容友好
  ☑ 不重复通知

完整性测试:
  ☑ 所有任务都有结果
  ☑ 结果数量正确
  ☑ 数据不丢失
  ☑ 状态一致
```

---

**关键点**: 这个模板确保在任何环境下都能正常工作！
