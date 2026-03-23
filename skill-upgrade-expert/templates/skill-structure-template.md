# 技能升级模板

**使用此模板快速创建新技能的完整结构**

---

## 目录结构模板

```bash
# 复制此命令创建完整目录结构
mkdir -p agentskills/skill-name/{references,experience,cases/{positive,negative},templates,tools,prompts}

# 创建核心文件
touch agentskills/skill-name/{SKILL.md,README.md,soul.md}
touch agentskills/skill-name/references/{classic-literature.md,concepts.md}
touch agentskills/skill-name/experience/patterns.md
touch agentskills/skill-name/lesson-memory.md
```

---

## SKILL.md 模板

```markdown
# 技能名称 (Skill Name)

**版本**: 5.0.0-cli-native
**方法**: [Methodology Name]
**最后更新**: YYYY-MM-DD

---

## 元数据

```yaml
metadata:
  version: "5.0.0-cli-native"
  methodology: "[Methodology]"
  domain: "[Domain]"
  category: "[Category]"

  capabilities:
    - [能力1]
    - [能力2]
    - [能力3]

  validated: true
  success_rate: "XX%"
  case_count: X
  avg_quality: "X/5"
```

---

## 技能概述

[简要描述技能的功能和价值]

---

## 6大绝对禁止原则

1. 禁止[原则1] - [理由]
2. 禁止[原则2] - [理由]
3. 禁止[原则3] - [理由]
4. 禁止[原则4] - [理由]
5. 禁止[原则5] - [理由]
6. 禁止[原则6] - [理由]

---

## 任务分解规则

### 第一层：主要阶段

- 阶段1: [阶段名称]
- 阶段2: [阶段名称]
- 阶段3: [阶段名称]

### 第二层：子任务

每个阶段分解为具体子任务

### 第三层：原子任务

可独立执行的最小任务单元

---

## 完成度验证清单

- ☑ [检查项1]
- ☑ [检查项2]
- ☑ [检查项3]
- ☑ [检查项4]

---

## CLI原生集成

### 任务队列支持

自动创建任务类型:
- [任务类型1]
- [任务类型2]
- [任务类型3]

### 状态持久化

三层持久化:

第一层: 会话持久化
- 当前任务状态
- 临时数据
- 位置: .claude/session/

第二层: 项目持久化
- 任务历史
- 分析结果
- 位置: project/tasks/

第三层: 学习持久化
- 经验模式
- 案例库
- 位置: experience/ & cases/

### 模型驱动执行

- 直接使用工具
- 不生成脚本
- 状态感知

---

## 自迭代学习

### 经验记录

- lesson-memory.md

### 模式识别

- experience/patterns.md

### 案例库

- cases/positive/ - 成功案例
- cases/negative/ - 失败案例

---

## 使用示例

[提供1-2个简要使用示例]

---

## 参考资料

- [经典文献链接]
- [工具文档链接]
- [相关资源]

---

## 版本历史

```yaml
1.0.0 (YYYY-MM-DD):
  - 初始版本
```
```

---

## README.md 模板

```markdown
# 技能名称 - 快速开始

**一句话描述技能的功能**

---

## 🎯 这个技能做什么？

[简要描述技能的核心功能]

**核心价值**:
- ✅ [价值1]
- ✅ [价值2]
- ✅ [价值3]

---

## 🚀 快速开始

```bash
# 使用示例
[使用示例]
```

---

## 📖 核心概念

### 概念1

[概念解释]

### 概念2

[概念解释]

---

## ✅ 质量保证

[质量检查要点]

---

## 📚 相关文档

- `SKILL.md` - 完整文档
- `references/` - 方法论文献
- `experience/` - 经验模式
- `cases/` - 案例库

---

**开始使用这个技能！**
```

---

## patterns.md 模板

```markdown
# [技能名称] - 识别的模式

**更新日期**: YYYY-MM-DD

---

## 🎯 高频分析模式

### Pattern 1: [模式名称]

**频率**: [高/中/低] (X次/年)
**成功率**: XX%

#### 模式描述

[详细描述这个模式]

#### 实施步骤

1. [步骤1]
2. [步骤2]
3. [步骤3]

#### 经验教训

✅ **成功因素**
   - [因素1]
   - [因素2]

⚠️ **注意事项**
   - [注意1]
   - [注意2]

---

### Pattern 2: [模式名称]

**频率**: [高/中/低] (X次/年)
**成功率**: XX%

[模式描述...]

---

## 💡 总体经验教训

✅ **最佳实践**
   - [实践1]
   - [实践2]
   - [实践3]

⚠️ **常见陷阱**
   - [陷阱1]
   - [陷阱2]
   - [陷阱3]

---

**版本**: 1.0.0
```

---

## case-study 模板

### 成功案例模板

```markdown
# Case XXX: [案例标题]

**日期**: YYYY-MM-DD
**分析类型**: [类型]
**主题**: [主题]

---

## 📋 背景信息

[描述案例背景]

---

## 🔍 分析过程

### Phase 1: [阶段1]

[详细描述]

### Phase 2: [阶段2]

[详细描述]

### Phase 3: [阶段3]

[详细描述]

---

## ✅ 关键发现

1. [发现1]
2. [发现2]
3. [发现3]

---

## 📊 质量评估

**评分**: 5/5

**理由**:
- [理由1]
- [理由2]
- [理由3]

---

## 💡 经验教训

### 成功因素

- [因素1]
- [因素2]

### 可复用的模式

- [模式1]
- [模式2]

---

**分析时长**: X小时
**质量评分**: 5/5
```

### 失败案例模板

```markdown
# Case XXX: [错误标题] - 失败案例

**日期**: YYYY-MM-DD
**错误类型**: [错误类型]

---

## ❌ 问题描述

[描述错误]

---

## 🔬 错误分析

### 错误原因

- [原因1]
- [原因2]
- [原因3]

### 导致的问题

- [后果1]
- [后果2]

---

## ✅ 正确做法

### 修正方案

1. [修正1]
2. [修正2]
3. [修正3]

### 修正结果

[描述修正后的结果]

---

## 💡 经验教训

⚠️ **关键错误**
   - [错误1]
   - [错误2]

✅ **正确原则**
   - [原则1]
   - [原则2]

### 预防措施

1. [措施1]
2. [措施2]
3. [措施3]

---

**质量评分**: 1/5 (失败案例，但学习价值高)
```

---

## 使用这些模板

```bash
# 1. 复制模板到新技能目录
cp -r agentskills/skill-upgrade-expert/templates/* agentskills/your-skill/

# 2. 重命名模板文件
cd agentskills/your-skill
mv skill-structure-template.md YOUR-SKILL-structure.md

# 3. 根据模板创建文件
# 按照 skill-structure-template.md 中的指导
# 创建完整的技能结构

# 4. 定制化内容
# 将模板中的占位符替换为实际内容
# 根据技能特点定制化
```

---

**模板已准备就绪 - 开始创建你的技能！**
