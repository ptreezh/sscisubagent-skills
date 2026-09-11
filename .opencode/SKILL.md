---
name: qoder-superpowers
description: Use when needing advanced CLI assistance with persistent planning and research capabilities - provides automated context injection and skill orchestration
version: 1.0.0
author: zhangshuren
email: zhangshuren@agent.qq.com
website: http://www.socienceAI.com
license: MIT
category: productivity
dependencies: []
hooks:
  - chat.message
---

# Qoder Superpowers

Advanced CLI assistance with persistent planning and research capabilities, featuring automated context injection and skill orchestration.

## Capabilities

- **Automated Context Injection**: Hooks into chat.message to automatically provide planning context
- **Persistent Planning**: Maintains task_plan.md, findings.md, and progress.md across sessions
- **Research Orchestration**: Seamlessly integrates 50+ SSCI research skills
- **Context Preservation**: Prevents goal drift and maintains important information

## Automatic Features

When this skill is active, it automatically:
- Injects planning context into chat interactions via chat.message hook
- Maintains persistent state using disk-based files
- Orchestrates other research skills as needed
- Preserves important context across CLI sessions

## Integration

This superpower integrates with:
- Planning-with-Files: For persistent task management
- SSCI Research Skills: For methodology-specific assistance
- Context Injection System: For seamless interaction flow