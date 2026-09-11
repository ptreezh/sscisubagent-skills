# 社会科学方法论 Skill 系统 - QWEN.md

**项目位置**: `D:\socienceAI\agentskills\`
**项目类型**: 社会科学方法论 CLI Skill 系统
**最后更新**: 2026-03-22

---

## 📋 项目概述

本项目是一个**社会科学方法论 Skill 系统**，包含 13 个独立的社会科学研究方法专家 Skill，每个 Skill 都具备 CLI 内自主进化能力。

### 核心特性

- ✅ **13 个方法论专家 Skill** - 覆盖质性研究、量化研究、混合方法研究
- ✅ **CLI 内自主进化** - 通过 hooks 自动记录教训、积累案例、定期进化
- ✅ **独立包设计** - 每个 Skill 都是独立完整的 CLI 插件包
- ✅ **跨平台兼容** - 支持 Qwen CLI、Claude CLI、Cursor 等多种环境

---

## 📁 目录结构

```
agentskills/
├── extensions/
│   └── skill-evolution/         # 进化引擎扩展
│       └── index.js             # ~400 行进化引擎代码
├── templates/                   # 模板文件
│   ├── soul.md.template
│   ├── lesson-memory.md.template
│   ├── case-study-template.md
│   ├── skill-hooks.yaml.template
│   └── compatibility.yaml.template
├── _shared_tools/               # 共享工具
│   ├── auto_skill_creator.py
│   ├── validate_skill_spec.py
│   └── verify_all_skills.py
├── grounded-theory-expert/      # 扎根理论专家 (完全配置)
│   ├── soul.md
│   ├── lesson-memory.md
│   ├── skill-hooks.yaml
│   ├── qwen-skill.yaml
│   └── case-library/
├── social-network-analysis-expert/  # 社会网络分析专家 (完全配置)
├── actor-network-analysis-expert/   # 行动者网络分析专家
├── bourdieu-field-analysis-expert/  # 布迪厄场域分析专家
├── digital-marx-expert/             # 数字马克思分析专家
├── digital-durkheim-expert/         # 数字涂尔干分析专家
├── digital-weber-expert/            # 数字韦伯分析专家
├── msqca-analysis-expert/           # 模糊集定性比较分析专家
├── did-analysis-expert/             # DID 分析专家
├── data-analysis-expert/            # 数据分析专家
├── business-ecosystem-analysis-expert/  # 商业生态系统分析专家
├── business-model-analysis-expert/      # 商业模式分析专家
├── survey-design-expert/                # 问卷设计专家
├── skill-creator/                       # Skill 创建工具
├── auto-execute.py                      # 自动化执行引擎
├── auto-test-runner.py                  # 自动化测试运行器
├── batch-test-all.py                    # 批量测试脚本
├── deploy.bat                           # 一键部署脚本
└── DEPLOYMENT-GUIDE.md                  # 部署指南
```

---

## 🎯 13 个 Skill 清单

| # | Skill 名称 | 方法论类型 | 状态 |
|---|-----------|-----------|------|
| 1 | grounded-theory-expert | 扎根理论 | ✅ 完全配置 |
| 2 | social-network-analysis-expert | 社会网络分析 | ✅ 完全配置 |
| 3 | actor-network-analysis-expert | 行动者网络理论 | 🟡 基础完成 |
| 4 | bourdieu-field-analysis-expert | 布迪厄场域分析 | 🟡 基础完成 |
| 5 | digital-marx-expert | 数字马克思分析 | 🟡 基础完成 |
| 6 | digital-durkheim-expert | 数字涂尔干分析 | 🟡 基础完成 |
| 7 | digital-weber-expert | 数字韦伯分析 | 🟡 基础完成 |
| 8 | msqca-analysis-expert | 模糊集 QCA | 🟡 基础完成 |
| 9 | did-analysis-expert | 双重差分分析 | 🟡 基础完成 |
| 10 | data-analysis-expert | 数据分析 | 🟡 基础完成 |
| 11 | business-ecosystem-analysis-expert | 商业生态系统分析 | 🟡 基础完成 |
| 12 | business-model-analysis-expert | 商业模式分析 | 🟡 基础完成 |
| 13 | survey-design-expert | 问卷设计 | 🟡 基础完成 |

**完全配置**: 有完整 skill-hooks.yaml 和 qwen-skill.yaml
**基础完成**: 有 soul.md 和 lesson-memory.md，可后续补充配置

---

## 🚀 快速启动

### 方式 1: 一键部署（推荐）

```bash
cd D:\socienceAI\agentskills
deploy.bat
```

部署完成后：
```bash
qwen
# 应该看到 [SkillEvolution] 日志
# 测试：使用扎根理论分析以下访谈数据...
```

### 方式 2: 手动部署

```bash
# 1. 复制扩展
xcopy /E /I extensions\skill-evolution %USERPROFILE%\.qwen\extensions\

