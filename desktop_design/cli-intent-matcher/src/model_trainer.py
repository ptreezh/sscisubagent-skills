# CLI意图分类模型训练器

import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from pathlib import Path
import re
from typing import Dict, List, Tuple, Any


class CLIIntentModelTrainer:
    """训练CLI意图分类模型"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.classifier = MultiOutputClassifier(
            RandomForestClassifier(n_estimators=100, random_state=42)
        )
        self.label_encoders = {}
        
    def create_training_data(self) -> pd.DataFrame:
        """创建训练数据集"""
        # 基于已收集的CLI信息创建训练数据
        training_data = []
        
        # 读取之前收集的CLI信息
        raw_data_path = Path("cli-intent-matcher/data/raw/cli_info.json")
        if raw_data_path.exists():
            with open(raw_data_path, 'r', encoding='utf-8') as f:
                cli_info = json.load(f)
        else:
            # 如果没有收集到数据，使用模拟数据
            cli_info = self._get_sample_data()
        
        # 根据CLI工具和技能信息生成训练样本
        training_samples = self._generate_training_samples(cli_info)
        
        for sample in training_samples:
            training_data.append({
                'user_intent': sample['intent'],
                'cli_tool': sample['cli_tool'],
                'skill_used': sample.get('skill', ''),
                'parameters': sample.get('parameters', ''),
                'expected_output_format': sample.get('output_format', 'text')
            })
        
        return pd.DataFrame(training_data)
    
    def _get_sample_data(self) -> Dict:
        """获取示例数据（当没有实际收集到数据时）"""
        return {
            "cli_tools": {
                "claude": {
                    "available": True,
                    "parameters": ["--print", "--model", "--agent", "--tools"]
                },
                "qwen": {
                    "available": True,
                    "parameters": ["--print", "--model", "--tools"]
                },
                "gemini": {
                    "available": True,
                    "parameters": ["--print", "--model", "--tools"]
                }
            },
            "skills": {
                "frontend-design": {
                    "description": "Create distinctive, production-grade frontend interfaces"
                },
                "docx": {
                    "description": "Document creation, editing, and analysis"
                },
                "pdf": {
                    "description": "PDF manipulation toolkit"
                }
            }
        }
    
    def _generate_training_samples(self, cli_info: Dict) -> List[Dict]:
        """基于CLI信息生成训练样本"""
        samples = []
        
        # 为每个CLI工具和技能生成相关意图
        for tool_name, tool_info in cli_info.get("cli_tools", {}).items():
            if tool_info.get("available", False):
                # 生成与该工具相关的意图
                tool_intents = self._get_tool_intents(tool_name, tool_info)
                samples.extend(tool_intents)
        
        # 为每个技能生成相关意图
        for skill_name, skill_info in cli_info.get("skills", {}).items():
            skill_intents = self._get_skill_intents(skill_name, skill_info)
            samples.extend(skill_intents)
        
        return samples
    
    def _get_tool_intents(self, tool_name: str, tool_info: Dict) -> List[Dict]:
        """为CLI工具生成意图样本"""
        intents = []
        
        # 根据工具名称生成相关意图
        tool_descriptions = {
            "claude": [
                "code review", "programming help", "software engineering", "debug code",
                "write documentation", "explain code", "refactor code", "create test",
                "generate code", "fix bug", "code analysis", "security review",
                "performance optimization", "architecture design", "algorithm implementation",
                "write research paper", "analyze literature", "summarize research", 
                "draft academic content", "review scholarly work", "analyze data",
                "create report", "write proposal", "edit manuscript", "format paper"
            ],
            "qwen": [
                "code generation", "programming assistance", "algorithm design",
                "system design", "code optimization", "data processing",
                "web development", "mobile app development", "api design",
                "analyze text", "process documents", "data analysis",
                "content creation", "text processing", "document analysis"
            ],
            "gemini": [
                "research", "information lookup", "data analysis", "content creation",
                "summarization", "translation", "report writing", "data visualization",
                "market analysis", "trend analysis", "academic research",
                "literature review", "scholarly analysis", "content synthesis",
                "research synthesis", "academic writing", "study analysis",
                "data interpretation", "research methodology", "theoretical analysis"
            ],
            "codebuddy": [
                "code help", "programming tips", "debugging", "best practices",
                "code explanation", "learning programming", "code mentoring",
                "syntax help", "debug assistance", "coding guidance",
                "write documentation", "create tutorials", "explain concepts",
                "draft technical content", "review technical writing"
            ],
            "stigmergy": [
                "research collaboration", "multi-agent coordination", "cross-CLI workflow",
                "skill orchestration", "agent collaboration", "workflow automation",
                "project coordination", "team collaboration", "process management"
            ]
        }
        
        descriptions = tool_descriptions.get(tool_name, ["general task"])
        
        # 英文表达方式
        for desc in descriptions:
            intents.append({
                "intent": f"Help me with {desc} using {tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"I need {tool_name} to {desc}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"Can {tool_name} help with {desc}?",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"Use {tool_name} for {desc}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"{tool_name} to {desc}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"I want to {desc}, which tool should I use? Maybe {tool_name}?",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"Could you help me {desc} with {tool_name}?",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"Help me {desc} using {tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"I'm working on {desc}, can {tool_name} assist?",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"Assist me with {desc} using {tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"I need assistance with {desc}, {tool_name} might help",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"Can you {desc} for me using {tool_name}?",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"Let's {desc} together with {tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"Help with {desc} - use {tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"Try to {desc} using {tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"See if {tool_name} can help with {desc}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
        
        # 中文表达方式
        chinese_descriptions = {
            "claude": [
                "代码审查", "编程帮助", "软件工程", "调试代码", "写文档",
                "解释代码", "重构代码", "创建测试", "生成代码", "修复bug",
                "代码分析", "安全审查", "性能优化", "架构设计", "算法实现",
                "写研究论文", "分析文献", "总结研究", "撰写学术内容", "审阅学术作品",
                "分析数据", "创建报告", "写提案", "编辑手稿", "格式化论文"
            ],
            "qwen": [
                "代码生成", "编程辅助", "算法设计", "系统设计", "代码优化",
                "数据处理", "网页开发", "移动应用开发", "API设计",
                "分析文本", "处理文档", "数据分析", "内容创作", "文本处理", "文档分析"
            ],
            "gemini": [
                "研究", "信息查询", "数据分析", "内容创作", "总结",
                "翻译", "报告撰写", "数据可视化", "市场分析", "趋势分析", "学术研究",
                "文献综述", "学术分析", "内容综合", "研究综合", "学术写作", "研究分析",
                "数据解释", "研究方法论", "理论分析", "社科研究", "人文研究"
            ],
            "codebuddy": [
                "代码帮助", "编程技巧", "调试", "最佳实践", "代码解释",
                "编程学习", "代码指导", "语法帮助", "调试协助", "编程指导",
                "写文档", "创建教程", "解释概念", "撰写技术内容", "审阅技术写作"
            ],
            "stigmergy": [
                "研究协作", "多智能体协调", "跨CLI工作流", "技能编排", "智能体协作",
                "工作流自动化", "项目协调", "团队协作", "过程管理", "文档协作"
            ]
        }
        
        chinese_descs = chinese_descriptions.get(tool_name, ["一般任务"])
        
        for desc in chinese_descs:
            intents.append({
                "intent": f"帮我{desc}，使用{tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"用{tool_name}帮我{desc}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"{tool_name}能帮我{desc}吗？",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"我想{desc}，{tool_name}可以吗？",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"使用{tool_name}来{desc}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"{tool_name} {desc}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"请帮我{desc}，用{tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"我需要{desc}，{tool_name}合适吗？",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"我正在做{desc}，{tool_name}能协助吗？",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"协助我{desc}，使用{tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"帮我{desc}，{tool_name}也许能帮忙",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"能帮我{desc}吗？用{tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"我们一起{desc}，用{tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"帮忙{desc} - 用{tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"尝试{desc}，使用{tool_name}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
            intents.append({
                "intent": f"看看{tool_name}能否帮忙{desc}",
                "cli_tool": tool_name,
                "parameters": " ".join(tool_info.get("parameters", []))
            })
        
        return intents
    
    def _get_skill_intents(self, skill_name: str, skill_info: Dict) -> List[Dict]:
        """为技能生成意图样本"""
        intents = []
        
        # 根据技能描述生成相关意图
        skill_descriptions = {
            "frontend-design": [
                "create UI component", "design web page", "build interface",
                "create button", "design dashboard", "make website", "build component",
                "create layout", "design user interface", "make responsive design",
                "create landing page", "build SPA", "design mobile interface",
                "create distinctive frontend interfaces", "avoid generic AI aesthetics", 
                "create polished UI design", "generate creative code", "build web components",
                "create web pages", "build artifacts", "create posters", "build applications",
                "create websites", "build landing pages", "create dashboards", 
                "build React components", "create HTML/CSS layouts", "style web UI",
                "beautify web UI", "create production-grade interfaces"
            ],
            "docx": [
                "create document", "edit document", "format document", 
                "add tracked changes", "review document", "write report",
                "create proposal", "format text", "add comments", "edit content",
                "write research paper", "draft academic paper", "format thesis",
                "create manuscript", "edit scholarly work", "review academic content",
                "write literature review", "create academic report", "format research paper",
                "edit thesis", "create research proposal", "write academic content",
                "write project proposal", "draft project application", "create project plan",
                "write book outline", "create chapter outline", "draft chapter content",
                "create research summary", "write abstract", "draft introduction",
                "write methodology", "create results section", "write conclusion",
                "draft literature review", "create bibliography", "format references",
                "write synthesis analysis", "create comprehensive analysis", "draft executive summary",
                "write detailed report", "create task breakdown", "outline sections",
                "create chapter breakdown", "draft précis analysis", "write précis",
                "comprehensive document creation", "editing and analysis", "professional documents",
                "working with tracked changes", "document tasks"
            ],
            "pdf": [
                "extract text", "merge PDFs", "split PDF", "fill form",
                "convert PDF", "analyze PDF", "extract data", "sign PDF",
                "annotate PDF", "compress PDF", "rotate pages", "add watermark",
                "extract research data", "analyze academic papers", "extract citations",
                "review scholarly articles", "annotate research papers", "compare documents",
                "extract literature", "review research papers", "analyze references",
                "extract research findings", "compare research results", "review academic content",
                "comprehensive PDF manipulation", "extracting text and tables", "creating new PDFs",
                "merging/splitting documents", "handling forms", "fill in PDF form",
                "programmatically process PDF", "generate PDF", "analyze PDF documents"
            ],
            "xlsx": [
                "create spreadsheet", "analyze data", "create chart",
                "calculate formulas", "format data", "pivot table", "create dashboard",
                "import data", "export data", "create report", "analyze trends",
                "create pivot", "format cells", "create formula", "analyze research data",
                "create data visualization", "statistical analysis", "data modeling",
                "analyze survey data", "create research charts", "process academic data",
                "create project timeline", "analyze project metrics", "create budget sheet",
                "analyze project data", "create task breakdown", "track project progress",
                "create resource allocation", "analyze project risks", "create milestone chart",
                "comprehensive spreadsheet creation", "editing and analysis", "formulas and formatting",
                "reading or analyzing data", "modify existing spreadsheets", "data analysis",
                "visualization in spreadsheets", "recalculating formulas"
            ],
            "pptx": [
                "create presentation", "design slides", "format slides",
                "add animations", "create charts", "insert images", "add transitions",
                "create template", "edit slides", "design layout",
                "create academic presentation", "design research slides", "format conference presentation",
                "create thesis defense", "make research summary", "design academic poster",
                "create project proposal", "design project presentation", "create project overview",
                "make project summary", "design project slides", "create project roadmap",
                "present research findings", "create literature review presentation", "outline chapters",
                "presentation creation", "editing and analysis", "working with layouts",
                "adding comments or speaker notes", "presentation tasks"
            ],
            "algorithmic-art": [
                "create generative art", "make visual art", "create patterns",
                "design flow field", "create particle system", "make animation",
                "generate art", "create visual effect", "design interactive art",
                "creating algorithmic art using p5.js", "seeded randomness", "interactive parameter exploration",
                "generative art", "algorithmic art", "flow fields", "particle systems",
                "create original algorithmic art", "avoid copyright violations"
            ],
            "webapp-testing": [
                "test web app", "debug UI", "test functionality", "capture screenshot",
                "automate testing", "verify behavior", "test responsive", "check forms",
                "interacting with and testing local web applications", "Playwright",
                "verifying frontend functionality", "debugging UI behavior",
                "capturing browser screenshots", "viewing browser logs"
            ],
            "doc-coauthoring": [
                "collaborative writing", "co-author document", "team writing",
                "collaborative editing", "joint document creation", "team collaboration",
                "research collaboration", "academic co-authoring", "document teamwork",
                "collaborative research", "team document", "joint writing project",
                "collaborative project proposal", "team research paper", "collaborative literature review",
                "joint project application", "team thesis writing", "collaborative book writing",
                "structured workflow for co-authoring documentation", "writing documentation",
                "proposals", "technical specs", "decision docs", "structured content",
                "efficiently transfer context", "refine content through iteration",
                "verify the doc works for readers"
            ],
            "internal-comms": [
                "write report", "create status update", "draft communication",
                "write newsletter", "create update", "draft internal document",
                "write project update", "create leadership update", "draft company communication",
                "write team update", "create progress report", "draft internal memo",
                "create project report", "draft project status", "write team communication",
                "create project summary", "draft team update", "write department report",
                "write all kinds of internal communications", "status reports",
                "leadership updates", "3P updates", "company newsletters", "FAQs",
                "incident reports", "project updates", "etc."
            ],
            "mathematical-statistics": [
                "statistical analysis", "data analysis", "research statistics",
                "analyze data", "perform statistical test", "calculate metrics",
                "analyze survey", "research methodology", "statistical modeling",
                "data interpretation", "research analysis", "statistical report",
                "analyze research data", "perform statistical analysis", "data modeling",
                "analyze project data", "perform statistical tests", "create statistical models",
                "analyze survey results", "calculate statistical measures", "interpret statistical data",
                "social science research", "descriptive statistics", "inferential statistics",
                "regression analysis", "variance analysis", "factor analysis",
                "complete statistical support"
            ],
            "field-analysis": [
                "field analysis", "sociological analysis", "research field study",
                "analyze social field", "study social dynamics", "analyze power relations",
                "research social structures", "analyze capital distribution",
                "study social context", "analyze social phenomena", "field research",
                "analyze research field", "study field dynamics", "analyze field structures",
                "research social field", "study field relations", "analyze field characteristics",
                "executing field analysis", "field boundary identification",
                "capital distribution analysis", "autonomy assessment",
                "habitus pattern analysis", "analyze social field structure",
                "power relations", "cultural capital"
            ],
            "ant": [
                "actor-network theory", "analyze networks", "research actor networks",
                "analyze relationships", "study network dynamics", "analyze connections",
                "research network theory", "study actor relations", "network analysis",
                "analyze heterogeneous networks", "study translation process", "network research",
                "analyze research networks", "study actor interactions", "analyze network relations",
                "performing actor-network theory analysis", "participant identification",
                "relationship network construction", "translation process tracking",
                "network dynamic analysis", "analyze heterogeneous actor networks",
                "trace fact construction process", "analyze technology social interaction"
            ],
            "network-computation": [
                "network analysis", "analyze relationships", "compute network metrics",
                "analyze social networks", "study network structures", "compute centrality",
                "analyze network data", "compute network properties", "network visualization",
                "study network dynamics", "analyze connections", "network modeling",
                "analyze research networks", "compute network measures", "study network patterns",
                "social network computing analysis", "network construction",
                "centrality measurement", "community detection", "network visualization",
                "complete network analysis support"
            ],
            "conflict-resolution": [
                "resolve conflict", "manage disagreement", "resolve分歧",
                "handle conflict", "manage dispute", "resolve academic disagreement",
                "handle research conflict", "resolve scholarly分歧", "manage academic debate",
                "resolve research分歧", "handle scholarly disagreement", "resolve academic conflict",
                "resolve project disagreements", "manage team conflicts", "resolve research disputes",
                "conflict resolution tools", "research disagreements", "theory",
                "methodology", "interpretation", "values", "constructive dialogue",
                "consensus building strategies"
            ],
            "validity-reliability": [
                "test validity", "analyze reliability", "research validity",
                "check research validity", "analyze research reliability", "test reliability",
                "validate research", "check validity", "analyze internal consistency",
                "test research validity", "analyze信度效度", "research quality assessment",
                "validate research methods", "check study validity", "analyze research quality",
                "research reliability analysis", "internal consistency", "test-retest reliability",
                "inter-rater reliability", "construct validity", "content validity",
                "criterion validity", "comprehensive analysis"
            ],
            "mcp-builder": [
                "creating high-quality MCP servers", "Model Context Protocol",
                "interact with external services", "well-designed tools",
                "building MCP servers", "integrate external APIs", "services",
                "Python FastMCP", "Node/TypeScript MCP SDK", "creating MCP (Model Context Protocol) servers",
                "enable LLMs to interact with external services", "well-designed tools",
                "building MCP servers to integrate external APIs or services"
            ],
            "skill-creator": [
                "creating effective skills", "creating a new skill", "update an existing skill",
                "extend Claude's capabilities", "specialized knowledge", "workflows",
                "tool integrations", "creating effective skills",
                "creating a new skill or update an existing skill",
                "extend Claude's capabilities with specialized knowledge",
                "workflows or tool integrations"
            ],
            "theme-factory": [
                "styling artifacts with a theme", "slides", "docs", "reportings",
                "HTML landing pages", "10 pre-set themes", "colors/fonts",
                "apply to any artifact", "generate a new theme on-the-fly",
                "styling artifacts with a theme", "10 pre-set themes with colors/fonts",
                "apply to any artifact that has been creating",
                "generate a new theme on-the-fly"
            ],
            "web-artifacts-builder": [
                "creating elaborate multi-component claude.ai HTML artifacts",
                "modern frontend web technologies", "React", "Tailwind CSS", "shadcn/ui",
                "complex artifacts requiring state management", "routing",
                "shadcn/ui components", "not for simple single-file HTML/JSX artifacts",
                "suite of tools for creating elaborate, multi-component claude.ai HTML artifacts",
                "using modern frontend web technologies", "React", "Tailwind CSS", "shadcn/ui",
                "complex artifacts requiring state management", "routing", "shadcn/ui components",
                "not for simple single-file HTML/JSX artifacts"
            ],
            "slack-gif-creator": [
                "creating animated GIFs optimized for Slack",
                "constraints", "validation tools", "animation concepts",
                "animated GIFs for Slack", "make me a GIF of X doing Y for Slack",
                "knowledge and utilities for creating animated GIFs optimized for Slack",
                "provides constraints", "validation tools", "animation concepts",
                "use when users request animated GIFs for Slack"
            ],
            "canvas-design": [
                "create beautiful visual art in .png and .pdf documents",
                "design philosophy", "create a poster", "piece of art", "design",
                "other static piece", "create original visual designs",
                "never copying existing artists' work", "avoid copyright violations",
                "create beautiful visual art", "using design philosophy",
                "when the user asks to create a poster", "piece of art", "design",
                "or other static piece", "create original visual designs",
                "never copying existing artists' work to avoid copyright violations"
            ],
            "brand-guidelines": [
                "Applies Anthropic's official brand colors and typography",
                "any sort of artifact", "having Anthropic's look-and-feel",
                "brand colors", "style guidelines", "visual formatting",
                "company design standards", "apply Anthropic's official brand colors",
                "typography to any sort of artifact", "benefit from having Anthropic's look-and-feel",
                "when brand colors or style guidelines", "visual formatting",
                "or company design standards apply"
            ],
            "alienation-analysis": [
                "performing alienation analysis", "social science research",
                "analyze alienation", "study alienation", "research alienation",
                "sociological analysis of alienation", "psychological analysis of alienation"
            ]
        }
        
        descriptions = skill_descriptions.get(skill_name, ["use skill"])
        
        # 英文表达方式
        for desc in descriptions:
            intents.append({
                "intent": f"Use {skill_name} to {desc}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"I want to {desc} with {skill_name}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"Can I use {skill_name} to {desc}?",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"I need to {desc}, should I use {skill_name}?",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"Help me {desc} using {skill_name}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"Use {skill_name} for {desc}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"{skill_name} to {desc}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"Could you help me {desc} with {skill_name}?",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
        
        # 中文表达方式
        chinese_skill_descriptions = {
            "frontend-design": [
                "创建UI组件", "设计网页", "构建界面", "创建按钮", "设计仪表板",
                "制作网站", "构建组件", "创建布局", "设计用户界面", "制作响应式设计",
                "创建登录页面", "构建单页应用", "设计移动界面",
                "创建独特前端界面", "避免通用AI美学", "创建精致UI设计", "生成创意代码",
                "构建网页组件", "创建网页", "构建工件", "创建海报", "构建应用",
                "创建网站", "构建登录页面", "创建仪表板", "构建React组件", 
                "创建HTML/CSS布局", "样式化网页UI", "美化网页UI", "创建生产级界面"
            ],
            "docx": [
                "创建文档", "编辑文档", "格式化文档", "添加修订", "审阅文档",
                "撰写报告", "创建提案", "格式化文本", "添加评论", "编辑内容",
                "写研究论文", "起草学术论文", "格式化学位论文", "创建手稿", "编辑学术作品",
                "审阅学术内容", "写文献综述", "创建学术报告", "格式化研究论文",
                "编辑论文", "创建研究提案", "写学术内容",
                "写项目申请", "起草项目申请书", "创建项目计划", "写项目论证",
                "创建著作大纲", "创建章节大纲", "起草章节内容", "写研究报告",
                "写文献综述", "创建研究摘要", "写摘要", "起草引言",
                "写方法论", "创建结果部分", "写结论", "起草文献综述",
                "创建参考文献", "格式化引用", "写综合分析", "创建全面分析", "起草执行摘要",
                "写详细报告", "创建任务分解", "创建章节细分", "起草精要分析",
                "写论文摘要", "创建章节细分", "起草综合分析",
                "全面文档创建", "编辑和分析", "专业文档", "处理修订更改",
                "文档任务"
            ],
            "pdf": [
                "提取文本", "合并PDF", "拆分PDF", "填写表单", "转换PDF",
                "分析PDF", "提取数据", "签署PDF", "注释PDF", "压缩PDF",
                "旋转页面", "添加水印", "提取研究数据", "分析学术论文", "提取引用",
                "审阅学术文章", "注释研究论文", "比较文档",
                "提取文献", "审阅研究论文", "分析参考文献", "提取研究发现",
                "比较研究成果", "审阅学术内容",
                "全面PDF操作", "提取文本和表格", "创建新PDF", "合并/拆分文档",
                "处理表单", "填写PDF表单", "程序化处理PDF", "生成PDF", "分析PDF文档"
            ],
            "xlsx": [
                "创建电子表格", "分析数据", "创建图表", "计算公式", "格式化数据",
                "数据透视表", "创建仪表板", "导入数据", "导出数据", "创建报告",
                "分析趋势", "创建透视表", "格式化单元格", "创建公式", "分析研究数据",
                "创建数据可视化", "统计分析", "数据建模", "分析调查数据", "创建研究图表",
                "处理学术数据", "创建项目时间线", "分析项目指标", "创建预算表",
                "分析项目数据", "创建任务分解", "跟踪项目进度", "创建资源分配",
                "分析项目风险", "创建里程碑图表",
                "全面电子表格创建", "编辑和分析", "公式和格式化", "读取或分析数据",
                "修改现有电子表格", "数据分析", "电子表格中的数据可视化", "重新计算公式"
            ],
            "pptx": [
                "创建演示文稿", "设计幻灯片", "格式化幻灯片", "添加动画", "创建图表",
                "插入图片", "添加过渡效果", "创建模板", "编辑幻灯片", "设计布局",
                "创建学术演示", "设计研究幻灯片", "格式化会议演示",
                "创建论文答辩", "制作研究摘要", "设计学术海报",
                "创建项目申请", "设计项目演示", "创建项目概览",
                "制作项目摘要", "设计项目幻灯片", "创建项目路线图",
                "展示研究成果", "创建文献综述演示", "概述章节",
                "演示文稿创建", "编辑和分析", "处理布局", "添加评论或演讲者备注",
                "演示文稿任务"
            ],
            "algorithmic-art": [
                "创建生成艺术", "制作视觉艺术", "创建图案", "设计流场", "创建粒子系统",
                "制作动画", "生成艺术", "创建视觉效果", "设计交互艺术",
                "使用p5.js创建算法艺术", "随机种子", "交互参数探索",
                "生成艺术", "算法艺术", "流场", "粒子系统", "创建原始算法艺术",
                "避免版权侵犯"
            ],
            "webapp-testing": [
                "测试网页应用", "调试UI", "测试功能", "捕获截图", "自动化测试",
                "验证行为", "测试响应式", "检查表单",
                "与本地网页应用交互和测试", "Playwright", "验证前端功能",
                "调试UI行为", "捕获浏览器截图", "查看浏览器日志"
            ],
            "doc-coauthoring": [
                "协作写作", "合作撰写文档", "团队写作", "协作编辑", "联合文档创建",
                "团队协作", "研究协作", "学术合作", "文档团队合作", "协作研究",
                "团队文档", "联合写作项目",
                "协作项目申请", "团队研究论文", "协作文献综述",
                "联合项目申请", "团队论文写作", "协作著作写作",
                "协作写作文档结构化工作流", "编写文档", "提案", "技术规格",
                "决策文档", "结构化内容", "高效转移上下文", "通过迭代完善内容",
                "验证文档对读者的适用性"
            ],
            "internal-comms": [
                "写报告", "创建状态更新", "起草通信", "写通讯", "创建更新",
                "起草内部文档", "写项目更新", "创建领导更新", "起草公司通信",
                "写团队更新", "创建进度报告", "起草内部备忘录",
                "创建项目报告", "起草项目状态", "写团队通信",
                "创建项目摘要", "起草团队更新", "写部门报告",
                "编写各种内部通信", "状态报告", "领导更新", "3P更新", "公司通讯",
                "常见问题", "事件报告", "项目更新", "等"
            ],
            "mathematical-statistics": [
                "统计分析", "数据分析", "研究统计", "分析数据", "执行统计检验",
                "计算指标", "分析调查", "研究方法论", "统计建模", "数据分析解释",
                "研究分析", "统计报告", "分析研究数据", "执行统计分析", "数据建模",
                "分析项目数据", "执行统计测试", "创建统计模型",
                "分析调查结果", "计算统计指标", "解释统计数据",
                "社会科学研究", "描述性统计", "推断统计", "回归分析", "方差分析",
                "因子分析", "完整统计支持"
            ],
            "field-analysis": [
                "场域分析", "社会学分析", "研究场域", "分析社会场域", "研究社会动态",
                "分析权力关系", "研究社会结构", "分析资本分布", "研究社会背景",
                "分析社会现象", "场域研究",
                "分析研究场域", "研究场域动态", "分析场域结构",
                "研究社会场域", "研究场域关系", "分析场域特征",
                "执行场域分析", "场域边界识别", "资本分布分析", "自主性评估",
                "习性模式分析", "分析社会场域结构", "权力关系", "文化资本"
            ],
            "ant": [
                "行动者网络理论", "分析网络", "研究行动者网络", "分析关系", "研究网络动态",
                "分析连接", "研究网络理论", "研究行动者关系", "网络分析", "分析异质网络",
                "研究转译过程", "网络研究",
                "分析研究网络", "研究行动者互动", "分析网络关系",
                "执行行动者网络理论分析", "参与者识别", "关系网络构建", "转译过程追踪",
                "网络动态分析", "分析异质行动者网络", "追踪事实构建过程", "分析技术社会互动"
            ],
            "network-computation": [
                "网络分析", "分析关系", "计算网络指标", "分析社会网络", "研究网络结构",
                "计算中心性", "分析网络数据", "计算网络属性", "网络可视化", "研究网络动态",
                "分析连接", "网络建模",
                "分析研究网络", "计算网络指标", "研究网络模式",
                "社会网络计算分析", "网络构建", "中心性测量", "社区检测", "网络可视化",
                "完整网络分析支持"
            ],
            "conflict-resolution": [
                "解决冲突", "管理分歧", "解决分歧", "处理冲突", "管理争议", "解决学术分歧",
                "处理研究冲突", "解决学术分歧", "管理学术辩论", "解决研究分歧", "处理学术分歧",
                "解决学术冲突",
                "解决项目分歧", "管理团队冲突", "解决研究争议",
                "冲突解决工具", "研究分歧", "理论", "方法论", "解释", "价值观",
                "建设性对话", "共识建立策略"
            ],
            "validity-reliability": [
                "测试效度", "分析信度", "研究效度", "检查研究效度", "分析研究信度", "测试信度",
                "验证研究", "检查效度", "分析内部一致性", "测试研究效度", "分析信度效度", "研究质量评估",
                "验证研究方法", "检查研究效度", "分析研究质量",
                "研究信度分析", "内部一致性", "重测信度", "评分者信度", "构念效度",
                "内容效度", "效标效度", "全面分析"
            ],
            "mcp-builder": [
                "创建高质量MCP服务器", "模型上下文协议", "与外部服务交互", "设计良好的工具",
                "构建MCP服务器", "集成外部API", "服务", "Python FastMCP", "Node/TypeScript MCP SDK",
                "创建MCP（模型上下文协议）服务器", "使LLM与外部服务交互", "设计良好的工具",
                "构建MCP服务器以集成外部API或服务"
            ],
            "skill-creator": [
                "创建有效技能", "创建新技能", "更新现有技能", "扩展Claude能力", "专业知识",
                "工作流", "工具集成", "创建有效技能", "创建新技能或更新现有技能",
                "用专业知识扩展Claude能力", "工作流或工具集成"
            ],
            "theme-factory": [
                "用主题样式化工件", "幻灯片", "文档", "报告", "HTML登录页面", "10种预设主题",
                "颜色/字体", "应用于任何工件", "动态生成新主题", "用主题样式化工件",
                "10种预设主题与颜色/字体", "应用于任何已创建的工件", "动态生成新主题"
            ],
            "web-artifacts-builder": [
                "创建复杂的多组件claude.ai HTML工件", "现代前端网页技术", "React", "Tailwind CSS",
                "shadcn/ui", "需要状态管理的复杂工件", "路由", "shadcn/ui组件", "不适用于简单单文件HTML/JSX工件",
                "创建复杂多组件claude.ai HTML工件套件", "使用现代前端网页技术", "React", "Tailwind CSS",
                "shadcn/ui", "需要状态管理的复杂工件", "路由", "shadcn/ui组件", "不适用于简单单文件HTML/JSX工件"
            ],
            "slack-gif-creator": [
                "创建针对Slack优化的动画GIF", "约束", "验证工具", "动画概念",
                "为Slack创建动画GIF", "为Slack创建X做Y的GIF", "为Slack创建动画GIF的知识和工具",
                "提供约束", "验证工具", "动画概念", "当用户要求为Slack创建动画GIF时使用"
            ],
            "canvas-design": [
                "在.png和.pdf文档中创建精美视觉艺术", "设计哲学", "创建海报", "艺术作品", "设计",
                "其他静态作品", "创建原始视觉设计", "不复制现有艺术家作品", "避免版权侵犯",
                "创建精美视觉艺术", "使用设计哲学", "当用户要求创建海报", "艺术作品", "设计",
                "或其它静态作品时", "创建原始视觉设计", "不复制现有艺术家作品以避免版权侵犯"
            ],
            "brand-guidelines": [
                "应用Anthropic官方品牌颜色和排版", "任何类型的工件", "具有Anthropic外观",
                "品牌颜色", "样式指南", "视觉格式化", "公司设计标准", "应用Anthropic官方品牌颜色",
                "排版到任何类型的工件", "受益于具有Anthropic外观", "当品牌颜色或样式指南",
                "视觉格式化", "或公司设计标准适用时"
            ],
            "alienation-analysis": [
                "执行异化分析", "社会科学研究", "分析异化", "研究异化", "研究异化",
                "异化社会学分析", "异化心理学分析"
            ]
        }
        
        chinese_descriptions = chinese_skill_descriptions.get(skill_name, ["使用技能"])
        
        for desc in chinese_descriptions:
            intents.append({
                "intent": f"用{skill_name}来{desc}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"帮我{desc}，使用{skill_name}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"{skill_name}可以{desc}吗？",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"我想{desc}，应该用{skill_name}吗？",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"帮我用{skill_name}{desc}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"使用{skill_name}来{desc}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"{skill_name} {desc}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
            intents.append({
                "intent": f"请帮我{desc}，用{skill_name}",
                "cli_tool": "stigmergy",
                "skill": skill_name,
                "parameters": f"skill {skill_name}"
            })
        
        return intents
    
    def train_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """训练模型"""
        print("开始训练模型...")
        
        # 准备特征
        X = df['user_intent']
        
        # 准备标签
        y_cli = df['cli_tool']
        y_skill = df['skill_used'].fillna('')
        y_params = df['parameters'].fillna('')
        
        # 向量化文本
        X_vectorized = self.vectorizer.fit_transform(X)
        
        # 分割训练/测试数据
        X_train, X_test, y_cli_train, y_cli_test = train_test_split(
            X_vectorized, y_cli, test_size=0.2, random_state=42
        )
        
        # 训练CLI工具分类器
        self.classifier.fit(X_train, np.column_stack([y_cli_train]))
        
        # 评估模型
        y_pred = self.classifier.predict(X_test)
        cli_pred = y_pred[:, 0] if y_pred.ndim > 1 else y_pred
        
        accuracy = accuracy_score(y_cli_test, cli_pred)
        print(f"模型准确率: {accuracy:.2f}")
        
        # 生成分类报告
        print("\n分类报告:")
        print(classification_report(y_cli_test, cli_pred))
        
        return {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'accuracy': accuracy,
            'feature_names': self.vectorizer.get_feature_names_out()
        }
    
    def save_model(self, model_data: Dict[str, Any], model_path: str):
        """保存训练好的模型"""
        model_dir = Path(model_path).parent
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存模型组件
        joblib.dump(model_data['vectorizer'], f"{model_path}_vectorizer.pkl")
        joblib.dump(model_data['classifier'], f"{model_path}_classifier.pkl")
        
        # 保存模型元数据
        metadata = {
            'accuracy': model_data['accuracy'],
            'feature_count': len(model_data['feature_names']),
            'training_date': __import__('datetime').datetime.now().isoformat()
        }
        
        with open(f"{model_path}_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"模型已保存到: {model_path}")


def main():
    trainer = CLIIntentModelTrainer()
    
    # 创建训练数据
    print("创建训练数据...")
    df = trainer.create_training_data()
    print(f"创建了 {len(df)} 个训练样本")
    
    if len(df) > 0:
        # 训练模型
        model_data = trainer.train_model(df)
        
        # 保存模型
        trainer.save_model(model_data, "cli-intent-matcher/data/models/intent_classifier")
    else:
        print("没有足够的数据来训练模型")


if __name__ == "__main__":
    main()