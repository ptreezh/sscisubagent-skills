# 技能升级快速参考

**快速查阅常用的升级模板和检查清单**

---

## 📋 SKILL.md模板

```yaml
# 技能名称 (Skill Name)

**版本**: 5.0.0-cli-native
**方法**: [Methodology Name]
**最后更新**: YYYY-MM-DD

## 元数据
metadata:
  version: "5.0.0-cli-native"
  methodology: "[Methodology]"
  domain: "[Domain]"
  category: "[Category]"

## 6大绝对禁止原则

1. 禁止[原则1]
2. 禁止[原则2]
3. 禁止[原则3]
4. 禁止[原则4]
5. 禁止[原则5]
6. 禁止[原则6]

## 任务分解规则

### 第一层：主要阶段
- 阶段1: [阶段名称]
- 阶段2: [阶段名称]
- 阶段3: [阶段名称]

### 第二层：子任务
每个阶段分解为具体子任务

### 第三层：原子任务
可独立执行的最小任务单元

## 完成度验证清单

- ☑ 检查项1
- ☑ 检查项2
- ☑ 检查项3

## CLI原生集成

### 任务队列支持
- 自动创建任务
- 持久化状态
- 追踪依赖

### 模型驱动执行
- 直接使用工具
- 不生成脚本
- 状态感知

## 自迭代学习

### 经验记录
- lesson-memory.md

### 模式识别
- experience/patterns.md

### 案例库
- cases/positive/
- cases/negative/
```

---

## ✅ Level 1 检查清单

**基础升级** (30分钟)

```yaml
核心文件:
  ☑ SKILL.md已创建
  ☑ 6大禁止原则已定制化
  ☑ 任务分解规则已定义
  ☑ 完成度验证清单已添加

目录结构:
  ☑ skill-name/目录已创建
  ☑ references/子目录
  ☑ experience/子目录
  ☑ cases/positive/子目录
  ☑ cases/negative/子目录
  ☑ templates/子目录

质量标准:
  ☑ 禁止原则针对该技能定制
  ☑ 任务分解规则具体可执行
  ☑ 验证清单明确完整
```

---

## ✅ Level 2 检查清单

**学术对齐** (1小时)

```yaml
经典文献:
  ☑ references/classic-literature.md
  ☑ 至少5篇核心文献
  ☑ 包含作者、年份、标题
  ☑ 简要说明贡献

核心概念:
  ☑ references/concepts.md (如需要)
  ☑ 关键术语定义
  ☑ 权威来源引用
  ☑ 应用示例

成功案例:
  ☑ cases/positive/case-001-[主题].md
  ☑ 完整的分析流程
  ☑ 关键决策说明
  ☑ 质量评分5/5

应用范围:
  ☑ 明确适用场景
  ☑ 说明边界条件
  ☑ 列出局限性
```

---

## ✅ Level 3 检查清单

**CLI原生集成** (30分钟)

```yaml
任务队列:
  ☑ SKILL.md添加CLI集成章节
  ☑ 定义任务类型
  ☑ 说明自动创建机制
  ☑ 依赖追踪规则

状态持久化:
  ☑ 三层持久化说明
  ☑ 会话层: .claude/session/
  ☑ 项目层: project/tasks/
  ☑ 学习层: experience/ & cases/

模型驱动:
  ☑ 优先使用工具
  ☑ 不生成中间脚本
  ☑ 直接调用模型能力
  ☑ 状态感知执行

模板文件:
  ☑ templates/task_plan.md.template
  ☑ 其他相关模板
```

---

## ✅ Level 4 检查清单

**自迭代学习** (1小时)

```yaml
经验模式:
  ☑ experience/patterns.md
  ☑ 至少3个高频模式
  ☑ 包含频率和成功率
  ☑ 经验教训总结

lesson-memory:
  ☑ lesson-memory.md
  ☑ 记录格式定义
  ☑ 经验提取机制
  ☑ 改进建议

案例扩充:
  ☑ 至少2个成功案例
  ☑ 至少1个失败案例（推荐）
  ☑ 案例包含完整流程
  ☑ 质量评估

自迭代流程:
  ☑ 经验提取规则
  ☑ 模式识别方法
  ☑ 知识更新机制
  ☑ 持续优化流程
```

---

