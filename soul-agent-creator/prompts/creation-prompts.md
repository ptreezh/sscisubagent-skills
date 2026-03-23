# Soul Agent Creator - 提示词库

用于引导用户完成 Soul Agent 创建的提示词模板。

---

## 需求澄清阶段

### prompt-clarify-research-field

```markdown
📋 需求澄清 - 研究领域

为了帮你创建最合适的方法论分身，我需要了解你的研究背景。

**请告诉我**：
1. 你所在的学科领域是什么？（如：社会学、管理学、教育学、传播学等）
2. 你的具体研究方向是什么？（如：组织行为、消费者行为、社会网络等）
3. 你目前的研究阶段？（如：课程学习、论文选题、数据收集、数据分析、论文写作）

根据你的回答，我会推荐最适合的方法论分身！
```

### prompt-clarify-methodology-preference

```markdown
📋 需求澄清 - 方法论偏好

了解了你的研究领域后，我来帮你选择合适的方法论。

**问题**：
1. 你更倾向于哪种研究范式？
   - 📖 质性研究（深入理解现象、建构理论）
   - 📊 定量研究（假设检验、统计分析）
   - 🔄 混合方法（结合两者优势）
   - 🧠 社会理论（理论分析和批判）

2. 你主要收集什么类型的数据？
   - 访谈/观察/文本（质性数据）
   - 问卷/实验/二手数据（定量数据）
   - 两者都有（混合数据）

3. 你之前接触过哪些研究方法？有特别感兴趣或想学习的吗？

请告诉我你的想法，我会据此推荐！
```

### prompt-clarify-use-scenario

```markdown
📋 需求澄清 - 使用场景

**问题**：
1. 你希望分身主要帮你解决什么问题？（可多选）
   - 数据分析（编码、统计、可视化）
   - 方法学习（理解方法论、操作步骤）
   - 论文写作（方法部分撰写、学术规范）
   - 研究设计（选择方法、设计流程）
   - 其他：____

2. 你期望的对话风格是？
   - 学术严谨（专业术语、规范表达）
   - 轻松友好（通俗易懂、耐心解释）
   - 简洁高效（直奔主题、少说废话）

3. 你需要分身集成哪些工具？
   - Python（数据分析、可视化）
   - R（统计分析）
   - Stata（计量经济分析）
   - 不需要工具集成

请告诉我你的需求！
```

---

## 技能推荐阶段

### prompt-recommend-skills

```markdown
📚 技能推荐

根据你的需求（{research_field}、{methodology_preference}、{use_scenario}），我推荐以下方法论分身：

**首选推荐**: {recommended_skill_1}
- 对标学者：{master_1}
- 核心能力：{capabilities_1}
- 适用场景：{applications_1}
- 推荐理由：{reason_1}

**备选推荐**: {recommended_skill_2}
- 对标学者：{master_2}
- 核心能力：{capabilities_2}
- 适用场景：{applications_2}
- 推荐理由：{reason_2}

**你更倾向于哪一个**？或者想了解更多细节？
```

### prompt-skill-comparison

```markdown
📊 技能对比

以下是两个技能的详细对比：

| 维度 | {skill_1_name} | {skill_2_name} |
|------|---------------|---------------|
| 对标学者 | {master_1} | {master_2} |
| 哲学基础 | {philosophy_1} | {philosophy_2} |
| 核心概念 | {concepts_1} | {concepts_2} |
| 数据类型 | {data_type_1} | {data_type_2} |
| 分析重点 | {focus_1} | {focus_2} |
| 学习曲线 | {difficulty_1} | {difficulty_2} |

**选择建议**：
- 如果你的数据是____，选择 {skill_1_name}
- 如果你想____，选择 {skill_2_name}

你更倾向于哪一个？
```

---

## 配置确认阶段

### prompt-confirm-configuration

