#!/usr/bin/env python3
"""
批量创建 13 个 skill 的测试记录文件
"""

import os
from datetime import datetime
from pathlib import Path

# 创建测试记录目录
test_dir = Path(r'D:\socienceAI\agentskills\test-records')
test_dir.mkdir(exist_ok=True)

# 13 个 skill 的测试配置
skills = [
    {
        'name': 'grounded-theory-expert',
        'task': '用户满意度研究(20 份访谈)的扎根理论分析',
        'expected_phases': 6,
        'methodology': 'Strauss & Corbin (1990)',
        'test_date': '待测试'
    },
    {
        'name': 'social-network-analysis-expert',
        'task': '科研合作网络分析(100 位学者)',
        'expected_phases': 4,
        'methodology': 'Scott (2017)',
        'test_date': '待测试'
    },
    {
        'name': 'bourdieu-field-analysis-expert',
        'task': '教育场域分析(N=1000 调查数据)',
        'expected_phases': 4,
        'methodology': 'Bourdieu (1984)',
        'test_date': '待测试'
    },
    {
        'name': 'msqca-analysis-expert',
        'task': '政策配置分析(30 个案例)',
        'expected_phases': 5,
        'methodology': 'Ragin (2008)',
        'test_date': '待测试'
    },
    {
        'name': 'did-analysis-expert',
        'task': '政策效应评估(面板数据 N=500, T=5)',
        'expected_phases': 5,
        'methodology': 'Angrist & Pischke (2009)',
        'test_date': '待测试'
    },
    {
        'name': 'data-analysis-expert',
        'task': '社会调查数据分析(N=500, 10 变量)',
        'expected_phases': 3,
        'methodology': '标准统计学方法',
        'test_date': '待测试'
    },
    {
        'name': 'business-ecosystem-analysis-expert',
        'task': '中国电动汽车产业商业生态系统分析',
        'expected_phases': 4,
        'methodology': 'Moore (1993)',
        'test_date': '待测试'
    },
    {
        'name': 'business-model-analysis-expert',
        'task': '特斯拉商业模式分析',
        'expected_phases': 4,
        'methodology': 'Osterwalder & Pigneur (2010)',
        'test_date': '待测试'
    },
    {
        'name': 'actor-network-analysis-expert',
        'task': '人工智能技术创新网络分析(ANT)',
        'expected_phases': 4,
        'methodology': 'Latour (2005)',
        'test_date': '待测试'
    },
    {
        'name': 'digital-marx-expert',
        'task': '平台经济的马克思主义政治经济学分析',
        'expected_phases': 4,
        'methodology': '马克思《资本论》',
        'test_date': '待测试'
    },
    {
        'name': 'digital-durkheim-expert',
        'task': '在线社区的涂尔干社会学分析',
        'expected_phases': 4,
        'methodology': 'Durkheim (1893)',
        'test_date': '待测试'
    },
    {
        'name': 'digital-weber-expert',
        'task': '现代科层制的韦伯社会学分析',
        'expected_phases': 4,
        'methodology': 'Weber (1922)',
        'test_date': '待测试'
    },
    {
        'name': 'survey-design-expert',
        'task': '大学生就业意向调查问卷设计',
        'expected_phases': 4,
        'methodology': 'Dillman (2007)',
        'test_date': '待测试
    }
]

# 测试记录模板
template = ""# {skill_name} 测试记录

**测试日期**: {test_date}  
**测试环境**: Qwen CLI (真实环境)  
**测试者**: {tester}

---

## 📋 测试任务

**任务描述**:
```
{task_description}
```

**预期行为**:
- [ ] 自动分解为 {expected_phases} 个 Phase
- [ ] 遵循 {methodology} 规范
- [ ] 创建 task_plan.md
- [ ] 支持 detail_level 参数
- [ ] 支持 phased_output
- [ ] 记录教训到 lesson-memory.md
- [ ] 积累案例到 case-library/

