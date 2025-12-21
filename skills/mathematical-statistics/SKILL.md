---
name: mathematical-statistics
description: 社会科学研究数理统计分析工具，提供描述性统计、推断统计、回归分析、方差分析、因子分析等完整统计支持
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [statistics, social-sciences, data-analysis, research-methods]
---

# Mathematical Statistics Skill for Social Sciences

## Overview
数理统计技能为社会科学研究提供全面的统计分析支持，包括描述性统计、推断统计、回归分析、方差分析、因子分析等，确保研究数据分析的科学性和准确性。

## When to Use This Skill
Use this skill when the user requests:
- Statistical analysis of social science data
- Descriptive statistics (means, standard deviations, distributions)
- Inferential statistics (t-tests, ANOVA, chi-square tests)
- Regression analysis (linear, logistic, multiple)
- Factor analysis or other multivariate techniques
- Reliability and validity analysis
- Data visualization for statistical results
- Interpretation of statistical outputs

## Quick Start
When a user requests statistical analysis:
1. **Understand** the research question and data structure
2. **Select** appropriate statistical methods based on data and question
3. **Execute** analysis with proper diagnostics
4. **Interpret** results in the context of the research question
5. **Visualize** findings appropriately

## Core Functions (Progressive Disclosure)

### Primary Functions
- **Descriptive Statistics**: Central tendency, dispersion, distribution shape
- **Inferential Statistics**: Hypothesis testing, confidence intervals
- **Regression Analysis**: Linear, logistic, and multiple regression
- **Analysis of Variance**: One-way, multi-way, repeated measures ANOVA

### Secondary Functions
- **Multivariate Analysis**: Factor analysis, discriminant analysis
- **Reliability Analysis**: Cronbach's Alpha, test-retest reliability
- **Effect Size Calculation**: Cohen's d, eta squared, odds ratios
- **Model Diagnostics**: Residual analysis, assumption checking

### Advanced Functions
- **Confirmatory Factor Analysis**: Model fit, validation
- **Advanced Modeling**: Hierarchical regression, mediation analysis
- **Bayesian Statistics**: Posterior estimation, model comparison
- **Power Analysis**: Sample size planning, post-hoc power

## Detailed Instructions

### 1. Data Preparation
   - Check data quality and completeness
   - Identify and handle missing values
   - Verify data types and distributions
   - Assess assumptions for planned analyses

### 2. Method Selection
   - Match statistical method to research question
   - Consider data characteristics (scale, distribution, sample size)
   - Account for study design (between/within subjects, experimental/control)
   - Verify assumptions for chosen method

### 3. Analysis Execution
   - Perform appropriate statistical tests
   - Calculate relevant effect sizes
   - Generate confidence intervals
   - Conduct diagnostic checks

### 4. Result Interpretation
   - Report statistical significance appropriately
   - Interpret effect sizes in practical context
   - Consider statistical power and limitations
   - Provide clear, jargon-free explanations

### 5. Visualization
   - Create appropriate charts for data distribution
   - Generate plots for relationship visualization
   - Provide publication-ready figures
   - Include error bars and confidence intervals

## Parameters
- `analysis_type`: Type of statistical analysis (descriptive, inferential, regression, etc.)
- `data_format`: Format of input data (CSV, Excel, JSON, etc.)
- `variables`: List of variables to analyze
- `hypothesis_type`: Type of hypothesis test (one-tailed, two-tailed)
- `confidence_level`: Confidence level for intervals (default 0.95)
- `effect_size`: Request for effect size calculation
- `visualization`: Request for data visualization

## Examples

### Example 1: Descriptive Analysis
User: "Analyze this survey data and provide descriptive statistics"
Response: Perform descriptive analysis, calculate central tendency and dispersion measures, create appropriate visualizations.

### Example 2: Regression Analysis
User: "Run a regression to predict job satisfaction from work conditions"
Response: Conduct multiple regression analysis, check assumptions, report coefficients and model fit, interpret results.

### Example 3: ANOVA
User: "Compare performance across three training groups"
Response: Perform one-way ANOVA, conduct post-hoc tests if significant, report effect sizes, interpret findings.

## Quality Assurance

- Follow statistical analysis best practices
- Verify statistical assumptions before analysis
- Report effect sizes and confidence intervals
- Conduct multiple comparison corrections when appropriate
- Validate model robustness

## Output Format

- Complete statistical analysis report
- Standardized statistical tables
- Publication-quality visualizations
- APA-formatted results reporting
- Reproducible Python/R code

## Resources
- Statistical analysis best practices guidelines
- APA formatting standards for statistics
- Common statistical software syntax (Python, R, SPSS)
- Python toolkit: `skills/mathematical-statistics/scripts/statistics_toolkit.py`

## Metadata
- Compatibility: Claude 3.5 Sonnet and above
- Domain: Social Sciences Research
- Language: Optimized for Chinese research context