# SocienceAI 90 天网站自主建设计划

> 🔴 **完全由 AI Agent 自主执行，无需人类团队**

**制定日期**: 2026-03-22
**执行者**: AI Agent (Qwen CLI)
**目标**: socienceAI.com 上线并获取首批用户

---

## 🎯 使命对齐

**使命**: 通过 AI 技术推动社会科学研究的范式革新，让严谨的社会科学方法论不再高深，让高质量的研究人人可为。

**网站的作用**:
1. 用户了解 SocienceAI 的窗口
2. 用户使用工具的入口
3. 用户获取帮助的渠道
4. 品牌建设和传播的载体

---

## 📊 现状盘点（Day 0）

### 已有资产

| 资产 | 状态 | 位置 |
|------|------|------|
| 12 种方法论 Skill | ✅ 完成 | `agentskills/` 目录下 12 个目录 |
| Soul Agent Creator | ✅ 完成 | `soul-agent-creator/` |
| 技术文档 | ✅ ~11000 行 | 各目录下 |
| 自主进化系统 | ✅ 完成 | `autonomous-evolution-engine.py` |
| 战略执行系统 | ✅ 完成 | `strategic-execution-engine.py` |

### 缺失内容

| 内容 | 优先级 | 工作量估算 |
|------|--------|-----------|
| 域名注册 | P0 | 30 分钟 |
| 网站框架 | P0 | 2 天 |
| 首页内容 | P0 | 1 天 |
| 方法论页面 (12 个) | P0 | 3 天 |
| 使用文档 | P1 | 2 天 |
| 博客系统 | P1 | 1 天 |
| 部署上线 | P0 | 1 天 |

---

## 🎯 90 天计划（AI 自主执行版）

### 第一阶段：网站上线（Day 1-14）

**目标**: socienceAI.com 上线，有基本内容

#### Week 1: 基础设施

**Day 1: 域名与托管**

任务清单：
- [ ] 检查域名是否已注册
- [ ] 如未注册，指导用户注册（需要用户付费）
- [ ] 选择托管平台（推荐 Vercel，免费）
- [ ] 创建 GitHub 仓库

**CLI 执行命令**:
```bash
# 创建项目目录
mkdir -p socienceai-website
cd socienceai-website

# 初始化 Git
git init

# 创建 Vercel 项目（需要用户先注册 Vercel 账号）
vercel init
```

**Day 2-3: 网站框架搭建**

使用 VitePress（简单、快速、适合文档型网站）

**CLI 执行命令**:
```bash
# 创建 VitePress 项目
npm create vitepress@latest . -- --template docs

# 安装依赖
npm install

# 创建基础目录结构
mkdir -p docs/.vitepress
mkdir -p docs/methodologies
mkdir -p docs/guide
mkdir -p docs/about
```

**配置文件** (`docs/.vitepress/config.mts`):
```javascript
export default {
  title: 'SocienceAI',
  description: '让社会科学研究人人可为',
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '方法论', link: '/methodologies/' },
      { text: '使用指南', link: '/guide/' },
      { text: '关于', link: '/about/' }
    ],
    sidebar: [
      {
        text: '方法论',
        items: [
          { text: '扎根理论', link: '/methodologies/grounded-theory' },
          { text: '社会网络分析', link: '/methodologies/sna' },
          // ... 其他 10 种
        ]
      }
    ]
  }
}
```

**Day 4-5: 首页内容生成**

**CLI 执行命令**:
```bash
# 生成首页内容
# 使用 AI 生成以下内容
```

首页内容 (`docs/index.md`):
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
  - title: 12 种方法论专家
    details: 扎根理论、社会网络分析、行动者网络理论等
  - title: AI 辅助分析
    details: 智能编码、自动验证、持续进化
  - title: 完全免费开源
    details: 开放源代码，欢迎贡献
---
```

**Day 6-7: 方法论页面生成**

**CLI 执行命令**:
```bash
# 为每种方法论生成页面
# 从已有的 soul.md 提取内容
```

每个方法论页面模板 (`docs/methodologies/grounded-theory.md`):
```markdown
# 扎根理论专家

