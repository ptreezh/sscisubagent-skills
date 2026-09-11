  1. 建立编码本
     - 记录所有编码
     - 定义每个范畴
     - 定义每个概念
     - 提供示例

  2. 持续更新
     - 新编码及时记录
     - 修改编码时更新
     - 合并编码时说明

  3. 编码一致性
     - 相同内容相同编码
     - 使用编码本检查
     - 定期审查
```

**量化标准**:
- ✅ 有完整编码本
- ✅ 编码定义清晰
- ✅ 编码一致
- ✅ 可复现

## 📋 任务分解规则

### 四大原则

1. **粒度可控原则**
   - 每个子任务必须在**一次会话**中完成
   - 单个任务不超过**3小时**
   - 任务间依赖关系明确

2. **量化标准原则**
   - 每个子任务有**明确的完成标准**
   - 可验证的输出产物（编码、备忘录、理论）
   - 可测量的质量指标

3. **独立验证原则**
   - 每个子任务完成后**独立验证**
   - 验证清单（质量检查点）
   - 不合格返工机制

4. **数据清单原则**
   - 子agent必须输出**完整的数据清单**
   - 原始数据、编码、备忘录
   - 确保可复现性

### 扎根理论分析任务分解模板

```yaml
完整扎根理论研究（3-6个月）:

  Phase 1: 数据准备与初步编码（1个月）
    Task 1.1: 资料收集（2周）
      - 输出: 访谈/观察资料
      - 验证: 资料完整性

    Task 1.2: 开放编码（2周）
      - 输出: 开放编码清单
      - 验证: 所有资料已编码

  Phase 2: 轴心编码（1-2个月）
    Task 2.1: 范畴识别（2周）
      - 输出: 范畴清单
      - 验证: 范畴间有区别

    Task 2.2: 轴心编码（2-6周）
      - 输出: 轴心编码图
      - 验证: 范畴关系明确

    Task 2.3: 备忘录撰写（2-6周）
      - 输出: 编码备忘录
      - 验证: 备忘录完整

  Phase 3: 选择式编码（1-2个月）
    Task 3.1: 核心范畴识别（2周）
      - 输出: 核心范畴
      - 验证: 核心范畴可以整合所有范畴

    Task 3.2: 理论整合（2-6周）
      - 输出: 理论草稿
      - 验证: 理论连贯

    Task 3.3: 饱和度检验（2周）
      - 输出: 饱和度报告
      - 验证: 理论饱和

  Phase 4: 理论撰写（1个月）
    Task 4.1: 理论撰写（2周）
      - 输出: 完整理论
      - 验证: 理论完整

    Task 4.2: 案例支撑（2周）
      - 输出: 案例引用清单
      - 验证: 所有范畴有案例支撑
```

## 🔄 CLI任务队列自动执行

### 自动激活条件

当满足以下任一条件时，技能自动激活任务队列模式：

```yaml
激活条件:
  - 任务估计时间 > 3小时
  - 包含3个以上独立子任务
  - 需要多阶段验证
  - 用户明确要求"分解任务"
```

### 扎根理论分析自动分解示例

```yaml
用户请求: "分析这些访谈资料，生成扎根理论"

自动分解为:

Phase 1: 开放编码（1小时）
  Task 1.1: 逐行编码前20份资料（30分钟）
    - 输出: 开放编码清单（前20份）
    - 验证: 每行都有编码

  Task 1.2: 识别初始范畴（30分钟）
    - 输出: 初始范畴清单
    - 验证: 范畴有区别

Phase 2: 轴心编码（1.5小时）
  Task 2.1: 范畴联结（45分钟）
    - 输出: 范畴关系图
    - 验证: 关系合理

  Task 2.2: 撰写编码备忘录（45分钟）
    - 输出: 备忘录文档
    - 验证: 备忘录完整

Phase 3: 选择式编码（1.5小时）
  Task 3.1: 识别核心范畴（30分钟）
    - 输出: 核心范畴
    - 验证: 核心范畴整合所有范畴

  Task 3.2: 构建故事线（30分钟）
    - 输出: 理论故事线
    - 验证: 故事线连贯

  Task 3.3: 撰写理论（30分钟）
    - 输出: 完整理论
    - 验证: 理论完整

