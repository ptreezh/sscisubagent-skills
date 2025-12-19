# SSCI中文社会科学研究技能包 - iFlow CLI 集成指南

## 📋 项目概述

**项目名称**: SSCI Subagent Skills (中文社会科学研究AI技能包)  
**版本**: 1.2.9  
**类型**: 混合项目 (Node.js + Python)  
**许可证**: MIT  
**仓库**: https://github.com/ssci-subagent-skills/ssci-subagent-skills

### 项目简介

这是一个专为中文社会科学研究者设计的专业AI技能包，兼容多个主流AI CLI工具（Claude Code、Qwen CLI、iFlow CLI等）。项目提供了完整的研究工具链，包括扎根理论编码、社会网络分析、文献管理等专业功能。

### 核心特性

- 🧠 **6个专业智能体** - 涵盖文献管理、扎根理论、社会网络分析、场域分析等
- 🛠️ **13个专业技能** - 包括开放编码、中心性分析、理论饱和度检验等
- 🌐 **多CLI支持** - 兼容Claude Code、Qwen CLI、iFlow CLI
- 🇨🇳 **中文优化** - 专门针对中文研究语境优化
- 🚀 **智能部署** - 提供多种部署方式和自动化工具
- 📊 **可视化界面** - 包含Web界面和命令行工具

---

## 🏗️ 项目架构

### 技术栈

#### Node.js 组件
- **运行时**: Node.js >= 14.0.0
- **包管理**: npm
- **核心依赖**:
  - `commander` - CLI命令框架
  - `inquirer` - 交互式命令行
  - `chalk` - 终端颜色输出
  - `fs-extra` - 文件系统操作
  - `ora` - 加载动画

#### Python 组件
- **运行时**: Python >= 3.8
- **包管理**: pip / uv (推荐)
- **核心依赖**:
  - `jieba` >= 0.42.0 - 中文分词
  - `networkx` >= 3.0.0 - 网络分析
  - `pandas` >= 1.5.0 - 数据处理
  - `numpy` >= 1.20.0 - 数值计算
  - `matplotlib` >= 3.5.0 - 数据可视化

### 目录结构

```
sscisubagent-skills/
├── agents/                    # 专业智能体定义
│   ├── literature-expert.md
│   ├── grounded-theory-expert.md
│   ├── sna-expert.md
│   ├── field-analysis-expert.md
│   ├── ant-expert.md
│   └── chinese-localization-expert.md
├── skills/                    # 技能包
│   ├── coding/               # 编码分析技能
│   │   ├── performing-open-coding/
│   │   ├── performing-axial-coding/
│   │   ├── performing-selective-coding/
│   │   ├── checking-theory-saturation/
│   │   └── writing-grounded-theory-memos/
│   ├── analysis/             # 数据分析技能
│   │   ├── performing-centrality-analysis/
│   │   ├── performing-network-computation/
│   │   └── processing-network-data/
│   ├── methodology/          # 方法论技能
│   │   └── resolving-research-conflicts/
│   ├── mathematical-statistics/
│   ├── validity-reliability/
│   └── conflict-resolution/
├── bin/                      # CLI可执行文件
│   └── ssci-cli.js
├── scripts/                  # 部署和工具脚本
│   ├── deploy-commands.js
│   ├── postinstall.js
│   └── utils.js
├── adapters/                 # CLI适配器
│   ├── iflow-cli-adapter.js
│   └── qwen-cli-adapter.js
├── tests/                    # 测试套件
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── performance/
├── tools/                    # Python工具
│   └── paper_search_tools.py
├── demo/                     # 示例代码
│   └── skill_demo.py
├── config/                   # 配置文件
│   └── subagent-skills-mapping.md
├── knowledge-base/           # 知识库
│   ├── core-concepts.md
│   ├── dynamic-loader.md
│   └── main-knowledge.md
├── skills_launcher.py        # 技能启动器
├── smart_deploy.py           # 智能部署器
├── web_interface.py          # Web界面
├── validate_skills.py        # 技能验证工具
├── package.json              # Node.js配置
├── pyproject.toml            # Python项目配置
├── requirements.txt          # Python依赖
└── README.md                 # 项目文档
```

