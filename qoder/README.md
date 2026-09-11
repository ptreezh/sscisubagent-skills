# Qoder CLI Configuration

This directory contains the Qoder CLI skills system with planning-with-files and SSCI integration.

## Skills Structure

The skills follow the OpenCode pattern with YAML frontmatter:

```yaml
---
name: skill-name
version: 1.0.0
description: Brief description
author: Author name
license: License type
category: Category
dependencies: []
---
```

## Available Skills

- **Main Skill**: `qoder/SKILL.md` - Core Qoder CLI functionality
- **Planning Skill**: `qoder/skills/planning-with-files.md` - Planning persistence
- **SSCI Skill**: `qoder/skills/ssci-integration.md` - Research skills integration

## Installation

To install these skills in Qoder CLI:

1. Place the `qoder/` directory in your project root
2. Ensure the directory structure is maintained
3. The skills will be automatically detected and loaded

## Usage

Once installed, use the skills as follows:

```
qoder planning-with-files:start
qoder skill grounded-theory-expert analyze interview data
qoder planning-with-files:status
```

## Skill Hierarchy

Following the OpenCode pattern, skills are loaded in this priority:
1. Project skills (./skills/) - Highest priority
2. Personal skills (~/.config/qoder/skills/) - Medium priority
3. System skills (bundled) - Lowest priority