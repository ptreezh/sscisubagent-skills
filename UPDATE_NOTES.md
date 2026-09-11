# 技能同步更新说明

## 更新概述

本次更新以 FTP 服务器 `socienceai.com/agentskills/_packages/` 的 zip 包为权威源，对本地技能库进行了全面同步。

## 权威源确定

对比了三个来源后，确定 FTP zip 包为最权威版本：

| 来源 | 技能数 | 文件完整性 | 结论 |
|------|--------|-----------|------|
| `D:\socienceAI` git 历史 (commit `68538690^`) | 60 | 基准版本 | 被 supersede |
| **FTP `_packages/` zip 包** | **60** | **最完整** | **✅ 权威源** |
| `D:\ssciskills\skills\` (合并后) | 64 | 包含额外非学术技能 | 非权威 |

## 关键发现：原技能存在的潜在问题

### 定性分析机械化、模板化问题

经详细对比，**原 git 历史版本存在明显的机械化/模板化倾向**，具体表现为：

1. **过度依赖工具脚本，缺乏灵活性**
   - 原版本每个技能都包含大量 Python 工具脚本（如 `analyze.py`, `evolution.py`, `planning-integration.py` 等）
   - 这些脚本试图将定性分析过程完全自动化，但定性研究的核心在于研究者的判断力和创造性思维
   - 机械化的分析流程可能限制研究者对复杂社会现象的深入理解

2. **固定模板限制批判性思维**
   - 原版本包含大量固定模板（`task_plan.md.template`, `findings.md.template`, `progress.md.template` 等）
   - 模板化的工作流程虽然提高了效率，但可能抑制研究者对研究设计的创新性思考
   - 不同研究情境需要不同的方法组合，过度模板化可能导致"削足适履"

3. **演化状态文件暗示过度系统化**
   - 每个技能都包含 `tools/.evolution/evolution_state.yaml` 和 `evolution.py`
   - 这种"自动演化"机制将知识生成过度系统化，忽视了社会科学研究中直觉、灵感等非系统性因素的重要性

4. **案例分析的标准化风险**
   - 原版本虽然包含正反案例，但案例结构高度一致（`case-001-*.md`, `case-01-*.md`）
   - 标准化的案例格式可能使研究者忽视具体情境的独特性和复杂性

### 新旧版本文件差异统计

| 技能 | 旧版文件数 | 新版文件数 | 差异 | 说明 |
|------|-----------|-----------|------|------|
| digital-durkheim-expert | 37 | 47 | +10 | 新增部署文档、备份文件 |
| did-analysis-expert | 32 | 40 | +8 | 新增测试用例、备份文件 |
| actor-network-analysis-expert | 42 | 49 | +7 | 新增测试提示词 |
| qca-analysis-expert | 33 | 40 | +7 | 新增案例、测试文件 |
| bourdieu-field-analysis-expert | 32 | 37 | +5 | 新增测试提示词 |
| digital-weber-expert | 28 | 33 | +5 | 新增测试文档 |
| cas-simulation-expert | 28 | 32 | +4 | 新增演化备份 |
| grounded-theory-expert | 48 | 52 | +4 | 新增数据文件、测试提示词 |
| social-network-analysis-expert | 41 | 45 | +4 | 新增 README、README |
| survey-design-expert | 24 | 28 | +4 | 新增测试框架 |

## 新版改进点

1. **更丰富的文档**：新增 README、部署指南、备份文件等元数据
2. **测试覆盖增强**：新增 `test-prompts.json`、`tests/.gitkeep` 等测试相关文件
3. **案例扩展**：部分技能新增更多正反案例
4. **清理冗余**：删除 `__pycache__` 等编译产物

## 同步操作记录

### `D:\ssciskills` (GitHub: superpower-socialscience-skills)

```bash
# 修复嵌套目录结构后提交
git add skills/
git commit -m "sync: replace skills with authoritative FTP zip versions (fix nested structure)"
git push upstream main
git push sscisubagent-skills main
```

- Commit: `d895b31`
- 状态: ✅ 已推送到 GitHub

### `D:\socienceAI` (Gitee/GitHub)

```bash
git add agentskills/
git commit -m "sync: add authoritative agentskills from FTP zip packages"
```

- Commit: `2e9f3a8`
- 状态: ⚠️ 本地已提交，推送失败（remote 权限问题）

## 技能清单

### 60 个学术技能（来自 FTP zip）

academic-paper-validation, action-research-expert, actor-network-analysis-expert, agile-pm-expert, balanced-scorecard-expert, bibliometric-analysis-expert, blue-ocean-strategy-expert, bourdieu-field-analysis-expert, brand-equity-expert, business-ecosystem-expert, business-model-expert, cas-simulation-expert, case-study-expert, change-management-expert, consumer-behavior-expert, content-analysis-expert, conversation-analysis-expert, data-analysis-expert, design-thinking-expert, did-analysis-expert, digital-durkheim-expert, digital-marx-expert, digital-weber-expert, discourse-analysis-expert, document-analysis-expert, ethnography-expert, factor-analysis-expert, grounded-theory-expert, historical-analysis-expert, internet-research-expert, ipa-analysis-expert, lean-startup-expert, longitudinal-analysis-expert, machine-learning-research-expert, media-analysis-expert, meta-analysis-expert, mixed-methods-expert, multilevel-modeling-expert, narrative-analysis-expert, nlp-text-mining-expert, okr-expert, organizational-diagnosis-expert, pest-analysis-expert, phenomenology-expert, porter-five-forces-expert, qca-analysis-expert, rct-experimental-design-expert, regression-analysis-expert, rhetoric-analysis-expert, secondary-analysis-expert, sem-analysis-expert, semiotics-analysis-expert, social-network-analysis-expert, social-sequence-analysis-expert, survey-design-expert, swot-analysis-expert, system-dynamics-expert, thematic-analysis-expert, value-proposition-expert, visual-analysis-expert

### 额外本地技能（5 个）

- skill-creator
- skill-upgrade-expert
- socienceai-project-soul
- soul-agent-creator
- soul-agents

## 建议后续行动

1. **审视工具脚本的使用场景**：建议保留核心工具脚本，但减少对自动化流程的依赖
2. **案例库建设**：鼓励研究者基于真实研究情境积累个性化案例，而非完全依赖标准化模板
3. **方法论反思**：在使用这些技能时，保持对方法论局限性的批判意识
4. **修复 remote 配置**：解决 `D:\socienceAI` 的推送权限问题
