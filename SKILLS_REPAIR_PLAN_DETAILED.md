# 技能修复详细计划 (Detailed Skills Repair Plan)

**版本**: 1.0.0  
**创建日期**: 2025-12-18  
**基于**: SKILLS_IMPLEMENTATION_METHODOLOGY.md 核心方法论

---

## 执行摘要 (Executive Summary)

### 总体评估

经过对13个核心技能的深入分析，发现以下关键问题：

**✅ 优势**：
- 所有13个核心技能都有完整的SKILL.md文件
- YAML frontmatter格式规范，符合Claude Skills标准
- 中文语境适配良好，触发条件清晰
- 质量检查清单完整

**⚠️ 主要问题**：
1. **重复技能问题严重**：存在6组重复技能（简化版vs详细版）
2. **定量脚本严重缺失**：13个技能中仅3个有scripts/目录
3. **定性定量分离不彻底**：SKILL.md包含过多技术细节
4. **references/目录全部缺失**：无法实现三层信息披露
5. **脚本接口不标准化**：现有脚本未遵循argparse + JSON输出规范
6. **中文文本处理未优化**：仅1个技能使用jieba，无uv集成

**📊 统计数据**：
- 总技能数：13个核心技能 + 6个重复技能 = 19个
- 有scripts/目录：3个 (23%)
- 有references/目录：0个 (0%)
- 符合方法论标准：2个 (15%)
- 需要重构：11个 (85%)
- 需要删除重复：6个

### 优先级排序

**高优先级（P0）**：
1. 删除重复技能（6个）
2. performing-open-coding（已有基础脚本）
3. performing-centrality-analysis（网络分析核心）
4. mathematical-statistics（已有脚本）

**中优先级（P1）**：
5. performing-axial-coding（编码核心）
6. performing-selective-coding（编码核心）
7. checking-theory-saturation（编码核心）
8. validity-reliability（已有脚本）

**低优先级（P2）**：
9. performing-network-computation
10. processing-network-data
11. resolving-research-conflicts
12. writing-grounded-theory-memos
13. conflict-resolution
14. network-computation

---

## 第一部分：重复技能清理计划

### 问题识别

发现以下6组重复技能（简化版 vs 详细版）：

| 简化版路径 | 详细版路径 | 重复类型 |
|-----------|-----------|---------|
| `skills/analysis/centrality-analysis/` | `skills/analysis/performing-centrality-analysis/` | 目录重复 |
| `skills/coding/open-coding/` | `skills/coding/performing-open-coding/` | 目录重复 |
| `skills/coding/theory-saturation/` | `skills/coding/checking-theory-saturation/` | 目录重复 |
| `skills/analysis/centrality-analysis-skill.md` | - | 单文件重复 |
| `skills/coding/open-coding-skill.md` | - | 单文件重复 |
| `skills/coding/axial-coding-skill.md` | - | 单文件重复 |

**反模式识别**：违反方法论第5条反模式（技能重复）

### 清理策略

**保留策略**：
- ✅ 保留详细版（`performing-*`目录）
- ❌ 删除简化版（单独目录和单文件）

**原因**：
1. 详细版符合方法论的完整结构要求
2. 详细版SKILL.md内容更丰富（5000-8000字）
3. 详细版有扩展空间（scripts/、references/）

### 具体任务清单

**任务1.1：删除重复目录（3个）**
```bash
# 删除简化版目录
rm -rf skills/analysis/centrality-analysis/
rm -rf skills/coding/open-coding/
rm -rf skills/coding/theory-saturation/
```
- 工作量：0.5小时
- 风险：低
- 依赖：无

**任务1.2：删除重复单文件（5个）**
```bash
# 删除单文件技能
rm skills/analysis/centrality-analysis-skill.md
rm skills/analysis/network-computation-skill.md
rm skills/analysis/network-data-skill.md
rm skills/coding/open-coding-skill.md
rm skills/coding/axial-coding-skill.md
rm skills/coding/selective-coding-skill.md
rm skills/coding/theory-saturation-skill.md
rm skills/coding/memo-writing-skill.md
```
- 工作量：0.5小时
- 风险：低
- 依赖：无

**任务1.3：更新SKILLS_MANIFEST.md**
- 移除重复技能的引用
- 确保只列出13个核心技能
- 工作量：0.5小时

**总工作量**：1.5小时

---

## 第二部分：逐技能深度分析与修复计划

---

## 技能1：performing-open-coding（开放编码）

### 当前状态评估

**✅ 已有资源**：
- SKILL.md：5047字节，112行 ✅ 符合长度要求
- scripts/auto_loader.py：基础概念提取脚本 ✅
- YAML frontmatter完整 ✅
- 触发条件清晰（6个关键词）✅

**❌ 缺失资源**：
- scripts/目录不完整（仅1个脚本）
- 缺少references/目录
- auto_loader.py未遵循标准接口
- 无pyproject.toml（uv集成）
- 无单元测试

### 定性定量分离分析

**定性部分（SKILL.md）**：✅ 良好
- 概念命名原则（"寻求支持"）✅
- 理论解释（开放编码原理）✅
- 质量标准（8项检查清单）✅
- 流程指导（5步法）✅

**定量部分（需要脚本化）**：⚠️ 严重不足
- ❌ 缺少：文本预处理脚本（jieba分词、去停用词）
- ❌ 缺少：概念聚类脚本（K-means、层次聚类）
- ❌ 缺少：持续比较脚本（相似度计算）
- ❌ 缺少：编码优化脚本（合并重复编码）
- ❌ 缺少：可视化脚本（概念网络图）
- ✅ 已有：auto_loader.py（基础概念提取）

**当前分离合理性**：⚠️ 部分合理
- SKILL.md中包含过多技术细节（如"jieba分词"）
- 应该移到references/technical-guide.md

### 缺失内容识别

**缺少的脚本（具体到函数级别）**：

1. **preprocess_text.py**（文本预处理）
   ```python
   def tokenize_chinese(text: str) -> List[str]
   def remove_stopwords(words: List[str]) -> List[str]
   def segment_by_meaning(text: str) -> List[str]
   ```

2. **extract_concepts.py**（概念提取）
   ```python
   def extract_action_concepts(text: str) -> List[Dict]
   def extract_emotion_concepts(text: str) -> List[Dict]
   def extract_relation_concepts(text: str) -> List[Dict]
   def abstract_concepts(raw_concepts: List) -> List[Dict]
   ```

3. **compare_codes.py**（持续比较）
   ```python
   def calculate_similarity(code1: str, code2: str) -> float
   def identify_duplicates(codes: List[Dict]) -> List[Tuple]
   def suggest_merges(codes: List[Dict]) -> List[Dict]
   ```

4. **cluster_concepts.py**（概念聚类）
   ```python
   def cluster_by_kmeans(concepts: List[Dict], n_clusters: int) -> Dict
   def cluster_hierarchical(concepts: List[Dict]) -> Dict
   def visualize_clusters(clusters: Dict) -> str  # 返回图片路径
   ```

