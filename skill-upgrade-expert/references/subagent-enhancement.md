# 子Agent支持增强版标准

**v5.0.0-cli-native标准 + 子Agent并行处理增强**

---

## 🎯 为什么需要子Agent支持？

### 复杂分析任务的痛点

```yaml
CLI任务队列的局限:

❌ 无法并行处理
  - 10个数据文件必须依次处理
  - 耗时: 10 × 30分钟 = 5小时

❌ 单一context压力
  - 大量数据导致context overflow
  - 质量下降

❌ 无法利用多核
  - CPU资源浪费
  - 效率低下

❌ 适合场景有限
  - 只适合少量、串行任务
  - 不适合大规模分析
```

### 子Agent的优势

```yaml
子Agent并行处理:

✅ 真正的并行执行
  - 10个文件同时处理
  - 耗时: max(30分钟) = 30分钟
  - 加速: 10x

✅ 独立context
  - 每个子Agent有完整context
  - 质量保证

✅ 资源优化
  - 充分利用多核
  - 效率最大化

✅ 适合复杂场景
  - 批量处理
  - 大规模分析
  - 并行计算
```

---

## 📋 增强版标准定义

### Level 3+: CLI原生 + 子Agent支持

```yaml
基础标准（必须）:
  ☑ CLI任务队列支持
  ☑ 状态持久化
  ☑ 模型驱动执行

增强标准（可选）:
  ☑ 子Agent识别策略
  ☑ 子Agent调用规范
  ☑ 结果整合机制
  ☑ 错误处理和恢复

版本标识:
  基础版: v5.0.0-cli-native
  增强版: v5.0.0-cli-native+agent
```

---

## 🔍 决策框架：何时使用子Agent？

### 决策树

```
接收任务
    ↓
任务可以分解为独立子任务？
    ├─ 否 → 使用CLI任务队列（串行）
    └─ 是 → 继续判断
            ↓
        子任务数量 > 5？
            ├─ 否 → 使用CLI任务队列
            └─ 是 → 继续判断
                    ↓
                子任务需要专门能力？
                    ├─ 否 → 使用general-purpose subagent
                    └─ 是 → 使用specialized subagent
```

### 具体判断标准

```yaml
使用CLI任务队列（串行）:
  - 任务数量: 1-5个
  - 任务有强依赖关系
  - 每个任务快速（<10分钟）
  - 总耗时 < 1小时

例子:
  - 单个文件的扎根理论编码
  - 单个数据集的统计分析
  - 单个案例的理论分析

使用子Agent并行:
  - 任务数量: >5个
  - 任务相互独立
  - 每个任务中等耗时（10-60分钟）
  - 总耗时 > 1小时

例子:
  - 10个数据文件的并行分析
  - 20个案例的并行编码
  - 50个文献的并行综述
```

---

## 🛠️ 实施规范

### 1. 子Agent识别策略

```yaml
在SKILL.md中添加:

## 子Agent使用策略

### 触发条件

```python
def should_use_subagents(tasks):
    """判断是否应该使用子Agent"""

    # 条件1: 任务数量
    if len(tasks) <= 5:
        return False, "任务数量少，使用CLI队列"

    # 条件2: 独立性
    if has_dependencies(tasks):
        return False, "任务有依赖，使用CLI队列"

    # 条件3: 时间估算
    total_time = estimate_time(tasks)
    if total_time < 60:  # 分钟
        return False, "总时间短，使用CLI队列"

    # 条件4: 专门能力需求
    if needs_specialization(tasks):
        return True, "需要专门能力，使用子Agent"

    # 默认：使用子Agent并行
    return True, "大量独立任务，使用子Agent"
```

### 子Agent类型选择

```yaml
General Subagent:
  适用: 通用任务
  类型: general-purpose
  示例: 并行文本分析

Specialized Subagent:
  适用: 特定方法论
  类型: [对应技能]
  示例:
    - grounded-theory-coder
    - sna-analyzer
    - data-analyzer
```

### 2. 子Agent调用规范

```yaml
标准调用模式:

def parallel_execute_with_subagents(tasks, subagent_type="general-purpose"):
    """并行执行任务的模板"""

    # 第一步：识别可并行任务
    parallel_tasks = identify_parallel_tasks(tasks)

    # 第二步：分组（如果需要）
    if len(parallel_tasks) > 10:
        batches = create_batches(parallel_tasks, batch_size=10)
    else:
        batches = [parallel_tasks]

    # 第三步：并行执行
    all_results = []
    for batch in batches:
        # 同时启动多个子Agent
        subagents = []
        for task in batch:
            subagent = Agent(
                subagent_type=subagent_type,
                prompt=f"""
                任务: {task['description']}
                输入: {task['input']}
                要求: {task['requirements']}

                请完成后返回:
                1. 执行结果
                2. 质量评估
                3. 遇到的问题
                """,
                run_in_background=True  # 并行执行
            )
            subagents.append(subagent)

        # 等待所有子Agent完成
        for subagent in subagents:
            result = await subagent
            all_results.append(result)

    # 第四步：整合结果
    integrated = integrate_results(all_results)

    return integrated
