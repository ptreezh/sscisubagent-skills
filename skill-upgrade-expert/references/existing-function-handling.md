# 已有功能处理策略

**如何处理目标技能中已存在的功能**

---

## 📋 第一步：功能审计

### 1.1 创建审计清单

```yaml
审计维度:
  Level 1: 基础升级
    ☑ 6大禁止原则是否存在？
    ☑ 任务分解规则是否存在？
    ☑ 完成度验证清单是否存在？
    ☑ 质量如何？（需要评估）

  Level 2: 学术对齐
    ☑ 经典文献是否引用？
    ☑ 核心概念是否定义？
    ☑ 成功案例是否存在？
    ☑ 质量如何？（需要评估）

  Level 3: CLI集成
    ☑ 任务队列支持是否实现？
    ☑ 状态持久化是否实现？
    ☑ 模型驱动执行是否实现？
    ☑ 质量如何？（需要评估）

  Level 4: 自迭代
    ☑ experience/patterns.md是否存在？
    ☑ lesson-memory.md是否存在？
    ☑ 案例库是否丰富？
    ☑ 质量如何？（需要评估）
```

### 1.2 质量评估标准

```yaml
评估标准:

5分 - 完全符合标准 ✅
  - 内容完整
  - 结构正确
  - 质量高
  - 无需修改
  → 保留，直接使用

4分 - 基本符合标准 ⚠️
  - 内容基本完整
  - 结构基本正确
  - 质量良好
  - 小幅改进即可
  → 保留，小幅优化

3分 - 部分符合标准 ⚠️
  - 内容部分完整
  - 结构有偏差
  - 质量中等
  - 需要较多改进
  → 改进，提升质量

2分 - 不符合标准 ❌
  - 内容不完整
  - 结构有误
  - 质量较低
  - 需要重大改进
  → 重写，替换原有

1分 - 缺失或完全错误 ❌
  - 功能缺失
  - 完全不符合
  - 无法使用
  → 创建，全新实现
```

---

## 🔄 第二步：处理策略矩阵

### 2.1 决策树

```
开始审计
    ↓
功能是否存在？
    ├─ 否 → 创建新功能 (CREATE)
    └─ 是 → 评估质量
            ↓
        质量评分？
            ├─ 5分 → 保留 (KEEP)
            ├─ 4分 → 优化 (OPTIMIZE)
            ├─ 3分 → 改进 (IMPROVE)
            └─ 2分/1分 → 重写 (REWRITE)
```

### 2.2 处理策略表

| 已有功能 | 质量评分 | 处理策略 | 操作说明 | 时间估算 |
|---------|---------|---------|---------|---------|
| **完整且高质量** | 5/5 | KEEP | 保留原样，不做修改 | 0分钟 |
| **基本完整** | 4/5 | OPTIMIZE | 小幅优化，补充细节 | 15分钟 |
| **部分完整** | 3/5 | IMPROVE | 改进结构和内容 | 30分钟 |
| **存在但有缺陷** | 2/5 | REWRITE | 重写该部分 | 45分钟 |
| **缺失或错误** | 1/5 | CREATE | 全新创建 | 60分钟 |

---

## 📝 第三步：具体处理方式

### 场景1: 已有6大禁止原则（质量评分：4/5）

**已有内容**:
```yaml
# data-analysis-expert的6大禁止

1. 禁止P值崇拜
2. 禁止忽视数据质量
3. 禁止方法误用
4. 禁止过度解读
5. 禁止隐瞒局限性
```

**问题**: 只有5条，缺少第6条

**处理策略**: OPTIMIZE (优化)

**操作**:
```yaml
步骤1: 评估现有5条
  - 内容准确 ✅
  - 针对性强 ✅
  - 覆盖主要问题 ✅

步骤2: 补充第6条
  - 分析: 缺少什么？
    → 缺少"忽视效应量"的问题
  - 新增: "禁止忽视效应量"

步骤3: 格式统一
  - 确保所有6条格式一致
  - 添加详细说明

步骤4: 验证
  - 是否完整？是 ✅
  - 是否准确？是 ✅
  - 是否有针对性？是 ✅

时间: 15分钟
```

**优化后**:
```yaml
1. 禁止P值崇拜
   理由: P值不能代表全部证据

2. 禁止忽视数据质量
   理由: 垃圾进，垃圾出

3. 禁止方法误用
   理由: 每种方法有适用前提

4. 禁止过度解读
   理由: 相关不等于因果

5. 禁止隐瞒局限性
   理由: 透明是科学的基础

6. 禁止忽视效应量
   理由: 统计显著性不等于实际意义
```

---

### 场景2: 已有经典文献（质量评分：2/5）

**已有内容**:
```yaml
# references/classic-literature.md

数据分析相关书籍:
- 统计学导论
- SPSS使用指南
- Excel数据分析
```

**问题**:
- ❌ 不是学术经典文献
- ❌ 缺少作者、年份
- ❌ 缺少贡献说明
- ❌ 质量不符合Level 2标准

