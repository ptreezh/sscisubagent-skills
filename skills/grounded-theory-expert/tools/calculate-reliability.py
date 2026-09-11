"""
编码者间信度计算工具
计算 Cohen's Kappa 系数
"""

from typing import List, Dict, Tuple
from collections import defaultdict
import math


def calculate_cohens_kappa(coding_1: List[str], coding_2: List[str]) -> Dict:
    """
    计算 Cohen's Kappa 系数
    
    参数:
        coding_1: 编码者 1 的编码列表
        coding_2: 编码者 2 的编码列表
    
    返回:
        Kappa 系数和统计信息
    """
    if len(coding_1) != len(coding_2):
        raise ValueError("两个编码列表长度必须相同")
    
    n = len(coding_1)
    if n == 0:
        return {
            'cohens_kappa': 0,
            'agreement_rate': 0,
            'status': 'error',
            'message': '编码列表为空'
        }
    
    # 计算观察一致性 (Po)
    agreements = sum(1 for c1, c2 in zip(coding_1, coding_2) if c1 == c2)
    po = agreements / n
    
    # 计算期望一致性 (Pe)
    # 统计每个编码的频次
    codes = set(coding_1 + coding_2)
    
    freq_1 = defaultdict(int)
    freq_2 = defaultdict(int)
    
    for code in coding_1:
        freq_1[code] += 1
    for code in coding_2:
        freq_2[code] += 1
    
    # 计算 Pe
    pe = sum((freq_1[code] / n) * (freq_2[code] / n) for code in codes)
    
    # 计算 Kappa
    if pe == 1:
        kappa = 0
    else:
        kappa = (po - pe) / (1 - pe)
    
    # 解释 Kappa 值
    if kappa >= 0.8:
        interpretation = 'excellent'
        status = 'acceptable'
    elif kappa >= 0.7:
        interpretation = 'good'
        status = 'acceptable'
    elif kappa >= 0.6:
        interpretation = 'moderate'
        status = 'acceptable'
    elif kappa >= 0.4:
        interpretation = 'fair'
        status = 'needs_improvement'
    else:
        interpretation = 'poor'
        status = 'unacceptable'
    
    return {
        'cohens_kappa': round(kappa, 3),
        'agreement_rate': round(po, 3),
        'expected_agreement': round(pe, 3),
        'total_codes': n,
        'agreements': agreements,
        'disagreements': n - agreements,
        'interpretation': interpretation,
        'status': status,
        'threshold': 0.7
    }


def calculate_percent_agreement(coding_1: List[str], coding_2: List[str]) -> float:
    """
    计算简单一致性百分比
    
    参数:
        coding_1: 编码者 1 的编码列表
        coding_2: 编码者 2 的编码列表
    
    返回:
        一致性百分比
    """
    if len(coding_1) != len(coding_2):
        raise ValueError("两个编码列表长度必须相同")
    
    agreements = sum(1 for c1, c2 in zip(coding_1, coding_2) if c1 == c2)
    return agreements / len(coding_1) if coding_1 else 0


def identify_disagreements(coding_1: List[str], coding_2: List[str]) -> List[Dict]:
    """
    识别分歧点
    
    参数:
        coding_1: 编码者 1 的编码列表
        coding_2: 编码者 2 的编码列表
    
    返回:
        分歧点列表
    """
    disagreements = []
    
    for i, (c1, c2) in enumerate(zip(coding_1, coding_2)):
        if c1 != c2:
            disagreements.append({
                'index': i,
                'coding_1': c1,
                'coding_2': c2
            })
    
    return disagreements


def calculate_reliability(codings: List[List[str]]) -> Dict:
    """
    计算多个编码者间的信度
    
    参数:
        codings: 编码者编码列表的列表
    
    返回:
        信度分析结果
    """
    if len(codings) < 2:
        return {
            'status': 'error',
            'message': '至少需要 2 个编码者'
        }
    
    # 计算所有编码者对的 Kappa
    kappa_pairs = []
    
    for i in range(len(codings)):
        for j in range(i + 1, len(codings)):
            kappa_result = calculate_cohens_kappa(codings[i], codings[j])
            kappa_pairs.append({
                'coder_1': i + 1,
                'coder_2': j + 1,
                'kappa': kappa_result['cohens_kappa'],
                'agreement_rate': kappa_result['agreement_rate']
            })
    
    # 平均 Kappa
    avg_kappa = sum(p['kappa'] for p in kappa_pairs) / len(kappa_pairs) if kappa_pairs else 0
    
    return {
        'average_kappa': round(avg_kappa, 3),
        'pairs': kappa_pairs,
        'num_coders': len(codings),
        'status': 'acceptable' if avg_kappa >= 0.7 else 'needs_improvement'
    }


if __name__ == '__main__':
    # 测试
    coding_1 = ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B']
    coding_2 = ['A', 'B', 'A', 'C', 'A', 'A', 'C', 'B']
    
    result = calculate_cohens_kappa(coding_1, coding_2)
    print(f"Cohen's Kappa: {result['cohens_kappa']}")
    print(f"一致性：{result['agreement_rate']}")
    print(f"解释：{result['interpretation']}")
    print(f"状态：{result['status']}")
    
    # 识别分歧
    disagreements = identify_disagreements(coding_1, coding_2)
    print(f"\n分歧点：{len(disagreements)}个")
    for d in disagreements:
        print(f"  位置{d['index']}: 编码者 1={d['coding_1']}, 编码者 2={d['coding_2']}")
