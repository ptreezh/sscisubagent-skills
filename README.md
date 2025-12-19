# SSCI中文社会科学研究AI Subagent技能包

[![npm version](https://badge.fury.io/js/ssci-subagent-skills.svg)](https://badge.fury.io/js/ssci-subagent-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stigmergy Compatible](https://img.shields.io/badge/Stigmergy-Compatible-brightgreen.svg)](https://github.com/ptreezh/stigmergy-CLI-Multi-Agents)

专为中文社会科学研究者设计的专业AI Subagent技能包，兼容7个主流AI CLI工具，支持Stigmergy统一管理。

## 🚀 使用示例

### 基础使用（各CLI通用）
```bash
# Claude Code
claude "请帮我进行开放编码分析，分析这段访谈文本"

# Qwen CLI  
qwen "请计算这个网络的中心性指标"

# iFlow CLI
iflow "请帮我解决研究中的方法论冲突"

# Gemini CLI
gemini "请帮我进行文献检索和分析"

# CodeBuddy CLI
codebuddy "请帮我进行数据统计分析"

# Codex CLI
codex "请帮我进行代码审查"

# QoderCLI
qodercli "请帮我进行项目文档编写"
```

### Stigmergy跨CLI调用
```bash
# 指定CLI执行任务
stigmergy use claude "进行开放编码分析"
stigmergy use qwen "计算网络中心性"
stigmergy use gemini "文献检索分析"

# 智能路由（自动选择最佳CLI）
stigmergy call "进行复杂的社会网络分析"
stigmergy call "处理跨学科的文献综述"

# 跨CLI协作
stigmergy use claude to "编码分析数据" | stigmergy use qwen to "统计验证结果"
```

### 智能体调用示例
```bash
# 直接调用智能体
claude "请使用文献管理专家帮我查找最新的社会网络研究论文"
qwen "请使用扎根理论专家分析这段访谈数据"
iflow "请使用场域分析专家研究中国教育场域"

# 通过Stigmergy跨CLI调用
stigmergy use claude "使用sna-expert分析这个网络数据"
stigmergy use qwen "使用grounded-theory-expert进行编码"
```

## 🎯 支持的AI CLI工具

| 工具 | 版本 | 状态 | 技能识别 | 部署命令 |
|------|------|------|----------|----------|
| **Claude Code** | 2.0.73 | ✅ 完全支持 | ✅ 13/13 | `ssci deploy claude` |
| **Qwen CLI** | 0.5.0 | ✅ 完全支持 | ✅ 13/13 | `ssci deploy qwen` |
| **iFlow CLI** | 0.4.7 | ✅ 完全支持 | ✅ 13/13 | `ssci deploy iflow` |
| **Gemini CLI** | 0.21.0 | ✅ 完全支持 | ✅ 13/13 | `ssci deploy gemini` |
| **CodeBuddy CLI** | 2.20.1 | ✅ 完全支持 | ⚠️ 需适配 | `ssci deploy codebuddy` |
| **Codex CLI** | 0.73.0 | ✅ 完全支持 | ⚠️ 需适配 | `ssci deploy codex` |
| **QoderCLI** | 0.1.15 | ✅ 完全支持 | ❌ 需登录 | `ssci deploy qodercli` |

## 📦 包含内容

### 🧠 专业智能体 (6个)

| 智能体 | 核心技能 | 专业领域 |
|--------|----------|----------|
| **literature-expert** | 文献管理、引用处理、学术写作 | 中文社会科学文献研究 |
| **grounded-theory-expert** | 扎根理论编码、理论构建 | 质性研究方法论 |
| **sna-expert** | 社会网络分析、中心性计算 | 网络科学研究 |
| **field-analysis-expert** | 布迪厄场域分析、资本分析 | 社会学理论研究 |
| **ant-expert** | 行动者网络理论、转译分析 | 科技社会学研究 |
| **chinese-localization-expert** | 中文本土化、学术表达优化 | 跨文化研究 |

### 🛠️ 专业技能包 (13个)

#### 📝 编码技能 (5个)
- `performing-open-coding` - 开放编码：中文质性数据概念识别、初始编码、持续比较
- `performing-axial-coding` - 轴心编码：范畴识别、属性维度分析、关系建立
- `performing-selective-coding` - 选择式编码：核心范畴识别、故事线构建、理论框架整合
- `checking-theory-saturation` - 理论饱和度检验：新概念识别、范畴完善度评估
- `writing-grounded-theory-memos` - 扎根理论备忘录：过程记录、反思分析、理论备忘录

#### 📊 分析技能 (3个)
- `performing-centrality-analysis` - 中心性分析：度中心性、接近中心性、介数中心性、特征向量中心性
- `performing-network-computation` - 网络计算分析：网络构建、基础指标计算、社区检测、网络可视化
- `processing-network-data` - 网络数据处理：关系数据收集、矩阵构建、数据清洗验证

#### 🎓 方法论技能 (1个)
- `resolving-research-conflicts` - 研究冲突解决：理论分歧、方法论争议、解释冲突、价值观分歧

#### 📁 特殊目录技能 (4个)
- `conflict-resolution` - 冲突解决工具
- `mathematical-statistics` - 数理统计分析
- `network-computation` - 网络计算
- `validity-reliability` - 信效度分析

## 🔧 部署方案对比

### 方案1：原生部署（简单直接）
```bash
npm install -g ssci-subagent-skills
ssci deploy --all
```
**优势**：无需额外依赖，直接部署到各CLI
**适用**：个人使用，简单场景

### 方案2：Stigmergy统一管理（推荐）
```bash
npm install -g stigmergy
cp -r skills/* ~/.stigmergy/skills/
stigmergy skill sync
```
**优势**：统一管理、跨CLI路由、技能市场
**适用**：团队协作，复杂场景

### 方案3：OpenSkills适配器
```bash
node adapters/openskills-universal-adapter.js --cli qwen
```
**优势**：深度适配、格式转换、触发优化
**适用**：特殊需求，定制化场景
- `qualitative-analysis-skill` - 质性分析：模式识别、主题提取、解释构建

#### ✍️ 写作技能
- `paper-structure-skill` - 论文结构：IMRAD结构、逻辑框架、章节组织
- `academic-expression-skill` - 学术表达：术语使用、语言规范、文体风格

#### 🔬 方法论技能
- `research-design-skill` - 研究设计：问题构建、假设发展、方法论选择
- `validity-assessment-skill` - 效度评估：内容效度、构念效度、外部效度

## 🔧 使用方法

### 快速开始

1. **安装并部署**
   ```bash
   npm install -g ssci-subagent-skills
   ssci deploy --all
   ```

2. **在AI CLI中使用**
   ```bash
   # Claude Code
   claude
   > 请用扎根理论专家帮我分析这段访谈文本

   # Qwen CLI
   qwen
   > 使用社会网络分析专家分析这个关系数据

   # iFlow CLI
   iflow
   > 请文献管理专家帮我搜索关于数字鸿沟的中文文献
   ```

### 高级用法

```bash
# 检测已安装的AI CLI工具
ssci detect

# 交互式设置和部署
ssci setup

# 部署到特定CLI工具
ssci deploy claude
ssci deploy qwen
ssci deploy iflow

# 验证部署状态
ssci validate
ssci validate --verbose

# 卸载技能包
ssci uninstall --all

# 更新到最新版本
ssci update

# 显示包信息
ssci info
```

### 在研究中的应用

#### 扎根理论研究示例
```bash
# 启动Claude Code
claude

# 对话示例
用户: 我正在进行大学生在线学习体验的扎根理论研究，请使用扎根理论专家帮我进行开放编码

Claude: [自动加载扎根理论专家]
我将帮助您进行扎根理论的开放编码分析。请提供您的访谈文本，我会：

1. **文本预处理**: 清理和分段您的质性数据
2. **概念识别**: 识别有意义的理论概念
3. **初始编码**: 生成行动导向的编码
4. **持续比较**: 在不同数据片段间进行比较
5. **备忘录撰写**: 记录分析过程中的思考和发现

请上传您的访谈文本文件或直接粘贴文本内容...
```

#### 社会网络分析示例
```bash
# 启动Qwen CLI
qwen

# 对话示例
用户: 请使用社会网络分析专家帮我分析企业创新网络数据

Qwen: [自动加载社会网络分析专家]
我将协助您进行社会网络分析。根据您的需求，我可以：

1. **网络数据处理**: 清洗和预处理您的网络数据
2. **中心性分析**: 计算度中心性、介数中心性、特征向量中心性
3. **结构洞分析**: 识别网络中的关键位置和桥梁节点
4. **凝聚子群识别**: 发现有紧密联系的网络群体
5. **网络可视化**: 生成直观的网络关系图

请提供您的网络数据（边列表或邻接矩阵格式），我将开始分析...
```

## 🏗️ 系统架构

```
npm包(ssci-subagent-skills)
    ↓ 一键部署
AI CLI工具 (Claude/Qwen/iFlow)
    ↓ 加载Subagent
专业智能体 (扎根理论专家等)
    ↓ 调用技能工具
专业技能包 (编码/分析/写作技能)
    ↓ 执行分析任务
专业化研究结果
```

## 📋 系统要求

- **Node.js**: 14.0.0 或更高版本
- **AI CLI工具**: Claude Code / Qwen CLI / iFlow CLI (至少一个)
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

## 🔍 部署验证

安装完成后，验证部署是否成功：

```bash
ssci validate --verbose
```

预期输出：
```
🔍 验证部署状态...

📊 验证结果:
  ✓ claude: 完整部署 (6个智能体, 12个技能)
    ✓ 智能体: literature-expert
    ✓ 智能体: grounded-theory-expert
    ✓ 技能: coding/open-coding-skill
    ✓ 技能: analysis/centrality-analysis-skill
    ...
```

## 🤝 贡献

欢迎社区贡献！请访问 [GitHub仓库](https://github.com/ssci-subagent-skills/ssci-subagent-skills) 提交Issue和Pull Request。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Claude Code](https://claude.com/code) - Subagent架构支持
- [Qwen CLI](https://github.com/QwenLM/qwen-code) - 国产CLI工具
- [iFlow CLI](https://github.com/iflow-ai/iflow-cli) - 国产CLI工具
- 中文社会科学研究社区 - 需求反馈和测试

---

**让AI成为中文社会科学研究的得力助手！** 🚀

更多信息请访问: https://github.com/ssci-subagent-skills/ssci-subagent-skills