# 快速启动指南

**5 分钟内部署并测试社会科学方法论 skill 进化系统！**

---

## ⚡ 快速部署（5 分钟）

### 步骤 1: 安装进化引擎扩展（1 分钟）

```bash
# 复制扩展文件
xcopy /E /I "D:\socienceAI\agentskills\extensions\skill-evolution" "%USERPROFILE%\.qwen\extensions\skill-evolution"

# 验证
dir "%USERPROFILE%\.qwen\extensions\skill-evolution"
```

### 步骤 2: 配置 Qwen CLI（1 分钟）

编辑 `%USERPROFILE%\.qwen\config.yaml`，添加：

```yaml
extensions:
  enabled:
    - skill-evolution
```

### 步骤 3: 复制 skill（1 分钟）

```bash
# 复制 grounded-theory-expert
xcopy /E /I "D:\socienceAI\agentskills\grounded-theory-expert" "%USERPROFILE%\.qwen\skills\grounded-theory-expert"

# 复制 social-network-analysis-expert
xcopy /E /I "D:\socienceAI\agentskills\social-network-analysis-expert" "%USERPROFILE%\.qwen\skills\social-network-analysis-expert"

# 验证
dir "%USERPROFILE%\.qwen\skills"
```

### 步骤 4: 启动测试（2 分钟）

```bash
# 启动 Qwen CLI
qwen

# 应该看到：
# [SkillEvolution] 进化引擎初始化...
# [SkillEvolution] 已加载 2 个 skill
```

---

## 🧪 快速测试

### 测试 1: 验证 soul.md 加载

在 Qwen CLI 中输入：

```
你是 grounded-theory-expert 吗？
```

应该看到类似回答：

```
是的，我是 grounded-theory-expert（扎根理论分析专家）。

我的使命是让扎根理论研究方法更加规范、严谨、易于应用。

我专注于：
- Glaser & Strauss (1967) 经典扎根理论
- Strauss & Corbin (1990) 程序化扎根理论
- Charmaz (2006) 建构型扎根理论
```

### 测试 2: 验证教训记录

执行一个任务后，检查：

```bash
type "%USERPROFILE%\.qwen\skills\grounded-theory-expert\lesson-memory.md"
```

应该看到新记录的教训。

### 测试 3: 验证案例积累

如果有成功案例，检查：

```bash
dir "%USERPROFILE%\.qwen\skills\grounded-theory-expert\case-library\successful-cases"
```

应该看到案例文件。

---

## 🔧 故障排查

### 问题：没有看到 [SkillEvolution] 日志

**解决**：

```bash
# 检查扩展是否安装
dir "%USERPROFILE%\.qwen\extensions"

# 检查 config.yaml
type "%USERPROFILE%\.qwen\config.yaml"
```

### 问题：skill 未找到

**解决**：

```bash
# 检查 skill 目录
dir "%USERPROFILE%\.qwen\skills"

# 重新复制
xcopy /E /I "D:\socienceAI\agentskills\grounded-theory-expert" "%USERPROFILE%\.qwen\skills\grounded-theory-expert"
```

---

## ✅ 验证清单

部署完成后，检查：

- [ ] 扩展已安装到 `%USERPROFILE%\.qwen\extensions\skill-evolution\`
- [ ] config.yaml 已配置 extensions
- [ ] skill 已复制到 `%USERPROFILE%\.qwen\skills\`
- [ ] 启动 Qwen CLI 看到 [SkillEvolution] 日志
- [ ] soul.md 已加载（skill 能正确介绍自己）
- [ ] lesson-memory.md 可以写入

---

## 🎯 下一步

部署成功后：

1. **使用 skill 进行分析**
   ```
   使用扎根理论分析以下访谈数据...
   ```

2. **查看进化状态**
   ```bash
   type "%USERPROFILE%\.qwen\skills\grounded-theory-expert\lesson-memory.md"
   ```

3. **每 10 次会话后查看进化报告**
   ```bash
   type "%USERPROFILE%\.qwen\skills\grounded-theory-expert\evolution-report.md"
   ```

---

**部署完成！开始使用吧！** 🚀
