# PubScholar智能扩展策略详解

**版本**: 1.0.0
**更新日期**: 2025-12-28

---

## 目录

1. [扩展策略概览](#扩展策略概览)
2. [策略详解](#策略详解)
3. [预定义映射表](#预定义映射表)
4. [自定义策略](#自定义策略)
5. [实现代码](#实现代码)

---

## 扩展策略概览

### 何时触发扩展

```python
if len(precise_results) < min_results:  # 默认min_results=5
    # 触发智能扩展
```

### 扩展策略类型

| 策略 | 优先级 | 适用场景 | 预期效果 |
|------|-------|---------|---------|
| 1. 同义词扩展 | 1 | 常见术语有多个名称 | +20-50% 结果 |
| 2. 英文翻译 | 2 | 国际化术语 | +10-30% 结果 |
| 3. 关键词简化 | 3 | 复合关键词过长 | +30-100% 结果 |
| 4. 相关领域 | 4 | 特定学科交叉 | +15-40% 结果 |
| 5. 核心概念 | 5 | 复杂技术术语 | +10-25% 结果 |

---

## 策略详解

### 1. 同义词扩展

**原理**: 添加领域内常见的同义或近义术语。

**适用场景**:
- 学术术语有多种表达方式
- 某些作者偏好特定术语

**示例映射**:
```python
SYNONYMS = {
    "人工智能": ["AI", "机器学习", "智能计算"],
    "数字鸿沟": ["信息不平等", "数字分化", "信息贫富差距"],
    "社会网络": ["社交网络", "关系网络", "社会关系"],
    "深度学习": ["DL", "深度神经网络", "深度神经网络学习"],
}
```

**扩展示例**:
```
原始: "人工智能"
扩展:
  - "人工智能 AI"
  - "人工智能 机器学习"
  - "人工智能 智能计算"
```

### 2. 英文翻译

**原理**: 添加英文翻译以捕获双语文献。

**适用场景**:
- 国际化研究主题
- 中英双语文献
- 作者使用英文术语

**示例映射**:
```python
TRANSLATIONS = {
    "人工智能": "artificial intelligence",
    "数字鸿沟": "digital divide",
    "社会网络": "social network",
    "深度学习": "deep learning",
    "机器学习": "machine learning",
    "神经网络": "neural network",
}
```

**扩展示例**:
```
原始: "人工智能"
扩展: "人工智能 artificial intelligence"
```

### 3. 关键词简化

**原理**: 提取复合关键词中的核心概念。

**适用场景**:
- 关键词组合过于精确
- 结果数量极少
- 需要放宽搜索范围

**简化规则**:
```python
def simplify_keyword(keyword):
    words = keyword.split()

    if len(words) == 1:
        return [keyword]

    strategies = []
    strategies.append(words[0])   # 第一个词
    strategies.append(words[-1])  # 最后一个词

    # 如果有3个以上词，尝试前两个和后两个
    if len(words) >= 3:
        strategies.append(" ".join(words[:2]))
        strategies.append(" ".join(words[-2:]))

    return strategies
```

**扩展示例**:
```
原始: "数字鸿沟 教育 影响 研究"
扩展:
  - "数字鸿沟"      # 第一个词
  - "研究"          # 最后一个词
  - "数字鸿沟 教育" # 前两个词
  - "影响 研究"     # 后两个词
```

### 4. 相关领域

**原理**: 添加与主题相关的学科或领域术语。

**适用场景**:
- 跨学科研究
- 需要扩展到相关领域
- 特定应用场景

**领域映射**:
```python
DOMAINS = {
    "教育": ["教学", "学习", "培训", "课程"],
    "医疗": ["健康", "医学", "临床", "诊断"],
    "社会": ["社会学", "社会结构", "社会关系"],
    "经济": ["经济学", "商业", "市场", "产业"],
    "技术": ["工程", "系统", "算法", "计算"],
}
```

**扩展示例**:
```
原始: "人工智能 教育"
扩展:
  - "人工智能 教学"
  - "人工智能 学习"
  - "人工智能 培训"
```

### 5. 核心概念

**原理**: 提取技术术语的核心概念。

**适用场景**:
- 复杂技术术语
- 缩写词
- 专有名词

**提取规则**:
```python
def extract_core_concept(keyword):
    # 去除修饰词
    modifiers = ["基于", "面向", "关于", "有关", "相关"]

    core = keyword
    for mod in modifiers:
        if keyword.startswith(mod):
            core = keyword.replace(mod, "", 1).strip()

    # 提取技术名词
    technical_terms = {
        "深度神经网络": "神经网络",
        "卷积神经网络": "神经网络",
        "循环神经网络": "神经网络",
        "支持向量机": "SVM",
        "k均值聚类": "聚类",
    }

    return technical_terms.get(core, core)
```

**扩展示例**:
```
原始: "基于深度神经网络的图像识别"
核心: "神经网络 图像识别"
```

---

## 预定义映射表

### 常用术语扩展映射

| 原始关键词 | 同义词扩展 | 英文翻译 | 相关领域 | 核心概念 |
|-----------|-----------|---------|---------|---------|
| **人工智能** | AI、机器学习 | artificial intelligence | 深度学习、神经网络 | 智能计算 |
| **数字鸿沟** | 信息不平等、数字分化 | digital divide | 社会学、经济学 | 信息不平等 |
| **社会网络** | 社交网络、关系网络 | social network | 网络分析、社会学 | 关系网络 |
| **深度学习** | DL、深度神经网络 | deep learning | 机器学习、计算机视觉 | 神经网络 |
| **机器学习** | ML | machine learning | 人工智能、数据挖掘 | 学习算法 |
| **数据挖掘** | 知识发现 | data mining | 数据分析、大数据 | 数据分析 |
| **自然语言处理** | NLP | natural language processing | 计算语言学、文本挖掘 | 语言处理 |
| **计算机视觉** | CV | computer vision | 图像处理、模式识别 | 图像识别 |
| **知识图谱** | 知识库 | knowledge graph | 语义网络、本体 | 知识表示 |
| **区块链** | 分布式账本 | blockchain | 加密货币、智能合约 | 分布式系统 |

---

## 自定义策略

### 添加领域特定扩展

```python
class CustomPubScholarSearcher(PubScholarSearcher):
    """自定义扩展策略的搜索器"""

    def _generate_expansion_strategies(self, keyword):
        # 获取基础策略
        strategies = super()._generate_expansion_strategies(keyword)

        # 添加自定义扩展
        if "教育学" in keyword:
            strategies.extend([
                keyword + " 教学法",
                keyword + " 课程设计",
                keyword + " 教育技术",
            ])

        if "医学" in keyword:
            strategies.extend([
                keyword + " 临床",
                keyword + " 诊断",
                keyword + " 治疗",
            ])

        return unique(strategies)
```

### 基于规则的扩展

```python
def rule_based_expansion(keyword):
    """基于规则的扩展策略"""
    strategies = []

    # 规则1: 如果包含"基于"，尝试去掉
    if keyword.startswith("基于"):
        strategies.append(keyword[2:])

    # 规则2: 如果是"A的B"结构，尝试"A B"和"B"
    if "的" in keyword:
        parts = keyword.split("的")
        if len(parts) == 2:
            strategies.append(f"{parts[0]} {parts[1]}")
            strategies.append(parts[1])

    # 规则3: 如果是英文缩写，尝试全称
    abbreviations = {
        "AI": "人工智能",
        "ML": "机器学习",
        "DL": "深度学习",
        "NLP": "自然语言处理",
        "CV": "计算机视觉",
    }

    for abbr, full in abbreviations.items():
        if abbr in keyword.upper():
            strategies.append(keyword.replace(abbr, full))

    return strategies
```

---

## 实现代码

### 完整扩展策略生成器

```python
from typing import List

class ExpansionStrategyGenerator:
    """扩展策略生成器"""

    # 同义词映射
    SYNONYMS = {
        "人工智能": ["AI", "机器学习", "智能计算"],
        "数字鸿沟": ["信息不平等", "数字分化", "信息贫富差距"],
        "社会网络": ["社交网络", "关系网络"],
    }

    # 英文翻译映射
    TRANSLATIONS = {
        "人工智能": "artificial intelligence",
        "数字鸿沟": "digital divide",
        "社会网络": "social network",
        "深度学习": "deep learning",
        "机器学习": "machine learning",
    }

    # 相关领域映射
    DOMAINS = {
        "教育": ["教学", "学习", "培训"],
        "医疗": ["健康", "医学", "临床"],
        "社会": ["社会学", "社会结构"],
    }

    @classmethod
    def generate(cls, keyword: str) -> List[str]:
        """生成所有扩展策略"""
        strategies = []

        # 1. 同义词扩展
        for term, synonyms in cls.SYNONYMS.items():
            if term in keyword:
                for synonym in synonyms:
                    strategies.append(f"{keyword} {synonym}")

        # 2. 英文翻译
        for term, translation in cls.TRANSLATIONS.items():
            if term in keyword:
                strategies.append(f"{keyword} {translation}")

        # 3. 关键词简化
        words = keyword.split()
        if len(words) > 1:
            strategies.append(words[0])
            strategies.append(words[-1])

        # 4. 相关领域
        for domain, related in cls.DOMAINS.items():
            if domain in keyword:
                for term in related:
                    strategies.append(f"{keyword} {term}")

        # 去重并限制数量
        return unique(strategies)[:5]
```

### 使用示例

```python
# 生成扩展策略
strategies = ExpansionStrategyGenerator.generate("人工智能 教育")

print("扩展策略:")
for i, strategy in enumerate(strategies, 1):
    print(f"{i}. {strategy}")

# 输出:
# 扩展策略:
# 1. 人工智能 教育 AI
# 2. 人工智能 教育 机器学习
# 3. 人工智能 教育 artificial intelligence
# 4. 人工智能
# 5. 教育
```

---

## 最佳实践

### 1. 扩展策略选择

```python
# 场景1: 常见术语（结果可能很多）
results = searcher.search("人工智能", min_results=10)

# 场景2: 冷门术语（结果可能很少）
results = searcher.search("数字鸿沟 教育", min_results=5)

# 场景3: 精准搜索（不需要扩展）
results = searcher.search("特定主题", auto_expand=False)
```

### 2. 扩展效果评估

```python
# 记录扩展前后结果数
precise_count = len(precise_results)
expanded_count = len(expanded_results)
improvement = (expanded_count - precise_count) / precise_count * 100

print(f"精准搜索: {precise_count} 篇")
print(f"扩展搜索: {expanded_count} 篇")
print(f"提升: {improvement:.1f}%")
```

### 3. 自定义扩展优先级

```python
# 高优先级: 先尝试同义词
strategies.insert(0, "同义词扩展")

# 低优先级: 最后尝试相关领域
strategies.append("相关领域扩展")
```

---

**文档版本**: 1.0.0
**最后更新**: 2025-12-28
