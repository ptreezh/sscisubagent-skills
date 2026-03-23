---
name: content-analysis-expert
description: |
  内容分析专家。提供系统化内容分析方法，支持经典内容分析、定向内容分析、归纳内容分析。
  核心能力包括：编码方案设计、编码簿开发、编码者间信度检验（Cohen's Kappa, Krippendorff's Alpha）、
  频次统计、 contingency分析、语义网络分析。遵循Krippendorff (2018)和Schreier (2012)方法论标准。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
  methodology: "Krippendorff (2018), Schreier (2012), Mayring (2014)"
---

# 内容分析专家 (Content Analysis Expert)

## 概述

内容分析专家是一个系统化的文本分析方法论技能，支持对文本、图像、音频等传播内容进行客观、系统、定量的分析。遵循Krippendorff (2018)内容分析方法论标准。

## 核心方法论

### 1. 经典内容分析（Classical Content Analysis）
- **定义**：对传播内容进行客观、系统、定量的描述
- **特点**：演绎式、假设驱动、预定义类别
- **适用场景**：媒体内容研究、传播效果研究

### 2. 定向内容分析（Directed Content Analysis）
- **定义**：基于现有理论或研究进行编码
- **特点**：理论驱动、验证性、修正类别
- **适用场景**：理论验证、概念测量

### 3. 归纳内容分析（Inductive Content Analysis）
- **定义**：从数据中涌现类别
- **特点**：数据驱动、探索性、开放编码
- **适用场景**：新领域探索、概念发展

## 分析流程

```
步骤1: 研究问题定义
   ↓
步骤2: 样本选择与抽样
   ↓
步骤3: 编码方案开发
   ↓
步骤4: 编码者培训
   ↓
步骤5: 预测试与修订
   ↓
步骤6: 正式编码
   ↓
步骤7: 信度检验
   ↓
步骤8: 数据分析
   ↓
步骤9: 结果报告
```

## 编码方案设计

### 类别系统
- **互斥性（Mutual Exclusivity）**：每个单元只能归入一个类别
- **穷尽性（Exhaustiveness）**：所有单元都能被归类
- **独立性（Independence）**：一个单元的分类不影响其他单元

### 编码单元类型
| 单元类型 | 定义 | 示例 |
|---------|------|------|
| 物理单元 | 计数单位 | 字数、页数、秒数 |
| 语法单元 | 语言结构 | 句子、段落、章节 |
| 命题单元 | 意义单位 | 主题、论点、断言 |
| 主题单元 | 内容单位 | 角色、话题、事件 |

## 编码者间信度

### 信度系数

| 系数 | 适用数据 | 公式 | 可接受值 |
|------|---------|------|---------|
| Cohen's Kappa | 名义变量 | (Po-Pe)/(1-Pe) | ≥ 0.70 |
| Krippendorff's Alpha | 各类数据 | 1-Do/De | ≥ 0.80 |
| Scott's Pi | 名义变量 | (Po-Pe)/(1-Pe) | ≥ 0.75 |
| 百分比一致 | 所有类型 | 同意数/总数 | ≥ 0.90 |

### 信度检验步骤
1. 随机抽取10-20%样本
2. 独立编码
3. 计算信度系数
4. 解决编码分歧
5. 达到可接受水平后继续

## 统计分析

### 描述性统计
- 类别频次分布
- 百分比统计
- 趋势分析

### 推断性统计
- 卡方检验
- 列联表分析
- 相关分析
- 回归分析

## 使用示例

```
用户: 分析这批新闻报道关于气候变化的框架

AI: 我将采用定向内容分析方法，步骤如下：

1. **框架识别**
   - 经济框架
   - 环境框架  
   - 政治框架
   - 科学框架
   - 道德框架

2. **编码方案**
   [详细编码簿...]

3. **信度检验**
   Cohen's Kappa = 0.85 (可接受)

4. **分析结果**
   框架频次分布...
   框架间关联...
```

## 工具函数

| 工具 | 功能 |
|------|------|
| `coding_scheme.py` | 编码方案生成与管理 |
| `reliability_tester.py` | 编码者间信度计算 |
| `frequency_analyzer.py` | 频次统计与可视化 |
| `contingency_analyzer.py` | 列联表分析 |

## 输出格式

```markdown
# 内容分析报告

## 研究问题
[明确的研究问题]

## 方法
- 分析类型：[经典/定向/归纳]
- 样本量：N = [数量]
- 编码单元：[单元类型]
- 编码者数量：[数量]

## 信度检验
| 指标 | 值 | 判断 |
|-----|-----|-----|
| Cohen's Kappa | 0.85 | 优秀 |

## 主要发现
[详细分析结果]

## 讨论
[解释与建议]
```

## 参考文献

1. Krippendorff, K. (2018). *Content Analysis: An Introduction to Its Methodology*. 4th ed. Sage.
2. Schreier, M. (2012). *Qualitative Content Analysis in Practice*. Sage.
3. Mayring, P. (2014). *Qualitative Content Analysis: Theoretical Foundation, Basic Procedures and Software Solution*. Klagenfurt.
4. Neuendorf, K.A. (2017). *The Content Analysis Guidebook*. 2nd ed. Sage.
5. Hsieh, H.F., & Shannon, S.E. (2005). Three approaches to qualitative content analysis. *Qualitative Health Research*, 15(9), 1277-1288.

---

**技能版本**: 5.0.0  
**方法论标准**: Krippendorff (2018)  
**创建时间**: 2026-03-15