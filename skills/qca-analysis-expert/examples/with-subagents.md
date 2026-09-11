# 批量QCA案例并行分析 - 子Agent示例

**使用子Agent并行处理多个案例的QCA集合论分析**

---

## 📋 场景描述

**任务**: 对10个国家的民主转型进行QCA分析

**案例列表**:
```
data/cases/
├── country_01.csv
├── country_02.csv
├── country_03.csv
├── country_04.csv
├── country_05.csv
├── country_06.csv
├── country_07.csv
├── country_08.csv
├── country_09.csv
└── country_10.csv
```

**变量定义**:
- **结果**: 民主转型 (成功/失败)
- **条件**: 经济发展、中产阶级、外部压力、公民社会、国家能力

---

## 🚀 两种执行方式对比

### 方式A: CLI任务队列（串行）

```yaml
用户请求: "对这10个国家的民主转型进行QCA分析"

系统行为:
  模式: CLI队列（自动选择）

  执行流程:
    Task 1: 分析 country_01.csv (60分钟)
      - 校准条件
      - 构建真值表
      - 必要性/充分性分析
    Task 2: 分析 country_02.csv (60分钟)
    ...
    Task 10: 分析 country_10.csv (60分钟)

  总时间: 600分钟（10小时）

  用户看到:
    ✅ 正在分析 country_01.csv...
    ✅ 正在分析 country_02.csv...
    ...
    ✅ 完成！总时间: 10小时
```

### 方式B: 子Agent并行（批量）

```yaml
用户请求: "对这10个国家的民主转型进行QCA分析"

系统行为:
  模式: 子Agent并行（自动选择）

  友好提示（仅第一次）:
    ℹ️  检测到批量QCA分析任务（10个案例）
    ℹ️  将使用并行处理以提升效率
    ℹ️  预计时间: 约65分钟（而非10小时）

  执行流程:
    启动10个qca-analyzer子Agent
    ├── 子Agent1: 分析 country_01.csv
    │   - 理论驱动校准
    │   - 真值表构建
    │   - 布尔最小化
    ├── 子Agent2: 分析 country_02.csv
    ├── ...
    └── 子Agent10: 分析 country_10.csv

    所有子Agent并行执行 ⚡

    整合阶段:
      - 合并所有案例的真值表
      - 跨案例必要性分析
      - 跨案例充分性分析
      - 识别共性因果路径

  总时间: 65分钟
  加速比: 9.2x ⚡

  用户看到:
    ✅ 正在并行分析10个案例...
    ✅ country_01.csv 分析完成 ✅
    ✅ country_02.csv 分析完成 ✅
    ...
    ✅ 跨案例整合完成！
    ✅ 总时间: 65分钟
    ✅ 加速: 9.2x ⚡
```

---

## 📊 结果示例

### 案例分析结果整合

```json
{
  "total_cases": 10,
  "successful": 10,
  "failed": 0,

  "conditions": ["经济发展", "中产阶级", "外部压力", "公民社会", "国家能力"],

  "necessity_analysis": {
    "经济发展": {
      "consistency": 0.92,
      "coverage": 0.78,
      "necessary": true
    },
    "公民社会": {
      "consistency": 0.88,
      "coverage": 0.65,
      "necessary": false
    }
  },

  "sufficiency_analysis": {
    "complex_solution": "经济发展*中产阶级*公民社会 + ~国家能力*外部压力",
    "intermediate_solution": "经济发展*公民社会 + 外部压力",
    "parsimonious_solution": "经济发展 + 外部压力",

    "consistency": 0.85,
    "coverage": 0.82,

    "paths": [
      {
        "path": "经济发展*中产阶级*公民社会",
        "consistency": 0.88,
        "coverage": 0.45,
        "cases": ["country_01", "country_03", "country_05", "country_07"]
      },
      {
        "path": "~国家能力*外部压力",
        "consistency": 0.82,
        "coverage": 0.38,
        "cases": ["country_02", "country_04", "country_09"]
      }
    ]
  },

  "calibration_quality": {
    "theory_driven": 10,
    "mechanical": 0,
    "quality_score": 5.0
  },

  "case_depth": {
    "total_cases": 10,
    "cases_studied": 10,
    "deep_analysis_cases": 10,
    "coverage": 100
  },

  "robustness_checks": {
    "parameter_sensitivity": "passed",
    "calibration_sensitivity": "passed",
    "case_sensitivity": "passed",
    "overall": "robust"
  }
}
```

