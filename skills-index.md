# 社会科学方法论技能包

**让专业方法论技能在你的 AI 工具中运行**

---

## 🎯 什么是方法论技能

**方法论技能**是专门为社会科学研究的 AI 助手设计的专业能力包，包含：

- ✅ 完整的方法论规范
- ✅ 标准化的工作流程
- ✅ 可执行的工具模块
- ✅ 丰富的模板示例

**支持平台**:
- 🦞 OpenClaw（小龙虾）
- 💼 WorkBuddy
- 🤖 Coze（扣子）
- ⚙️ Dify
- 🔧 LangChain
- 🤖 AutoGen

---

## 📦 可用技能包（12 种）

### 质性研究方法

| 技能 | 对标学者 | 核心功能 | 下载 |
|------|---------|---------|------|
| **扎根理论** | Kathy Charmaz | 开放编码、轴心编码、选择式编码 | [下载](#) |
| **社会网络分析** | Linton Freeman | 中心性分析、社区检测、结构洞 | [下载](#) |
| **行动者网络理论** | Bruno Latour | 行动者识别、转译过程、网络追踪 | [下载](#) |
| **布迪厄场域分析** | Pierre Bourdieu | 场域识别、资本分析、习性分析 | [下载](#) |

### 定量研究方法

| 技能 | 对标学者 | 核心功能 | 下载 |
|------|---------|---------|------|
| **QCA 定性比较分析** | Charles Ragin | 模糊集校准、真值表、布尔最小化 | [下载](#) |
| **DID 双重差分** | Angrist & Pischke | 平行趋势检验、双向固定效应 | [下载](#) |
| **回归分析** | Ronald Fisher | OLS 估计、假设检验、模型诊断 | [下载](#) |
| **问卷设计** | Don A. Dillman | 问题设计、抽样方法、信效度检验 | [下载](#) |

### 混合方法与社会理论

| 技能 | 对标学者 | 核心功能 | 下载 |
|------|---------|---------|------|
| **混合方法研究** | John Creswell | 三角验证、互补设计、转换整合 | [下载](#) |
| **数字马克思分析** | David Harvey | 数字劳动、剩余价值、意识形态批判 | [下载](#) |
| **数字涂尔干分析** | Émile Durkheim | 集体意识、社会团结、神圣世俗 | [下载](#) |
| **数字韦伯分析** | Max Weber | 理性化、科层制、祛魅 | [下载](#) |

---

## 🚀 快速开始（5 分钟）

### 步骤 1: 选择你的平台

**本地部署型**（数据不出本地）:
- [OpenClaw 使用教程](/tutorials/openclaw/)
- [WorkBuddy 使用教程](/tutorials/workbuddy/)

**云端部署型**（开箱即用）:
- [Coze 使用教程](/tutorials/coze/)
- [Dify 使用教程](/tutorials/dify/)

### 步骤 2: 下载技能包

**方式 1: Git 克隆（推荐）**:
```bash
git clone https://github.com/socienceai/agentskills.git
cd agentskills
```

**方式 2: 下载 ZIP**:
1. 访问 [GitHub 仓库](https://github.com/socienceai/agentskills)
2. 点击 "Code" → "Download ZIP"
3. 解压到本地

**方式 3: 单个技能下载**:
```bash
# 以扎根理论为例
git clone https://github.com/socienceai/agentskills.git grounded-theory-expert
```

### 步骤 3: 加载技能

**OpenClaw/WorkBuddy**:
```bash
# 复制到技能目录
cp -r grounded-theory-expert ~/.openclaw/skills/

# 加载使用
openclaw --skill grounded-theory-expert "任务描述"
```

**Coze**:
1. 创建新 Bot
2. 配置人设（复制 SKILL.md 内容）
3. 添加插件（对应 tools/）
4. 上传知识库（对应 templates/）
5. 发布 Bot

**Dify**:
1. 导入应用配置
2. 配置提示词
3. 添加工具
4. 上传知识库
5. 发布应用

---

## 📚 详细教程

### 平台特定教程

- [OpenClaw（小龙虾）技能加载教程](/tutorials/openclaw/)
  - 安装 OpenClaw
  - 下载技能包
  - 配置技能路径
  - 加载和使用技能
  - 常见问题解答

- [WorkBuddy 技能加载教程](/tutorials/workbuddy/)
  - 安装 WorkBuddy
  - 技能兼容性说明
  - 加载和使用技能
  - 与 OpenClaw 的区别

- [Coze（扣子）技能导入教程](/tutorials/coze/)
  - 创建 Bot
  - 配置人设
  - 添加插件
  - 上传知识库
  - 发布 Bot

- [Dify 技能导入教程](/tutorials/dify/)
  - 创建应用
  - 配置 YAML
  - 添加工具
  - 部署应用

### 通用教程

- [什么是技能？](/tutorials/what-are-skills/)
- [如何下载技能包？](/tutorials/how-to-download/)
- [如何选择平台？](/tutorials/how-to-choose-platform/)
- [技能开发与定制](/tutorials/skill-development/)
- [故障排查指南](/tutorials/troubleshooting/)

---

## 💡 使用示例

### 示例 1: 扎根理论分析

**平台**: OpenClaw

```bash
# 加载技能
openclaw --skill grounded-theory-expert

# 输入任务
请对以下访谈数据进行开放编码：

"我觉得工作压力很大，每天都要加班，
但是没有明确的晋升通道，感觉很迷茫。"
```

**输出**:
```
## 开放编码结果

### 初始概念
1. 工作压力 - "我觉得工作压力很大"
2. 加班现象 - "每天都要加班"
3. 晋升困境 - "没有明确的晋升通道"
4. 迷茫情绪 - "感觉很迷茫"

### 下一步建议
1. 进行轴心编码，建立概念间关系
2. 收集更多数据进行持续比较
3. 撰写备忘录记录编码思考
```

### 示例 2: 社会网络分析

**平台**: Coze

**Bot 配置**:
- 名称：社会网络分析专家
- 人设：专业的社会网络分析助手
- 插件：数据分析、可视化

**用户输入**:
```
请分析以下社会网络：
节点：A, B, C, D, E
关系：A-B, A-C, B-C, B-D, C-E, D-E
```

**Bot 回复**:
```
## 社会网络分析结果

### 网络特征
- 节点数：5
- 边数：6
- 密度：0.6

### 中心性分析
| 节点 | 度中心性 | 中介中心性 |
|------|---------|-----------|
| B    | 0.75    | 0.33      |
| C    | 0.75    | 0.33      |

### 关键发现
B 和 C 是网络中的关键节点
```

---

## ❓ 常见问题

### Q: 什么是技能？

**A**: 技能是为 AI 助手设计的专业能力包，包含方法论规范、工作流程、工具模块和使用示例。

### Q: 如何下载技能？

**A**: 可以通过 Git 克隆、下载 ZIP 或单个技能下载。详见[下载教程](/tutorials/how-to-download/)。

### Q: 支持哪些平台？

**A**: 支持 OpenClaw、WorkBuddy、Coze、Dify、LangChain、AutoGen 等主流平台。

### Q: 技能收费吗？

**A**: 完全免费开源，遵循 MIT 许可证。

### Q: 如何贡献技能？

**A**: 欢迎通过 GitHub 提交 PR，详见[贡献指南](/contributing/)。

### Q: 遇到问题怎么办？

**A**: 查看[故障排查指南](/tutorials/troubleshooting/)，或在 GitHub 提 Issue。

---

## 🔗 相关资源

### 技能仓库

- [GitHub 技能仓库](https://github.com/socienceai/agentskills)
- [技能包下载](https://github.com/socienceai/agentskills/archive/main.zip)
- [技能开发文档](https://github.com/socienceai/agentskills/wiki/Skill-Development)

### 平台文档

- [OpenClaw 文档](https://github.com/openclaw/openclaw)
- [WorkBuddy 文档](https://github.com/workbuddy/workbuddy)
- [Coze 文档](https://www.coze.cn/docs)
- [Dify 文档](https://docs.dify.ai)

### 社区支持

- [GitHub Discussions](https://github.com/socienceai/agentskills/discussions)
- [Issues](https://github.com/socienceai/agentskills/issues)
- [社区微信群](#)（扫码加入）

---

## 📧 联系我们

**技术支持**: support@socienceai.com  
**商务合作**: business@socienceai.com  
**社区讨论**: [GitHub Discussions](https://github.com/socienceai/agentskills/discussions)

---

## 🎯 下一步

- [查看技能列表](#可用技能包)
- [阅读使用教程](#详细教程)
- [下载技能包](#步骤 2 下载技能包)
- [查看使用示例](#使用示例)

---

**最后更新**: 2026-03-22  
**维护者**: SocienceAI Team

*让社会科学研究人人可为*