5. **validate_codes.py**（编码验证）
   ```python
   def check_naming_convention(codes: List[Dict]) -> List[str]
   def check_definition_quality(codes: List[Dict]) -> List[str]
   def check_example_sufficiency(codes: List[Dict]) -> List[str]
   ```

**缺少的references文档**：

1. **references/theory.md**（理论背景）
   - 扎根理论的历史和流派
   - 开放编码的理论基础
   - Glaser vs Strauss的方法差异
   - 约5000字

2. **references/examples.md**（完整案例）
   - 中文访谈数据的完整编码案例
   - 从原始文本到概念列表的全过程
   - 约3000字

3. **references/troubleshooting.md**（故障排除）
   - 常见问题的详细解决方案
   - 编码质量问题的诊断方法
   - 约2000字

4. **references/chinese-context.md**（中文语境）
   - 中文质性研究的特殊性
   - 中文概念命名的最佳实践
   - 约2000字

**SKILL.md需要简化**：⚠️ 需要轻微简化
- 当前5047字节，接近上限
- 可以将"技术支持"部分移到references/technical-guide.md
- 减少200-300字节

### 修复计划

**优先级**：P0（高优先级）

**具体任务清单**：

1. **重构auto_loader.py为标准接口**（2小时）
   - 添加argparse命令行接口
   - 实现JSON标准化输出（summary + details + metadata）
   - 添加错误处理和日志
   - 添加性能指标记录

2. **创建5个核心脚本**（8小时）
   - preprocess_text.py（2小时）
   - extract_concepts.py（2小时）
   - compare_codes.py（2小时）
   - cluster_concepts.py（1.5小时）
   - validate_codes.py（0.5小时）

3. **创建pyproject.toml**（0.5小时）
   - 配置uv包管理
   - 添加jieba、pandas、scikit-learn依赖
   - 配置国内镜像

4. **创建references/目录**（4小时）
   - theory.md（1.5小时）
   - examples.md（1小时）
   - troubleshooting.md（1小时）
   - chinese-context.md（0.5小时）

5. **创建单元测试**（3小时）
   - tests/test_preprocess.py
   - tests/test_extract.py
   - tests/test_compare.py
   - 目标覆盖率：80%

6. **简化SKILL.md**（1小时）
   - 移除技术细节到references/
   - 优化快速工具部分
   - 更新引用链接

7. **创建scripts/README.md**（0.5小时）
   - 脚本使用指南
   - 参数说明
   - 示例命令

**总工作量**：19小时

**方法论对齐检查**：
- ✅ 定性定量严格分离
- ✅ 三层信息披露完整
- ✅ 标准化脚本接口
- ✅ 中文文本处理优化（jieba + uv）
- ✅ 质量检查清单完整
- ✅ 避免反模式

---

## 技能2：performing-axial-coding（轴心编码）

### 当前状态评估

**✅ 已有资源**：
- SKILL.md：5252字节，118行 ✅
- YAML frontmatter完整 ✅
- 触发条件清晰（6个关键词）✅
- 质量检查清单完整（4个维度）✅

**❌ 缺失资源**：
- 无scripts/目录 ❌ 严重问题
- 无references/目录 ❌
- 无pyproject.toml ❌
- 无单元测试 ❌

### 定性定量分离分析

**定性部分（SKILL.md）**：✅ 优秀
- 范畴命名原则 ✅
- Paradigm模型解释 ✅
- 关系类型分析 ✅
- 质量标准（4个维度）✅

**定量部分（需要脚本化）**：❌ 完全缺失
- ❌ 缺少：范畴识别脚本（聚类算法）
- ❌ 缺少：属性维度分析脚本
- ❌ 缺少：关系建立脚本（网络分析）
- ❌ 缺少：Paradigm构建脚本
- ❌ 缺少：可视化脚本（范畴网络图、Paradigm模型图）

**当前分离合理性**：⚠️ 基本合理
- SKILL.md中建议使用"scikit-learn"、"NetworkX"
- 这些技术细节应该移到references/

### 缺失内容识别

**缺少的脚本（具体到函数级别）**：

1. **identify_categories.py**（范畴识别）
   ```python
   def cluster_codes_to_categories(codes: List[Dict], min_codes: int = 3) -> List[Dict]
   def name_category(codes: List[Dict]) -> str
   def define_category(codes: List[Dict]) -> str
   def build_category_hierarchy(categories: List[Dict]) -> Dict
   ```

2. **analyze_properties.py**（属性维度分析）
   ```python
   def identify_properties(category: Dict) -> List[str]
   def define_dimensions(property: str, data: List) -> Dict
   def position_on_dimension(case: Dict, dimension: Dict) -> float
   def analyze_distribution(positions: List[float]) -> Dict
   ```

3. **build_relationships.py**（关系建立）
   ```python
   def identify_causal_relations(categories: List[Dict]) -> List[Tuple]
   def identify_conditional_relations(categories: List[Dict]) -> List[Tuple]
   def identify_strategy_relations(categories: List[Dict]) -> List[Tuple]
   def identify_interaction_relations(categories: List[Dict]) -> List[Tuple]
   def calculate_relation_strength(relation: Tuple, data: List) -> float
   ```

4. **construct_paradigm.py**（Paradigm构建）
   ```python
   def identify_conditions(categories: List[Dict]) -> List[str]
   def identify_actions(categories: List[Dict]) -> List[str]
   def identify_consequences(categories: List[Dict]) -> List[str]
   def build_paradigm_model(conditions, actions, consequences) -> Dict
   def validate_paradigm(model: Dict, data: List) -> Dict
   ```

5. **visualize_axial.py**（可视化）
   ```python
   def visualize_category_network(categories: List[Dict], relations: List) -> str
   def visualize_paradigm_model(paradigm: Dict) -> str
   def visualize_property_dimensions(properties: List[Dict]) -> str
   ```

**缺少的references文档**：

1. **references/paradigm-theory.md**（Paradigm理论）
   - Strauss & Corbin的Paradigm模型详解
   - 条件-行动-结果的逻辑关系
   - 约3000字

2. **references/category-examples.md**（范畴案例）
   - 中文研究中的范畴构建案例
   - 从概念到范畴的完整过程
   - 约4000字

3. **references/relationship-types.md**（关系类型）
   - 四种关系类型的详细说明
   - 关系识别的方法和技巧
   - 约2000字

4. **references/troubleshooting.md**（故障排除）
   - 范畴过于宽泛的处理
   - 概念归属不明确的解决
   - 约2000字

**SKILL.md需要简化**：⚠️ 需要简化
- 当前5252字节，略超推荐值
- 可以将"技术工具建议"移到references/
- 减少300-400字节

### 修复计划

**优先级**：P1（中优先级）

**具体任务清单**：

1. **创建scripts/目录和5个核心脚本**（10小时）
   - identify_categories.py（3小时）
   - analyze_properties.py（2小时）
   - build_relationships.py（3小时）
   - construct_paradigm.py（1.5小时）
   - visualize_axial.py（0.5小时）

2. **创建pyproject.toml**（0.5小时）
   - 配置依赖：pandas、scikit-learn、networkx、matplotlib

