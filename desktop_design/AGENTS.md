# AGENTS.md

This file provides guidance to Qoder (qoder.com) when working with code in this repository.

# AGENTS Configuration

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

# Development Commands

## Common Development Tasks

### Running the Application
```bash
# Start the development server
npm run dev

# Build the application
npm run build
```

### Testing
```bash
# Run all tests
npm test

# Run health checks
npm run health-check

# Check system status
npm run status

# Monitor system
npm run monitor
```

### Deployment
```bash
# Deploy to Stigmergy
npm run deploy:stigmergy

# Deploy to multiple CLIs
npm run deploy:multi

# Deploy to all platforms
npm run deploy:all
```

# Code Architecture Overview

## Project Structure
This is a desktop application project built with Electron that provides a graphical interface for managing Stigmergy CLI tools and skills. The project follows a typical Electron architecture:

```
Electron Desktop App
├── Main Process (Node.js)
│   ├── CLI Wrappers
│   ├── Config Managers
│   ├── File Managers
│   └── Security Controls
├── Renderer Process (React)
│   ├── UI Components
│   ├── State Management
│   └── User Interaction
└── IPC Communication Layer
    ├── Main ↔ Renderer Communication
    └── CLI Call Results Passing
```

## Key Components

### 1. Stigmergy CLI Integration
The application wraps the Stigmergy CLI to provide a graphical interface for all its commands:
- Skill management (list, install, remove, sync)
- Cross-CLI collaboration (use, call)
- Status monitoring
- Configuration management

### 2. Multi-CLI Support
The application supports integration with multiple AI CLI tools:
- Claude
- Qwen
- iFlow
- Gemini
- Codebuddy
- Codex
- QoderCLI

### 3. Skill Management System
Complete lifecycle management for skills:
- Upload/download skills
- Install/remove skills
- Configure skill parameters
- Enable/disable skills
- Batch operations

### 4. Project Management
Integrated project management features:
- Project creation and directory management
- File tree visualization
- Integrated code editor
- Git version control integration

## Technology Stack
- **Frontend**: React with TypeScript
- **Backend**: Node.js with Electron
- **Build System**: Webpack
- **Testing**: Jest/Playwright for end-to-end testing
- **Deployment**: Custom deployment scripts for different CLI platforms

## Core Principles
1. **Zero CLI Dependency**: Users should never need to touch the command line
2. **Local Privacy**: All processing happens locally with no cloud dependencies
3. **Full Stigmergy Compatibility**: 100% support for all Stigmergy commands
4. **Cross-CLI Collaboration**: Seamless integration between different AI tools
5. **User-Friendly Interface**: Modern, intuitive graphical interface

When working on this codebase, focus on maintaining these principles while implementing new features or fixing bugs.