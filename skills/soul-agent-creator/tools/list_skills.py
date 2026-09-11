#!/usr/bin/env python3
"""
列出所有可用的方法论技能

用法:
    from tools import list_skills
    skills = list_skills.list_all()
    print(list_skills.format_display(skills))
"""

from typing import Dict, List

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
            ("位置 - 习性分析", "关联客观位置与主观倾向"),
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
            ("OLS 估计", "普通最小二乘法参数估计"),
            ("假设检验", "t 检验、F 检验、置信区间"),
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
    "digital-durkheim": {
        "name": "数字涂尔干分析专家",
        "name_en": "Digital Durkheim Expert",
        "category": "theory",
        "master": "Émile Durkheim",
        "school": "Digital Sociology of Religion",
        "philosophy": "Functionalism",
        "paradigm": "数字社会团结",
        "key_works": [
            "Durkheim, E. (1912). The Elementary Forms of the Religious Life",
            "Lynch, G. (2012). After Durkheim: An Agenda for the Sociology of Religion",
        ],
        "prohibitions": [
            ("禁止忽视集体意识", "必须分析数字社会的集体表征"),
            ("禁止混淆机械/有机团结", "必须区分传统与数字团结形式"),
            ("禁止忽略失范现象", "必须分析数字社会的失范问题"),
        ],
        "concepts": [
            ("集体意识", "分析数字社会的共同信仰和情感"),
            ("社会团结", "研究数字社会的整合机制"),
            ("神圣/世俗", "区分数字社会的神圣与世俗领域"),
        ],
        "applications": ["数字宗教研究", "在线社区分析", "网络仪式研究"],
    },
    "digital-weber": {
        "name": "数字韦伯分析专家",
        "name_en": "Digital Weber Expert",
        "category": "theory",
        "master": "Max Weber",
        "school": "Digital Rationalization Theory",
        "philosophy": "Interpretive Sociology",
        "paradigm": "数字理性化",
        "key_works": [
            "Weber, M. (1922). Economy and Society",
            "Weber, M. (1905). The Protestant Ethic and the Spirit of Capitalism",
        ],
        "prohibitions": [
            ("禁止忽视理性化过程", "必须分析数字社会的理性化趋势"),
            ("禁止混淆权威类型", "必须区分传统/魅力/法理权威"),
            ("禁止忽略祛魅现象", "必须分析数字社会的祛魅过程"),
        ],
        "concepts": [
            ("理性化", "分析数字社会的理性化程度"),
            ("科层制", "研究数字组织的科层化特征"),
            ("祛魅", "分析传统权威的祛魅过程"),
        ],
        "applications": ["平台科层制研究", "数字权威分析", "技术理性批判"],
    },
    "survey-design": {
        "name": "问卷设计专家",
        "name_en": "Survey Design Expert",
        "category": "quantitative",
        "master": "Don A. Dillman / Floyd J. Fowler",
        "school": "Survey Methodology",
        "philosophy": "Standardized Measurement",
        "paradigm": "调查研究方法",
        "key_works": [
            "Dillman, D.A. (2014). Internet, Phone, Mail, and Mixed-Mode Surveys",
            "Fowler, F.J. (2014). Survey Research Methods",
        ],
        "prohibitions": [
            ("禁止引导性问题", "问题必须中立无引导"),
            ("禁止双重问题", "每个问题只问一件事"),
            ("禁止忽略预测试", "必须经过认知访谈和预测试"),
        ],
        "concepts": [
            ("问题设计", "设计清晰无歧义的问题"),
            ("抽样方法", "选择合适的抽样策略"),
            ("信效度检验", "检验量表的信度和效度"),
        ],
        "applications": ["社会调查", "市场研究", "政策评估"],
    },
}

CATEGORY_NAMES = {
    "qualitative": "📖 质性研究方法",
    "quantitative": "📊 定量研究方法",
    "mixed": "🔄 混合研究方法",
    "theory": "🧠 社会理论视角",
}


def list_all() -> Dict[str, Dict]:
    """列出所有可用技能"""
    return SKILLS_METADATA


def list_by_category(category: str) -> Dict[str, Dict]:
    """按类别列出技能"""
    return {
        skill_id: meta
        for skill_id, meta in SKILLS_METADATA.items()
        if meta["category"] == category
    }


def get_skill(skill_id: str) -> Dict:
    """获取单个技能的详细信息"""
    if skill_id not in SKILLS_METADATA:
        raise ValueError(f"未知的技能 ID: {skill_id}")
    return SKILLS_METADATA[skill_id]


def format_display(skills: Dict[str, Dict] = None) -> str:
    """格式化显示技能列表"""
    if skills is None:
        skills = SKILLS_METADATA
    
    lines = []
    lines.append("\n📚 可用的方法论分身:\n")
    
    # 按类别分组
    categories = {}
    for skill_id, meta in skills.items():
        cat = meta["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((skill_id, meta))
    
    for cat, skill_list in categories.items():
        lines.append(f"\n{CATEGORY_NAMES.get(cat, cat)}")
        lines.append("-" * 40)
        for skill_id, meta in skill_list:
            lines.append(f"  • {skill_id:25} - {meta['name']}")
    
    return "\n".join(lines)


def recommend_by_field(field: str) -> List[str]:
    """根据研究领域推荐技能"""
    recommendations = {
        "管理学": ["grounded-theory", "social-network-analysis", "mixed-methods"],
        "社会学": ["bourdieu-field-analysis", "actor-network-theory", "digital-marxism"],
        "教育学": ["grounded-theory", "survey-design", "mixed-methods"],
        "传播学": ["social-network-analysis", "digital-durkheim", "digital-weber"],
        "经济学": ["regression-analysis", "did-analysis", "qca-analysis"],
        "政治学": ["bourdieu-field-analysis", "qca-analysis", "digital-marxism"],
        "心理学": ["survey-design", "regression-analysis", "mixed-methods"],
    }
    
    for key, skills in recommendations.items():
        if key in field:
            return skills
    
    # 默认推荐
    return ["grounded-theory", "mixed-methods", "survey-design"]


def search_by_keyword(keyword: str) -> List[str]:
    """根据关键词搜索技能"""
    results = []
    keyword_lower = keyword.lower()
    
    for skill_id, meta in SKILLS_METADATA.items():
        # 搜索名称
        if keyword_lower in meta["name"].lower() or keyword_lower in skill_id.lower():
            results.append(skill_id)
            continue
        
        # 搜索应用
        for app in meta.get("applications", []):
            if keyword_lower in app.lower():
                results.append(skill_id)
                break
        
        # 搜索概念
        for concept, _ in meta.get("concepts", []):
            if keyword_lower in concept.lower():
                results.append(skill_id)
                break
    
    return list(set(results))  # 去重
