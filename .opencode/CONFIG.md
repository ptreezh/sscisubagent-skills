---
name: qoder-installation
description: Configuration for Qoder CLI skills installation following OpenCode pattern
version: 1.0.0
author: zhangshuren
email: zhangshuren@agent.qq.com
website: http://www.socienceAI.com
license: MIT
category: configuration
skills_registry:
  - path: ./.opencode/SKILL.md
    enabled: true
  - path: ./.opencode/skills/planning-with-files.md
    enabled: true
  - path: ./.opencode/skills/ssci-integration.md
    enabled: true
skill_directories:
  - ./.opencode/skills/          # Project skills (highest priority)
  - ~/.config/qoder/skills/      # Personal skills (medium priority)
  - ./qoder/skills/              # System skills (lowest priority)
  - ./sscisubagent-skills/skills/ # SSCI skills integration
hooks:
  pre_execution:
    - read_planning_files
  post_execution:
    - save_findings
    - update_progress
priority_order:
  - project: ./.opencode/skills/
  - personal: ~/.config/qoder/skills/
  - system: ./qoder/skills/
---

# Qoder CLI Configuration

This configuration implements the OpenCode pattern for skill management in Qoder CLI, with three-tier skill loading and proper YAML frontmatter support.