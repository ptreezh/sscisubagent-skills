---
name: planning-with-files
version: 1.0.0
description: Planning persistence system using disk-based files
author: Qoder Team
license: MIT
category: planning
dependencies: []
---

# Planning-with-Files Skill

This skill implements a 3-file pattern (`task_plan.md`, `findings.md`, `progress.md`) to create persistent, disk-based memory for AI workflows, treating the "Filesystem = Disk (persistent, unlimited)" versus "Context Window = RAM".

## Functionality

- **task_plan.md**: Stores goals, steps, and resources needed
- **findings.md**: Captures key insights, data points, and observations  
- **progress.md**: Tracks completed tasks, in-progress items, and blockers

## Commands

- `planning-with-files:start` - Initialize planning files
- `planning-with-files:status` - Check status of planning files
- Automatic integration with other skills to maintain context

## Hooks

The skill implements execution hooks:
- **Pre-execution**: Reads planning files before skill execution
- **Post-execution**: Saves findings and updates progress after execution
- **Context preservation**: Maintains planning state across sessions

## Integration

This skill seamlessly integrates with SSCI research skills to maintain research continuity and prevent goal drift during extended AI interactions.