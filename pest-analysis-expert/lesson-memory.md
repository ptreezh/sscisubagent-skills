# PEST/PESTEL分析经验记忆

## 技能概述

本技能为PEST/PESTEL环境分析专家，提供系统化的宏观环境分析方法论支持。

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
pest-analysis-expert/
├── SKILL.md                    # 核心技能定义
├── skill.yaml                  # 技能配置
├── subagents.yaml              # 子Agent定义
├── prompts/
│   └── system-prompt.md        # 系统提示词
├── references/
│   ├── classic-literature.md   # 经典文献
│   └── detailed-guide.md       # 详细指南
├── cases/
│   └── positive/               # 成功案例
├── templates/                  # 模板文件
├── experience/
│   └── patterns.md             # 经验模式
├── tools/                      # 工具脚本
└── lesson-memory.md            # 本文件
```

---

## 经验记录

### 2026-03-15: 技能补全完成

**任务**：将pest-analysis-expert从骨架版补全到v5.0.0-cli-native标准

**完成内容**：
1. 创建prompts/system-prompt.md - 完整的系统提示词，包含CRCT思维链
2. 创建references/classic-literature.md - 核心文献引用
3. 创建references/detailed-guide.md - 详细方法论指南
4. 创建cases/positive/case-001-ev-industry.md - 新能源汽车行业案例
5. 创建experience/patterns.md - 成功/失败模式总结

---

## 6大绝对禁止原则

1. 禁止维度遗漏 - 必须分析所有六个维度
2. 禁止因素空泛 - 每个因素必须具体、可描述
3. 禁止无证据 - 所有因素必须有数据或证据支撑
4. 禁止静态分析 - 必须考虑时间维度和趋势
5. 禁止忽视关联 - 必须分析维度间的交叉影响
6. 禁止脱离战略 - 因素必须与战略决策相关

---

**最后更新**: 2026-03-15
**版本**: 5.0.0-cli-native+agent
