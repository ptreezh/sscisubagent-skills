---
name: qoder-config
version: 1.0.0
description: Qoder CLI configuration with skills registry
author: Qoder Team
license: MIT
skills_registry:
  - path: ./qoder/SKILL.md
    enabled: true
  - path: ./qoder/skills/planning-with-files.md
    enabled: true
  - path: ./qoder/skills/ssci-integration.md
    enabled: true
plugin_paths:
  - ./qoder/plugins/
skill_directories:
  - ./qoder/skills/
  - ./sscisubagent-skills/skills/
  - ~/.config/qoder/skills/
  - ./.opencode/skills/
hooks:
  pre_execution:
    - read_plan
  post_execution:
    - save_findings
    - update_progress
  global:
    - initialize_planning_files
    - preserve_planning_context
    - maintain_context
---
# Qoder CLI Configuration File

This configuration defines the skills registry and system settings for Qoder CLI.

## Configuration Details

- **skills_registry**: List of skill files to load
- **plugin_paths**: Directories to search for plugins
- **skill_directories**: Directories to search for skills (following priority order)
- **hooks**: System hooks for maintaining planning context