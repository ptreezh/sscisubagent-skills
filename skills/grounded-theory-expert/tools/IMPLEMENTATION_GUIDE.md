# 迭代控制器与分批渐次分析机制

**版本**: 2.0.0  
**日期**: 2026-03-07  
**作者**: grounded-theory-expert

---

## 📋 目录

1. [概述](#概述)
2. [核心组件](#核心组件)
3. [状态文件格式设计](#状态文件格式设计)
4. [分批分析流程](#分批分析流程)
5. [恢复机制](#恢复机制)
6. [使用示例](#使用示例)
7. [故障排除](#故障排除)

---

## 概述

### 解决的问题

1. **大批量数据处理**: 用户分析《西游记》100 回，但原 skill 只分析了前 12 个文件就宣布结束
2. **中断恢复**: 分析过程中断后无法从断点继续
3. **中间状态持久化**: 没有保存中间分析结果
4. **完整性检查**: 无法确认是否所有文件都已分析

### 核心功能

| 功能 | 描述 | 实现文件 |
|------|------|----------|
| 迭代控制 | 最大迭代次数、收敛检测、质量评审、自我校对 | `iteration_controller.py` |
| 分批分析 | 分批加载、渐次整合、中间状态保存 | `batch_analyzer.py` |
| 状态持久化 | JSON 格式状态文件、支持恢复 | 两个组件都实现 |
| 完整性检查 | 检查所有文件是否分析完成 | `batch_analyzer.py` |

---

## 核心组件

### 1. IterationController（迭代控制器）

**核心类**: `IterationController`

**功能**:
- 迭代循环控制
- 质量评审（46 个检查点）
- 自我校对（18 个策略）
- 收敛检测
- 状态持久化

**关键参数**:
```python
IterationController(
    max_iterations=10,           # 最大迭代次数
    convergence_threshold=85.0,  # 收敛阈值（%）
    min_improvement=5.0,         # 最小改进率（%）
    early_stopping_patience=3    # 提前停止耐心值
)
```

**迭代循环流程**:
```
执行分析 → 质量评审 → 判断通过？
    ↓ 否
自我校对 → 应用修正 → 重新分析
    ↓ 是
检查收敛 → 达到阈值？→ 结束迭代
```

### 2. BatchAnalyzer（分批分析器）

**核心类**: `BatchAnalyzer`

**功能**:
- 分批加载文件
- 分析当前批次
- 合并到累积状态
- 保存中间状态
- 最终整合
- 理论饱和度检验

**关键参数**:
```python
BatchAnalyzer(
    data_dir="./data",           # 数据目录
    batch_size=10,               # 每批文件数
    state_dir="./state",         # 状态保存目录
    log_dir="./logs"             # 日志目录
)
```

**分批分析流程**:
```
for batch in 1..N:
    1. 加载当前批次文件
    2. 分析当前批次
    3. 合并到累积状态
    4. 保存中间状态
5. 最终整合
6. 理论饱和度检验
```

---

## 状态文件格式设计

### 1. 迭代状态文件

**文件路径**: `./state/iteration_state/iteration_state.json`

**结构**:
```json
{
  "controller_config": {
    "max_iterations": 10,
    "convergence_threshold": 85.0,
    "min_improvement": 5.0,
    "early_stopping_patience": 3
  },
  "current_state": {
    "current_phase": 2,
    "current_iteration": 5,
    "status": "running",
    "timestamp": "2026-03-07T10:30:00"
  },
  "iteration_history": [
    {
      "phase": 2,
      "iteration": 1,
      "status": "running",
      "quality_score": 72.5,
      "improvement_rate": 0.0,
      "timestamp": "2026-03-07T10:20:00",
      "checks_passed": 3,
      "checks_failed": 1,
      "corrections_applied": ["SC-006"],
      "log_file": "./logs/iterations/..."
    }
  ],
  "quality_history": [72.5, 78.0, 83.5, 86.0, 87.5]
}
```

**字段说明**:
- `controller_config`: 迭代控制器配置
- `current_state`: 当前迭代状态
- `iteration_history`: 历史迭代记录
- `quality_history`: 质量分数历史（用于收敛检测）

### 2. 分批分析状态文件

**文件路径**: `./state/batch_analysis/batch_analysis_state.json`

**结构**:
```json
{
  "metadata": {
    "version": "1.0",
    "created_at": "2026-03-07T10:00:00",
    "data_dir": "./data",
    "batch_size": 10,
    "file_pattern": "*.txt"
  },
  "progress": {
    "total_files": 100,
    "total_batches": 10,
    "completed_batches": 3,
    "current_batch": 3,
    "status": "in_progress"
  },
  "cumulative_state": {
    "concepts": ["concept_1", "concept_2", ...],
    "categories": {
      "category_A": {
        "properties": ["prop1", "prop2"],
        "dimensions": ["dim1", "dim2"]
      }
    },
    "relationships": [
      {"from": "A", "to": "B", "type": "causal"}
    ],
    "memos": [
      {"id": "memo_1", "content": "...", "timestamp": "..."}
    ]
  },
  "batch_history": [
    {
      "batch_number": 1,
      "file_count": 10,
      "files": ["chapter_001.txt", ...],
      "status": "completed",
      "start_time": "2026-03-07T10:00:00",
      "end_time": "2026-03-07T10:05:00",
      "result_file": "./state/batch_1_result.json",
      "error_message": null
    }
  ]
}
```

**字段说明**:
- `metadata`: 元数据
- `progress`: 分析进度
- `cumulative_state`: 累积分析状态（概念、范畴、关系、备忘录）
- `batch_history`: 批次分析历史

### 3. 进度文件（快速查询）

**文件路径**: `./state/batch_analysis/analysis_progress.json`

**结构**:
```json
{
  "current_batch": 3,
  "total_batches": 10,
  "completed_files": 30,
  "total_files": 100,
  "progress_percentage": 30.0,
  "status": "in_progress",
  "timestamp": "2026-03-07T10:05:00"
}
```

### 4. 批次结果文件

**文件路径**: `./state/batch_analysis/batch_{N}_result.json`

**结构**:
```json
{
  "batch_number": 1,
  "files_analyzed": 10,
  "timestamp": "2026-03-07T10:05:00",
  "open_coding": {
    "concepts": ["concept_1_1", "concept_1_2", ...],
    "codes": ["code_1_1", "code_1_2", ...]
  },
  "axial_coding": {
    "categories": {
      "category_1_A": {
        "properties": ["prop1", "prop2"],
        "dimensions": ["dim1", "dim2"]
      }
    }
  },
  "relationships": [...],
  "memos": [...]
}
```

### 5. 最终整合结果

**文件路径**: `./state/batch_analysis/final_integration_result.json`

**结构**:
```json
{
  "timestamp": "2026-03-07T12:00:00",
  "phase": "final_integration",
  "summary": {
    "total_concepts": 350,
    "total_categories": 25,
    "total_relationships": 80,
    "total_memos": 50,
    "total_files_analyzed": 100,
    "total_batches": 10
  },
  "concepts": [...],
  "categories": {...},
  "relationships": [...],
  "memos": [...],
  "integration_notes": [
    "整合了 10 个批次的分析结果",
    "共分析 100 个文件",
    "识别出 350 个概念",
    "形成 25 个范畴",
    "建立 80 条关系"
  ]
}
```

### 6. 饱和度检验结果

**文件路径**: `./state/batch_analysis/saturation_test_result.json`

**结构**:
```json
{
  "timestamp": "2026-03-07T12:05:00",
  "phase": "saturation_test",
  "overall_saturation": 92.5,
  "status": "saturated",
  "by_dimension": {
    "concept_saturation": {
      "score": 95,
      "status": "saturated",
      "existing_concepts": 320,
      "new_concepts": 5,
      "new_concept_rate": 0.016
    },
    "category_saturation": {
      "score": 90,
      "status": "saturated",
      "total_categories": 25,
      "new_categories": 0,
      "hierarchy_complete": true,
      "properties_developed": true,
      "dimensions_developed": true
    },
    "relationship_saturation": {...},
    "proposition_saturation": {...}
  },
  "recommendations": [
    "理论已达到饱和状态，可以结束数据收集并撰写最终报告"
  ],
  "summary": "理论饱和度：92.5% - saturated"
}
```

---

## 分批分析流程

### 完整流程图

```
开始
  ↓
初始化 BatchAnalyzer
  ↓
检查是否可以恢复？→ YES → 加载状态，从断点继续
  ↓ NO
for batch = 1 to N:
  ├─ 加载当前批次文件 (load_batch)
  ├─ 分析当前批次 (analyze_batch)
  ├─ 合并到累积状态 (merge_to_cumulative)
  ├─ 保存中间状态 (save_state)
  └─ 记录批次历史
  ↓
所有批次完成？
  ↓ YES
最终整合 (final_integration)
  ↓
理论饱和度检验 (saturation_test)
  ↓
完整性检查 (check_completeness)
  ↓
输出最终结果
  ↓
结束
```

### 详细步骤说明

#### 步骤 1: 初始化

```python
analyzer = BatchAnalyzer(
    data_dir="./data/chapters",    # 《西游记》100 回目录
    batch_size=10,                  # 每批 10 回
    state_dir="./state",
    log_dir="./logs"
)

# 初始化后:
# - total_files = 100
# - total_batches = 10
# - current_batch = 0
```

#### 步骤 2: 分批分析

```python
# 批次 1: 分析第 1-10 回
files = analyzer.load_batch(1)  # ['chapter_001.txt', ..., 'chapter_010.txt']
result = analyzer.analyze_batch(files, 1)
analyzer.merge_to_cumulative(result, 1)
analyzer.save_state(1, 'completed')

# 累积状态更新:
# - concepts: 0 → 35
# - categories: 0 → 3
# - completed_batches: 0 → 1
```

#### 步骤 3: 渐次整合

每批分析后都合并到累积状态：

```python
def merge_to_cumulative(self, result, batch_number):
    # 合并概念
    self.cumulative_state.concepts.update(new_concepts)
    
    # 合并范畴
    for cat_name, cat_data in batch_categories.items():
        if cat_name not in self.cumulative_state.categories:
            self.cumulative_state.categories[cat_name] = cat_data
        else:
            # 更新现有范畴的属性和维度
            ...
    
    # 合并关系和备忘录
    ...
```

#### 步骤 4: 中间状态持久化

每批完成后保存状态：

```python
analyzer.save_state(batch_num=1, status='completed')
```

保存到 `batch_analysis_state.json`，包含：
- 当前进度
- 累积状态（概念、范畴、关系、备忘录）
- 批次历史

#### 步骤 5: 最终整合

所有批次完成后：

```python
final_result = analyzer.final_integration()
```

整合内容：
- 所有概念去重
- 所有范畴整合
- 所有关系网络
- 所有备忘录

#### 步骤 6: 理论饱和度检验

```python
saturation_result = analyzer.saturation_test()
```

检验维度：
- 概念饱和度
- 范畴饱和度
- 关系饱和度
- 命题饱和度
- 整体饱和度

#### 步骤 7: 完整性检查

```python
completeness = analyzer.check_completeness()
```

检查内容：
- 是否所有文件都分析了
- 是否有遗漏的文件
- 完整性百分比

---

## 恢复机制

### 恢复场景

1. **计划内中断**: 用户主动暂停（Ctrl+C）
2. **计划外中断**: 系统崩溃、断电、网络中断
3. **超时中断**: LLM API 超时

### 恢复流程

```
重新启动分析
  ↓
检查状态文件是否存在？
  ↓ YES
读取 batch_analysis_state.json
  ↓
解析进度信息:
  - completed_batches: 3
  - current_batch: 3
  - cumulative_state: {...}
  ↓
用户确认恢复？→ YES
  ↓
从 batch 4 继续分析
  ↓
加载已保存的累积状态
  ↓
继续分析剩余批次
```

### 恢复代码示例

```python
# 创建分析器
analyzer = BatchAnalyzer(
    data_dir="./data/chapters",
    batch_size=10
)

# 检查是否可以恢复
if analyzer.can_resume():
    resume_info = analyzer.get_resume_info()
    print(f"发现未完成的分析:")
    print(f"  已完成：{resume_info['completed_batches']}/{resume_info['total_batches']}")
    print(f"  概念数：{resume_info['concepts_count']}")
    print(f"  范畴数：{resume_info['categories_count']}")
    
    # 恢复分析
    result = analyzer.analyze_all_batches(resume=True)
else:
    # 从头开始
    result = analyzer.analyze_all_batches(resume=False)
```

### 命令行恢复

```bash
# 从中断处恢复
python analyze.py ./data/chapters/ --resume

# 非交互模式（自动恢复）
python analyze.py ./data/chapters/ --resume --non-interactive
```

### 状态文件完整性保护

1. **原子写入**: 先写入临时文件，再重命名
2. **备份机制**: 保存前备份旧状态
3. **校验和**: 可选添加 CRC 校验

---

## 使用示例

### 示例 1: 分析《西游记》100 回

```bash
# 准备数据
mkdir ./data/chapters
# 将 100 回文本文件放入目录

# 执行分批分析（每批 10 回）
python analyze.py ./data/chapters/ --batch --batch-size 10

# 输出:
# ================================================================================
# 扎根理论分析 v2.0
# ================================================================================
# 分析类型：batch
# 文件数量：100
# ================================================================================
#
# 📊 开始分批分析
#    总文件数：100
#    批次大小：10
#    总批次数：10
#
# [分析过程...]
#
# ================================================================================
# 分析完成！
# ================================================================================
# 总文件数：100
# 总批次数：10
# 完成批次：10
# 概念数量：350
# 范畴数量：25
# 理论饱和度：92.5%
# 饱和度状态：saturated
```

### 示例 2: 中断后恢复

```bash
# 第一次运行（中断）
python analyze.py ./data/chapters/ --batch
# Ctrl+C 中断于批次 3

# 第二次运行（恢复）
python analyze.py ./data/chapters/ --resume --non-interactive

# 输出:
# 📌 发现未完成的分析:
#    已完成批次：3/10
#    概念数量：105
#    范畴数量：8
# 从批次 4 恢复分析
```

### 示例 3: 自定义迭代参数

```bash
python analyze.py ./data/chapters/ \
    --batch \
    --batch-size 15 \
    --max-iterations 15 \
    --convergence 90.0 \
    --output ./output
```

### 示例 4: Python API 调用

```python
from analyze import SkillExpert

# 创建专家实例
expert = SkillExpert(
    working_dir='./session',
    batch_size=10,
    max_iterations=10,
    convergence_threshold=85.0
)

# 执行分批分析
result = expert.analyze(
    data='./data/chapters',
    analysis_type='batch',
    resume=False
)

# 获取进度
progress = expert.get_progress()
print(f"进度：{progress['batch_analysis']['progress_percentage']}%")
```

---

## 故障排除

### 问题 1: 状态文件损坏

**症状**: 恢复时提示"状态文件损坏"

**解决**:
```bash
# 删除损坏的状态文件，从头开始
rm -rf ./state/batch_analysis/
python analyze.py ./data/chapters/ --batch
```

### 问题 2: 批次分析卡住

**症状**: 某个批次长时间无响应

**诊断**:
```bash
# 查看日志
tail -f ./logs/batch_analysis/batch_analysis_*.log
```

**解决**:
```bash
# 跳过当前批次，继续下一批
# 手动编辑状态文件，增加 current_batch
```

### 问题 3: 收敛困难

**症状**: 迭代次数达到上限仍未收敛

**解决**:
```bash
# 降低收敛阈值
python analyze.py ./data/chapters/ --convergence 80.0

# 或增加最大迭代次数
python analyze.py ./data/chapters/ --max-iterations 20
```

### 问题 4: 内存不足

**症状**: 分析大文件时内存溢出

**解决**:
```bash
# 减小批次大小
python analyze.py ./data/chapters/ --batch-size 5
```

---

## 附录：文件清单

### 核心文件

| 文件 | 行数 | 功能 |
|------|------|------|
| `tools/analyze.py` | ~500 | 主分析入口（集成版） |
| `tools/iteration_controller.py` | ~700 | 迭代控制器 |
| `tools/batch_analyzer.py` | ~650 | 分批分析器 |
| `tools/assess-saturation.py` | ~200 | 饱和度评估（已有） |

### 状态文件

| 文件 | 格式 | 说明 |
|------|------|------|
| `iteration_state.json` | JSON | 迭代状态 |
| `batch_analysis_state.json` | JSON | 分批分析状态 |
| `analysis_progress.json` | JSON | 快速进度查询 |
| `batch_{N}_result.json` | JSON | 批次分析结果 |
| `final_integration_result.json` | JSON | 最终整合结果 |
| `saturation_test_result.json` | JSON | 饱和度检验结果 |

### 日志文件

| 文件 | 说明 |
|------|------|
| `iteration_*.log` | 迭代日志 |
| `batch_analysis_*.log` | 分批分析日志 |
| `quality_review_*.log` | 质量评审日志 |
| `self_correction_*.log` | 自我校对日志 |

---

**实现完成！现在可以处理大批量扎根理论分析任务，支持中断恢复和完整性检查。**
