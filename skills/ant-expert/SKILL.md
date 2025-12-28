---
name: ant-expert
description: 行动者网络理论专家分析技能，整合参与者识别、网络分析和转译过程追踪功能，提供全面的ANT分析框架
version: 1.0.0
author: socienceAI.com
license: MIT
tags: [actor-network-theory, ANT, science-technology-studies, socio-technical, networks, participant-identification, network-analysis, translation-process]
compatibility: Claude 3.5 Sonnet and above
metadata:
  domain: science-and-technology-studies
  methodology: actor-network-theory
  complexity: advanced
  integration_type: analysis_tool
  last_updated: "2025-12-27"
allowed-tools: [python, bash, read_file, write_file]
---

# 行动者网络理论专家分析技能 (ANT Expert Analysis)

## 概述

行动者网络理论专家分析技能整合了参与者识别、网络分析和转译过程追踪功能，为社会科学研究提供全面的ANT分析框架。该技能帮助研究者识别人类和非人类行动者、构建关系网络、追踪网络构建过程并分析网络动态。

## 使用时机

当用户请求以下分析时使用此技能：
- 涉及人类和非人类行动者的社会技术网络分析
- 网络中行动者（人类和非人类）的识别
- 转译过程和网络构建的追踪
- 事实、技术或实践构建过程的分析
- 异质网络中权力关系的理解
- 网络稳定化或去稳定化过程的调查
- 物质对象在社会过程中的作用检验
- 创新过程和技术采纳的研究
- 政策网络和实施过程的分析
- 科学知识构建过程的调查

## 快速开始

当用户请求ANT分析时：
1. **绘制**所有相关人类和非人类行动者
2. **追踪**行动者间的连接
3. **跟随**转译过程（问题化到动员）
4. **分析**物质-符号关系
5. **评估**网络稳定性和动态

## 核心功能（渐进式披露）

### 主要功能
- **行动者识别**: 识别人类和非人类行动者
- **网络分析**: 分析网络拓扑和结构
- **转译过程追踪**: 追踪问题化、利益化、征召和动员
- **基本习性**: 理解参与者的倾向

### 次要功能
- **边界分析**: 定义网络边界和排除
- **关系动态**: 分析网络中关系的强度和性质
- **自主性评估**: 评估独立于外部力量的程度
- **历史分析**: 追溯网络发展的时间线

### 高级功能
- **符号暴力**: 识别支配和误解的机制
- **多网络分析**: 检查网络间的关系
- **网络演化**: 分析网络结构的变化
- **复杂习性**: 检查习性如何使能/限制实践

## 详细指令

### 第一阶段：行动者识别与映射
   - 识别所有相关的人类和非人类行动者
   - 确定行动者间的关系
   - 评估不同行动者的能动性
   - 绘制初始网络配置
   - 考虑核心和边缘行动者

### 第二阶段：网络分析
   - 追踪行动者间的连接
   - 分析关系的强度和性质
   - 识别关键中介和转译中介
   - 绘制网络拓扑
   - 考虑网络边界和排除

### 第三阶段：转译过程追踪
   - 识别问题化阶段
   - 追踪利益化和征召过程
   - 分析动员策略
   - 检查利益如何被转译
   - 考虑转译失败的时刻

### 第四阶段：物质符号分析
   - 检查非人类行动者的能动性
   - 分析社会-物质纠缠
   - 识别技术与对象中的脚本
   - 考虑物质安排如何塑造社会关系
   - 理解物质安排的表演性

### 第五阶段：网络动态评估
   - 分析稳定或去稳定网络的因素
   - 识别变化和转换的时刻
   - 检查网络内的权力关系
   - 考虑潜在的未来发展
   - 评估网络的鲁棒性

### 第六阶段：综合与解释
   - 整合所有维度的发现
   - 将ANT分析与更广泛的社会过程联系起来
   - 考虑中国社会背景和文化特殊性
   - 提供可操作的见解

## 参数
- `analysis_type`: 分析类型 (actors, network, translation, comprehensive)
- `actor_type`: 行动者类型 (human, non-human, hybrid)
- `network_scope`: 网络分析范围 (local, regional, global)
- `translation_phase`: 转译阶段 (problematization, interessement, enrollment, mobilization)
- `agency_level`: 能动性水平 (high, medium, low)
- `methodology`: 分析方法 (qualitative, quantitative, mixed)
- `cultural_context`: 文化背景考虑 (特别是中文研究背景)

## 示例

### 示例 1: 技术采纳网络分析
User: "分析中国电动汽车采纳的行动者网络"
Response: 识别政府机构、汽车制造商、消费者、充电基础设施、电池技术、环境关切、法规等行动者，分析它们之间的关系和转译过程。

### 示例 2: 医疗网络分析
User: "分析远程医疗实施的行动者网络"
Response: 识别医生、患者、医院管理员、医疗设备、数字平台、健康数据、医疗协议、监管机构等行动者，追踪它们的转译过程。

### 示例 3: 政策实施网络分析
User: "分析农村教育政策实施的行动者网络"
Response: 识别政府官员、教师、学生、家长、学校、教育技术、教科书、互联网基础设施、当地社区等行动者，评估网络的稳定性。

## 质量标准

- 严格应用ANT原则（广义对称性、转译）
- 包括人类和非人类行动者
- 保持关系分析的重点
- 考虑历史和文化背景
- 提供基于证据的解释

## 输出格式

```json
{
  "summary": {
    "actors_identified": 25,
    "network_connections": 42,
    "translation_phases_completed": 4,
    "non_human_actors": 8,
    "stability_score": 0.78,
    "analysis_type": "comprehensive"
  },
  "details": {
    "actors": [...],
    "relationships": [...],
    "translation_process": {...},
    "network_dynamics": {...}
  },
  "metadata": {
    "timestamp": "2025-12-27T10:30:00",
    "version": "1.0.0"
  }
}
```

## 资源
- ANT理论著作（Latour, Callon, Law）
- ANT方法指南
- 科学技术研究文献
- 中国背景下ANT应用实例

## 完成标志

完成高质量的ANT分析应该：
1. 提供完整的行动者网络映射
2. 追踪完整的转译过程
3. 评估网络稳定性和动态
4. 分析物质-符号关系

---

*此技能为行动者网络理论分析提供专业的综合框架和工具，确保研究的科学性和严谨性。*