3. **创建references/目录**（4小时）
   - paradigm-theory.md（1.5小时）
   - category-examples.md（1.5小时）
   - relationship-types.md（0.5小时）
   - troubleshooting.md（0.5小时）

4. **创建单元测试**（3小时）
   - tests/test_categories.py
   - tests/test_properties.py
   - tests/test_relationships.py
   - 目标覆盖率：80%

5. **简化SKILL.md**（1小时）
   - 移除技术细节
   - 更新引用链接

6. **创建scripts/README.md**（0.5小时）

**总工作量**：19小时

**方法论对齐检查**：
- ✅ 定性定量严格分离
- ✅ 三层信息披露完整
- ✅ 标准化脚本接口
- ⚠️ 中文文本处理优化（需要添加jieba支持）
- ✅ 质量检查清单完整
- ✅ 避免反模式

---

## 技能3：performing-selective-coding（选择式编码）

### 当前状态评估

**✅ 已有资源**：
- SKILL.md：5720字节，108行 ✅
- YAML frontmatter完整 ✅
- 触发条件清晰（6个关键词）✅
- 质量检查清单完整（4个维度）✅

**❌ 缺失资源**：
- 无scripts/目录 ❌ 严重问题
- 无references/目录 ❌
- 无pyproject.toml ❌
- 无单元测试 ❌

### 定性定量分离分析

**定性部分（SKILL.md）**：✅ 优秀
- 核心范畴选择标准 ✅
- 故事线构建指导 ✅
- 理论框架整合方法 ✅
- 饱和度检验标准 ✅

**定量部分（需要脚本化）**：❌ 完全缺失
- ❌ 缺少：核心范畴识别脚本（网络中心性分析）
- ❌ 缺少：故事线构建脚本（时间序列分析）
- ❌ 缺少：理论框架整合脚本
- ❌ 缺少：饱和度检验脚本
- ❌ 缺少：可视化脚本（理论模型图、故事线图）

### 缺失内容识别

**缺少的脚本（具体到函数级别）**：

1. **identify_core_category.py**（核心范畴识别）
   ```python
   def calculate_explanatory_power(category: Dict, data: List) -> float
   def calculate_connectivity(category: Dict, relations: List) -> float
   def calculate_data_support(category: Dict, data: List) -> float
   def rank_categories(categories: List[Dict]) -> List[Dict]
   def validate_core_category(category: Dict, criteria: Dict) -> bool
   ```

2. **construct_storyline.py**（故事线构建）
   ```python
   def extract_timeline(data: List[Dict]) -> List[Dict]
   def identify_key_events(timeline: List) -> List[Dict]
   def identify_actors(data: List) -> List[str]
   def build_causal_chain(events: List[Dict]) -> List[Tuple]
   def generate_storyline(timeline, actors, causal_chain) -> str
   ```

3. **integrate_theory.py**（理论框架整合）
   ```python
   def formulate_propositions(categories: List[Dict], relations: List) -> List[str]
   def build_conceptual_framework(propositions: List[str]) -> Dict
   def explain_mechanisms(framework: Dict) -> Dict
   def define_boundaries(framework: Dict, data: List) -> Dict
   ```

4. **check_saturation.py**（饱和度检验）
   ```python
   def check_new_concepts(new_data: List, existing_concepts: List) -> Dict
   def check_category_completeness(categories: List[Dict]) -> Dict
   def check_relation_stability(relations: List, new_relations: List) -> Dict
   def assess_theory_completeness(theory: Dict) -> Dict
   def generate_saturation_report(checks: Dict) -> Dict
   ```

5. **visualize_selective.py**（可视化）
   ```python
   def visualize_theory_model(theory: Dict) -> str
   def visualize_storyline(storyline: Dict) -> str
   def visualize_saturation_trends(saturation_data: List) -> str
   ```

**缺少的references文档**：

1. **references/core-category-theory.md**（核心范畴理论）
   - 核心范畴的理论基础
   - 选择标准的详细说明
   - 约2000字

2. **references/storyline-examples.md**（故事线案例）
   - 中文研究中的故事线案例
   - 从范畴到故事线的过程
   - 约3000字

3. **references/saturation-criteria.md**（饱和度标准）
   - 饱和度的判断标准详解
   - 不同饱和度水平的处理
   - 约2000字

4. **references/troubleshooting.md**（故障排除）
   - 核心范畴难以确定的处理
   - 故事线不连贯的解决
   - 约2000字

**SKILL.md需要简化**：⚠️ 需要简化
- 当前5720字节，超过推荐值
- 可以将详细的判断标准移到references/
- 减少500-700字节

### 修复计划

**优先级**：P1（中优先级）

**具体任务清单**：

1. **创建scripts/目录和5个核心脚本**（10小时）
   - identify_core_category.py（2.5小时）
   - construct_storyline.py（2.5小时）
   - integrate_theory.py（2.5小时）
   - check_saturation.py（2小时）
   - visualize_selective.py（0.5小时）

2. **创建pyproject.toml**（0.5小时）

3. **创建references/目录**（3.5小时）
   - core-category-theory.md（1小时）
   - storyline-examples.md（1.5小时）
   - saturation-criteria.md（0.5小时）
   - troubleshooting.md（0.5小时）

4. **创建单元测试**（3小时）
   - tests/test_core_category.py
   - tests/test_storyline.py
   - tests/test_saturation.py
   - 目标覆盖率：80%

5. **简化SKILL.md**（1小时）
   - 移除详细标准到references/
   - 更新引用链接

6. **创建scripts/README.md**（0.5小时）

**总工作量**：18.5小时

**方法论对齐检查**：
- ✅ 定性定量严格分离
- ✅ 三层信息披露完整
- ✅ 标准化脚本接口
- ✅ 质量检查清单完整
- ✅ 避免反模式

---

## 技能4：checking-theory-saturation（理论饱和度检验）

### 当前状态评估

**✅ 已有资源**：
- SKILL.md：6227字节，117行 ⚠️ 超过推荐长度
- YAML frontmatter完整 ✅
- 触发条件清晰（6个关键词）✅
- 质量检查清单完整（4个维度）✅

**❌ 缺失资源**：
- 无scripts/目录 ❌ 严重问题
- 无references/目录 ❌
- 无pyproject.toml ❌
- 无单元测试 ❌

### 定性定量分离分析

**定性部分（SKILL.md）**：✅ 优秀但过于详细
- 饱和度定义清晰 ✅
- 4个检验维度完整 ✅
- 判断标准明确 ✅
- 但内容过多，需要简化 ⚠️

**定量部分（需要脚本化）**：❌ 完全缺失
- ❌ 缺少：概念稳定性检验脚本
- ❌ 缺少：范畴完整性检验脚本
- ❌ 缺少：关系稳定性检验脚本
- ❌ 缺少：理论完整性检验脚本
- ❌ 缺少：综合饱和度评估脚本
- ❌ 缺少：可视化脚本（饱和度趋势图）

### 缺失内容识别

**缺少的脚本（具体到函数级别）**：

1. **check_concept_saturation.py**（概念饱和检验）
   ```python
   def analyze_new_concepts(new_data: List, existing_concepts: List) -> Dict
   def calculate_concept_novelty(concept: str, existing: List) -> float
   def check_concept_completeness(concepts: List[Dict]) -> Dict
   def assess_abstraction_level(concepts: List[Dict]) -> Dict
   ```

