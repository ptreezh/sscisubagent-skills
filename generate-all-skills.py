#!/usr/bin/env python3
"""
批量生成 60+ 技能展示页面
生成日期：2026-03-23
"""

import os
from pathlib import Path

# 60 个技能包列表
skills = [
    # 质性研究方法 (20 个)
    {"dir": "grounded-theory-expert", "name": "扎根理论", "scholar": "Kathy Charmaz", "methods": ["开放编码", "轴心编码", "选择式编码", "理论饱和度"], "category": "质性研究"},
    {"dir": "actor-network-analysis-expert", "name": "行动者网络分析", "scholar": "Bruno Latour", "methods": ["行动者识别", "转译过程", "网络稳定化", "黑箱化分析"], "category": "质性研究"},
    {"dir": "bourdieu-field-analysis-expert", "name": "布迪厄场域分析", "scholar": "Pierre Bourdieu", "methods": ["场域识别", "资本分析", "习性分析", "位置 - 习性分析"], "category": "质性研究"},
    {"dir": "case-study-expert", "name": "案例研究", "scholar": "Robert K. Yin", "methods": ["案例选择", "数据收集", "模式匹配", "解释构建"], "category": "质性研究"},
    {"dir": "content-analysis-expert", "name": "内容分析", "scholar": "Klaus Krippendorff", "methods": ["编码方案", "信度检验", "类别构建", "频率分析"], "category": "质性研究"},
    {"dir": "conversation-analysis-expert", "name": "对话分析", "scholar": "Harvey Sacks", "methods": ["话轮转换", "序列组织", "修复机制", "偏好组织"], "category": "质性研究"},
    {"dir": "discourse-analysis-expert", "name": "话语分析", "scholar": "Norman Fairclough", "methods": ["文本分析", "话语实践", "社会实践", "批判分析"], "category": "质性研究"},
    {"dir": "document-analysis-expert", "name": "文档分析", "scholar": "John W. Creswell", "methods": ["文档收集", "内容编码", "主题提取", "三角验证"], "category": "质性研究"},
    {"dir": "ethnography-expert", "name": "民族志", "scholar": "Clifford Geertz", "methods": ["参与观察", "深度访谈", "田野笔记", "深描"], "category": "质性研究"},
    {"dir": "internet-research-expert", "name": "互联网研究", "scholar": "Christine Hine", "methods": ["虚拟民族志", "网络分析", "数字痕迹", "在线访谈"], "category": "质性研究"},
    {"dir": "ipa-analysis-expert", "name": "解释性现象分析", "scholar": "Jonathan Smith", "methods": ["现象学还原", "解释学循环", "个案分析", "主题提炼"], "category": "质性研究"},
    {"dir": "narrative-analysis-expert", "name": "叙事分析", "scholar": "Catherine Kohler Riessman", "methods": ["故事结构", "情节分析", "人物分析", "主题分析"], "category": "质性研究"},
    {"dir": "phenomenology-expert", "name": "现象学", "scholar": "Edmund Husserl", "methods": ["本质还原", "先验还原", "意向性分析", "生活世界"], "category": "质性研究"},
    {"dir": "secondary-analysis-expert", "name": "二手数据分析", "scholar": "Louise Corti", "methods": ["数据评估", "重新分析", "比较分析", "元分析"], "category": "质性研究"},
    {"dir": "semiotics-analysis-expert", "name": "符号学分析", "scholar": "Roland Barthes", "methods": ["能指/所指", "外延/内涵", "神话分析", "符号系统"], "category": "质性研究"},
    {"dir": "thematic-analysis-expert", "name": "主题分析", "scholar": "Virginia Braun", "methods": ["数据熟悉", "初始编码", "主题搜索", "主题审查"], "category": "质性研究"},
    {"dir": "visual-analysis-expert", "name": "视觉分析", "scholar": "Gillian Rose", "methods": ["内容分析", "符号分析", "话语分析", "实践分析"], "category": "质性研究"},
    {"dir": "social-sequence-analysis-expert", "name": "社会序列分析", "scholar": "Andrew Abbott", "methods": ["序列编码", "模式识别", "时间分析", "事件史"], "category": "质性研究"},
    {"dir": "rhetoric-analysis-expert", "name": "修辞分析", "scholar": "Kenneth Burke", "methods": ["戏剧五要素", "认同分析", "隐喻分析", "论证分析"], "category": "质性研究"},
    {"dir": "data-analysis-expert", "name": "数据分析", "scholar": "John W. Tukey", "methods": ["探索性分析", "描述统计", "推断统计", "可视化"], "category": "质性研究"},
    
    # 定量研究方法 (15 个)
    {"dir": "social-network-analysis-expert", "name": "社会网络分析", "scholar": "Linton Freeman", "methods": ["中心性分析", "社区检测", "结构洞", "网络可视化"], "category": "定量研究"},
    {"dir": "qca-analysis-expert", "name": "QCA 定性比较分析", "scholar": "Charles Ragin", "methods": ["模糊集校准", "真值表", "布尔最小化", "必要性/充分性"], "category": "定量研究"},
    {"dir": "did-analysis-expert", "name": "DID 双重差分", "scholar": "Angrist & Pischke", "methods": ["平行趋势", "双向固定效应", "稳健性检验", "安慰剂检验"], "category": "定量研究"},
    {"dir": "regression-analysis-expert", "name": "回归分析", "scholar": "Ronald Fisher", "methods": ["OLS 估计", "假设检验", "模型诊断", "共线性检验"], "category": "定量研究"},
    {"dir": "survey-design-expert", "name": "问卷设计", "scholar": "Don A. Dillman", "methods": ["问题设计", "抽样方法", "信度检验", "效度检验"], "category": "定量研究"},
    {"dir": "factor-analysis-expert", "name": "因子分析", "scholar": "Charles Spearman", "methods": ["探索性因子", "验证性因子", "因子旋转", "因子得分"], "category": "定量研究"},
    {"dir": "sem-analysis-expert", "name": "结构方程模型", "scholar": "Karl Jöreskog", "methods": ["测量模型", "结构模型", "路径分析", "模型拟合"], "category": "定量研究"},
    {"dir": "multilevel-modeling-expert", "name": "多层线性模型", "scholar": "Stephen Raudenbush", "methods": ["随机截距", "随机斜率", "跨层交互", "增长模型"], "category": "定量研究"},
    {"dir": "machine-learning-research-expert", "name": "机器学习研究", "scholar": "Tom Mitchell", "methods": ["监督学习", "无监督学习", "特征工程", "模型评估"], "category": "定量研究"},
    {"dir": "nlp-text-mining-expert", "name": "NLP 文本挖掘", "scholar": "Christopher Manning", "methods": ["分词", "词性标注", "情感分析", "主题模型"], "category": "定量研究"},
    {"dir": "bibliometric-analysis-expert", "name": "文献计量分析", "scholar": "Eugene Garfield", "methods": ["引文分析", "共引分析", "耦合分析", "h 指数"], "category": "定量研究"},
    {"dir": "meta-analysis-expert", "name": "Meta 分析", "scholar": "Gene V. Glass", "methods": ["效应量计算", "异质性检验", "发表偏倚", "亚组分析"], "category": "定量研究"},
    {"dir": "rct-experimental-design-expert", "name": "RCT 实验设计", "scholar": "Ronald A. Fisher", "methods": ["随机化", "对照组", "盲法", "样本量计算"], "category": "定量研究"},
    {"dir": "longitudinal-analysis-expert", "name": "纵向数据分析", "scholar": "John Nesselroade", "methods": ["增长曲线", "潜变量增长", "时间序列", "面板数据"], "category": "定量研究"},
    {"dir": "cas-simulation-expert", "name": "CAS 仿真模拟", "scholar": "John Holland", "methods": ["Agent 建模", "涌现分析", "适应性", "非线性"], "category": "定量研究"},
    
    # 混合方法与商业分析 (25 个)
    {"dir": "mixed-methods-expert", "name": "混合方法研究", "scholar": "John Creswell", "methods": ["三角验证", "解释性序列", "探索性序列", "转换整合"], "category": "混合方法"},
    {"dir": "business-ecosystem-expert", "name": "商业生态系统分析", "scholar": "James F. Moore", "methods": ["生态映射", "角色分析", "共同进化", "健康度评估"], "category": "商业分析"},
    {"dir": "business-model-expert", "name": "商业模式分析", "scholar": "Alexander Osterwalder", "methods": ["画布模型", "价值主张", "收入模式", "成本结构"], "category": "商业分析"},
    {"dir": "brand-equity-expert", "name": "品牌资产分析", "scholar": "David Aaker", "methods": ["品牌知名度", "品牌联想", "感知质量", "品牌忠诚度"], "category": "商业分析"},
    {"dir": "consumer-behavior-expert", "name": "消费者行为分析", "scholar": "Leon G. Schiffman", "methods": ["购买决策", "影响因素", "细分市场", "行为预测"], "category": "商业分析"},
    {"dir": "organizational-diagnosis-expert", "name": "组织诊断", "scholar": "Warren G. Bennis", "methods": ["组织评估", "问题识别", "变革建议", "效果评估"], "category": "商业分析"},
    {"dir": "system-dynamics-expert", "name": "系统动力学", "scholar": "Jay W. Forrester", "methods": ["因果回路", "存量流量", "反馈分析", "仿真模拟"], "category": "商业分析"},
    {"dir": "design-thinking-expert", "name": "设计思维", "scholar": "Tim Brown", "methods": ["共情", "定义", "构思", "原型", "测试"], "category": "商业分析"},
    {"dir": "lean-startup-expert", "name": "精益创业", "scholar": "Eric Ries", "methods": ["MVP", "构建 - 测量 - 学习", "创新核算", " pivot"], "category": "商业分析"},
    {"dir": "agile-pm-expert", "name": "敏捷项目管理", "scholar": "Jeff Sutherland", "methods": ["Scrum", "Sprint", "每日站会", "回顾会议"], "category": "商业分析"},
    {"dir": "okr-expert", "name": "OKR 目标管理", "scholar": "Andrew Grove", "methods": ["目标设定", "关键结果", "对齐", "跟踪"], "category": "商业分析"},
    {"dir": "balanced-scorecard-expert", "name": "平衡计分卡", "scholar": "Robert Kaplan", "methods": ["财务维度", "客户维度", "内部流程", "学习成长"], "category": "商业分析"},
    {"dir": "swot-analysis-expert", "name": "SWOT 分析", "scholar": "Albert Humphrey", "methods": ["优势", "劣势", "机会", "威胁"], "category": "商业分析"},
    {"dir": "pest-analysis-expert", "name": "PEST 分析", "scholar": "Francis Aguilar", "methods": ["政治", "经济", "社会", "技术"], "category": "商业分析"},
    {"dir": "porter-five-forces-expert", "name": "波特五力分析", "scholar": "Michael Porter", "methods": ["供应商议价力", "购买者议价力", "新进入者威胁", "替代品威胁", "行业竞争"], "category": "商业分析"},
    {"dir": "value-proposition-expert", "name": "价值主张分析", "scholar": "Michael Lanning", "methods": ["客户细分", "价值地图", "痛点分析", "收益分析"], "category": "商业分析"},
    {"dir": "action-research-expert", "name": "行动研究", "scholar": "Kurt Lewin", "methods": ["计划", "行动", "观察", "反思"], "category": "混合方法"},
    {"dir": "change-management-expert", "name": "变革管理", "scholar": "John P. Kotter", "methods": ["紧迫感", "指导联盟", "愿景", "授权行动"], "category": "商业分析"},
    {"dir": "digital-marx-expert", "name": "数字马克思分析", "scholar": "David Harvey", "methods": ["数字劳动", "剩余价值", "意识形态批判", "阶级结构"], "category": "社会理论"},
    {"dir": "digital-durkheim-expert", "name": "数字涂尔干分析", "scholar": "Émile Durkheim", "methods": ["集体意识", "社会团结", "神圣/世俗", "失范"], "category": "社会理论"},
    {"dir": "digital-weber-expert", "name": "数字韦伯分析", "scholar": "Max Weber", "methods": ["理性化", "科层制", "祛魅", "权威类型"], "category": "社会理论"},
    {"dir": "skill-upgrade-expert", "name": "技能升级", "scholar": "SocienceAI", "methods": ["技能评估", "学习路径", "实践项目", "认证"], "category": "工具"},
]

