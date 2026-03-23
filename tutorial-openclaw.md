# OpenClaw（小龙虾）技能使用教程

**最后更新**: 2026-03-22  
**难度**: 入门  
**时间**: 10 分钟

---

## 📋 什么是 OpenClaw

**OpenClaw**（中文名：小龙虾）是一个本地部署的 AI 智能体 CLI 工具，支持加载各种技能（Skills）来扩展 AI 的能力。

**核心特点**:
- ✅ 本地部署，数据不出本地
- ✅ 支持技能扩展
- ✅ 开源免费
- ✅ 社区活跃

**适用场景**:
- 社会科学研究数据分析
- 质性研究编码
- 文献综述
- 学术写作

---

## 🚀 快速开始（5 分钟上手）

### 步骤 1: 安装 OpenClaw

```bash
# 方式 1: npm 安装（推荐）
npm install -g openclaw

# 方式 2: pip 安装
pip install openclaw

# 方式 3: 从 GitHub 下载
git clone https://github.com/openclaw/openclaw.git
cd openclaw
npm install
```

**验证安装**:
```bash
openclaw --version
# 输出：openclaw v1.x.x
```

---

### 步骤 2: 下载技能包

**方式 1: Git 克隆（推荐）**:
```bash
# 克隆整个技能仓库
git clone https://github.com/socienceai/agentskills.git
cd agentskills
```

**方式 2: 下载单个技能**:
```bash
# 以扎根理论为例
git clone https://github.com/socienceai/agentskills.git grounded-theory-expert
```

**方式 3: 直接下载 ZIP**:
1. 访问 https://github.com/socienceai/agentskills
2. 点击 "Code" → "Download ZIP"
3. 解压到本地

---

### 步骤 3: 配置技能路径

**方式 1: 复制到技能目录（推荐）**:
```bash
# 创建技能目录
mkdir -p ~/.openclaw/skills

# 复制技能到技能目录
cp -r grounded-theory-expert ~/.openclaw/skills/
```

**方式 2: 配置环境变量**:
```bash
# Windows (PowerShell)
$env:OPENCLAW_SKILLS_PATH="D:\socienceAI\agentskills"

# Linux/Mac
export OPENCLAW_SKILLS_PATH="/path/to/agentskills"
```

**方式 3: 命令行指定**:
```bash
openclaw --skill /path/to/grounded-theory-expert "任务描述"
```

---

### 步骤 4: 加载技能

**方式 1: 自动加载（技能在技能目录）**:
```bash
# 技能在~/.openclaw/skills/目录时自动加载
openclaw "使用扎根理论分析以下访谈数据..."
```

**方式 2: 手动指定技能**:
```bash
openclaw --skill grounded-theory-expert "使用扎根理论分析以下访谈数据..."
```

**方式 3: 交互式加载**:
```bash
# 启动 OpenClaw
openclaw

# 在交互界面中加载技能
> /load grounded-theory-expert
> 使用扎根理论分析以下访谈数据...
```

---

## 📚 使用示例

### 示例 1: 扎根理论分析

```bash
# 加载技能
openclaw --skill grounded-theory-expert

# 输入任务
请对以下访谈数据进行开放编码：

"我觉得工作压力很大，每天都要加班，
但是没有明确的晋升通道，感觉很迷茫。"
```

**预期输出**:
```
## 开放编码结果

### 初始概念
1. 工作压力
   - 原始引文："我觉得工作压力很大"
   - 范畴：工作环境

2. 加班现象
   - 原始引文："每天都要加班"
   - 范畴：工作强度

3. 晋升困境
   - 原始引文："没有明确的晋升通道"
   - 范畴：职业发展

4. 迷茫情绪
   - 原始引文："感觉很迷茫"
   - 范畴：心理状态

### 下一步建议
1. 继续进行主轴编码，建立概念间关系
2. 收集更多访谈数据，进行持续比较
3. 撰写备忘录，记录编码思考过程
```

---

### 示例 2: 社会网络分析

```bash
# 加载技能
openclaw --skill social-network-analysis-expert

# 输入任务
请分析以下社会网络数据：

节点：A, B, C, D, E
关系：
A-B, A-C, B-C, B-D, C-E, D-E
```

**预期输出**:
```
## 社会网络分析结果

### 网络基本特征
- 节点数：5
- 边数：6
- 密度：0.6
- 平均度：2.4

### 中心性分析
| 节点 | 度中心性 | 接近中心性 | 中介中心性 |
|------|---------|-----------|-----------|
| A    | 0.5     | 0.67      | 0.17      |
| B    | 0.75    | 0.83      | 0.33      |
| C    | 0.75    | 0.83      | 0.33      |
| D    | 0.5     | 0.67      | 0.17      |
| E    | 0.5     | 0.67      | 0.17      |

### 关键节点
- B 和 C 是网络中的关键节点（中心性最高）

### 建议
1. 识别网络中的子群结构
2. 分析结构洞位置
3. 可视化网络图谱
```

---

### 示例 3: 布迪厄场域分析

