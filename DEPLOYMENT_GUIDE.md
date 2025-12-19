# 中文社会科学研究技能部署指南

## 🎯 项目概述

本项目提供完整的中文社会科学研究AI技能包，支持7个主流AI CLI工具，兼容agentskills.io标准，提供3种部署方案。所有技能都符合渐进式信息披露原则，包含Python辅助工具和完整的测试覆盖。

## 🚀 快速部署（推荐）

### 方案1：一键部署（最简单）
```bash
# 1. 安装npm包
npm install -g ssci-subagent-skills

# 2. 一键部署到所有CLI
ssci deploy --all

# 3. 验证部署状态
ssci status
```

### 方案2：Stigmergy统一管理（最强大）
```bash
# 1. 安装Stigmergy CLI
npm install -g stigmergy

# 2. 复制技能到Stigmergy
cp -r skills/* ~/.stigmergy/skills/

# 3. 同步到所有CLI
stigmergy skill sync

# 4. 测试跨CLI调用
stigmergy call "进行开放编码分析"
```

### 方案3：手动部署（最灵活）
```bash
# 部署到特定CLI
ssci deploy claude    # Claude Code
ssci deploy qwen      # Qwen CLI
ssci deploy gemini    # Gemini CLI
ssci deploy iflow     # iFlow CLI
ssci deploy codebuddy # CodeBuddy CLI
ssci deploy codex     # Codex CLI
ssci deploy qodercli  # QoderCLI
```

## 📋 支持的AI CLI工具

| CLI工具 | 版本 | 部署状态 | 技能识别 | 推荐度 |
|---------|------|----------|----------|--------|
| **Claude Code** | 2.0.73 | ✅ 完全支持 | ✅ 13/13 | ⭐⭐⭐⭐⭐ |
| **Qwen CLI** | 0.5.0 | ✅ 完全支持 | ✅ 13/13 | ⭐⭐⭐⭐⭐ |
| **iFlow CLI** | 0.4.7 | ✅ 完全支持 | ✅ 13/13 | ⭐⭐⭐⭐ |
| **Gemini CLI** | 0.21.0 | ✅ 完全支持 | ✅ 13/13 | ⭐⭐⭐⭐ |
| **CodeBuddy CLI** | 2.20.1 | ✅ 完全支持 | ⚠️ 需适配 | ⭐⭐⭐ |
| **Codex CLI** | 0.73.0 | ✅ 完全支持 | ⚠️ 需适配 | ⭐⭐⭐ |
| **QoderCLI** | 0.1.15 | ✅ 完全支持 | ❌ 需登录 | ⭐⭐ |

## 🔧 详细部署方案

### 方案A：原生部署（npm包）

#### 1. 安装npm包
```bash
# 全局安装
npm install -g ssci-subagent-skills

# 验证安装
ssci --version
```

#### 2. 自动部署
```bash
# 部署到所有可用CLI
ssci deploy --all

# 或部署到特定CLI
ssci deploy claude
ssci deploy qwen
ssci deploy gemini
```

#### 3. 验证部署
```bash
# 检查部署状态
ssci status

# 测试技能调用
claude "请帮我进行开放编码分析"
qwen "请计算网络中心性"
```

### 方案B：Stigmergy统一管理

#### 1. 安装Stigmergy
```bash
# 安装Stigmergy CLI
npm install -g stigmergy

# 验证安装
stigmergy --version
```

#### 2. 系统诊断
```bash
# 系统诊断
stigmergy diagnostic

# 检查CLI状态
stigmergy status

# 扫描可用工具
stigmergy scan
```

#### 3. 技能管理
```bash
# 复制技能到Stigmergy
cp -r skills/* ~/.stigmergy/skills/

# 同步到所有CLI
stigmergy skill sync

# 列出可用技能
stigmergy skill list

# 读取特定技能
stigmergy skill read performing-open-coding
```

#### 4. 跨CLI调用
```bash
# 指定CLI执行
stigmergy use claude "进行编码分析"
stigmergy use qwen "进行统计分析"

# 智能路由
stigmergy call "复杂网络分析"

# 跨CLI协作
stigmergy use claude to "处理数据" | stigmergy use qwen to "验证结果"
```

### 方案C：OpenSkills适配器

#### 1. 使用通用适配器
```bash
# 为特定CLI生成适配配置
node adapters/openskills-universal-adapter.js --cli qwen
node adapters/openskills-universal-adapter.js --cli gemini
node adapters/openskills-universal-adapter.js --cli codebuddy
```

#### 2. 手动适配
```bash
# 生成CLI特定配置
npm run deploy:qwen-auto
npm run deploy:gemini-auto
npm run deploy:codebuddy-auto
```

#### 3. 验证适配
```bash
# 测试技能识别
qwen -p "列出可用技能"
gemini -p "测试技能加载"
codebuddy -p "验证技能功能"
```

## 📊 部署验证

### 验证清单
- [ ] npm包安装成功
- [ ] CLI工具检测正常
- [ ] 技能文件复制完整
- [ ] 配置文件生成正确
- [ ] 技能识别测试通过
- [ ] 跨CLI调用正常

### 自动化验证脚本
```bash
# 运行完整验证
npm run validate:deployment

# 测试所有CLI
npm run test:all-clis

# 生成验证报告
npm run report:deployment
```

## 🔧 高级配置

### 自定义部署路径
```bash
# 指定自定义路径
ssci deploy --target /custom/path/skills

# 使用配置文件
ssci deploy --config custom-config.json
```

### 选择性部署
```bash
# 仅部署智能体
ssci deploy --agents-only

# 仅部署技能
ssci deploy --skills-only

# 部署特定类别
ssci deploy --category coding
ssci deploy --category analysis
```