2. **check_category_saturation.py**（范畴饱和检验）
   ```python
   def check_property_sufficiency(category: Dict) -> Dict
   def check_dimension_completeness(category: Dict) -> Dict
   def check_internal_consistency(category: Dict) -> Dict
   def assess_category_development(categories: List[Dict]) -> Dict
   ```

3. **check_relation_saturation.py**（关系饱和检验）
   ```python
   def identify_new_relations(new_data: List, existing_relations: List) -> List
   def check_relation_accuracy(relations: List, data: List) -> Dict
   def check_network_completeness(relations: List) -> Dict
   def assess_relation_stability(relations_history: List[List]) -> Dict
   ```

4. **check_theory_saturation.py**（理论饱和检验）
   ```python
   def check_explanatory_power(theory: Dict, data: List) -> Dict
   def check_theory_consistency(theory: Dict) -> Dict
   def check_theory_completeness(theory: Dict) -> Dict
   def assess_theory_value(theory: Dict) -> Dict
   ```

5. **assess_overall_saturation.py**（综合评估）
   ```python
   def integrate_saturation_checks(checks: Dict) -> Dict
   def determine_saturation_level(integrated: Dict) -> str  # "完全饱和"/"部分饱和"/"未饱和"
   def generate_recommendations(saturation_level: str, checks: Dict) -> List[str]
   def generate_saturation_report(all_results: Dict) -> Dict
   ```

6. **visualize_saturation.py**（可视化）
   ```python
   def visualize_concept_trends(concept_history: List) -> str
   def visualize_saturation_radar(saturation_scores: Dict) -> str
   def visualize_saturation_timeline(timeline_data: List) -> str
   ```

**缺少的references文档**：

1. **references/saturation-theory.md**（饱和度理论）
   - 理论饱和度的理论基础
   - 不同学派的饱和度标准
   - 约3000字

2. **references/saturation-examples.md**（饱和度案例）
   - 中文研究中的饱和度判断案例
   - 从未饱和到完全饱和的过程
   - 约3000字

3. **references/saturation-metrics.md**（饱和度指标）
   - 量化饱和度的指标体系
   - 指标的计算方法
   - 约2000字

4. **references/troubleshooting.md**（故障排除）
   - 难以判断饱和度的处理
   - 饱和度标准不一致的解决
   - 约2000字

**SKILL.md需要简化**：❌ 必须简化
- 当前6227字节，超过推荐值
- 可以将详细的检验步骤移到references/
- 减少1000-1500字节

### 修复计划

**优先级**：P1（中优先级）

**具体任务清单**：

1. **创建scripts/目录和6个核心脚本**（11小时）
   - check_concept_saturation.py（2小时）
   - check_category_saturation.py（2小时）
   - check_relation_saturation.py（2小时）
   - check_theory_saturation.py（2小时）
   - assess_overall_saturation.py（2.5小时）
   - visualize_saturation.py（0.5小时）

2. **创建pyproject.toml**（0.5小时）

3. **创建references/目录**（4小时）
   - saturation-theory.md（1.5小时）
   - saturation-examples.md（1.5小时）
   - saturation-metrics.md（0.5小时）
   - troubleshooting.md（0.5小时）

4. **创建单元测试**（3小时）
   - tests/test_concept_saturation.py
   - tests/test_category_saturation.py
   - tests/test_overall_saturation.py
   - 目标覆盖率：80%

5. **简化SKILL.md**（1.5小时）
   - 移除详细检验步骤到references/
   - 保留核心流程和快速工具
   - 更新引用链接

6. **创建scripts/README.md**（0.5小时）

**总工作量**：20.5小时

**方法论对齐检查**：
- ✅ 定性定量严格分离
- ✅ 三层信息披露完整
- ✅ 标准化脚本接口
- ✅ 质量检查清单完整
- ✅ 避免反模式

---

## 技能5：writing-grounded-theory-memos（扎根理论备忘录写作）

### 当前状态评估

**✅ 已有资源**：
- SKILL.md：6326字节，141行 ⚠️ 超过推荐长度
- YAML frontmatter完整 ✅
- 触发条件清晰（6个关键词）✅
- 质量检查清单完整 ✅

**❌ 缺失资源**：
- 无scripts/目录 ❌ 严重问题
- 无references/目录 ❌
- 无pyproject.toml ❌
- 无单元测试 ❌

### 定性定量分离分析

**定性部分（SKILL.md）**：✅ 优秀但过于详细
- 备忘录类型清晰（4种）✅
- 写作原则完整 ✅
- 质量标准明确 ✅
- 但内容过多，需要简化 ⚠️

**定量部分（需要脚本化）**：⚠️ 部分需要
- ❌ 缺少：备忘录模板生成脚本
- ❌ 缺少：备忘录关联分析脚本
- ❌ 缺少：备忘录质量检查脚本
- ⚠️ 注意：备忘录写作主要是定性工作，脚本作为辅助

### 缺失内容识别

**缺少的脚本（具体到函数级别）**：

1. **generate_memo_template.py**（模板生成）
   ```python
   def generate_concept_memo_template(concept: Dict) -> str
   def generate_relation_memo_template(relation: Tuple) -> str
   def generate_process_memo_template(stage: str) -> str
   def generate_theoretical_memo_template(theory: Dict) -> str
   ```

2. **link_memos.py**（备忘录关联）
   ```python
   def identify_related_memos(memo: Dict, all_memos: List) -> List[str]
   def build_memo_network(memos: List[Dict]) -> Dict
   def suggest_memo_connections(memo: Dict, context: Dict) -> List[str]
   ```

3. **check_memo_quality.py**（质量检查）
   ```python
   def check_memo_completeness(memo: Dict) -> Dict
   def check_memo_clarity(memo: Dict) -> Dict
   def check_memo_depth(memo: Dict) -> Dict
   def generate_quality_report(memos: List[Dict]) -> Dict
   ```

4. **organize_memos.py**（备忘录组织）
   ```python
   def categorize_memos(memos: List[Dict]) -> Dict
   def create_memo_timeline(memos: List[Dict]) -> List[Dict]
   def create_memo_index(memos: List[Dict]) -> Dict
   ```

**缺少的references文档**：

1. **references/memo-theory.md**（备忘录理论）
   - 备忘录在扎根理论中的作用
   - 不同学派的备忘录实践
   - 约2000字

2. **references/memo-examples.md**（备忘录案例）
   - 中文研究中的备忘录案例
   - 不同类型备忘录的实例
   - 约4000字

3. **references/memo-templates.md**（备忘录模板）
   - 各类备忘录的标准模板
   - 模板使用指南
   - 约2000字

4. **references/troubleshooting.md**（故障排除）
   - 备忘录写作的常见问题
   - 质量提升的方法
   - 约1500字

**SKILL.md需要简化**：❌ 必须简化
- 当前6326字节，超过推荐值
- 可以将详细的写作指导移到references/
- 减少1000-1500字节

### 修复计划