```bash
# 加载技能
openclaw --skill bourdieu-field-analysis-expert

# 输入任务
请用布迪厄场域理论分析以下教育场景：

"某重点大学中，来自不同家庭背景的学生
在学业表现、社交活动、未来发展等方面
表现出明显差异。"
```

**预期输出**:
```
## 布迪厄场域分析结果

### 场域识别
- 分析对象：重点大学教育场域
- 场域边界：该校在校学生
- 场域特征：精英教育环境

### 资本分析
1. 经济资本
   - 高收入家庭：学费无忧，可专注学习
   - 低收入家庭：需兼职打工，时间分散

2. 文化资本
   - 高知家庭：文化习惯契合学校要求
   - 低知家庭：需要适应新文化环境

3. 社会资本
   - 高地位家庭：社会关系网络丰富
   - 低地位家庭：社会关系网络有限

### 习性分析
- 优势群体：习性与场域要求匹配
- 弱势群体：习性需要调整适应

### 再生产机制
教育场域通过资本差异再生产社会不平等

### 建议
1. 学校应提供经济资助
2. 开展文化适应辅导
3. 建立多元评价体系
```

---

## 🔧 高级用法

### 1. 技能组合使用

```bash
# 同时加载多个技能
openclaw --skill grounded-theory-expert --skill social-network-analysis-expert

# 任务
请先用扎根理论编码访谈数据，
然后用社会网络分析分析编码结果的关系网络。
```

### 2. 自定义配置

```bash
# 查看技能配置
openclaw --skill grounded-theory-expert --show-config

# 修改配置（编辑 skill.yaml）
nano ~/.openclaw/skills/grounded-theory-expert/skill.yaml
```

### 3. 技能开发

```bash
# 创建新技能
openclaw --create-skill my-skill

# 技能结构
my-skill/
├── SKILL.md
├── skill.yaml
├── tools/
└── templates/
```

---

## ❓ 常见问题

### Q1: 技能加载失败

**问题**: `Error: Skill not found`

**解决方案**:
```bash
# 1. 检查技能路径
ls ~/.openclaw/skills/

# 2. 确认技能名称
openclaw --list-skills

# 3. 重新复制技能
cp -r grounded-theory-expert ~/.openclaw/skills/
```

### Q2: 技能执行报错

**问题**: `Error: Tool not found`

**解决方案**:
```bash
# 1. 检查工具依赖
cd ~/.openclaw/skills/grounded-theory-expert
pip install -r requirements.txt

# 2. 检查 Python 版本
python --version  # 需要 Python 3.8+

# 3. 重新安装工具
python tools/setup.py install
```

### Q3: 输出结果不理想

**问题**: 输出太简单或不符合预期

**解决方案**:
```bash
# 1. 提供更详细的任务描述
openclaw --skill grounded-theory-expert "
请对以下访谈数据进行详细的开放编码分析，
要求：
1. 识别所有初始概念
2. 为每个概念提供原始引文
3. 将概念归类到范畴
4. 提供下一步分析建议

访谈数据：..."

# 2. 调整技能配置
nano ~/.openclaw/skills/grounded-theory-expert/skill.yaml

# 3. 查看技能文档
cat ~/.openclaw/skills/grounded-theory-expert/SKILL.md
```

### Q4: 如何更新技能

**解决方案**:
```bash
# 方式 1: Git 拉取更新
cd ~/agentskills
git pull

# 方式 2: 重新下载
rm -rf ~/agentskills
git clone https://github.com/socienceai/agentskills.git

# 方式 3: 手动更新
# 访问 GitHub 下载最新版本
```

---

## 📖 相关资源

### 官方文档

- [OpenClaw 官方文档](https://github.com/openclaw/openclaw)
- [OpenClaw 技能开发指南](https://github.com/openclaw/skills-guide)

### 技能仓库

- [SocienceAI 技能仓库](https://github.com/socienceai/agentskills)
- [12 种社会科学方法论技能](https://github.com/socienceai/agentskills)

### 社区支持

- [OpenClaw 社区](https://github.com/openclaw/openclaw/discussions)
- [SocienceAI 社区](https://github.com/socienceai/agentskills/discussions)

---

## 🎯 下一步学习

### 入门教程

1. ✅ 完成本教程
2. [WorkBuddy 技能加载教程](/tutorials/workbuddy/)
3. [Coze 技能导入教程](/tutorials/coze/)

### 进阶教程

1. [技能开发与定制](/tutorials/skill-development/)
2. [多技能组合使用](/tutorials/skill-combination/)
3. [技能性能优化](/tutorials/skill-optimization/)

### 专业教程

1. [扎根理论实操指南](/skills/grounded-theory/tutorial/)
2. [社会网络分析实战](/skills/social-network-analysis/tutorial/)
3. [布迪厄场域分析案例](/skills/bourdieu-field-analysis/tutorial/)

---

**教程版本**: 1.0  
**最后更新**: 2026-03-22  
**维护者**: SocienceAI Team

*让社会科学研究人人可为*
