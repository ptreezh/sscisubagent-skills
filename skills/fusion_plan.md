# Comprehensive Fusion Plan for SSCI Subagent Skills

## Overview

This document outlines a comprehensive fusion plan for organizing the SSCI subagent skills into cohesive, well-structured subagent systems. Rather than eliminating skills, this plan proposes organizing related skills into parent-child relationships where appropriate, with each subagent having specialized modules that work together cohesively.

## 1. Actor-Network Theory (ANT) Subagent

### Current Skills:
- `ant` (main skill)
- `ant-network-analysis`
- `ant-participant-identification`
- `ant-translation-process`

### Proposed Structure:
```
ant/
├── SKILL.md (main orchestrator skill)
├── modules/
│   ├── network_analysis.py
│   ├── participant_identification.py
│   └── translation_process.py
├── scripts/
│   ├── ant_analysis_with_fallback.py (main orchestrator)
│   ├── identify_participants.py
│   ├── trace_translation.py
│   └── analyze_network.py
├── references/
└── tests/
```

### Relationship:
- The main `ant` skill acts as an orchestrator that can delegate to specialized modules
- Each specialized skill becomes a module within the comprehensive ANT framework
- The main skill provides a unified interface while maintaining specialized functionality

## 2. Field Analysis Subagent

### Current Skills:
- `field-analysis` (main skill)
- `field-boundary-identification`
- `field-capital-analysis`
- `field-habitus-analysis`

### Proposed Structure:
```
field-analysis/
├── SKILL.md (main orchestrator skill)
├── modules/
│   ├── boundary_identification.py
│   ├── capital_analysis.py
│   └── habitus_analysis.py
├── scripts/
│   ├── field_analyzer.py (main orchestrator)
│   ├── boundary_identifier.py
│   ├── capital_analyzer.py
│   └── habitus_analyzer.py
├── references/
└── tests/
```

### Relationship:
- The main `field-analysis` skill orchestrates the comprehensive field analysis process
- Specialized skills become modules focusing on specific aspects of field theory
- Each module contributes to the holistic field analysis framework

## 3. Grounded Theory Subagent

### Current Skills:
- `performing-open-coding`
- `performing-axial-coding`
- `performing-selective-coding`
- `checking-theory-saturation`
- `writing-grounded-theory-memos`

### Proposed Structure:
```
grounded-theory/
├── SKILL.md (comprehensive grounded theory framework)
├── stages/
│   ├── open_coding.py
│   ├── axial_coding.py
│   └── selective_coding.py
├── tools/
│   ├── saturation_checker.py
│   └── memo_writer.py
├── scripts/
│   ├── workflow_manager.py (coordinates between stages)
│   ├── data_passer.py (passes data between stages)
│   └── quality_checker.py (cross-stage quality checks)
├── references/
└── tests/
```

### Relationship:
- The grounded theory process follows a sequential workflow from open to axial to selective coding
- Each stage builds upon the previous one with specialized functionality
- Tools support the overall process with saturation checking and memo writing
- The subagent ensures seamless data flow between stages

## 4. Digital Marx Subagent

### Current Skills:
- `digital-marx` (main skill)
- `historical-materialist-analysis`
- `class-structure-analysis`
- `practical-marxist-application`
- `alienation-analysis`
- `dialectical-quantitative-synthesis`

### Proposed Structure:
```
digital-marx/
├── SKILL.md (comprehensive Marxist analysis framework)
├── modules/
│   ├── historical_materialism.py
│   ├── class_analysis.py
│   ├── alienation_analysis.py
│   ├── practical_application.py
│   └── dialectical_synthesis.py
├── scripts/
│   ├── marxist_analyzer.py (main orchestrator)
│   ├── historical_materialist_analyzer.py
│   ├── class_structure_analyzer.py
│   ├── alienation_analyzer.py
│   ├── practical_application_analyzer.py
│   └── dialectical_synthesizer.py
├── references/
└── tests/
```

### Relationship:
- The main `digital-marx` skill provides the overarching framework
- Each specialized skill becomes a module contributing to the comprehensive Marxist analysis
- The subagent integrates all Marxist concepts into a cohesive analytical system
- `alienation-analysis` is integrated as a core module rather than separate skill

## 5. Social Network Analysis (SNA) Subagent

### Current Skills:
- `network-computation` (main skill)
- `performing-network-computation`
- `processing-network-data`
- `performing-centrality-analysis`

### Proposed Structure:
```
network-computation/
├── SKILL.md (comprehensive SNA framework)
├── modules/
│   ├── data_processing.py
│   ├── network_analysis.py
│   └── centrality_analysis.py
├── scripts/
│   ├── network_computation_orchestrator.py (main orchestrator)
│   ├── data_processor.py
│   ├── network_analyzer.py
│   └── centrality_calculator.py
├── references/
└── tests/
```

### Relationship:
- Consolidate `network-computation` and `performing-network-computation` into a single comprehensive skill
- Maintain specialized functionality as modules within the unified SNA framework
- Create a clear workflow from data processing to network analysis to visualization

## 6. Alienation Analysis Integration

### Current Skills:
- `alienation_analysis` (incomplete)
- `alienation-analysis` (complete)

### Proposed Integration:
- Remove the incomplete `alienation_analysis` skill
- Integrate the complete `alienation-analysis` functionality into the digital-marx subagent as a core module
- Maintain the specialized alienation analysis capabilities within the broader Marxist framework

## Benefits of the Fusion Plan

### 1. Improved Organization
- Clear parent-child relationships between skills
- Reduced redundancy while maintaining functionality
- Better alignment with theoretical frameworks

### 2. Enhanced Usability
- Unified interfaces for complex analytical processes
- Clearer pathways for users to select appropriate tools
- Streamlined workflows for multi-stage analyses

### 3. Theoretical Coherence
- Skills organized around coherent theoretical frameworks
- Better integration between related concepts
- More holistic analytical approaches

### 4. Maintainability
- Centralized management of related functionality
- Easier updates and improvements
- Consistent quality standards across modules

## Implementation Strategy

### Phase 1: Consolidation
- Merge duplicate or overlapping skills
- Create unified skill directories with modular components
- Update documentation to reflect new structure

### Phase 2: Integration
- Implement orchestration between modules
- Create standardized interfaces between components
- Develop unified output formats

### Phase 3: Enhancement
- Add cross-module validation and quality checks
- Implement workflow management tools
- Create comprehensive testing frameworks

## Quality Assurance

### Consistency Standards
- Standardized input/output formats across all modules
- Consistent parameter naming conventions
- Unified error handling and validation
- Common documentation structure

### Theoretical Alignment
- Ensure all modules adhere to the parent theoretical framework
- Maintain consistency with original theoretical concepts
- Preserve specialized functionality within the integrated approach
- Validate theoretical coherence across modules

This fusion plan maintains the specialized functionality of individual skills while organizing them into cohesive, theoretically-grounded subagent systems that better serve the needs of Chinese social science research.