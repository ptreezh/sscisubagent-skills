# Stigmergy 多智能体系统

**本平台的多智能体协同系统 - 无需自备 AI 模型算力**

**最后更新**: 2026-03-22  
**安装方式**: npm install -g stigmergy  
**核心特点**: 多 Agent 协同、自动进化、无需自备算力

---

## 🎯 什么是 Stigmergy

**Stigmergy** 是本平台（SocienceAI）的多智能体协同系统，支持多个 AI Agent 协同工作和进化。

**核心优势**:
- ✅ **无需自备 AI 模型算力** - 使用云端 AI 模型
- ✅ **多 Agent 协同** - 多个专家 Agent 协同工作
- ✅ **自动进化** - Agent 间相互学习、共同进化
- ✅ **npm 安装** - 一键安装，开箱即用
- ✅ **技能兼容** - 支持 agentskills.io 规范技能

**适用场景**:
- 复杂社会科学研究（需要多方法论协同）
- 跨学科研究（需要多领域专家）
- 团队协同研究（多用户协作）
- 大规模数据分析（分布式处理）

---

## 🚀 快速开始（5 分钟）

### 步骤 1: 安装 Stigmergy

```bash
# npm 安装（推荐）
npm install -g stigmergy

# 验证安装
stigmergy --version
```

### 步骤 2: 配置 AI 模型

**无需自备算力** - Stigmergy 使用云端 AI 模型：

```bash
# 配置云端 AI（默认配置）
stigmergy config --use-cloud

# 或配置具体 AI 服务
stigmergy config --ai-provider qwen  # 使用通义千问
stigmergy config --ai-provider coze   # 使用 Coze
```

**可选：使用本地模型**（如有）:
```bash
# 配置本地 Ollama
stigmergy config --ai-provider ollama --model qwen2.5

# 配置本地 LM Studio
stigmergy config --ai-provider lm-studio
```

### 步骤 3: 下载技能

```bash
# 下载社会科学方法论技能
git clone https://github.com/socienceai/agentskills.git
cd agentskills
```

### 步骤 4: 加载多 Agent 系统

```bash
# 加载多个专家 Agent
stigmergy load grounded-theory-expert
stigmergy load social-network-analysis-expert
stigmergy load bourdieu-field-analysis-expert

# 查看已加载的 Agent
stigmergy list-agents
```

---

## 📚 使用示例

### 示例 1: 多方法论协同分析

**场景**: 需要同时使用扎根理论和社会网络分析

```bash
# 启动多 Agent 协同
stigmergy use grounded-theory-expert,social-network-analysis-expert "
请对以下研究进行协同分析：

1. 使用扎根理论对访谈数据进行编码
2. 使用社会网络分析分析编码结果的关系网络
3. 综合两种方法的结果，给出研究建议
"
```

**输出**:
```
## 多 Agent 协同分析结果

### Agent 1: 扎根理论专家
## 开放编码结果
1. 工作压力 - "我觉得工作压力很大"
2. 加班现象 - "每天都要加班"
...

### Agent 2: 社会网络分析专家
## 网络分析结果
- 概念节点：5 个
- 关系边：8 条
- 核心概念：工作压力、职业发展
...

### 协同结论
综合两种方法分析，建议：
1. 工作压力是核心范畴
2. 与职业发展呈负相关
3. 需要进一步收集数据验证
...
```

---

### 示例 2: 跨学科研究

**场景**: 需要多个学科专家协同

```bash
# 加载多个学科专家
stigmergy load digital-marx-expert
stigmergy load digital-weber-expert
stigmergy load digital-durkheim-expert

# 启动跨学科分析
stigmergy use digital-marx-expert,digital-weber-expert,digital-durkheim-expert "
请从三个理论视角分析平台经济：

1. 数字马克思视角：分析数字劳动和剩余价值
2. 数字韦伯视角：分析平台科层制和理性化
3. 数字涂尔干视角：分析平台社会的团结形式
4. 综合三个视角，给出综合判断
"
```

---

### 示例 3: 协同进化

**场景**: 多个 Agent 协同工作并共同进化

```bash
# 启动协同进化模式
stigmergy evolve --agents grounded-theory-expert,sna-expert "
研究任务：分析在线社区的社会网络结构

要求：
1. 两个 Agent 协同工作
2. 相互学习对方的方法论
3. 进化出新的分析方法
"
```

**进化过程**:
```
迭代 1:
- 扎根理论 Agent: 编码社区文本数据
- 社会网络 Agent: 分析用户关系网络

迭代 2:
- 扎根理论 Agent: 学习网络分析概念
- 社会网络 Agent: 学习编码方法

迭代 3:
- 协同进化出"网络编码分析法"
- 结合两种方法的优势
```

---

## 🔧 高级功能

### 1. Agent 编排

**定义工作流**:
```yaml
# workflow.yaml
name: 混合方法研究工作流
agents:
  - grounded-theory-expert
  - qca-expert
  - mixed-methods-expert

workflow:
  - agent: grounded-theory-expert
    task: 质性数据分析
    output: coding_results
  
  - agent: qca-expert
    task: QCA 分析
    input: coding_results
    output: qca_results
  
  - agent: mixed-methods-expert
    task: 混合方法整合
    input: coding_results,qca_results
    output: final_report
```

