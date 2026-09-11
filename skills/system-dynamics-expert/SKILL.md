---
name: system-dynamics-expert
description: |
  系统动力学专家。提供因果回路图构建、库存流量建模、反馈循环分析、政策仿真功能。适用于系统分析、政策评估、动态建模场景。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
---

---
#XM|name: system-dynamics-expert
#TX|description: System Dynamics Expert - 技能说明
#ZM|---
> ## 🔴 强制自动执行规则
> 
> **创建任务列表后，必须立即按顺序执行第一个任务，禁止询问用户！**
> 
> ❌ 禁止："告诉我要启动哪个任务"、"请选择要执行的任务"
> ✅ 必须：显示任务列表 → 立即开始执行第一个任务


#BT|
#MQ|# SKILL.md - system-dynamics-expert
#HN|
#JZ|## 基本信息
#JT|
#KJ|---
#PN|metadata:
#TS|  version: "5.0.0-cli-native+agent"
#PH|  methodology: "System Dynamics (Forrester, Sterman)"
#VP|  absolute-prohibitions: true
#SM|  task-decomposition-rules: true
#SK|  ai-cli-native: true
#BB|  task-queue-support: true
#TV|  agentskills-io: true
#JT|  cross-platform: true
#SQ|  state-persistence: true
#MS|  self-iteration: true
#RR|  academic-alignment: true
#SK|  subagent-support: true
#NH|  graceful-fallback: true
#NV|  execution_modes:
#MX|    cli_queue: "CLI任务队列（基础）"
#MR|    subagent_parallel: "子Agent并行（增强）"
#QS|  performance:
#QT|    sequential: "25分钟/模型"
#MH|    parallel: "30分钟/10模型（8.3x加速）"
#NB|  created: "2026-03-08"
#NS|  updated: "2026-03-08"
#WV|  author: "SocienceAI Methodology Expert"
#TW|  license: "MIT"
#ZK|  alignment_reference: "grounded-theory-coding (v5.0.0)"
#XM|---
#RB|
#MQ|# SKILL.md - system-dynamics-expert
#MS|
#JZ|## 🚀 在 AI CLI 中使用
#BH|
#NZ|### 方式 1: 在对话中直接使用（推荐）
#RZ|
#YB|```
#NX|你：使用系统动力学技能分析城市人口增长
#KS|
#KT|AI: 好的，我将使用系统动力学技能进行分析。
#BR|    正在创建任务队列...
#BY|
#QN|    任务清单：
#VJ|    1. 问题界定 (20 分钟)
#QW|    2. 变量识别 (20 分钟)
#VX|    3. 因果回路分析 (30 分钟)
#NM|    4. 存流量建模 (30 分钟)
#NZ|    5. 仿真分析 (30 分钟)
#YJ|    6. 政策干预分析 (20 分钟)
#XN|    7. 系统动力学报告 (20 分钟)
#NJ|
#SP|    共 7 个任务，预计 170 分钟。开始执行...
#VQ|```
#YQ|
### 方式 2: 使用 Python 工具

python tools:

#### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | causal_loop_analyzer.py | 识别和分析因果回路 |
| 2 | stock_flow_analyzer.py | 分析存量和流量 |
| 3 | model_validator.py | 验证系统动力学模型 |
| 4 | simulation_runner.py | 运行系统动力学模拟 |
| 5 | parameter_sweep.py | 参数空间探索 |
| 6 | scenario_builder.py | 构建备选方案场景 |
| 7 | sensitivity_analyzer.py | 参数敏感性分析 |
| 8 | behavior_analyzer.py | 系统行为模式识别 |

#### 使用示例

