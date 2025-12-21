# 选择式编码工具集

## 工具概览

| 工具 | 功能 | 输入 | 输出 |
|-----|------|------|------|
| identify_core_category.py | 核心范畴识别 | categories.json, relations.json | core_category.json |
| construct_storyline.py | 故事线构建 | data.json, categories.json, relations.json | storyline.json |
| integrate_theory.py | 理论框架整合 | categories.json, relations.json | theory.json |
| check_saturation.py | 饱和度检验 | existing.json, new.json | saturation.json |

---

## 完整工作流

```bash
# 第一步：识别核心范畴
python scripts/identify_core_category.py \
  --input categories.json \
  --relations relationships.json \
  --output core_category.json

# 第二步：构建故事线
python scripts/construct_storyline.py \
  --input data.json \
  --categories categories.json \
  --relations relationships.json \
  --output storyline.json

# 第三步：整合理论框架
python scripts/integrate_theory.py \
  --categories categories.json \
  --relations relationships.json \
  --output theory.json

# 第四步：检验饱和度
python scripts/check_saturation.py \
  --existing theory.json \
  --new new_data.json \
  --output saturation.json
```

---

## 标准化接口

所有工具遵循统一的接口规范：

### 命令行参数
- `--input, -i`：输入文件
- `--output, -o`：输出文件
- `--help, -h`：帮助信息

### 输出格式（三层JSON）
```json
{
  "summary": {
    "key_metric": "value",
    "processing_time": 2.5
  },
  "details": {
    "detailed_results": "..."
  },
  "metadata": {
    "timestamp": "2025-12-19T...",
    "version": "1.0.0"
  }
}
```

---

## 依赖安装

```bash
uv pip install -r ../requirements.txt
# 或
uv pip install pandas networkx scikit-learn numpy
```

---

## 故障排除

**问题1**：ModuleNotFoundError
```bash
uv pip install pandas networkx
```

**问题2**：FileNotFoundError
- 检查输入文件路径是否正确
- 确保文件格式为JSON

**问题3**：输出不合理
- 检查输入数据质量
- 调整工具参数
- 参考 `../references/troubleshooting/`

---

*更多信息见 `../references/README.md`*
