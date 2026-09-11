---
name: nlp-text-mining-expert
description: |
  NLP Text Mining expert. Provides text preprocessing, entity extraction, topic modeling, sentiment analysis, and document classification using natural language processing techniques. Suitable for text analytics, information extraction, and NLP-based research.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

---|------|------|
| 清洗 | 去除HTML、特殊字符 | 正则表达式 |
| 分词 | 中文: jieba, 英文: NLTK | jieba, spaCy |
| 去停用词 | 移除无意义词 | 停用词表 |
| 词性标注 | 标注词性 | jieba.posseg |
| 词形还原 | 还原词根 | WordNet |
| 标准化 | 大小写、繁简转换 | opencc |

### 中文分词示例

```python
import jieba
import jieba.analyse

text = "自然语言处理是人工智能的重要分支"

# 基础分词
words = jieba.lcut(text)
# ['自然语言', '处理', '是', '人工智能', '的', '重要', '分支']

# 关键词提取
keywords = jieba.analyse.extract_tags(text, topK=5)
# ['自然语言', '人工智能', '处理', '重要', '分支']
```

## 特征提取

### 词袋模型(Bag of Words)

```
文档向量 = 词频向量

示例:
文档1: "我喜欢看电影"  → [1, 1, 1, 0, 0]
文档2: "我喜欢听音乐"  → [1, 1, 0, 1, 1]

词汇表: [我, 喜欢, 看电影, 听, 音乐]
```

### TF-IDF

```
TF(t,d) = 词t在文档d中的频率
IDF(t) = log(总文档数 / 含词t的文档数)
TF-IDF = TF × IDF

作用: 降低常见词权重，提升区分性词权重
```

### 词向量(Word Embeddings)

| 模型 | 特点 | 维度 |
|------|------|------|
| Word2Vec | 上下文预测 | 100-300 |
| GloVe | 全局共现 | 100-300 |
| BERT | 上下文感知 | 768+ |
| FastText | 子词信息 | 100-300 |

## 主题建模

### LDA (Latent Dirichlet Allocation)

```
假设:
- 文档是主题的混合
- 主题是词的分布

生成过程:
主题分布θ → 主题z → 词分布φ → 词w

参数:
K: 主题数量
α: 文档-主题先验
β: 主题-词先验
```

### 主题评估

| 指标 | 含义 | 原则 |
|------|------|------|
| 困惑度 | 模型预测能力 | 越低越好 |
| 一致性 | 主题词相关度 | 越高越好 |
| 主题数 | K值选择 | 困惑度拐点 |

### Python实现

```python
from gensim import corpora, models

# 创建词典和语料
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# 训练LDA
lda = models.LdaModel(
    corpus, 
    num_topics=10, 
    id2word=dictionary,
    passes=10
)

# 查看主题
for idx, topic in lda.print_topics():
    print(f"主题{idx}: {topic}")
```

## 情感分析

### 方法对比

| 方法 | 优点 | 缺点 |
|------|------|------|
| 词典方法 | 简单、可解释 | 覆盖有限 |
| 机器学习 | 可定制 | 需标注数据 |
| 深度学习 | 效果好 | 计算量大 |
| 预训练模型 | 即用、效果好 | 黑箱 |

### 情感词典

```
中文情感词典:
- HowNet情感词典
- 大连理工情感词典
- 清华大学中文褒贬义词典
- BosonNLP情感词典

情感得分计算:
Score = Σ(sentiment_word) / 词数
```

### BERT情感分析

```python
from transformers import pipeline

# 加载预训练模型
classifier = pipeline("sentiment-analysis", 
                      model="bert-base-chinese")

# 情感预测
result = classifier("这家餐厅的菜品非常好吃！")
# [{'label': 'POSITIVE', 'score': 0.99}]
```

## 命名实体识别(NER)

### 实体类型

| 类型 | 示例 |
|------|------|
| 人名(PER) | 张三、李四 |
| 地名(LOC) | 北京、上海 |
| 机构名(ORG) | 北京大学、腾讯 |
| 时间(TIME) | 2024年3月 |
| 数值(NUM) | 100万、50% |

### spaCy实现

```python
import spacy

nlp = spacy.load("zh_core_web_sm")
doc = nlp("张三在北京大学学习")

for ent in doc.ents:
    print(f"{ent.text}: {ent.label_}")
# 张三: PERSON
# 北京大学: ORG
```

## 文本分类

### 分类流程