**执行工作流**:
```bash
stigmergy run workflow.yaml
```

---

### 2. 分布式处理

**大规模数据分析**:
```bash
# 启动多个 Worker Agent
stigmergy worker --count 5

# 分配任务
stigmergy distribute "
分析 1000 份访谈数据：
- Worker 1-5: 各分析 200 份
- 使用 grounded-theory-expert
- 结果汇总到主 Agent
"
```

---

### 3. Agent 市场

**浏览可用 Agent**:
```bash
# 查看可用 Agent
stigmergy marketplace list

# 搜索 Agent
stigmergy marketplace search "qualitative"

# 安装 Agent
stigmergy marketplace install agent-name
```

---

### 4. 协同学习

**Agent 间相互学习**:
```bash
# 启动协同学习
stigmergy learn --agents agent1,agent2,agent3 "
学习目标：
1. 分享各自的方法论知识
2. 学习其他 Agent 的专长
3. 形成综合知识库
"
```

---

## 📊 与其他平台对比

| 特性 | Stigmergy | OpenClaw | WorkBuddy | Coze |
|------|---------|---------|---------|------|
| **多 Agent 协同** | ✅ 核心功能 | ❌ 单 Agent | ❌ 单 Agent | ⚠️ 有限 |
| **无需自备算力** | ✅ 云端 AI | ❌ 需自备 | ❌ 需自备 | ✅ 云端 |
| **安装方式** | npm | npm/pip | npm/pip | 网页 |
| **自动进化** | ✅ 协同进化 | ⚠️ 自主进化 | ⚠️ 自主进化 | ❌ |
| **分布式处理** | ✅ 支持 | ❌ | ❌ | ❌ |
| **技能兼容** | ✅ agentskills.io | ✅ agentskills.io | ✅ agentskills.io | ⚠️ 转换 |

---

## ❓ 常见问题

### Q: Stigmergy 需要自备 AI 模型吗？

**A**: 不需要！Stigmergy 默认使用云端 AI 模型，无需自备算力。

当然，如果你有本地模型，也可以配置使用：
```bash
# 使用云端 AI（默认，无需自备算力）
stigmergy config --use-cloud

# 或使用本地模型（需自备算力）
stigmergy config --ai-provider ollama
```

### Q: 如何配置云端 AI？

**A**: 
```bash
# 使用通义千问
stigmergy config --ai-provider qwen --api-key YOUR_API_KEY

# 使用 Coze
stigmergy config --ai-provider coze --api-key YOUR_API_KEY
```

### Q: 多 Agent 如何收费？

**A**: 
- Stigmergy 本身免费开源
- 云端 AI 服务按使用量收费（如通义千问 API）
- 本地模型免费（但需自备算力）

### Q: 如何保证 Agent 协同效果？

**A**: 
1. 选择相关的 Agent（如扎根理论 + 社会网络分析）
2. 定义清晰的协同任务
3. 使用工作流编排
4. 启用协同学习功能

### Q: Stigmergy 与 SocienceAI 平台的关系？

**A**: 
- Stigmergy 是 SocienceAI 平台的多智能体协同系统
- SocienceAI 提供方法论技能
- Stigmergy 提供多 Agent 协同能力
- 两者结合，实现复杂社会科学研究

---

## 📖 相关资源

### 官方文档

- [Stigmergy 官方文档](https://github.com/stigmergy/stigmergy)
- [安装指南](https://github.com/stigmergy/stigmergy/wiki/Installation)
- [使用教程](https://github.com/stigmergy/stigmergy/wiki/Tutorial)
- [API 参考](https://github.com/stigmergy/stigmergy/wiki/API-Reference)

### 技能仓库

- [SocienceAI 技能仓库](https://github.com/socienceai/agentskills)
- [Stigmergy 技能市场](https://github.com/stigmergy/marketplace)

### 社区支持

- [GitHub Discussions](https://github.com/stigmergy/stigmergy/discussions)
- [SocienceAI 社区](https://github.com/socienceai/agentskills/discussions)

---

## 🎯 下一步学习

### 入门教程

1. ✅ 完成本教程
2. [OpenClaw 技能加载教程](/tutorials/openclaw/)
3. [WorkBuddy 技能加载教程](/tutorials/workbuddy/)
4. [Coze 技能导入教程](/tutorials/coze/)

### 进阶教程

1. [多 Agent 协同工作流](/tutorials/stigmergy/workflow/)
2. [Agent 协同进化](/tutorials/stigmergy/evolution/)
3. [分布式处理](/tutorials/stigmergy/distributed/)

### 专业教程

1. [扎根理论多 Agent 分析](/skills/grounded-theory/stigmergy/)
2. [社会网络多 Agent 分析](/skills/social-network-analysis/stigmergy/)
3. [混合方法多 Agent 分析](/skills/mixed-methods/stigmergy/)

---

**教程版本**: 1.0  
**最后更新**: 2026-03-22  
**维护者**: SocienceAI Team

*让社会科学研究人人可为*