**处理策略**: REWRITE (重写)

**操作**:
```yaml
步骤1: 备份原有内容
  - 移动到 references/old-literature.md.bak
  - 保留以备参考

步骤2: 重新创建
  - 查找真正的经典文献
  - 学术权威性优先
  - 包含完整信息

步骤3: 编写新内容
  1. Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences
     - 贡献: 效应量的标准

  2. Abbott, A. (1988). "Transcending General Linear Reality"
     - 贡献: 因果分析方法论

  3. Gelman, A. (2019). "The Problems with P-Values"
     - 贡献: P值批判

  ... (更多文献)

步骤4: 验证质量
  - 是否学术权威？是 ✅
  - 信息是否完整？是 ✅
  - 贡献是否清晰？是 ✅

时间: 45分钟
```

---

### 场景3: 已有CLI集成（质量评分：5/5）

**已有内容**:
```yaml
# SKILL.md中的CLI集成章节

## CLI原生集成

### 任务队列支持
已实现自动任务创建
任务类型: data-prep, analysis, validation

### 状态持久化
三层架构完整
会话层: .claude/session/
项目层: project/tasks/
学习层: experience/

### 模型驱动执行
直接使用工具，不生成脚本
```

**问题**: 无

**处理策略**: KEEP (保留)

**操作**:
```yaml
步骤1: 验证完整性
  ☑ 任务队列: 完整 ✅
  ☑ 状态持久化: 完整 ✅
  ☑ 模型驱动: 完整 ✅

步骤2: 质量检查
  ☑ 符合CLI原生标准 ✅
  ☑ 文档清晰 ✅
  ☑ 可直接使用 ✅

步骤3: 保留原样
  - 不做任何修改
  - 直接使用
  - 记录在审计报告中

时间: 0分钟 ✨
```

---

### 场景4: 已有经验模式（质量评分：3/5）

**已有内容**:
```yaml
# experience/patterns.md

数据分析模式:

模式1: 描述性统计
做描述性统计分析

模式2: 推断统计
做推断统计分析

模式3: 可视化
画图表
```

**问题**:
- ⚠️ 内容过于简单
- ⚠️ 缺少频率和成功率
- ⚠️ 缺少经验教训
- ⚠️ 不符合高质量标准

**处理策略**: IMPROVE (改进)

**操作**:
```yaml
步骤1: 保留有价值的内容
  - 模式分类: 保留（描述性、推断性、可视化）
  - 基础结构: 保留

步骤2: 扩展和深化
  原有: 模式1: 描述性统计 - 做描述性统计分析

  改进后:
  ### Pattern 1: 描述性统计模式

  **频率**: 高频 (30次/年)
  **成功率**: 95%

  #### 分析流程
  1. 数据清洗
  2. 计算集中趋势
  3. 计算离散程度
  4. 检查分布形态

  #### 经验教训
  ✅ **成功因素**
     - 先检查数据质量
     - 选择合适的统计量
     - 可视化辅助理解

  ⚠️ **常见错误**
     - 忽视异常值
     - 只报告均值
     - 缺少可视化

步骤3: 统一格式
  - 添加元数据（频率、成功率）
  - 扩展经验教训
  - 使用标准模板

步骤4: 验证
  - 是否实用？是 ✅
  - 是否详细？是 ✅
  - 是否可学习？是 ✅

时间: 30分钟
```

---

## 🛠️ 第四步：实用工具

### 4.1 自动化审计脚本

创建 `tools/audit-skill.py`:

```python
#!/usr/bin/env python3
"""
技能审计工具
自动检查技能的功能完整性和质量
"""

import os
import json
from pathlib import Path

def audit_skill(skill_path):
    """审计单个技能"""
    audit_result = {
        "skill": skill_path,
        "levels": {},
        "recommendations": []
    }

    # Level 1审计
    skill_md = Path(skill_path) / "SKILL.md"
    if skill_md.exists():
        content = read_file(skill_md)
        has_prohibitions = check_prohibitions(content)
        has_decomposition = check_decomposition(content)

        audit_result["levels"]["level1"] = {
            "exists": True,
            "prohibitions": has_prohibitions,
            "decomposition": has_decomposition,
            "quality": estimate_quality(content)
        }
    else:
        audit_result["levels"]["level1"] = {"exists": False}

    # Level 2审计
    lit_md = Path(skill_path) / "references" / "classic-literature.md"
    if lit_md.exists():
        # 评估文献质量
        audit_result["levels"]["level2"] = audit_literature(lit_md)
    else:
        audit_result["levels"]["level2"] = {"exists": False}

    # Level 3审计
    # 检查CLI集成章节

    # Level 4审计
    patterns_md = Path(skill_path) / "experience" / "patterns.md"
    if patterns_md.exists():
        audit_result["levels"]["level4"] = audit_patterns(patterns_md)
    else:
        audit_result["levels"]["level4"] = {"exists": False}

    # 生成建议
    audit_result["recommendations"] = generate_recommendations(audit_result)

    return audit_result

def generate_recommendations(audit_result):
    """根据审计结果生成处理建议"""
    recommendations = []

    for level, data in audit_result["levels"].items():
        if not data.get("exists"):
            recommendations.append({
                "level": level,
                "action": "CREATE",
                "reason": "功能缺失"
            })
        elif data.get("quality", 0) <= 2:
            recommendations.append({
                "level": level,
                "action": "REWRITE",
                "reason": "质量不符合标准"
            })
        elif data.get("quality", 0) == 3:
            recommendations.append({
                "level": level,
                "action": "IMPROVE",
                "reason": "需要改进"
            })
        elif data.get("quality", 0) == 4:
            recommendations.append({
                "level": level,
                "action": "OPTIMIZE",
                "reason": "小幅优化"
            })
        else:  # quality == 5
            recommendations.append({
                "level": level,
                "action": "KEEP",
                "reason": "质量优秀"
            })

    return recommendations

# 使用示例
if __name__ == "__main__":
    result = audit_skill("agentskills/my-skill")
    print(json.dumps(result, indent=2))
```

