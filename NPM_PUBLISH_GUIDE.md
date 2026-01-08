# NPM包发布指南

## 📦 发布前准备

### 1. 检查npm账户

```bash
# 登录npm
npm login

# 验证登录状态
npm whoami
```

### 2. 验证包名可用性

```bash
# 检查包名是否已被占用
npm view ssci-subagent-skills

# 如果显示404，说明包名可用
```

### 3. 更新版本号

```bash
# 更新版本号（patch/minor/major）
npm version patch  # 1.0.0 -> 1.0.1
npm version minor  # 1.0.0 -> 1.1.0
npm version major  # 1.0.0 -> 2.0.0
```

## 🚀 发布步骤

### 方式1: 直接发布（推荐）

```bash
# 1. 构建包（如果需要）
npm run build

# 2. 运行测试
npm run validate

# 3. 发布到npm
npm publish

# 4. 验证发布
npm view ssci-subagent-skills
```

### 方式2: 使用发布标签

```bash
# 发布带标签的版本
npm publish --tag beta    # 测试版
npm publish --tag latest  # 正式版
```

### 方式3: 发布到私有仓库

```bash
# 发布到私有npm仓库
npm publish --registry https://your-private-registry.com
```

## 📋 发布检查清单

发布前请确认以下事项：

- [ ] package.json配置正确
- [ ] 版本号已更新
- [ ] README.md完整
- [ ] CHANGELOG.md已更新
- [ ] 所有文件已提交到Git
- [ ] .gitignore配置正确
- [ ] 技能和智能体格式正确
- [ ] postinstall.js脚本正常工作
- [ ] validate-skills.js通过验证
- [ ] 测试用例通过（如果有）
- [ ] 许可证信息正确

## 🔍 验证发布

### 检查包信息

```bash
# 查看包信息
npm view ssci-subagent-skills

# 查看所有版本
npm view ssci-subagent-skills versions

# 查看最新版本
npm view ssci-subagent-skills version
```

### 测试安装

```bash
# 全局安装测试
npm install -g ssci-subagent-skills

# 本地安装测试
npm install ssci-subagent-skills

# 验证安装
stigmergy skill list
npm run validate
```

## 🔄 更新包

### 更新流程

```bash
# 1. 更新代码
git add .
git commit -m "feat: 新功能描述"
git push origin main

# 2. 更新版本号
npm version patch

# 3. 发布新版本
npm publish

# 4. 推送标签
git push origin main --tags
```

### 撤销发布

```bash
# 撤销24小时内发布的版本
npm unpublish ssci-subagent-skills@1.0.1

# 撤销最新版本
npm unpublish ssci-subagent-skills@latest --force

# 注意：超过24小时无法撤销
```

## 📊 包管理

### 查看下载统计

```bash
# 查看下载量
npm view ssci-subagent-skills downloads

# 查看最近30天下载量
npm view ssci-subagent-skills downloads --json
```

### 查看依赖关系

```bash
# 查看包的依赖
npm view ssci-subagent-skills dependencies

# 查看谁依赖了这个包
npm view ssci-subagent-skills dependents
```

## 🛠️ 故障排除

### 问题1: 发布失败 - 403 Forbidden

**原因**: 包名已被占用或权限不足

**解决方案**:
```bash
# 检查包名
npm view ssci-subagent-skills

# 如果被占用，更换包名
# 修改package.json中的name字段
```

### 问题2: 发布失败 - E404 Not Found

**原因**: npm未登录或token过期

**解决方案**:
```bash
# 重新登录
npm login

# 或使用token
npm config set //registry.npmjs.org/:_authToken YOUR_TOKEN
```

### 问题3: 文件未包含在包中

**原因**: 文件未被package.json的files字段包含

**解决方案**:
```json
{
  "files": [
    "skills/",
    "agents/",
    "scripts/",
    "README.md",
    "CHANGELOG.md",
    "LICENSE"
  ]
}
```

### 问题4: postinstall脚本未执行

**原因**: 脚本权限或路径问题

**解决方案**:
```bash
# 确保脚本有执行权限
chmod +x scripts/postinstall.js

# 验证脚本语法
node -c scripts/postinstall.js
```

## 📝 版本管理

### 语义化版本

- **主版本号 (Major)**: 不兼容的API修改
- **次版本号 (Minor)**: 向下兼容的功能性新增
- **修订号 (Patch)**: 向下兼容的问题修正

### 版本示例

```bash
# Bug修复
npm version patch  # 1.0.0 -> 1.0.1

# 新功能
npm version minor  # 1.0.0 -> 1.1.0

# 重大变更
npm version major  # 1.0.0 -> 2.0.0

# 预发布版本
npm version prepatch   # 1.0.0 -> 1.0.1-0
npm version prerelease # 1.0.0 -> 1.0.1-0
npm version premajor   # 1.0.0 -> 2.0.0-0
```

## 🔐 安全性

### 设置双因素认证

```bash
# 启用2FA
npm profile enable-2fa auth-and-writes

# 查看token
npm token list

# 创建新token
npm token create --read-only
```

### 审计依赖

```bash
# 审计安全漏洞
npm audit

# 自动修复
npm audit fix

# 强制修复
npm audit fix --force
```

## 📚 相关资源

- [NPM官方文档](https://docs.npmjs.com/)
- [package.json规范](https://docs.npmjs.com/cli/v9/configuring-npm/package-json)
- [语义化版本](https://semver.org/)
- [Stigmergy CLI](https://github.com/stigmergy-cli/stigmergy-cli)

## 🤝 贡献指南

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