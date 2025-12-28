---
name: validity-reliability
description: 研究信度效度分析工具，提供内部一致性、重测信度、评分者信度、构念效度、内容效度、效标效度等全面分析
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [reliability, validity, research-methods, psychometrics, measurement]
---

# Validity and Reliability Analysis Skill

## Overview
信度效度分析技能为社会科学研究提供全面的测量质量评估，包括信度分析（内部一致性、重测信度、评分者信度）和效度分析（内容效度、构念效度、效标效度），确保研究工具的科学性和有效性。

## When to Use This Skill
Use this skill when the user requests:
- Reliability analysis of research instruments
- Internal consistency assessment (Cronbach's Alpha, Omega)
- Test-retest reliability evaluation
- Inter-rater reliability analysis
- Validity assessment of measurement tools
- Content validity evaluation
- Construct validity testing (EFA, CFA)
- Criterion validity analysis
- Factor analysis for scale validation
- Scale development and refinement

## Quick Start
When a user requests reliability and validity assessment:
1. **Evaluate** the measurement design and data quality
2. **Assess** reliability using appropriate coefficients
3. **Test** validity through factor analysis and other methods
4. **Interpret** results in the context of measurement theory
5. **Recommend** improvements if needed

## Core Functions (Progressive Disclosure)

### Primary Functions
- **Internal Consistency**: Cronbach's Alpha, item-total correlations
- **Factor Analysis**: Exploratory Factor Analysis (EFA) for structure
- **Convergent Validity**: Average Variance Extracted (AVE), factor loadings
- **Basic Reporting**: Standardized reliability and validity statistics

### Secondary Functions
- **Test-Retest Reliability**: Stability over time
- **Inter-rater Reliability**: Agreement among evaluators
- **Discriminant Validity**: Fornell-Larcker criterion, HTMT
- **Item Analysis**: Difficulty, discrimination indices

### Advanced Functions
- **Confirmatory Factor Analysis**: Model fit testing, CFA
- **Measurement Invariance**: Cross-group comparisons
- **Composite Reliability**: Construct reliability assessment
- **Higher-Order Models**: Complex factor structures

## Detailed Instructions

### 1. Measurement Design Evaluation
   - Review scale structure and item design
   - Check for potential response biases
   - Assess item wording and clarity
   - Verify response format appropriateness

### 2. Data Quality Check
   - Handle missing values appropriately
   - Detect and address outliers
   - Assess distribution characteristics
   - Verify sample size adequacy

### 3. Reliability Analysis
   - Calculate various reliability coefficients
   - Assess confidence intervals
   - Identify problematic items
   - Evaluate dimensionality

### 4. Validity Verification
   - Conduct factor analysis (EFA/CFA)
   - Test convergent and discriminant validity
   - Assess criterion-related validity
   - Evaluate content validity evidence

### 5. Quality Improvement Recommendations
   - Suggest specific scale improvements
   - Recommend item revisions or removal
   - Propose additional validation studies
   - Provide reporting guidelines

## Parameters
- `analysis_type`: Type of analysis (reliability, validity, combined)
- `data_format`: Format of input data (CSV, Excel, SPSS, etc.)
- `scale_items`: List of items to analyze
- `sample_size`: Number of participants/respondents
- `factor_structure`: Expected factor structure (if known)
- `validation_criteria`: External criteria for criterion validity
- `report_format`: Format for output (APA, journal-specific, etc.)

## Examples

### Example 1: Internal Consistency
User: "Assess the internal consistency of this 20-item scale"
Response: Calculate Cronbach's Alpha, Omega coefficient, item-total correlations, identify problematic items.

### Example 2: Factor Analysis
User: "Perform EFA to identify the factor structure of this scale"
Response: Conduct exploratory factor analysis, determine optimal number of factors, interpret factor loadings, suggest modifications.

### Example 3: Construct Validity
User: "Test the construct validity of this new measure"
Response: Perform CFA, assess model fit, evaluate convergent and discriminant validity, interpret results.

## Quality Standards

- Follow psychometric best practices
- Provide APA-formatted statistical reports
- Include effect sizes and confidence intervals
- Conduct multiple comparison corrections when appropriate
- Verify model assumption conditions

## Output Format

- Complete reliability and validity analysis report
- Standardized statistical tables
- Factor structure visualizations
- Measurement model path diagrams
- Reproducible analysis code

## Resources
- Best practices in psychometrics
- Guidelines for scale development and validation
- Statistical software syntax for reliability/validity analysis
- Python toolkit: `skills/validity-reliability/scripts/validity_reliability_toolkit.py`

## Metadata
- Compatibility: Claude 3.5 Sonnet and above
- Domain: Psychometrics and Scale Development
- Language: Optimized for Chinese research context