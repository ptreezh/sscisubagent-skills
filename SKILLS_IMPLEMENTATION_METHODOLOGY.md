# 技能实现核心方法论

**版本**: 1.0.0  
**创建日期**: 2025-12-18  
**基于**: sscisubagent-skills技能包深度分析

---

## 核心认知

### 技能的本质

**技能 = 提示词(定性) + 脚本(定量) + 上下文(参考)**

```
技能是对AI能力的扩展，是提示词、上下文和脚本程序的混合体：
- 确定性逻辑 → 代码化/脚本化
- 综合智能分析 → 提示词指导
- 详细背景知识 → 参考文档（按需加载）
```

### 设计哲学

**渐进式披露原则**：
- 优化AI上下文负载
- 只在必要时加载必要文件
- 针对应用场景分层组织

---

## 十大核心原则

### 1. 定性定量严格分离

**定性部分（SKILL.md提示词）**：
- ✅ 概念命名原则（如"寻求支持"而非"support_seeking"）
- ✅ 理论解释（如Paradigm模型的逻辑）
- ✅ 质量标准（如饱和度判断标准）
- ✅ 中文语境适配（如"关系资本"的文化含义）
- ✅ 流程指导（如"先识别范畴，再分析属性"）

**定量部分（scripts/脚本）**：
- ✅ 文本预处理（jieba分词、去停用词）
- ✅ 聚类算法（K-means、层次聚类）
- ✅ 网络计算（中心性、社区发现）
- ✅ 统计检验（t检验、卡方检验、因子分析）
- ✅ 可视化生成（网络图、直方图、热力图）

**反模式警示**：
- ❌ 在SKILL.md中写算法伪代码（应该用脚本）
- ❌ 在脚本中硬编码概念命名规则（应该用提示词）

---

### 2. 三层信息披露

**第1层：SKILL.md核心提示词（5-10秒理解）**
```markdown
---
name: performing-axial-coding
description: 执行扎根理论的轴心编码，识别范畴、分析属性、建立关系。当需要将开放编码结果整合为范畴体系时使用。
---

## 使用时机
- "轴心编码"
- "范畴构建"
- "概念归类"

## 快速工具
```bash
python scripts/identify_categories.py --input codes.json --output categories.json
```
```

**第2层：JSON输出摘要（30秒阅读）**
```json
{
  "summary": {
    "total_categories": 8,
    "key_categories": ["学习支持", "情感调节", "目标设定"],
    "relationship_count": 12,
    "paradigm_identified": true
  }
}
```

**第3层：references/详细文档（按需深入）**
```markdown
# references/theory.md
## 轴心编码的理论基础
Strauss & Corbin (1998) 提出的轴心编码...
（详细理论背景，5000字）
```

---

### 3. 标准化脚本接口

**命令行接口规范**：
```python
#!/usr/bin/env python3
"""
功能描述：范畴识别脚本

使用方式：
  python identify_categories.py --input codes.json --output categories.json
  
依赖：
  - pandas>=2.0.0
  - scikit-learn>=1.3.0
"""
import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='识别范畴')
    parser.add_argument('--input', '-i', required=True, help='输入的编码JSON文件')
    parser.add_argument('--output', '-o', default='categories.json', help='输出文件')
    parser.add_argument('--min-codes', type=int, default=3, help='每个范畴最少编码数')
    args = parser.parse_args()
    
    # 处理逻辑
    result = process_categories(args.input, args.min_codes)
    
    # 标准化输出
    output = {
        'summary': {
            'total_categories': len(result['categories']),
            'processing_time': result['time']
        },
        'details': {
            'categories': result['categories'],
            'statistics': result['stats']
        },
        'metadata': {
            'input_file': args.input,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 识别完成：{len(result['categories'])}个范畴")
    print(f"📄 详细结果：{args.output}")

if __name__ == '__main__':
    main()
```

**输出格式标准**：
```json
{
  "summary": {
    "total_items": 100,
    "success_rate": 0.95,
    "processing_time": 2.5
  },
  "details": {
    "items": [...],
    "statistics": {...}
  },
  "metadata": {
    "input_file": "data.txt",
    "timestamp": "2025-12-18T10:30:00",
    "version": "1.0.0"
  }
}
```

---

### 4. 中文文本处理优化

