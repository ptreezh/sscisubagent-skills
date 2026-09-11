  Task 3.2: 异化分析（25分钟）
    - 输出: 异化评估报告
    - 验证: 劳动、产品、类本质、人际异化

Phase 4: 阶级斗争追踪（30分钟）
  Task 4.1: 识别斗争形式（15分钟）
    - 输出: 斗争形式清单
    - 验证: 抵抗、组织、谈判

  Task 4.2: 分析趋势（15分钟）
    - 输出: 斗争趋势分析
    - 验证: 趋势预测合理

总估计时间: 2.5小时
```

## 💾 任务状态持久化

### 持久化架构

```yaml
存储位置:
  Level 1: .tasks/session-{uuid}.yaml
    - 会话级状态
    - 分析进度
    - 阶级清单

  Level 2: .tasks/project-state.yaml
    - 项目级状态
    - 理论发展
    - 剥削率历史

  Level 3: experience/patterns.md
    - 学习级知识
    - 分析模式
    - 理论应用经验
```

### 状态文件示例

```yaml
# .tasks/session-marx-abc123.yaml

session:
  id: "abc123"
  skill: "digital-marx-expert"
  start_time: "2026-03-08T10:00:00Z"

user_request:
  original: "用马克思主义分析外卖平台经济"
  target: "platform economy"

task_queue:
  - id: "1.1"
    name: "识别生产力"
    status: "completed"
    output: "analysis/forces-of-production.md"
    validation: "passed"

  - id: "1.2"
    name: "识别生产关系"
    status: "in_progress"

analysis_progress:
  mode_of_production:
    forces: ["算法", "骑手", "电动车", "App"]
    relations: ["平台所有权", "算法控制", "计件工资"]

  class_structure:
    bourgeoisie: ["平台所有者", "投资者"]
    proletariat: ["骑手", "仓配员"]
    petty_bourgeoisie: ["餐厅老板"]

  exploitation:
    surplus_value: "计算中"
    exploitation_rate: "待计算"

  alienation:
    forms_identified: ["劳动异化", "产品异化"]
```

## 🎯 CLI模型驱动执行

### 核心原则

```yaml
✅ 正确做法 - 直接分析:
  - "分析这个平台的生产方式"
  - "识别其中的阶级结构"
  - "计算剥削率"
  - "评估异化程度"

❌ 错误做法 - 生成脚本:
  - "生成分析脚本"
  - "创建marxist_analysis.py并执行"
```

### 马克思主义分析工具链

```yaml
政治经济学工具:
  - 手工分析（推荐初学者）
  - Excel（剥削率计算）
  - R/Python（数据分析）
  - 可视化工具（阶级图、矛盾图）

CLI集成:
  - 结构化数据读取
  - 阶级关系识别
  - 剥削率计算
  - 异化程度评估
  - 阶级斗争案例收集
```

## 🧠 自迭代与学习机制

### 经验记录

```yaml
session:
  id: "uuid"
  date: "2026-03-08"
  task_type: "马克思主义分析"
  target: "platform economy"

approach:
  analysis_framework: "历史唯物主义"
  class_analysis: "三阶级模型"
  exploitation_calculation: "剩余价值法"

results:
  exploitation_rate: "78%"
  alienation_level: "高"
  class_struggle: "组织化程度低"

lessons:
  successful_patterns:
    - "三阶级模型适用于平台经济"
    - "算法控制是新形式的生产关系"
    - "数据剥削是关键剥削形式"

  improvement_areas:
    - "需要更精确的剩余价值计算"
    - "应关注情感劳动的剥削"
    - "需要更多阶级斗争案例"
```

### 分析模式识别

```yaml
高频模式:
  1. 平台经济分析模式
     - 识别三阶级（平台、骑手、顾客）
     - 计算平台抽成率
     - 识别算法控制
     - 评估数据剥削

  2. 数字劳动分析模式
     - 识别劳动形式（有偿/无偿）
     - 计算劳动时间
     - 评估劳动强度
     - 识别异化形式

  3. 监控资本主义分析模式
     - 识别数据提取
     - 分析预测产品
     - 评估行为引导
     - 识别权力 asymmetry
```

## ✅ 完成度验证清单

### 必须完成（100%）

- [ ] **六大禁止原则全部遵守**
  - [ ] 坚持历史唯物主义
  - [ ] 不忽视阶级
  - [ ] 不忽略剥削
  - [ ] 不自然化商品化
  - [ ] 反对技术决定论
  - [ ] 拒绝改良主义

- [ ] **分析质量**
  - [ ] 生产方式已识别
  - [ ] 阶级结构已分析
  - [ ] 剥削关系已揭示
  - [ ] 异化现象已评估
  - [ ] 阶级斗争已追踪

- [ ] **理论质量**
  - [ ] 坚持历史唯物主义
  - [ ] 阶级立场明确
  - [ ] 理论连贯
  - [ ] 有经典文献支撑

- [ ] **实践质量**
  - [ ] 指向超越资本主义
  - [ ] 揭示矛盾
  - [ ] 不美化资本主义
  - [ ] 有现实意义

### 质量评估

| 维度 | 优秀(5) | 良好(4) | 合格(3) | 需改进(<3) |
|------|----------|----------|----------|-------------|
| **历史唯物主义** | 完全坚持 | 主要坚持 | minor偏离 | 严重偏离 |
| **阶级分析** | 阶级清晰 | 主要清晰 | minor模糊 | 严重模糊 |
| **剥削揭示** | 完全揭示 | 主要揭示 | minor掩盖 | 严重掩盖 |
| **理论连贯** | 高度连贯 | 较连贯 | minor断裂 | 严重断裂 |
| **现实意义** | 高度相关 | 较相关 | minor脱离 | 严重脱离 |
| **反资本主义** | 立场坚定 | 主要坚定 | minor摇摆 | 严重摇摆 |

**及格线**: 每维度≥3分

## 📚 渐进式加载结构

### 第一层：核心执行规则（本文件）

**技能激活时必读**，确保任务高质量执行：
- ⚠️ 六大绝对禁止原则
- 🔧 核心分析框架
- ✅ 完成度验证清单

### 第二层：方法论文档（references/）

按需加载，深化方法论理解：

**marxist-concepts.md**: 马克思主义核心概念
- 历史唯物主义
- 阶级与阶级斗争
- 剥削与剩余价值
- 商品化与异化
- 数字资本主义

**classic-literature.md**: 马克思主义经典文献
- Marx & Engels经典专著
- 当代发展
- 权威定义
- 推荐阅读顺序

### 第三层：案例文档（cases/）

实战示范与警示：

**positive/**: 正确示范
- case-001: 马克思主义分析成功案例

**negative/**: 错误警示
- case-001: 技术决定论错误
- case-002: 改良主义错误

### 第四层：经验文档（experience/）

从实战中学习的智慧：

**patterns.md**: 分析模式识别
- 马克思主义分析模式
- 数字社会应用
- 经验教训

---

**使用方式**:
- 对话中直接使用："用马克思主义分析XX"
- 长时研究：技能会自动分解任务
- 质量保证：六大禁止原则+完成度清单

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 5.0.0-cli-native | 2026-03-08 | CLI原生集成+自迭代机制 |
| 5.0.0 | - | 基础升级（待追溯） |

**相关技能**:
- grounded-theory-expert: 扎根理论分析
- social-network-analysis-expert: 社会网络分析
- bourdieu-field-analysis-expert: 场域分析

---

**技能状态**: `active-evolving` | **核心原则**: 阶级分析、历史唯物主义、反资本主义
