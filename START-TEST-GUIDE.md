# Qwen CLI Skill 真实环境测试 - 启动指南

**快速开始**: 5 分钟内开始测试

---

## ⚡ 步骤 1: 部署 skill 和扩展（2 分钟）

**运行部署脚本**:
```bash
cd D:\socienceAI\agentskills
deploy-for-test.bat
```

**部署内容**:
- ✅ 2 个扩展（skill-evolution, skill-task-integration）
- ✅ 13 个 skill
- ✅ Qwen CLI 配置

---

## ⚡ 步骤 2: 重启 Qwen CLI（如果需要）

**如果已经在 Qwen CLI 中**:

输入：
```
/exit
```

然后重新启动：
```bash
qwen
```

**应该看到**:
```
[SkillEvolution] 进化引擎初始化...
[SkillEvolution] 已加载 13 个 skill
[SkillTaskIntegration] 任务集成扩展初始化...
```

---

## ⚡ 步骤 3: 开始测试（1 分钟）

**测试第 1 个 skill**:

输入：
```
你是 grounded-theory-expert 吗？请介绍一下你的角色和能力。
```

**预期回答**:
```
是的，我是 grounded-theory-expert（扎根理论分析专家）。

我的使命是让扎根理论研究方法更加规范、严谨、易于应用。

我专注于：
- Glaser & Strauss (1967) 经典扎根理论
- Strauss & Corbin (1990) 程序化扎根理论
- Charmaz (2006) 建构型扎根理论

我支持自主进化机制，会记录每次分析的教训，积累成功案例。
```

---

## ⚡ 步骤 4: 提出复杂任务

**输入**:
```
我正在进行一项用户满意度研究，收集了 20 份深度访谈记录（每份 1000-1500 字）。

请你对这些访谈数据进行扎根理论分析，建构用户满意度理论模型。

要求：
1. 执行完整的开放性编码、轴心编码、选择式编码
2. 计算编码者间信度（Cohen's Kappa > 0.7）
3. 进行理论饱和度检验（多维度）
4. 生成理论命题
5. 生成研究报告

请自动分解这个任务，创建任务计划，并执行分析。
```

**观察点**:
- ✅ 是否自动分解为多个 Phase
- ✅ 是否创建 task_plan.md
- ✅ 分解是否合理
- ✅ 是否遵循专业规范

---

## ⚡ 步骤 5: 记录测试结果

**打开测试记录模板**:
```bash
notepad test-record-template.md
```

**填写**:
- 测试日期
- 技能名称
- 任务描述
- 观察结果
- 评分

---

## 📋 测试顺序

**第 1 批** (现在):
1. grounded-theory-expert ← **当前测试**
2. social-network-analysis-expert

**第 2 批** (稍后):
3. bourdieu-field-analysis-expert
4. msqca-analysis-expert

**第 3 批**:
5. did-analysis-expert
6. data-analysis-expert

... (共 7 批)

---

## 🔄 如果重启 Qwen CLI

**重启后继续测试**:

输入：
```
继续 Skill 真实环境测试计划。

当前测试进度：
- 已完成：grounded-theory-expert
- 当前测试：social-network-analysis-expert
- 待测试：其他 11 个 skill

请继续测试。
```

---

## 📊 测试记录

**每个 skill 完成后**:
1. 填写 test-record-template.md
2. 保存到 `test-records/{skill-name}-test-record.md`
3. 计算评分
4. 给出评级

**汇总报告**:
- 完成所有 13 个 skill 后
- 生成 SKILL-TEST-SUMMARY.md
- 生成 SKILL-TEST-RANKING.md

---

## ✅ 质量保障

**测试原则**:
- ✅ 质量第一，绝不妥协
- ✅ 真实 CLI 环境测试
- ✅ 严格评分
- ✅ 详细记录

**如果 skill 失败**:
- 记录失败原因
- 评分为实际得分
- 提出改进建议
- **不降低测试标准**

---

## 🎯 成功标准

**测试成功的标志**:
1. ✅ 所有 13 个 skill 都完成测试
2. ✅ 每个 skill 都有详细测试记录
3. ✅ 生成汇总报告和排名
4. ✅ 提出改进建议

---

## 📞 需要帮助

**如果遇到问题**:

1. **skill 未加载**:
   ```bash
   # 检查部署
   dir "%USERPROFILE%\.qwen\skills"
   
   # 重新部署
   deploy-for-test.bat
   ```

2. **扩展未工作**:
   ```bash
   # 检查扩展
   dir "%USERPROFILE%\.qwen\extensions"
   
   # 检查配置
   type "%USERPROFILE%\.qwen\config.yaml"
   ```

3. **测试记录问题**:
   - 查看 test-record-template.md
   - 按照模板填写

---

**准备就绪！开始测试吧！** 🚀

**当前状态**: 准备开始测试 grounded-theory-expert

**下一步**: 在 Qwen CLI 中输入测试问题
