# SocienceAI 首页微调方案

**执行日期**: 2026-03-22  
**执行原则**: 保持首页整体结构，仅微调关键内容

---

## 🎯 微调内容

### 1. Hero 区 CTA 按钮

**原文案**:
```
了解我们 →
智能体协同平台 →
快速上手 →
```

**修改为**:
```
了解我们 →
技能协同平台 →
快速上手 →
```

### 2. 服务板块标题

**原文案**:
```
社会科学专业技能
```

**修改为**:
```
社会科学专业技能（12 种方法论技能）
```

**原描述**:
```
扎根理论分析、场域分析、社会网络分析等专业技能，为社会科学研究提供智能辅助。
```

**修改为**:
```
扎根理论、社会网络分析、行动者网络理论、布迪厄场域分析、QCA、DID 等 12 种专业方法论技能，一键加载，手把手教你做研究。
```

### 3. 增加技能栏目

**在"社会科学专业技能"卡片中增加**:
```
<p style="margin-top: 1rem; padding: 0.5rem; background: #f0f9ff; border-radius: 0.25rem; font-size: 0.875rem;">
<strong>🔥 首推平台：</strong>WorkBuddy（研究者首选）| Stigmergy（多 CLI 协同）| Coze（免费额度）| 钉钉悟空（企业集成）| Qwen（中文能力强）
</p>
<p style="margin-top: 0.5rem; font-size: 0.875rem;">
<strong>📚 技能列表：</strong>扎根理论 | 社会网络分析 | 行动者网络理论 | 布迪厄场域分析 | QCA | DID | 回归分析 | 问卷设计 | 混合方法 | 数字马克思 | 数字涂尔干 | 数字韦伯
</p>
<p style="margin-top: 0.5rem;">
<a href="/skills/" style="color: #2563eb; text-decoration: none; font-weight: 600;">查看全部 12 种技能 →</a>
</p>
```

### 4. 页脚链接更新

**原链接**:
```
Agent 服务 → /ai-agents.html
```

**修改为**:
```
方法论技能 → /skills/
```

---

## 📋 执行步骤

### Step 1: 备份原文件

```bash
# FTP 连接后
右键点击 /htdocs/index.html
下载到本地 backup/index-2026-03-22-backup.html
```

### Step 2: 修改文件

**修改位置 1**: Hero 区 CTA 按钮（约第 150 行）
```html
<!-- 原代码 -->
<a href="#agents" class="btn btn-secondary">智能体协同平台 →</a>

<!-- 修改后 -->
<a href="#skills" class="btn btn-secondary">技能协同平台 →</a>
```

**修改位置 2**: 服务板块第一个卡片（约第 200 行）
```html
<!-- 原代码 -->
<h3>社会科学专业技能</h3>
<p>扎根理论分析、场域分析、社会网络分析等专业技能，为社会科学研究提供智能辅助。</p>

<!-- 修改后 -->
<h3>社会科学专业技能（12 种方法论技能）</h3>
<p>扎根理论、社会网络分析、行动者网络理论、布迪厄场域分析、QCA、DID 等 12 种专业方法论技能，一键加载，手把手教你做研究。</p>
<p style="margin-top: 1rem; padding: 0.5rem; background: #f0f9ff; border-radius: 0.25rem; font-size: 0.875rem;">
<strong>🔥 首推平台：</strong>WorkBuddy（研究者首选）| Stigmergy（多 CLI 协同）| Coze（免费额度）| 钉钉悟空（企业集成）| Qwen（中文能力强）
</p>
<p style="margin-top: 0.5rem; font-size: 0.875rem;">
<strong>📚 技能列表：</strong>扎根理论 | 社会网络分析 | 行动者网络理论 | 布迪厄场域分析 | QCA | DID | 回归分析 | 问卷设计 | 混合方法 | 数字马克思 | 数字涂尔干 | 数字韦伯
</p>
<p style="margin-top: 0.5rem;">
<a href="/skills/" style="color: #2563eb; text-decoration: none; font-weight: 600;">查看全部 12 种技能 →</a>
</p>
```

**修改位置 3**: 页脚链接（约第 300 行）
```html
<!-- 原代码 -->
<li><a href="/ai-agents.html">Agent 服务</a></li>

<!-- 修改后 -->
<li><a href="/skills/">方法论技能</a></li>
```

### Step 3: 上传文件

```bash
# 在 FTP 客户端中
拖拽修改后的 index.html 到远程 /htdocs/
确认覆盖
```

### Step 4: 验证

访问 http://www.socienceai.com
检查修改是否正确显示

---

## ✅ 验证清单

- [ ] Hero 区"智能体协同平台"改为"技能协同平台"
- [ ] 服务板块第一个卡片增加 12 种方法论技能说明
- [ ] 服务板块第一个卡片增加首推平台
- [ ] 服务板块第一个卡片增加技能列表
- [ ] 页脚"Agent 服务"改为"方法论技能"
- [ ] 页面样式正常
- [ ] 链接正常

---

**执行日期**: 2026-03-22  
**执行者**: SocienceAI Soul  
**原则**: 微调，不更换首页

*立即行动，快速执行*
