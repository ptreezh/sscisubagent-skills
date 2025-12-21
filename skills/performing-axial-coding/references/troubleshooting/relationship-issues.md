# 关系识别问题排查

> **前置阅读**：建议先查看 `INDEX.md` 快速诊断表。

## 问题1：关系论证不充分

### 症状
- 关系的数据支持少于3个片段
- 关系的逻辑不清晰
- 关系的强度评分低（<0.5）

### 诊断
```bash
python scripts/build_relationships.py \
  --input categories.json \
  --min_strength 0.5
# 查看 weak_relations 字段
```

### 解决方案

**方案A：回到原始数据寻找证据**

重新阅读访谈记录，搜索关键词：
```
搜索："性格" + "成绩" / "学习"
搜索："内向" / "外向" + "适应"
```

**修正关系**：
```
原关系：个人性格 → 学业成绩（直接因果，证据不足）

修正后：
个人性格 → 寻求帮助行为 → 学业成绩
（间接因果，证据充分）
```

**方案B：降低关系强度声明**

如果证据确实不足，诚实报告：
```
"数据显示个人性格可能影响学业成绩（强度：0.3，弱关系），
但证据有限，需要进一步研究。"
```

**方案C：删除证据不足的关系**
```bash
python scripts/build_relationships.py \
  --min_strength 0.5 \
  --min_evidence 3
```

### 验证
- ✅ 每个关系至少3个数据片段
- ✅ 逻辑链条清晰
- ✅ 关系强度≥0.5

---

## 问题2：Paradigm模型不完整

### 症状
- Paradigm的某些组件缺失
- 逻辑链条不连贯
- 模型无法解释大部分数据

### 诊断
```bash
python scripts/construct_paradigm.py \
  --input relationships.json \
  --validate
# 查看 validation.missing_components
```

### 解决方案

**系统补充缺失组件**：

**补充中介条件**：
- 询问："为什么同样的策略，有的人有效，有的人无效？"
- 识别：个人性格、社会支持、学校资源

**补充结果**：
- 询问："采取这些行动后，发生了什么？"
- 识别：短期结果、长期结果、非预期结果

**使用工具辅助**：
```bash
python scripts/construct_paradigm.py \
  --auto_complete  # 自动补充缺失组件
```

### 验证
- ✅ 所有六个组件都存在
- ✅ 逻辑链条连贯
- ✅ 每个组件有数据支持

---

## 问题3：关系类型判断错误

### 症状
- 将条件关系误判为因果关系
- 忽略了互动关系
- 关系方向错误

### 解决方案

**重新学习关系类型**：
- 阅读 `../relationship-types/INDEX.md`
- 理解四种关系的区别

**使用判断清单**：
- 因果：A在时间上先于B？A导致B？
- 条件：在特定情境下才成立？
- 策略：有目的的行动？
- 互动：双向影响？

---

## 快速修复命令

```bash
# 问题1：关系论证不充分
python scripts/build_relationships.py --min_evidence 3

# 问题2：Paradigm不完整
python scripts/construct_paradigm.py --auto_complete --validate

# 问题3：关系类型判断
# 需要人工重新判断，参考关系类型文档
```

---

*文档大小：约500字 | 阅读时间：2分钟*