**优先级**：P2（低优先级）

**原因**：备忘录写作主要是定性工作，脚本辅助作用有限

**具体任务清单**：

1. **创建scripts/目录和4个辅助脚本**（5小时）
   - generate_memo_template.py（1.5小时）
   - link_memos.py（1.5小时）
   - check_memo_quality.py（1.5小时）
   - organize_memos.py（0.5小时）

2. **创建pyproject.toml**（0.5小时）

3. **创建references/目录**（3.5小时）
   - memo-theory.md（1小时）
   - memo-examples.md（1.5小时）
   - memo-templates.md（0.5小时）
   - troubleshooting.md（0.5小时）

4. **创建单元测试**（2小时）
   - tests/test_memo_templates.py
   - tests/test_memo_quality.py
   - 目标覆盖率：70%

5. **简化SKILL.md**（1.5小时）
   - 移除详细写作指导到references/
   - 保留核心原则和快速工具
   - 更新引用链接

6. **创建scripts/README.md**（0.5小时）

**总工作量**：13小时

**方法论对齐检查**：
- ✅ 定性定量严格分离（备忘录主要是定性）
- ✅ 三层信息披露完整
- ✅ 标准化脚本接口（辅助工具）
- ✅ 质量检查清单完整
- ✅ 避免反模式

---

## 技能6：performing-centrality-analysis（中心性分析）

### 当前状态评估

**✅ 已有资源**：
- SKILL.md：6423字节，115行 ⚠️ 超过推荐长度
- YAML frontmatter完整 ✅
- 触发条件清晰（6个关键词）✅
- 质量检查清单完整（4个维度）✅

**❌ 缺失资源**：
- 无scripts/目录 ❌ 严重问题
- 无references/目录 ❌
- 无pyproject.toml ❌
- 无单元测试 ❌

### 定性定量分离分析

**定性部分（SKILL.md）**：✅ 优秀但过于详细
- 4种中心性类型解释清晰 ✅
- 应用场景明确 ✅
- 中文语境适配良好 ✅
- 但包含过多技术细节 ⚠️

**定量部分（需要脚本化）**：❌ 完全缺失
- ❌ 缺少：网络数据加载脚本
- ❌ 缺少：中心性计算脚本（4种中心性）
- ❌ 缺少：关键节点识别脚本
- ❌ 缺少：中心性对比分析脚本
- ❌ 缺少：可视化脚本（网络图、分布图）

**当前分离合理性**：⚠️ 需要改进
- SKILL.md中包含算法细节（如"Brandes算法"）
- 这些技术细节应该移到references/

### 缺失内容识别

**缺少的脚本（具体到函数级别）**：

1. **load_network.py**（网络加载）
   ```python
   def load_edgelist(file_path: str) -> nx.Graph
   def load_adjacency_matrix(file_path: str) -> nx.Graph
   def load_adjacency_list(file_path: str) -> nx.Graph
   def validate_network(G: nx.Graph) -> Dict
   def clean_network(G: nx.Graph) -> nx.Graph
   ```

2. **calculate_centrality.py**（中心性计算）
   ```python
   def calculate_degree_centrality(G: nx.Graph) -> Dict[str, float]
   def calculate_closeness_centrality(G: nx.Graph) -> Dict[str, float]
   def calculate_betweenness_centrality(G: nx.Graph) -> Dict[str, float]
   def calculate_eigenvector_centrality(G: nx.Graph) -> Dict[str, float]
   def calculate_all_centralities(G: nx.Graph) -> Dict[str, Dict]
   ```

3. **identify_key_nodes.py**（关键节点识别）
   ```python
   def rank_nodes_by_centrality(centrality: Dict, top_n: int = 10) -> List[Tuple]
   def identify_hubs(centrality_scores: Dict) -> List[str]
   def identify_bridges(betweenness: Dict, threshold: float) -> List[str]
   def identify_influencers(eigenvector: Dict, threshold: float) -> List[str]
   def classify_nodes(centrality_scores: Dict) -> Dict[str, List]
   ```

4. **compare_centralities.py**（中心性对比）
   ```python
   def calculate_centrality_correlation(cent1: Dict, cent2: Dict) -> float
   def compare_rankings(cent1: Dict, cent2: Dict) -> Dict
   def identify_discrepancies(centrality_scores: Dict) -> List[Dict]
   def analyze_centrality_distribution(centrality: Dict) -> Dict
   ```

5. **visualize_centrality.py**（可视化）
   ```python
   def visualize_network_with_centrality(G: nx.Graph, centrality: Dict) -> str
   def visualize_centrality_distribution(centrality: Dict) -> str
   def visualize_centrality_comparison(centralities: Dict) -> str
   def visualize_key_nodes(G: nx.Graph, key_nodes: List) -> str
   ```

**缺少的references文档**：

1. **references/centrality-theory.md**（中心性理论）
   - 4种中心性的数学定义和公式
   - 算法原理详解（Brandes算法等）
   - 约4000字

2. **references/centrality-examples.md**（中心性案例）
   - 中文社会网络的中心性分析案例
   - 不同中心性指标的解释示例
   - 约3000字

3. **references/chinese-context.md**（中文语境）
   - 中国社会的"关系"网络特点
   - 中心性在中国文化中的解释
   - 约2000字

4. **references/troubleshooting.md**（故障排除）
   - 网络规模过大的处理
   - 中心性结果矛盾的分析
   - 约2000字

**SKILL.md需要简化**：❌ 必须简化
- 当前6423字节，超过推荐值
- 可以将算法细节和公式移到references/
- 减少1000-1500字节

### 修复计划

**优先级**：P0（高优先级）

**原因**：网络分析是核心功能，需求量大

**具体任务清单**：

1. **创建scripts/目录和5个核心脚本**（10小时）
   - load_network.py（1.5小时）
   - calculate_centrality.py（3小时）
   - identify_key_nodes.py（2小时）
   - compare_centralities.py（2小时）
   - visualize_centrality.py（1.5小时）

2. **创建pyproject.toml**（0.5小时）
   - 配置依赖：networkx、pandas、matplotlib、numpy

3. **创建references/目录**（4小时）
   - centrality-theory.md（2小时）
   - centrality-examples.md（1.5小时）
   - chinese-context.md（0.5小时）
   - troubleshooting.md（0.5小时）

4. **创建单元测试**（3小时）
   - tests/test_load_network.py
   - tests/test_centrality.py
   - tests/test_key_nodes.py
   - 目标覆盖率：80%

5. **简化SKILL.md**（1.5小时）
   - 移除算法细节到references/
   - 保留核心概念和快速工具
   - 更新引用链接

6. **创建scripts/README.md**（0.5小时）

**总工作量**：19.5小时

**方法论对齐检查**：
- ✅ 定性定量严格分离
- ✅ 三层信息披露完整
- ✅ 标准化脚本接口
- ✅ 质量检查清单完整
- ✅ 避免反模式

---

## 技能7：performing-network-computation（网络计算分析）

### 当前状态评估

**✅ 已有资源**：
- SKILL.md：6768字节，161行 ❌ 严重超过推荐长度
- YAML frontmatter完整 ✅
- 触发条件清晰（6个关键词）✅
- 质量检查清单完整 ✅