**jieba + uv集成（pyproject.toml）**：
```toml
[project]
name = "performing-axial-coding"
version = "1.0.0"
requires-python = ">=3.8"
dependencies = [
    "jieba>=0.42.1",
    "pandas>=2.0.0",
    "scikit-learn>=1.3.0",
]

[tool.uv]
# 使用国内镜像加速
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple/"
default = true

# 缓存jieba词典
[tool.uv.cache]
keys = ["jieba"]
```

**中文分词优化**：
```python
import jieba
import jieba.posseg as pseg

# 预加载学术词典
jieba.load_userdict("academic_terms.txt")

# 停用词过滤
stopwords = set(line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8'))

def tokenize_chinese(text):
    """中文分词（优化版）"""
    words = pseg.cut(text)
    return [w.word for w in words 
            if w.word not in stopwords 
            and len(w.word) > 1
            and w.flag in ['n', 'v', 'a']]  # 只保留名词、动词、形容词
```

---

### 5. SKILL.md写作模式

**标准模板**：
```markdown
---
name: skill-name
description: 一句话描述何时使用此技能（第三人称，1-2句话）
---

# 技能中文名称 (English Name)

一段话总结技能的核心功能和价值。

## 使用时机

当用户提到以下需求时，使用此技能：
- "关键词1" 或 "同义词1"
- "关键词2" 或 "同义词2"
- "关键词3" 或 "同义词3"
- 需要执行XXX任务

## 快速工具

```bash
# 核心脚本调用（一行命令）
python scripts/main_script.py --input data.txt --output result.json
```

## 执行步骤

### 第一步：任务准备
1. **子步骤1**
   - 具体操作说明
   - 注意事项

2. **子步骤2**
   - 具体操作说明

### 第二步：核心处理
使用脚本执行确定性计算：
```bash
python scripts/calculator.py --input prepared.json
```

### 第三步：结果分析
1. **分析输出**
   - 解释关键指标
   - 识别重要模式

2. **质量检查**
   - 验证结果合理性
   - 检查异常值

### 第四步：输出交付
生成标准化报告。

## 输出要求

### 基本输出
- 核心结果（3-5项）
- 关键指标（量化数据）

### 高级分析
- 深入解释
- 理论意义

## 质量检查清单

在完成任务后，请检查以下项目：

### 数据质量
- [ ] 输入数据完整
- [ ] 数据格式正确
- [ ] 异常值处理

### 结果质量
- [ ] 结果符合预期
- [ ] 指标计算正确
- [ ] 解释合理

### 中文语境
- [ ] 术语使用准确
- [ ] 文化适配恰当

## 常见问题处理

**问题1：XXX**
- 解决：YYY
- 方法：ZZZ

**问题2：XXX**
- 解决：YYY

## 技术说明

详细的技术背景和理论，参见：
- `references/theory.md` - 理论背景
- `references/examples.md` - 完整案例
- `scripts/README.md` - 脚本使用指南

## 完成标志

完成高质量的XXX应该产出：
1. 标准化的JSON输出
2. 详细的分析报告
3. 可视化图表（如适用）

---

*此技能为XXX研究提供完整支持。*
```

---

### 6. JavaScript技能的SOLID架构

**适用场景**：理论分析类技能（ANT、场域分析）

**目录结构**：
```
skill-name/
├── index.js              # 主入口（依赖注入）
├── src/
│   ├── Analyzer.js       # 核心分析器（单一职责）
│   ├── Extractor.js      # 数据提取器（单一职责）
│   ├── Validator.js      # 验证器（单一职责）
│   └── interfaces/
│       ├── IAnalyzer.js  # 分析器接口
│       └── IExtractor.js # 提取器接口
├── __tests__/
│   ├── Analyzer.test.js
│   └── integration.test.js
└── SKILL.md
```

