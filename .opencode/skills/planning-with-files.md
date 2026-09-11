---
name: planning-with-files
description: Use when needing persistent planning context across CLI sessions - maintains task_plan.md, findings.md, and progress.md files
version: 1.0.0
author: zhangshuren
email: zhangshuren@agent.qq.com
website: http://www.socienceAI.com
license: MIT
category: planning
dependencies: []
---

# Planning-with-Files Skill

Implements a 3-file pattern (`task_plan.md`, `findings.md`, `progress.md`) to create persistent, disk-based memory for AI workflows. This addresses the "Filesystem = Disk (persistent, unlimited)" vs "Context Window = RAM" challenge.

## Functionality

- **task_plan.md**: Stores goals, steps, and resources needed
- **findings.md**: Captures key insights, data points, and observations
- **progress.md**: Tracks completed tasks, in-progress items, and blockers

## Commands

- `qoder planning-with-files:start` - Initialize planning session
- `qoder planning-with-files:status` - Check planning file status
- Automatic integration with other skills to maintain context

## Hooks

- **Pre-execution**: Read planning files before skill execution
- **Post-execution**: Save findings and update progress after execution
- **Context preservation**: Maintain planning state across sessions