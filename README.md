# SocienceAI Superpowers - Social Science Research AI Skills

**Author:** zhangshuren  
**Email:** zhangshuren@agent.qq.com  
**Website:** http://www.socienceAI.com

This project implements a superpowers-style skill system for social science research, featuring 66 validated AI research skills for qualitative, quantitative, and mixed methods research.

## Overview

The system implements the superpowers pattern with:

1. **66 Specialized Research Skills**: Comprehensive collection covering qualitative, quantitative, and mixed methods social science research
2. **Automated Context Injection**: Uses `chat.message` hook to automatically inject planning context into conversations
3. **Intelligent Skill Orchestration**: Automatically selects and chains appropriate research skills based on context
4. **Three-Tier Skill System**: Follows priority order - project → personal → system
5. **Plugin Registration**: Plugins register via symlink mechanism with hook support

## Skill Categories

### 📝 Qualitative Research Methods (14)
- grounded-theory-expert, thematic-analysis-expert, discourse-analysis-expert, narrative-analysis-expert
- content-analysis-expert, case-study-expert, ethnography-expert, phenomenology-expert
- ipa-analysis-expert, conversation-analysis-expert, rhetoric-analysis-expert, visual-analysis-expert
- semiotics-analysis-expert, document-analysis-expert

### 📊 Quantitative & Mixed Methods (12)
- social-network-analysis-expert, qca-analysis-expert, regression-analysis-expert, sem-analysis-expert
- factor-analysis-expert, meta-analysis-expert, did-analysis-expert, multilevel-modeling-expert
- longitudinal-analysis-expert, mixed-methods-expert, secondary-analysis-expert, survey-design-expert

### 🌐 Network & System Methods (5)
- actor-network-analysis-expert, cas-simulation-expert, system-dynamics-expert
- social-sequence-analysis-expert, bibliometric-analysis-expert

### 📚 Classical Theory & Digital Methods (3)
- digital-marx-expert, digital-durkheim-expert, digital-weber-expert

### ⚔️ Field & Strategic Analysis (9)
- bourdieu-field-analysis-expert, pest-analysis-expert, swot-analysis-expert, porter-five-forces-expert
- blue-ocean-strategy-expert, balanced-scorecard-expert, design-thinking-expert
- value-proposition-expert, lean-startup-expert

### 🏢 Management & Business (6)
- okr-expert, change-management-expert, agile-pm-expert, organizational-diagnosis-expert
- business-model-expert, business-ecosystem-expert

### 📢 Additional Methods (17)
- machine-learning-research-expert, nlp-text-mining-expert, internet-research-expert, media-analysis-expert
- historical-analysis-expert, rct-experimental-design-expert, action-research-expert, brand-equity-expert
- consumer-behavior-expert, data-analysis-expert, skill-upgrade-expert, skill-creator
- socienceai-project-soul, soul-agent-creator, soul-agents

## Skills Location

All 66 skills are located in the `skills/` directory at the repository root, with each skill in its own directory containing:
- `SKILL.md` - Skill definition and instructions
- Supporting files for implementation and templates

## Superpowers Architecture

### Core Superpower
- `.opencode/SKILL.md`: Main superpower with `chat.message` hook for automatic context injection

### Specialized Skills
- `.opencode/skills/planning-context-injector.md`: Injects planning context via `chat.message` hook
- `.opencode/skills/research-skill-orchestrator.md`: Orchestrates research skills via `chat.message` hook

### Plugin System
- `qoder_superpowers.js`: Plugin with `chat.message` hook registration
- `install_superpowers.js`: Installation script with symlink mechanism

### Configuration
- `qoder_superpowers_config.json`: Superpowers configuration with hook mappings
- Three-tier priority system (project → personal → system)

## Features

1. **Automatic Context Injection**: Hooks into `chat.message` to provide planning context automatically
2. **Intelligent Skill Selection**: Orchestrates appropriate research skills based on queries
3. **Three-Tier Skill System**: Proper priority order with project → personal → system
4. **Plugin Registration**: Symlink-based plugin system with hook support
5. **Persistent Planning**: Maintains context across sessions using disk-based files

## Installation

The system follows the superpowers installation pattern:

```
node install_superpowers.js
```

This creates:
- Three-tier skill directories: project → personal → system
- Plugin registration via symlink mechanism
- Hook configuration for `chat.message`
- Initial planning files

## Usage

Once installed, the superpowers work automatically:

- Planning context is automatically injected into conversations via `chat.message` hook
- Research skills are intelligently selected and orchestrated based on context
- Context persists across CLI sessions using task_plan.md, findings.md, progress.md

## Hook System

The superpowers use `chat.message` hooks for:
- Automatic planning context injection
- Intelligent skill orchestration
- Context-aware research assistance
- Seamless integration with existing workflows

## Skills Priority

Follows the superpowers pattern priority order:
1. **Project Skills** (`.opencode/skills/`): Highest priority
2. **Personal Skills** (`~/.config/qoder/skills/`): Medium priority  
3. **System Skills** (`./qoder/skills/`): Lowest priority

## Plugin Registration

Plugins register via symlink mechanism:
- Plugin files in `~/.config/qoder/plugins/`
- Hook registration for `chat.message` and other events
- Automatic activation when superpowers are loaded

## Integration Benefits

- **Seamless Context**: Automatic planning context injection without manual intervention
- **Intelligent Assistance**: Research skills selected based on actual needs
- **Persistent Memory**: Context maintained across sessions via disk files
- **Flexible Architecture**: Easy to extend with new skills and hooks
- **Priority Management**: Proper skill precedence with override capabilities