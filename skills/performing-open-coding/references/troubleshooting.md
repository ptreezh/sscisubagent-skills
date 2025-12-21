# 开放编码故障排除指南

> **渐进式披露**：本文档提供常见问题的解决方案。理论背景见 `theory.md`，实践案例见 `examples.md`。

## 快速诊断

### 问题分类

根据症状快速定位问题类型：

| 症状 | 问题类型 | 跳转 |
|------|---------|------|
| 概念数量过多（>100个） | 过度编码 | [问题1](#问题1过度编码) |
| 概念数量过少（<10个） | 编码不足 | [问题2](#问题2编码不足) |
| 概念过于具体 | 抽象层次低 | [问题3](#问题3抽象层次不当) |
| 概念过于抽象 | 抽象层次高 | [问题3](#问题3抽象层次不当) |
| 大量重复概念 | 缺少比较 | [问题4](#问题4重复编码) |
| 概念命名混乱 | 命名不规范 | [问题5](#问题5命名不规范) |
| 工具报错 | 技术问题 | [技术问题](#技术问题) |

---

## 概念性问题

### 问题1：过度编码

#### 症状

- 概念数量超过100个
- 很多概念只出现1次
- 概念间高度相似

#### 诊断

```bash
# 使用工具检查
python scripts/auto_loader.py --input interview.txt --output concepts.json

# 查看概念数量
cat concepts.json | grep "total_concepts"
```

**判断标准**：
- 1000字文本 → 期望10-20个概念
- 如果>50个 → 过度编码

#### 解决方案

**方案1：提升抽象层次**

❌ **过度编码**：
```
- "向张老师请教问题"
- "向李老师请教问题"
- "向王老师请教问题"
```

✅ **合理编码**：
```
- "寻求教师指导"（合并为一个概念）
```

**方案2：使用聚类工具**

```bash
# 自动聚类相似概念
python scripts/cluster_concepts.py --input concepts.json --n-clusters 10
```

**方案3：使用比较工具**

```bash
# 识别重复概念
python scripts/compare_codes.py --input concepts.json --threshold 0.8
```

#### 预防措施

- 编码时即思考抽象层次
- 定期进行持续比较
- 使用"3次规则"：概念至少出现3次才独立

---

### 问题2：编码不足

#### 症状

- 概念数量过少（<10个）
- 概念过于宽泛
- 遗漏重要现象

#### 诊断

```bash
# 检查编码覆盖率
python scripts/validate_codes.py --input concepts.json
```

**判断标准**：
- 1000字文本 → 期望10-20个概念
- 如果<10个 → 编码不足

#### 解决方案

**方案1：降低抽象层次**

❌ **编码不足**：
```
- "社会互动"（过于宽泛）
```

✅ **合理编码**：
```
- "寻求教师指导"
- "建立同伴关系"
- "参与社团活动"
```

**方案2：逐行细读**

- 放慢阅读速度
- 每一句话都问："这里发生了什么？"
- 使用备忘录记录思考过程

**方案3：使用自动提取工具**

```bash
# 快速识别候选概念
python scripts/auto_loader.py --input interview.txt --top 30
```

---

### 问题3：抽象层次不当

#### 症状A：过于具体

**表现**：
- 概念包含具体人名、地点、时间
- 无法推广到其他情境

**示例**：
```
❌ "2024年3月15日向张老师请教微积分第三章问题"
✅ "寻求学科指导"
```

#### 症状B：过于抽象

**表现**：
- 概念过于哲学化
- 难以用具体例子说明

**示例**：
```
❌ "存在性焦虑"
✅ "体验学业压力"
```

#### 解决方案

**三层抽象模型**：

```
层次3（理论）：资源动员策略
    ↓
层次2（概念）：寻求教师指导 ← 目标层次
    ↓
层次1（描述）：向张老师请教微积分问题
```

**操作建议**：
- 保持在层次2（概念层）
- 可以用层次1的例子说明
- 为层次3的理论构建做准备

---

### 问题4：重复编码

#### 症状

- 多个概念语义相似
- 难以区分概念边界
- 编码系统混乱

#### 诊断

```bash
# 自动识别重复
python scripts/compare_codes.py --input concepts.json --threshold 0.7
```

**输出示例**：
```json
{
  "duplicates": [
    {
      "code1": "寻求帮助",
      "code2": "寻求支持",
      "similarity": 0.89,
      "suggestion": "建议合并"
    }
  ]
}
```

#### 解决方案

**方案1：明确概念边界**

**区分相似概念**：
- `寻求教师指导` - 学术问题
- `寻求情感支持` - 情感问题
- `寻求同伴帮助` - 来自同学

**方案2：合并高相似概念**

**合并规则**：
- 相似度>0.85 → 必须合并
- 相似度0.70-0.85 → 考虑合并
- 相似度<0.70 → 保留独立

**方案3：使用编码词典**

创建编码词典避免重复：
```json
{
  "寻求教师指导": {
    "同义词": ["向老师请教", "请教老师"],
    "定义": "主动向教师寻求学习方法的指导",
    "示例": ["..."]
  }
}
```

---

### 问题5：命名不规范

#### 症状

- 使用名词而非动词
- 命名过长或过短
- 命名不一致

#### 诊断

```bash
# 检查命名规范
python scripts/validate_codes.py --input concepts.json
```

**常见问题**：
```json
{
  "issues": {
    "naming": [
      "概念3 '老师': 建议使用行动导向的命名",
      "概念5 '学习': 名称过短",
      "概念7 '向张老师请教微积分问题': 名称过长"
    ]
  }
}
```

#### 解决方案

**命名规范检查清单**：

✅ **使用动词开头**：
```
✅ "寻求帮助"、"建立关系"、"适应环境"
❌ "帮助"、"关系"、"环境"
```

✅ **长度适中（2-8字符）**：
```
✅ "寻求教师指导"（6字符）
❌ "求"（1字符，过短）
❌ "向张老师请教微积分第三章问题"（14字符，过长）
```

✅ **命名一致性**：
```
✅ 统一使用"寻求"：寻求帮助、寻求指导、寻求支持
❌ 混用"寻求"、"请求"、"要求"
```

---

## 技术问题

### 工具1：preprocess_text.py

#### 错误：jieba加载慢

**症状**：
```
Building prefix dict from the default dictionary ...
Loading model cost 5.0 seconds.
```

**原因**：首次加载jieba词典

**解决**：
```bash
# 使用uv加速（已在pyproject.toml配置）
uv run python scripts/preprocess_text.py --input data.txt
```

#### 错误：编码问题

**症状**：
```
UnicodeDecodeError: 'gbk' codec can't decode
```

**解决**：
```python
# 确保使用UTF-8编码
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()
```

### 工具2：compare_codes.py

#### 错误：相似度计算失败

**症状**：
```
ValueError: empty vocabulary
```

**原因**：概念文本过短或全是停用词

**解决**：
```bash
# 检查概念质量
python scripts/validate_codes.py --input concepts.json

# 过滤掉过短的概念（<2字符）
```

### 工具3：cluster_concepts.py

#### 错误：聚类数量不合理

**症状**：
```
WARNING: 概念数量(5)少于聚类数(10)
```

**解决**：
```bash
# 自动确定聚类数
python scripts/cluster_concepts.py --input concepts.json
# 不指定--n-clusters，工具会自动确定

# 或手动指定合理数量
python scripts/cluster_concepts.py --input concepts.json --n-clusters 3
```

---

## 工作流问题

### 问题：不知从何开始

#### 推荐流程

```bash
# 步骤1：预处理（清洗数据）
python scripts/preprocess_text.py --input raw.txt --output clean.json

# 步骤2：快速编码（获得初步概念）
python scripts/auto_loader.py --input raw.txt --output concepts_v1.json

# 步骤3：人工精炼（提升质量）
# 手动编辑concepts_v1.json，改进命名和定义

# 步骤4：持续比较（识别重复）
python scripts/compare_codes.py --input concepts_v2.json --output comparison.json

# 步骤5：质量验证（检查规范）
python scripts/validate_codes.py --input concepts_v2.json --output validation.json

# 步骤6：概念聚类（发现模式，可选）
python scripts/cluster_concepts.py --input concepts_v2.json --output clusters.json
```

### 问题：工具输出看不懂

#### JSON输出结构

所有工具使用统一的三层结构：

```json
{
  "summary": {
    // 第1层：核心摘要（5-10秒理解）
    "total_concepts": 20,
    "top_concepts": ["学习", "帮助"]
  },
  "details": {
    // 第2层：详细数据（深入分析）
    "concepts": [...]
  },
  "metadata": {
    // 第3层：元信息（追溯和审计）
    "timestamp": "2024-03-15T10:30:00"
  }
}
```

**使用建议**：
- 快速查看：只看`summary`
- 深入分析：查看`details`
- 追溯来源：查看`metadata`

---

## 质量问题

### 问题：质量评分低

#### 诊断

```bash
python scripts/validate_codes.py --input concepts.json
```

**输出**：
```json
{
  "summary": {
    "total_score": 45.0,
    "grade": "F (不及格)"
  }
}
```

#### 改进步骤

1. **查看具体问题**：
```json
{
  "details": {
    "issues": {
      "naming": ["概念1: 建议使用行动导向"],
      "definition": ["概念2: 缺少定义"],
      "example": ["概念3: 缺少示例"]
    }
  }
}
```

2. **逐项修复**：
   - 命名问题 → 改用动词开头
   - 定义问题 → 补充清晰定义
   - 示例问题 → 添加具体示例

3. **重新验证**：
```bash
python scripts/validate_codes.py --input concepts_fixed.json
```

---

## 获取帮助

### 自助资源

- **理论基础**：`theory.md`
- **实践案例**：`examples.md`
- **中文特殊性**：`chinese-context.md`

### 工具帮助

```bash
# 查看工具使用说明
python scripts/auto_loader.py --help
python scripts/compare_codes.py --help
python scripts/cluster_concepts.py --help
python scripts/validate_codes.py --help
```

---

*本文档提供故障排除方案。理论背景见 `theory.md`，实践案例见 `examples.md`。*
