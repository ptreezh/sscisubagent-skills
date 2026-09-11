# SWOT分析经验记忆

## 技能概述

本技能为SWOT战略分析专家，提供系统化的SWOT分析方法论支持。

---

## 版本历史

### v5.0.0-cli-native+agent (2026-03-15)

**新增功能**：
- 添加Planning-With-Files支持
- 添加CRCT思维链
- 添加三层状态持久化
- 添加子Agent并行支持
- 完善质量保证体系

**目录结构**：
```
swot-analysis-expert/
├── SKILL.md                    # 核心技能定义
├── skill.yaml                  # 技能配置
├── subagents.yaml              # 子Agent定义
├── prompts/
│   └── system-prompt.md        # 系统提示词
├── references/
│   ├── classic-literature.md   # 经典文献
│   └── detailed-guide.md       # 详细指南
├── cases/
│   ├── positive/               # 成功案例
│   └── negative/               # 失败案例
├── templates/
│   ├── task_plan.md.template   # 任务计划模板
│   ├── progress.md.template    # 进度跟踪模板
│   └── findings.md.template    # 发现记录模板
├── experience/
│   └── patterns.md             # 经验模式
├── tools/                      # 工具脚本
└── lesson-memory.md            # 本文件
```

---

## 经验记录

### 2026-03-15: 技能补全完成

**任务**：将swot-analysis-expert从骨架版补全到v5.0.0-cli-native标准

**完成内容**：
1. 创建prompts/system-prompt.md - 完整的系统提示词，包含CRCT思维链
2. 创建references/classic-literature.md - 6篇核心文献引用
3. 创建references/detailed-guide.md - 详细方法论指南
4. 创建cases/positive/case-001-ai-startup.md - AI创业公司完整案例
5. 创建cases/negative/case-001-superficial-analysis.md - 表层化分析负面案例
6. 创建templates/ - 3个模板文件
7. 创建experience/patterns.md - 成功/失败模式总结

**经验教训**：
1. 骨架版技能严重不符合v5.0.0标准，文件数从3个需补全到20+
2. 必须包含CRCT思维链、Planning-With-Files支持
3. 必须有三层持久化机制
4. 必须有成功和失败案例

---

## 质量标准

### 必须达到的标准

1. **因素完整性**：每类因素至少3个
2. **因素具体性**：每个因素有具体描述和证据
3. **评估数据化**：评分有依据，权重总和为1.0
4. **战略逻辑性**：战略有因素支撑，具体可操作
5. **行动可行性**：有优先级、时间规划和资源匹配

### 绝对禁止

1. 禁止预设战略
2. 禁止忽略负面因素
3. 禁止无证据评估
4. 禁止因素遗漏
5. 禁止战略空泛
6. 禁止静态思维

---

## 后续改进计划

### 待添加功能

- [ ] 工具脚本开发（factor_identifier.py等）
- [ ] 定量分析方法（AHP-SWOT）
- [ ] 动态SWOT更新机制
- [ ] 更多行业案例

### 待优化内容

- [ ] 提示词精炼
- [ ] 案例库扩充
- [ ] 工具效率优化

---

**最后更新**: 2026-03-15
**版本**: 5.0.0-cli-native+agent
