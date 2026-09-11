# Qoder CLI Skills Installation Guide

This document describes how to install and configure the Qoder CLI skills system with planning-with-files functionality and SSCI (Social Science Computational Intelligence) skills integration.

## Installation Tiers

The Qoder CLI follows a three-tier skill loading system:

1. **Project Skills** (`.opencode/skills/` or `./skills/`): Project-specific skills with highest priority
2. **Personal Skills** (`~/.config/qoder/skills/`): User-specific skills with medium priority  
3. **System Skills** (bundled with Qoder): Core skills with lowest priority

Priority order: Project > Personal > System

## Prerequisites

- Node.js v14.0.0 or higher
- Git for cloning skill repositories
- Access to SSCI skills repository

## Installation Steps

### 1. Clone the Qoder CLI Skills System

```bash
git clone https://github.com/yourusername/qoder-skills.git
cd qoder-skills
npm install
```

### 2. Install SSCI Skills Dependencies

The system integrates with SSCI Subagent Skills for social science research:

```bash
# If not already present, clone the SSCI skills
git clone https://github.com/ptreezh/sscisubagent-skills.git
```

### 3. Configure Qoder CLI

The system uses the configuration file `qoder_config.json` to define skills and plugins:

```json
{
  "skills": {
    "enabled": true,
    "directories": [
      "./sscisubagent-skills/skills",
      "./custom_skills"
    ],
    "plugins": {
      "planning-with-files": {
        "enabled": true,
        "hooks": {
          "preExecution": ["read_plan"],
          "postExecution": ["save_findings", "update_progress"]
        },
        "files": {
          "plan": "task_plan.md",
          "findings": "findings.md",
          "progress": "progress.md"
        }
      }
    }
  }
}
```

### 4. Set Up Directories

Create the necessary directory structure:

```bash
mkdir -p ~/.config/qoder/skills
mkdir -p .opencode/skills
```

### 5. Link System Skills

Skills are loaded dynamically from the configured directories. The system automatically discovers and registers skills from:

- `./sscisubagent-skills/skills` (SSCI skills)
- `./custom_skills` (user-defined skills)
- `~/.config/qoder/skills` (personal skills)
- `.opencode/skills` (project skills)

## Skill Format

Skills are organized as directories containing:

- `SKILL.md`: Main skill documentation with YAML frontmatter
- `scripts/`: Skill implementation files
- `prompts/`: AI prompt templates
- `references/`: Supporting documentation

Example SKILL.md structure:
```markdown
---
name: example-skill
version: 1.0.0
description: An example skill
author: Your Name
---

# Example Skill

This skill demonstrates the basic structure...
```

## Plugin Registration

Plugins are registered via the configuration system. The planning-with-files plugin is enabled by default and manages the three planning files:

- `task_plan.md`: Task planning and goals
- `findings.md`: Research findings and insights
- `progress.md`: Progress tracking

## Usage

After installation, use the Qoder CLI as follows:

```bash
# Start a planning session
node qoder_cli.js planning-with-files:start

# Execute an SSCI skill
node qoder_cli.js skill grounded-theory-expert analyze interview data

# Check planning status
node qoder_cli.js planning-with-files:status

# Execute other skills
node qoder_cli.js skill network-computation analyze connections
```

## Dynamic Skill Loading

Skills load dynamically using the internal skill execution system. The system can discover and execute skills without restart using the `skill_executor.js` module.

## Updates

To update system skills:

```bash
# Update SSCI skills
cd sscisubagent-skills
git pull origin main

# Update Qoder CLI skills
cd qoder-skills
git pull origin main
```

## Troubleshooting

1. **Missing skills**: Ensure the skill directories are correctly specified in `qoder_config.json`
2. **Planning files not created**: Verify write permissions in the current directory
3. **Configuration errors**: Check that `qoder_config.json` is valid JSON
4. **Skill execution fails**: Confirm that skill directories contain proper `SKILL.md` files

## Customization

To add custom skills:

1. Create a new directory in `./custom_skills/`
2. Add a `SKILL.md` file with YAML frontmatter
3. Include implementation scripts in the `scripts/` subdirectory
4. Restart Qoder CLI or use dynamic loading if available

## Security Considerations

- Only load skills from trusted sources
- Review skill implementations before execution
- Configure appropriate permissions for planning files
- Validate input parameters to prevent injection attacks