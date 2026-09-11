#!/usr/bin/env python3
"""
Soul Agent Creator - 小龙虾分身创建工具
========================================

帮助OpenClaw小白用户快速创建方法论专家分身。

用法:
    python create-soul-agent.py                           # 交互式创建
    python create-soul-agent.py --skill grounded-theory  # 指定技能创建
    python create-soul-agent.py --list                   # 列出所有可用技能
    python create-soul-agent.py --demo                   # 创建演示分身

作者: SocienceAI Soul Agent System
版本: 1.0.0
"""

import os
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path
import json

# ============================================================================
# 配置
# ============================================================================

# 模板目录
TEMPLATE_DIR = Path(__file__).parent / "templates" / "soul-agent-template"
AGENTSKILLS_DIR = Path(__file__).parent.parent

# 默认存储目录
DEFAULT_STORAGE = Path.home() / ".stigmergy" / "soul-agents"

# 技能元数据定义
SKILLS_METADATA = {
    # ===== 质性研究方法 =====
    "grounded-theory": {
        "name": "扎根理论专家",
        "name_en": "Grounded Theory Expert",
        "category": "qualitative",
        "master": "Kathy Charmaz / Strauss & Corbin",
        "school": "Constructivist Grounded Theory (Glaser & Strauss 1967)",
        "philosophy": "Symbolic Interactionism",
        "paradigm": "建构主义扎根理论",
        "key_works": [
            "Charmaz, K. (2014). Constructing Grounded Theory",
            "Strauss, A. & Corbin, J. (1990). Basics of Qualitative Research",
        ],
        "prohibitions": [
            ("禁止预设结论", "必须让数据自然涌现，不带预设假设编码"),
            ("禁止脱离原始数据", "每个编码必须有原始引文支撑"),
            ("禁止忽视负面案例", "必须主动寻找并整合矛盾证据"),
        ],
        "concepts": [
            ("开放编码", "从数据中提取初始概念"),
            ("轴心编码", "建立概念间关系"),
            ("选择式编码", "整合为核心范畴"),
        ],
        "applications": ["质性研究数据分析", "理论建构研究", "扎根理论研究"],
    },
    "actor-network-theory": {
        "name": "行动者网络理论专家",
        "name_en": "ANT Expert",
        "category": "qualitative",
        "master": "Bruno Latour",
        "school": "Actor-Network Theory (Latour 2005)",
        "philosophy": "Symmetry Principle",
        "paradigm": "技术社会学",
        "key_works": [
            "Latour, B. (2005). Reassembling the Social",
            "Callon, M. (1986). Some Elements of a Sociology of Translation",
        ],
        "prohibitions": [
            ("禁止人为/非人二分", "人与非人行动者必须对称对待"),
            ("禁止黑箱化", "必须打开每个黑箱追踪到底"),
            ("禁止预设边界", "网络边界由行动者自己定义"),
        ],
        "concepts": [
            ("行动者识别", "识别所有人类和非人行动者"),
            ("转译过程", "追踪利益赋予和动员过程"),
            ("网络稳定化", "分析网络如何维持稳定"),
        ],
        "applications": ["科技社会学研究", "创新扩散分析", "技术评估"],
    },
    "bourdieu-field-analysis": {
        "name": "布迪厄场域分析专家",
        "name_en": "Bourdieu Field Analysis Expert",
        "category": "qualitative",
        "master": "Pierre Bourdieu",
        "school": "Bourdieu's Field Theory (1984, 1993)",
        "philosophy": "Relational Thinking",
        "paradigm": "文化社会学",
        "key_works": [
            "Bourdieu, P. (1984). Distinction",
            "Bourdieu, P. (1993). The Field of Cultural Production",
        ],
        "prohibitions": [
            ("禁止本质主义解释", "坚持关系性思维，位置决定行为"),
            ("禁止单一资本分析", "必须分析经济/文化/社会/符号资本"),
            ("禁止忽略习性", "必须分析行动者的主观倾向"),
        ],
        "concepts": [
            ("场域识别", "确定分析对象的社会空间"),
            ("资本分析", "测量多种资本的分布"),
            ("位置-习性分析", "关联客观位置与主观倾向"),
        ],
        "applications": ["文化研究", "教育社会学", "权力结构分析"],
    },
    # ===== 定量研究方法 =====
    "regression-analysis": {
        "name": "回归分析专家",
        "name_en": "Regression Analysis Expert",
        "category": "quantitative",
        "master": "Ronald Fisher / Karl Pearson",
        "school": "Classical Statistics",
        "philosophy": "Hypothesis Testing",
        "paradigm": "推断统计学",
        "key_works": [
            "Fisher, R.A. (1925). Statistical Methods for Research Workers",
            "Wooldridge, J.M. (2013). Introductory Econometrics",
        ],
        "prohibitions": [
            ("禁止忽视共线性", "必须检验变量间多重共线性"),
            ("禁止忽略异方差", "必须检验并处理异方差问题"),
            ("禁止因果推断过度", "回归揭示相关，非因果"),
        ],
        "concepts": [
            ("OLS估计", "普通最小二乘法参数估计"),
            ("假设检验", "t检验、F检验、置信区间"),
            ("模型诊断", "残差分析、拟合度检验"),
        ],
        "applications": ["计量经济学分析", "社会科学实证研究", "预测建模"],
    },
    "qca-analysis": {
        "name": "定性比较分析专家",
        "name_en": "QCA Expert",
        "category": "quantitative",
        "master": "Charles Ragin",
        "school": "Qualitative Comparative Analysis (Ragin 1987)",
        "philosophy": "Set-Theoretic Thinking",
        "paradigm": "集合论因果分析",
        "key_works": [
            "Ragin, C.C. (2008). Redesigning Social Inquiry",
            "Schneider, C.Q. & Wagemann, C. (2012). Set-Theoretic Methods",
        ],
        "prohibitions": [
            ("禁止脱离理论校准", "校准必须有理论依据，不能用统计分位数"),
            ("禁止忽略案例独特性", "必须回到案例深入分析"),
            ("禁止过度简化", "至少报告复杂解和简化解"),
        ],
        "concepts": [
            ("模糊集校准", "将连续变量转化为集合隶属度"),
            ("真值表构建", "列出所有条件组合与案例分布"),
            ("布尔最小化", "简化逻辑表达式识别因果路径"),
        ],
        "applications": ["中小样本比较研究", "因果复杂性分析", "混合方法研究"],
    },
    "did-analysis": {
        "name": "双重差分分析专家",
        "name_en": "DID Analysis Expert",
        "category": "quantitative",
        "master": "Joshua Angrist & Jörn-Steffen Pischke",
        "school": "Difference-in-Differences (Angrist & Pischke 2009)",
        "philosophy": "Quasi-Experimental Design",
        "paradigm": "政策评估",
        "key_works": [
            "Angrist, J.D. & Pischke, J.S. (2009). Mostly Harmless Econometrics",
            "Bertrand, M., Duflo, E. & Mullainathan, S. (2004). How Much Should We Trust Differences-in-Differences Estimates?",
        ],
        "prohibitions": [
            ("禁止未检验平行趋势", "平行趋势检验未通过不得报告效应"),
            ("禁止忽视聚类标准误", "必须使用聚类稳健标准误"),
            ("禁止选择性报告", "必须报告所有预定义分析结果"),
        ],
        "concepts": [
            ("平行趋势假设", "处理组和对照组在干预前有相同趋势"),
            ("双向固定效应", "控制个体和时间固定效应"),
            ("稳健性检验", "安慰剂检验、敏感性分析"),
        ],
        "applications": ["政策效果评估", "准实验设计分析", "因果推断"],
    },
    # ===== 混合研究方法 =====
    "mixed-methods": {
        "name": "混合方法研究专家",
        "name_en": "Mixed Methods Expert",
        "category": "mixed",
        "master": "John Creswell / Vicki Plano Clark",
        "school": "Mixed Methods Research (Creswell & Plano Clark 2018)",
        "philosophy": "Pragmatism",
        "paradigm": "实用主义方法论",
        "key_works": [
            "Creswell, J.W. & Plano Clark, V.L. (2018). Designing and Conducting Mixed Methods Research",
            "Tashakkori, A. & Teddlie, C. (2010). SAGE Handbook of Mixed Methods Research",
        ],
        "prohibitions": [
            ("禁止简单混合", "必须有明确的整合策略"),
            ("禁止方法孤立", "定性与定量必须相互验证"),
            ("禁止顺序随意", "混合顺序必须有理论依据"),
        ],
        "concepts": [
            ("三角验证", "多方法验证同一现象"),
            ("互补设计", "定量与定性互补各自局限"),
            ("转换/整合", "在分析阶段整合证据"),
        ],
        "applications": ["复杂现象研究", "多层次分析", "理论检验与发展"],
    },
    # ===== 社会理论 =====
    "digital-marxism": {
        "name": "数字马克思分析专家",
        "name_en": "Digital Marxism Expert",
        "category": "theory",
        "master": "David Harvey / Christian Fuchs",
        "school": "Marxist Digital Studies",
        "philosophy": "Historical Materialism",
        "paradigm": "数字政治经济学",
        "key_works": [
            "Fuchs, C. (2014). Digital Labour and Karl Marx",
            "Harvey, D. (2010). A Companion to Marx's Capital",
        ],
        "prohibitions": [
            ("禁止非历史分析", "必须置于历史唯物主义框架"),
            ("禁止资本拜物教忽略", "必须揭示数字现象的拜物教形式"),
            ("禁止阶级分析缺失", "必须识别数字时代的阶级结构"),
        ],
        "concepts": [
            ("数字劳动", "分析平台经济中的劳动形式"),
            ("剩余价值", "追踪数字资本的积累机制"),
            ("意识形态批判", "揭示数字技术的意识形态功能"),
        ],
        "applications": ["平台经济研究", "数字劳动分析", "资本主义批判"],
    },
    "social-network-analysis": {
        "name": "社会网络分析专家",
        "name_en": "Social Network Analysis Expert",
        "category": "quantitative",
        "master": "Linton Freeman / Stanley Wasserman",
        "school": "Social Network Analysis (Wasserman & Faust 1994)",
        "philosophy": "Structuralism",
        "paradigm": "关系社会学",
        "key_works": [
            "Wasserman, S. & Faust, K. (1994). Social Network Analysis",
            "Borgatti, S.P. & Foster, P.C. (2003). The Network Paradigm in Organizational Research",
        ],
        "prohibitions": [
            ("禁止孤立个体观", "必须从关系角度分析"),
            ("禁止忽略结构", "必须分析网络整体结构特征"),
            ("禁止静态网络观", "必须考虑网络动态演变"),
        ],
        "concepts": [
            ("中心性分析", "识别网络中的关键节点"),
            ("社区检测", "识别网络中的子群结构"),
            ("结构洞分析", "识别信息优势位置"),
        ],
        "applications": ["组织网络研究", "社交网络分析", "知识网络研究"],
    },
}