```markdown
📋 分身配置确认

根据你的需求，我为你定制了以下配置：

**基本信息**
- 分身名称：{custom_name}
- 对标学者：{master}
- 方法论：{methodology}
- 研究领域：{field}

**核心能力**
- {capability_1}
- {capability_2}
- {capability_3}

**对话风格**
- 风格：{communication_style}
- 详细程度：{detail_level}
- 正式程度：{formality}

**存储位置**
- 路径：~/.stigmergy/soul-agents/{soul_id}/

**确认以上配置**？
- 回复"确认"或"y"开始创建
- 回复"修改"调整配置
```

### prompt-modify-configuration

```markdown
✏️ 修改配置

好的，请告诉我你想修改什么：

1. **分身名称** - 当前：{current_name}
2. **对标学者** - 当前：{current_master}
3. **对话风格** - 当前：{current_style}
4. **核心能力** - 当前：{current_capabilities}
5. **其他定制需求**

请告诉我具体想修改哪一项，或者直接说你的新需求！
```

---

## 创建执行阶段

### prompt-creating-soul

```markdown
🔨 正在创建分身...

📁 创建目录结构：{output_dir}
  ✅ 创建：SOUL.md
  ✅ 创建：SOUL_CONFIG.yaml
  ✅ 创建：METHODOLOGY.md
  ✅ 创建：README.md
  ✅ 创建：metadata.json
  ✅ 创建：memory/ & evolution/

🎉 分身创建完成！
```

---

## 激活指导阶段

### prompt-activation-guide

```markdown
✅ Soul Agent 创建成功！

📋 分身信息
- Soul ID: {soul_id}
- 名称：{display_name}
- 对标：{master}
- 路径：{storage_path}

🚀 激活方式

**方式 1: 环境变量**
```bash
export SOUL_AGENT_ID="{soul_id}"
```

**方式 2: 直接指定配置**
```bash
opencode --soul-config {storage_path}/SOUL.md
```

**方式 3: Stigmergy 调用**
```bash
stigmergy use soul {soul_id}
```

📖 下一步
1. 查看生成的文件：{storage_path}/SOUL.md
2. 根据需要修改配置：{storage_path}/SOUL_CONFIG.yaml
3. 在 OpenClaw/CLI 中激活分身
4. 开始与你的学术分身对话！

有任何问题随时问我！
```

---

## 快速创建模式

### prompt-quick-create

```markdown
⚡ 快速创建模式

好的！我将为你创建一个{skill_name}分身，使用默认配置：

- 分身名称：{skill_name}
- 对标学者：{master}
- 核心能力：{capabilities}
- 对话风格：学术严谨
- 存储位置：~/.stigmergy/soul-agents/{soul_id}/

确认创建？(回复"确认"或"y"即可)
```

---

## 错误处理

### prompt-error-unknown-skill

```markdown
❌ 未知的技能 ID: {skill_id}

可用的方法论分身包括：

📖 质性研究方法
  • grounded-theory - 扎根理论专家
  • actor-network-theory - 行动者网络理论专家
  • bourdieu-field-analysis - 布迪厄场域分析专家

📊 定量研究方法
  • social-network-analysis - 社会网络分析专家
  • qca-analysis - 定性比较分析专家
  • did-analysis - 双重差分分析专家

🔄 混合研究方法
  • mixed-methods - 混合方法研究专家

🧠 社会理论视角
  • digital-marxism - 数字马克思分析专家
  • digital-durkheim - 数字涂尔干分析专家
  • digital-weber - 数字韦伯分析专家

请告诉我你想创建哪个分身，或者输入技能 ID（如：grounded-theory）
```

### prompt-error-creation-failed

```markdown
❌ 创建失败

错误信息：{error_message}

**可能的原因**：
1. 目录权限问题
2. 磁盘空间不足
3. 模板文件缺失

**解决方案**：
1. 检查目录权限：确保 ~/.stigmergy/soul-agents/ 可写
2. 检查磁盘空间
3. 重新运行创建命令

如果问题持续，请联系技术支持。
```

---

*提示词库版本：1.0.0*
*最后更新：2026-03-22*
