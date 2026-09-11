# Skill Creator 安装指南

## 概述

Skill Creator 是一个用于创建、修改和改进技能的元技能。它提供了完整的技能开发生命周期支持。

## 安装位置

`agentskills/skill-creator/`

## 目录结构

```
skill-creator/
├── SKILL.md           # 技能主文档（包含完整的使用说明）
├── skill.yaml         # 技能配置文件
├── agents/           # 子Agent配置
│   ├── analyzer.md   # 分析Agent
│   ├── comparator.md # 比较Agent
│   └── grader.md     # 评分Agent
├── scripts/          # 辅助脚本
│   ├── package_skill.py       # 打包技能
│   ├── quick_validate.py      # 快速验证
│   ├── run_eval.py           # 运行评估
│   ├── run_loop.py           # 运行循环
│   ├── improve_description.py # 改进描述
│   ├── generate_report.py    # 生成报告
│   └── aggregate_benchmark.py # 聚合基准
├── eval-viewer/       # 评估查看器
│   ├── generate_review.py    # 生成评估报告
│   └── viewer.html          # 可视化查看器
├── references/        # 参考文档
└── assets/           # 资源文件
```

## 核心功能

### 1. 创建新技能
- 从零开始创建技能
- 定义技能名称、描述和触发条件
- 编写SKILL.md文档
- 创建必要的脚本和工具

### 2. 编辑和改进现有技能
- 优化技能描述
- 改进指令清晰度
- 添加缺失的工具和脚本
- 修复边缘情况处理

### 3. 运行评估测试
- 创建测试用例
- 运行盲比较测试
- 生成详细报告
- 分析结果和提出改进建议

### 4. 基准测试
- 性能基准测试
- 方差分析
- 多配置比较
- 聚合分析

## 使用方法

### 基本使用

当用户提到以下内容时，此技能会自动触发：
- "创建技能" / "创建一个技能"
- "编辑技能" / "改进技能"
- "测试技能" / "评估技能"
- "基准测试" / "性能测试"
- "优化技能描述"

### 直接调用

你也可以直接使用 Skill tool 调用：

```bash
/skill skill-creator
```

## 工作流程

### 创建技能的标准流程：

1. **捕获意图** - 理解用户想要什么
2. **访谈和研究** - 了解边缘情况和依赖关系
3. **编写SKILL.md** - 创建技能文档
4. **创建测试用例** - 定义验证标准
5. **运行评估** - 测试技能效果
6. **迭代改进** - 根据反馈优化
7. **大规模测试** - 扩展测试集

### 编辑现有技能：

1. 读取现有技能
2. 识别问题和改进空间
3. 提出改进建议
4. 实施改进
5. 验证改进效果

## 依赖项

- Python >= 3.8
- pyyaml >= 6.0
- jinja2 >= 3.0

## 兼容性

- agentskills.io
- claude-desktop
- qwen-cli

## 注意事项

1. **渐进式披露**：保持SKILL.md在500行以内，使用分层结构
2. **描述优化**：技能描述应该"主动"一些，以提高触发率
3. **用户友好**：注意用户的编程背景，适当解释技术术语
4. **灵活运用**：根据具体需求调整流程

## 更多信息

详细的使用说明请参考 `SKILL.md` 文件。

## 许可证

MIT License - 来自 Anthropic
