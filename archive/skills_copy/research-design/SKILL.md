---
name: research-design
description: 研究设计技能，为社会科学研究提供系统的设计框架，包括研究问题构建、方法选择、数据收集和分析策略
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [research-design, social-science-methodology, study-planning, research-strategy, methodological-framework]
---

# Research Design Skill

## 技能概述

为社会科学研究提供系统性的研究设计框架，帮助研究者构建严谨的研究方案，从问题提出到数据分析的全过程规划。

## 核心功能

### 1. 研究问题构建
- **问题识别**: 从现象到研究问题的转化
- **问题细化**: 将研究问题分解为可操作的子问题
- **问题评估**: 评估问题的可行性、重要性和创新性
- **概念操作化**: 将抽象概念转化为可测量的指标

### 2. 研究方法选择
- **方法匹配**: 根据研究问题选择合适的方法
- **方法评估**: 评估不同方法的优缺点和适用性
- **方法整合**: 多方法设计和三角验证策略
- **创新方法**: 探索新的研究方法和技术

### 3. 研究设计框架
```python
class ResearchDesignFramework:
    """研究设计框架"""

    def __init__(self):
        self.design_components = {
            'research_question': self._formulate_question,
            'literature_review': self._review_literature,
            'methodology': self._design_methodology,
            'sampling': self._design_sampling,
            'data_collection': self._plan_collection,
            'data_analysis': self._plan_analysis,
            'ethics': self._address_ethics
        }

    def develop_research_plan(self, research_topic: str, objectives: list):
        """开发研究计划"""
        plan = {
            'research_questions': self._generate_questions(research_topic, objectives),
            'literature_review': self._conduct_review(research_topic),
            'methodology': self._select_methodology(research_topic, objectives),
            'sampling_strategy': self._design_sampling(research_topic),
            'data_collection_plan': self._create_collection_plan(research_topic),
            'analysis_strategy': self._create_analysis_plan(research_topic),
            'timeline': self._estimate_timeline(objectives),
            'resources': self._estimate_resources(research_topic)
        }
        return plan
```

### 4. 数据收集策略
- **数据类型选择**: 定性、定量或混合数据
- **收集方法**: 问卷调查、访谈、观察、文档分析等
- **工具开发**: 问卷、访谈提纲、观察表等
- **质量控制**: 数据收集过程的质量监控

### 5. 分析策略设计
- **分析方法**: 统计分析、质性分析、混合分析
- **软件工具**: SPSS、R、NVivo、Atlas.ti等
- **验证策略**: 信度效度检验、三角验证
- **结果解释**: 结果的理论和实践意义

## 设计流程

### 第一步：研究问题明确
- 识别研究现象和问题
- 构建清晰的研究问题
- 确定研究目标和假设
- 定义核心概念

### 第二步：文献回顾
- 搜索相关文献
- 识别研究空白
- 确定理论基础
- 评估现有方法

### 第三步：方法论选择
- 选择研究范式（定量/定性/混合）
- 确定研究策略
- 选择数据收集方法
- 设计分析计划

### 第四步：研究设计实施
- 制定详细计划
- 开发测量工具
- 确定样本策略
- 规划时间进度

## 中国社会研究特殊考虑

### 1. 文化背景
- 考虑中国文化背景对研究的影响
- 适应中国社会的特殊性
- 重视关系和面子文化
- 考虑集体主义与个人主义

### 2. 伦理考量
- 尊重中国社会的伦理规范
- 考虑敏感话题的处理
- 保护参与者隐私
- 遵活适应当地伦理要求

### 3. 实践相关性
- 关注研究的实践意义
- 考虑政策和管理应用
- 重视社会影响
- 与本土理论结合

## 质量标准

### 1. 设计质量
- 研究问题清晰明确
- 方法选择合理适当
- 设计逻辑严密
- 可操作性强

### 2. 科学性标准
- 理论基础扎实
- 方法论严谨
- 数据质量可控
- 分析策略恰当

### 3. 实用性标准
- 研究结果可推广
- 实施可行性高
- 资源利用合理
- 时间安排现实

## 工具和资源

### 1. 设计模板
- 研究计划模板
- 伦理审查申请模板
- 数据收集工具模板
- 分析框架模板

### 2. 评估清单
- 研究问题评估清单
- 方法选择评估清单
- 质量控制清单
- 伦理合规清单

### 3. 指南文档
- 研究设计指南
- 方法论选择指南
- 数据收集指南
- 分析策略指南

## 常见问题与解决方案

### 1. 问题模糊
- **挑战**: 研究问题不够明确
- **解决**: 使用问题细化技术，明确边界和范围

### 2. 方法不当
- **挑战**: 方法与问题不匹配
- **解决**: 重新评估问题-方法匹配度

### 3. 资源不足
- **挑战**: 时间、经费或人力不足
- **解决**: 调整研究范围或寻求合作

### 4. 伦理问题
- **挑战**: 研究伦理审查困难
- **解决**: 提前规划伦理问题，寻求指导

## 成功指标

### 1. 设计完整性
- 所有设计要素完整
- 逻辑关系清晰
- 可操作性强
- 风险评估充分

### 2. 方法适宜性
- 方法与问题匹配
- 方法可行性高
- 资源要求合理
- 伦理合规

### 3. 实施可行性
- 时间安排合理
- 资源分配适当
- 风险应对充分
- 质量控制有效

---

*此技能为中文社会科学研究提供系统性的研究设计支持，确保研究的科学性和可行性。*