## 概述

扎根理论是一种质性研究方法，由 Glaser 和 Strauss 于 1967 年提出。

## 核心概念

- 开放编码
- 轴心编码
- 选择式编码
- 理论饱和度

## 适用场景

- 访谈数据分析
- 理论建构研究
- 探索性研究

## 如何使用

```bash
# 使用 CLI
qwen "使用扎根理论分析以下访谈数据..."
```

## 对标学者

Kathy Charmaz / Strauss & Corbin

## 核心著作

- Charmaz, K. (2014). Constructing Grounded Theory
- Strauss, A. & Corbin, J. (1990). Basics of Qualitative Research
```

#### Week 2: 内容填充 + 部署

**Day 8-10: 使用文档生成**

**CLI 执行命令**:
```bash
# 生成使用文档
# 从 soul-agent-creator 的 README.md 提取
```

**Day 11-12: 关于页面 + 联系方式**

**Day 13-14: 部署上线**

**CLI 执行命令**:
```bash
# 构建网站
npm run build

# 部署到 Vercel
vercel --prod
```

**完成标准**:
- ✅ socienceAI.com 可访问
- ✅ 首页完整
- ✅ 12 种方法论页面完成
- ✅ 使用文档完成
- ✅ 关于页面完成

---

### 第二阶段：内容建设（Day 15-45）

**目标**: 建立完整的内容体系，吸引自然流量

#### Week 3-4: 博客系统 + 内容生成

**任务**:
- [ ] 搭建博客系统（VitePress 自带博客功能）
- [ ] 生成 10 篇方法论文章
- [ ] 生成 5 个案例研究

**CLI 执行命令**:
```bash
# 创建博客目录
mkdir -p docs/blog/posts

# 生成文章（使用 AI）
```

**文章主题**（10 篇）:
1. 什么是扎根理论？
2. 如何编码访谈数据？
3. 社会网络分析入门
4. 行动者网络理论详解
5. 布迪厄场域分析指南
6. QCA 方法实操
7. 混合方法研究设计
8. 数字马克思分析框架
9. 如何选择合适的研究方法？
10. AI 如何辅助社会科学研究

**案例研究**（5 个）:
1. 研究生学位论文数据分析
2. 组织创新研究
3. 员工满意度研究
4. 平台经济研究
5. 在线社区分析

#### Week 5-6: SEO 优化

**任务**:
- [ ] 关键词研究
- [ ] 页面 SEO 优化
- [ ] 提交 Google Search Console
- [ ] 创建 sitemap.xml

**CLI 执行命令**:
```bash
# 生成 sitemap
npm install sitemap
# 运行 sitemap 生成脚本
```

**SEO 关键词**:
- 扎根理论
- 社会网络分析
- 质性研究方法
- 社会科学 AI
- 研究方法论

---

### 第三阶段：推广获客（Day 46-90）

**目标**: 获取首批 100 用户

#### Week 7-8: 社交媒体启动

**任务**:
- [ ] 创建 Twitter 账号
- [ ] 创建知乎账号
- [ ] 发布首条内容

**CLI 执行命令**:
```bash
# 生成社交媒体内容
# Twitter: 140 字符以内
# 知乎：长文格式
```

**内容计划**:
- Twitter: 每日 1 条（产品更新、方法论小知识）
- 知乎: 每周 2 篇（方法论问答）

#### Week 9-10: 社区推广

**任务**:
- [ ] Reddit r/socialscience 发帖
- [ ] 知乎回答问题（方法论相关）
- [ ] 学术论坛发帖

**CLI 执行命令**:
```bash
# 生成推广内容
# 注意：不要 spam，要提供价值
```

#### Week 11-13: 用户反馈收集

**任务**:
- [ ] 添加网站分析（Google Analytics）
- [ ] 添加反馈表单
- [ ] 收集并分析用户反馈

**CLI 执行命令**:
```bash
# 添加 Google Analytics
# 创建反馈表单（使用 Google Forms 或 Typeform）
```

---

## 📈 关键指标

| 指标 | Day 14 | Day 45 | Day 90 |
|------|--------|--------|--------|
| 网站上线 | ✅ | - | - |
| 内容页面 | 15 | 30 | 50 |
| 博客文章 | 0 | 10 | 20 |
| 月访问量 | 0 | 100 | 1000 |
| 活跃用户 | 0 | 10 | 100 |
| 用户反馈 | 0 | 3 | 20 |

---

## 🔧 每日执行流程（AI 自主）

### 每日自动任务

**早晨（自动执行）**:
```bash
# 1. 检查网站状态
curl -I https://socienceAI.com