**依赖注入示例**：
```javascript
// index.js
class ParticipantSkill {
    constructor(extractor, analyzer, validator) {
        this.extractor = extractor;
        this.analyzer = analyzer;
        this.validator = validator;
    }
    
    async execute(inputData) {
        // 1. 验证输入
        const validationResult = this.validator.validate(inputData);
        if (!validationResult.isValid) {
            throw new Error(validationResult.errors.join(', '));
        }
        
        // 2. 提取数据
        const extracted = await this.extractor.extract(inputData);
        
        // 3. 分析处理
        const analyzed = await this.analyzer.analyze(extracted);
        
        // 4. 分层输出
        return {
            overview: this._buildOverview(analyzed),
            summary: this._buildSummary(analyzed),
            details: analyzed
        };
    }
    
    _buildOverview(data) {
        return {
            title: "参与者分析概览",
            keyFindings: data.topParticipants.slice(0, 3),
            description: `识别了${data.totalParticipants}个参与者`
        };
    }
}

// 使用
const skill = new ParticipantSkill(
    new TextExtractor(),
    new ParticipantAnalyzer(),
    new InputValidator()
);

const result = await skill.execute(inputText);
```

---

### 7. 分层输出设计

**三层输出结构**：
```javascript
{
  // 第1层：核心概念（5-10秒理解）
  "overview": {
    "title": "轴心编码分析结果",
    "keyFindings": [
      "识别了8个主要范畴",
      "建立了12条范畴关系",
      "核心范畴为'学习支持'"
    ],
    "description": "完成了从25个开放编码到8个范畴的整合"
  },
  
  // 第2层：关键发现（30秒阅读）
  "summary": {
    "metrics": {
      "totalCategories": 8,
      "totalRelationships": 12,
      "averageCodesPerCategory": 3.1
    },
    "topCategories": [
      {"name": "学习支持", "importance": 0.35},
      {"name": "情感调节", "importance": 0.28},
      {"name": "目标设定", "importance": 0.22}
    ],
    "visualizations": [
      "category_network.png",
      "paradigm_model.png"
    ]
  },
  
  // 第3层：详细数据（深入分析）
  "details": {
    "categories": [...],  // 完整范畴列表
    "relationships": [...],  // 完整关系列表
    "paradigm": {...},  // Paradigm模型
    "rawData": {...}  // 原始数据
  },
  
  // 元数据
  "metadata": {
    "skillName": "performing-axial-coding",
    "version": "1.0.0",
    "timestamp": "2025-12-18T10:30:00",
    "processingTime": 2.5,
    "inputFile": "codes.json"
  }
}
```

---

### 8. 质量保证机制

**测试驱动开发（TDD）**：
```python
# tests/test_category_identifier.py
import pytest
from scripts.identify_categories import CategoryIdentifier

def test_identify_categories_from_codes():
    """测试从编码中识别范畴"""
    # Arrange
    codes = [
        {"code": "寻求帮助", "frequency": 10},
        {"code": "获得支持", "frequency": 8},
        {"code": "建立关系", "frequency": 5}
    ]
    identifier = CategoryIdentifier(min_codes=2)
    
    # Act
    categories = identifier.identify(codes)
    
    # Assert
    assert len(categories) >= 1
    assert categories[0]['name'] in ['学习支持', '社交支持']
    assert all(len(c['codes']) >= 2 for c in categories)

def test_handle_insufficient_codes():
    """测试处理编码不足的情况"""
    codes = [{"code": "单个编码", "frequency": 1}]
    identifier = CategoryIdentifier(min_codes=3)
    
    with pytest.raises(ValueError, match="至少需要3个编码"):
        identifier.identify(codes)
```

**质量检查清单**：
```markdown
## SKILL.md质量标准
- [ ] YAML frontmatter完整（name + description）
- [ ] description是第三人称，1-2句话
- [ ] 触发条件清晰（至少6个关键词）
- [ ] 执行步骤可操作（4步法）
- [ ] 有质量检查清单
- [ ] 有常见问题处理
- [ ] 引用了scripts/和references/
- [ ] 中文语境适配良好
- [ ] 文档长度≤5000字

## 脚本质量标准
- [ ] 标准命令行接口（argparse）
- [ ] JSON标准化输出（summary + details + metadata）
- [ ] 错误处理完善（try-except + 友好提示）
- [ ] 性能指标记录（processing_time）
- [ ] 有单元测试（覆盖率≥80%）
- [ ] 有使用文档（docstring + README）
- [ ] 依赖管理清晰（pyproject.toml或package.json）
```

---

### 9. 技能开发完整流程

**阶段1：需求分析（1天）**
1. 识别技能的核心功能
2. 确定触发条件（关键词）
3. 分析定性vs定量部分
4. 设计输入输出格式

