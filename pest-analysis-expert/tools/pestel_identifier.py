"""
PESTEL分析因素识别工具

功能：
1. 从文本数据中识别PESTEL六维度因素
2. 对因素进行分类和评估
3. 生成交叉影响矩阵

使用方法：
    python pestel_identifier.py --input data.txt --output pestel_factors.json

作者: PEST Analysis Expert v5.0.0
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Factor:
    """PESTEL因素数据结构"""
    id: str
    name: str
    dimension: str  # P, E, S, T, EN, L
    description: str
    evidence: List[str]
    impact: int = 3
    probability: int = 3
    urgency: str = "medium"  # short, medium, long
    score: int = 0
    
    def __post_init__(self):
        self.score = self.impact * self.probability


# 各维度关键词
DIMENSION_KEYWORDS = {
    'P': {  # Political
        'keywords': [
            '政策', '政府', '法规', '政治', '外交', '贸易', '税收',
            '补贴', '监管', '行政', '立法', '选举', '国际关系'
        ],
        'patterns': [
            r'政府(.+)政策',
            r'(.+)监管',
            r'贸易(.+)政策'
        ]
    },
    'E': {  # Economic
        'keywords': [
            '经济', 'GDP', '利率', '汇率', '通胀', '就业', '收入',
            '消费', '投资', '成本', '价格', '增长', '衰退'
        ],
        'patterns': [
            r'经济(.+)增长',
            r'(.+)成本',
            r'通胀率(.+)'
        ]
    },
    'S': {  # Social
        'keywords': [
            '人口', '社会', '文化', '教育', '健康', '生活方式',
            '价值观', '消费习惯', '老龄化', '城镇化', '人口结构'
        ],
        'patterns': [
            r'人口(.+)变化',
            r'(.+)趋势',
            r'社会(.+)现象'
        ]
    },
    'T': {  # Technological
        'keywords': [
            '技术', '创新', '研发', '专利', '数字化', '智能化',
            'AI', '大数据', '云计算', '物联网', '区块链', '5G'
        ],
        'patterns': [
            r'(.+)技术突破',
            r'研发(.+)投入',
            r'(.+)创新'
        ]
    },
    'EN': {  # Environmental
        'keywords': [
            '环境', '气候', '碳', '排放', '环保', '绿色', '可持续',
            '资源', '能源', '污染', '生态', '碳中和'
        ],
        'patterns': [
            r'(.+)排放',
            r'环境(.+)保护',
            r'碳中和(.+)'
        ]
    },
    'L': {  # Legal
        'keywords': [
            '法律', '法规', '合规', '诉讼', '知识产权', '劳动法',
            '消费者保护', '数据安全', '隐私', '监管处罚'
        ],
        'patterns': [
            r'(.+)法规',
            r'(.+)合规',
            r'法律(.+)规定'
        ]
    }
}


def identify_factors(text: str) -> List[Factor]:
    """从文本中识别PESTEL因素"""
    factors = []
    factor_counts = {d: 0 for d in ['P', 'E', 'S', 'T', 'EN', 'L']}
    
    for dimension, config in DIMENSION_KEYWORDS.items():
        for keyword in config['keywords']:
            if keyword in text:
                factor_counts[dimension] += 1
                factor = Factor(
                    id=f"{dimension}{factor_counts[dimension]}",
                    name=keyword,
                    dimension=dimension,
                    description=f"识别到的{dimension}维度因素：{keyword}",
                    evidence=[f"关键词匹配：{keyword}"]
                )
                factors.append(factor)
    
    return factors


def export_factors(factors: List[Factor], output_path: str):
    """导出因素到JSON文件"""
    output = {
        "metadata": {
            "exported_at": datetime.now().isoformat(),
            "total_factors": len(factors),
            "dimensions": {
                d: len([f for f in factors if f.dimension == d])
                for d in ['P', 'E', 'S', 'T', 'EN', 'L']
            }
        },
        "factors": [asdict(f) for f in factors]
    }
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"导出完成：{output_path}")
    print(f"总因素数：{len(factors)}")


def main():
    parser = argparse.ArgumentParser(description='PESTEL因素识别工具')
    parser.add_argument('--input', '-i', required=True, help='输入文本文件路径')
    parser.add_argument('--output', '-o', default='pestel_factors.json', help='输出JSON文件路径')
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()
    
    factors = identify_factors(text)
    export_factors(factors, args.output)


if __name__ == '__main__':
    main()