---

## 🧪 测试过程

### 步骤 1: 启动 skill

**输入**:
```
你是 {skill_name} 吗？请介绍一下你的角色和能力。
```

**输出**:
```
(待记录)
```

**观察**:
- ✅/❌ skill 正确介绍自己
- ✅/❌ 根据 soul.md 回答
- ✅/❌ 提到进化机制

### 步骤 2: 提出复杂任务

**输入**:
```
(完整任务描述)
```

**输出**:
```
(待记录)
```

**观察**:
- ✅/❌ 自动分解任务
- ✅/❌ 分解为 {expected_phases} 个 Phase
- ✅/❌ 创建 task_plan.md
- ✅/❌ 任务分解合理

### 步骤 3: 启动任务执行

**输入**:
```
开始执行 Phase 1
```

**输出**:
```
(待记录)
```

**观察**:
- ✅/❌ 开始执行 Phase 1
- ✅/❌ 遵循专业规范
- ✅/❌ 使用正确术语
- ✅/❌ 执行质量检查

### 步骤 4: 测试信息渐进式披露

**输入**:
```
请用摘要模式(detail_level=1)输出当前结果. 
```

**输出**:
```
(待记录)
```

**观察**:
- ✅/❌ 支持 detail_level=1
- ✅/❌ 输出简洁
- ✅/❌ 包含关键信息

### 步骤 5: 测试进化机制

**输入**:
```
查看教训记忆. 
```

**输出**:
```
(待记录)
```

**观察**:
- ✅/❌ 记录教训
- ✅/❌ 教训格式正确
- ✅/❌ 有改进策略

### 步骤 6: 测试 CLI 任务集成

**输入**:
```
/task list
```

**输出**:
```
(待记录)
```

**观察**:
- ✅/❌ 显示任务清单
- ✅/❌ 显示进度
- ✅/❌ 格式清晰

---

## 📊 评分

| 测试项目 | 预期 | 实际 | 评分 | 备注 |
|----------|------|------|------|------|
| 任务分解 | 自动分解 | | /40 | |
| 专业规范 | 严格遵守 | | /40 | |
| 持久化 | 创建 task_plan.md | | /10 | |
| 信息披露 | 支持 detail_level | | /10 | |
| **总分** | | | **/100** | |

### 评级

- ⭐⭐⭐⭐⭐ (90-100): 优秀
- ⭐⭐⭐⭐ (80-89): 良好
- ⭐⭐⭐ (70-79): 合格
- ⭐⭐ (60-69): 需改进
- ⭐ (<60): 不合格

**本 skill 评级**: ⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐ / ⭐⭐ / ⭐

---

## 💡 改进建议

### 优点
1. 
2. 
3. 

### 需改进
1. 
2. 
3. 

---

## 📁 附件

- task_plan.md
- lesson-memory.md (更新后)
- case-library/ (更新后)
- 输出日志

---

**测试完成**

*完成日期*: {complete_date}  
*总分*: /100  
*评级*: ⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐ / ⭐⭐ / ⭐
""

# 批量创建测试记录文件
for skill in skills:
    record_content = template.format(
        skill_name=skill[name'],
        test_date=skill['test_date'],
        tester='待填写',
        task_description=skill['task'],
        expected_phases=skill['expected_phases'],
        methodology=skill['methodology'],
        complete_date='待填写'
    )
    
    record_path = test_dir / f"{skill['name']}-test-record.md"
    with open(record_path, 'w', encoding='utf-8') as f:
        f.write(record_content)
    
    print(f"✅ 创建 {skill['name']} 测试记录")

print()
print("="*70)
print("批量创建完成！")
print("="*70)
print()
print(f"创建文件数：{len(skills)}")
print(f"文件位置：{test_dir}")
print()
print("下一步:")
print("1. 在 Qwen CLI 中逐个执行测试")
print("2. 填写测试记录")
print("3. 评分和评级")
print()
