# 批量问卷设计并行执行 - 子Agent示例

**使用子Agent并行设计多个主题的问卷**

---

## 📋 场景描述

**任务**: 为10个不同部门设计员工满意度调查问卷

**部门列表**:
```
departments/
├── research_development.json
├── marketing.json
├── sales.json
├── human_resources.json
├── finance.json
├── it_services.json
├── operations.json
├── customer_service.json
├── legal.json
└── executive.json
```

每个部门的需求文件包含：
- 部门特点
- 关键维度
- 特殊需求
- 样本规模

---

## 🚀 两种执行方式对比

### 方式A: CLI任务队列（串行）

```yaml
用户请求: "为这10个部门各设计一份员工满意度问卷"

系统行为:
  模式: CLI队列（自动选择）

  执行流程:
    Task 1: 设计 research_development 问卷 (45分钟)
      - 文献回顾与量表选择
      - 变量操作化
      - 题目编写
      - 专家评审清单
      - 认知访谈指南
    Task 2: 设计 marketing 问卷 (45分钟)
    ...
    Task 10: 设计 executive 问卷 (45分钟)

  总时间: 450分钟（7.5小时）

  用户看到:
    ✅ 正在设计 research_development 问卷...
    ✅ 正在设计 marketing 问卷...
    ...
    ✅ 完成！总时间: 7.5小时
```

### 方式B: 子Agent并行（批量）

```yaml
用户请求: "为这10个部门各设计一份员工满意度问卷"

系统行为:
  模式: 子Agent并行（自动选择）

  友好提示（仅第一次）:
    ℹ️  检测到批量问卷设计任务（10个部门）
    ℹ️  将使用并行处理以提升效率
    ℹ️  预计时间: 约50分钟（而非7.5小时）

  执行流程:
    启动10个survey-designer子Agent
    ├── 子Agent1: 设计 research_development 问卷
    │   - 量表: Minnesota Satisfaction Questionnaire (短版)
    │   - 维度: 工作自主性、创新支持、团队协作
    │   - 题目: 25题
    │   - 特殊: 创新文化维度
    ├── 子Agent2: 设计 marketing 问卷
    │   - 量表: Job Descriptive Index
    │   - 维度: 工作压力、成就感、团队氛围
    │   - 题目: 30题
    │   - 特殊: 工作生活平衡维度
    ├── 子Agent3: 设计 sales 问卷
    │   - 量表: 自主设计 + 已验证量表混合
    │   - 维度: 激励机制、目标挑战、培训支持
    │   - 题目: 28题
    │   - 特殊: 佣金满意度维度
    ├── ...
    └── 子Agent10: 设计 executive 问卷
        - 量表: 高管专用问卷
        - 维度: 战略清晰度、决策权、组织文化
        - 题目: 20题
        - 特殊: 领导力效能维度

    所有子Agent并行执行 ⚡

    整合阶段:
      - 识别共性维度
      - 保留部门特色
      - 建立跨部门可比性
      - 生成实施指南

  总时间: 50分钟
  加速比: 9.0x ⚡

  用户看到:
    ✅ 正在并行设计10个部门的问卷...
    ✅ research_development 问卷完成 ✅
    ✅ marketing 问卷完成 ✅
    ✅ sales 问卷完成 ✅
    ...
    ✅ 所有问卷设计完成！
    ✅ 跨部门整合完成！
    ✅ 总时间: 50分钟
    ✅ 加速: 9.0x ⚡
```

---

## 📊 结果示例

### 问卷设计整合报告

```json
{
  "total_departments": 10,
  "successful": 10,
  "failed": 0,

  "questionnaires": [
    {
      "department": "research_development",
      "items": 25,
      "dimensions": ["工作自主性", "创新支持", "团队协作", "薪酬福利"],
      "scale_reliability": 0.87,
      "theoretical_basis": "MSQ + JDI",
      "special_dimensions": ["创新文化"],
      "estimated_time": "8分钟"
    },
    {
      "department": "sales",
      "items": 28,
      "dimensions": ["激励机制", "目标挑战", "培训支持", "团队氛围"],
      "scale_reliability": 0.84,
      "theoretical_basis": "JDI + 自主设计",
      "special_dimensions": ["佣金满意度"],
      "estimated_time": "9分钟"
    }
  ],

  "common_dimensions": [
    "工作满意度",
    "组织支持",
    "团队协作",
    "薪酬福利",
    "发展机会"
  ],

  "unique_dimensions": [
    "创新文化" (research_development),
    "佣金满意度" (sales),
    "客户压力" (customer_service),
    "战略清晰度" (executive)
  ],

  "cross_department_comparability": {
    "common_core": 5,
    "department_specific": 15,
    "balance_ratio": 0.33
  },

  "quality_metrics": {
    "theoretical_basis": 4.9,
    "clarity": 4.8,
    "neutrality": 5.0,
    "completeness": 4.7,
    "overall_quality": 4.85
  },

  "implementation_guide": {
    "platform": "Qualtrics",
    "estimated_response_time": "8-10分钟",
    "recommended_sample": "各部门全体员工",
    "pilot_test_required": true
  }
}
```

