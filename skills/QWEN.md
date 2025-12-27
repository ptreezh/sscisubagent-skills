# SSCI Subagent Skills - Comprehensive Documentation

## Project Overview

This directory contains a comprehensive collection of specialized skills for Chinese social science research, implemented as part of the Stigmergy multi-agent system. Each skill is designed to support specific analytical tasks in social science research, following the agentskills.io standard and incorporating progressive disclosure principles.

The skills cover a wide range of methodologies including:
- Quantitative analysis (statistics, network analysis)
- Qualitative analysis (grounded theory coding)
- Theoretical frameworks (Actor-Network Theory, Bourdieu's Field Theory)
- Mixed-method approaches

## Architecture & Structure

The directory contains multiple skill implementations, each organized in its own subdirectory with the following structure:
```
skill-name/
├── SKILL.md          # Skill documentation with metadata
├── pyproject.toml    # Dependencies and project config
├── scripts/          # Implementation scripts
├── references/       # Additional documentation
├── tests/            # Test files (where applicable)
```

Each skill follows a standardized format with:
- YAML frontmatter metadata
- Clear usage instructions
- Progressive disclosure of functionality
- Standardized JSON output format
- Integration with the Claude skills system

## Key Skills Categories

### Quantitative Analysis Skills
- `mathematical-statistics`: Comprehensive statistical analysis toolkit
- `validity-reliability`: Psychometric validation tools
- `network-computation`: Social network analysis tools
- `performing-centrality-analysis`: Network centrality calculations

### Qualitative Analysis Skills
- `performing-open-coding`: Grounded theory open coding
- `performing-axial-coding`: Grounded theory axial coding
- `performing-selective-coding`: Grounded theory selective coding
- `writing-grounded-theory-memos`: Memo writing for grounded theory

### Theoretical Framework Skills
- `ant`: Actor-Network Theory analysis
- `ant-participant-identification`: ANT participant identification
- `ant-translation-process`: ANT translation process analysis
- `ant-network-analysis`: ANT network analysis
- `field-analysis`: Bourdieu's field theory analysis
- `field-boundary-identification`: Field boundary identification
- `field-capital-analysis`: Field capital analysis

### Specialized Research Skills
- `digital-marx`: Digital Marx analysis
- `digital-durkheim`: Digital Durkheim analysis
- `digital-weber`: Digital Weber analysis
- `conflict-resolution`: Conflict resolution in research
- `dissent-resolution`: Dissent resolution in research
- `research-design`: Research design framework

## Implementation Standards

### Technical Implementation
- Python-based implementations with standardized command-line interfaces
- Argparse for parameter handling
- Standardized three-layer JSON output format:
  1. Summary: Key metrics and overview
  2. Details: Complete analysis results
  3. Metadata: Processing information and context
- Error handling and validation
- Support for Chinese language processing (e.g., jieba for Chinese text)

### Theoretical Rigor
- Skills grounded in established social science theories
- Methodological principles clearly articulated
- Validity and reliability considerations addressed
- Cultural context integration (especially for Chinese research)

### Progressive Disclosure
- Core functions presented first
- Detailed instructions provided as needed
- Advanced features available for complex analyses
- Examples provided for common use cases

## Dependencies & Requirements

Most skills require Python 3.8+ and common data science libraries:
- pandas: Data manipulation
- numpy: Numerical computations
- scipy: Statistical functions
- networkx: Network analysis
- scikit-learn: Machine learning algorithms
- jieba: Chinese text processing
- matplotlib/seaborn: Visualization

Dependencies are specified in individual pyproject.toml files.

## Usage Patterns

Skills are designed to be used in the Claude environment with the following patterns:
1. Automatic skill selection based on user request
2. Standardized parameter interface
3. Rich output with actionable insights
4. Integration with broader research workflows

## Quality Assurance

- Skills follow established methodological standards
- Implementation includes validation and error checking
- Output formats are standardized across skills
- Cultural appropriateness for Chinese research context
- Integration with quality checklists and troubleshooting guides

## Integration with Claude Skills Standard

All skills:
- Follow the agentskills.io standard format
- Include YAML frontmatter with metadata
- Provide clear usage instructions
- Define parameters and expected outputs
- Include examples of use
- Specify compatibility and requirements

## Development Conventions

### Coding Standards
- Python 3.8+ compatibility
- Type hints for function parameters and return values
- Comprehensive error handling
- Standardized command-line interface using argparse
- UTF-8 encoding for Chinese language support

### Documentation Standards
- Complete SKILL.md documentation with metadata
- Clear "When to Use" sections
- Progressive disclosure of functionality
- Examples and use cases
- Quality checklists

## Building and Running

Skills are executed as command-line tools within the Claude environment:

```bash
# Example execution of a statistical analysis skill
python scripts/descriptive_statistics.py --input data.csv --output results.json

# Example execution of a network analysis skill
python scripts/calculate_centrality.py --input network.json --output centrality.json

# Example execution of an open coding skill
python scripts/auto_loader.py --input interview.txt --output concepts.json
```

## Future Development

### Planned Enhancements
- Additional statistical methods
- Advanced network analysis techniques
- Integration with more data formats
- Enhanced visualization capabilities
- More theoretical frameworks
- Cross-skill integration workflows

### Maintenance Requirements
- Regular review of theoretical foundations
- Updates to implementation based on feedback
- Expansion of cultural context considerations
- Integration with new analytical tools

### Organizational Structure and Fusion Plan

Based on analysis of the skills directory, the skills are organized around coherent theoretical frameworks rather than being redundant. The following organizational structure is recommended to better integrate related skills:

#### 1. Actor-Network Theory (ANT) Subagent
- `ant` (main orchestrator skill)
- `ant-network-analysis` (network analysis module)
- `ant-participant-identification` (participant identification module)
- `ant-translation-process` (translation process module)

These skills form a cohesive ANT analysis framework where the main skill orchestrates specialized modules.

#### 2. Field Analysis Subagent
- `field-analysis` (main orchestrator skill)
- `field-boundary-identification` (boundary identification module)
- `field-capital-analysis` (capital analysis module)
- `field-habitus-analysis` (habitus analysis module)

These skills form a comprehensive field analysis framework based on Bourdieu's theoretical approach.

#### 3. Grounded Theory Subagent
- `performing-open-coding` (open coding stage)
- `performing-axial-coding` (axial coding stage)
- `performing-selective-coding` (selective coding stage)
- `checking-theory-saturation` (saturation assessment tool)
- `writing-grounded-theory-memo` (documentation tool)

These skills represent the sequential stages of grounded theory methodology with supporting tools.

#### 4. Digital Marx Subagent
- `digital-marx` (main orchestrator skill)
- `historical-materialist-analysis` (historical materialism module)
- `class-structure-analysis` (class analysis module)
- `practical-marxist-application` (application module)
- `alienation-analysis` (alienation analysis module)
- `dialectical-quantitative-synthesis` (methodology module)

These skills form a comprehensive Marxist analysis framework integrating various theoretical components.

#### 5. Social Network Analysis (SNA) Subagent
- `network-computation` (main orchestrator skill)
- `performing-network-computation` (technical implementation)
- `processing-network-data` (data processing module)
- `performing-centrality-analysis` (centrality analysis module)

These skills form a complete network analysis workflow from data processing to analysis.

#### Fusion Plan

A detailed fusion plan has been developed to organize these skills into cohesive subagent systems. The plan maintains specialized functionality while creating clear parent-child relationships:

1. **ANT Subagent**: Integrates all ANT-related skills with the main `ant` skill as orchestrator
2. **Field Analysis Subagent**: Combines field theory skills under the main `field-analysis` skill
3. **Grounded Theory Subagent**: Creates a sequential workflow for grounded theory stages
4. **Digital Marx Subagent**: Unifies Marxist analysis components under `digital-marx`
5. **SNA Subagent**: Consolidates network analysis skills into a comprehensive framework

For complete details of the fusion plan, see the `fusion_plan.md` file in this directory.