# SocienceAI 战略调整方案

**制定日期**: 2026-03-22  
**战略核心**: 从"智能体服务"转向"方法论技能"  
**兼容平台**: 8 个国内主流平台  
**规范标准**: agentskills.io v1.0 + 平台适配器  
**使命对齐**: 让社会科学研究人人可为

---

## 🎯 战略调整原因

### 问题识别

**当前问题**:
1. "智能体"概念过于抽象，用户难以理解
2. 12 个智能体页面，但缺少实际使用教程
3. 用户不知道如何加载和使用技能
4. 缺少与国内平台的对接

**用户需求**:
- 如何下载技能？
- 如何在 WorkBuddy 中加载？
- 如何在 Coze 编程中使用？
- 如何在钉钉悟空/青豆/OpenCode 等平台导入？

### 战略机会

**市场趋势**:
- WorkBuddy、Coze 编程等国内平台火热
- 钉钉悟空企业用户众多
- agentskills.io 规范成为标准
- 社会科学 AI 应用需求增长

**我们的优势**:
- 12 种成熟的方法论技能
- 完整的 agentskills.io 规范技能包
- 工具模块齐全
- 学术规范性强

---

## 🎯 新战略定位

### 从"智能体服务"到"方法论技能"

**旧定位**: 提供 AI 智能体服务  
**新定位**: 提供遵循 agentskills.io 规范的方法论技能，兼容 8 个国内主流平台

**价值主张调整**:
```
旧：让 AI 智能体为你服务
新：让专业方法论技能在你的 AI 工具中运行
```

### 核心产品

**方法论技能包** (agentskills.io 规范):
```
skill-package/
├── SKILL.md              # 技能定义
├── skill.yaml            # 技能配置
├── tools/                # 工具模块
├── templates/            # 模板文件
├── adapters/             # 平台适配器
│   ├── workbuddy/
│   ├── coze/
│   ├── dingtalk/
│   ├── qwen/
│   ├── opencode/
│   ├── kilocode/
│   ├── stigmergy/
│   └── openclaw/
└── README.md             # 使用说明
```

**支持平台** (8 个国内主流):
- ✅ WorkBuddy（首推）
- ✅ Coze 编程（首推）
- ✅ 钉钉悟空（首推）
- ✅ Qwen（首推）
- ✅ OpenCode
- ✅ KiloCode
- ✅ Stigmergy
- ✅ OpenClaw

---

## 🚀 战略实施路径

### Phase 1: 网站内容调整（1-2 周）

**行动 1: 更新导航**
```
旧导航: Agent 服务 → 12 个智能体页面
新导航: 方法论技能 → 12 个技能包 + 使用教程
```

**行动 2: 创建教程页面**
- 通用使用教程
- OpenClaw 加载教程
- WorkBuddy 加载教程
- Coze 导入教程
- 其他平台教程

**行动 3: 更新智能体页面**
- 添加技能下载链接
- 添加各平台加载说明
- 添加使用示例

### Phase 2: 技能包标准化（2-3 周）

**行动 1: 统一技能格式**
- 制定 SKILL.md 标准
- 制定 skill.yaml 标准
- 制定工具模块标准

**行动 2: 开发平台适配器**
- OpenClaw 适配器
- WorkBuddy 适配器
- Coze 适配器
- Dify 适配器

**行动 3: 创建技能包**
- 打包 12 种方法论技能
- 添加平台适配器
- 添加使用说明

### Phase 3: 分发与推广（3-4 周）

**行动 1: GitHub 发布**
- 创建 socienceai/skills 仓库
- 发布技能包
- 添加使用文档

**行动 2: 平台技能市场**
- OpenClaw 技能市场
- WorkBuddy 技能市场
- Coze 技能商店
- Dify 应用市场

**行动 3: 教程推广**
- 视频教程制作
- 博客文章发布
- 社区推广

---

## 📊 网站结构调整方案

### 新导航结构

```
主导航（9 个）:
1. 首页
2. 方法论技能 ← 新增核心入口
3. 使用教程 ← 新增核心入口
4. 技能下载 ← 新增
5. 赋能工具 → /Tech/index.html
6. 培训课程 → /courses/courses.html
7. 白皮书 → /whitePaper/index.html
8. 关于我们 → /Dao/index.html
9. 联系我们 → /contact.html
```

### 方法论技能页面结构

```
/skills/                    # 方法论技能首页
├── /skills/grounded-theory/           # 扎根理论技能
│   ├── index.html                     # 技能介绍
│   ├── download.html                  # 下载页面
│   ├── tutorial/                      # 使用教程
│   │   ├── openclaw.html              # OpenClaw 加载
│   │   ├── workbuddy.html             # WorkBuddy 加载
│   │   ├── coze.html                  # Coze 导入
│   │   └── dify.html                  # Dify 导入
│   └── examples.html                  # 使用示例
├── /skills/social-network-analysis/   # 社会网络分析
├── /skills/actor-network-analysis/    # 行动者网络分析
├── /skills/bourdieu-field-analysis/   # 布迪厄场域分析
├── /skills/qca/                       # QCA 分析
├── /skills/did/                       # DID 分析
├── /skills/regression/                # 回归分析
├── /skills/survey/                    # 问卷设计
├── /skills/mixed-methods/             # 混合方法
├── /skills/digital-marx/              # 数字马克思
├── /skills/digital-durkheim/          # 数字涂尔干
└── /skills/digital-weber/             # 数字韦伯
```

