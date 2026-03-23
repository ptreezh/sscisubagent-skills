# 批量扎根理论编码 - 子Agent并行示例

**使用子Agent并行处理多个访谈文件的扎根理论编码**

---

## 📋 场景描述

**任务**: 对10个访谈文件进行开放编码

**文件列表**:
```
data/interviews/
├── participant_01.txt
├── participant_02.txt
├── participant_03.txt
├── participant_04.txt
├── participant_05.txt
├── participant_06.txt
├── participant_07.txt
├── participant_08.txt
├── participant_09.txt
└── participant_10.txt
```

---

## 🚀 两种执行方式对比

### 方式A: CLI任务队列（串行）

```yaml
用户请求: "对data/interviews/下的10个访谈进行编码"

系统行为:
  模式: CLI队列（自动选择）

  执行流程:
    Task 1: 编码 participant_01.txt (30分钟)
    Task 2: 编码 participant_02.txt (30分钟)
    Task 3: 编码 participant_03.txt (30分钟)
    ...
    Task 10: 编码 participant_10.txt (30分钟)

  总时间: 300分钟（5小时）

  用户看到:
    ✅ 正在编码 participant_01.txt...
    ✅ 正在编码 participant_02.txt...
    ...
    ✅ 完成！总时间: 5小时
```

### 方式B: 子Agent并行（批量）

```yaml
用户请求: "对data/interviews/下的10个访谈进行编码"

系统行为:
  模式: 子Agent并行（自动选择）

  友好提示（仅第一次）:
    ℹ️  检测到批量任务（10个访谈文件）
    ℹ️  将使用并行处理以提升效率
    ℹ️  预计时间: 约35分钟（而非5小时）

  执行流程:
    启动10个grounded-theory-coder子Agent
    ├── 子Agent1: 编码 participant_01.txt
    ├── 子Agent2: 编码 participant_02.txt
    ├── ...
    └── 子Agent10: 编码 participant_10.txt

    所有子Agent并行执行 ⚡

  总时间: 35分钟
  加速比: 8.6x ⚡

  用户看到:
    ✅ 正在并行处理10个访谈文件...
    ✅ participant_01.txt 完成 ✅
    ✅ participant_02.txt 完成 ✅
    ...
    ✅ 所有文件完成！总时间: 35分钟
    ✅ 加速: 8.6x ⚡
```

---

## 📊 结果示例

### 编码结果整合

```json
{
  "total_files": 10,
  "successful": 10,
  "failed": 0,

  "total_codes": 247,
  "codes_per_file": 24.7,

  "unique_concepts": 38,
  "concept_frequency": {
    "工作灵活性": 25,
    "社交需求": 18,
    "时间管理": 15,
    "工作生活边界": 12,
    "远程工作挑战": 10
  },

  "emerging_categories": [
    {
      "name": "数字时代的边界重构",
      "frequency": 8,
      "examples": ["时间边界", "空间边界", "心理边界"]
    },
    {
      "name": "远程工作的双面性",
      "frequency": 6,
      "examples": ["灵活性", "孤立感"]
    }
  ],

  "quality_score": 4.8,
  "saturation_status": "接近饱和",
  "next_steps": [
    "1. 进行轴心编码",
    "2. 识别核心范畴",
    "3. 建立范畴联系"
  ]
}
```

### 高频概念示例

```yaml
Top 5 概念:

1. 工作灵活性 (25次)
   participant_01: "可以灵活安排工作时间"
   participant_03: "自主决定工作节奏"
   participant_05: "工作地点自由选择"
   ...

2. 社交需求 (18次)
   participant_02: "想念办公室的同事"
   participant_07: "缺乏面对面交流"
   participant_09: "需要社交互动"
   ...

3. 时间管理 (15次)
   participant_01: "省去通勤时间"
   participant_04: "更好的时间分配"
   participant_08: "自主控制工作节奏"
   ...

4. 工作生活边界 (12次)
   participant_03: "工作和生活难以区分"
   participant_06: "需要建立边界"
   participant_10: "边界模糊问题"
   ...

5. 远程工作挑战 (10次)
   participant_02: "容易分心"
   participant_05: "家庭干扰"
   participant_08: "自律要求高"
   ...
```

---

## 🎯 使用方式

### 自动模式（推荐）

```
你: "对data/interviews/下的所有访谈文件进行编码"

系统:
  - 自动检测到10个文件
  - 自动选择子Agent并行模式
  - 显示友好提示
  - 35分钟后完成
```

### 手动指定子Agent

```
你: "使用子Agent并行处理这些访谈文件"

系统:
  - 强制使用子Agent并行
  - 不进行自动决策
  - 35分钟后完成
```

### 手动指定CLI队列

```
你: "使用CLI队列依次处理这些访谈文件"

系统:
  - 强制使用CLI队列
  - 依次处理每个文件
  - 5小时后完成
```

---

## ✅ 完成后的下一步

批量编码完成后，自动进入下一阶段：

```yaml
阶段2: 轴心编码
  - 任务: 识别核心范畴
  - 输入: 247个编码、38个概念
  - 输出: 核心范畴清单

阶段3: 选择式编码
  - 任务: 构建理论故事线
  - 输入: 核心范畴
  - 输出: 完整扎根理论

阶段4: 饱和度检验
  - 任务: 验证理论饱和
  - 输入: 当前理论
  - 输出: 饱和度报告
```

---

## 💡 关键洞察

### 1. 并行编码的优势

```yaml
传统方式（CLI队列）:
  - 依次处理
  - 总时间: 5小时
  - 优点: 简单
  - 缺点: 慢

并行方式（子Agent）:
  - 同时处理
  - 总时间: 35分钟
  - 优点: 快（8.6x加速）
  - 缺点: 无
```

### 2. 质量保证

```yaml
子Agent编码质量:
  - 每个子Agent独立编码
  - 避免主观偏见
  - 编码一致性高
  - 质量评分: 4.8/5

整合策略:
  - 合并相似概念
  - 识别高频模式
  - 发现新兴范畴
  - 保证理论完整性
```

### 3. 适用场景

```yaml
最适合子Agent并行的场景:
  ✅ 大量访谈文件（>5个）
  ✅ 文件相互独立
  ✅ 需要快速处理
  ✅ 批量数据处理

不适合的场景:
  ❌ 少量文件（<3个）
  ❌ 文件有依赖关系
  ❌ 需要深度分析
  ❌ 复杂理论建构
```

---

## 🎉 总结

**使用子Agent并行批量编码**:
- ⚡ 8.6x加速（10个文件：5小时→35分钟）
- ✅ 质量保证（4.8/5评分）
- 🎯 自动决策（系统自动选择最优方式）
- 🛡️ 优雅降级（子Agent不可用时自动降级）
- 💡 用户友好（批量任务时友好提示）

**立即体验批量编码的威力！** ⚡
