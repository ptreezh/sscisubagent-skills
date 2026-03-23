# 首页微调执行记录（本地文件）

**执行日期**: 2026-03-22  
**文件位置**: `D:\socienceAI\agentskills\website\docs\index.md`  
**执行状态**: 准备就绪

---

## 📋 本地网站文件

**源文件**: `website/docs/index.md`  
**生成文件**: `website/docs/index.html`  
**构建命令**: `npm run build`

---

## 🎯 修改内容

### 原文案
```markdown
---
layout: home
hero:
  name: SocienceAI
  text: 让社会科学研究人人可为
  tagline: 通过 AI 技术推动社会科学研究的范式革新
  actions:
    - theme: brand
      text: 开始使用
      link: /guide/quick-start
    - theme: alt
      text: 方法论
      link: /methodologies/
features:
  - icon: 📚
    title: 12 种方法论专家
    details: 扎根理论、社会网络分析等
  - icon: 🤖
    title: AI 辅助分析
    details: 智能编码、自动验证
  - icon: ✅
    title: 严格质量保证
    details: 所有报告经过严格测试
---
```

### 修改为
```markdown
---
layout: home
hero:
  name: SocienceAI
  text: 让社会科学研究人人可为
  tagline: 通过 AI 技术推动社会科学研究的范式革新
  actions:
    - theme: brand
      text: 开始使用
      link: /guide/quick-start
    - theme: alt
      text: 技能协同平台
      link: /skills/
features:
  - icon: 📚
    title: 12 种方法论技能
    details: 扎根理论、社会网络分析、QCA 等
  - icon: 🤖
    title: AI 辅助分析
    details: 智能编码、自动验证
  - icon: ✅
    title: 严格质量保证
    details: 所有报告经过严格测试
---
```

---

## 🚀 执行步骤

### Step 1: 修改 index.md

编辑文件：`D:\socienceAI\agentskills\website\docs\index.md`

**修改 1**: Hero actions
```markdown
# 原文案
- text: 方法论
  link: /methodologies/

# 修改为
- text: 技能协同平台
  link: /skills/
```

**修改 2**: features
```markdown
# 原文案
- icon: 📚
  title: 12 种方法论专家
  details: 扎根理论、社会网络分析等

# 修改为
- icon: 📚
  title: 12 种方法论技能
  details: 扎根理论、社会网络分析、QCA 等
```

### Step 2: 重新构建

```bash
cd D:\socienceAI\agentskills\website
npm run build
```

### Step 3: FTP 上传

上传生成的 `index.html` 到服务器 `/htdocs/index.html`

---

## ✅ 验证清单

- [ ] Hero 区"方法论"改为"技能协同平台"
- [ ] features"12 种方法论专家"改为"12 种方法论技能"
- [ ] 页面样式正常
- [ ] 链接正常

---

**创建日期**: 2026-03-22  
**执行状态**: 准备就绪  
**文件位置**: `website/docs/index.md`

*立即行动，快速执行*
