---
name: planning-context-injector
description: Use when needing automatic planning context injection into chat messages - hooks into chat.message to provide task_plan.md, findings.md, and progress.md context automatically
version: 1.0.0
author: zhangshuren
email: zhangshuren@agent.qq.com
website: http://www.socienceAI.com
license: MIT
category: planning
dependencies: [qoder-superpowers]
hooks:
  - chat.message
---

# Planning Context Injector

Automatically injects planning context into chat messages via the chat.message hook. This skill monitors conversations and automatically provides relevant context from planning files.

## Functionality

- **Automatic Context Injection**: Hooks into chat.message to automatically prepend planning context
- **File Monitoring**: Watches task_plan.md, findings.md, and progress.md for updates
- **Context Relevance**: Determines which planning information is most relevant to the current conversation
- **Persistent Awareness**: Maintains awareness of planning state across sessions

## Hook Mechanism

The skill uses the `chat.message` hook to:
- Intercept incoming messages
- Retrieve current planning context
- Enrich messages with relevant planning information
- Pass enriched messages to downstream processing

## Integration

Works in conjunction with:
- Qoder Superpowers: For overall orchestration
- Planning-with-Files: For file management
- Research Skills: For context-aware assistance