**阶段2：架构设计（1天）**
1. 选择实现语言（Python/JavaScript）
2. 设计分层结构（SKILL.md + scripts/ + references/）
3. 规划脚本接口（命令行参数、输出格式）
4. 确定依赖库（jieba、NetworkX、scikit-learn等）

**阶段3：实现开发（3-5天）**
1. 编写SKILL.md（第1层提示词）
   - YAML frontmatter
   - 使用时机
   - 快速工具
   - 执行步骤
   - 质量检查清单

2. 实现scripts/（第3层脚本）
   - 核心计算脚本
   - 可视化脚本
   - 验证脚本

3. 创建references/（第2层上下文）
   - 理论背景（theory.md）
   - 完整案例（examples.md）
   - 故障排除（troubleshooting.md）

**阶段4：测试验证（2天）**
1. 单元测试（__tests__/或tests/unit/）
2. 集成测试（tests/integration/）
3. 端到端测试（真实数据）
4. 性能测试（大规模数据）

**阶段5：文档完善（1天）**
1. 补充使用示例
2. 添加故障排除指南
3. 更新SKILLS_MANIFEST.md
4. 编写README.md（如独立技能）

**阶段6：质量审计（1天）**
1. 运行validate_skills.py
2. 检查质量检查清单
3. 代码审查
4. 文档审查

---

### 10. 中文本土化适配

**术语本土化**：
```python
# 中文社科术语映射
CHINESE_TERMS = {
    'guanxi_capital': '关系资本',
    'danwei_system': '单位制度',
    'political_capital': '政治资本',
    'face_concept': '面子观念',
    'hierarchy_acceptance': '等级接受度'
}

# 场域分析的中国特色
class ChineseFieldAdapter:
    def adapt_field_features(self, field_data):
        """识别中国特色的场域特征"""
        features = {
            'danwei_influence': self._calculate_danwei_influence(field_data),
            'guanxi_importance': self._calculate_guanxi_importance(field_data),
            'political_capital_role': self._calculate_political_capital(field_data)
        }
        return features
```

**文化敏感性处理**：
```markdown
## 中文语境适配

### 关系资本（Guanxi Capital）
在中国社会中，"关系"不仅是社会资本，更是一种独特的文化现象：
- 差序格局：关系的亲疏远近
- 人情往来：互惠性原则
- 面子维护：社会声誉管理

### 单位制度（Danwei System）
虽然单位制度已经弱化，但仍然影响着：
- 资源分配方式
- 社会身份认同
- 职业发展路径
```

---

## 实践指南

### 指南1：何时使用Python vs JavaScript

**使用Python的场景**：
- ✅ 中文文本处理（jieba分词）
- ✅ 数据分析（pandas、numpy）
- ✅ 机器学习（scikit-learn）
- ✅ 统计分析（scipy.stats）
- ✅ 网络分析（NetworkX）

**使用JavaScript的场景**：
- ✅ 理论分析（ANT、场域分析）
- ✅ 需要SOLID架构
- ✅ 复杂的依赖注入
- ✅ 前端可视化（D3.js）

---

### 指南2：脚本开发最佳实践

**使用uv包管理（推荐）**：
```toml
# pyproject.toml
[project]
name = "skill-name"
version = "1.0.0"
requires-python = ">=3.8"
dependencies = [
    "jieba>=0.42.1",
    "pandas>=2.0.0",
]

[tool.uv]
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple/"
default = true
```

**标准化错误处理**：
```python
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    try:
        # 处理逻辑
        result = process_data(args.input)
        
    except FileNotFoundError as e:
        logging.error(f"文件未找到: {e}")
        sys.exit(1)
        
    except ValueError as e:
        logging.error(f"数据格式错误: {e}")
        sys.exit(2)
        
    except Exception as e:
        logging.error(f"未知错误: {e}")
        sys.exit(99)
    
    logging.info(f"✅ 处理完成")
```

---

### 指南3：SKILL.md优化技巧

**保持简洁（≤5000字）**：
```markdown
## 执行步骤

### 第一步：数据准备
使用脚本预处理数据：
```bash
python scripts/preprocess.py --input raw.txt --output clean.json
```

详细的预处理说明，参见 `references/preprocessing-guide.md`
```

