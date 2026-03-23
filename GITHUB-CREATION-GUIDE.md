# GitHub 仓库创建指南

**目标**: 创建 `superpower-socialscience-skills` 仓库

---

## 🎯 方案 1: 手动创建（推荐）

### 步骤 1: 登录 GitHub

1. 打开浏览器
2. 访问：https://github.com/login
3. 使用 `ptreezh` 账号登录

### 步骤 2: 创建新仓库

1. 点击右上角 **+** 按钮
2. 选择 **New repository**
3. 填写信息：
   - **Repository name**: `superpower-socialscience-skills`
   - **Description**: `60 种社会科学方法论技能包 - SocienceAI`
   - **Visibility**: ✅ Public (公开)
   - **Initialize this repository with**: ❌ 不勾选

4. 点击 **Create repository**

### 步骤 3: 推送代码

在终端执行以下命令：

```bash
cd D:\socienceAI\agentskills

# 初始化 Git（如已初始化可跳过）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 60 种社会科学方法论技能包"

# 添加远程仓库
git remote add origin https://github.com/ptreezh/superpower-socialscience-skills.git

# 重命名分支为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

---

## 🎯 方案 2: 使用 GitHub Desktop

### 步骤 1: 安装 GitHub Desktop

1. 访问：https://desktop.github.com/
2. 下载并安装

### 步骤 2: 添加本地仓库

1. 打开 GitHub Desktop
2. 使用 `ptreezh` 账号登录
3. 点击 **File** → **Add Local Repository**
4. 选择目录：`D:\socienceAI\agentskills`
5. 点击 **Add repository**

### 步骤 3: 发布到 GitHub

1. 点击右上角 **Publish repository**
2. 填写信息：
   - **Name**: `superpower-socialscience-skills`
   - **Description**: `60 种社会科学方法论技能包`
   - ✅ 勾选 **Keep this code private** (如需要私有)
3. 点击 **Publish repository**

---

## 🎯 方案 3: 使用命令行工具 gh

### 步骤 1: 安装 gh

```bash
# Windows (Chocolatey)
choco install gh

# 或使用 winget
winget install GitHub.cli
```

### 步骤 2: 登录 GitHub

```bash
gh auth login
# 按提示操作，选择 ptreezh 账号
```

### 步骤 3: 创建仓库并推送

```bash
cd D:\socienceAI\agentskills

# 创建仓库
gh repo create ptreezh/superpower-socialscience-skills --public --source=. --remote=origin

# 推送
git push -u origin main
```

---

## 📋 仓库信息

### 仓库名称
`superpower-socialscience-skills`

### 仓库描述
```
60 种社会科学方法论技能包

包含：
- 质性研究方法 (20 个)
- 定量研究方法 (15 个)
- 混合方法与商业分析 (25 个)

每个技能包包含：
- SKILL.md - 技能定义
- skill.yaml - 技能配置
- tools/ - 工具模块
- templates/ - 模板文件

网站：http://www.socienceai.com
```

### 许可证
MIT License

### 标签
```
social-science, methodology, ai-skills, grounded-theory, network-analysis, qca, research-methods
```

---

## 🔧 Git 配置检查清单

### 推送前检查

- [ ] Git 已初始化
- [ ] 所有文件已添加 (`git status`)
- [ ] 已提交 (`git log`)
- [ ] 远程仓库已添加 (`git remote -v`)
- [ ] 分支名为 `main` (`git branch`)

### 推送后检查

- [ ] 仓库页面显示文件
- [ ] README.md 正确显示
- [ ] 所有技能包目录可见
- [ ] 文件大小正确

---

## 📞 问题排查

### 问题 1: 推送失败 - 认证错误

**解决**:
```bash
# 清除缓存的凭证
git credential-cache exit

# 重新推送
git push -u origin main
# 输入 GitHub 账号密码
```

### 问题 2: 仓库已存在

**解决**:
- 使用不同的仓库名
- 或删除现有仓库后重试

### 问题 3: 文件太大

**解决**:
```bash
# 检查大文件
git rev-parse HEAD | xargs git ls-tree -r | awk '$3 > 10485760 { print $4 }'

# 使用 Git LFS
git lfs install
git lfs track "*.zip"
git add .gitattributes
```

---

## 📊 预期结果

### 仓库结构

```
superpower-socialscience-skills/
├── README.md
├── grounded-theory-expert/
├── social-network-analysis-expert/
├── qca-analysis-expert/
├── ... (60 个技能包)
└── ...
```

### 访问地址

**GitHub**: https://github.com/ptreezh/superpower-socialscience-skills

---

**创建日期**: 2026-03-23 21:50  
**执行者**: SocienceAI Soul  
**状态**: 等待手动创建

*按步骤操作，3 分钟完成*
