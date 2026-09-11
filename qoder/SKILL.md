---
name: qoder-skills
version: 1.0.0
description: Qoder CLI Skills with Planning-with-Files and SSCI Integration
author: Qoder Team
license: MIT
---

# Qoder CLI Skills System

This skill package provides comprehensive AI assistance with planning capabilities and SSCI (Social Science Computational Intelligence) integration.

## Features

- Planning-with-Files functionality (task_plan.md, findings.md, progress.md)
- Integration with 50+ SSCI research skills
- Persistent planning context across sessions
- Multi-tier skill loading system

## Usage

### Planning Commands
- `qoder planning-with-files:start` - Initialize planning session
- `qoder planning-with-files:status` - Check planning status

### SSCI Research Skills
- `qoder skill grounded-theory-expert [params]` - Grounded theory analysis
- `qoder skill network-computation [params]` - Network analysis
- `qoder skill field-analysis [params]` - Field analysis
- `qoder skill ant [params]` - Actor-network theory analysis
- `qoder skill digital-marx [params]` - Digital marxist analysis
- `qoder skill fsqca-analysis [params]` - Fuzzy-set QCA analysis
- `qoder skill business-ecosystem-analysis [params]` - Business ecosystem analysis

## Skill Architecture

The system implements a three-tier skill loading system:
1. Project Skills (./.opencode/skills/ or ./skills/) - Highest priority
2. Personal Skills (~/.config/qoder/skills/) - Medium priority  
3. System Skills (bundled with Qoder) - Lowest priority

## Plugin System

The planning-with-files plugin manages persistent planning context through:
- Pre-execution hooks: Read planning files before skill execution
- Post-execution hooks: Save findings and update progress after execution
- Context preservation: Maintain planning state across sessions