# QWEN Configuration

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
<name>ant-participant-identification</name>
<description>识别行动者网络理论中的参与者，包括人类和非人类行动者，以及他们的特征、关系和网络位置。当需要识别人类和非人类行动者、确定其角色和特征时使用此技能。</description>
<location>stigmergy</location>
</skill>

<skill>
<name>ant-translation-process</name>
<description>追踪行动者网络理论中的转译过程，包括问题化、利益化、征召和动员四个阶段，以及争议和转译失败的分析。当需要追踪事实构建过程、分析网络稳定化过程或理解技术社会构建过程时使用此技能。</description>
<location>stigmergy</location>
</skill>

<skill>
<name>ant-network-analysis</name>
<description>分析行动者网络的结构、动态和稳定性，包括网络拓扑、关系强度、中心性、凝聚力和演化过程。当需要分析网络结构、识别关键节点、评估网络稳定性或追踪网络演化时使用此技能。</description>
<location>stigmergy</location>
</skill>

<skill>
<name>ant-power-analysis</name>
<description>分析行动者网络中的权力关系，包括权力流动、权力结构、权力行使和权力效果评估。当需要分析网络中的权力分布、权力流动路径或权力关系结构时使用此技能。</description>
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
<name>dissent-resolution</name>
<description>研究分歧解决技能，处理学术研究中的不同观点、争议和异议，促进建设性对话和共识达成</description>
<location>stigmergy</location>
</skill>

<skill>
<name>research-design</name>
<description>研究设计技能，为社会科学研究提供系统的设计框架，包括研究问题构建、方法选择、数据收集和分析策略</description>
<location>stigmergy</location>
</skill>

<skill>
<name>performing-open-coding</name>
<description>当用户需要执行扎根理论的开放编码，包括中文质性数据的概念识别、初始编码、持续比较和备忘录撰写时使用此技能</description>
<location>stigmergy</location>
</skill>

<skill>
<name>performing-axial-coding</name>
<description>当用户需要执行扎根理论的轴心编码，包括范畴识别、属性维度分析、关系建立和Paradigm构建时使用此技能</description>
<location>stigmergy</location>
</skill>

<skill>
<name>performing-selective-coding</name>
<description>当用户需要执行扎根理论的选择式编码，包括核心范畴识别、故事线构建、理论框架整合和理论饱和度检验时使用此技能</description>
<location>stigmergy</location>
</skill>

<skill>
<name>checking-theory-saturation</name>
<description>检验扎根理论饱和度，包括新概念识别、范畴完善度、关系充分性和理论完整性评估。当需要判断理论是否达到饱和、是否需要补充数据或是否可以结束研究时使用此技能</description>
<location>stigmergy</location>
</skill>

<skill>
<name>writing-grounded-theory-memos</name>
<description>撰写扎根理论备忘录，包括过程记录、反思分析、理论备忘录和编码备忘录。当需要记录编码过程、深化理论思考、保存研究发现或进行理论反思时使用此技能</description>
<location>stigmergy</location>
</skill>

<skill>
<name>performing-centrality-analysis</name>
<description>执行社会网络中心性分析，包括度中心性、接近中心性、介数中心性和特征向量中心性的计算和解释。当需要识别网络中的关键节点、权力中心或信息枢纽时使用此技能</description>
<location>stigmergy</location>
</skill>

<skill>
<name>performing-network-computation</name>
<description>执行社会网络计算分析，包括网络构建、基础指标计算、社区检测、网络可视化和高级网络分析。当需要进行复杂的社会网络分析、构建网络模型或计算网络统计指标时使用此技能</description>
<location>stigmergy</location>
</skill>

<skill>
<name>processing-network-data</name>
<description>处理社会网络数据，包括关系数据收集、矩阵构建、数据清洗验证和多模网络处理。当需要从问卷、访谈、观察或数字记录中提取关系数据，构建标准化的网络矩阵时使用此技能</description>
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
<name>field-boundary-identification</name>
<description>识别和分析社会场域的边界，包括场域范围、界限、排除机制和与其他场域的关系。当需要定义场域边界、确定场域范围或分析场域边界维持机制时使用此技能。</description>
<location>stigmergy</location>
</skill>

<skill>
<name>field-capital-analysis</name>
<description>分析社会场域中的资本类型、分布、转换和竞争，包括经济资本、社会资本、文化资本和象征资本。当需要分析场域中的资本分布、理解资本转换机制或评估资本竞争格局时使用此技能。</description>
<location>stigmergy</location>
</skill>

<skill>
<name>field-habitus-analysis</name>
<description>分析社会场域中的习性模式，包括行动者的行为倾向、认知结构、实践逻辑和场域结构的相互关系。当需要理解行动者的实践逻辑、分析习性与场域的关系或评估习性对场域实践的影响时使用此技能。</description>
<location>stigmergy</location>
</skill>

<skill>
<name>field-dynamics-analysis</name>
<description>分析社会场域的动力学过程，包括场域竞争、权力关系变化、资本转换过程和场域演化趋势。当需要分析场域内的竞争格局、权力关系变化或场域演化过程时使用此技能。</description>
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

## 更新说明

所有SSCI子智能体技能现在都已按照agentskills.io标准进行了优化，实现了：
1. 渐进式信息披露架构
2. 定性与定量功能分离
3. 模块化设计
4. 完善的依赖管理与降级机制

有关详细信息，请参阅项目中的文档：
- SKILL_DESIGN_STANDARDS.md - 技能设计标准
- IMPLEMENTATION_SUMMARY.md - 实现摘要
- OPTIMIZATION_SUMMARY.md - 优化摘要
- TEST_REPORT_SUMMARY.md - 测试报告摘要