---

## 🚀 安装与部署

### 方式1: NPM全局安装（推荐）

```bash
# 全局安装npm包
npm install -g ssci-subagent-skills

# 一键部署到所有AI CLI工具
ssci deploy --all

# 或使用交互式设置
ssci setup
```

### 方式2: 本地开发安装

```bash
# 克隆仓库
git clone https://github.com/ssci-subagent-skills/ssci-subagent-skills.git
cd sscisubagent-skills

# 安装Node.js依赖
npm install

# 安装Python依赖（推荐使用uv）
pip install -r requirements.txt
# 或使用uv（更快）
uv sync

# 运行智能部署器
python smart_deploy.py --deploy
```

### 方式3: 部署到特定CLI

```bash
# 部署到iFlow CLI
ssci deploy iflow

# 部署到Claude Code
ssci deploy claude

# 部署到Qwen CLI
ssci deploy qwen
```

### 验证部署

```bash
# 检测已安装的CLI工具
ssci detect

# 验证部署状态
ssci validate --verbose

# 查看技能包信息
ssci info
```

---

## 💻 使用方法

### 在iFlow CLI中使用

启动iFlow CLI后，技能会自动加载。你可以直接使用自然语言触发相应的技能：

```bash
# 启动iFlow CLI
iflow

# 使用示例
> 请帮我进行中文开放编码分析
> 分析这个社交网络的中心性
> 检验理论是否达到饱和
> 使用扎根理论专家分析这段访谈文本
```

### 使用命令行启动器

```bash
# 启动交互式技能选择器
python skills_launcher.py

# 显示欢迎界面
python skills_launcher.py --welcome

# 快速启动最近使用的技能
python skills_launcher.py --quick
```

### 使用Web界面

```bash
# 安装Web依赖（首次使用）
pip install flask flask-cors

# 启动Web服务
python web_interface.py

# 在浏览器中访问
# http://127.0.0.1:5000
```

### 直接调用Python工具

```bash
# 中文文本预处理
python skills/coding/open-coding/scripts/preprocess.py --input interview.txt

# 网络中心性分析
python skills/analysis/centrality-analysis/scripts/centrality.py --input network.json

# 理论饱和度检验
python skills/coding/theory-saturation/scripts/assess_saturation.py --data-dir data/
```

---

## 📚 核心技能详解

### 编码分析技能（5个）

1. **performing-open-coding** - 开放编码
   - 中文质性数据的概念识别
   - 初始编码和持续比较
   - 支持jieba中文分词

2. **performing-axial-coding** - 轴心编码
   - 范畴识别和属性维度分析
   - 关系建立和Paradigm构建

3. **performing-selective-coding** - 选择式编码
   - 核心范畴识别
   - 故事线构建和理论框架整合

4. **checking-theory-saturation** - 理论饱和度检验
   - 新概念识别
   - 范畴完善度评估

5. **writing-grounded-theory-memos** - 扎根理论备忘录写作
   - 过程记录和反思分析
   - 理论备忘录和编码备忘录

### 数据分析技能（3个）

1. **performing-centrality-analysis** - 中心性分析
   - 度中心性、接近中心性
   - 介数中心性、特征向量中心性

2. **performing-network-computation** - 网络计算分析
   - 网络构建和基础指标计算
   - 社区检测和网络可视化

3. **processing-network-data** - 网络数据处理
   - 关系数据收集
   - 矩阵构建和数据清洗验证

### 方法论技能（1个）

1. **resolving-research-conflicts** - 研究冲突解决
   - 理论分歧处理
   - 方法论争议解决

---

## 🧪 测试与验证

### 运行测试套件

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行单元测试
python -m pytest tests/unit/ -v

# 运行集成测试
python -m pytest tests/integration/ -v

