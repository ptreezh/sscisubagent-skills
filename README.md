# SSCI Subagent Skills

<div align="center">

**中文社会科学研究多代理技能系统**

A comprehensive multi-agent skill system for social science research, designed specifically for Chinese academic contexts.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/Claude-Code-compatible-orange.svg)](https://claude.ai/claude-code)

</div>

---

## 项目概述 / Overview

SSCI Subagent Skills 是一个为中文社会科学研究设计的专业多代理技能系统。该系统整合了质性研究、量化研究、社会网络分析、组织生态分析等多种研究方法，为研究者提供从研究设计到数据分析的全流程支持。

SSCI Subagent Skills is a professional multi-agent skill system designed for Chinese social science research. It integrates qualitative research, quantitative research, social network analysis, organizational ecosystem analysis, and other research methods, providing comprehensive support from research design to data analysis.

### 核心特性 / Core Features

- **多理论框架支持** / Multi-theoretical Framework Support
  - 扎根理论 (Grounded Theory)
  - 社会网络分析 (Social Network Analysis)
  - 行动者网络理论 (Actor-Network Theory)
  - 布迪厄场域理论 (Bourdieu's Field Theory)
  - 数字马克思主义 (Digital Marxism)
  - 数字韦伯理论 (Digital Weber)

- **研究方法工具** / Research Method Tools
  - 质性数据分析
  - 量化统计分析
  - 模糊集定性比较分析 (fsQCA/msQCA)
  - 双重差分分析 (DID)
  - 研究设计评估

- **组织与商业分析** / Organizational & Business Analysis
  - 商业生态系统分析
  - 商业模式分析
  - 数字化转型分析
  - 组织网络分析

---

## 安装指南 / Installation

### 系统要求 / Requirements

- Python 3.8 or higher
- Claude Code CLI or compatible AI CLI tool
- Git (for cloning the repository)

### 快速安装 / Quick Install

```bash
# 克隆仓库 / Clone repository
git clone https://github.com/ptreezh/sscisubagent-skills.git
cd sscisubagent-skills

# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 配置技能路径 / Configure skills path
# 根据你的CLI工具配置技能目录
# Configure skills directory according to your CLI tool
```

### 配置说明 / Configuration

1. **Claude Code 用户 / Users:**
   ```bash
   # 将技能目录添加到 Claude Code 配置
   # Add skills directory to Claude Code config
   stigmergy skill add ./skills
   ```

2. **其他 CLI 工具 / Other CLI Tools:**
   参考 [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) 获取详细配置说明

---

## 11个核心专家智能体 / 11 Core Expert Agents

### 质性研究专家 / Qualitative Research Experts

1. **扎根理论专家** (Grounded Theory Expert)
   - 文件: `agents/grounded-theory-expert.md`
   - 功能: 开放编码、轴心编码、选择式编码、理论饱和度检验
   - 技能: `skills/grounded-theory-expert/`

### 网络分析专家 / Network Analysis Experts

2. **社会网络分析专家** (SNA Expert)
   - 文件: `agents/sna-expert.md`
   - 功能: 网络数据收集、中心性分析、社区检测、结构洞分析
   - 技能: `skills/network-computation-expert/`, `skills/sna-analysis/`

### 理论分析专家 / Theoretical Analysis Experts

3. **行动者网络理论专家** (ANT Expert)
   - 文件: `agents/ant-expert.md`
   - 功能: 行动者识别、转译过程分析、网络动态追踪
   - 技能: `skills/ant-expert/`, `skills/ant-network-analysis/`

4. **布迪厄场域分析专家** (Field Analysis Expert)
   - 文件: `agents/field-analysis-expert.md`
   - 功能: 场域边界识别、资本分布分析、习性模式分析
   - 技能: `skills/field-expert/`

5. **数字马克思主义专家** (Digital Marx Expert)
   - 文件: `agents/digital-marx-expert.md`
   - 功能: 历史唯物主义分析、阶级结构分析、异化分析
   - 技能: `skills/digital-marx-expert/`, `skills/digital-marx/`

6. **数字韦伯理论专家** (Digital Weber Expert)
   - 功能: 理解类型分析、制度分析、比较研究
   - 技能: `skills/digital-weber/`

7. **数字迪尔凯姆专家** (Digital Durkheim Expert)
   - 功能: 社会事实识别、团结分析、功能分析
   - 技能: `skills/digital-durkheim/`

### 辅助研究专家 / Research Support Experts

8. **文献专家** (Literature Expert)
   - 文件: `agents/literature-expert.md`
   - 功能: 文献检索、整理、引用格式化、研究趋势分析

9. **中文本地化专家** (Chinese Localization Expert)
   - 文件: `agents/chinese-localization-expert.md`
   - 功能: 中文学术概念本土化、研究方法论适配、文化语境分析

### 商业与组织分析专家 / Business & Organizational Analysis Experts

10. **数字化转型生态系统分析师** (Digital Transformation Ecosystem Analyst)
    - 文件: `agents/digital-transformation-ecosystem-analyst/`
    - 功能: 行业数字化转型分析、关键物种识别、生态图谱构建
    - 技能: `skills/ecosystem-analysis/`, `skills/digital-transformation/`

11. **数字化转型创新分析师** (Digital Transformation Innovation Analyst)
    - 文件: `agents/digital-transformation-innovation-analyst/`
    - 功能: 数字化创新路径规划、商业场景解构分析

**补充技能 / Additional Skills:**
- **商业生态分析专家**: `skills/business-ecosystem-analysis/`
- **商业模式分析专家**: `skills/business-model-analysis/`
- **生态系统关系分析**: `skills/ecosystem-relationship-analysis/`
- **商业数据收集**: `skills/business-ecosystem-data-collection/`

---

## 项目结构 / Project Structure

```
sscisubagent-skills/
├── agents/                    # 代理定义文件 / Agent definitions
│   ├── grounded-theory-expert.md
│   ├── sna-expert.md
│   ├── ant-expert.md
│   ├── field-analysis-expert.md
│   ├── digital-marx-expert.md
│   ├── literature-expert.md
│   ├── chinese-localization-expert.md
│   ├── digital-transformation-ecosystem-analyst/
│   ├── digital-transformation-innovation-analyst/
│   └── references/            # 参考资料和HTML文档
├── skills/                    # 技能实现 / Skills implementation
│   ├── grounded-theory-expert/
│   ├── network-computation/
│   ├── ant-expert/
│   ├── field-expert/
│   ├── digital-marx/
│   ├── ecosystem-analysis/
│   ├── business-ecosystem-analysis/
│   └── ...
│   │   ├── references/
│   │   └── algorithms/
│   ├── performing-open-coding/
│   ├── performing-axial-coding/
│   ├── digital-marx/
│   ├── business-ecosystem-analysis/
│   └── ...
├── tests/                     # 测试脚本 / Test scripts
├── test_data/                 # 测试数据 / Test data
├── archive/                   # 历史版本 / Archive
└── docs/                      # 文档 / Documentation
```

---

## 使用指南 / Usage Guide

### 基本用法 / Basic Usage

#### 1. 扎根理论分析 / Grounded Theory Analysis

```python
from skills.grounded_theory_expert import GroundedTheoryExpert

# 初始化专家 / Initialize expert
expert = GroundedTheoryExpert()

# 开放编码 / Open coding
concepts = expert.perform_open_coding(interview_data)

# 轴心编码 / Axial coding
categories = expert.perform_axial_coding(concepts)

# 选择式编码 / Selective coding
theory = expert.perform_selective_coding(categories)
```

#### 2. 社会网络分析 / Social Network Analysis

```python
from skills.network_computation import NetworkComputation

# 初始化网络分析器 / Initialize network analyzer
analyzer = NetworkComputation()

# 计算中心性指标 / Calculate centrality measures
centrality = analyzer.calculate_centrality(network_data)

# 社区检测 / Community detection
communities = analyzer.detect_communities(network_data)

# 网络可视化 / Network visualization
analyzer.visualize_network(network_data)
```

#### 3. 商业生态系统分析 / Business Ecosystem Analysis

```python
from skills.business_ecosystem_analysis import EcosystemAnalyzer

# 分析生态系统 / Analyze ecosystem
analyzer = EcosystemAnalyzer()
structure = analyzer.analyze_ecosystem(company_data)
```

### CLI 调用示例 / CLI Usage Examples

```bash
# 使用 Claude Code 调用技能 / Use skill with Claude Code
claude "使用扎根理论专家分析这段访谈数据"

# 跨 CLI 调用 / Cross-CLI invocation
stigmergy use claude skill grounded-theory-expert
```

---

## 54个核心技能 / 54 Core Skills

> 完整技能清单请查看: [COMPLETE_SKILLS_INVENTORY.md](COMPLETE_SKILLS_INVENTORY.md)

### 扎根理论 (6个) / Grounded Theory

| 技能 | 描述 |
|------|------|
| `grounded-theory-expert` | 完整扎根理论分析流程 |
| `performing-open-coding` | 开放编码分析 |
| `performing-axial-coding` | 轴心编码分析 |
| `performing-selective-coding` | 选择式编码分析 |
| `checking-theory-saturation` | 理论饱和度检验 |
| `writing-grounded-theory-memos` | 备忘录撰写 |

### 行动者网络理论 (6个) / ANT

| 技能 | 描述 |
|------|------|
| `ant` | ANT主技能 |
| `ant-expert` | ANT专家分析 |
| `ant-subagent` | ANT子代理 |
| `ant-network-analysis` | 网络分析 |
| `ant-participant-identification` | 行动者识别 |
| `ant-translation-process` | 转译过程分析 |

### 场域分析 (5个) / Field Analysis

| 技能 | 描述 |
|------|------|
| `field-analysis` | 场域分析主技能 |
| `field-expert` | 场域专家 |
| `field-boundary-identification` | 边界识别 |
| `field-capital-analysis` | 资本分析 |
| `field-habitus-analysis` | 习性分析 |

### 数字马克思主义 (6个) / Digital Marx

| 技能 | 描述 |
|------|------|
| `digital-marx` | 数字马克思主义主技能 |
| `digital-marx-expert` | 马克思主义专家 |
| `historical-materialist-analysis` | 历史唯物主义 |
| `class-structure-analysis` | 阶级结构分析 |
| `capital-analysis` | 资本分析 |
| `alienation-analysis` | 异化分析 |

### 网络分析 (5个) / Network Analysis

| 技能 | 描述 |
|------|------|
| `network-computation` | 网络计算 |
| `network-computation-expert` | 网络计算专家 |
| `processing-network-data` | 数据处理 |
| `performing-network-computation` | 网络计算执行 |
| `performing-centrality-analysis` | 中心性分析 |

### 量化分析 (5个) / Quantitative Analysis

| 技能 | 描述 |
|------|------|
| `mathematical-statistics` | 数理统计 |
| `validity-reliability` | 信度效度 |
| `fsqca-analysis` | 模糊集QCA |
| `msqca-analysis` | 多值集QCA |
| `did-analysis` | 双重差分 |

### 研究方法 (4个) / Research Methods

| 技能 | 描述 |
|------|------|
| `research-design` | 研究设计 |
| `data-analysis` | 数据分析 |
| `conflict-resolution` | 冲突解决 |
| `dissent-resolution` | 异议解决 |

### 数字理论 (2个) / Digital Theory

| 技能 | 描述 |
|------|------|
| `digital-weber` | 数字韦伯理论 |
| `digital-durkheim` | 数字迪尔凯姆理论 |

### 商业分析 (8个) / Business Analysis

| 技能 | 描述 |
|------|------|
| `business-model-analysis` | 商业模式分析 |
| `business-model-canvas-analysis` | 商业画布 |
| `business-service-supply-analysis` | 服务供应分析 |
| `business-ecosystem-data-collection` | 数据收集 |
| `ecosystem-relationship-analysis` | 生态关系 |
| `competitive-analysis` | 竞争分析 |
| `management-theory-analysis` | 管理理论 |
| `operations-analysis` | 运营分析 |

### 数字化转型 (2个，含8个子技能) / Digital Transformation

| 技能 | 描述 |
|------|------|
| `ecosystem-analysis` | 生态分析（5个子技能） |
| `digital-transformation` | 数字化转型（3个子技能） |

### 支持工具 (6个) / Support Tools

| 技能 | 描述 |
|------|------|
| `visualization-expert` | 可视化专家 |
| `trusted-web-scraper` | 网页抓取 |
| `information-verification` | 信息验证 |
| `spark-integration` | Spark集成 |
| `dialectical-quantitative-synthesis` | 辩证量化综合 |
| `practical-marxist-application` | 实践马义应用 |

---

**总计: 54个核心技能** (完整清单见 `COMPLETE_SKILLS_INVENTORY.md`)

---

## 开发指南 / Development Guide

### 贡献指南 / Contributing

我们欢迎各种形式的贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

We welcome all forms of contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### 开发环境设置 / Development Setup

```bash
# 创建虚拟环境 / Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 安装开发依赖 / Install dev dependencies
pip install -r requirements-dev.txt

# 运行测试 / Run tests
pytest tests/

# 代码格式化 / Code formatting
black skills/
isort skills/
```

### 技能开发规范 / Skill Development Standards

所有技能必须遵循以下规范：

1. **YAML Frontmatter**: 包含技能元数据
2. **标准结构**: SKILL.md, scripts/, references/, algorithms/
3. **测试覆盖**: 包含单元测试和集成测试
4. **文档完整**: 包含使用示例和API文档

详见 [SKILL_DESIGN_GUIDELINES.md](docs/SKILL_DESIGN_GUIDELINES.md)

---

## 测试 / Testing

```bash
# 运行所有测试 / Run all tests
pytest tests/

# 运行特定技能测试 / Run specific skill tests
pytest tests/test_grounded_theory.py

# 生成覆盖率报告 / Generate coverage report
pytest --cov=skills tests/
```

---

## 文档 / Documentation

- [安装指南](INSTALLATION_GUIDE.md) - 详细安装说明
- [技能设计指南](docs/SKILL_DESIGN_GUIDELINES.md) - 技能开发规范
- [API文档](docs/API.md) - 完整API参考
- [案例研究](docs/CASE_STUDIES.md) - 实际应用案例

---

## 常见问题 / FAQ

<details>
<summary><b>如何添加新技能？</b></summary>

1. 在 `skills/` 目录创建新文件夹
2. 创建 `SKILL.md` 文件，包含YAML frontmatter
3. 添加 `scripts/`, `references/`, `algorithms/` 子目录
4. 编写测试文件
5. 更新文档

</details>

<details>
<summary><b>支持的CLI工具有哪些？</b></summary>

- Claude Code (推荐 / Recommended)
- Gemini CLI
- Qwen CLI
- IFlow CLI
- 其他兼容的AI CLI工具

</details>

<details>
<summary><b>如何处理中文数据？</b></summary>

所有技能都针对中文语境进行了优化，支持：
- 中文文本编码和分析
- 中文术语识别
- 中文学术写作规范
- 本土化案例库

</details>

---

## 路线图 / Roadmap

### v2.0 (计划中 / Planned)

- [ ] 增加更多理论框架支持
- [ ] 优化多语言支持
- [ ] 增强可视化功能
- [ ] 添加Web界面
- [ ] 集成更多数据源

### v1.5 (进行中 / In Progress)

- [ ] 完善测试覆盖率
- [ ] 优化性能
- [ ] 增加文档
- [ ] 改进错误处理

---

## 许可证 / License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 致谢 / Acknowledgments

- 感谢 Claude Code 团队提供的优秀工具
- 感谢所有贡献者的支持
- 特别感谢中文社会科学研究社区的反馈和建议

---

## 联系方式 / Contact

- 项目主页: [https://github.com/yourusername/sscisubagent-skills](https://github.com/yourusername/sscisubagent-skills)
- 问题反馈: [GitHub Issues](https://github.com/yourusername/sscisubagent-skills/issues)
- 邮件: zhang.shuren@foxmail.com

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star！**

**If this project helps you, please give it a ⭐ Star!**

Made with ❤️ for the Social Science Research Community

</div>
