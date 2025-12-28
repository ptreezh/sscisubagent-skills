# 快速部署指南

**版本**: 1.0.0
**作者**: socienceAI.com
**联系**: zhangshuren@freeagentskills.com

---

## 一键部署

### 方法1: 使用自动化脚本（推荐）

**Linux/macOS**:
```bash
./scripts/deploy.sh
```

**Windows**:
```cmd
scripts\deploy.bat
```

### 方法2: 创建Release（自动触发CI/CD）

```bash
# 1. 创建版本标签
git tag -a v1.0.0 -m "Release v1.0.0"

# 2. 推送标签
git push origin v1.0.0

# 3. 在GitHub创建Release
# 访问: https://github.com/ptreezh/sscisubagent-skills/releases/new
```

---

## 首次部署配置

### 步骤1: 配置GitHub Secrets

1. 访问仓库设置: https://github.com/ptreezh/sscisubagent-skills/settings/secrets/actions
2. 添加Secret: `AGENTSKILLS_API_KEY`
3. 值: 从 https://agentskills.io/developer 获取

### 步骤2: 更新版本号

编辑 `.agentskills/config.yml`:
```yaml
project:
  version: "1.0.0"  # 修改为当前版本
```

### 步骤3: 运行部署脚本

```bash
./scripts/deploy.sh -t v1.0.0 -m "Release v1.0.0"
```

---

## 验证部署

### 检查CI/CD状态

1. 访问: https://github.com/ptreezh/sscisubagent-skills/actions
2. 查看最新工作流运行状态
3. 确保所有check通过（绿色✅）

### 验证技能发布

1. 访问: https://agentskills.io
2. 搜索: "sscisubagent-skills"
3. 检查技能是否成功发布

---

## 常用命令

```bash
# 查看Git状态
git status

# 查看更改
git diff

# 添加所有更改
git add .

# 创建提交
git commit -m "feat: 更新内容"

# 推送到远程
git push origin main

# 创建版本标签
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 查看日志
git log --oneline -10
```

---

## 故障排查

### Git推送失败
```bash
# 拉取并rebase
git pull origin main --rebase

# 解决冲突后推送
git push origin main
```

### CI/CD失败
1. 查看Actions日志: https://github.com/ptreezh/sscisubagent-skills/actions
2. 检查错误信息
3. 修复问题后重新推送

### 发布失败
```bash
# 检查API密钥
echo $AGENTSKILLS_API_KEY

# 手动测试发布
python .github/scripts/publish_to_agentskills.py
```

---

## 获取帮助

**文档**:
- [完整部署指南](DEPLOYMENT_GUIDE.md)
- [README](README.md)
- [贡献指南](CONTRIBUTING.md)

**联系**:
- 作者: socienceAI.com
- 邮箱: zhangshuren@freeagentskills.com
- Issues: https://github.com/ptreezh/sscisubagent-skills/issues

---

**快速部署，让您的技能即刻上线！** 🚀