## 🎯 常见任务模板

### 任务创建模板

```yaml
task-id: X.Y
title: 任务标题
description: 详细描述
steps:
  - 步骤1
  - 步骤2
  - 步骤3
acceptance:
  - 验收标准1
  - 验收标准2
estimated-time: 30分钟
dependencies: [X.1, X.2]
```

### 案例编写模板

```yaml
# Case XXX: [案例标题]

**日期**: YYYY-MM-DD
**分析类型**: [类型]
**主题**: [主题]

## 背景信息
[描述背景]

## 分析过程
[详细过程]

## 关键发现
[发现列表]

## 质量评估
**评分**: 5/5
**理由**: [评分理由]

## 经验教训
[经验总结]
```

### 模式记录模板

```yaml
### Pattern X: [模式名称]

**频率**: [高/中/低] (X次/年)
**成功率**: XX%

#### 描述
[模式描述]

#### 实施步骤
1. 步骤1
2. 步骤2
3. 步骤3

#### 经验教训
✅ **成功因素**
   - 因素1
   - 因素2

⚠️ **注意事项**
   - 注意1
   - 注意2
```

---

## ⏱️ 时间估算

```yaml
单个技能升级:
  Level 1: 30分钟
  Level 2: 1小时
  Level 3: 30分钟
  Level 4: 1小时
  验证: 15分钟
  ---
  总计: 约3小时

批量升级 (5个并行):
  准备: 30分钟
  执行: 3.5小时
  验证: 1小时
  ---
  总计: 约5小时
  加速比: 3x

批量升级 (10个并行):
  准备: 1小时
  执行: 4小时
  验证: 1.5小时
  ---
  总计: 约6.5小时
  加速比: 5x
```

---

## 🚀 快速命令

### 创建新技能结构

```bash
# 创建完整目录结构
mkdir -p agentskills/skill-name/{references,experience,cases/{positive,negative},templates,tools,prompts}

# 创建基础文件
touch agentskills/skill-name/{SKILL.md,README.md,soul.md}
touch agentskills/skill-name/references/{classic-literature.md,concepts.md}
touch agentskills/skill-name/experience/patterns.md
touch agentskills/skill-name/lesson-memory.md
```

### 复制模板

```bash
# 从skill-upgrade-expert复制模板
cp agentskills/skill-upgrade-expert/templates/* agentskills/your-skill/templates/
cp agentskills/skill-upgrade-expert/references/* agentskills/your-skill/references/
```

---

## 📊 质量评分标准

```yaml
内容完整性 (5分):
  5分: 所有Level完整实施
  4分: 主要部分完成
  3分: 基础部分完成
  2分: 部分完成
  1分: 刚开始

方法论准确性 (5分):
  5分: 完全符合方法论
  4分: 基本符合
  3分: 部分符合
  2分: 有偏差
  1分: 不符合

实用性 (5分):
  5分: 立即可用
  4分: 经过调整可用
  3分: 需要较多调整
  2分: 需要重大调整
  1分: 不可用

CLI集成度 (5分):
  5分: 深度集成
  4分: 良好集成
  3分: 基础集成
  2分: 集成不足
  1分: 未集成

自迭代能力 (5分):
  5分: 完整机制
  4分: 良好机制
  3分: 基础机制
  2分: 机制不足
  1分: 无机制

总分: 25分
合格: 15分 (3/5平均)
优秀: 20分 (4/5平均)
卓越: 25分 (5/5平均)
```

---

## 💡 最佳实践

### DO (推荐做法)

```yaml
✅ 按Level顺序升级
✅ 每个Level完成后验证
✅ 定期保存进度
✅ 使用模板保持一致性
✅ 记录决策和理由
✅ 收集真实案例
✅ 持续迭代改进
```

### DON'T (避免做法)

```yaml
❌ 跳过Level
❌ 追求速度牺牲质量
❌ 忽视文档
❌ 缺少案例
❌ 不验证质量
❌ 模板化但缺乏定制
❌ 忽视经验积累
```

---

## 🔗 相关文档

- `SKILL.md` - 完整方法论
- `README.md` - 快速开始
- `examples/upgrade-workflow.md` - 升级流程详解
- `examples/batch-upgrade.md` - 批量升级指南

---

**快速参考结束 - 查看完整文档了解更多**
