# SocienceAI AgentSkills

**符合 agentskills.io 规范的社会科学分析技能集合**

---

## 📋 项目概述

本项目提供 13 个社会科学分析专家技能，每个技能都：
- ✅ 符合 agentskills.io 规范
- ✅ 内置 planning-with-files 机制
- ✅ 支持复杂任务分解
- ✅ 支持长时间持续运行
- ✅ 经过严格方法论审核

---

## 🎯 可用 Skills

### 社会分析类 (6 个)

| Skill | 状态 | 方法论基础 |
|-------|------|------------|
| [grounded-theory-expert](./grounded-theory-expert/) | ✅ 已实现 | Glaser & Strauss (1967), Strauss & Corbin (1990), Charmaz (2006) |
| social-network-analysis-expert | ⏳ 实现中 | Wellman & Berkowitz (1988), Scott (2017) |
| actor-network-analysis-expert | ⏳ 实现中 | Latour (2005), Callon (1986), Law (1992) |
| bourdieu-field-analysis-expert | ⏳ 实现中 | Bourdieu (1984, 1993), Swartz (1997) |
| digital-marx-expert | ⏳ 实现中 | Marx (1867), Fuchs (2014), Harvey (2010) |
| digital-durkheim-expert | ⏳ 实现中 | Durkheim (1893, 1897) |

### 社会理论类 (2 个)

| Skill | 状态 | 方法论基础 |
|-------|------|------------|
| digital-weber-expert | ⏳ 实现中 | Weber (1922), Kalberg (1994) |
| social-theory-integration-expert | ⏳ 实现中 | 多理论整合框架 |

### 统计方法类 (3 个)

| Skill | 状态 | 方法论基础 |
|-------|------|------------|
| msqca-analysis-expert | ⏳ 实现中 | Ragin (1987, 2008), Schneider & Wagemann (2012) |
| did-analysis-expert | ⏳ 实现中 | Angrist & Pischke (2009), Bertrand et al. (2004) |
| advanced-statistical-analysis-expert | ⏳ 实现中 | 标准统计学方法 |

### 商业分析类 (2 个)

| Skill | 状态 | 方法论基础 |
|-------|------|------------|
| business-ecosystem-analysis-expert | ⏳ 实现中 | Moore (1993), Iansiti & Levien (2004), Adner (2017) |
| business-model-analysis-expert | ⏳ 实现中 | Osterwalder & Pigneur (2010), Teece (2010) |

### 研究设计类 (1 个)

| Skill | 状态 | 方法论基础 |
|-------|------|------------|
| survey-design-expert | ⏳ 实现中 | Dillman (2007), Fowler (2014), DeVellis (2016) |

---

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone <repository-url> agentskills
cd agentskills

# 进入特定技能目录
cd grounded-theory-expert

# 安装依赖
npm install
```

### 使用

```bash
# 初始化会话
npm run init

# 运行分析
npm start

# 检查进度
npm run check
```

### 配置

```bash
# 设置会话目录
export SESSION_DIR="./my-session"

# 设置 LLM API 密钥
export LLM_API_KEY="your-key"
```

---

## 📁 技能结构

每个技能都遵循标准结构：

```
skill-name/
├── SKILL.md                    # 方法论文档
├── skill.yaml                  # 配置文件
├── skill.js                    # 主实现
├── prompts/                    # 提示词模板
├── templates/                  # planning-with-files 模板
│   ├── task_plan.md.template
│   ├── findings.md.template
│   └── progress.md.template
├── scripts/                    # 会话管理脚本
│   ├── init-session.sh
│   └── check-complete.sh
├── services/                   # 核心服务
├── cases/                      # 示例案例
├── references/                 # 理论参考文献
└── test/                       # 测试文件
```

---

## 🔧 Planning-with-Files 机制

所有技能都内置 planning-with-files 机制：

### 任务计划 (task_plan.md)

- 阶段划分
- 质量检查点
- 错误日志
- 完成进度追踪

### 发现记录 (findings.md)

- 研究发现
- 关键洞察
- 数据引用
- 编码备忘录

### 进度日志 (progress.md)

- 会话记录
- 完成情况
- 下一步计划
- 测试记录

---

## 📊 实施进度

```
总进度：8% (1/13 Skills 实现)

✅ 已完成：1 个 (grounded-theory-expert)
⏳ 进行中：0 个
⏳ 待实现：12 个
```

### 实施路线图

- **Week 1-2**: 基础 Skills (3 个) ✅ 1/3
- **Week 3-4**: 统计方法与商业分析 (4 个) ⏳ 0/4
- **Week 5-6**: 社会理论 Skills (4 个) ⏳ 0/4
- **Week 7-8**: 复杂 Skills (2 个) ⏳ 0/2
- **Week 9-10**: 测试与验证
- **Week 11-12**: 部署到 agentskills.io

---

## 🧪 测试

```bash
# 运行所有测试
npm test

# 运行特定技能测试
cd grounded-theory-expert && npm test

# 生成覆盖率报告
npm run test:coverage
```

---

## 📚 文档

- [项目概览](./PROJECT-OVERVIEW.md)
- [实施指南](./IMPLEMENTATION-GUIDE.md)
- [Skill 开发模板](./SKILL-TEMPLATE.md)
- [Testing 指南](./TESTING-GUIDE.md)

---

## 🤝 贡献

欢迎贡献！请查看：

1. [贡献指南](./CONTRIBUTING.md)
2. [代码规范](./CODE-OF-CONDUCT.md)
3. [Issue 列表](../../issues)

---

## 📄 许可证

MIT License

---

## 📞 支持

- **文档**: 查看各技能的 SKILL.md
- **Issue**: [GitHub Issues](../../issues)
- **邮件**: support@socienceai.com

---

**版本**: 1.0.0  
**最后更新**: 2026-03-03  
**维护者**: SocienceAI Team
