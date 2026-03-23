# 智能体服务技能加载机制分析报告

**分析日期**: 2026-03-22  
**分析范围**: 国内外主流智能体平台  
**分析目的**: 理解技能加载机制，制定最优战略

---

## 📊 智能体平台分类

### 按部署方式分类

```
1. 云端部署型
   - Coze（扣子）
   - Dify
   - FastGPT
   - 通义千问 APP

2. 本地部署型
   - OpenClaw（小龙虾）
   - WorkBuddy
   - Qwen CLI
   - Claude Code

3. 混合部署型
   - LangChain
   - AutoGen
   - CrewAI
```

---

## 🔧 各平台技能加载机制

### 1. OpenClaw（小龙虾）

**平台类型**: 本地部署 CLI 工具  
**技能格式**: Markdown + YAML  
**加载方式**: 文件系统路径

**技能结构**:
```
skill-name/
├── SKILL.md           # 技能定义（角色、工作流程）
├── skill.yaml         # 技能配置（工具、输入输出）
├── tools/             # 工具模块
├── templates/         # 模板文件
└── examples/          # 示例
```

**加载机制**:
```bash
# 方式 1: 自动加载（技能目录）
# 技能放在 ~/.qwen/skills/ 目录
# 启动时自动扫描加载

# 方式 2: 手动指定
qwen --skill /path/to/skill "任务描述"

# 方式 3: 环境变量
export QWEN_SKILL_PATH=/path/to/skills
qwen "任务描述"
```

**技能下载与使用**:
```bash
# 1. 下载技能包
git clone https://github.com/socienceai/agentskills.git
cd agentskills/skill-name

# 2. 复制到技能目录
cp -r skill-name ~/.qwen/skills/

# 3. 使用技能
qwen --skill skill-name "任务描述"
```

**特点**:
- ✅ 完全本地化，数据不出本地
- ✅ 支持技能间调用
- ✅ 支持工具扩展
- ⚠️ 需要一定的命令行基础

---

### 2. WorkBuddy

**平台类型**: 本地部署 CLI 工具  
**技能格式**: Markdown + YAML（与 OpenClaw 兼容）  
**加载方式**: 文件系统路径

**技能结构**: 与 OpenClaw 相同

**加载机制**:
```bash
# 方式 1: 配置技能路径
# 在 workbuddy.config 中配置
skill_paths:
  - /path/to/skills

# 方式 2: 命令行指定
workbuddy --skill /path/to/skill "任务描述"

# 方式 3: 自动发现
# 技能放在~/.workbuddy/skills/自动加载
```

**与 OpenClaw 的兼容性**:
- ✅ 技能格式完全兼容
- ✅ 可以直接复用 OpenClaw 技能
- ✅ 工具模块通用

---

### 3. Coze（扣子）

**平台类型**: 云端部署  
**技能格式**: Bot 配置 + 插件  
**加载方式**: 在线配置

**技能结构**:
```
Bot 配置
├── 人设与回复逻辑
├── 插件配置
├── 知识库
└── 工作流
```

**加载机制**:
```
1. 在线创建 Bot
2. 配置人设（类似 SKILL.md）
3. 添加插件（类似 tools/）
4. 上传知识库（类似 templates/）
5. 发布 Bot
```

**本地技能迁移到 Coze**:
```
步骤 1: 提取 SKILL.md 核心内容
步骤 2: 转换为 Coze 的人设配置
步骤 3: 将 tools/转换为 Coze 插件
步骤 4: 上传 templates/到知识库
步骤 5: 配置工作流
步骤 6: 测试发布
```

**特点**:
- ✅ 无需部署，开箱即用
- ✅ 可视化配置
- ✅ 丰富的插件生态
- ⚠️ 数据在云端
- ⚠️ 技能格式不兼容

---

### 4. Dify

**平台类型**: 云端/本地混合部署  
**技能格式**: YAML 配置 + Python 工具  
**加载方式**: API 或界面配置

**技能结构**:
```
app/
├── config.yaml        # 应用配置
├── prompt.yaml        # 提示词配置
├── tools/             # Python 工具
└── knowledge/         # 知识库
```

**加载机制**:
```bash
# 方式 1: 界面导入
# 通过 Web 界面导入 YAML 配置

# 方式 2: API 部署
curl -X POST https://api.dify.ai/apps \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d @config.yaml

# 方式 3: Docker 部署
docker run -d -v ./apps:/apps dify
```

**特点**:
- ✅ 支持本地部署
- ✅ API 友好
- ✅ 支持工作流编排
- ⚠️ 技能格式需要转换

---

### 5. LangChain

**平台类型**: 开发框架  
**技能格式**: Python 代码  
**加载方式**: 代码导入

**技能结构**:
```python
from langchain.agents import AgentExecutor, Tool
from langchain.memory import ConversationBufferMemory

# 定义工具
tools = [
    Tool(name="工具 1", func=function1),
    Tool(name="工具 2", func=function2),
]

# 定义记忆
memory = ConversationBufferMemory()

# 创建 Agent
agent = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory
)
```

**特点**:
- ✅ 高度灵活
- ✅ 开发者友好
- ✅ 生态丰富
- ⚠️ 需要编程能力

---

