# Stigmergy集成指南

## 🎯 概述

Stigmergy是一个多AI CLI协作系统，提供统一的技能管理和跨CLI路由功能。本指南详细介绍如何将SSCI技能包与Stigmergy集成，实现最佳的多CLI协作体验。

## 🚀 快速开始

### 安装Stigmergy
```bash
# 安装Stigmergy CLI
npm install -g stigmergy

# 验证安装
stigmergy --version
```

### 系统诊断
```bash
# 完整系统诊断
stigmergy diagnostic

# 检查CLI工具状态
stigmergy status

# 扫描可用AI CLI工具
stigmergy scan
```

## 📦 技能管理

### 安装技能到Stigmergy

#### 方法1：从本地复制（推荐）
```bash
# 复制所有技能到Stigmergy
cp -r skills/* ~/.stigmergy/skills/

# 验证技能安装
stigmergy skill list
```

#### 方法2：从GitHub安装
```bash
# 从GitHub仓库安装
stigmergy skill install anthropics/skills

# 安装特定技能
stigmergy skill install claude-ai/pdf
```

#### 方法3：从本地仓库安装
```bash
# 初始化本地仓库
cd skills
git init
git add .
git commit -m "Initial commit"

# 安装到Stigmergy
stigmergy skill install local:ssci-skills
```

### 技能同步
```bash
# 同步到所有CLI配置
stigmergy skill sync

# 强制同步（覆盖现有配置）
stigmergy skill sync --force

# 仅同步到特定CLI
stigmergy skill sync --target claude,qwen
```

## 🔄 跨CLI调用

### 基础调用模式

#### 1. 直接路由到指定CLI
```bash
# 在Claude中执行任务
stigmergy claude "请帮我进行开放编码分析"

# 在Qwen中执行任务
stigmergy qwen "请计算网络中心性指标"

# 在Gemini中执行任务
stigmergy gemini "请帮我进行文献检索"
```

#### 2. 智能路由（自动选择最佳CLI）
```bash
# 自动选择最适合的CLI
stigmergy call "进行复杂的社会网络分析"
stigmergy call "处理跨学科文献综述"
stigmergy call "生成统计分析报告"
```

#### 3. 跨CLI协作
```bash
# Claude处理数据，Qwen验证结果
stigmergy use claude to "分析访谈数据" | stigmergy use qwen to "统计验证结果"

# 多步骤协作流程
stigmergy use gemini to "检索相关文献" \
  | stigmergy use claude to "文献内容分析" \
  | stigmergy use qwen to "生成综述报告"
```

### 高级调用模式

#### 1. 条件路由
```bash
# 基于任务类型自动选择
stigmergy call --condition "coding" "编写Python分析代码"
stigmergy call --condition "analysis" "进行统计分析"
stigmergy call --condition "writing" "撰写学术报告"
```

#### 2. 并行执行
```bash
# 并行执行多个任务
stigmergy call --parallel "分析数据集A" "分析数据集B" "生成对比报告"
```

#### 3. 管道操作
```bash
# 创建处理管道
data.json | stigmergy call "数据分析" | stigmergy call "可视化" | stigmergy call "报告生成"
```

## 🎛️ 智能体调用

### 直接调用智能体
```bash
# 在指定CLI中调用智能体
stigmergy use claude "使用文献管理专家查找最新研究"
stigmergy use qwen "使用扎根理论专家分析数据"
stigmergy use gemini "使用场域分析专家研究教育场域"
```

### 跨CLI智能体调用
```bash
# 在Claude中使用Qwen的智能体
stigmergy use claude "请使用qwen的扎根理论专家功能"

# 在Qwen中使用Claude的智能体
stigmergy use qwen "请调用claude的文献管理专家"

# 智能体协作
stigmergy use claude "使用sna-expert分析网络" | \
stigmergy use qwen "使用grounded-theory-expert编码分析结果"
```

## 🔧 配置管理

### CLI配置文件
Stigmergy会为每个CLI生成专门的配置文件：

#### Claude配置 (`~/.claude/claude.md`)
```yaml
skills_system priority="1"
<usage>
Stigmergy统一技能系统管理
- stigmergy skill read <skill-name>
- stigmergy use <cli-name> skill <skill-name>
- stigmergy call skill <skill-name>
</usage>
```

#### Qwen配置 (`~/.qwen/qwen.md`)
```yaml
skills_system priority="1"
<usage>
Stigmergy技能调用系统
- Bash("stigmergy skill read <name>")
- Bash("stigmergy use <cli> skill <name>")
</usage>
```

### 技能优先级配置
```bash
# 设置技能优先级
stigmergy config set priority.claude high
stigmergy config set priority.qwen medium

# 设置默认CLI
stigmergy config set default.cli claude

# 设置路由规则
stigmergy config set routing.analysis claude
stigmergy config set routing.writing qwen
```