总估计时间: 4小时
```

## 🔄 CLI任务队列自动执行

### 双模式执行架构

本技能支持两种执行模式，根据任务特点**自动选择**最佳方式：

#### 模式A: CLI任务队列（基础/默认）

**使用场景**:
- 少量访谈资料（1-5个）
- 任务有依赖关系
- 单个文件编码

**实现**:
```yaml
1. TaskCreate创建编码任务
2. 主Agent依次执行编码
3. TaskUpdate更新状态
4. 持久化编码结果
```

**特点**:
- ✅ 简单可靠
- ✅ 上下文完整
- ✅ 适合小批量

#### 模式B: 子Agent并行（增强）

**使用场景**:
- 批量访谈资料（>5个）
- 资料相互独立
- 需要显著加速

**实现**:
```yaml
1. 识别可并行任务
2. 启动多个grounded-theory-coder子Agent
3. 并行执行编码
4. 整合编码结果
```

**特点**:
- ⚡ 5-10x加速
- ✅ 独立context
- ✅ 适合大批量

**性能对比**:
```yaml
10个访谈文件:
  CLI队列: 5小时（依次处理）
  子Agent: 35分钟（并行处理）
  加速比: 8.6x ⚡
```

### 自动决策逻辑（对用户透明）

```python
def decide_coding_mode(data_files):
    """自动决策使用哪种编码模式"""

    # 判断1: 文件数量
    if len(data_files) <= 5:
        return "CLI_QUEUE", "文件少，使用CLI队列"

    # 判断2: 独立性
    if has_dependencies(data_files):
        return "CLI_QUEUE", "有依赖关系，使用CLI队列"

    # 判断3: 数据量
    total_size = sum(file_size(f) for f in data_files)
    if total_size < 100_000:  # 100KB
        return "CLI_QUEUE", "数据量小，使用CLI队列"

    # 默认：使用子Agent并行
    return "SUBAGENT_PARALLEL", "批量编码，使用子Agent并行"
```

### ⚠️ 优雅降级机制

**保证**: 即使子Agent不可用，核心功能仍然正常工作

```yaml
降级触发条件:
  1. Agent tool不可用
     → 自动降级到CLI队列
     → 友好提示（如果任务多）

  2. 资源不足（内存/CPU）
     → 自动降级到CLI队列
     → 避免系统崩溃

  3. 子Agent执行失败
     → 自动降级到CLI队列
     → 任务不会丢失

  4. 用户配置禁用
     → 尊重用户选择
     → 使用CLI队列

降级原则:
  ✅ 功能完整性 - 所有编码任务都能完成
  ✅ 数据不丢失 - 降级过程数据安全
  ✅ 用户友好 - 批量任务时友好提示
  ✅ 透明处理 - 小任务时完全透明
```

### 子Agent调用规范

#### grounded-theory-coder

**子Agent类型**: specialized subagent

**能力**: 开放编码、轴心编码、选择式编码

**调用格式**:
```yaml
子Agent Prompt模板:

  任务: 扎根理论开放编码

  文件: {file_path}
  数据长度: {data_length} 字符

  要求:
    1. 逐行/逐句编码
    2. 不预设结论
    3. 紧贴数据
    4. 识别概念和范畴

  禁止:
    ❌ 预设结论
    ❌ 脱离数据编码
    ❌ 编码无理论依据
    ❌ 忽视负面案例

  返回格式:
    {
      "codes": [
        {"text": "...", "code": "...", "memo": "..."}
      ],
      "concepts": [...],
      "categories": [...],
      "quality": 5
    }
```

#### 批量编码实现

```python
def batch_code_with_subagents(data_files):
    """批量编码使用子Agent并行"""

    # 第一步：检查可用性
    availability = check_subagent_availability()

    if not availability["available"]:
        # 子Agent不可用，降级到CLI队列
        notify_fallback(availability["reason"], len(data_files))
        return execute_with_cli_queue(data_files)

    # 第二步：启动子Agent
    subagents = []
    for file_path in data_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data_content = f.read()

        subagent_prompt = f"""
        # 扎根理论编码任务

        文件: {file_path}
        数据长度: {len(data_content)} 字符

        {data_content[:1000]}...  # 前1000字符

        请进行开放编码，返回JSON格式结果。
        """

        subagent = Agent(
            subagent_type="grounded-theory-coder",
            prompt=subagent_prompt,
            run_in_background=True  # 并行执行
        )
        subagents.append(subagent)

    # 第三步：收集结果
    results = []
    for subagent in subagents:
        try:
            result = await subagent
            results.append(result)
        except Exception as e:
            logger.error(f"子Agent失败: {e}")
            # 降级到CLI队列处理这个文件
            result = code_single_file_with_cli(file_path)
            results.append(result)

    # 第四步：整合结果
    integrated = integrate_coding_results(results)

    return integrated