### 6. AutoGen（Microsoft）

**平台类型**: 开发框架  
**技能格式**: Python 代码  
**加载方式**: 代码配置

**技能结构**:
```python
from autogen import AssistantAgent, UserProxyAgent

# 配置 Agent
assistant = AssistantAgent(
    name="assistant",
    system_message="你是 XXX 专家",
    llm_config={"config_list": [...]},
)

# 配置用户代理
user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="ALWAYS",
)

# 启动对话
user_proxy.initiate_chat(assistant, message="任务描述")
```

**特点**:
- ✅ 多 Agent 协作
- ✅ 代码执行能力强
- ⚠️ 需要编程能力

---

### 7. FastGPT

**平台类型**: 云端部署  
**技能格式**: 工作流配置  
**加载方式**: 在线配置

**技能结构**:
```
应用
├── 提示词配置
├── 工作流
├── 知识库
└── API 配置
```

**特点**:
- ✅ 可视化工作流
- ✅ 知识库增强
- ⚠️ 技能格式不通用

---

## 📋 技能格式对比

| 平台 | 技能格式 | 加载方式 | 兼容性 | 部署难度 |
|------|---------|---------|--------|---------|
| OpenClaw | Markdown+YAML | 文件路径 | ⭐⭐⭐⭐⭐ | 中 |
| WorkBuddy | Markdown+YAML | 文件路径 | ⭐⭐⭐⭐⭐ | 中 |
| Coze | Bot 配置 | 在线配置 | ⭐⭐ | 低 |
| Dify | YAML+Python | API/界面 | ⭐⭐⭐ | 中 |
| LangChain | Python 代码 | 代码导入 | ⭐⭐⭐⭐ | 高 |
| AutoGen | Python 代码 | 代码配置 | ⭐⭐⭐⭐ | 高 |
| FastGPT | 工作流配置 | 在线配置 | ⭐⭐ | 低 |

---

## 🎯 技能标准化建议

### 通用技能包结构

```
skill-package/
├── SKILL.md              # 技能定义（通用）
├── skill.yaml            # 技能配置（通用）
├── tools/                # 工具模块
│   ├── __init__.py
│   ├── tool1.py
│   └── tool2.py
├── templates/            # 模板文件
│   ├── template1.md
│   └── template2.md
├── examples/             # 使用示例
│   ├── example1.md
│   └── example2.md
├── adapters/             # 平台适配器
│   ├── openclaw/
│   ├── workbuddy/
│   ├── coze/
│   └── dify/
└── README.md             # 使用说明
```

### 平台适配器

**OpenClaw 适配器**:
```yaml
# adapters/openclaw/adapter.yaml
platform: openclaw
skill_path: ~/.qwen/skills/{{skill_name}}
load_command: qwen --skill {{skill_name}}
```

**WorkBuddy 适配器**:
```yaml
# adapters/workbuddy/adapter.yaml
platform: workbuddy
skill_path: ~/.workbuddy/skills/{{skill_name}}
load_command: workbuddy --skill {{skill_name}}
```

**Coze 适配器**:
```yaml
# adapters/coze/adapter.yaml
platform: coze
import_type: bot_config
config_file: bot_config.json
```

**Dify 适配器**:
```yaml
# adapters/dify/adapter.yaml
platform: dify
import_type: api
config_file: app_config.yaml
api_endpoint: https://api.dify.ai/apps
```

---

## 🚀 技能分发策略

### 策略 1: 统一技能包 + 平台适配器

**优点**:
- ✅ 一次开发，多平台部署
- ✅ 维护成本低
- ✅ 用户选择灵活

**缺点**:
- ⚠️ 需要开发适配器
- ⚠️ 平台特性可能无法充分利用

### 策略 2: 平台定制化技能

**优点**:
- ✅ 充分利用平台特性
- ✅ 用户体验最佳

**缺点**:
- ⚠️ 开发成本高
- ⚠️ 维护成本高

### 推荐策略：混合策略

**核心技能**: 统一格式（Markdown+YAML）  
**平台适配**: 开发适配器  
**特性优化**: 针对大平台定制优化

---

## 📚 技能使用教程框架

### 通用教程结构

```
1. 技能介绍
   - 技能功能
   - 适用场景
   - 前置要求

2. 技能下载
   - GitHub 下载
   - Git 克隆
   - 直接下载 ZIP

3. 平台特定加载
   - OpenClaw 加载
   - WorkBuddy 加载
   - Coze 导入
   - Dify 导入
   - 其他平台

4. 使用示例
   - 基础示例
   - 进阶示例
   - 最佳实践

5. 故障排查
   - 常见问题
   - 解决方案
   - 技术支持
```

---

## 💡 战略建议

### 1. 技能格式标准化

**行动**:
- 制定统一的技能格式标准
- 开发平台适配器
- 提供转换工具

### 2. 多平台分发

**行动**:
- GitHub 统一发布
- 各平台技能市场
- 文档中心

### 3. 教程体系

**行动**:
- 通用使用教程
- 平台特定教程
- 视频教程

### 4. 社区建设

**行动**:
- GitHub 社区
- 技能贡献指南
- 用户案例分享

---

**分析完成日期**: 2026-03-22  
**分析师**: SocienceAI Team