# ============================================================================
# 辅助函数
# ============================================================================


def print_header(text):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_subheader(text):
    """打印副标题"""
    print(f"\n📌 {text}")


def format_skill_list():
    """格式化技能列表"""
    lines = []
    lines.append("\n📚 可用的方法论分身:\n")

    # 按类别分组
    categories = {}
    for skill_id, meta in SKILLS_METADATA.items():
        cat = meta["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((skill_id, meta))

    category_names = {
        "qualitative": "📖 质性研究方法",
        "quantitative": "📊 定量研究方法",
        "mixed": "🔄 混合研究方法",
        "theory": "🧠 社会理论视角",
    }

    for cat, skills in categories.items():
        lines.append(f"\n{category_names.get(cat, cat)}")
        lines.append("-" * 40)
        for skill_id, meta in skills:
            lines.append(f"  • {skill_id:25} - {meta['name']}")

    return "\n".join(lines)


def load_template(template_name):
    """加载模板文件"""
    template_path = TEMPLATE_DIR / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"模板文件不存在: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def generate_soul_id(skill_id, custom_name=None):
    """生成Soul ID"""
    if custom_name:
        # 从自定义名称生成ID
        name_part = "".join(c for c in custom_name if c.isalnum())[:10].lower()
    else:
        name_part = skill_id.replace("-", "")[:10]

    timestamp = datetime.now().strftime("%Y%m%d")
    return f"soul_{name_part}_{timestamp}"


def fill_template(template, skill_id, meta, custom_name=None, created_date=None):
    """填充模板变量"""
    soul_id = generate_soul_id(skill_id, custom_name)
    display_name = custom_name or meta["name"]

    replacements = {
        "{SOUL_NAME}": soul_id,
        "{SOUL_ID}": soul_id,
        "{SOUL_DISPLAY_NAME}": display_name,
        "{CREATED_DATE}": created_date or datetime.now().strftime("%Y-%m-%d"),
        "{METHODOLOGY}": meta["name"],
        "{METHODOLOGY_MASTER}": meta["master"],
        "{METHODOLOGY_SCHOOL}": meta["school"],
        "{PARADIGM}": meta["philosophy"],
        "{FIELD}": meta["category"],
        "{SUBFIELD}": meta["name"],
        "{KEY_WORK_1}": meta["key_works"][0] if meta["key_works"] else "",
        "{KEY_WORK_2}": meta["key_works"][1] if len(meta["key_works"]) > 1 else "",
        "{TRAIT_1}": "学术严谨",
        "{TRAIT_2}": "方法论精准",
        "{TRAIT_3}": "开放性思维",
        "{COMMUNICATION_STYLE}": "学术规范",
        "{TONE}": "专业严谨",
        "{COGNITIVE_APPROACH}": "证据驱动",
        "{THINKING_PATTERN}": "归纳与演绎结合",
        "{PROHIBITION_1_NAME}": meta["prohibitions"][0][0]
        if len(meta["prohibitions"]) > 0
        else "",
        "{PROHIBITION_1_DESC}": meta["prohibitions"][0][1]
        if len(meta["prohibitions"]) > 0
        else "",
        "{PROHIBITION_2_NAME}": meta["prohibitions"][1][0]
        if len(meta["prohibitions"]) > 1
        else "",
        "{PROHIBITION_2_DESC}": meta["prohibitions"][1][1]
        if len(meta["prohibitions"]) > 1
        else "",
        "{PROHIBITION_3_NAME}": meta["prohibitions"][2][0]
        if len(meta["prohibitions"]) > 2
        else "",
        "{PROHIBITION_3_DESC}": meta["prohibitions"][2][1]
        if len(meta["prohibitions"]) > 2
        else "",
        "{ANALYSIS_TYPE_1}": meta["applications"][0]
        if len(meta["applications"]) > 0
        else "",
        "{ANALYSIS_TYPE_2}": meta["applications"][1]
        if len(meta["applications"]) > 1
        else "",
        "{ANALYSIS_TYPE_3}": meta["applications"][2]
        if len(meta["applications"]) > 2
        else "",
        "{APPLICATION_1}": meta["applications"][0]
        if len(meta["applications"]) > 0
        else "",
        "{APPLICATION_2}": meta["applications"][1]
        if len(meta["applications"]) > 1
        else "",
        "{APPLICATION_3}": meta["applications"][2]
        if len(meta["applications"]) > 2
        else "",
        "{RESEARCH_TYPE_1}": meta["applications"][0]
        if len(meta["applications"]) > 0
        else "",
        "{RESEARCH_TYPE_2}": meta["applications"][1]
        if len(meta["applications"]) > 1
        else "",
        "{RESEARCH_TYPE_3}": meta["applications"][2]
        if len(meta["applications"]) > 2
        else "",
        "{SKILL_1}": f"{skill_id}-expert",
        "{SKILL_2}": "academic-writing",
        "{VERSION}": "1.0.0",
        # METHODOLOGY.md 变量
        "{SCHOOL_1}": "主流学派",
        "{SCHOOL_1_AUTHOR}": meta["master"],
        "{SCHOOL_1_VIEW}": meta["philosophy"],
        "{SCHOOL_2}": "相关学派",
        "{SCHOOL_2_AUTHOR}": "",
        "{SCHOOL_2_VIEW}": "",
        "{PARADIGM_NAME}": meta["philosophy"],
        "{PARADIGM_DESCRIPTION}": "",
        "{CONCEPT_1}": meta["concepts"][0][0] if len(meta["concepts"]) > 0 else "",
        "{CONCEPT_1_DEFINITION}": "",
        "{CONCEPT_1_OPERATION}": "",
        "{CONCEPT_1_EXAMPLE}": "",
        "{CONCEPT_2}": meta["concepts"][1][0] if len(meta["concepts"]) > 1 else "",
        "{CONCEPT_2_DEFINITION}": "",
        "{CONCEPT_2_OPERATION}": "",
        "{CONCEPT_2_EXAMPLE}": "",
        "{STEP_1_NAME}": "数据准备",
        "{STEP_1_ACTION_1}": "数据收集与整理",
        "{STEP_1_ACTION_2}": "数据清洗与编码",
        "{STEP_2_NAME}": "核心分析",
        "{STEP_2_ACTION_1}": "执行分析方法",
        "{STEP_2_ACTION_2}": "质量检查",
        "{STEP_3_NAME}": "结果生成",
        "{STEP_3_ACTION_1}": "结果汇总",
        "{STEP_3_ACTION_2}": "报告撰写",
        "{STEP_4_NAME}": "验证",
        "{STEP_4_ACTION_1}": "完整性检查",
        "{STEP_4_ACTION_2}": "学术规范性审查",
        "{RELIABILITY_1}": "内部一致性",
        "{RELIABILITY_1_STANDARD}": "α > 0.7",
        "{RELIABILITY_1_METHOD}": "Cronbach's α",
        "{RELIABILITY_2}": "评分者信度",
        "{RELIABILITY_2_STANDARD}": "κ > 0.7",
        "{RELIABILITY_2_METHOD}": "Krippendorff's α",
        "{VALIDITY_1}": "内容效度",
        "{VALIDITY_1_STANDARD}": "专家评审通过",
        "{VALIDITY_1_METHOD}": "专家咨询",
        "{VALIDITY_2}": "建构效度",
        "{VALIDITY_2_STANDARD}": "因子载荷 > 0.5",
        "{VALIDITY_2_METHOD}": "验证性因子分析",
        "{ERROR_1_NAME}": "方法误用",
        "{ERROR_1_MANIFESTATION}": "",
        "{ERROR_1_CORRECT}": "",
        "{ERROR_2_NAME}": "过度推断",
        "{ERROR_2_MANIFESTATION}": "",
        "{ERROR_2_CORRECT}": "",
        "{ERROR_3_NAME}": "样本偏差",
        "{ERROR_3_MANIFESTATION}": "",
        "{ERROR_3_CORRECT}": "",
        "{REFERENCE_1}": meta["key_works"][0] if meta["key_works"] else "",
        "{REFERENCE_1_DESC}": "核心文献",
        "{REFERENCE_2}": meta["key_works"][1] if len(meta["key_works"]) > 1 else "",
        "{REFERENCE_2_DESC}": "方法指南",
        "{REFERENCE_3}": "",
        "{REFERENCE_3_DESC}": "",
    }

    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)

    return result