## 📊 监控和诊断

### 系统状态监控
```bash
# 实时监控
stigmergy monitor --real-time

# 系统健康检查
stigmergy health-check

# 性能统计
stigmergy stats --detailed
```

### 日志管理
```bash
# 查看实时日志
stigmergy logs --follow

# 查看错误日志
stigmergy logs --level error

# 查看特定CLI日志
stigmergy logs --cli claude
```

### 技能使用统计
```bash
# 技能使用统计
stigmergy stats --skills

# CLI使用统计
stigmergy stats --clis

# 跨CLI调用统计
stigmergy stats --cross-cli
```

## 🛠️ 高级功能

### 技能市场
```bash
# 搜索技能
stigmergy skill search "社会网络分析"

# 安装技能
stigmergy skill install user/network-analysis-skill

# 发布技能
stigmergy skill publish --name my-skill

# 评价技能
stigmergy skill rate network-analysis-skill --stars 5
```

### 工作流管理
```bash
# 创建工作流
stigmergy workflow create "研究分析流程"

# 执行工作流
stigmergy workflow run "研究分析流程" --data interview.json

# 列出工作流
stigmergy workflow list
```

### 自动化任务
```bash
# 设置定时任务
stigmergy schedule add "daily-literature-review" "0 9 * * *" "stigmergy call '检查最新文献'"

# 设置触发器
stigmergy trigger add "new-data" "stigmergy call '自动分析新数据'"
```

## 🔧 故障排除

### 常见问题解决

#### 1. 技能同步失败
```bash
# 检查Stigmergy状态
stigmergy status

# 重新同步
stigmergy skill sync --force

# 检查权限
stigmergy perm-check
```

#### 2. 跨CLI调用失败
```bash
# 检查CLI可用性
stigmergy scan

# 重新部署集成
stigmergy deploy

# 查看详细错误
stigmergy logs --tail 50
```

#### 3. 智能体调用异常
```bash
# 检查智能体配置
stigmergy config list --agents

# 重新同步智能体
stigmergy sync --agents

# 测试智能体调用
stigmergy test agent literature-expert
```

### 性能优化

#### 1. 缓存优化
```bash
# 清理缓存
stigmergy clean

# 配置缓存策略
stigmergy config set cache.ttl 3600
stigmergy config set cache.max-size 1GB
```

#### 2. 并发优化
```bash
# 设置并发限制
stigmergy config set concurrency.max 5

# 启用连接池
stigmergy config set pool.enabled true
```

## 📈 最佳实践

### 1. 技能组织
- 按功能域组织技能
- 使用清晰的命名规范
- 提供详细的触发条件

### 2. CLI选择策略
- Claude：适合复杂分析和写作任务
- Qwen：适合数据处理和统计分析
- Gemini：适合文献检索和知识问答
- iFlow：适合中文本土化研究

### 3. 工作流设计
- 使用模块化设计
- 合理分配任务到不同CLI
- 建立错误处理机制

### 4. 监控和维护
- 定期检查系统状态
- 监控技能使用情况
- 及时更新和优化配置

## 🎯 使用场景示例

### 场景1：完整研究流程
```bash
# 1. 文献检索（Gemini）
stigmergy use gemini "检索社会网络分析相关文献"

# 2. 文献分析（Claude）
stigmergy use claude "分析文献内容，识别研究 gap"

# 3. 数据收集（Qwen）
stigmergy use qwen "收集和处理网络数据"

# 4. 数据分析（Claude）
stigmergy use claude "使用sna-expert进行网络分析"

# 5. 结果验证（Qwen）
stigmergy use qwen "统计分析分析结果"

# 6. 报告撰写（Claude）
stigmergy use claude "基于分析结果撰写研究报告"
```

### 场景2：团队协作
```bash
# 研究者A：数据收集
stigmergy use qwen "收集访谈数据并整理"

# 研究者B：编码分析
stigmergy use claude "使用grounded-theory-expert进行编码"

# 研究者C：网络分析
stigmergy use claude "使用sna-expert分析网络结构"

# 整合分析
stigmergy call "整合多源数据，生成综合分析报告"
```

## 📚 相关资源

- [Stigmergy官方文档](https://github.com/ptreezh/stigmergy-CLI-Multi-Agents)
- [agentskills.io标准](https://agentskills.io)
- [OpenSkills生态](https://github.com/numman-ali/openskills)
- [SSCI技能包仓库](https://github.com/ssci-subagent-skills/ssci-subagent-skills)

---

*通过Stigmergy实现真正的多CLI协作，让AI研究工具发挥最大效能！* 🚀