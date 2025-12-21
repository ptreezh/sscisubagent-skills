# 依赖管理配置文件

# 定义每个技能的依赖需求
SKILL_DEPENDENCIES = {
    "mathematical-statistics": {
        "advanced": ["statsmodels", "pingouin", "scikit-learn"],
        "fallback": ["numpy", "scipy", "pandas"]  # 基础功能所需
    },
    "validity-reliability": {
        "advanced": ["factor-analyzer", "statsmodels", "pingouin"],
        "fallback": ["numpy", "scipy", "pandas"]
    },
    "network-computation": {
        "advanced": ["networkx", "igraph", "python-louvain"],
        "fallback": ["numpy", "pandas"]  # 我们的基础实现
    },
    "ant-participant-identification": {
        "advanced": ["networkx", "nltk", "spacy"],
        "fallback": ["re", "collections"]  # 使用Python标准库
    },
    "ant-translation-process": {
        "advanced": ["networkx", "nltk", "spacy"],
        "fallback": ["re", "collections"]
    },
    "ant-network-analysis": {
        "advanced": ["networkx", "igraph", "community"],
        "fallback": ["numpy", "pandas"]
    },
    "field-boundary-identification": {
        "advanced": ["pandas", "numpy", "scikit-learn"],
        "fallback": ["pandas", "numpy"]
    },
    "field-capital-analysis": {
        "advanced": ["pandas", "numpy", "scipy", "scikit-learn"],
        "fallback": ["pandas", "numpy", "scipy"]
    },
    "field-habitus-analysis": {
        "advanced": ["pandas", "numpy", "nltk", "jieba"],
        "fallback": ["pandas", "numpy", "re"]
    },
    "performing-open-coding": {
        "advanced": ["jieba", "nltk", "spacy", "sklearn"],
        "fallback": ["re", "collections", "json"]
    },
    "performing-axial-coding": {
        "advanced": ["sklearn", "pandas", "numpy"],
        "fallback": ["pandas", "numpy"]
    },
    "performing-selective-coding": {
        "advanced": ["sklearn", "pandas", "numpy"],
        "fallback": ["pandas", "numpy"]
    },
    "checking-theory-saturation": {
        "advanced": ["sklearn", "pandas", "numpy"],
        "fallback": ["pandas", "numpy"]
    },
    "writing-grounded-theory-memos": {
        "advanced": ["pandas", "nltk", "jieba"],
        "fallback": ["json", "re"]
    },
    "processing-network-data": {
        "advanced": ["networkx", "pandas", "numpy"],
        "fallback": ["pandas", "numpy"]
    },
    "performing-centrality-analysis": {
        "advanced": ["networkx", "igraph", "numpy"],
        "fallback": ["numpy", "pandas"]
    },
    "performing-network-computation": {
        "advanced": ["networkx", "igraph", "community"],
        "fallback": ["numpy", "pandas"]
    }
}

# 安装命令映射
INSTALL_COMMANDS = {
    "statsmodels": "statsmodels",
    "pingouin": "pingouin",
    "scikit-learn": "scikit-learn",
    "factor-analyzer": "factor-analyzer",
    "networkx": "networkx",
    "igraph": "python-igraph",
    "python-louvain": "python-louvain",
    "nltk": "nltk",
    "spacy": "spacy",
    "jieba": "jieba",
    "community": "python-louvain"
}

# 依赖组定义
DEPENDENCY_GROUPS = {
    "statistics": ["statsmodels", "pingouin", "scikit-learn"],
    "network_analysis": ["networkx", "igraph", "python-louvain", "community"],
    "nlp": ["nltk", "spacy", "jieba"],
    "psychometrics": ["factor-analyzer", "statsmodels", "pingouin"]
}