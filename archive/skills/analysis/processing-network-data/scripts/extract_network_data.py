#!/usr/bin/env python
"""
网络数据提取工具
从清洗后的调查数据中提取网络关系数据
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Set
from collections import defaultdict

def extract_edgelist(respondents: List[Dict]) -> List[Dict]:
    """提取边列表"""
    edges = []
    edge_set = set()  # 用于去重
    
    for respondent in respondents:
        source = respondent.get('name', '')
        source_id = respondent.get('id', '')
        
        if not source:
            continue
            
        collaborators = respondent.get('collaborators', [])
        
        for collab in collaborators:
            target = collab.get('name', '')
            if not target:
                continue
            
            # 创建边的唯一标识
            edge_id = tuple(sorted([source, target]))
            if edge_id in edge_set:
                continue
            edge_set.add(edge_id)
            
            # 计算权重（基于合作频率）
            frequency = collab.get('frequency', '')
            weight_map = {
                '每天': 1.0,
                '每周': 0.8,
                '每月': 0.6,
                '每季度': 0.4,
                '每年': 0.2,
                '偶尔': 0.3
            }
            weight = weight_map.get(frequency, 0.5)
            
            edge = {
                'source': source,
                'target': target,
                'weight': weight,
                'type': collab.get('type', ''),
                'frequency': frequency,
                'source_id': source_id
            }
            edges.append(edge)
    
    return edges

def extract_adjacency_matrix(respondents: List[Dict]) -> Dict:
    """提取邻接矩阵"""
    # 获取所有节点
    nodes = set()
    for respondent in respondents:
        nodes.add(respondent.get('name', ''))
        for collab in respondent.get('collaborators', []):
            nodes.add(collab.get('name', ''))
    nodes = [n for n in nodes if n]  # 移除空值
    
    # 创建节点映射
    node_to_index = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)
    
    # 初始化矩阵
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    # 填充矩阵
    for respondent in respondents:
        source = respondent.get('name', '')
        if not source or source not in node_to_index:
            continue
            
        source_idx = node_to_index[source]
        
        for collab in respondent.get('collaborators', []):
            target = collab.get('name', '')
            if not target or target not in node_to_index:
                continue
                
            target_idx = node_to_index[target]
            
            # 计算权重
            frequency = collab.get('frequency', '')
            weight_map = {
                '每天': 1.0,
                '每周': 0.8,
                '每月': 0.6,
                '每季度': 0.4,
                '每年': 0.2,
                '偶尔': 0.3
            }
            weight = weight_map.get(frequency, 0.5)
            
            # 填充矩阵（无向图）
            matrix[source_idx][target_idx] = weight
            matrix[target_idx][source_idx] = weight
    
    return {
        'matrix': matrix,
        'node_labels': nodes,
        'node_to_index': node_to_index,
        'size': n
    }

def extract_node_attributes(respondents: List[Dict]) -> Dict:
    """提取节点属性"""
    attributes = {}
    
    # 添加受访者属性
    for respondent in respondents:
        name = respondent.get('name', '')
        if not name:
            continue
            
        attr = {
            'id': respondent.get('id', ''),
            'department': respondent.get('department', ''),
            'position': respondent.get('position', ''),
            'age': respondent.get('age'),
            'gender': respondent.get('gender', ''),
            'publications': respondent.get('publications'),
            'h_index': respondent.get('h_index'),
            'research_areas': respondent.get('research_areas', []),
            'grant_amount': respondent.get('grant_amount'),
            'is_respondent': True
        }
        attributes[name] = attr
    
    # 添加仅作为合作者出现的节点属性
    respondent_names = set(r.get('name', '') for r in respondents)
    
    for respondent in respondents:
        for collab in respondent.get('collaborators', []):
            name = collab.get('name', '')
            if name and name not in attributes:
                attributes[name] = {
                    'id': '',
                    'department': '',
                    'position': '',
                    'age': None,
                    'gender': '',
                    'publications': None,
                    'h_index': None,
                    'research_areas': [],
                    'grant_amount': None,
                    'is_respondent': False
                }
    
    return attributes

def calculate_network_statistics(edges: List[Dict], nodes: List[str]) -> Dict:
    """计算网络统计信息"""
    n_nodes = len(nodes)
    n_edges = len(edges)
    
    # 计算密度
    max_edges = n_nodes * (n_nodes - 1) / 2
    density = n_edges / max_edges if max_edges > 0 else 0
    
    # 边类型统计
    edge_types = defaultdict(int)
    total_weight = 0
    
    for edge in edges:
        edge_type = edge.get('type', '未知')
        edge_types[edge_type] += 1
        total_weight += edge.get('weight', 0)
    
    # 平均权重
    avg_weight = total_weight / n_edges if n_edges > 0 else 0
    
    return {
        'n_nodes': n_nodes,
        'n_edges': n_edges,
        'density': round(density, 4),
        'avg_weight': round(avg_weight, 3),
        'edge_types': dict(edge_types),
        'total_weight': round(total_weight, 3)
    }

def main():
    parser = argparse.ArgumentParser(
        description='网络数据提取工具',
        epilog='示例：python extract_network_data.py --input cleaned.json --output network.json --format edgelist'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入清洗后的数据文件（JSON）')
    parser.add_argument('--output', '-o', default='network_data.json', help='输出文件')
    parser.add_argument('--format', '-f',
                       choices=['edgelist', 'adjacency', 'both'],
                       default='edgelist',
                       help='输出格式')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 提取受访者数据
    respondents = data.get('details', {}).get('cleaned_data', [])
    if not respondents:
        print("错误：未找到清洗后的受访者数据", file=sys.stderr)
        sys.exit(1)
    
    # 提取网络数据
    result = {}
    
    # 提取边列表
    edges = extract_edgelist(respondents)
    result['edges'] = edges
    
    # 提取节点属性
    node_attributes = extract_node_attributes(respondents)
    result['node_attributes'] = node_attributes
    
    # 提取邻接矩阵（如果需要）
    if args.format in ['adjacency', 'both']:
        adjacency = extract_adjacency_matrix(respondents)
        result['adjacency_matrix'] = adjacency
    
    # 计算统计信息
    nodes = list(node_attributes.keys())
    statistics = calculate_network_statistics(edges, nodes)
    result['statistics'] = statistics
    
    end_time = datetime.now()
    
    # 准备输出
    summary = {
        'n_nodes': statistics['n_nodes'],
        'n_edges': statistics['n_edges'],
        'density': statistics['density'],
        'format': args.format,
        'processing_time': round((end_time - start_time).total_seconds(), 2)
    }
    
    output = {
        'summary': summary,
        'details': result,
        'metadata': {
            'input_file': args.input,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'processing-network-data'
        }
    }
    
    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 网络数据提取完成")
        print(f"  - 节点数：{statistics['n_nodes']}")
        print(f"  - 边数：{statistics['n_edges']}")
        print(f"  - 网络密度：{statistics['density']:.4f}")
        print(f"  - 边类型：{list(statistics['edge_types'].keys())}")
        print(f"  - 输出格式：{args.format}")
        print(f"  - 输出文件：{args.output}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()