```

### 3. 结果整合机制

```yaml
整合策略:

策略1: 简单聚合
  适用: 结果相互独立
  方法: 汇总所有结果
  示例: 多个文件的分析结果

策略2: 合并去重
  适用: 结果有重叠
  方法: 去重、合并相似项
  示例: 多个数据源的编码

策略3: 综合分析
  适用: 结果需要进一步处理
  方法: 二次分析、模式识别
  示例: 多个案例的理论分析

策略4: 投票决策
  适用: 需要一致性判断
  方法: 多数投票、一致性检验
  示例: 多个编码者的结果

实现模板:

def integrate_subagent_results(results, strategy="aggregate"):
    """整合子Agent结果"""

    if strategy == "aggregate":
        # 简单聚合
        return {
            "total": len(results),
            "results": results,
            "summary": summarize(results)
        }

    elif strategy == "merge":
        # 合并去重
        merged = merge_and_deduplicate(results)
        return merged

    elif strategy == "analyze":
        # 综合分析
        patterns = identify_patterns(results)
        return {
            "raw_results": results,
            "patterns": patterns,
            "insights": generate_insights(patterns)
        }

    elif strategy == "vote":
        # 投票决策
        return vote_on_results(results)
```

### 4. 错误处理和恢复

```yaml
错误处理策略:

策略1: 重试机制
  - 失败的任务自动重试
  - 最多重试3次
  - 记录失败原因

策略2: 降级处理
  - 子Agent失败 → 降级到CLI队列
  - 并行失败 → 降级到串行
  - 记录降级原因

策略3: 部分成功
  - 部分子Agent失败
  - 使用成功的结果
  - 标记失败的任务

实现:

def execute_with_fallback(tasks):
    """带回退机制的执行"""

    try:
        # 尝试并行执行
        results = parallel_execute_with_subagents(tasks)
        return results, "success"

    except SubagentError as e:
        # 降级到CLI队列
        log_error(e)
        results = execute_with_cli_queue(tasks)
        return results, "degraded"

    except Exception as e:
        # 完全失败
        log_error(e)
        return None, "failed"
```

---

## 📝 SKILL.md更新模板

### 添加子Agent章节

```markdown
## CLI原生集成 + 子Agent支持

### 任务队列支持

#### 模式1: CLI任务队列（基础）

**适用场景**: 少量任务（1-5个）、有依赖关系

**实现**:
- 使用TaskCreate/TaskUpdate/TaskGet
- 主Agent依次执行
- 状态持久化到文件

**示例**:
```yaml
任务:
  - 任务1: 数据加载
  - 任务2: 数据清洗
  - 任务3: 数据分析

执行: 串行执行
```

#### 模式2: 子Agent并行（增强）

**适用场景**: 大量独立任务（>5个）、需要并行加速

**实现**:
- 识别可并行任务
- 使用Agent tool调用子Agent
- 并行执行、结果整合

**示例**:
```yaml
任务:
  - 文件1: 分析
  - 文件2: 分析
  - ...
  - 文件10: 分析

执行: 10个子Agent并行
加速: 10x
```

### 决策流程

```python
# 任务分析
if 任务数量 <= 5 or 有依赖关系:
    使用CLI任务队列
else:
    使用子Agent并行

# 执行
if 使用子Agent:
    results = parallel_execute_with_subagents(tasks)
else:
    results = execute_with_cli_queue(tasks)
```

### 状态持久化

无论使用哪种模式，都持久化到:

**会话层**: .claude/session/
**项目层**: project/tasks/
**学习层**: experience/ & cases/
```

---

## 🎓 实战案例

### 案例1: 批量扎根理论编码

**场景**: 10个访谈文件的编码

```yaml
不使用子Agent:
  时间: 10 × 30分钟 = 5小时
  方式: 依次处理每个文件

使用子Agent:
  时间: max(30分钟) = 30分钟
  方式: 10个子Agent并行

实现:

def batch_coding_with_subagents(files):
    # 启动10个子Agent
    subagents = []
    for file in files:
        subagent = Agent(
            subagent_type="grounded-theory-coder",
            prompt=f"""
            对文件 {file} 进行开放编码。

            要求:
            1. 逐行编码
            2. 识别概念
            3. 不预设结论
            4. 返回编码结果
            """,
            run_in_background=True
        )
        subagents.append(subagent)

    # 等待所有完成
    all_codes = []
    for subagent in subagents:
        codes = await subagent
        all_codes.append(codes)

    # 整合结果
    integrated_codes = integrate_coding_results(all_codes)

    return integrated_codes