# 2. 复制 skill
xcopy /E /I grounded-theory-expert %USERPROFILE%\.qwen\skills\

# 3. 配置 config.yaml
# 添加 extensions 配置

# 4. 启动测试
qwen
```

### 方式 3: 测试所有 Skill

```bash
python batch-test-all.py
```

---

## 🔧 核心组件

### 1. 进化引擎 (extensions/skill-evolution/index.js)

```javascript
// 进化引擎负责：
- init(): 初始化
- loadSkills(): 加载 skill
- onSessionStart(): 会话启动时加载状态
- onPrePrompt(): 注入 skill 状态到提示词
- onTaskComplete(): 记录教训
- addCase(): 积累案例
- triggerPeriodicEvolution(): 定期进化（每 10 次会话）
```

### 2. soul.md - 角色定义

每个 Skill 的核心配置文件，包含：
- YAML Front Matter（角色、价值观、专长）
- 使命声明
- 工作方式
- 成功案例
- 进化机制说明

### 3. lesson-memory.md - 教训记忆

记录每次任务的教训：
- 情境描述
- 错误表现
- 根本原因
- 改进策略
- 应用案例

### 4. case-library/ - 案例库

存储成功案例：
- successful-cases/
- typical-patterns/
- methodology-examples/

### 5. skill-hooks.yaml - Hooks 配置

配置 CLI hooks 触发机制：
- on_cli_start
- on_session_start
- on_user_input
- on_task_complete
- on_periodic

---

## 🔄 进化机制流程

```
CLI 启动
    ↓
加载 skill-evolution 扩展
    ↓
触发 onSessionStart
    ↓
加载 soul.md, lesson-memory.md, case-library/
    ↓
用户输入 → onPrePrompt
    ↓
注入 skill 状态到系统提示词
    ↓
Skill 执行分析
    ↓
任务完成 → onTaskComplete
    ↓
记录教训 → lesson-memory.md
积累案例 → case-library/
    ↓
每 10 次会话 → onPeriodic
    ↓
复习教训、提炼模式、更新 soul.md
```

---

## 📊 项目统计

### 文件统计
- **模板文件**: 5 个
- **应用文件**: 39+ 个
- **扩展代码**: ~400 行
- **文档**: 6+ 个
- **脚本**: 3+ 个
- **总文件数**: 53+ 个
- **总代码行数**: 2500+ 行

### 质量指标
- **soul.md 覆盖率**: 100% (13/13)
- **lesson-memory.md 覆盖率**: 100% (13/13)
- **case-library 覆盖率**: 100% (13/13)
- **配置完整度**: 15% (2/13 完全配置)
- **文档完整度**: 100%

---

## 🛠️ 常用命令

### 部署相关
```bash
# 一键部署
deploy.bat

# 验证部署
verify-deployment.bat

# 手动复制 skill
xcopy /E /I grounded-theory-expert %USERPROFILE%\.qwen\skills\
```

### 测试相关
```bash
# 批量测试所有 skill
python batch-test-all.py

# 测试单个 skill
python auto-test-runner.py grounded-theory-expert

# 运行测试套件
python -m pytest tests/
```

### 开发相关
```bash
# 创建新 skill
python batch-create-skill-files.py <skill-name>

# 验证 skill 配置
python _shared_tools/validate_skill_spec.py <skill-name>