def create_soul_agent(skill_id, custom_name=None, output_dir=None, verbose=True):
    """创建Soul Agent分身"""

    if skill_id not in SKILLS_METADATA:
        raise ValueError(f"未知的技能ID: {skill_id}")

    meta = SKILLS_METADATA[skill_id]
    soul_id = generate_soul_id(skill_id, custom_name)
    display_name = custom_name or meta["name"]
    created_date = datetime.now().strftime("%Y-%m-%d")

    # 确定输出目录
    if output_dir is None:
        output_dir = DEFAULT_STORAGE / soul_id
    else:
        output_dir = Path(output_dir)

    # 创建目录结构
    dirs_to_create = [
        output_dir,
        output_dir / "memory",
        output_dir / "memory" / "lessons",
        output_dir / "memory" / "patterns",
        output_dir / "evolution",
        output_dir / "cases",
        output_dir / "cases" / "positive",
        output_dir / "cases" / "negative",
        output_dir / "templates",
        output_dir / "logs",
        output_dir / "data",
        output_dir / "results",
    ]

    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"\n📁 创建目录结构: {output_dir}")

    # 生成并保存文件
    files_to_generate = [
        ("SOUL.md", "SOUL.md"),
        ("SOUL_CONFIG.yaml", "SOUL_CONFIG.yaml"),
        ("METHODOLOGY.md", "METHODOLOGY.md"),
    ]

    for template_name, output_name in files_to_generate:
        template = load_template(template_name)
        content = fill_template(template, skill_id, meta, custom_name, created_date)

        output_path = output_dir / output_name
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        if verbose:
            print(f"  ✅ 创建: {output_name}")

    # 生成README.md
    readme_content = f"""# {display_name}

> Soul Agent - {meta["name"]}分身

## 关于

本分身对标 **{meta["master"]}** 的 **{meta["name"]}** 方法论，
严格遵守学术规范，支持自主进化。

## 快速开始

```bash
# 在OpenClaw中激活本分身
# 设置环境变量
export SOUL_AGENT_ID="{soul_id}"

# 或直接指定配置文件
opencode --soul-config ~/.stigmergy/soul-agents/{soul_id}/SOUL.md
```

## 配置

详细配置请查看: [SOUL_CONFIG.yaml](SOUL_CONFIG.yaml)

## 进化历史

| 日期 | 事件 |
|------|------|
| {created_date} | Soul Agent创建 |

## 目录结构

```
{soul_id}/
├── SOUL.md           # 灵魂身份定义
├── SOUL_CONFIG.yaml  # 配置文件
├── METHODOLOGY.md    # 方法论文档
├── memory/           # 记忆系统
│   ├── lessons/      # 教训记忆
│   └── patterns/     # 成功模式
├── evolution/        # 进化记录
├── cases/           # 案例库
│   ├── positive/    # 正面案例
│   └── negative/    # 负面案例
├── templates/       # 工作模板
├── logs/           # 日志
├── data/           # 数据
└── results/        # 结果
```

---
*由Soul Agent Creator生成 | {created_date}*
"""

    readme_path = output_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    if verbose:
        print(f"  ✅ 创建: README.md")

    # 生成记忆初始化文件
    lessons_init = f"""# 教训记忆 - {display_name}

> 记录分析过程中的教训和错误

## 记录格式

```markdown
## [日期] 教训标题

### 问题
描述遇到的问题

### 原因
根本原因分析

### 教训
从中学到的经验

### 防止措施
如何避免再次发生
```

## 历史记录

暂无记录

---
*初始化: {created_date}*
"""

    patterns_init = f"""# 成功模式 - {display_name}

> 记录成功的分析模式和最佳实践

## 记录格式

```markdown
## 模式名称

### 适用场景
何时使用此模式

### 执行步骤
具体操作步骤

### 成功案例
相关案例引用

### 关键要点
核心成功因素
```

## 模式库

暂无记录

---
*初始化: {created_date}*
"""

    evolution_init = f"""# 进化日志 - {display_name}

> 记录Soul Agent的进化历史

## 进化事件

| 日期 | 事件类型 | 描述 | 经验值变化 |
|------|----------|------|------------|
| {created_date} | 创建 | Soul Agent初始化 | +0 |

## 统计

- 总进化次数: 0
- 总经验值: 0
- 最高质量评分: 0

---
*初始化: {created_date}*
"""

    with open(
        output_dir / "memory" / "lessons" / "README.md", "w", encoding="utf-8"
    ) as f:
        f.write(lessons_init)

    with open(
        output_dir / "memory" / "patterns" / "README.md", "w", encoding="utf-8"
    ) as f:
        f.write(patterns_init)

    with open(output_dir / "evolution" / "log.md", "w", encoding="utf-8") as f:
        f.write(evolution_init)

    if verbose:
        print(f"  ✅ 创建: memory/ & evolution/")

    # 生成元数据文件
    metadata = {
        "soul_id": soul_id,
        "skill_id": skill_id,
        "display_name": display_name,
        "created": created_date,
        "version": "1.0.0",
        "master": meta["master"],
        "methodology": meta["name"],
        "category": meta["category"],
        "storage_path": str(output_dir),
        "status": "active",
    }

    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    if verbose:
        print(f"  ✅ 创建: metadata.json")

    return {
        "soul_id": soul_id,
        "display_name": display_name,
        "output_dir": str(output_dir),
        "skill": skill_id,
        "master": meta["master"],
    }


