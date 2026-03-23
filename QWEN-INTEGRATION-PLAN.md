# Qwen CLI 内自动化运行系统

**系统名称**: Qwen Autonomous Execution Engine  
**运行环境**: Qwen CLI 内部  
**自动化级别**: Level 3 - 完全自主

---

## 🎯 核心需求

系统必须在 **Qwen CLI 对话中**：
1. ✅ 自主读取任务计划
2. ✅ 自主执行任务（创建 skill 文件）
3. ✅ 自动质量检查
4. ✅ 自动错误恢复
5. ✅ 持续运行（多轮对话）
6. ✅ 状态持久化（跨会话）

---

## 🤖 实现方案

### 方案 1: Qwen Skill 模式

创建一个 Qwen skill，在对话中调用：

```
用户：启动自动化任务执行
Qwen: 加载 autonomous-execution skill
Qwen: 开始执行任务...
```

### 方案 2: Qwen Plugin 模式

创建一个 Qwen plugin，自动监听并执行：

```
[Plugin: AutoExecutor]
检测到任务计划更新...
开始执行任务...
任务完成！
```

### 方案 3: Qwen Hook 模式

创建 Qwen hooks，在特定事件触发时执行：

```yaml
hooks:
  on_session_start:
    - check_pending_tasks
  on_file_change:
    - trigger_task_execution
```

---

## 📋 实现步骤

### 步骤 1: 创建 Qwen Skill 定义

```yaml
# qwen-skill.yaml
name: autonomous-execution
version: 1.0.0
description: Qwen CLI 内自动化任务执行技能
triggers:
  - "启动自动化"
  - "执行任务"
  - "继续执行"
actions:
  - parse_task_plan
  - execute_task
  - quality_check
  - error_recovery
```

### 步骤 2: 创建对话状态管理

```python
# qwen-state.py
class QwenConversationState:
    def __init__(self):
        self.current_task = None
        self.completed_tasks = []
        self.pending_tasks = []
    
    def save(self):
        # 保存到 Qwen 会话状态
        pass
    
    def load(self):
        # 从 Qwen 会话状态加载
        pass
```

### 步骤 3: 创建自动化执行器

```python
# qwen-auto-executor.py
class QwenAutoExecutor:
    def __init__(self, conversation_state):
        self.state = conversation_state
    
    async def execute_cycle(self):
        # 1. 解析任务计划
        tasks = self.parse_task_plan()
        
        # 2. 执行任务
        for task in tasks:
            result = await self.execute_task(task)
            
            # 3. 质量检查
            if not self.quality_check(result):
                # 4. 错误恢复
                await self.error_recovery(task)
        
        # 5. 更新状态
        self.state.save()
```

### 步骤 4: 创建 Qwen 对话提示词

```markdown
# System Prompt for Qwen Auto-Execution

你是一个自动化任务执行助手。

## 行为规则

1. 当用户说"启动自动化"时，开始执行任务
2. 每轮对话执行一个任务
3. 执行完成后报告结果
4. 询问是否继续执行下一个任务
5. 持续运行直到所有任务完成

## 输出格式

```
📋 任务：{task_name}
🔨 执行中...
✅ 完成！
📊 进度：{completed}/{total}
➡️ 继续执行下一个任务？(是/否)
```
```

---

## 🔄 Qwen CLI 内运行流程

```
用户：启动自动化任务执行

Qwen: 
🤖 自动化任务执行系统启动

📋 当前任务队列:
1. bourdieu-field-analysis-expert
2. actor-network-analysis-expert
3. ...

🔨 开始执行任务 1: bourdieu-field-analysis-expert

[执行中...]

✅ 任务完成！
📊 进度：1/13
➡️ 继续执行下一个任务？(是/否)

用户：是

Qwen:
🔨 开始执行任务 2: actor-network-analysis-expert

[执行中...]

✅ 任务完成！
📊 进度：2/13
➡️ 继续执行下一个任务？(是/否)
```

---

## 📁 需要的文件

1. `qwen-skill.yaml` - Qwen skill 定义
2. `qwen-state.py` - 状态管理
3. `qwen-auto-executor.py` - 执行器
4. `qwen-system-prompt.md` - 系统提示词
5. `qwen-integration.py` - Qwen 集成接口

---

## 🚀 启动方式

### 方式 1: 命令行启动

```bash
qwen "启动自动化任务执行"
```

### 方式 2: Skill 调用

```bash
qwen-skill autonomous-execution --start
```

### 方式 3: 自动触发

```yaml
# .qwen/config.yaml
auto_execute:
  enabled: true
  on_task_plan_change: true
```

---

## ⚙️ 配置选项

```yaml
# .qwen/auto-execution.yaml
execution:
  mode: conversation  # conversation, background, hybrid
  tasks_per_turn: 1   # 每轮对话执行任务数
  auto_continue: true # 自动继续
  quality_check: true # 质量检查
  error_recovery: true # 错误恢复
  
notification:
  on_task_complete: true
  on_error: true
  on_all_complete: true
```

---

**下一步**: 创建完整的 Qwen CLI 集成实现
