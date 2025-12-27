# Best Practices for SSCI Subagent Skills

This document outlines the best practices for developing and maintaining SSCI subagent skills according to the agentskills.io standard and the specific needs of Chinese social science research.

## 1. Compliance with agentskills.io Standard

### Required Components
- **SKILL.md file**: Every skill must have a SKILL.md file with YAML frontmatter
- **Name field**: 1-64 characters, lowercase alphanumeric and hyphens only
- **Description field**: 1-1024 characters, describing what the skill does and when to use it
- **Directory naming**: Skill directory name must match the `name` field in SKILL.md

### Recommended Additional Fields
```yaml
---
name: skill-name
description: Clear, concise description of what the skill does and when to use it
license: MIT  # Optional but recommended
compatibility: Claude 3.5 Sonnet and above  # Optional but useful
metadata:
  domain: specific-domain
  methodology: specific-methodology
  complexity: beginner/intermediate/advanced
  integration_type: analysis_tool/other
  last_updated: "YYYY-MM-DD"
  author: author-name  # Not required but useful
  version: 1.0.0  # Not required but useful
allowed-tools: [python, bash, read_file, write_file]  # Experimental but useful
tags: [list, of, relevant, tags]  # Not required but useful for discovery
---
```

### Compliance Audit Results

Our analysis of the skills directory revealed that 15 skills are currently non-compliant with the agentskills.io standard as they are missing the required SKILL.md file:

**Non-Compliant Skills (Missing SKILL.md):**
1. `2025_12_21_cnki-downloader.skill.install`
2. `alienation_analysis`
3. `business-ecosystem-data-collection`
4. `business-model-analysis`
5. `business-model-canvas-analysis`
6. `business-service-supply-analysis`
7. `capital-analysis`
8. `competitive-analysis`
9. `ecosystem-relationship-analysis`
10. `information-verification`
11. `management-theory-analysis`
12. `operations-analysis`
13. `spark-integration`
14. `visualization-expert`

**Compliance Implementation Plan:**
- **Phase 1**: Create missing SKILL.md files for incomplete directories
- **Phase 2**: Convert existing documentation (INFO.md, README.md) to SKILL.md format
- **Phase 3**: Ensure all skills follow the standardized directory structure

## 2. Directory Structure

### Standard Structure
```
skill-name/
├── SKILL.md (required)
├── scripts/ (optional) - All executable scripts
├── references/ (optional) - Additional documentation
├── assets/ (optional) - Static resources
├── tests/ (optional but recommended) - Unit and integration tests
└── pyproject.toml (optional) - Dependencies
```

### Best Practices
1. **Consistent naming**: Ensure skill directory name matches the `name` field
2. **Organized scripts**: Place all executable code in the `scripts/` directory
3. **Documentation separation**: Use `references/` for detailed documentation
4. **Test inclusion**: Add tests to ensure functionality and reliability

## 3. SKILL.md Content Structure

### Progressive Disclosure Format
- **Metadata section** (~100 tokens): Loaded at startup for all skills
- **Instructions section** (<5000 tokens recommended): Loaded when skill is activated
- **Resource references**: Loaded only when required

### Recommended Content Sections
1. **Overview**: Brief description of the skill's purpose
2. **When to Use**: Clear guidelines on appropriate usage scenarios
3. **Quick Start**: High-level usage instructions
4. **Detailed Instructions**: Step-by-step processes
5. **Output Format**: Expected output structure
6. **Quality Checklist**: Validation criteria for results
7. **Troubleshooting**: Common issues and solutions
8. **Further Learning**: Additional resources and references

## 4. Script Development Standards

### Command-Line Interface
All scripts should implement standardized command-line interfaces:

```python
#!/usr/bin/env python3
"""
Script description
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
import logging

def main():
    parser = argparse.ArgumentParser(
        description='Script description',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python script.py --input data.txt --output results.json
  python script.py -i data.txt -o results.json --param value
        """
    )
    parser.add_argument('--input', '-i', required=True, help='Input file path')
    parser.add_argument('--output', '-o', default='output.json', help='Output file path')
    parser.add_argument('--param', '-p', help='Additional parameter')
    
    args = parser.parse_args()
    
    # Process and generate standardized output
    # ... implementation ...
    
    # Write standardized JSON output
    output = {
        'summary': {
            # Key metrics and overview
        },
        'details': {
            # Complete results
        },
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'skill-name'
        }
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
```

### Error Handling and Validation
- Implement comprehensive error handling with clear messages
- Validate inputs before processing
- Use appropriate logging levels
- Follow consistent error code conventions

## 5. Standardized Output Format

### Three-Tier JSON Structure
All skills should output data in this standardized format:

```json
{
  "summary": {
    "key_metric_1": value,
    "key_metric_2": value,
    "processing_time": seconds
  },
  "details": {
    "full_results": [...],
    "additional_data": {...}
  },
  "metadata": {
    "timestamp": "2025-12-26T10:30:00",
    "version": "1.0.0",
    "skill": "skill-name",
    "input_file": "input.json"
  }
}
```

## 6. Quality Assurance

### Validation
- Use `skills-ref validate ./my-skill` to validate SKILL.md files
- Include internal validation checks in scripts
- Provide unit tests for script functionality
- Include quality metrics in outputs

### Documentation
- Provide clear usage instructions
- Include examples of input and expected output
- Document dependencies and installation requirements
- Add quality checklists for users

## 7. Cultural and Domain-Specific Considerations

### Chinese Context
- Maintain bilingual documentation (Chinese/English) where appropriate
- Consider cultural context in examples and explanations
- Address specific needs of Chinese social science research
- Use appropriate terminology for Chinese academic context

### Domain-Specific
- Include domain-specific terminology and concepts
- Provide context-appropriate examples
- Consider interdisciplinary applications
- Address specific methodological requirements

## 8. Integration and Orchestration

### Subagent Architecture
- Organize related skills into coherent subagent systems
- Implement clear parent-child relationships between skills
- Provide unified interfaces where appropriate
- Maintain specialized functionality within integrated systems
- Ensure consistent parameter and output formats across related skills

## 9. Performance and Scalability

### Efficiency
- Optimize algorithms for performance
- Implement appropriate data structures
- Consider memory usage for large datasets
- Provide progress indicators for long-running processes

### Scalability
- Design for varying data sizes
- Implement appropriate caching mechanisms
- Consider parallel processing where beneficial
- Ensure scripts handle edge cases gracefully

## 10. Maintenance and Evolution

### Versioning
- Maintain version information in metadata
- Document changes between versions
- Provide migration paths for breaking changes
- Follow semantic versioning where appropriate

### Feedback Mechanisms
- Include quality metrics in output
- Provide mechanisms for user feedback
- Implement continuous improvement processes
- Monitor usage and effectiveness

## 11. File Size and Performance

### Content Size
- Keep main SKILL.md files under 500 lines
- Use relative paths for file references
- Move detailed documentation to `references/` directory
- Optimize images and assets in `assets/` directory

## 12. Testing and Validation

### Testing Strategy
- Include unit tests for script functionality
- Create integration tests for complete workflows
- Test with various input data types and sizes
- Validate output format compliance

### Validation Tools
- Use `skills-ref validate` for SKILL.md validation
- Implement internal validation in scripts
- Create test datasets for validation
- Document validation procedures

These best practices ensure that SSCI subagent skills maintain high quality, comply with the agentskills.io standard, and effectively serve the needs of Chinese social science research.