### 问卷结构示例

```yaml
研究开发部问卷结构:

第一部分: 基本信息 (3题)
  Q1. 您在公司工作的年限
  Q2. 您的职位级别
  Q3. 您的教育背景

第二部分: 工作自主性 (6题, MSQ短版)
  Q4. 我可以自主决定工作方式
  Q5. 我对工作进度有控制权
  ...

第三部分: 创新支持 (7题, 自主设计)
  Q10. 公司鼓励尝试新方法
  Q11. 失败的创新被接受
  Q12. 有充足的创新资源
  ...

第四部分: 团队协作 (5题, JDI)
  Q17. 团队成员互相支持
  Q18. 团队沟通顺畅
  ...

第五部分: 薪酬福利 (4题, MSQ)
  Q22. 我对薪酬水平满意
  Q23. 福利待遇公平
  ...

信度估计: Cronbach's α = 0.87
完成时间: 约8分钟
```

---

## 🎯 使用方式

### 自动模式（推荐）

```
你: "为departments/下的所有部门设计满意度问卷"

系统:
  - 自动检测到10个部门
  - 自动选择子Agent并行模式
  - 显示友好提示
  - 50分钟后完成
```

### 手动指定子Agent

```
你: "使用子Agent并行为这些部门设计问卷"

系统:
  - 强制使用子Agent并行
  - 不进行自动决策
  - 50分钟后完成
```

### 手动指定CLI队列

```
你: "使用CLI队列依次为每个部门设计问卷"

系统:
  - 强制使用CLI队列
  - 依次设计每个问卷
  - 7.5小时后完成
```

---

## ✅ 完成后的下一步

批量问卷设计完成后，自动进入实施准备阶段：

```yaml
阶段2: 预测试准备
  - 任务: 为每个问卷准备预测试材料
  - 输入: 10份问卷草稿
  - 输出:
    - 专家评审清单
    - 认知访谈指南
    - 试测实施计划

阶段3: 在线平台设置
  - 任务: 在Qualtrics/SurveyMonkey设置问卷
  - 输入: 问卷终稿
  - 输出: 在线问卷链接

阶段4: 数据收集实施
  - 任务: 分发问卷并收集数据
  - 输入: 在线问卷链接
  - 输出: 原始数据
```

---

## 💡 关键洞察

### 1. 并行问卷设计的优势

```yaml
传统方式（CLI队列）:
  - 依次设计
  - 总时间: 7.5小时
  - 优点: 简单
  - 缺点: 慢

并行方式（子Agent）:
  - 同时设计
  - 总时间: 50分钟
  - 优点: 快（9.0x加速）
  - 缺点: 无
```

### 2. 质量保证

```yaml
子Agent问卷设计质量:
  - 每个子Agent独立设计
  - 基于理论选择量表
  - 避免编造题目
  - 质量评分: 4.85/5

整合策略:
  - 识别共性维度（跨部门可比）
  - 保留部门特色（满足特殊需求）
  - 建立平衡比例（共性vs特色）
  - 确保信效度达标
```

### 3. 适用场景

```yaml
最适合子Agent并行的场景:
  ✅ 多主题问卷设计（>5个）
  ✅ 主题相互独立
  ✅ 需要快速设计
  ✅ 标准化问卷需求

不适合的场景:
  ❌ 单一问卷深度设计
  ❌ 问卷有强依赖
  ❌ 需要大量定制
  ❌ 复杂实验设计
```

---

## 🎉 总结

**使用子Agent并行批量问卷设计**:
- ⚡ 9.0x加速（10个问卷：7.5小时→50分钟）
- ✅ 质量保证（4.85/5评分）
- 🎯 自动决策（系统自动选择最优方式）
- 🛡️ 优雅降级（子Agent不可用时自动降级）
- 💡 用户友好（批量任务时友好提示）

**立即体验批量问卷设计的威力！** ⚡