# 批量更新 skill
python _shared_tools/batch_update_skills.py
```

---

## 📖 文档索引

| 文档 | 用途 |
|------|------|
| [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) | 部署指南 |
| [COMPLETE-PROJECT-SUMMARY.md](COMPLETE-PROJECT-SUMMARY.md) | 完整项目总结 |
| [FINAL-COMPLETION-REPORT.md](FINAL-COMPLETION-REPORT.md) | 最终完成报告 |
| [AUTOMATION-SYSTEM.md](AUTOMATION-SYSTEM.md) | 自动化系统说明 |
| [CLI-TASK-INTEGRATION-AND-DISCLOSURE-OPTIMIZATION.md](CLI-TASK-INTEGRATION-AND-DISCLOSURE-OPTIMIZATION.md) | CLI 任务集成优化 |

---

## 🔍 使用示例

### 示例 1: 使用扎根理论专家

```bash
qwen
```

在 CLI 中输入：
```
使用扎根理论分析以下访谈数据...
[粘贴访谈数据]
```

Skill 会自动：
1. 加载角色定义（soul.md）
2. 注入历史教训（lesson-memory.md）
3. 参考案例库（case-library/）
4. 执行多阶段分析
5. 记录新教训

### 示例 2: 使用社会网络分析专家

```
使用社会网络分析方法分析以下关系数据...
[粘贴关系数据]
```

### 示例 3: 创建新 Skill

```bash
python batch-create-skill-files.py phenomenology-expert
```

会创建：
- phenomenology-expert/soul.md
- phenomenology-expert/lesson-memory.md
- phenomenology-expert/case-library/

---

## ⚙️ 配置说明

### Qwen CLI 配置 (~/.qwen/config.yaml)

```yaml
extensions:
  enabled:
    - skill-evolution

  skill-evolution:
    auto_load: true
    log_level: info
```

### Skill 配置示例 (skill-hooks.yaml)

```yaml
skill_name: grounded-theory-expert
version: 3.0.0

hooks:
  on_cli_start:
    enabled: true
    action: load_soul
    file: soul.md

  on_session_start:
    enabled: true
    actions:
      - action: load_state
        files:
          - lesson-memory.md
          - case-library/

  on_task_complete:
    enabled: true
    actions:
      - action: record_lesson
        file: lesson-memory.md
```

---

## 🐛 故障排查

### 问题 1: 扩展未加载

**症状**: 没有看到 [SkillEvolution] 日志

**解决方案**:
```bash
# 检查扩展目录
ls %USERPROFILE%\.qwen\extensions\

# 检查 config.yaml 配置
cat %USERPROFILE%\.qwen\config.yaml
```

### 问题 2: skill 未找到

**症状**: [SkillEvolution] Skills 目录不存在

**解决方案**:
```bash
# 创建 skills 目录
mkdir -p %USERPROFILE%\.qwen\skills\

# 复制 skill
xcopy /E /I grounded-theory-expert %USERPROFILE%\.qwen\skills\
```

### 问题 3: hooks 未触发

**症状**: 任务完成后没有记录教训

**解决方案**:
```bash
# 检查 skill-hooks.yaml 配置
cat %USERPROFILE%\.qwen\skills\grounded-theory-expert\skill-hooks.yaml

# 确保 hooks 部分 enabled: true
```

---

## 📈 开发路线图

### 已完成
- ✅ 13 个 Skill 核心文件创建
- ✅ 进化引擎实现
- ✅ 部署脚本实现
- ✅ 测试框架实现

### 短期（1-2 周）
- [ ] 为剩余 11 个 Skill 创建 skill-hooks.yaml
- [ ] 为剩余 11 个 Skill 创建 qwen-skill.yaml
- [ ] 积累初始案例（每个 Skill 3-5 个）

### 中期（1 个月）
- [ ] 完善所有 Skill 配置
- [ ] 建立案例库（每个 Skill 10+ 案例）
- [ ] 优化进化引擎性能

### 长期（3 个月+）
- [ ] 扩展到更多 Skill
- [ ] 开源发布
- [ ] 建立 Skill 市场

---

## 🎯 最佳实践

### 1. 使用 Skill 时
- 明确说明使用哪个 Skill
- 提供充分的数据/材料
- 等待 Skill 自动记录教训

### 2. 创建新 Skill 时
- 使用模板文件
- 遵循 soul.md 格式
- 配置 skill-hooks.yaml

### 3. 优化 Skill 时
- 查看 lesson-memory.md 了解历史教训
- 参考 case-library/中的成功案例
- 定期运行批量测试

---

## 📞 支持和资源

**项目位置**: `D:\socienceAI\agentskills\`

**快速启动**:
```bash
cd D:\socienceAI\agentskills
deploy.bat
qwen
```

**核心文档**:
- 快速启动：DEPLOYMENT-GUIDE.md
- 项目总结：COMPLETE-PROJECT-SUMMARY.md
- 完成报告：FINAL-COMPLETION-REPORT.md

**技能列表**:
- 完全配置：grounded-theory-expert, social-network-analysis-expert
- 基础配置：其他 11 个 Skill

---

**最后更新**: 2026-03-22
**项目状态**: ✅ 可部署使用
