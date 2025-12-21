#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关系建立脚本 - 轴心编码

功能：
- 识别因果关系
- 识别条件关系
- 识别策略关系
- 识别互动关系

使用方式：
  python build_relationships.py --input categories.json --output relationships.json
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import networkx as nx

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# 关系类型
RELATION_TYPES = {
    'CAUSAL': '因果关系',
    'CONDITIONAL': '条件关系',
    'STRATEGY': '策略关系',
    'INTERACTION': '互动关系'
}

def identify_causal_relations(categories: List[Dict]) -> List[Dict]:
    """
    识别因果关系
    
    策略：基于时间序列和逻辑推理
    
    Returns:
        因果关系列表
    """
    relations = []
    
    # 简单启发式：查找"导致"、"引起"、"产生"等关键词
    causal_keywords = ['导致', '引起', '产生', '造成', '带来', '促使']
    
    for i, cat1 in enumerate(categories):
        for j, cat2 in enumerate(categories):
            if i == j:
                continue
            
            # 检查编码定义中是否包含因果关键词
            cat1_codes = cat1.get('codes', [])
            cat2_codes = cat2.get('codes', [])
            
            causal_score = 0
            for code1 in cat1_codes:
                definition1 = code1.get('definition', '')
                for keyword in causal_keywords:
                    if keyword in definition1:
                        causal_score += 1
            
            if causal_score > 0:
                relations.append({
                    'source': cat1['name'],
                    'target': cat2['name'],
                    'type': 'CAUSAL',
                    'strength': min(causal_score / len(cat1_codes), 1.0),
                    'evidence_count': causal_score
                })
    
    return relations

def identify_conditional_relations(categories: List[Dict]) -> List[Dict]:
    """
    识别条件关系
    
    策略：查找"当...时"、"如果...则"模式
    
    Returns:
        条件关系列表
    """
    relations = []
    
    conditional_keywords = ['当', '如果', '假如', '只要', '一旦', '条件']
    
    for i, cat1 in enumerate(categories):
        for j, cat2 in enumerate(categories):
            if i == j:
                continue
            
            cat1_codes = cat1.get('codes', [])
            
            conditional_score = 0
            for code in cat1_codes:
                definition = code.get('definition', '')
                for keyword in conditional_keywords:
                    if keyword in definition:
                        conditional_score += 1
            
            if conditional_score > 0:
                relations.append({
                    'source': cat1['name'],
                    'target': cat2['name'],
                    'type': 'CONDITIONAL',
                    'strength': min(conditional_score / len(cat1_codes), 1.0),
                    'evidence_count': conditional_score
                })
    
    return relations

def identify_strategy_relations(categories: List[Dict]) -> List[Dict]:
    """
    识别策略关系
    
    策略：查找行动导向的概念
    
    Returns:
        策略关系列表
    """
    relations = []
    
    strategy_keywords = ['策略', '方法', '方式', '手段', '措施', '应对']
    
    for category in categories:
        cat_codes = category.get('codes', [])
        
        strategy_score = 0
        for code in cat_codes:
            concept = code.get('concept') or code.get('code', '')
            for keyword in strategy_keywords:
                if keyword in concept:
                    strategy_score += 1
        
        if strategy_score > 0:
            relations.append({
                'category': category['name'],
                'type': 'STRATEGY',
                'strength': min(strategy_score / len(cat_codes), 1.0),
                'evidence_count': strategy_score
            })
    
    return relations

