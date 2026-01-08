# NPM包安装与Stigmergy集成指南

## 📦 NPM包信息

- **包名**: `ssci-subagent-skills`
- **版本**: 1.0.0
- **仓库**: https://github.com/ptreezh/sscisubagent-skills
- **许可证**: MIT

## 🚀 快速安装

### 方式1: 通过npm安装（推荐）

```bash
# 全局安装
npm install -g ssci-subagent-skills

# 或本地安装
npm install ssci-subagent-skills
```

### 方式2: 从GitHub安装

```bash
npm install git+https://github.com/ptreezh/sscisubagent-skills.git
```

## 🔧 自动配置

npm包安装后会自动执行以下操作：

1. **检测Stigmergy**: 检查系统是否已安装stigmergy-cli
2. **同步技能**: 自动将技能同步到stigmergy
3. **部署到CLI**: 自动部署到所有可用的AI CLI工具

### 手动执行配置

如果自动配置失败，可以手动执行：

```bash
# 同步技能到stigmergy
stigmergy skill sync

# 部署到CLI工具
stigmergy deploy

# 验证安装
npm run validate
```

## 📚 可用的技能

### 核心研究技能

| 技能名称 | 描述 | 用途 |
|---------|------|------|
| `ant` | 行动者网络理论分析 | 分析异质性行动者网络、追踪事实构建过程 |
| `field-analysis` | 布迪厄场域分析 | 分析社会场域结构、权力关系和文化资本 |
| `field-expert` | 场域分析专家 | 完整的场域分析工作流 |
| `grounded-theory-expert` | 扎根理论专家 | 质性研究的编码和理论构建 |
| `network-computation` | 社会网络计算 | 网络构建、中心性分析、社区检测 |
| `mathematical-statistics` | 数理统计分析 | 描述性统计、推断统计、回归分析 |
| `validity-reliability` | 信度效度分析 | 内部一致性、构念效度、效标效度 |
| `conflict-resolution` | 冲突解决 | 研究分歧处理和共识建立 |

### 业务分析技能

| 技能名称 | 描述 | 用途 |
|---------|------|------|
| `business-ecosystem-analysis` | 商业生态系统分析 | 生态系统结构分析 |
| `digital-transformation` | 数字化转型分析 | 数字化成熟度评估 |
| `ecosystem-analysis` | 生态分析 | 关系网络映射 |

## 🤖 可用的智能体

| 智能体名称 | 描述 | 核心技能 |
|-----------|------|---------|
| `ant-expert` | 行动者网络理论专家 | ant, ant-network-analysis, ant-translation-process |
| `field-analysis-expert` | 场域分析专家 | field-analysis, field-boundary-identification, field-capital-analysis |
| `grounded-theory-expert` | 扎根理论专家 | performing-open-coding, performing-axial-coding, performing-selective-coding |
| `literature-expert` | 文献管理专家 | 文献检索、引用格式化 |
| `sna-expert` | 社会网络分析专家 | network-computation, performing-centrality-analysis |
| `chinese-localization-expert` | 中文本土化专家 | 概念本土化、方法论适配 |
| `digital-marx-expert` | 数字马克思主义专家 | 历史唯物主义、阶级结构分析 |

## 💻 使用方法

### 在Claude CLI中使用

启动Claude CLI后，直接使用自然语言触发技能：

```bash
# 启动Claude
claude

# 使用示例
> 请帮我分析这个文本的场域结构
> 使用行动者网络理论分析这段内容
> 进行扎根理论的开放编码
> 分析这个社交网络的中心性
```

### 在iFlow CLI中使用

```bash
# 启动iFlow
iflow

# 使用示例
> 分析教育场域的资本分布
> 执行社会网络分析
> 检验理论饱和度
```

### 在Qwen CLI中使用

```bash
# 启动Qwen
qwen

# 使用示例
> 使用布迪厄场域理论分析
> 进行质性数据分析
> 计算网络中心性指标
```

## 🔍 验证安装

### 检查已安装的技能

```bash
# 列出所有技能
stigmergy skill list

# 查看特定技能
stigmergy skill read field-expert

# 验证技能格式
stigmergy skill validate
```

### 检查CLI状态

```bash
# 查看CLI工具状态
stigmergy status

# 扫描可用的CLI工具
stigmergy scan
```

### 运行验证脚本

```bash
# 验证技能和智能体格式
npm run validate
```

## 🛠️ 故障排除

### 问题1: 技能无法同步

**解决方案**:
```bash
# 检查stigmergy是否安装
stigmergy --version

# 重新安装stigmergy
npm install -g stigmergy-cli

# 手动同步
stigmergy skill sync --force
```

### 问题2: 技能无法触发

**解决方案**:
```bash
# 重新部署
stigmergy deploy --force

# 检查技能格式
npm run validate

# 重启CLI工具
```

### 问题3: 自动配置失败

**解决方案**:
```bash
# 手动执行postinstall脚本
node scripts/postinstall.js

# 或手动执行配置命令
stigmergy skill sync
stigmergy deploy
```

## 📦 包结构

```
ssci-subagent-skills/
├── skills/              # 技能目录
│   ├── ant/            # 行动者网络理论
│   ├── field-analysis/ # 场域分析
│   ├── field-expert/   # 场域分析专家
│   └── ...
├── agents/             # 智能体目录
│   ├── ant-expert.md
│   ├── field-analysis-expert.md
│   └── ...
├── scripts/            # 工具脚本
│   ├── postinstall.js  # 安装后配置
│   └── validate-skills.js # 验证脚本
├── package.json        # NPM包配置
├── pyproject.toml      # Python项目配置
└── README.md           # 项目文档
```

## 🔄 更新包

```bash
# 更新到最新版本
npm update -g ssci-subagent-skills

# 或从GitHub更新
npm install -g git+https://github.com/ptreezh/sscisubagent-skills.git

# 重新同步技能
stigmergy skill sync --force
```

## 📖 更多信息

- **GitHub仓库**: https://github.com/ptreezh/sscisubagent-skills
- **问题反馈**: https://github.com/ptreezh/sscisubagent-skills/issues
- **Stigmergy文档**: https://github.com/stigmergy-cli/stigmergy-cli

## 🤝 贡献

欢迎贡献代码和提出建议！

1. Fork仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**最后更新**: 2026-01-08
**版本**: 1.0.0