**避免过度详细**：
```markdown
❌ 不好的写法（过于详细）：
## 中心性分析原理
度中心性的计算公式为：C_D(v) = deg(v) / (n-1)
其中deg(v)是节点v的度数，n是网络节点总数...
（继续500字的数学推导）

✅ 好的写法（简洁+引用）：
## 中心性分析
使用脚本计算四种中心性指标：
```bash
python scripts/centrality.py --input network.json
```

详细的理论背景和公式推导，参见 `references/centrality-theory.md`
```

---

### 指南4：测试策略

**单元测试（80%覆盖率）**：
```python
# tests/test_extractor.py
def test_extract_concepts():
    extractor = ConceptExtractor()
    text = "学生寻求老师的帮助"
    concepts = extractor.extract(text)
    assert "寻求帮助" in concepts

def test_handle_empty_text():
    extractor = ConceptExtractor()
    with pytest.raises(ValueError):
        extractor.extract("")
```

**集成测试**：
```python
# tests/integration/test_workflow.py
def test_complete_workflow():
    # 1. 预处理
    preprocess_result = subprocess.run(
        ['python', 'scripts/preprocess.py', '--input', 'test_data/raw.txt'],
        capture_output=True
    )
    assert preprocess_result.returncode == 0
    
    # 2. 概念提取
    extract_result = subprocess.run(
        ['python', 'scripts/extract.py', '--input', 'clean.json'],
        capture_output=True
    )
    assert extract_result.returncode == 0
    
    # 3. 验证输出
    with open('concepts.json') as f:
        data = json.load(f)
    assert 'summary' in data
    assert 'details' in data
```

---

## 反模式警示

### 反模式1：SKILL.md过于详细
```markdown
❌ 错误示例：
## 聚类算法详解
K-means算法的步骤如下：
1. 随机选择k个初始中心点
2. 计算每个数据点到中心点的距离
3. 将数据点分配到最近的中心点
4. 重新计算每个簇的中心点
5. 重复步骤2-4直到收敛
（继续1000字的算法详解和代码示例）

✅ 正确示例：
## 范畴识别
使用聚类算法自动识别范畴：
```bash
python scripts/identify_categories.py --input codes.json
```

算法细节参见 `references/clustering-algorithm.md`
```

---

### 反模式2：缺少脚本支持
```markdown
❌ 错误示例：
## 中心性计算
请手动计算每个节点的度中心性：
1. 统计每个节点的连接数
2. 除以(n-1)得到标准化度中心性
3. 重复以上步骤计算其他中心性...

✅ 正确示例：
## 中心性计算
```bash
python scripts/centrality.py --input network.json --output centrality.json
```
脚本自动计算四种中心性指标。
```

---

### 反模式3：输出格式不一致
```markdown
❌ 错误示例：
# 脚本A输出
{"result": [...]}

# 脚本B输出
{"data": {...}, "status": "ok"}

# 脚本C输出
[1, 2, 3, 4, 5]

✅ 正确示例：
# 所有脚本统一输出格式
{
  "summary": {...},
  "details": {...},
  "metadata": {...}
}
```

---

### 反模式4：忽视中文语境
```markdown
❌ 错误示例：
识别了以下capital types:
- cultural_capital
- social_capital
- economic_capital

✅ 正确示例：
识别了以下资本类型：
- 文化资本（学历、知识、品味）
- 社会资本（关系网络、社会地位）
- 经济资本（财富、收入）
- 政治资本（权力、职位）[中国扩展]
- 关系资本（人脉、面子）[中国扩展]
```

---

### 反模式5：技能重复
```markdown
❌ 错误示例：
skills/
├── centrality-analysis/SKILL.md  # 简化版
└── performing-centrality-analysis/SKILL.md  # 详细版

✅ 正确示例：
skills/
└── performing-centrality-analysis/
    ├── SKILL.md  # 统一的详细版
    ├── scripts/
    └── references/
```

---

### 反模式6：过度设计（违反YAGNI）
```python
❌ 错误示例：
class CategoryIdentifier:
    def __init__(self, strategy_factory, config_manager, logger_factory, 
                 cache_manager, event_bus, metrics_collector):
        # 过度设计，引入了不必要的复杂性
        pass

✅ 正确示例：
class CategoryIdentifier:
    def __init__(self, min_codes=3):
        self.min_codes = min_codes
    
    def identify(self, codes):
        # 简单直接，满足需求即可
        pass
```

