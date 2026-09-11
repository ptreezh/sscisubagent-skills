# Qwen CLI 内自动化运行系统

**运行环境**: Qwen CLI  
**自动化级别**: Level 3 - 完全自主  
**状态**: ✅ 已实现

---

## 🚀 快速开始

### 方式 1: 对话启动

在 Qwen CLI 中输入：

```
启动自动化任务执行
```

Qwen 将响应：

```
✅ 自动化系统已启动

```
tasks: 6
mode: conversation
auto_continue: true
```

开始执行第一个任务...

📋 任务：bourdieu-field-analysis-expert
🔨 执行中...
✅ 完成！
📊 进度：1/6
➡️ 继续执行下一个任务？(是/否)
```

### 方式 2: 命令启动

```bash
python qwen-auto-executor.py start
```

### 方式 3: 持续对话

```
用户：启动自动化

Qwen: ✅ 已启动，开始执行...

用户：继续

Qwen: ✅ 任务完成，继续下一个...

用户：状态

Qwen: 📊 当前状态...
```

---

## 📋 可用命令

| 命令 | 说明 | 示例 |
|------|------|------|
| start | 启动自动化 | `启动自动化` |
| execute | 执行一轮 | `执行任务` |
| status | 查看状态 | `状态` |
| stop | 停止 | `停止` |
| continue | 继续 | `继续` |

---

## 🔄 对话流程

```
┌─────────────────────────────────────────────────────────┐
│              Qwen CLI 对话流程                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  用户：启动自动化                                        │
│       ↓                                                 │
│  Qwen: 加载 autonomous-execution skill                  │
│       ↓                                                 │
│  Qwen: 解析任务计划                                      │
│       ↓                                                 │
│  Qwen: 执行第一个任务                                    │
│       ↓                                                 │
│  Qwen: 报告结果 + 询问继续                               │
│       ↓                                                 │
│  用户：继续                                             │
│       ↓                                                 │
│  Qwen: 执行下一个任务                                    │
│       ↓                                                 │
│  ... 循环直到所有任务完成                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ⚙️ 配置选项

编辑 `qwen-skill.yaml`:

```yaml
config:
  mode: conversation  # conversation, background
  tasks_per_turn: 1   # 每轮对话执行任务数
  auto_continue: true # 自动继续
  quality_check: true # 质量检查
  error_recovery: true # 错误恢复
```

---

## 📊 状态持久化

系统自动保存状态到：

- `qwen-automation-state.json` - 执行状态
- `QWEN-AUTO-LOG.md` - 执行日志

跨会话继续：

```
用户：继续之前的自动化

Qwen: 📊 加载状态...
      已完成：5 个任务
      待执行：1 个任务
      继续执行？
```

---

## 🎯 自动化功能

### 1. 智能任务解析 ✅

```
Qwen: 📋 解析 task_plan.md...
      找到 6 个待办任务
      按优先级排序
```

### 2. 完整内容生成 ✅

```
Qwen: 🔨 生成 skill 内容...
      ✅ 创建 9 个文件/目录
```

### 3. 自动质量检查 ✅

```
Qwen: 🔍 质量检查...
      ✅ 文件存在性
      ✅ 文件大小
      ✅ YAML 格式
      ✅ Markdown 结构
      ✅ Python 语法
      ✅ 配置完整性
```

### 4. 自动错误恢复 ✅

```
Qwen: ⚠️ 执行失败，启动错误恢复...
      策略 1: 清理并重新生成
      策略 2: 简化模板
      策略 3: 跳过任务
```

---

## 📁 文件结构

```
agentskills/
├── qwen-skill.yaml           # Qwen skill 配置
├── qwen-auto-executor.py     # 自动执行器
├── qwen-automation-state.json # 状态文件
├── QWEN-AUTO-LOG.md          # 日志文件
└── task_plan.md              # 任务计划
```

---

## 🔧 集成到 Qwen CLI

### 步骤 1: 复制 skill 到 Qwen 目录

```bash
cp qwen-skill.yaml ~/.qwen/skills/autonomous-execution/
cp qwen-auto-executor.py ~/.qwen/skills/autonomous-execution/
```

### 步骤 2: 注册 skill

```bash
qwen skill register autonomous-execution
```

### 步骤 3: 启用 skill

```bash
qwen skill enable autonomous-execution
```

### 步骤 4: 使用

```bash
qwen "启动自动化任务执行"
```

---

## 💡 使用示例

### 示例 1: 启动并持续执行

```
用户：启动自动化任务执行

Qwen: ✅ 自动化系统已启动
      
      开始执行第一个任务：bourdieu-field-analysis-expert
      🔨 执行中...
      ✅ 完成！
      📊 进度：1/6
      ➡️ 继续执行下一个任务？(是/否)

用户：是

Qwen: 🔨 执行第二个任务：actor-network-analysis-expert
      🔨 执行中...
      ✅ 完成！
      📊 进度：2/6
      ➡️ 继续执行下一个任务？(是/否)
```

### 示例 2: 查看状态

```
用户：自动化状态

Qwen: 📊 自动化系统状态
      
      ```
      status: running
      completed: 2
      failed: 0
      pending: 4
      turns: 2
      ```
```

### 示例 3: 停止并恢复

```
用户：停止

Qwen: ⏹️ 自动化系统已停止
      已完成：2 个任务

[稍后]

用户：继续自动化

Qwen: 📊 加载状态...
      已完成：2 个任务
      待执行：4 个任务
      继续执行？
```

---

## 🎯 与独立脚本的区别

| 特性 | 独立脚本 | Qwen CLI 集成 |
|------|----------|--------------|
| 运行环境 | Python | Qwen CLI 对话 |
| 交互方式 | 命令行 | 自然语言 |
| 状态管理 | 文件 | Qwen 会话 + 文件 |
| 错误处理 | 自动 | 自动 + 用户确认 |
| 持续性 | 后台运行 | 对话轮次 |
| 适用场景 | 批量执行 | 交互式执行 |

---

## 🚀 下一步

1. ✅ 系统已实现
2. ⏳ 复制到 Qwen 目录
3. ⏳ 注册 skill
4. ⏳ 测试对话流程

---

**Qwen CLI 内自动化系统已实现！可以在 Qwen 对话中自动化持续运行！**