### 使用教程页面结构

```
/tutorials/                 # 使用教程首页
├── /tutorials/getting-started/        # 快速开始
│   ├── what-are-skills.html           # 什么是技能
│   ├── how-to-download.html           # 如何下载
│   └── how-to-load.html               # 如何加载
├── /tutorials/openclaw/               # OpenClaw 教程
│   ├── installation.html              # 安装 OpenClaw
│   ├── skill-loading.html             # 技能加载
│   └── examples.html                  # 使用示例
├── /tutorials/workbuddy/              # WorkBuddy 教程
├── /tutorials/coze/                   # Coze 教程
├── /tutorials/dify/                   # Dify 教程
└── /tutorials/troubleshooting/        # 故障排查
```

---

## 🎯 核心价值主张

### 对用户的价值

**研究者**:
- ✅ 下载即用，无需配置
- ✅ 支持多种工具，选择灵活
- ✅ 学术规范，结果可信
- ✅ 持续更新，持续改进

**开发者**:
- ✅ 开放源代码，可 fork 修改
- ✅ 标准化格式，易于扩展
- ✅ 社区贡献，共同建设

**企业用户**:
- ✅ 本地部署，数据安全
- ✅ 定制化服务，满足特定需求
- ✅ 技术支持，培训服务

### 对平台的价值

**OpenClaw/WorkBuddy**:
- ✅ 丰富技能生态
- ✅ 提升平台价值
- ✅ 吸引更多用户

**Coze/Dify**:
- ✅ 专业内容填充
- ✅ 差异化竞争
- ✅ 学术背书

---

## 📈 实施时间表

### 第 1 周：网站内容调整

- [ ] 更新导航菜单
- [ ] 创建方法论技能首页
- [ ] 创建使用教程首页
- [ ] 更新 12 个技能页面（添加下载链接）

### 第 2 周：教程内容创建

- [ ] 通用使用教程
- [ ] OpenClaw 加载教程
- [ ] WorkBuddy 加载教程
- [ ] Coze 导入教程
- [ ] Dify 导入教程

### 第 3 周：技能包标准化

- [ ] 统一技能格式
- [ ] 开发平台适配器
- [ ] 打包 12 种技能
- [ ] GitHub 仓库创建

### 第 4 周：发布与推广

- [ ] GitHub 发布
- [ ] 平台技能市场发布
- [ ] 教程视频制作
- [ ] 博客文章推广

---

## 🎯 成功指标

### 短期指标（1 个月）

- [ ] 网站更新完成
- [ ] 教程内容完整
- [ ] GitHub 仓库创建
- [ ] 技能下载量 100+

### 中期指标（3 个月）

- [ ] 技能下载量 1000+
- [ ] 平台技能市场上架
- [ ] 用户案例 10+
- [ ] 社区贡献者 10+

### 长期指标（6 个月）

- [ ] 技能下载量 10000+
- [ ] 平台技能市场热门技能
- [ ] 用户案例 100+
- [ ] 社区贡献者 100+

---

## 💡 关键成功因素

### 1. 易用性

**目标**: 让用户 5 分钟内学会使用

**行动**:
- 简化下载流程
- 提供详细教程
- 制作视频教程
- 提供示例代码

### 2. 兼容性

**目标**: 支持主流平台

**行动**:
- 开发平台适配器
- 提供转换工具
- 测试各平台兼容性

### 3. 可信度

**目标**: 学术规范，结果可信

**行动**:
- 严格方法论规范
- 提供参考文献
- 提供使用示例
- 提供故障排查

### 4. 社区建设

**目标**: 建立活跃社区

**行动**:
- GitHub 社区运营
- 用户案例分享
- 技能贡献指南
- 定期更新维护

---

## 🚨 风险与应对

### 风险 1: 用户学习成本高

**应对**:
- 提供详细教程
- 制作视频教程
- 提供示例代码
- 建立问答社区

### 风险 2: 平台兼容性问题

**应对**:
- 充分测试各平台
- 提供转换工具
- 及时修复 bug
- 收集用户反馈

### 风险 3: 技能更新维护

**应对**:
- 建立更新机制
- 鼓励社区贡献
- 定期审查技能
- 提供维护文档

---

**战略制定日期**: 2026-03-22  
**战略执行期**: 4 周  
**战略负责人**: SocienceAI Team

*让社会科学研究人人可为*
