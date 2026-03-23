# GitHub 仓库创建 - 紧急指南

**目标**: 创建 `superpower-socialscience-skills` 仓库

---

## ⚡ 快速创建（2 分钟）

### 步骤 1: 打开 GitHub

**已打开浏览器**:
1. 在当前浏览器标签页访问：https://github.com/new

**或新标签页**:
1. 按 `Ctrl+T` 打开新标签
2. 访问：https://github.com/new

### 步骤 2: 填写仓库信息

**Repository name** (必填):
```
superpower-socialscience-skills
```

**Description** (可选):
```
60 种社会科学方法论技能包 - SocienceAI
包含质性研究 (20)、定量研究 (15)、混合方法 (25)
```

**Visibility**:
- ✅ **Public** (公开)

**Initialize**:
- ❌ **不要勾选** "Add a README file"

### 步骤 3: 创建

点击绿色按钮：**Create repository**

---

## 📤 推送代码（1 分钟）

### 复制仓库 URL

创建成功后，复制显示的 URL：
```
https://github.com/ptreezh/superpower-socialscience-skills.git
```

### 执行推送

**打开命令提示符**:
```bash
cd D:\socienceAI\agentskills
```

**执行推送命令**:
```bash
# 如 Git 未初始化
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ptreezh/superpower-socialscience-skills.git

# 推送
git push -u origin main
```

---

## 🔑 如提示认证

### 使用 Personal Access Token

**创建 Token**:
1. 访问：https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 填写描述：`agentskills-upload`
4. 勾选权限：✅ **repo** (Full control)
5. 点击 **Generate token**
6. **复制 token**（只显示一次！）

**使用 Token**:
```bash
git push -u origin main
# Username: ptreezh
# Password: [粘贴 token]
```

---

## ✅ 验证

**访问仓库**:
https://github.com/ptreezh/superpower-socialscience-skills

**应看到**:
- ✅ 60 个技能包目录
- ✅ 最近提交记录
- ✅ 文件列表

---

## 🆘 遇到问题？

### 问题：浏览器无法访问

**解决**:
1. 检查网络连接
2. 清除浏览器缓存
3. 或使用无痕模式

### 问题：推送失败

**错误**: `Authentication failed`

**解决**:
1. 创建 Personal Access Token
2. 使用 token 作为密码

### 问题：仓库已存在

**解决**:
1. 访问：https://github.com/ptreezh
2. 查找已有仓库
3. 删除或重命名

---

## 📋 检查清单

- [ ] 访问 https://github.com/new
- [ ] 填写仓库名：`superpower-socialscience-skills`
- [ ] 选择 Public
- [ ] 不勾选 Initialize
- [ ] 点击 Create repository
- [ ] 复制仓库 URL
- [ ] 执行 `git push -u origin main`
- [ ] 验证仓库页面

---

**创建日期**: 2026-03-23 22:10  
**状态**: 等待手动创建

*2 分钟创建，1 分钟推送*
