# 技术问题排查

> **前置阅读**：建议先查看 `INDEX.md` 快速诊断表。

## 问题1：工具运行报错

### 常见错误1：FileNotFoundError
```
FileNotFoundError: [Errno 2] No such file or directory: 'codes.json'
```

**解决**：检查输入文件路径
```bash
# 确保文件存在
ls codes.json

# 使用绝对路径
python scripts/identify_categories.py --input /path/to/codes.json
```

---

### 常见错误2：KeyError
```
KeyError: 'concept'
```

**解决**：检查输入JSON格式
```json
{
  "details": {
    "concepts": [
      {"concept": "...", "frequency": 10, "definition": "..."}
    ]
  }
}
```

---

### 常见错误3：ModuleNotFoundError
```
ModuleNotFoundError: No module named 'jieba'
```

**解决**：安装依赖
```bash
uv pip install jieba pandas scikit-learn networkx
```

---

### 常见错误4：工具运行很慢

**原因**：
- 概念数量过多（>100个）
- 聚类方法过慢（hierarchical）

**解决**：
```bash
# 减少概念数量
python scripts/preprocess.py --max_concepts 50

# 使用更快的聚类方法
python scripts/identify_categories.py --method kmeans

# 减少聚类数量
python scripts/identify_categories.py --n_categories 5
```

---

## 问题2：输出格式问题

### 症状
输出的JSON文件无法被下一个工具读取

### 解决
```bash
# 验证输出格式
python scripts/validate_output.py --input categories.json

# 转换格式
python scripts/convert_format.py \
  --input old_format.json \
  --output new_format.json
```

---

## 问题3：工具输出不合理

### 症状
- 工具将明显不相关的概念聚类到一起
- 工具识别的关系不符合逻辑

### 解决方案

**方案A：调整工具参数**

**增加聚类数量**：
```bash
python scripts/identify_categories.py --n_categories 8
```

**更换聚类方法**：
```bash
python scripts/identify_categories.py --method hierarchical
```

**调整最小概念数**：
```bash
python scripts/identify_categories.py --min_codes 2
```

**方案B：清理输入数据**

在运行工具前：
1. 检查概念命名是否规范
2. 合并明显重复的概念
3. 删除质量差的概念

```bash
python scripts/validate_codes.py --input codes.json
```

**方案C：结合人工判断**

工具只是辅助，最终判断需要研究者：
1. 使用工具生成初步聚类
2. 人工检查和调整
3. 重新定义范畴边界

---

## 快速修复命令

```bash
# 错误1：文件不存在
ls codes.json

# 错误2：格式错误
python scripts/validate_output.py --input codes.json

# 错误3：缺少依赖
uv pip install -r requirements.txt

# 错误4：运行慢
python scripts/identify_categories.py --method kmeans --n_categories 5

# 问题2：输出格式
python scripts/validate_output.py --input categories.json

# 问题3：输出不合理
python scripts/identify_categories.py --n_categories 8 --method hierarchical
```

---

## 预防措施

### 1. 环境检查
```bash
# 检查Python版本
python --version  # 需要 >=3.8

# 检查依赖
uv pip list | grep jieba
```

### 2. 输入验证
```bash
# 验证输入格式
python scripts/validate_input.py --input codes.json
```

### 3. 定期备份
```bash
cp categories.json categories_backup_$(date +%Y%m%d).json
```

---

*文档大小：约500字 | 阅读时间：2分钟*
