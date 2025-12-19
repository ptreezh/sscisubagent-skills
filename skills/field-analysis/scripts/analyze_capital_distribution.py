#!/usr/bin/env python3
"""
资本分布分析工具

功能：
1. 文化资本分析（教育、知识、技能）
2. 社会资本分析（关系网络、社会联系）
3. 象征资本分析（声望、荣誉、认可）
4. 经济资本分析（物质财富）
5. 资本转换关系分析

标准化接口：argparse + 三层JSON输出
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def analyze_cultural_capital(data: List[Dict]) -> Dict:
    """分析文化资本分布"""
    education_levels = []
    skills = []
    cultural_activities = []
    
    for item in data:
        # 教育水平
        edu = item.get('education', '')
        if edu == '博士':
            education_levels.append(5)
        elif edu == '硕士':
            education_levels.append(4)
        elif edu == '本科':
            education_levels.append(3)
        elif edu == '大专':
            education_levels.append(2)
        elif edu == '高中':
            education_levels.append(1)
        else:
            education_levels.append(0)
        
        # 技能数量
        skills.append(len(item.get('skills', [])))
        
        # 文化活动参与度
        cultural_activities.append(len(item.get('cultural_activities', [])))
    
    # 计算文化资本指数
    cultural_capital = []
    for i in range(len(data)):
        # 标准化各维度
        edu_score = education_levels[i] / 5.0
        skill_score = min(skills[i] / 10.0, 1.0)
        activity_score = min(cultural_activities[i] / 5.0, 1.0)
        
        # 加权平均（教育权重最高）
        capital_score = (edu_score * 0.5 + skill_score * 0.3 + activity_score * 0.2)
        cultural_capital.append(round(capital_score, 4))
    
    # 分析分布
    mean_cultural = np.mean(cultural_capital)
    std_cultural = np.std(cultural_capital)
    
    # 识别文化资本层次
    levels = []
    for score in cultural_capital:
        if score >= 0.8:
            levels.append('高')
        elif score >= 0.5:
            levels.append('中')
        else:
            levels.append('低')
    
    return {
        'type': 'cultural',
        'scores': cultural_capital,
        'mean': round(float(mean_cultural), 4),
        'std': round(float(std_cultural), 4),
        'distribution': {
            '高': levels.count('高'),
            '中': levels.count('中'),
            '低': levels.count('低')
        },
        'inequality_gini': round(float(gini_coefficient(cultural_capital)), 4)
    }


def analyze_social_capital(data: List[Dict]) -> Dict:
    """分析社会资本分布"""
    network_sizes = []
    tie_strengths = []
    structural_holes = []
    
    for item in data:
        # 网络规模
        network = item.get('social_network', {})
        network_sizes.append(len(network))
        
        # 关系强度（基于互动频率）
        ties = network.values() if network else []
        if ties:
            tie_strengths.append(np.mean(ties))
        else:
            tie_strengths.append(0)
        
        # 结构洞（简化计算）
        structural_holes.append(item.get('structural_holes', 0))
    
    # 计算社会资本指数
    social_capital = []
    for i in range(len(data)):
        # 标准化
        size_score = min(network_sizes[i] / 50.0, 1.0)
        strength_score = tie_strengths[i] / 10.0 if tie_strengths[i] > 0 else 0
        holes_score = 1 - min(structural_holes[i] / 10.0, 1.0)
        
        # 加权平均
        capital_score = (size_score * 0.4 + strength_score * 0.4 + holes_score * 0.2)
        social_capital.append(round(capital_score, 4))
    
    return {
        'type': 'social',
        'scores': social_capital,
        'mean': round(float(np.mean(social_capital)), 4),
        'std': round(float(np.std(social_capital)), 4),
        'network_stats': {
            'avg_size': round(float(np.mean(network_sizes)), 2),
            'avg_tie_strength': round(float(np.mean(tie_strengths)), 2)
        },
        'inequality_gini': round(float(gini_coefficient(social_capital)), 4)
    }


def analyze_symbolic_capital(data: List[Dict]) -> Dict:
    """分析象征资本分布"""
    prestige_scores = []
    recognitions = []
    honors = []
    
    for item in data:
        # 声望评分
        prestige_scores.append(item.get('prestige_score', 0))
        
        # 获得认可
        recognitions.append(len(item.get('recognitions', [])))
        
        # 荣誉头衔
        honors.append(len(item.get('honors', [])))
    
    # 计算象征资本指数
    symbolic_capital = []
    for i in range(len(data)):
        # 标准化
        prestige_score = min(prestige_scores[i] / 100.0, 1.0)
        recognition_score = min(recognitions[i] / 10.0, 1.0)
        honor_score = min(honors[i] / 5.0, 1.0)
        
        # 加权平均
        capital_score = (prestige_score * 0.5 + recognition_score * 0.3 + honor_score * 0.2)
        symbolic_capital.append(round(capital_score, 4))
    
    return {
        'type': 'symbolic',
        'scores': symbolic_capital,
        'mean': round(float(np.mean(symbolic_capital)), 4),
        'std': round(float(np.std(symbolic_capital)), 4),
        'top_10_percent': round(float(np.percentile(symbolic_capital, 90)), 4),
        'inequality_gini': round(float(gini_coefficient(symbolic_capital)), 4)
    }


def analyze_economic_capital(data: List[Dict]) -> Dict:
    """分析经济资本分布"""
    incomes = []
    assets = []
    investments = []
    
    for item in data:
        incomes.append(item.get('annual_income', 0))
        assets.append(item.get('total_assets', 0))
        investments.append(item.get('investments', 0))
    
    # 计算经济资本指数（对数转换处理）
    economic_capital = []
    for i in range(len(data)):
        # 对数转换处理大数值
        income_score = np.log1p(incomes[i]) / np.log1p(1000000)  # 100万为基准
        asset_score = np.log1p(assets[i]) / np.log1p(10000000)  # 1000万为基准
        investment_score = np.log1p(investments[i]) / np.log1p(1000000)  # 100万为基准
        
        # 加权平均
        capital_score = (income_score * 0.4 + asset_score * 0.4 + investment_score * 0.2)
        economic_capital.append(round(min(capital_score, 1.0), 4))
    
    return {
        'type': 'economic',
        'scores': economic_capital,
        'mean': round(float(np.mean(economic_capital)), 4),
        'std': round(float(np.std(economic_capital)), 4),
        'wealth_stats': {
            'avg_income': round(float(np.mean(incomes)), 0),
            'avg_assets': round(float(np.mean(assets)), 0)
        },
        'inequality_gini': round(float(gini_coefficient(economic_capital)), 4)
    }


def gini_coefficient(values: List[float]) -> float:
    """计算基尼系数"""
    sorted_values = sorted(values)
    n = len(values)
    if n == 0:
        return 0.0
    
    cumsum = np.cumsum(sorted_values)
    sum_values = cumsum[-1]
    if sum_values == 0:
        return 0.0
    
    gini = (n + 1 - 2 * np.sum(cumsum) / sum_values) / n
    return max(0.0, min(1.0, gini))


def analyze_capital_conversion(capitals: Dict) -> Dict:
    """分析资本转换关系"""
    # 计算资本类型间的相关性
    cultural = capitals.get('cultural', {}).get('scores', [])
    social = capitals.get('social', {}).get('scores', [])
    symbolic = capitals.get('symbolic', {}).get('scores', [])
    economic = capitals.get('economic', {}).get('scores', [])
    
    # 确保所有列表长度相同
    min_len = min(len(cultural), len(social), len(symbolic), len(economic))
    if min_len == 0:
        return {'correlations': {}, 'conversions': {}}
    
    cultural = cultural[:min_len]
    social = social[:min_len]
    symbolic = symbolic[:min_len]
    economic = economic[:min_len]
    
    # 计算相关性（简化版本）
    correlations = {}
    
    # 文化资本与其他资本的相关性
    if len(cultural) > 1:
        correlations['cultural-social'] = round(float(np.corrcoef(cultural, social)[0, 1]), 4)
        correlations['cultural-symbolic'] = round(float(np.corrcoef(cultural, symbolic)[0, 1]), 4)
        correlations['cultural-economic'] = round(float(np.corrcoef(cultural, economic)[0, 1]), 4)
    
    # 转换效率分析
    conversions = {}
    conversions['cultural_to_symbolic'] = {
        'correlation': correlations.get('cultural-symbolic', 0),
        'efficiency': 'high' if correlations.get('cultural-symbolic', 0) > 0.5 else 'medium' if correlations.get('cultural-symbolic', 0) > 0.3 else 'low'
    }
    
    return {
        'correlations': correlations,
        'conversions': conversions
    }


def main():
    parser = argparse.ArgumentParser(
        description='资本分布分析工具',
        epilog='示例：python analyze_capital_distribution.py --input data.json --type cultural'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--type', '-t', default='all',
                       choices=['cultural', 'social', 'symbolic', 'economic', 'all'],
                       help='资本类型（默认：all）')
    parser.add_argument('--output', '-o', default='capital_distribution.json', help='输出文件')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict):
            if 'data' in data:
                data = data['data']
            else:
                data = [data]
        elif not isinstance(data, list):
            data = [data]
    
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 分析资本分布
    results = {}
    
    if args.type == 'all' or args.type == 'cultural':
        results['cultural'] = analyze_cultural_capital(data)
    
    if args.type == 'all' or args.type == 'social':
        results['social'] = analyze_social_capital(data)
    
    if args.type == 'all' or args.type == 'symbolic':
        results['symbolic'] = analyze_symbolic_capital(data)
    
    if args.type == 'all' or args.type == 'economic':
        results['economic'] = analyze_economic_capital(data)
    
    # 分析资本转换关系
    if args.type == 'all':
        results['conversion'] = analyze_capital_conversion(results)
    
    end_time = datetime.now()
    
    # 标准化输出
    output = {
        'summary': {
            'n_participants': len(data),
            'capital_types': list(results.keys()),
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'capital_distribution': results
        },
        'metadata': {
            'input_file': args.input,
            'analysis_type': args.type,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'field-analysis'
        }
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 资本分布分析完成")
    print(f"  - 参与者数：{len(data)}")
    print(f"  - 资本类型：{len(results)}")
    print(f"  - 输出文件：{args.output}")


if __name__ == '__main__':
    main()