### 关键发现示例

```yaml
因果路径分析:

路径1: 经济发展 × 中产阶级 × 公民社会
  一致性: 0.88
  原始覆盖度: 0.45
  唯一覆盖度: 0.42

  案例归属:
    - country_01: 瑞典 (完全隶属)
    - country_03: 丹麦 (完全隶属)
    - country_05: 芬兰 (完全隶属)
    - country_07: 挪威 (完全隶属)

  机制解释:
    "经济发展提供物质基础，
     中产阶级推动改革，
     公民社会组织行动，
     三者结合触发民主转型"

路径2: ~国家能力 × 外部压力
  一致性: 0.82
  原始覆盖度: 0.38
  唯一覆盖度: 0.35

  案例归属:
    - country_02: 韩国 (1987)
    - country_04: 智利 (1989)
    - country_09: 南非 (1994)

  机制解释:
    "国家能力弱化 + 外部压力增强
     导致威权政权崩溃，
     为民主转型创造机会"
```

---

## 🎯 使用方式

### 自动模式（推荐）

```
你: "对data/cases/下的所有国家进行QCA分析"

系统:
  - 自动检测到10个案例
  - 自动选择子Agent并行模式
  - 显示友好提示
  - 65分钟后完成
```

### 手动指定子Agent

```
你: "使用子Agent并行分析这些国家的民主转型"

系统:
  - 强制使用子Agent并行
  - 不进行自动决策
  - 65分钟后完成
```

### 手动指定CLI队列

```
你: "使用CLI队列依次分析每个国家"

系统:
  - 强制使用CLI队列
  - 依次处理每个案例
  - 10小时后完成
```

---

## ✅ 完成后的下一步

批量QCA分析完成后，自动进入深入分析阶段：

```yaml
阶段2: 案例深入比较
  - 任务: 比较不同路径的案例
  - 输入: 因果路径、案例归属
  - 输出: 跨案例比较报告

阶段3: 机制提炼
  - 任务: 提炼中层理论机制
  - 输入: 跨案例比较
  - 输出: 机制命题集

阶段4: 稳健性检验
  - 任务: 检验结果稳健性
  - 输入: 当前解
  - 输出: 稳健性报告
```

---

## 💡 关键洞察

### 1. 并行QCA分析的优势

```yaml
传统方式（CLI队列）:
  - 依次分析
  - 总时间: 10小时
  - 优点: 简单
  - 缺点: 慢

并行方式（子Agent）:
  - 同时分析
  - 总时间: 65分钟
  - 优点: 快（9.2x加速）
  - 缺点: 无
```

### 2. 质量保证

```yaml
子AgentQCA分析质量:
  - 每个子Agent独立分析
  - 理论驱动校准
  - 避免主观偏见
  - 质量评分: 5.0/5

整合策略:
  - 跨案例必要性分析
  - 跨案例充分性分析
  - 识别共性因果路径
  - 发现案例异质性
```

### 3. 适用场景

```yaml
最适合子Agent并行的场景:
  ✅ 大量案例（>5个）
  ✅ 案例相互独立
  ✅ 需要快速分析
  ✅ 比较案例研究

不适合的场景:
  ❌ 少量案例（<3个）
  ❌ 案例有强依赖
  ❌ 需要深度单案例研究
  ❌ 复杂理论建构
```

---

## 🎉 总结

**使用子Agent并行批量QCA分析**:
- ⚡ 9.2x加速（10个案例：10小时→65分钟）
- ✅ 质量保证（5.0/5评分）
- 🎯 自动决策（系统自动选择最优方式）
- 🛡️ 优雅降级（子Agent不可用时自动降级）
- 💡 用户友好（批量任务时友好提示）

**立即体验批量QCA分析的威力！** ⚡