---

### 反模式7：缺少测试
```markdown
❌ 错误示例：
skill-name/
├── SKILL.md
└── scripts/
    └── calculator.py  # 没有测试

✅ 正确示例：
skill-name/
├── SKILL.md
├── scripts/
│   └── calculator.py
└── __tests__/
    └── calculator.test.py  # 有测试
```

---

### 反模式8：硬编码配置
```python
❌ 错误示例：
def identify_categories(codes):
    # 硬编码的阈值
    if len(codes) < 3:
        raise ValueError("至少需要3个编码")
    
    # 硬编码的聚类参数
    kmeans = KMeans(n_clusters=5, random_state=42)

✅ 正确示例：
def identify_categories(codes, min_codes=3, n_clusters=None):
    if len(codes) < min_codes:
        raise ValueError(f"至少需要{min_codes}个编码")
    
    # 自动确定聚类数
    if n_clusters is None:
        n_clusters = estimate_optimal_clusters(codes)
    
    kmeans = KMeans(n_clusters=n_clusters)
```

---

## 质量检查总清单

### SKILL.md质量
- [ ] YAML frontmatter完整（name + description）
- [ ] description第三人称，1-2句话
- [ ] 触发条件清晰（≥6个关键词）
- [ ] 执行步骤可操作（4步法）
- [ ] 有快速工具调用示例
- [ ] 有质量检查清单
- [ ] 有常见问题处理
- [ ] 引用了scripts/和references/
- [ ] 中文语境适配良好
- [ ] 文档长度≤5000字

### 脚本质量
- [ ] 标准命令行接口（argparse）
- [ ] JSON标准化输出（summary + details + metadata）
- [ ] 错误处理完善（try-except + 友好提示）
- [ ] 性能指标记录（processing_time）
- [ ] 有单元测试（覆盖率≥80%）
- [ ] 有使用文档（docstring + README）
- [ ] 依赖管理清晰（pyproject.toml）
- [ ] 使用uv包管理（推荐）

### 架构质量
- [ ] 定性定量严格分离
- [ ] 三层信息披露完整
- [ ] 分层输出格式统一
- [ ] 目录结构规范
- [ ] 无重复文件

### 测试质量
- [ ] 单元测试覆盖率≥80%
- [ ] 有集成测试
- [ ] 有端到端测试
- [ ] 测试数据充分

### 文档质量
- [ ] 有理论背景（references/theory.md）
- [ ] 有完整案例（references/examples.md）
- [ ] 有故障排除（references/troubleshooting.md）
- [ ] 有脚本使用指南（scripts/README.md）

---

## 附录：参考文件清单

### 最佳实践示例

**Python技能（中文文本处理）**：
- `skills/coding/open-coding/SKILL.md` - 简洁的工具导向设计
- `skills/coding/open-coding/scripts/extract_concepts.py` - 标准脚本接口
- `skills/coding/open-coding/pyproject.toml` - uv包管理配置

**JavaScript技能（理论分析）**：
- `skills/ant/participant-skill/index.js` - SOLID架构主入口
- `skills/ant/participant-skill/src/ParticipantExtractor.js` - 单一职责实现

**架构文档**：
- `SKILLS_ARCHITECTURE_AUDIT.md` - 定性定量分离原则
- `SKILLS_QUALITY_AUDIT.md` - 质量评估标准
- `SKILLS_OPTIMIZATION_GUIDE.md` - 设计哲学

---

## 总结

### 核心要点

1. **技能 = 提示词 + 脚本 + 上下文**
2. **定性定量严格分离**：智能分析用提示词，确定性计算用脚本
3. **三层信息披露**：优化AI上下文负载
4. **标准化接口**：统一的命令行接口和输出格式
5. **中文本土化**：jieba优化 + 文化适配
6. **质量保证**：TDD + 质量检查清单
7. **避免反模式**：过度详细、缺少脚本、输出不一致、忽视中文

### 下一步行动

1. 使用本方法论审查现有技能
2. 识别不符合规范的技能
3. 按优先级修复问题
4. 开发新技能时严格遵循方法论
5. 持续优化和迭代

---

*本方法论基于sscisubagent-skills技能包的深度分析提取，适用于所有Claude Skills的开发。*
