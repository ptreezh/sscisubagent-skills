# 技能包下载说明

**生成日期**: 2026-03-23  
**技能总数**: 60 个

---

## ⚠️ 重要说明

由于服务器配置限制，技能包 ZIP 文件暂时无法直接下载。

**解决方案**: 请从 GitHub 仓库下载技能包。

---

## 📥 下载方式

### 方式 1: GitHub 下载（推荐）

**GitHub 仓库**: https://github.com/socienceai/agentskills

1. 访问 GitHub 仓库
2. 点击 "Code" → "Download ZIP"
3. 解压到本地技能目录

### 方式 2: Git 克隆

```bash
git clone https://github.com/socienceai/agentskills.git
cd agentskills
```

### 方式 3: 单个技能下载

每个技能包都在独立的目录中，可以直接复制使用：

```
grounded-theory-expert/     # 扎根理论
social-network-analysis-expert/  # 社会网络分析
qca-analysis-expert/        # QCA
...
```

---

## 📦 技能包结构

每个技能包包含：

```
skill-name/
├── SKILL.md              # 技能定义
├── skill.yaml            # 技能配置
├── soul.md               # 角色定义（如有）
├── README.md             # 使用说明（如有）
├── tools/                # 工具模块
│   ├── analyze.py
│   └── ...
└── templates/            # 模板文件
    └── task_plan.md.template
```

---

## 🔧 使用方式

### OpenClaw

```bash
# 复制技能到技能目录
cp -r grounded-theory-expert ~/.openclaw/skills/

# 使用技能
openclaw --skill grounded-theory-expert "任务描述"
```

### WorkBuddy

```bash
# 复制技能到技能目录
cp -r grounded-theory-expert ~/.workbuddy/skills/

# 使用技能
workbuddy --skill grounded-theory-expert "任务描述"
```

### Qwen

```bash
# 复制技能到技能目录
cp -r grounded-theory-expert ~/.qwen/skills/

# 使用技能
qwen --skill grounded-theory-expert "任务描述"
```

---

## 📋 完整技能列表

### 质性研究方法 (20 个)

1. grounded-theory-expert - 扎根理论
2. actor-network-analysis-expert - 行动者网络分析
3. bourdieu-field-analysis-expert - 布迪厄场域分析
4. case-study-expert - 案例研究
5. content-analysis-expert - 内容分析
6. conversation-analysis-expert - 对话分析
7. discourse-analysis-expert - 话语分析
8. document-analysis-expert - 文档分析
9. ethnography-expert - 民族志
10. internet-research-expert - 互联网研究
11. ipa-analysis-expert - IPA 分析
12. narrative-analysis-expert - 叙事分析
13. phenomenology-expert - 现象学
14. secondary-analysis-expert - 二手数据分析
15. semiotics-analysis-expert - 符号学分析
16. thematic-analysis-expert - 主题分析
17. visual-analysis-expert - 视觉分析
18. social-sequence-analysis-expert - 社会序列分析
19. rhetoric-analysis-expert - 修辞分析
20. data-analysis-expert - 数据分析

### 定量研究方法 (15 个)

1. social-network-analysis-expert - 社会网络分析
2. qca-analysis-expert - QCA
3. did-analysis-expert - DID
4. regression-analysis-expert - 回归分析
5. survey-design-expert - 问卷设计
6. factor-analysis-expert - 因子分析
7. sem-analysis-expert - SEM
8. multilevel-modeling-expert - 多层模型
9. machine-learning-research-expert - 机器学习
10. nlp-text-mining-expert - NLP 文本挖掘
11. bibliometric-analysis-expert - 文献计量
12. meta-analysis-expert - Meta 分析
13. rct-experimental-design-expert - RCT 设计
14. longitudinal-analysis-expert - 纵向分析
15. cas-simulation-expert - CAS 仿真

### 混合方法与商业分析 (25 个)

1. mixed-methods-expert - 混合方法
2. business-ecosystem-expert - 商业生态系统
3. business-model-expert - 商业模式
4. brand-equity-expert - 品牌资产
5. consumer-behavior-expert - 消费者行为
6. organizational-diagnosis-expert - 组织诊断
7. system-dynamics-expert - 系统动力学
8. design-thinking-expert - 设计思维
9. lean-startup-expert - 精益创业
10. agile-pm-expert - 敏捷项目管理
11. okr-expert - OKR
12. balanced-scorecard-expert - 平衡计分卡
13. swot-analysis-expert - SWOT
14. pest-analysis-expert - PEST
15. porter-five-forces-expert - 波特五力
16. value-proposition-expert - 价值主张
17. action-research-expert - 行动研究
18. change-management-expert - 变革管理
19. digital-marx-expert - 数字马克思
20. digital-durkheim-expert - 数字涂尔干
21. digital-weber-expert - 数字韦伯
22. skill-upgrade-expert - 技能升级
23. historical-analysis-expert - 历史分析
24. media-analysis-expert - 媒体分析

---

## 📞 获取帮助

**GitHub Issues**: https://github.com/socienceai/agentskills/issues

**邮箱**: contact@socienceai.com

---

**更新日期**: 2026-03-23  
**维护者**: SocienceAI Team

*60 个专业方法论技能，GitHub 下载，即刻使用*
