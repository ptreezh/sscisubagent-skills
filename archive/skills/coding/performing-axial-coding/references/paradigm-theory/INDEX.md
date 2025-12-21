# Paradigm模型理论概览

> **渐进式学习**：本文档提供核心概念。详细内容见子文档。

## 什么是Paradigm模型

Paradigm（范式）模型是Strauss & Corbin（1990, 1998）提出的轴心编码核心工具，用于系统化地建立范畴间的逻辑关系。

**核心价值**：
- 将零散的范畴整合为系统性的理论框架
- 揭示社会现象的内在逻辑和机制
- 为理论构建提供清晰的分析路径

**基本结构**：
```
因果条件 → 现象 → 行动策略 → 结果
         ↑              ↑
      语境条件      中介条件
```

## Paradigm的六个组件（快速参考）

### 1. 现象（Phenomenon）
**定义**：研究的核心事件、中心议题

**识别**：反复出现的主题、连接最多的范畴

**案例**：学业适应困难

**详见**：`six-components.md` - 第1节

---

### 2. 因果条件（Causal Conditions）
**定义**：导致现象发生的事件、情境

**识别**：寻找"导致"、"引起"、"因为"等关键词

**案例**：学习方法差异、课程难度提升

**详见**：`six-components.md` - 第2节

---

### 3. 语境（Context）
**定义**：现象发生的特定情境、背景

**识别**：回答"在什么条件下"、"在哪里"

**案例**：重点大学竞争环境、远离家乡

**详见**：`six-components.md` - 第3节

---

### 4. 中介条件（Intervening Conditions）
**定义**：促进或限制行动策略的结构性因素

**识别**：分析为什么同样的行动效果不同

**案例**：个人性格、社会支持、学校资源

**详见**：`six-components.md` - 第4节

---

### 5. 行动/互动策略（Action/Interaction Strategies）
**定义**：应对现象而采取的有目的行动

**识别**：寻找动词短语（"寻求"、"调整"、"建立"）

**案例**：寻求学业支持、调整学习方法

**详见**：`six-components.md` - 第5节

---

### 6. 结果（Consequences）
**定义**：行动/互动策略产生的结果

**识别**：分析短期/长期、预期/非预期结果

**案例**：成绩提升、自信增强、过度依赖

**详见**：`six-components.md` - 第6节

---

## 理论流派对比

| 流派 | 代表人物 | 核心特点 | 适用场景 |
|-----|---------|---------|---------|
| **Strauss流派** | Strauss & Corbin | 结构化编码程序 | 初学者、系统研究 |
| **Glaser流派** | Glaser | 理论自然涌现 | 经验丰富者 |
| **建构主义** | Charmaz | 强调主观建构 | 解释主义研究 |

**本技能采用**：Strauss & Corbin流派（结构化、系统化）

**详见**：`six-components.md` - 理论流派章节

---

## 中国本土化要点

**关键适配**：
- 关系导向：将"关系"作为独立分析维度
- 集体主义：分析个人与集体的关系
- 面子文化：考虑"面子"如何影响行动选择
- 权威尊重：分析权威的影响

**详见**：`chinese-adaptation.md`

---

## 质量标准（快速检查）

**完整性**：
- [ ] 所有六个组件都有数据支持
- [ ] 逻辑链条清晰连贯

**密度**：
- [ ] 范畴间有丰富的关系
- [ ] 关系有充分证据

**变异性**：
- [ ] 考虑了不同情境的变化
- [ ] 识别了中介条件

**整合性**：
- [ ] 核心现象明确
- [ ] 形成连贯的理论故事

**详见**：`quality-standards.md`

---

## 工具支持

本技能提供4个核心脚本辅助Paradigm构建：

```bash
# 1. 识别核心范畴
python scripts/identify_categories.py --input codes.json

# 2. 建立关系
python scripts/build_relationships.py --input categories.json

# 3. 构建Paradigm
python scripts/construct_paradigm.py --input relationships.json

# 4. 分析属性（可选）
python scripts/analyze_properties.py --input categories.json
```

**注意**：工具提供初步分析，最终判断需要研究者的理论敏感性。

---

## 下一步学习

**理论深化**：
- 阅读 `six-components.md` 了解六个组件的详细说明
- 阅读 `chinese-adaptation.md` 了解中国本土化实践

**实践应用**：
- 跳转到 `../category-construction/INDEX.md` 开始范畴构建
- 跳转到 `../relationship-types/INDEX.md` 学习关系识别

**问题解决**：
- 跳转到 `../troubleshooting/INDEX.md` 查看常见问题

---

## 参考文献

- Strauss, A., & Corbin, J. (1998). *Basics of Qualitative Research* (2nd ed.). Sage.
- 陈向明 (2000). 《质的研究方法与社会科学研究》. 教育科学出版社.

---

*文档大小：约1000字 | 阅读时间：3分钟*