```

### 案例2: 并行社会网络分析

**场景**: 20个时间点的网络演化分析

```yaml
不使用子Agent:
  时间: 20 × 15分钟 = 5小时

使用子Agent:
  时间: max(15分钟) = 15分钟

实现:

def temporal_sna_parallel(time_points):
    # 每个时间点一个子Agent
    subagents = []
    for tp in time_points:
        subagent = Agent(
            subagent_type="sna-analyzer",
            prompt=f"""
            分析时间点 {tp} 的网络结构。

            计算:
            1. 中心性指标
            2. 社区结构
            3. 结构洞

            返回: 完整分析结果
            """,
            run_in_background=True
        )
        subagents.append(subagent)

    # 收集结果
    networks = []
    for subagent in subagents:
        network = await subagent
        networks.append(network)

    # 分析演化模式
    evolution = analyze_evolution(networks)

    return evolution
```

### 案例3: 大规模文献综述

**场景**: 50篇文献的并行分析

```yaml
挑战:
  - 文献数量多
  - 需要提取关键信息
  - 需要识别模式

解决方案:

def literature_review_parallel(papers):
    # 分批处理（每批10个）
    batches = create_batches(papers, batch_size=10)

    all_results = []
    for batch in batches:
        # 每批并行处理
        subagents = []
        for paper in batch:
            subagent = Agent(
                subagent_type="literature-analyzer",
                prompt=f"""
                分析文献: {paper['title']}

                提取:
                1. 研究问题
                2. 方法
                3. 主要发现
                4. 理论框架
                """,
                run_in_background=True
            )
            subagents.append(subagent)

        # 收集这批的结果
        for subagent in subagents:
            result = await subagent
            all_results.append(result)

    # 综合分析
    synthesis = synthesize_literature(all_results)

    return synthesis
```

---

## ✅ 验证清单

### 增强版认证检查

```yaml
基础检查（v5.0.0-cli-native）:
  ☑ CLI任务队列支持
  ☑ 状态持久化
  ☑ 模型驱动执行
  ☑ 其他Level 1-4要求

增强检查（+agent）:
  ☑ 子Agent使用策略文档化
  ☑ 子Agent调用代码示例
  ☑ 结果整合机制
  ☑ 错误处理机制
  ☑ 实战案例展示
  ☑ 性能对比数据

版本标识:
  基础版: v5.0.0-cli-native
  增强版: v5.0.0-cli-native+agent
```

---

## 📊 性能对比

### 实测数据（假设）

```yaml
场景: 10个文件的扎根理论编码

CLI任务队列:
  文件数: 10
  每文件: 30分钟
  总时间: 300分钟（5小时）
  Context使用: 高（累积）

子Agent并行:
  文件数: 10
  每文件: 30分钟
  总时间: 35分钟（启动5分钟 + 处理30分钟）
  Context使用: 低（每个独立）

加速比: 8.6x ⚡
```

---

## 🎯 实施建议

### 渐进式采用

```yaml
阶段1: 保持CLI队列（当前）
  - 所有技能已实现
  - 适合大多数场景

阶段2: 识别需要并行的技能
  - grounded-theory-expert（批量编码）
  - sna-expert（多时间点分析）
  - data-analysis-expert（多文件处理）

阶段3: 为特定技能添加子Agent
  - 作为可选功能
  - 保持向后兼容
  - 提供开关控制

阶段4: 文档和验证
  - 更新SKILL.md
  - 添加examples
  - 性能测试
```

---

## 🔄 更新现有技能

### 为技能添加子Agent支持

```yaml
步骤1: 评估需求
  - 这个技能是否经常处理大量独立任务？
  - 是否有明显性能瓶颈？
  - 用户是否抱怨速度慢？

步骤2: 设计子Agent策略
  - 何时使用子Agent？
  - 使用什么类型的子Agent？
  - 如何整合结果？

步骤3: 实现并测试
  - 实现并行处理逻辑
  - 测试正确性
  - 测试性能提升

步骤4: 文档更新
  - 在SKILL.md中说明
  - 添加examples/with-subagents.md
  - 更新README

步骤5: 标识版本
  - v5.0.0-cli-native（基础）
  - v5.0.0-cli-native+agent（增强）
```

---

## 🎉 总结

```yaml
增强版标准:

v5.0.0-cli-native:
  ✅ CLI任务队列
  ✅ 适合大多数场景
  ✅ 简单可靠

v5.0.0-cli-native+agent:
  ✅ CLI任务队列 + 子Agent并行
  ✅ 适合复杂大规模场景
  ✅ 性能提升显著（5-10x）

灵活性:
  - 可选增强
  - 向后兼容
  - 按需启用

适用性:
  - 大多数技能: CLI队列即可
  - 复杂分析: 添加子Agent
  - 批量处理: 强烈推荐子Agent
```

---

**下一步**: 选择1-2个技能，示范如何添加子Agent支持！