**❌ 缺失资源**：
- 无scripts/目录 ❌ 严重问题
- 无references/目录 ❌
- 无pyproject.toml ❌
- 无单元测试 ❌

### 定性定量分离分析

**定性部分（SKILL.md）**：⚠️ 过于详细
- 网络构建方法清晰 ✅
- 基础指标解释完整 ✅
- 社区检测方法详细 ✅
- 但内容过多，需要大幅简化 ❌

**定量部分（需要脚本化）**：❌ 完全缺失
- ❌ 缺少：网络构建脚本
- ❌ 缺少：基础指标计算脚本
- ❌ 缺少：社区检测脚本
- ❌ 缺少：网络可视化脚本

### 缺失内容识别

**缺少的脚本（具体到函数级别）**：

1. **build_network.py**（网络构建）
   ```python
   def build_from_edgelist(edges: List[Tuple]) -> nx.Graph
   def build_from_matrix(matrix: np.ndarray, node_labels: List) -> nx.Graph
   def build_from_survey(survey_data: pd.DataFrame) -> nx.Graph
   def add_node_attributes(G: nx.Graph, attributes: Dict) -> nx.Graph
   def add_edge_weights(G: nx.Graph, weights: Dict) -> nx.Graph
   ```

2. **calculate_metrics.py**（基础指标）
   ```python
   def calculate_network_size(G: nx.Graph) -> Dict
   def calculate_density(G: nx.Graph) -> float
   def calculate_average_degree(G: nx.Graph) -> float
   def calculate_clustering_coefficient(G: nx.Graph) -> Dict
   def calculate_path_metrics(G: nx.Graph) -> Dict
   def calculate_all_basic_metrics(G: nx.Graph) -> Dict
   ```

3. **detect_communities.py**（社区检测）
   ```python
   def detect_louvain(G: nx.Graph) -> Dict
   def detect_girvan_newman(G: nx.Graph, k: int) -> Dict
   def detect_label_propagation(G: nx.Graph) -> Dict
   def compare_community_methods(G: nx.Graph) -> Dict
   def evaluate_community_quality(G: nx.Graph, communities: Dict) -> Dict
   ```

4. **visualize_network.py**（网络可视化）
   ```python
   def visualize_basic_network(G: nx.Graph) -> str
   def visualize_with_communities(G: nx.Graph, communities: Dict) -> str
   def visualize_with_centrality(G: nx.Graph, centrality: Dict) -> str
   def create_interactive_visualization(G: nx.Graph) -> str
   ```

**缺少的references文档**：

1. **references/network-theory.md**（网络理论）
   - 社会网络分析的理论基础
   - 网络指标的数学定义
   - 约4000字

2. **references/community-detection.md**（社区检测）
   - 社区检测算法详解
   - 算法选择指南
   - 约3000字

3. **references/network-examples.md**（网络案例）
   - 中文社会网络分析案例
   - 不同类型网络的分析示例
   - 约3000字

4. **references/troubleshooting.md**（故障排除）
   - 网络构建的常见问题
   - 社区检测结果不理想的处理
   - 约2000字

**SKILL.md需要简化**：❌ 必须大幅简化
- 当前6768字节，严重超过推荐值
- 需要移除大量技术细节到references/
- 减少2000-2500字节

### 修复计划

**优先级**：P2（低优先级）

**原因**：与performing-centrality-analysis功能重叠，优先级较低

**具体任务清单**：

1. **创建scripts/目录和4个核心脚本**（9小时）
   - build_network.py（2.5小时）
   - calculate_metrics.py（2.5小时）
   - detect_communities.py（3小时）
   - visualize_network.py（1小时）

2. **创建pyproject.toml**（0.5小时）

3. **创建references/目录**（4小时）
   - network-theory.md（2小时）
   - community-detection.md（1.5小时）
   - network-examples.md（1.5小时）
   - troubleshooting.md（0.5小时）

4. **创建单元测试**（3小时）
   - tests/test_build_network.py
   - tests/test_metrics.py
   - tests/test_communities.py
   - 目标覆盖率：80%

5. **大幅简化SKILL.md**（2小时）
   - 移除技术细节到references/
   - 保留核心流程和快速工具
   - 更新引用链接

6. **创建scripts/README.md**（0.5小时）

**总工作量**：19小时

---

## 技能8：processing-network-data（网络数据处理）

### 当前状态评估

**✅ 已有资源**：
- SKILL.md：8480字节，178行 ❌ 严重超过推荐长度
- YAML frontmatter完整 ✅
- 触发条件清晰（6个关键词）✅
- 质量检查清单完整 ✅

**❌ 缺失资源**：
- 无scripts/目录 ❌ 严重问题
- 无references/目录 ❌
- 无pyproject.toml ❌
- 无单元测试 ❌

### 修复计划

**优先级**：P2（低优先级）

**原因**：数据处理是基础工作，但优先级低于核心分析功能

**简要任务清单**：
1. 创建4个数据处理脚本（8小时）
2. 创建references/目录（3小时）
3. 创建单元测试（2.5小时）
4. 大幅简化SKILL.md（2小时）
5. 创建pyproject.toml和README（1小时）

**总工作量**：16.5小时

---

## 技能9：resolving-research-conflicts（研究冲突解决）

### 当前状态评估

**✅ 已有资源**：
- SKILL.md：7085字节，135行 ❌ 超过推荐长度
- YAML frontmatter完整 ✅
- 触发条件清晰（6个关键词）✅

**❌ 缺失资源**：
- 无scripts/目录 ❌
- 无references/目录 ❌
- 无pyproject.toml ❌
- 无单元测试 ❌

### 定性定量分离分析

**定性部分（SKILL.md）**：✅ 优秀
- 分歧类型识别清晰 ✅
- 对话策略完整 ✅
- 共识建立机制详细 ✅

**定量部分（需要脚本化）**：⚠️ 部分需要
- ❌ 缺少：分歧分析脚本（文本分析）
- ❌ 缺少：证据整合脚本
- ❌ 缺少：共识度量脚本
- ⚠️ 注意：冲突解决主要是定性工作，脚本作为辅助

### 修复计划

**优先级**：P2（低优先级）

**原因**：主要是定性工作，脚本辅助作用有限

**简要任务清单**：
1. 创建3个辅助脚本（5小时）
2. 创建references/目录（3小时）
3. 创建单元测试（2小时）
4. 简化SKILL.md（1.5小时）
5. 创建pyproject.toml和README（1小时）

**总工作量**：12.5小时

---

## 技能10-13：特殊目录技能

### conflict-resolution（冲突解决）

**当前状态**：
- SKILL.md：2697字节，37行 ✅ 长度合适
- 无scripts/目录 ❌
- 与resolving-research-conflicts功能重叠 ⚠️

**问题**：与技能9重复

**修复策略**：
- **选项A**：合并到resolving-research-conflicts
- **选项B**：明确区分（conflict-resolution处理一般冲突，resolving-research-conflicts处理研究冲突）

**推荐**：选项A（合并）

**工作量**：2小时

---