### 4.2 审计报告模板

创建 `templates/audit-report.md`:

```markdown
# [技能名称] 审计报告

**审计日期**: YYYY-MM-DD
**当前版本**: X.X.X
**目标版本**: 5.0.0-cli-native

---

## 📊 审计摘要

```yaml
总体评估:
  当前状态: [基础/部分/接近目标]
  需要改进: X个Level
  可以保留: Y个Level
  预估时间: X小时
```

---

## Level 1: 基础升级

**状态**: [存在/不存在]
**质量评分**: X/5

**已有内容**:
[列出已有内容]

**处理策略**: [KEEP/OPTIMIZE/IMPROVE/REWRITE/CREATE]

**行动清单**:
- [ ] [具体行动1]
- [ ] [具体行动2]

**预估时间**: X分钟

---

## Level 2: 学术对齐

**状态**: [存在/不存在]
**质量评分**: X/5

[同样的结构...]

---

## Level 3: CLI集成

**状态**: [存在/不存在]
**质量评分**: X/5

[同样的结构...]

---

## Level 4: 自迭代

**状态**: [存在/不存在]
**质量评分**: X/5

[同样的结构...]

---

## 📋 总体行动计划

### 优先级排序

1. **高优先级** (立即处理)
   - [ ] [功能1] - CREATE - 60分钟
   - [ ] [功能2] - REWRITE - 45分钟

2. **中优先级** (本周处理)
   - [ ] [功能3] - IMPROVE - 30分钟
   - [ ] [功能4] - OPTIMIZE - 15分钟

3. **低优先级** (有空处理)
   - [ ] [功能5] - KEEP - 0分钟

### 总时间估算

- 必须做: X小时
- 建议做: Y小时
- 可选: Z小时
- **总计**: X+Y+Z 小时

---

## ✅ 完成标准

- [ ] 所有Level达到3分以上
- [ ] 总体质量达到4/5
- [ ] 通过完整验证清单
```

---

## 🎯 实战建议

### 原则1: 审计优先

```yaml
在做任何修改前:
  1. 完整审计现有功能
  2. 评估质量评分
  3. 制定处理策略
  4. 估算时间和成本

避免:
  ❌ 盲目重写
  ❌ 忽视已有内容
  ❌ 浪费时间
```

### 原则2: 质量优先

```yaml
决策优先级:
  1. 质量评分 5分 → 保留 (KEEP)
  2. 质量评分 4分 → 优化 (OPTIMIZE)
  3. 质量评分 3分 → 改进 (IMPROVE)
  4. 质量评分 2分 → 重写 (REWRITE)
  5. 质量评分 1分 → 创建 (CREATE)

目标:
  - 保留优秀的已有内容
  - 改进可用的内容
  - 重写不合格的内容
  - 创建缺失的内容
```

### 原则3: 渐进式改进

```yaml
不要一次性重写所有内容:

✅ 推荐做法:
  - 先审计，后决策
  - 保留好的，改进差的
  - 分批处理，逐步完善
  - 持续迭代

❌ 避免做法:
  - 全部推倒重来
  - 浪费已有成果
  - 一次性完成所有
  - 缺少渐进改进
```

---

## 📊 时间对比

```yaml
全新创建技能:
  - 时间: 3小时
  - 无已有内容可利用

部分功能已有:
  - 时间: 1-2.5小时
  - 取决于已有功能质量

完整功能（高质量）:
  - 时间: 0-30分钟
  - 只需小幅优化或保留

审计价值:
  - 节省时间: 30分钟 - 2.5小时
  - 避免浪费: 不重写已有好内容
  - 质量保证: 更了解现状
```

---

**总结**: 审计是升级的第一步，也是最关键的一步！