def interactive_create():
    """交互式创建分身"""
    print_header("🦞 Soul Agent 分身创建向导")

    print("\n欢迎使用小龙虾分身创建工具！")
    print("我将帮助您创建一个对标顶级学术专家的AI分身。\n")

    # 选择技能
    print(format_skill_list())

    while True:
        skill_input = input("\n🔹 请选择技能ID (输入数字或ID): ").strip().lower()

        # 尝试转换为数字
        try:
            idx = int(skill_input) - 1
            skill_ids = list(SKILLS_METADATA.keys())
            if 0 <= idx < len(skill_ids):
                skill_id = skill_ids[idx]
                break
        except ValueError:
            pass

        # 直接输入ID
        if skill_input in SKILLS_METADATA:
            skill_id = skill_input
            break

        print("❌ 无效选择，请重试")

    meta = SKILLS_METADATA[skill_id]
    print(f"\n✅ 已选择: {meta['name']}")
    print(f"   对标学者: {meta['master']}")

    # 自定义名称
    custom_name = input("\n🔹 请输入分身名称 (直接回车使用默认): ").strip()
    if not custom_name:
        custom_name = None
        print(f"   使用默认名称: {meta['name']}")
    else:
        print(f"   自定义名称: {custom_name}")

    # 确认创建
    print("\n" + "-" * 40)
    confirm = input("📌 确认创建分身? (y/n): ").strip().lower()

    if confirm != "y":
        print("\n❌ 已取消创建")
        return

    # 创建分身
    print("\n🔨 正在创建分身...\n")

    try:
        result = create_soul_agent(skill_id, custom_name, verbose=True)

        print("\n" + "=" * 60)
        print("  ✅ Soul Agent 创建成功!")
        print("=" * 60)
        print(f"\n📋 分身信息:")
        print(f"   Soul ID: {result['soul_id']}")
        print(f"   名称: {result['display_name']}")
        print(f"   对标: {result['master']}")
        print(f"   路径: {result['output_dir']}")
        print("\n📖 使用方法:")
        print(f"   在OpenClaw中设置: export SOUL_AGENT_ID={result['soul_id']}")
        print("\n" + "=" * 60)

    except Exception as e:
        print(f"\n❌ 创建失败: {e}")
        raise


