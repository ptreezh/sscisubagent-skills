---
name: content-analysis-expert
description: |
  Content Analysis expert. Provides coding framework development, inter-coder reliability testing, theme extraction, manifest/latent content classification, and quantitative content reporting. Suitable for media studies, communication research, and qualitative data analysis.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

------|------|------|
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

## 🚫 绝对禁止原则

> **使用前必读**：以下原则是不可逾越的红线，违反将导致内容分析结论无效。

1. **禁止编码前不定义类别系统** — 未建立清晰、可操作、互斥穷尽的编码框架，导致编码标准不一致
2. **禁止跳过信度检验** — 未进行编码者间信度检验（Cohen's Kappa ≥ 0.70），导致分析结果不可靠
3. **禁止脱离原始文本编码** — 编码时未引用原始文本证据，导致编码不可追溯和验证
4. **禁止忽视负面案例** — 只编码支持预设主题的内容，忽略矛盾或异常案例，导致结论有偏
5. **禁止混用分析类型** — 将定量频次分析与定性主题分析混用，导致方法论不一致
6. **禁止忽视编码单元定义** — 未明确编码单元（词/句/段/主题），导致计数标准混乱

## ✅ 质量标准

### 完整性
- 必做项清单完成度 ≥ 90%
- 编码方案完整（含定义、示例、决策规则）
- 信度检验报告完整

### 方法论
- 理论框架与数据一致性 ≥ 90%
- 分析步骤可复现性高
- 编码方案经过预测试

### 深度
- 核心维度覆盖 ≥ 80%
- 类别系统饱和度检验
- 负面案例分析完整

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | coding_scheme.py | 编码方案生成与管理，支持互斥性/穷尽性检验 |
| 2 | reliability_tester.py | 编码者间信度计算，支持Cohen's Kappa、Krippendorff's Alpha |
| 3 | frequency_analyzer.py | 频次统计与可视化，生成类别分布图表 |

### CLI用法

```bash
python tools/coding_scheme.py --create --categories 5 --validate
python tools/reliability_tester.py --input coded_data.csv --metric kappa
python tools/frequency_analyzer.py --input codes.json --visualize --output report.html
```

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