```bash
# 1. 因果回路分析
python tools/causal_loop_analyzer.py -i data/variables.yaml -o results/causal_loops.json

# 2. 存量流量分析  
python tools/stock_flow_analyzer.py -i data/stock_flow.yaml -o results/stock_flow.json

# 3. 模型验证
python tools/model_validator.py -i results/stock_flow.json -o results/validation.json

# 4. 运行模拟
python tools/simulation_runner.py -i results/validated_model.json --horizon 100 -o results/simulation.json

# 5. 参数探索
python tools/parameter_sweep.py -i results/simulation.json --ranges params.json -o results/sweep.json

# 6. 场景构建
python tools/scenario_builder.py --base model.json --changes scenarios.yaml -o results/scenarios.json

# 7. 敏感性分析
python tools/sensitivity_analyzer.py --model model.json --parameter growth_rate -o results/sensitivity.json

# 8. 行为分析
python tools/behavior_analyzer.py --model model.json --horizon 100 -o results/behavior.json
```
#JZ|
#JZ|## 基本信息
#BH|
#NZ|**名称**: system-dynamics-expert (System Dynamics Modeling Expert)
#RZ|**版本**: 5.0.0-cli-native+agent
#YB|**作者**: SocienceAI Methodology Expert
#NX|**许可证**: MIT
#KS|**对齐标准**: grounded-theory-coding (v5.0.0)
#NM|**子Agent支持**: ✅ 支持（批量模型仿真可使用子Agent并行）
#BY|
#QN|## 描述
#QW|
#PX|## 🖥️ 项目初始化（跨平台Python脚本）
#QW|
#RM|```python
#RM|import os
#RM|
#RM|# 设置项目路径（跨平台兼容）
#RM|project_path = r"D:\\your_project_path\\项目名"
#RM|
#RM|# 创建标准目录结构
#RM|for subdir in ['.tasks', 'data', 'results', 'visualizations', 'logs']:
#RM|    os.makedirs(os.path.join(project_path, subdir), exist_ok=True)
#RM|
#RM|print(f"项目目录创建完成: {project_path}")
#RM|```
#BY|
#VX|**系统动力学建模专家** - 支持**复杂任务分解**和**长时任务执行**的动态仿真技能。
#NM|
#NZ|基于System Dynamics方法，通过Stock & Flow图和反馈回路分析系统的动态行为，研究复杂系统的非线性、延迟和反馈机制。
#YJ|
#VS|### 核心能力
#XN|
#NJ|1. **系统建模**
#SP|   - Stock (存量) 识别与定义
#VQ|   - Flow (流量) 建模
#YQ|   - 反馈回路识别（正反馈、负反馈）
#VW|
#KQ|2. **动态分析**
#YT|   - 延迟建模（物质延迟，信息延迟）
#ST|   - 非线性关系
#JW|   - 时间边界与行为模式
#JQ|
#HX|3. **仿真实验**
#XH|   - 情景模拟
#BT|   - 政策干预分析
#XR|   - 敏感性测试
#PR|
#QB|4. **干预设计**
#NP|   - 杠杆点识别
#NV|   - 政策优化
#KP|   - 系统变革策略
#JW|
#PT|### 适用场景
#PX|
#MB|- ✅ 政策分析（公共卫生、环境、经济政策）
#WN|- ✅ 组织管理（供应链、项目管理）
#SN|- ✅ 城市系统（人口、交通、资源）
#TN|- ✅ 生态系统（资源管理、环境可持续）
#XV|- ✅ 商业战略（市场扩散、竞争动态）
#WR|
#JK|## ⚠️ 六大绝对禁止原则
#KR|
#KJ|### 1. 禁止线性思维
#VS|
#XM|**错误**: "A增加，B线性增加"
#NS|**正确**: 反馈回路、非线性、阈值、突发行为
#RT|
#YM|### 2. 禁止忽视延迟
#BX|
#YR|**错误**: 即时因果
#SH|**正确**: 物质延迟，信息延迟对系统行为的影响
#ZT|
#RR|### 3. 禁止忽视反馈
#BP|
#MV|**错误**: 单向因果链
#NX|**正确**: 识别正反馈（增强）、负反馈（平衡）回路
#ZS|
#VK|### 4. 禁止边界过窄
#YS|
#BJ|**错误**: 过度简化系统边界
#HS|**正确**: 包含关键反馈、即使难以量化
#HT|
#VX|### 5. 禁止单一情景
#YQ|
#SK|**错误**: 只模拟一种情景
#BW|**正确**: 多情景分析、敏感性测试
#YX|
#YY|### 6. 禁止不校准验证
#PP|
#JH|**错误**: 不与历史数据对比
#YK|**正确**: 模型校准、历史拟合、有效性检验
#BK|
#WQ|### 任务分解模板
#RM|
#VY|```yaml
#XY|完整SD项目（4-8周）:
#QY|
#XY|  Phase 1: 问题界定（1周）
#MX|    Task 1.1: 动态问题识别（2小时）
#ZJ|      - 输出: 问题陈述文档
#XJ|      - 验证: 问题边界清晰
#WV|
#SJ|    Task 1.2: 关键变量选择（2小时）
#KJ|      - 输出: 变量清单
#RJ|      - 验证: Stock/Flow区分明确
#PX|
#ZX|    Task 1.3: 参考模式绘制（3小时）
#YY|      - 输出: 时间序列图
#BP|      - 验证: 行为模式识别准确
#QZ|
#ZN|  Phase 2: 系统建模（2-3周）
#MY|    Task 2.1: 因果回路图CLD（1周）
#YX|      - 输出: CLD图文档
#KN|      - 验证: 反馈回路完整
#QR|
#ZY|    Task 2.2: Stock & Flow图SFD（1周）
#YX|      - 输出: SFD图文档
#HM|      - 验证: 存量流量结构正确
#RS|
#YY|    Task 2.3: 方程与参数（1周）
#WW|      - 输出: 完整方程清单
#HK|      - 验证: 单位一致、逻辑正确
#PT|
#JQ|  Phase 3: 仿真与分析（2-3周）
#PV|    Task 3.1: 模型校准（1周）
#WS|      - 输出: 校准后模型
#WV|      - 验证: 与历史数据拟合
#HM|
#YK|    Task 3.2: 行为模式重现（1周）
#HN|      - 输出: 模式重现报告
#WN|      - 验证: 参考模式重现
#TT|
#VV|    Task 3.3: 敏感性分析（1周）
#RM|      - 输出: 敏感性报告
#NB|      - 验证: 关键参数识别
#ZB|
#TW|  Phase 4: 干预设计（1-2周）
#XX|    Task 4.1: 杠杆点识别（3天）
#JW|      - 输出: 杠杆点分析
#QT|      - 验证: 干预效果预期
#NX|
#HZ|    Task 4.2: 政策情景测试（1周）
#VB|      - 输出: 多情景仿真结果
#TP|      - 验证: 情景对比清晰
#PN|
#MQ|    Task 4.3: 干预策略优化（4天）
#WH|      - 输出: 最优策略建议
#SJ|      - 验证: 策略可行性
#MR|```
#RT|
#BN|## 📋 任务分解规则
#QN|
#BS|### 四大原则
#VY|
#RS|1. **粒度可控原则**
#KS|   - 每个子任务必须在**一次会话**中完成
#QP|   - 单个任务不超过**3小时**
#WP|   - 任务间依赖关系明确
#VB|
#XP|2. **量化标准原则**
#TH|   - 每个子任务有**明确的完成标准**
#MR|   - 可验证的输出产物（模型、结果、报告）
#QW|   - 可测量的质量指标
#XH|
#RH|3. **独立验证原则**
#HZ|   - 每个子任务完成后**独立验证**
#XX|   - 验证清单（质量检查点）
#VW|   - 不合格返工机制
#XN|
#ZT|4. **模型透明原则**
#RQ|   - 子agent必须输出**完整的模型文档**
#ZM|   - 假设、方程、参数完全透明
#YW|   - 确保可复现性
#JR|
#KV|## 📚 渐进式加载结构
#MV|
#JV|### 第一层：核心执行规则（本文件）
#JM|
#XT|**技能激活时必读**，确保任务高质量执行：
#JW|- ⚠️ 六大绝对禁止原则
#HY|- 📋 任务分解规则
#QX|- ✅ 完成度验证清单
#NH|
#NZ|### 第二层：方法论文档（references/）
#ZK|
#NH|按需加载，深化方法论理解：
#YZ|
#BR|**modeling-tools.md**: 建模工具详解
#QW|- Vensim使用指南
#SW|- Stella建模方法
#NK|- Insight Maker在线工具
#QJ|- PySD Python实现
#BB|
#ST|**long-term-tasks.md**: 长时研究项目
#XH|- 公共卫生政策建模（4-6周）
#XX|- 供应链动态优化（3-4周）
#SS|- 环境可持续性分析（4-5周）
#KK|
#ZN|### 第三层：案例文档（cases/）
#PZ|
#VS|实战示范与警示：
#XJ|
#RM|**positive/**: 正确示范
#VJ|- case-001: 流行病传播建模
#YN|- case-002: 供应链牛鞭效应
#QP|
#NR|**negative/**: 错误警示
#PX|- case-001: 线性思维的错误
#PJ|- case-002: 忽视延迟的后果
#MY|
#PP|## ✅ 完成度验证清单
#WZ|
#QB|### 必须完成（100%）
#NQ|
#KY|- [ ] **六大禁止原则全部遵守**
#QX|  - [ ] 反馈思维（非线性）
#TZ|  - [ ] 延迟建模
#SJ|  - [ ] 反馈回路识别
#QX|  - [ ] 合理边界设定
#JP|  - [ ] 多情景分析
#QT|  - [ ] 模型校准验证
#PT|
#PS|- [ ] **模型质量**
#MH|  - [ ] Stock识别完整
#RZ|  - [ ] Flow建模准确
#RS|  - [ ] 反馈回路清晰
#ZV|  - [ ] 延迟适当
#TZ|
#BZ|- [ ] **分析质量**
#JR|  - [ ] 参考模式重现
#JR|  - [ ] 敏感性分析完成
#MQ|  - [ ] 情景测试充分
#BK|
#YJ|- [ ] **透明性**
#NZ|  - [ ] 完整的CLD/SFD图
#YR|  - [ ] 所有方程已文档化
#TZ|  - [ ] 参数来源透明
#XS|  - [ ] 模型可复现
#WJ|
#ZK|### 质量评估
#SV|
#ZX|| 维度 | 优秀(5) | 良好(4) | 合格(3) | 需改进(<3) |
#RN||------|----------|----------|----------|-------------|
#NQ|| **反馈思维** | 完全非线性 | 主要非线性 | minor线性 | 严重线性 |
#WB|| **延迟建模** | 完整延迟 | 主要延迟 | minor忽视 | 严重忽视 |
#RZ|| **反馈识别** | 所有回路 | 主要回路 | minor遗漏 | 严重遗漏 |
#VZ|| **边界设定** | 合理完整 | 主要合理 | minor过窄 | 严重过窄 |
#WN|| **多情景分析** | 充分测试 | 主要测试 | minor单一 | 严重单一 |
#YZ|| **模型校准** | 完全拟合 | 良好拟合 | minor偏差 | 严重偏差 |
#WZ|
#ZX|**及格线**: 每维度≥3分
#MH|
#VK|## 🎯 建模承诺书
#NB|
#MP|作为系统动力学专家，我承诺：
#WY|
#TP|1. **绝不线性思维**
#JY|   - 总是识别反馈回路
#JX|   - 考虑非线性关系
#JQ|   - 关注阈值和突变
#BX|
#JJ|2. **绝不忽视延迟**
#TJ|   - 建模物质延迟
#BZ|   - 建模信息延迟
#QK|   - 分析延迟对行为的影响
#YM|
#JX|3. **绝不忽视反馈**
#QV|   - 识别正反馈（增强回路）
#RW|   - 识别负反馈（平衡回路）
#ZB|   - 分析回路交互
#NP|
#PM|4. **绝不边界过窄**
#YB|   - 包含关键反馈
#XH|   - 考虑外生变量
#HW|   - 避免过度简化
#NX|
#NZ|5. **绝不在单一情景下结论**
#PP|   - 测试多种情景
#BQ|   - 进行敏感性分析
#HH|   - 报告不确定性
#NN|
#PN|
#RB|
#BK|## 详细指南
#ZT|
#RJ|完整的使用指南请参考: [详细指南](references/detailed-guide.md)