```
标注数据
    │
    ↓
文本预处理
    │
    ↓
特征提取(TF-IDF/BERT)
    │
    ↓
模型训练
├── 传统: NB, SVM, RF
└── 深度: CNN, LSTM, BERT
    │
    ↓
模型评估
├── 准确率
├── 精确率/召回率
└── F1分数
```

### 评估指标

```
准确率(Accuracy) = 正确预测数 / 总预测数
精确率(Precision) = TP / (TP + FP)
召回率(Recall) = TP / (TP + FN)
F1 = 2 × P × R / (P + R)
```

## 可视化方法

| 方法 | 用途 |
|------|------|
| 词云 | 词频展示 |
| 主题词分布 | 主题理解 |
| 情感趋势图 | 时间序列情感 |
| 网络图 | 词语共现 |
| 热力图 | 文档-主题分布 |

## 使用示例

```
用户: 分析这批社交媒体评论的主题和情感

AI: 我将执行完整的文本分析流程：

## 数据概况
- 评论数: 10,000条
- 时间范围: 2024年1月-3月
- 来源: 微博、小红书

## 主题建模(LDA)
主题1(32%): 产品质量
  - 质量, 差, 假货, 劣质
主题2(28%): 物流服务  
  - 快递, 慢, 丢件, 态度
主题3(22%): 价格优惠
  - 便宜, 优惠, 活动, 性价比
主题4(18%): 客服体验
  - 客服, 回复, 解决, 推诿

## 情感分析
- 正面评论: 35%
- 负面评论: 45%
- 中性评论: 20%

## 洞察提取
1. 物流服务是主要痛点(负面占比62%)
2. 价格促销带来正面情感
3. 客服体验需要改善
```

## 🚫 绝对禁止原则

> **使用前必读**：以下原则是不可逾越的红线，违反将导致NLP文本挖掘结论无效。

1. **禁止不处理类别不平衡** — 正面:负面=1:9时直接训练模型，导致少数类召回率接近零
2. **禁止脱离语境的词汇统计** — 仅统计词频而不考虑上下文语义，导致误解词语真实含义
3. **禁止混淆准确率与有效性** — 高准确率可能来自类别不平衡，而非模型真正有效
4. **禁止忽视文本预处理质量** — 分词错误、停用词表不匹配领域，直接影响后续分析可靠性
5. **禁止不检验模型泛化能力** — 用训练集评估模型后直接应用，忽视过拟合和数据漂移风险
6. **禁止脱离标注质量的模型评估** — 标注数据本身有偏（如标注者间信度低），则模型评估结果不可信

## ✅ 质量标准

### 完整性
- 必做项清单完成度 ≥ 90%
- 文本预处理步骤记录完整
- 类别分布说明清晰

### 方法论
- 理论框架与数据一致性 ≥ 90%
- 分析步骤可复现性高（含预处理参数）
- 模型选择有据可查

### 深度
- 核心维度覆盖 ≥ 80%
- 类别不平衡处理方案说明
- 模型可解释性分析

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | text_preprocessor.py | 文本预处理，支持分词、去停用词、词形还原、繁简转换（跨平台） |
| 2 | topic_modeler.py | 主题建模，支持LDA、BERTopic、 coherence score计算 |
| 3 | sentiment_analyzer.py | 情感分析，支持词典方法、机器学习、深度学习多方法对比 |
| 4 | ner_extractor.py | 命名实体识别，支持多语言NER、实体类型自定义 |

### CLI用法

```bash
python tools/text_preprocessor.py --input raw_text.txt --output cleaned.txt --lang zh
python tools/topic_modeler.py --input corpus.txt --method lda --num-topics 10 --output topics.json
python tools/sentiment_analyzer.py --input reviews.csv --method bert --output sentiment.json
```

### CLI用法

```bash
# NLP文本挖掘推荐使用jieba、gensim、transformers等库
python -c "import jieba; print(list(jieba.cut('自然语言处理')))"
```

## 参考文献

1. Jurafsky, D., & Martin, J.H. (2024). *Speech and Language Processing*. 3rd ed.
2. Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python*.
3. Blei, D.M. (2012). Probabilistic topic models. *CACM*, 55, 77-84.
4. Devlin, J., et al. (2019). BERT: Pre-training of deep bidirectional transformers.

---

**技能版本**: 5.0.0  
**方法论标准**: Jurafsky & Martin (2024)  
**创建时间**: 2026-03-15