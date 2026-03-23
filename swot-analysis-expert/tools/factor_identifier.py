"""
SWOT分析因素识别工具

功能：
1. 从文本数据中识别潜在的优势、劣势、机会、威胁因素
2. 对因素进行分类和初步评分
3. 生成因素清单

使用方法：
    python factor_identifier.py --input data.txt --output factors.json

作者: SWOT Analysis Expert v5.0.0
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Factor:
    """SWOT因素数据结构"""
    id: str
    name: str
    category: str  # S, W, O, T
    description: str
    evidence: List[str]
    impact: int = 3  # 1-5
    probability: int = 3  # 1-5
    score: int = 0
    
    def __post_init__(self):
        self.score = self.impact * self.probability


# 因素识别关键词
FACTOR_KEYWORDS = {
    'S': {  # 优势
        'positive_keywords': [
            '优势', '强项', '领先', '竞争力', '独特', '核心能力',
            '品牌', '专利', '技术领先', '市场份额', '资金充足',
            '人才', '渠道', '资源', '经验', '声誉'
        ],
        'context_patterns': [
            r'我们的?优势[是为](.+)',
            r'核心竞争力[是为](.+)',
            r'领先于(.+)',
            r'(.+)是我们的强项'
        ]
    },
    'W': {  # 劣势
        'negative_keywords': [
            '劣势', '不足', '短板', '落后', '缺乏', '问题',
            '成本高', '效率低', '人才流失', '资金紧张',
            '渠道不足', '品牌弱', '技术落后', '管理问题'
        ],
        'context_patterns': [
            r'我们的?劣势[是为](.+)',
            r'存在(.+)问题',
            r'(.+)不足',
            r'缺乏(.+)'
        ]
    },
    'O': {  # 机会
        'opportunity_keywords': [
            '机会', '机遇', '增长', '扩张', '新兴', '趋势',
            '政策支持', '市场需求', '技术突破', '消费升级',
            '国际化', '数字化转型', '新市场', '新需求'
        ],
        'context_patterns': [
            r'市场机会[是为](.+)',
            r'(.+)是增长点',
            r'政策支持(.+)',
            r'新兴(.+)市场'
        ]
    },
    'T': {  # 威胁
        'threat_keywords': [
            '威胁', '风险', '竞争', '下降', '萎缩', '挑战',
            '新进入者', '替代品', '成本上升', '监管收紧',
            '经济衰退', '技术颠覆', '人才争夺', '价格战'
        ],
        'context_patterns': [
            r'面临(.+)威胁',
            r'(.+)是风险',
            r'竞争(.+)加剧',
            r'(.+)构成挑战'
        ]
    }
}


def identify_factors(text: str) -> List[Factor]:
    """
    从文本中识别SWOT因素
    
    Args:
        text: 输入文本
        
    Returns:
        识别出的因素列表
    """
    factors = []
    factor_counts = {'S': 0, 'W': 0, 'O': 0, 'T': 0}
    
    for category, config in FACTOR_KEYWORDS.items():
        # 基于关键词识别
        for keyword in config['positive_keywords'] if category in ['S', 'O'] else config.get('negative_keywords', config.get('opportunity_keywords', config.get('threat_keywords', []))):
            if keyword in text:
                factor_counts[category] += 1
                factor = Factor(
                    id=f"{category}{factor_counts[category]}",
                    name=keyword,
                    category=category,
                    description=f"识别到的{category}类因素：{keyword}",
                    evidence=[f"关键词匹配：{keyword}"]
                )
                factors.append(factor)
        
        # 基于模式识别
        for pattern in config['context_patterns']:
            matches = re.finditer(pattern, text)
            for match in matches:
                factor_counts[category] += 1
                factor = Factor(
                    id=f"{category}{factor_counts[category]}",
                    name=match.group(1)[:20],  # 截取前20字符作为名称
                    category=category,
                    description=f"从模式匹配识别：{match.group(0)}",
                    evidence=[f"模式匹配：{pattern}"]
                )
                # 避免重复
                if not any(f.name == factor.name and f.category == factor.category for f in factors):
                    factors.append(factor)
    
    return factors


def calculate_weights(factors: List[Factor]) -> Dict[str, float]:
    """
    计算因素权重
    
    Args:
        factors: 因素列表
        
    Returns:
        权重字典
    """
    category_scores = {'S': 0, 'W': 0, 'O': 0, 'T': 0}
    category_counts = {'S': 0, 'W': 0, 'O': 0, 'T': 0}
    
    for factor in factors:
        category_scores[factor.category] += factor.score
        category_counts[factor.category] += 1
    
    total_score = sum(category_scores.values())
    
    weights = {}
    for cat in ['S', 'W', 'O', 'T']:
        if total_score > 0:
            weights[cat] = round(category_scores[cat] / total_score, 2)
        else:
            weights[cat] = 0.25
    
    return weights


def export_factors(factors: List[Factor], output_path: str):
    """
    导出因素到JSON文件
    
    Args:
        factors: 因素列表
        output_path: 输出路径
    """
    output = {
        "metadata": {
            "exported_at": datetime.now().isoformat(),
            "total_factors": len(factors),
            "categories": {
                "S": len([f for f in factors if f.category == 'S']),
                "W": len([f for f in factors if f.category == 'W']),
                "O": len([f for f in factors if f.category == 'O']),
                "T": len([f for f in factors if f.category == 'T'])
            }
        },
        "factors": [asdict(f) for f in factors],
        "weights": calculate_weights(factors)
    }
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"导出完成：{output_path}")
    print(f"总因素数：{len(factors)}")
    print(f"分类统计：S={output['metadata']['categories']['S']}, "
          f"W={output['metadata']['categories']['W']}, "
          f"O={output['metadata']['categories']['O']}, "
          f"T={output['metadata']['categories']['T']}")


def main():
    parser = argparse.ArgumentParser(description='SWOT因素识别工具')
    parser.add_argument('--input', '-i', required=True, help='输入文本文件路径')
    parser.add_argument('--output', '-o', default='factors.json', help='输出JSON文件路径')
    args = parser.parse_args()
    
    # 读取输入
    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 识别因素
    factors = identify_factors(text)
    
    # 导出结果
    export_factors(factors, args.output)


if __name__ == '__main__':
    main()