### 批量部署
```bash
# 批量部署到多个环境
ssci deploy --env dev,test,prod

# 并行部署
ssci deploy --parallel
```

## 🚨 故障排除

### 常见问题

#### 1. CLI检测失败
```bash
# 手动检查CLI
claude --version
qwen --version
gemini --version

# 重新检测
ssci scan --force
```

#### 2. 权限问题
```bash
# Windows权限修复
stigmergy fix-perms

# Linux/Mac权限修复
sudo chmod -R 755 ~/.claude ~/.qwen ~/.gemini
```

#### 3. 技能识别失败
```bash
# 重新同步
stigmergy skill sync --force

# 重新部署
ssci deploy --force claude
```

#### 4. 中文编码问题
```bash
# 检查编码设置
stigmergy diagnostic --encoding

# 重新生成配置
stigmergy skill sync --encoding utf8
```

### 性能优化

#### 1. 缓存清理
```bash
# 清理Stigmergy缓存
stigmergy clean

# 清理npm缓存
npm cache clean --force
```

#### 2. 并行部署
```bash
# 启用并行部署
ssci deploy --parallel --max-jobs 4
```

## 📈 监控和维护

### 部署监控
```bash
# 实时监控
ssci monitor --real-time

# 生成报告
ssci report --deployment --format html
```

### 定期维护
```bash
# 自动更新
ssci upgrade --auto

# 健康检查
ssci health-check
```

---

*选择适合你的部署方案，让AI成为中文社会科学研究的强大助手！* 🚀

## 🔧 技能验证

### 运行验证工具
```bash
cd sscisubagent-skills
python validate_skills.py
```

### 检查清单
- [ ] 所有技能都有有效的YAML frontmatter
- [ ] 技能名称符合规范（小写字母、数字、连字符）
- [ ] 描述明确说明使用时机
- [ ] 技能内容结构清晰
- [ ] 辅助脚本可正常运行

## 📋 技能清单

### 编码类技能 (5个)
1. **performing-open-coding** - 开放编码
2. **performing-axial-coding** - 轴心编码
3. **performing-selective-coding** - 选择式编码
4. **checking-theory-saturation** - 理论饱和度检验
5. **writing-grounded-theory-memos** - 扎根理论备忘录写作

### 分析类技能 (3个)
1. **performing-centrality-analysis** - 中心性分析
2. **performing-network-computation** - 网络计算分析
3. **processing-network-data** - 网络数据处理

### 方法论类技能 (1个)
1. **resolving-research-conflicts** - 研究冲突解决

### 特殊目录技能 (4个)
1. **conflict-resolution** - 冲突解决
2. **mathematical-statistics** - 数理统计
3. **network-computation** - 网络计算
4. **validity-reliability** - 信效度分析

## 🛠️ 辅助工具

### Python依赖
```bash
pip install jieba networkx numpy pandas matplotlib seaborn
```

### 自动加载器使用
```bash
# 开放编码快速分析
python skills/coding/performing-open-coding/scripts/auto_loader.py data.txt

# 网络数据预处理
python skills/analysis/processing-network-data/scripts/preprocessor.py data.csv
```

## 📚 使用示例

### Claude Code 中的使用
```
用户: 我有一份访谈数据需要做开放编码分析
Claude: [自动触发 performing-open-coding 技能]
我将帮您执行扎根理论的开放编码过程...

用户: 需要分析这个社交网络的中心性
Claude: [自动触发 performing-centrality-analysis 技能]
我将为您计算网络的中心性指标...
```

### OpenSkills 中的使用
```bash
# 读取特定技能
openskills read performing-open-coding

# 列出可用技能
openskills list

# 管理技能
openskills manage
```

## ⚠️ 注意事项

### 兼容性
- ✅ Claude Code (最新版本)
- ✅ OpenSkills (最新版本)
- ✅ Python 3.8+
- ✅ 支持中文字符

### 性能优化
- 技能采用渐进式加载，避免上下文过载
- Python脚本提供快速预处理
- 验证工具确保质量

### 中文支持
- 所有技能专门针对中文研究优化
- 支持中文文本处理和分析
- 符合中文学术写作规范

## 🔍 故障排除

### 常见问题

**问题**: 技能无法触发
- 检查YAML frontmatter格式
- 确认技能描述包含触发关键词
- 重启Claude Code或OpenSkills

**问题**: Python脚本运行错误
- 检查依赖包是否安装
- 确认文件路径正确
- 查看错误日志

**问题**: 中文字符显示异常
- 确认文件编码为UTF-8
- 检查终端字符编码设置
- 更新相关软件版本

### 获取帮助
- 查看 `SKILLS_MANIFEST.md` 了解技能详情
- 运行 `python validate_skills.py` 检查技能状态
- 查看各技能目录下的README文件

## 📈 未来扩展

### 添加新技能
1. 创建技能目录: `mkdir skills/new-skill`
2. 创建SKILL.md文件，包含必需的YAML frontmatter
3. 编写技能内容，遵循现有格式
4. 运行验证工具检查格式
5. 添加到技能清单

### 更新现有技能
1. 编辑相应的SKILL.md文件
2. 更新Python辅助脚本
3. 运行验证工具
4. 更新版本信息

## 🎉 完成

恭喜！您已成功部署中文社会科学研究技能包。现在您可以：

- 在Claude Code中使用专业的研究分析技能
- 通过OpenSkills在多个AI平台使用这些技能
- 利用Python工具进行自动化数据处理
- 享受渐进式加载带来的高效体验

---

*如有问题，请参考各技能文档或运行验证工具进行诊断。*