def create_demo():
    """创建演示分身"""
    print_header("🦞 创建演示分身")
    print("\n📖 将为扎根理论创建完整演示分身...\n")

    result = create_soul_agent("grounded-theory", "我的扎根理论研究助手", verbose=True)

    print("\n" + "=" * 60)
    print("  ✅ 演示分身创建成功!")
    print("=" * 60)
    print(f"\n📋 分身信息:")
    print(f"   Soul ID: {result['soul_id']}")
    print(f"   名称: {result['display_name']}")
    print(f"   路径: {result['output_dir']}")
    print("\n📖 接下来:")
    print(f"   1. 查看生成的文件: {result['output_dir']}")
    print(f"   2. 修改SOUL.md自定义分身行为")
    print(f"   3. 在OpenClaw中激活分身")
    print("=" * 60)


# ============================================================================
# 主程序
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Soul Agent Creator - 小龙虾分身创建工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python create-soul-agent.py --interactive    # 交互式创建
  python create-soul-agent.py --skill grounded-theory --name "我的助手"
  python create-soul-agent.py --list           # 列出所有技能
  python create-soul-agent.py --demo           # 创建演示分身
        """,
    )

    parser.add_argument("--skill", "-s", help="指定技能ID创建分身")
    parser.add_argument("--name", "-n", help="自定义分身名称")
    parser.add_argument("--output", "-o", help="指定输出目录")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有可用技能")
    parser.add_argument("--demo", "-d", action="store_true", help="创建演示分身")

    args = parser.parse_args()

    # 列出技能
    if args.list:
        print_header("📚 可用的方法论分身")
        print(format_skill_list())
        print()
        return

    # 创建演示分身
    if args.demo:
        create_demo()
        return

    # 交互式创建
    if args.interactive or (not args.skill and not args.demo):
        interactive_create()
        return

    # 指定技能创建
    if args.skill:
        if args.skill not in SKILLS_METADATA:
            print(f"❌ 未知技能ID: {args.skill}")
            print(format_skill_list())
            sys.exit(1)

        print(f"\n🔨 创建分身: {args.skill}")
        if args.name:
            print(f"   名称: {args.name}")

        result = create_soul_agent(args.skill, args.name, args.output, verbose=True)

        print("\n" + "=" * 60)
        print("  ✅ 创建成功!")
        print("=" * 60)
        print(f"\n📋 Soul ID: {result['soul_id']}")
        print(f"📍 路径: {result['output_dir']}")
        return

    # 无参数时显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
