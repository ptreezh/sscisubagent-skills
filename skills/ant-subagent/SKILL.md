---
name: ant-subagent
description: 行动者网络理论子智能体，提供网络分析、参与者识别和转译过程分析的统一接口
version: 1.0.0
author: socienceAI.com
license: MIT
tags: [ant, actor-network-theory, subagent, network-analysis, participant-identification]
compatibility: Claude 3.5 Sonnet and above, iFlow CLI
metadata:
  domain: sociology
  methodology: actor-network-theory
  complexity: advanced
  last_updated: "2025-12-20"
allowed-tools: [python, bash, read_file, write_file]
---

# ANT Subagent (Actor-Network Theory Subagent)

## Skill Overview
The ANT Subagent is a comprehensive Actor-Network Theory analysis tool that provides a unified interface for analyzing networks of human and non-human actors. This subagent integrates network analysis, participant identification, and translation processes within the theoretical framework of Actor-Network Theory.

## Theoretical Framework
Actor-Network Theory (ANT) is a theoretical framework that maps relationships between actors - both human and non-human - in a network. It emphasizes the importance of connections and translations between actors in shaping social phenomena. This subagent implements core ANT concepts including:

- Actor identification (both human and non-human)
- Network mapping and visualization
- Translation processes (problematisation, interessement, enrollment, mobilization)
- Symmetry between human and non-human actors
- Network stabilization and destabilization

## Core Capabilities
1. **Network Analysis**: Comprehensive mapping and analysis of actor networks
2. **Participant Identification**: Identification of both human and non-human actors in the network
3. **Translation Process Analysis**: Analysis of how actors are enrolled and mobilized in networks
4. **Network Visualization**: Visual representation of actor relationships and connections

## Usage
```
ant-subagent [options] [input_data]
```

## Options
- `--analyze-network`: Perform comprehensive network analysis
- `--identify-participants`: Identify all actors in the network (human and non-human)
- `--trace-translation`: Analyze translation processes in the network
- `--visualize-network`: Generate network visualization
- `--input-file`: Path to input data file
- `--output-format`: Output format (json, markdown, html)

## Input Requirements
- Text data describing social phenomena or systems
- Network data with actor relationships
- Qualitative data for translation process analysis

## Output Format
- JSON: Structured data with network analysis results
- Markdown: Human-readable analysis report
- HTML: Interactive network visualization

## Integration Points
This subagent integrates the following capabilities:
- Network analysis (from ant-network-analysis)
- Participant identification (from ant-participant-identification) 
- Translation process analysis (from ant-translation-process)

## Quality Assurance
- Theoretical consistency with ANT principles
- Comprehensive actor identification
- Accurate translation process mapping
- Valid network visualization

## Standards Compliance
- Adheres to agentskills.io standards
- Implements progressive disclosure principles
- Maintains theoretical rigor
- Follows technical implementation standards