def identify_interaction_relations(categories: List[Dict]) -> List[Dict]:
    """
    识别互动关系
    
    策略：查找相互影响的模式
    
    Returns:
        互动关系列表
    """
    relations = []
    
    interaction_keywords = ['互动', '相互', '交流', '影响', '作用', '反馈']
    
    for i, cat1 in enumerate(categories):
        for j, cat2 in enumerate(categories[i+1:], start=i+1):
            cat1_codes = cat1.get('codes', [])
            cat2_codes = cat2.get('codes', [])
            
            interaction_score = 0
            for code in cat1_codes + cat2_codes:
                definition = code.get('definition', '')
                concept = code.get('concept') or code.get('code', '')
                for keyword in interaction_keywords:
                    if keyword in definition or keyword in concept:
                        interaction_score += 1
            
            if interaction_score > 0:
                relations.append({
                    'source': cat1['name'],
                    'target': cat2['name'],
                    'type': 'INTERACTION',
                    'bidirectional': True,
                    'strength': min(interaction_score / (len(cat1_codes) + len(cat2_codes)), 1.0),
                    'evidence_count': interaction_score
                })
    
    return relations

def build_relationship_network(relations: List[Dict]) -> Dict:
    """
    构建关系网络
    
    Returns:
        网络统计信息
    """
    G = nx.DiGraph()
    
    for rel in relations:
        if 'source' in rel and 'target' in rel:
            G.add_edge(rel['source'], rel['target'], 
                      type=rel['type'], 
                      weight=rel['strength'])
    
    # 计算网络指标
    if len(G.nodes()) > 0:
        density = nx.density(G)
        try:
            avg_degree = sum(dict(G.degree()).values()) / len(G.nodes())
        except:
            avg_degree = 0
    else:
        density = 0
        avg_degree = 0
    
    return {
        'nodes': len(G.nodes()),
        'edges': len(G.edges()),
        'density': round(density, 3),
        'average_degree': round(avg_degree, 2)
    }

def main():
    parser = argparse.ArgumentParser(
        description='关系建立工具 - 轴心编码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python build_relationships.py --input categories.json --output relationships.json
        """
    )
    parser.add_argument('--input', '-i', required=True, help='输入的范畴JSON文件')
    parser.add_argument('--output', '-o', default='relationships.json', help='输出JSON文件')
    args = parser.parse_args()
    
    start_time = time.time()
    
    try:
        # 读取范畴数据
        input_path = Path(args.input)
        if not input_path.exists():
            logging.error(f"文件不存在: {args.input}")
            sys.exit(1)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取范畴列表
        if 'details' in data and 'categories' in data['details']:
            categories = data['details']['categories']
        elif isinstance(data, list):
            categories = data
        else:
            logging.error("无法识别的数据格式")
            sys.exit(2)
        
        if len(categories) < 2:
            logging.error("范畴数量不足（至少需要2个）")
            sys.exit(3)
        
        logging.info(f"✓ 读取范畴: {len(categories)} 个")
        
        # 识别各类关系
        causal_relations = identify_causal_relations(categories)
        conditional_relations = identify_conditional_relations(categories)
        strategy_relations = identify_strategy_relations(categories)
        interaction_relations = identify_interaction_relations(categories)
        
        all_relations = causal_relations + conditional_relations + interaction_relations
        
        # 构建网络
        network_stats = build_relationship_network(all_relations)
        
        processing_time = time.time() - start_time
        
        # 构建输出
        output = {
            'summary': {
                'total_relations': len(all_relations),
                'causal': len(causal_relations),
                'conditional': len(conditional_relations),
                'strategy': len(strategy_relations),
                'interaction': len(interaction_relations),
                'network_density': network_stats['density'],
                'processing_time': round(processing_time, 2)
            },
            'details': {
                'causal_relations': causal_relations,
                'conditional_relations': conditional_relations,
                'strategy_relations': strategy_relations,
                'interaction_relations': interaction_relations,
                'network_statistics': network_stats
            },
            'metadata': {
                'input_file': str(input_path.absolute()),
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            }
        }
        
        # 保存
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        logging.info(f"✅ 关系识别完成")
        logging.info(f"   总关系数: {len(all_relations)}")
        logging.info(f"   因果关系: {len(causal_relations)}")
        logging.info(f"   网络密度: {network_stats['density']}")
        logging.info(f"📄 详细结果: {args.output}")
        
    except Exception as e:
        logging.error(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(99)

if __name__ == "__main__":
    main()