# 生成 HTML
html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <title>方法论技能 - SocienceAI</title>
    <meta name="description" content="60 种社会科学方法论技能，一键下载，手把手教你做研究">
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --border-color: #e5e7eb;
            --light-bg: #f9fafb;
            --white: #ffffff;
        }
        body { font-family: 'Inter', sans-serif; line-height: 1.6; color: var(--text-primary); margin: 0; padding: 0; }
        .modern-nav { background: var(--white); box-shadow: 0 2px 4px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 1000; }
        .modern-container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
        .nav-brand { display: flex; align-items: center; text-decoration: none; color: inherit; }
        .nav-logo { width: 48px; height: 48px; margin-right: 1rem; border-radius: 0.5rem; }
        .nav-menu { display: flex; list-style: none; gap: 2rem; margin: 0; padding: 0; }
        .nav-link { text-decoration: none; color: var(--text-secondary); font-weight: 500; transition: color 0.3s; }
        .nav-link:hover, .nav-link.active { color: var(--primary-color); }
        .hero-section { padding: 6rem 0; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; text-align: center; }
        .hero-title { font-size: 3rem; font-weight: 700; margin-bottom: 1rem; }
        .hero-subtitle { font-size: 1.25rem; margin-bottom: 2rem; }
        .modern-card { background: var(--white); border: 1px solid var(--border-color); border-radius: 0.75rem; padding: 1.5rem; transition: all 0.3s ease; margin-bottom: 1.5rem; }
        .modern-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.1); border-color: var(--primary-color); }
        .card-title { font-size: 1.25rem; font-weight: 600; color: var(--primary-color); margin-bottom: 0.5rem; }
        .card-scholar { font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1rem; }
        .card-methods { list-style: none; padding: 0; margin: 0 0 1rem 0; }
        .card-methods li { font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 0.25rem; }
        .card-methods li:before { content: "✓ "; color: var(--primary-color); font-weight: bold; }
        .btn { display: inline-block; padding: 0.5rem 1rem; border-radius: 0.5rem; text-decoration: none; font-weight: 600; transition: all 0.3s; cursor: pointer; border: none; font-size: 0.875rem; margin-right: 0.5rem; }
        .btn-primary { background: var(--primary-color); color: white; }
        .btn-primary:hover { background: var(--secondary-color); }
        .btn-secondary { background: transparent; color: var(--primary-color); border: 2px solid var(--primary-color); }
        .btn-secondary:hover { background: var(--primary-color); color: white; }
        .category-section { padding: 4rem 0; }
        .category-section:nth-child(even) { background: var(--light-bg); }
        .section-title { font-size: 2rem; font-weight: 700; text-align: center; margin-bottom: 0.5rem; }
        .section-subtitle { text-align: center; color: var(--text-secondary); font-size: 1rem; margin-bottom: 2rem; }
        .skills-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
        .modern-footer { background: #111827; color: #9ca3af; padding: 3rem 0; }
        .footer-brand { display: flex; align-items: center; margin-bottom: 1rem; }
        .footer-logo { width: 48px; height: 48px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1.5rem; margin-right: 1rem; }
        .footer-title { font-size: 1.5rem; font-weight: 700; color: white; }
        .footer-description { line-height: 1.6; margin-bottom: 2rem; }
        .footer-links { list-style: none; padding: 0; }
        .footer-links li { margin-bottom: 0.5rem; }
        .footer-links a { color: #9ca3af; text-decoration: none; transition: color 0.3s; }
        .footer-links a:hover { color: white; }
        .footer-bottom { margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #374151; text-align: center; }
        .search-box { max-width: 600px; margin: 2rem auto; display: flex; gap: 0.5rem; }
        .search-input { flex: 1; padding: 0.75rem 1rem; border: 2px solid var(--border-color); border-radius: 0.5rem; font-size: 1rem; }
        .search-input:focus { outline: none; border-color: var(--primary-color); }
        .filter-buttons { display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; margin: 2rem 0; }
        .filter-btn { padding: 0.5rem 1rem; border: 2px solid var(--border-color); background: white; border-radius: 2rem; cursor: pointer; transition: all 0.3s; }
        .filter-btn:hover, .filter-btn.active { border-color: var(--primary-color); background: var(--primary-color); color: white; }
        @media (max-width: 768px) { .nav-menu { display: none; } .hero-title { font-size: 2rem; } .skills-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <nav class="modern-nav">
        <div class="modern-container">
            <div style="display: flex; justify-content: space-between; align-items: center; height: 80px;">
                <a href="index.html" class="nav-brand">
                    <img src="logo.png" alt="SocienceAI Logo" class="nav-logo">
                    <div>
                        <div style="font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">SocienceAI</div>
                        <div style="font-size: 0.875rem; color: var(--text-secondary); font-weight: 400;">让社会科学与 AI 双向赋能</div>
                    </div>
                </a>
                <ul class="nav-menu">
                    <li><a href="index.html" class="nav-link">首页</a></li>
                    <li><a href="skills.html" class="nav-link active">方法论技能</a></li>
                    <li><a href="resources.html" class="nav-link">精品 AI</a></li>
                    <li><a href="Tech/index.html" class="nav-link">赋能工具</a></li>
                    <li><a href="courses/courses.html" class="nav-link">培训课程</a></li>
                    <li><a href="whitePaper/index.html" class="nav-link">白皮书</a></li>
                    <li><a href="Dao/index.html" class="nav-link">关于我们</a></li>
                    <li><a href="blog/" class="nav-link">博客</a></li>
                    <li><a href="contact.html" class="nav-link">联系我们</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <section class="hero-section">
        <div class="modern-container">
            <h1 class="hero-title">60 种专业方法论技能</h1>
            <p class="hero-subtitle">一键下载，手把手教你做研究</p>
            <div class="search-box">
                <input type="text" class="search-input" id="searchInput" placeholder="搜索技能名称、学者或方法...">
                <button class="btn btn-primary" onclick="filterSkills()">搜索</button>
            </div>
        </div>
    </section>

    <main>
        <div class="filter-buttons">
            <button class="filter-btn active" onclick="filterCategory('all')">全部</button>
            <button class="filter-btn" onclick="filterCategory('质性研究')">质性研究</button>
            <button class="filter-btn" onclick="filterCategory('定量研究')">定量研究</button>
            <button class="filter-btn" onclick="filterCategory('混合方法')">混合方法</button>
            <button class="filter-btn" onclick="filterCategory('商业分析')">商业分析</button>
            <button class="filter-btn" onclick="filterCategory('社会理论')">社会理论</button>
        </div>

'''

# 按分类生成技能卡片
categories = {}
for skill in skills:
    cat = skill["category"]
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(skill)

for cat_name, cat_skills in categories.items():
    html_template += f'''
        <section class="category-section" data-category="{cat_name}">
            <div class="modern-container">
                <h2 class="section-title">{cat_name}</h2>
                <p class="section-subtitle">{len(cat_skills)} 个专业方法论技能</p>
                <div class="skills-grid">
'''
    for skill in cat_skills:
        methods_html = "".join([f"<li>{m}</li>" for m in skill["methods"]])
        html_template += f'''
                    <div class="modern-card" data-name="{skill['name']}" data-scholar="{skill['scholar']}" data-methods="{' '.join(skill['methods'])}">
                        <h3 class="card-title">{skill['name']}</h3>
                        <p class="card-scholar">对标学者：{skill['scholar']}</p>
                        <ul class="card-methods">
                            {methods_html}
                        </ul>
                        <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                            <a href="{skill['dir']}/" class="btn btn-primary">技能详情</a>
                            <a href="{skill['dir']}/" download class="btn btn-secondary">下载技能</a>
                        </div>
                    </div>
'''
    html_template += '''
                </div>
            </div>
        </section>
'''

html_template += '''
    </main>

    <footer class="modern-footer">
        <div class="modern-container">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem;">
                <div>
                    <div class="footer-brand">
                        <div class="footer-logo">AI</div>
                        <div class="footer-title">SocienceAI</div>
                    </div>
                    <p class="footer-description">SocienceAI 致力于构建 AI 与社会科学研究的双向赋能体系，通过 AI 释放人类研究者自由创新的核心潜力，提升 AI 智能体的集体智能和社会智能。</p>
                </div>
                <div>
                    <h4 style="color: white; margin-bottom: 1rem;">快速链接</h4>
                    <ul class="footer-links">
                        <li><a href="index.html">首页</a></li>
                        <li><a href="skills.html">方法论技能</a></li>
                        <li><a href="Tech/index.html">赋能工具</a></li>
                        <li><a href="contact.html">联系我们</a></li>
                    </ul>
                </div>
                <div>
                    <h4 style="color: white; margin-bottom: 1rem;">关于我们</h4>
                    <ul class="footer-links">
                        <li><a href="Dao/index.html">关于我们</a></li>
                        <li><a href="Dao/Manifesto.html">项目使命</a></li>
                        <li><a href="privacy.html">隐私政策</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 SocienceAI. 保留所有权利.</p>
            </div>
        </div>
    </footer>

    <script>
        function filterSkills() {
            const searchInput = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.modern-card');
            cards.forEach(card => {
                const name = card.getAttribute('data-name').toLowerCase();
                const scholar = card.getAttribute('data-scholar').toLowerCase();
                const methods = card.getAttribute('data-methods').toLowerCase();
                if (name.includes(searchInput) || scholar.includes(searchInput) || methods.includes(searchInput)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        function filterCategory(category) {
            const sections = document.querySelectorAll('.category-section');
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            sections.forEach(section => {
                if (category === 'all' || section.getAttribute('data-category') === category) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
        }

        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                filterSkills();
            }
        });
    </script>
</body>
</html>
'''

# 保存文件
output_path = Path("D:/socienceAI/agentskills/skills-complete.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"✅ 生成完成：{output_path}")
print(f"📊 技能总数：{len(skills)}")
print(f"📂 分类数量：{len(categories)}")
for cat, skills_in_cat in categories.items():
    print(f"  - {cat}: {len(skills_in_cat)} 个")