### mathematical-statistics（数理统计）

**当前状态**：
- SKILL.md：3269字节，40行 ✅ 长度合适
- scripts/目录：✅ 已有2个脚本
  - simplified_statistics.py（261行）
  - statistics_toolkit.py

**✅ 优势**：
- 已有完整的脚本实现
- 脚本功能完整（描述性统计、t检验、方差分析等）

**❌ 问题**：
- 脚本未遵循标准接口（无argparse）
- 脚本输出格式不统一
- 无pyproject.toml（uv集成）
- 无references/目录
- 无单元测试

### 修复计划

**优先级**：P0（高优先级）

**原因**：已有脚本基础，修复成本低，收益高

**具体任务清单**：

1. **重构2个现有脚本为标准接口**（4小时）
   - 添加argparse命令行接口
   - 实现JSON标准化输出
   - 添加错误处理

2. **创建pyproject.toml**（0.5小时）
   - 配置依赖：scipy、numpy、pandas

3. **创建references/目录**（3小时）
   - statistics-theory.md（1.5小时）
   - statistics-examples.md（1小时）
   - troubleshooting.md（0.5小时）

4. **创建单元测试**（3小时）
   - tests/test_descriptive.py
   - tests/test_inferential.py
   - 目标覆盖率：80%

5. **优化SKILL.md**（1小时）
   - 添加快速工具调用示例
   - 更新引用链接

6. **创建scripts/README.md**（0.5小时）

**总工作量**：12小时

---

### validity-reliability（信效度分析）

**当前状态**：
- SKILL.md：2509字节，36行 ✅ 长度合适
- scripts/目录：✅ 已有2个脚本
  - simplified_validity_reliability.py（283行）
  - validity_reliability_toolkit.py

**问题与修复计划**：与mathematical-statistics类似

**优先级**：P1（中优先级）

**总工作量**：12小时

---

### network-computation（网络计算）

**当前状态**：
- SKILL.md：3105字节，43行 ✅ 长度合适
- 无scripts/目录 ❌
- 与performing-network-computation功能重叠 ⚠️

**问题**：与技能7重复

**修复策略**：
- **选项A**：合并到performing-network-computation
- **选项B**：明确区分（network-computation处理基础计算，performing-network-computation处理高级分析）

**推荐**：选项A（合并）

**工作量**：2小时

---

## 第三部分：优先级排序与实施时间表

### 优先级矩阵

| 优先级 | 技能名称 | 工作量 | 原因 |
|-------|---------|-------|------|
| **P0** | 删除重复技能 | 1.5小时 | 清理冗余，必须优先 |
| **P0** | performing-open-coding | 19小时 | 已有基础，编码核心 |
| **P0** | performing-centrality-analysis | 19.5小时 | 网络分析核心 |
| **P0** | mathematical-statistics | 12小时 | 已有脚本，修复成本低 |
| **P1** | performing-axial-coding | 19小时 | 编码核心 |
| **P1** | performing-selective-coding | 18.5小时 | 编码核心 |
| **P1** | checking-theory-saturation | 20.5小时 | 编码核心 |
| **P1** | validity-reliability | 12小时 | 已有脚本 |
| **P2** | performing-network-computation | 19小时 | 功能重叠，优先级低 |
| **P2** | processing-network-data | 16.5小时 | 基础工作，优先级低 |
| **P2** | resolving-research-conflicts | 12.5小时 | 定性为主，脚本辅助 |
| **P2** | writing-grounded-theory-memos | 13小时 | 定性为主，脚本辅助 |
| **P2** | 合并重复技能 | 4小时 | 清理工作 |

### 实施时间表（6个阶段）

#### 阶段1：清理与高优先级基础（Week 1-2）

**目标**：清理重复技能，完成P0技能

**任务**：
1. 删除重复技能（1.5小时）
2. performing-open-coding（19小时）
3. mathematical-statistics（12小时）
4. performing-centrality-analysis（19.5小时）

**总工作量**：52小时（约2周）

**交付成果**：
- ✅ 清理6组重复技能
- ✅ 3个P0技能完全符合方法论
- ✅ 更新SKILLS_MANIFEST.md

---

#### 阶段2：编码类技能完善（Week 3-5）

**目标**：完成编码类核心技能

**任务**：
1. performing-axial-coding（19小时）
2. performing-selective-coding（18.5小时）
3. checking-theory-saturation（20.5小时）

**总工作量**：58小时（约3周）

**交付成果**：
- ✅ 编码类5个技能全部完善
- ✅ 形成完整的扎根理论技能链

---

#### 阶段3：分析类技能完善（Week 6-7）

**目标**：完成分析类核心技能

**任务**：
1. validity-reliability（12小时）
2. performing-network-computation（19小时）
3. processing-network-data（16.5小时）

**总工作量**：47.5小时（约2周）

**交付成果**：
- ✅ 分析类技能全部完善
- ✅ 形成完整的网络分析技能链

---

#### 阶段4：方法论类技能完善（Week 8）

**目标**：完成方法论类技能

**任务**：
1. resolving-research-conflicts（12.5小时）
2. writing-grounded-theory-memos（13小时）

**总工作量**：25.5小时（约1周）

**交付成果**：
- ✅ 方法论类技能全部完善

---

#### 阶段5：重复技能合并（Week 9）

**目标**：合并重复的特殊目录技能

**任务**：
1. 合并conflict-resolution到resolving-research-conflicts（2小时）
2. 合并network-computation到performing-network-computation（2小时）

**总工作量**：4小时

**交付成果**：
- ✅ 删除2个重复技能
- ✅ 更新SKILLS_MANIFEST.md

---

#### 阶段6：质量审计与文档完善（Week 10）

**目标**：全面质量审计，确保符合方法论

**任务**：
1. 运行validate_skills.py（2小时）
2. 逐技能质量检查（10小时）
3. 更新所有文档（5小时）
4. 创建使用示例（3小时）

**总工作量**：20小时（约1周）

**交付成果**：
- ✅ 所有技能通过质量审计
- ✅ 完整的使用文档
- ✅ 发布v2.0.0版本

---

### 总工作量统计

| 阶段 | 工作量 | 周数 |
|-----|-------|------|
| 阶段1 | 52小时 | 2周 |
| 阶段2 | 58小时 | 3周 |
| 阶段3 | 47.5小时 | 2周 |
| 阶段4 | 25.5小时 | 1周 |
| 阶段5 | 4小时 | 0.5周 |
| 阶段6 | 20小时 | 1周 |
| **总计** | **207小时** | **9.5周** |

**按每周40小时计算**：约5.2周（满负荷工作）
**按每周20小时计算**：约10.4周（兼职工作）

---

## 第四部分：方法论对齐核查表

### 核查表模板（每个技能）