# 运行端到端测试
python -m pytest tests/e2e/ -v

# 运行性能测试
python -m pytest tests/performance/ -v

# 生成覆盖率报告
python -m pytest tests/ --cov=skills --cov-report=html
```

### 验证技能格式

```bash
# 验证所有技能的YAML frontmatter
python validate_skills.py

# 查看验证报告
cat skills_validation_report.txt
```

### 系统诊断

```bash
# 运行智能诊断
python smart_deploy.py --diagnose

# 生成使用指南
python smart_deploy.py --guide

# 创建快速启动脚本
python smart_deploy.py --quick-start
```

---

## 🔧 开发与扩展

### 添加新技能

1. 创建技能目录结构：
```bash
mkdir -p skills/new-category/new-skill
cd skills/new-category/new-skill
```

2. 创建SKILL.md文件（必须包含YAML frontmatter）：
```markdown
---
name: new-skill
description: 技能描述和使用时机
---

# 技能详细内容
...
```

3. 添加Python脚本（可选）：
```bash
mkdir scripts
touch scripts/main.py
```

4. 验证技能格式：
```bash
python validate_skills.py
```

### 添加新智能体

1. 在`agents/`目录创建Markdown文件：
```bash
touch agents/new-expert.md
```

2. 定义智能体配置和能力

3. 在`package.json`中注册智能体

### 自定义部署

编辑`scripts/deploy-commands.js`添加自定义部署逻辑。

---

## 📊 性能与优化

### 渐进式加载

- 技能采用渐进式信息披露原则
- 简洁的描述避免上下文过载
- 详细内容仅在触发时加载

### 依赖管理

- 优先使用`uv`包管理器（比pip快10-100倍）
- 自动检测和选择最佳包管理器
- 智能依赖冲突解决

### 中文优化

- 使用jieba进行高效中文分词
- 自动初始化jieba词典
- 支持自定义词典扩展

---

## 🐛 故障排除

### 常见问题

**Q: 技能无法触发**
- 检查YAML frontmatter格式
- 确认技能描述包含触发关键词
- 重启AI CLI工具

**Q: Python脚本运行错误**
- 检查依赖包是否安装：`pip list | grep jieba`
- 确认Python版本：`python --version` (需要3.8+)
- 查看错误日志

**Q: 中文字符显示异常**
- 确认文件编码为UTF-8
- 检查终端字符编码设置
- 更新相关软件版本

**Q: npm全局安装失败**
- 使用管理员权限运行
- 检查npm配置：`npm config list`
- 尝试使用yarn：`yarn global add ssci-subagent-skills`

### 诊断工具

```bash
# 系统诊断
python smart_deploy.py --diagnose

# 验证部署
ssci validate --verbose

