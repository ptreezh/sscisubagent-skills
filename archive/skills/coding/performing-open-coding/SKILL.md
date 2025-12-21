---
name: performing-open-coding
description: 当用户需要执行扎根理论的开放编码，包括中文质性数据的概念识别、初始编码、持续比较和备忘录撰写时使用此技能。
---

# 开放编码技能 (Performing Open Coding)

专门用于扎根理论研究的开放编码阶段，对中文质性数据进行系统性的概念识别和初始编码工作。

## 使用时机

当用户提到以下需求时，使用此技能：
- "开放编码" 或 "执行开放编码"
- "扎根理论编码" 或 "质性数据编码"
- "概念识别" 或 "概念提取"
- "初始编码" 或 "逐行编码"
- "持续比较" 或 "编码比较"
- "备忘录撰写" 或 "编码备忘录"
- 需要分析中文访谈、观察记录或文档资料

## 快速开始

### 工具链（5个脚本）

```bash
# 1. 文本预处理
python scripts/preprocess_text.py --input interview.txt --output clean.json

# 2. 快速概念提取
python scripts/auto_loader.py --input interview.txt --output concepts.json

# 3. 持续比较
python scripts/compare_codes.py --input concepts.json --output comparison.json

# 4. 概念聚类（可选）
python scripts/cluster_concepts.py --input concepts.json --output clusters.json

# 5. 编码验证
python scripts/validate_codes.py --input concepts.json --output validation.json
```

## 核心流程

### 第一步：数据预处理

使用预处理工具清洗文本：
```bash
python scripts/preprocess_text.py --input raw.txt --output clean.json
```

**关键要点**：
- 中文分词（jieba）
- 停用词过滤
- 语义分段

详见：`references/theory.md` - 预处理原理

### 第二步：概念识别

使用自动提取工具获得初步概念：
```bash
python scripts/auto_loader.py --input raw.txt --output concepts_v1.json
```

**编码原则**：
- ✅ 使用动词开头（"寻求帮助"）
- ✅ 保持适度抽象（既不过具体也不过抽象）
- ✅ 提供清晰定义和示例

详见：`references/examples.md` - 完整编码案例

**人工精炼**：
- 改进概念命名
- 补充清晰定义
- 添加具体示例

### 第三步：持续比较

使用比较工具识别重复和关系：
```bash
python scripts/compare_codes.py --input concepts.json --output comparison.json
```

**比较维度**：
- 相似度>0.8 → 考虑合并
- 相似度0.5-0.8 → 建立关联
- 相似度<0.5 → 独立概念

详见：`references/theory.md` - 持续比较方法

### 第四步：编码优化

**使用聚类发现模式**（可选）：
```bash
python scripts/cluster_concepts.py --input concepts.json --output clusters.json
```

**使用验证工具检查质量**：
```bash
python scripts/validate_codes.py --input concepts.json --output validation.json
```

**质量标准**：
- 命名规范：动词开头，长度适中
- 定义完整：清晰说明概念内涵
- 示例充分：至少2个具体例子

详见：`references/troubleshooting.md` - 常见问题解决

### 第五步：备忘录撰写

记录编码过程的关键思考：
- 概念识别的理由
- 概念间的关系发现
- 方法反思和改进

详见：`writing-grounded-theory-memos` 技能

## 输出格式

所有工具使用统一的三层JSON格式：

```json
{
  "summary": {
    "total_concepts": 20,
    "top_concepts": ["学习", "帮助", "关系"],
    "processing_time": 2.5
  },
  "details": {
    "concepts": [...],
    "statistics": {...}
  },
  "metadata": {
    "timestamp": "2025-12-18T10:30:00",
    "version": "1.0.0"
  }
}
```

详见：`references/examples.md` - 完整输出示例

## 质量检查清单

在完成开放编码后，请检查以下项目：

- [ ] 所有概念命名都使用行动导向的动词开头
- [ ] 每个概念都有清晰的定义和说明
- [ ] 提供了具体且代表性的示例
- [ ] 进行了充分的持续比较分析
- [ ] 撰写了完整的分析备忘录
- [ ] 准确理解了中文语境的特殊含义
- [ ] 保持了编码的一致性和连贯性
- [ ] 概念的抽象层次适当，不过于具体也不过于抽象

## 常见问题

**快速诊断**：
- 概念过多/过少 → 见 `references/troubleshooting.md` - 问题1、2
- 抽象层次不当 → 见 `references/troubleshooting.md` - 问题3
- 重复编码 → 使用 `compare_codes.py` 自动识别
- 命名不规范 → 使用 `validate_codes.py` 检查

**中文特殊性**：
- 关系导向、面子文化、集体主义
- 详见：`references/chinese-context.md`

## 深入学习

- **理论基础**：`references/theory.md` - 扎根理论流派、核心原则
- **实践案例**：`references/examples.md` - 完整编码过程
- **故障排除**：`references/troubleshooting.md` - 问题诊断和解决
- **中文语境**：`references/chinese-context.md` - 文化和语言特点

## 完成标志

完成开放编码后，应该产出：
1. 完整的概念编码清单
2. 详细的备忘录记录
3. 概念间关系分析
4. 质量评估报告

---

*此技能专为中文质性研究设计，提供从数据预处理到概念提取的完整开放编码支持。*