```markdown
## 技能名称：[skill-name]

### 1. 定性定量严格分离 ✅/❌
- [ ] SKILL.md只包含概念、理论、流程指导
- [ ] 确定性逻辑全部脚本化
- [ ] 无算法伪代码在SKILL.md中

### 2. 三层信息披露 ✅/❌
- [ ] 第1层：SKILL.md核心提示词（≤5000字）
- [ ] 第2层：JSON输出摘要（summary + details）
- [ ] 第3层：references/详细文档

### 3. 标准化脚本接口 ✅/❌
- [ ] 使用argparse命令行接口
- [ ] JSON标准化输出（summary + details + metadata）
- [ ] 错误处理完善
- [ ] 性能指标记录

### 4. 中文文本处理优化 ✅/❌/N/A
- [ ] 使用jieba分词（如适用）
- [ ] 配置uv包管理（pyproject.toml）
- [ ] 使用国内镜像
- [ ] 中文停用词处理

### 5. SKILL.md写作模式 ✅/❌
- [ ] YAML frontmatter完整
- [ ] 使用时机清晰（≥6个关键词）
- [ ] 快速工具调用示例
- [ ] 执行步骤可操作（4步法）
- [ ] 质量检查清单完整
- [ ] 引用scripts/和references/

### 6. 分层输出设计 ✅/❌
- [ ] overview（5-10秒理解）
- [ ] summary（30秒阅读）
- [ ] details（深入分析）
- [ ] metadata（元数据）

### 7. 质量保证机制 ✅/❌
- [ ] 单元测试覆盖率≥80%
- [ ] 集成测试
- [ ] 质量检查清单
- [ ] 错误处理测试

### 8. 中文本土化适配 ✅/❌
- [ ] 术语本土化
- [ ] 文化敏感性处理
- [ ] 中文语境示例
- [ ] 符合中文表达习惯

### 9. 目录结构规范 ✅/❌
- [ ] SKILL.md存在
- [ ] scripts/目录（如需要）
- [ ] references/目录
- [ ] tests/目录
- [ ] pyproject.toml（如有脚本）
- [ ] scripts/README.md（如有脚本）

### 10. 避免反模式 ✅/❌
- [ ] 无SKILL.md过于详细
- [ ] 无缺少脚本支持
- [ ] 无输出格式不一致
- [ ] 无忽视中文语境
- [ ] 无技能重复
- [ ] 无过度设计
- [ ] 无缺少测试
- [ ] 无硬编码配置

**总分**：[X/10]

**符合度**：[优秀/良好/合格/不合格]
- 优秀：9-10分
- 良好：7-8分
- 合格：5-6分
- 不合格：<5分
```

---

## 第五部分：实施建议

### 建议1：采用TDD（测试驱动开发）

**原因**：
- 确保脚本质量
- 提前发现设计问题
- 便于重构

**实践**：
1. 先写测试用例
2. 再实现功能
3. 重构优化

### 建议2：使用模板加速开发

**创建以下模板**：
1. `templates/script_template.py`（标准脚本模板）
2. `templates/test_template.py`（测试模板）
3. `templates/pyproject_template.toml`（配置模板）
4. `templates/README_template.md`（文档模板）

### 建议3：持续集成（CI/CD）

**使用GitHub Actions**：
1. 自动运行测试
2. 检查代码质量
3. 验证SKILL.md格式
4. 生成覆盖率报告

### 建议4：文档优先

**原则**：
- 先写SKILL.md和references/
- 再实现脚本
- 确保文档与代码一致

### 建议5：定期审查

**频率**：每完成一个技能后审查
**内容**：
- 方法论对齐检查
- 代码质量审查
- 文档完整性审查
- 用户体验测试

---

## 附录A：脚本接口标准模板

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[脚本名称]

功能描述：[简要说明]

使用方式：
  python [script_name].py --input data.json --output result.json
  
依赖：
  - [依赖1]>=版本
  - [依赖2]>=版本
"""

import argparse
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='[脚本功能描述]',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # 必需参数
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='输入文件路径'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='output.json',
        help='输出文件路径（默认：output.json）'
    )
    
    # 可选参数
    parser.add_argument(
        '--param1',
        type=int,
        default=10,
        help='参数1说明（默认：10）'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细信息'
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # 1. 加载数据
        logging.info(f"加载数据：{args.input}")
        with open(args.input, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        
        # 2. 数据验证
        validate_input(input_data)
        
        # 3. 处理逻辑
        start_time = datetime.now()
        result = process_data(input_data, args.param1)
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # 4. 构建标准化输出
        output = {
            'summary': {
                'total_items': len(result.get('items', [])),
                'processing_time': processing_time,
                'key_metrics': result.get('metrics', {})
            },
            'details': {
                'items': result.get('items', []),
                'statistics': result.get('statistics', {})
            },
            'metadata': {
                'input_file': args.input,
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'parameters': {
                    'param1': args.param1
                }
            }
        }
        
        # 5. 保存结果
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        # 6. 输出摘要
        logging.info(f"✅ 处理完成")
        logging.info(f"   处理项目数：{output['summary']['total_items']}")
        logging.info(f"   处理时间：{processing_time:.2f}秒")
        logging.info(f"📄 详细结果：{args.output}")
        
    except FileNotFoundError as e:
        logging.error(f"文件未找到：{e}")
        return 1
    except ValueError as e:
        logging.error(f"数据格式错误：{e}")
        return 2
    except Exception as e:
        logging.error(f"未知错误：{e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 99
    
    return 0

def validate_input(data: Dict) -> None:
    """验证输入数据"""
    required_fields = ['field1', 'field2']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"缺少必需字段：{field}")

def process_data(data: Dict, param1: int) -> Dict:
    """处理数据的核心逻辑"""
    # TODO: 实现具体逻辑
    result = {
        'items': [],
        'metrics': {},
        'statistics': {}
    }
    return result

if __name__ == '__main__':
    exit(main())
```

---

## 附录B：pyproject.toml标准模板

```toml
[project]
name = "skill-name"
version = "1.0.0"
description = "技能简要描述"
requires-python = ">=3.8"
dependencies = [
    "jieba>=0.42.1",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
]

[tool.uv]
# 使用国内镜像加速
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple/"
default = true

# 缓存配置
[tool.uv.cache]
keys = ["jieba"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=scripts --cov-report=html --cov-report=term"

[tool.black]
line-length = 100
target-version = ['py38']

[tool.flake8]
max-line-length = 100
exclude = [".git", "__pycache__", "build", "dist"]
```

---

## 总结

本详细修复计划提供了：

1. **13个核心技能的逐一深度分析**
2. **6组重复技能的清理策略**
3. **具体到函数级别的缺失脚本识别**
4. **详细的references/文档规划**
5. **可执行的任务清单和工作量估算**
6. **6个阶段的实施时间表**
7. **完整的方法论对齐核查表**
8. **标准化的脚本和配置模板**

**总工作量**：约207小时（9.5周）

**关键成功因素**：
- 严格遵循SKILLS_IMPLEMENTATION_METHODOLOGY.md
- 采用TDD确保质量
- 持续审查和迭代
- 文档优先原则

**预期成果**：
- 13个完全符合方法论的高质量技能
- 完整的脚本工具链
- 丰富的参考文档
- 80%以上的测试覆盖率
- 发布sscisubagent-skills v2.0.0

---

**文档版本**: 1.0.0  
**最后更新**: 2025-12-18  
**下一步行动**: 开始阶段1（清理与高优先级基础）