# 检测CLI工具
ssci detect
```

---

## 📖 相关文档

- `README.md` - 项目主文档
- `SKILLS_MANIFEST.md` - 完整技能清单
- `INTELLIGENT_USAGE_GUIDE.md` - 智能化使用指南
- `DEPLOYMENT_GUIDE.md` - 详细部署指南
- `COMPREHENSIVE_TEST_PLAN.md` - 测试计划
- `IMPROVEMENT_ROADMAP.md` - 改进路线图

---

## 🤝 贡献指南

欢迎社区贡献！

1. Fork仓库
2. 创建特性分支：`git checkout -b feature/new-skill`
3. 提交更改：`git commit -am 'Add new skill'`
4. 推送分支：`git push origin feature/new-skill`
5. 提交Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [Claude Code](https://claude.com/code) - Subagent架构支持
- [Qwen CLI](https://github.com/QwenLM/qwen-code) - 国产CLI工具
- [iFlow CLI](https://github.com/iflow-ai/iflow-cli) - 国产CLI工具
- 中文社会科学研究社区 - 需求反馈和测试

---

## 📞 联系方式

- **GitHub Issues**: https://github.com/ssci-subagent-skills/ssci-subagent-skills/issues
- **Email**: skills@ssci.ai
- **文档**: https://ssci-subagent-skills.readthedocs.io

---

**最后更新**: 2025-12-18  
**文档版本**: 1.0  
**适用于**: iFlow CLI, Claude Code, Qwen CLI

---

*让AI成为中文社会科学研究的得力助手！* 🚀


<!-- SKILLS_START -->
<skills_system priority="1">

## Stigmergy Skills

<usage>
Load skills using Stigmergy skill manager:

Direct call (current CLI):
  Bash("stigmergy skill read <skill-name>")

Cross-CLI call (specify CLI):
  Bash("stigmergy use <cli-name> skill <skill-name>")

Smart routing (auto-select best CLI):
  Bash("stigmergy call skill <skill-name>")

The skill content will load with detailed instructions.
Base directory will be provided for resolving bundled resources.
</usage>

<available_skills>

<skill>
<name>algorithmic-art</name>
<description>Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists&apos; work to avoid copyright violations.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>ant</name>
<description>执行行动者网络理论分析，包括参与者识别、关系网络构建、转译过程追踪和网络动态分析。当需要分析异质性行动者网络、追踪事实构建过程或分析技术社会互动时使用此技能。</description>
<location>stigmergy</location>
</skill>

<skill>
<name>brand-guidelines</name>
<description>Applies Anthropic&apos;s official brand colors and typography to any sort of artifact that may benefit from having Anthropic&apos;s look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>canvas-design</name>
<description>Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists&apos; work to avoid copyright violations.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>conflict-resolution</name>
<description>研究分歧解决工具，处理学术研究中的理论、方法论、解释、价值观等分歧，提供建设性对话和共识建立策略</description>
<location>stigmergy</location>
</skill>

<skill>
<name>doc-coauthoring</name>
<description>Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>docx</name>
<description>Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks</description>
<location>stigmergy</location>
</skill>

<skill>
<name>field-analysis</name>
<description>执行布迪厄场域分析，包括场域边界识别、资本分布分析、自主性评估和习性模式分析。当需要分析社会场域的结构、权力关系和文化资本时使用此技能。</description>
<location>stigmergy</location>
</skill>

<skill>
<name>frontend-design</name>
<description>Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>internal-comms</name>
<description>A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).</description>
<location>stigmergy</location>
</skill>

<skill>
<name>mathematical-statistics</name>
<description>社会科学研究数理统计分析工具，提供描述性统计、推断统计、回归分析、方差分析、因子分析等完整统计支持</description>
<location>stigmergy</location>
</skill>

<skill>
<name>mcp-builder</name>
<description>Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).</description>
<location>stigmergy</location>
</skill>

<skill>
<name>network-computation</name>
<description>社会网络计算分析工具，提供网络构建、中心性测量、社区检测、网络可视化等完整的网络分析支持</description>
<location>stigmergy</location>
</skill>

<skill>
<name>pdf</name>
<description>Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>pptx</name>
<description>Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks</description>
<location>stigmergy</location>
</skill>

<skill>
<name>skill-creator</name>
<description>Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude&apos;s capabilities with specialized knowledge, workflows, or tool integrations.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>slack-gif-creator</name>
<description>Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like &quot;make me a GIF of X doing Y for Slack.&quot;</description>
<location>stigmergy</location>
</skill>

<skill>
<name>template-skill</name>
<description>Replace with description of the skill and when Claude should use it.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>theme-factory</name>
<description>Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>validity-reliability</name>
<description>研究信度效度分析工具，提供内部一致性、重测信度、评分者信度、构念效度、内容效度、效标效度等全面分析</description>
<location>stigmergy</location>
</skill>

<skill>
<name>web-artifacts-builder</name>
<description>Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>webapp-testing</name>
<description>Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.</description>
<location>stigmergy</location>
</skill>

<skill>
<name>xlsx</name>
<description>Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas</description>
<location>stigmergy</location>
</skill>

</available_skills>

</skills_system>
<!-- SKILLS_END -->
