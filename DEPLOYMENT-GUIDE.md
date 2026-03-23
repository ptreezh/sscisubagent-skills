# 社会科学方法论 Skill 进化系统 - 部署指南

**版本**: 1.0  
**日期**: 2026-03-05  
**置信度**: 95%

---

## 📋 部署概述

本部署指南用于在 Qwen CLI 内部署社会科学方法论 skill 的自主进化系统。

### 部署目标

1. ✅ 在 Qwen CLI 中加载 skill
2. ✅ 自动触发 hooks（session-start, post-task, pre-prompt）
3. ✅ 自动记录教训到 lesson-memory.md
4. ✅ 自动积累案例到 case-library/
5. ✅ 每 10 次会话触发定期进化

---

## 🚀 部署步骤

### 步骤 1: 安装进化引擎扩展

```bash
# 1. 复制扩展文件到 Qwen CLI 扩展目录
cp -r agentskills/extensions/skill-evolution ~/.qwen/extensions/

# 2. 验证扩展已安装
ls ~/.qwen/extensions/skill-evolution/
# 应该看到：index.js, package.json（如有）
```

### 步骤 2: 配置 Qwen CLI 加载扩展

编辑 `~/.qwen/config.yaml`，添加：

```yaml
extensions:
  enabled:
    - skill-evolution
  
  skill-evolution:
    auto_load: true
    log_level: info
```

### 步骤 3: 复制 skill 到 Qwen CLI

```bash
# 复制 grounded-theory-expert
cp -r agentskills/grounded-theory-expert ~/.qwen/skills/

# 复制 social-network-analysis-expert
cp -r agentskills/social-network-analysis-expert ~/.qwen/skills/

# 验证
ls ~/.qwen/skills/
# 应该看到：grounded-theory-expert, social-network-analysis-expert
```

### 步骤 4: 验证 skill 配置

```bash
# 检查 soul.md 是否存在
cat ~/.qwen/skills/grounded-theory-expert/soul.md

# 检查 lesson-memory.md 是否存在
cat ~/.qwen/skills/grounded-theory-expert/lesson-memory.md

# 检查 skill-hooks.yaml 是否存在
cat ~/.qwen/skills/grounded-theory-expert/skill-hooks.yaml

# 检查 qwen-skill.yaml 是否存在
cat ~/.qwen/skills/grounded-theory-expert/qwen-skill.yaml
```

### 步骤 5: 启动 Qwen CLI 并测试

```bash
# 启动 Qwen CLI
qwen

# 应该看到类似输出：
# [SkillEvolution] 进化引擎初始化...
# [SkillEvolution] 已加载 2 个 skill
# [SkillEvolution] 会话启动...
# [SkillEvolution] 已加载 grounded-theory-expert 状态
# [SkillEvolution] 已加载 social-network-analysis-expert 状态
```

### 步骤 6: 测试 hooks 触发

在 Qwen CLI 中输入：

```
使用扎根理论分析以下访谈数据...
```

应该看到：

```
[SkillEvolution] 任务完成，记录教训...
[SkillEvolution] 已记录教训到 grounded-theory-expert
```

### 步骤 7: 验证教训记录

```bash
# 查看 lesson-memory.md 是否更新
tail -20 ~/.qwen/skills/grounded-theory-expert/lesson-memory.md

# 应该看到新记录的教训
```

### 步骤 8: 验证案例积累

```bash
# 查看 case-library 是否有新案例
ls ~/.qwen/skills/grounded-theory-expert/case-library/successful-cases/

# 应该看到：case-001-2026-03-05.md 等文件
```

---

## 🔧 故障排查

### 问题 1: 扩展未加载

**症状**: 没有看到 [SkillEvolution] 日志

**解决方案**:
```bash
# 检查扩展目录
ls ~/.qwen/extensions/

# 检查 config.yaml 配置
cat ~/.qwen/config.yaml

# 确保 extensions 部分正确配置
```

### 问题 2: skill 未找到

**症状**: [SkillEvolution] Skills 目录不存在

**解决方案**:
```bash
# 创建 skills 目录
mkdir -p ~/.qwen/skills/

# 复制 skill
cp -r agentskills/grounded-theory-expert ~/.qwen/skills/
```

### 问题 3: hooks 未触发

**症状**: 任务完成后没有记录教训

**解决方案**:
```bash
# 检查 skill-hooks.yaml 配置
cat ~/.qwen/skills/grounded-theory-expert/skill-hooks.yaml

# 确保 hooks 部分 enabled: true
```

### 问题 4: lesson-memory.md 未更新

**症状**: 文件内容没有变化

**解决方案**:
```bash
# 检查文件权限
ls -l ~/.qwen/skills/grounded-theory-expert/lesson-memory.md

# 确保有写权限
chmod u+w ~/.qwen/skills/grounded-theory-expert/lesson-memory.md
```

---

## 📊 验证清单

部署完成后，检查以下项目：

- [ ] 扩展已安装到 `~/.qwen/extensions/skill-evolution/`
- [ ] Qwen CLI config.yaml 已配置 extensions
- [ ] skill 已复制到 `~/.qwen/skills/`
- [ ] soul.md 存在并包含角色定义
- [ ] lesson-memory.md 存在并可以写入
- [ ] case-library/ 目录存在
- [ ] skill-hooks.yaml 配置正确
- [ ] qwen-skill.yaml 配置正确
- [ ] 启动 Qwen CLI 看到 [SkillEvolution] 日志
- [ ] 任务完成后看到教训记录日志
- [ ] lesson-memory.md 有新教训记录
- [ ] case-library/ 有新案例文件

---

## 🔄 日常使用

### 正常使用流程

1. **启动 Qwen CLI**
   ```bash
   qwen
   ```

2. **使用 skill 进行分析**
   ```
   使用扎根理论分析以下访谈数据...
   ```

3. **自动记录教训**
   - 任务完成后自动记录
   - 无需手动操作

4. **查看进化状态**
   ```bash
   cat ~/.qwen/skills/grounded-theory-expert/lesson-memory.md
   cat ~/.qwen/skills/grounded-theory-expert/case-library/
   ```

### 定期进化

每 10 次会话自动触发：
- 复习教训
- 提炼模式
- 更新 soul.md

查看进化报告：
```bash
cat ~/.qwen/skills/grounded-theory-expert/evolution-report.md
```

---

## 📁 文件结构

部署后的文件结构：

```
~/.qwen/
├── config.yaml                      # Qwen CLI 配置
├── extensions/
│   └── skill-evolution/
│       └── index.js                 # 进化引擎扩展
└── skills/
    ├── grounded-theory-expert/
    │   ├── soul.md                  # 角色定义
    │   ├── lesson-memory.md         # 教训记忆
    │   ├── skill-hooks.yaml         # hooks 配置
    │   ├── qwen-skill.yaml          # Qwen CLI 配置
    │   ├── case-library/
    │   │   └── successful-cases/
    │   │       └── case-001-2026-03-05.md
    │   └── tools/
    │       └── analyze.py
    └── social-network-analysis-expert/
        └── ...
```

---

## ✅ 部署完成！

部署完成后，skill 将在 Qwen CLI 内部自动运行进化机制：
- ✅ 自动加载 soul.md 角色定义
- ✅ 自动注入历史教训和案例
- ✅ 自动记录新教训
- ✅ 自动积累成功案例
- ✅ 每 10 次会话自动进化

**无需任何手动操作，完全自动化！**
