---
name: research-skill-orchestrator
description: Use when conducting multi-method social science research - automatically selects and orchestrates appropriate SSCI research skills based on research goals and context
version: 1.0.0
author: zhangshuren
email: zhangshuren@agent.qq.com
website: http://www.socienceAI.com
license: MIT
category: research
dependencies: [qoder-superpowers, planning-context-injector]
hooks:
  - chat.message
---

# Research Skill Orchestrator

Automatically selects and orchestrates appropriate SSCI research skills based on research goals and context, with automatic planning integration.

## Functionality

- **Skill Selection**: Analyzes research queries to select the most appropriate SSCI skills
- **Workflow Orchestration**: Chains multiple research skills together in logical sequences
- **Context Awareness**: Uses planning context to inform skill selection and execution
- **Automatic Integration**: Seamlessly integrates with planning files to track research progress

## Supported Research Workflows

### Qualitative Analysis
- Triggers grounded-theory-expert for open/axial/selective coding
- Integrates with planning to track coding progress

### Network Analysis  
- Activates network-computation for centrality and community analysis
- Updates planning files with network insights

### Field Analysis
- Engages field-analysis for boundary, capital, and habitus analysis
- Maintains research context in planning files

### Mixed Methods
- Coordinates multiple skill types for comprehensive analysis
- Manages complex research workflows across skills

## Hook Mechanism

Uses `chat.message` hook to:
- Analyze research queries for skill requirements
- Determine optimal skill sequences
- Execute selected skills with proper context
- Update planning files with results and next steps