```

#### 结果整合机制

```python
def integrate_coding_results(subagent_results):
    """整合多个子Agent的编码结果"""

    # 第一步：收集所有编码
    all_codes = []
    for result in subagent_results:
        all_codes.extend(result["codes"])

    # 第二步：合并相似概念
    merged_concepts = merge_similar_concepts(
        [r["concepts"] for r in subagent_results]
    )

    # 第三步：识别高频概念
    concept_frequency = calculate_frequency(
        [c for result in subagent_results
         for c in result["concepts"]]
    )

    # 第四步：生成综合报告
    integrated = {
        "total_files": len(subagent_results),
        "total_codes": len(all_codes),
        "unique_concepts": len(merged_concepts),
        "concept_frequency": concept_frequency,
        "emerging_categories": identify_emerging(merged_concepts),
        "quality_score": average([r["quality"] for r in subagent_results])
    }

    return integrated
```

#### 用户控制（可选）

**强制使用子Agent**:
```
"使用子Agent并行处理这10个访谈文件"
```

**强制使用CLI队列**:
```
"使用CLI队列依次处理这10个文件"
```

**自动选择（默认）**:
```
"处理这10个访谈文件"
→ 系统自动选择最优方式
```

### 自动激活条件

当满足以下任一条件时，技能自动激活任务队列模式：

```yaml
激活条件:
  - 任务估计时间 > 3小时
  - 包含3个以上独立子任务
  - 需要多阶段验证
  - 用户明确要求"分解任务"
```

### 扎根理论分析自动分解示例

**小批量（CLI队列）**:
```yaml
用户请求: "分析这3个访谈资料，生成扎根理论"

自动执行:
  模式: CLI队列（串行）

  Task 1: 编码interview1.txt
  Task 2: 编码interview2.txt
  Task 3: 编码interview3.txt

  总时间: 90分钟
```

**大批量（子Agent并行）**:
```yaml
用户请求: "分析这20个访谈资料，生成扎根理论"

自动执行:
  模式: 子Agent并行（自动选择）

  友好提示:
    ℹ️  检测到批量任务（20个文件）
    ℹ️  将使用并行处理以提升效率
    ℹ️  预计时间: 约35分钟（而非10小时）

  执行:
    启动20个grounded-theory-coder子Agent
    并行处理所有文件
    整合编码结果

  总时间: 35分钟
  加速比: 17x ⚡
```

### 持久化架构

```yaml
存储位置:
  Level 1: .tasks/session-{uuid}.yaml
    - 会话级状态
    - 编码进度
    - 范畴清单

  Level 2: .tasks/project-state.yaml
    - 项目级状态
    - 理论发展
    - 饱和度状态

  Level 3: experience/patterns.md
    - 学习级知识
    - 编码模式
    - 理论生成经验
```

### 状态文件示例

```yaml
# .tasks/session-gt-abc123.yaml

session:
  id: "abc123"
  skill: "grounded-theory-expert"
  start_time: "2026-03-08T10:00:00Z"

user_request:
  original: "分析这些访谈资料，生成扎根理论"
  data_files: ["interview1.txt", "interview2.txt", ...]

task_queue:
  - id: "1.1"
    name: "逐行编码前20份资料"
    status: "completed"
    output: "codes/open-codes-phase1.md"
    validation: "passed"

  - id: "1.2"
    name: "识别初始范畴"
    status: "in_progress"

encoding_progress:
  total_files: 50
  encoded_files: 20
  codes_count: 156
  categories_count: 12

categories:
  - name: "权力结构"
    properties: ["资源控制", "决策权"]
    dimension: "正式 vs 非正式"
  - name: "抵抗策略"
    properties: ["公开反对", "消极抵抗"]
    dimension: "个体 vs 集体"

memos:
  - "编码发现初始范畴间的权力动态关系"
  - "需要进一步探索非正式权力机制"
```

## 🎯 CLI模型驱动执行

### 核心原则

```yaml
✅ 正确做法 - 直接编码:
  - "逐行阅读这份访谈，进行开放编码"
  - "识别这些编码中的范畴"
  - "建立范畴间的关系"

❌ 错误做法 - 生成脚本:
  - "生成编码脚本"
  - "创建coding.py并执行"
