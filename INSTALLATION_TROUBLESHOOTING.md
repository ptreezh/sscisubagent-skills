# 安装故障排除指南

## 问题1：npm install后postinstall脚本未自动运行

### 原因
npm在某些情况下可能会跳过postinstall脚本，特别是：
1. 使用了`--ignore-scripts`标志
2. npm配置中禁用了脚本
3. 网络问题导致脚本下载失败

### 解决方案

#### 方法1：手动运行postinstall脚本
```bash
# Windows
cd %APPDATA%\npm\node_modules\ssci-subagent-skills
node scripts/postinstall.js

# Linux/Mac
cd ~/.npm-global/node_modules/ssci-subagent-skills
node scripts/postinstall.js
```

#### 方法2：使用npm run触发
```bash
npm run postinstall
```

#### 方法3：强制运行postinstall
```bash
npm rebuild ssci-subagent-skills
```

#### 方法4：重新安装
```bash
npm uninstall -g ssci-subagent-skills
npm install -g ssci-subagent-skills
```

### 验证安装

检查postinstall是否成功执行：
```bash
# 查看stigmergy技能列表
stigmergy skill list

# 应该看到新增的技能：
# • ant
# • field-analysis
# • field-expert
# • grounded-theory-expert
# • network-computation
# • mathematical-statistics
# • validity-reliability
# • conflict-resolution
```

---

## 问题2：技能未同步到Stigmergy

### 解决方案

#### 手动同步
```bash
stigmergy skill sync
```

#### 验证同步
```bash
stigmergy skill list
```

---

## 问题3：CLI工具未部署

### 解决方案

#### 手动部署
```bash
stigmergy deploy
```

#### 检查部署状态
```bash
stigmergy status
```

---

## 完整安装流程（推荐）

```bash
# 1. 全局安装
npm install -g ssci-subagent-skills

# 2. 手动运行postinstall（确保配置完成）
npm run postinstall

# 3. 验证安装
npm run validate

# 4. 检查技能列表
stigmergy skill list

# 5. 检查CLI状态
stigmergy status
```

---

## 常见错误信息

### 错误：`stigmergy command not found`
**原因**：Stigmergy未安装
**解决**：
```bash
npm install -g stigmergy
```

### 错误：`Cannot find module 'stigmergy'`
**原因**：Stigmergy未正确安装
**解决**：
```bash
npm uninstall -g stigmergy
npm install -g stigmergy
```

### 错误：`Permission denied`
**原因**：权限不足
**解决**：
```bash
# Windows：以管理员身份运行PowerShell
# Linux/Mac：使用sudo
sudo npm install -g ssci-subagent-skills
```

---

## 获取帮助

如果以上方法都无法解决问题，请：
1. 检查npm版本：`npm --version`（建议 >= 7.0.0）
2. 检查Node.js版本：`node --version`（建议 >= 14.0.0）
3. 查看npm日志：`npm config get cache`
4. 提交Issue：https://github.com/ptreezh/sscisubagent-skills/issues

---

## 卸载

```bash
# 卸载包
npm uninstall -g ssci-subagent-skills

# 清理配置（可选）
stigmergy skill remove ant
stigmergy skill remove field-analysis
# ... 移除其他技能
```