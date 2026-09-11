# Qoder CLI Skills Installation

This document describes how to install and configure Qoder CLI skills following the OpenCode pattern with three tiers: project (`.opencode/skills/`), personal (`~/.config/qoder/skills/`), and system (bundled). Skills are Markdown files named `SKILL.md` with YAML frontmatter. Priority order is project > personal > system.

## Skill Format

Skills require `SKILL.md` with YAML frontmatter:

```yaml
---
name: my-skill
description: Use when [condition] - [what it does]
version: 1.0.0
author: Your Name
license: MIT
category: category
dependencies: []
---
```

## Directory Structure

```
.opencode/                 # Project-level skills
├── SKILL.md               # Main skill definition
└── skills/                # Individual skills
    ├── planning-with-files.md
    └── ssci-integration.md

~/.config/qoder/skills/    # Personal skills (medium priority)
└── custom-skill.md

qoder/skills/             # System skills (lowest priority)
└── bundled-skill.md
```

## Installation

### Method 1: Project Skills (Highest Priority)
Place skills in `.opencode/skills/` directory in your project root:

```bash
mkdir -p .opencode/skills
# Add your SKILL.md files to .opencode/ and .opencode/skills/
```

### Method 2: Personal Skills (Medium Priority)
Place skills in personal configuration directory:

```bash
mkdir -p ~/.config/qoder/skills
# Add your skill files to ~/.config/qoder/skills/
```

### Method 3: System Skills (Lowest Priority)
Skills bundled with Qoder CLI in the `qoder/skills/` directory.

## Priority Order

Skills are loaded in this order (highest to lowest priority):
1. **Project Skills**: `.opencode/skills/` - Project-specific skills
2. **Personal Skills**: `~/.config/qoder/skills/` - User-specific skills  
3. **System Skills**: Bundled with Qoder - Core system skills

## Skill Registration

Skills register automatically when placed in the correct directories. The system discovers `SKILL.md` files with proper YAML frontmatter and loads them according to priority order.

## Hooks System

The system supports hooks for maintaining context:

- **Pre-execution hooks**: Execute before skill execution
- **Post-execution hooks**: Execute after skill completion
- **Context preservation**: Maintain state across sessions

## Naming Convention

For clarity when multiple skills exist:
- Project skills: `project:skill-name`
- System skills: `system:skill-name`

## Usage

After installation, use skills through Qoder CLI:

```bash
# Start planning session
qoder planning-with-files:start

# Execute research skills
qoder skill grounded-theory-expert analyze data

# Check planning status
qoder planning-with-files:status
```

## Updates

Skills update dynamically when:
- New skill files are added to directories
- Existing skill files are modified
- System reloads configuration