# 2. 查看前一日数据（如果有 Google Analytics）
# 3. 生成今日任务列表
```

**工作时间（AI 执行）**:
```bash
# 1. 内容生成（文章、页面）
# 2. 代码优化（网站功能）
# 3. SEO 优化
# 4. 社交媒体内容生成
```

**晚上（自动执行）**:
```bash
# 1. 提交代码到 GitHub
# 2. 触发 Vercel 部署
# 3. 记录今日完成
# 4. 生成明日计划
```

---

## 📋 第一周详细计划

### Day 1: 域名与托管

**任务**:
- [ ] 检查域名状态
- [ ] 注册域名（需要用户协助付费，约$12/年）
- [ ] 创建 Vercel 账号（免费）
- [ ] 创建 GitHub 账号（免费）

**需要用户协助**:
- 注册域名（$12/年）
- 注册 Vercel 账号
- 注册 GitHub 账号

**CLI 执行**:
```bash
# 创建项目目录
mkdir -p D:\socienceAI\website
cd D:\socienceAI\website
git init
```

### Day 2-3: 网站框架

**任务**:
- [ ] 安装 VitePress
- [ ] 创建配置文件
- [ ] 创建导航结构
- [ ] 测试本地运行

**CLI 执行**:
```bash
npm create vitepress@latest . -- --template docs
npm install
npm run dev
```

### Day 4-5: 首页生成

**任务**:
- [ ] 生成首页内容
- [ ] 设计页面布局
- [ ] 添加 CTA 按钮

**CLI 执行**:
```bash
# 生成 docs/index.md
```

### Day 6-7: 方法论页面

**任务**:
- [ ] 生成 12 个方法论页面
- [ ] 从已有 soul.md 提取内容
- [ ] 统一页面格式

**CLI 执行**:
```bash
# 批量生成方法论页面
python scripts/generate-methodology-pages.py
```

---

## ⚠️ 风险与应对

### 风险 1: 域名已被注册

**应对**:
- 使用替代域名：socience-ai.com、socienceai.org
- 或购买已注册域名（成本高）

### 风险 2: AI 生成内容质量不足

**应对**:
- 人工审核关键内容（需要用户协助）
- 多次迭代优化
- 收集用户反馈改进

### 风险 3: 没有用户访问

**应对**:
- 持续 SEO 优化
- 主动社区推广
- 付费广告测试（小规模）

---

## 📞 需要用户协助的事项

**一次性事项**:
- [ ] 注册域名（$12/年）
- [ ] 注册 Vercel 账号（免费）
- [ ] 注册 GitHub 账号（免费）
- [ ] 注册 Google Analytics（免费）

**定期事项**:
- [ ] 每周审核内容质量（30 分钟）
- [ ] 每月查看数据报告（1 小时）

---

## ✅ 成功标准

### Day 14 成功标准

- ✅ socienceAI.com 可访问
- ✅ 首页完整（使命、价值主张、CTA）
- ✅ 12 种方法论页面完成
- ✅ 使用文档完成
- ✅ 网站加载速度 < 3 秒

### Day 90 成功标准

- ✅ 月访问量 1000+
- ✅ 活跃用户 100+
- ✅ 用户反馈 20+ 条
- ✅ Google 搜索"socienceAI"可找到
- ✅ 社交媒体粉丝 500+

---

*完全由 AI Agent 自主执行*

*"让社会科学研究人人可为"*