```

### 扎根理论工具链

```yaml
质性分析工具:
  - 手工编码（推荐初学者）
  - NVivo（高级分析）
  - ATLAS.ti（网络可视化）
  - MAXQDA（混合方法）

CLI集成:
  - 逐行处理文本
  - 实时编码
  - 动态范畴管理
  - 备忘录同步
```

## 🧠 自迭代与学习机制

### 经验记录

```yaml
session:
  id: "uuid"
  date: "2026-03-08"
  task_type: "扎根理论分析"
  data_type: "访谈资料"

approach:
  coding_method: "逐行编码"
  categories_identified: 12
  core_category: "权力重构"

results:
  theory: "组织变革中的权力重构理论"
  quality: "高"

lessons:
  successful_patterns:
    - "持续比较法很有效"
    - "备忘录帮助理论整合"

  improvement_areas:
    - "编码初期应更开放"
    - "需要更早识别负面案例"
```

### 编码模式识别

```yaml
高频模式:
  1. 开放编码模式
     - 逐行编码
     - 持续比较
     - 范畴归纳

  2. 轴心编码模式
     - 范畴联结
     - 维度识别
     - 关系建立

  3. 理论生成模式
     - 核心范畴识别
     - 故事线构建
     - 理论整合
```

## ✅ 完成度验证清单

### 必须完成（100%）

- [ ] **六大禁止原则全部遵守**
  - [ ] 编码前未预设结论
  - [ ] 每个编码有原始引文
  - [ ] 编码有理论依据
  - [ ] 负面案例被编码
  - [ ] 追求理论饱和而非编码数量
  - [ ] 编码标准一致

- [ ] **编码质量**
  - [ ] 所有资料已编码
  - [ ] 编码本完整
  - [ ] 备忘录完整

- [ ] **范畴质量**
  - [ ] 范畴有定义
  - [ ] 范畴有属性
  - [ ] 范畴有维度

- [ ] **理论质量**
  - [ ] 核心范畴识别
  - [ ] 理论整合
  - [ ] 饱和度检验
  - [ ] 故事线连贯

### 质量评估

| 维度 | 优秀(5) | 良好(4) | 合格(3) | 需改进(<3) |
|------|----------|----------|----------|-------------|
| **编码扎根性** | 完全扎根 | 主要扎根 | minor脱离 | 严重脱离 |
| **编码系统性** | 高度系统 | 较系统 | minor碎片 | 严重碎片 |
| **范畴发展** | 完整清晰 | 主要完整 | minor缺失 | 严重缺失 |
| **理论连贯** | 高度连贯 | 较连贯 | minor断裂 | 严重断裂 |
| **饱和度** | 完全饱和 | 基本饱和 | minor不足 | 严重不足 |
| **负面案例** | 全部考虑 | 主要考虑 | minor忽视 | 严重忽视 |

**及格线**: 每维度≥3分

## 📚 渐进式加载结构

### 第一层：核心执行规则（本文件）

**技能激活时必读**，确保任务高质量执行：
- ⚠️ 六大绝对禁止原则
- 📋 任务分解规则
- ✅ 完成度验证清单

### 第二层：方法论文档（references/）

按需加载，深化方法论理解：

**classic-literature.md**: 扎根理论经典文献
- Glaser & Strauss (1967)
- Strauss & Corbin (1990)
- Charmaz (2006)
- 权威定义与应用范围

**long-term-tasks.md**: 长时扎根理论研究
- 3-6个月完整研究
- 分阶段指南
- 验证清单

### 第三层：案例文档（cases/）

实战示范与警示：

**positive/**: 正确示范
- case-001: 扎根理论完整研究
- case-002: 理论饱和度检验

**negative/**: 错误警示
- case-001: 编码前预设结论
- case-002: 忽视负面案例

---

**使用方式**:
- 对话中直接使用："使用扎根理论分析XX资料"
- 长时研究：技能会自动分解任务
- 质量保证：六大禁止原则+完成度清单

**版本历史**:
| 版本 | 日期 | 变更 |
|------|------|------|
| 5.0.0-cli-native | 2026-03-08 | CLI原生集成+自迭代机制 |
| 5.0.0 | - | 基础升级（待追溯） |
| 2.0.0 | 2026-03-05 | 初始模板 |

**相关技能**:
- data-analysis-expert: 定量数据分析
- qca-analysis-expert: 集合论分析
- grounded-theory-coding: 扎根理论编码（金标准）
