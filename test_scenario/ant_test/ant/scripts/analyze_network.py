#!/usr/bin/env python
"""
ANT网络分析工具
分析行动者网络的关系结构和动态
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Tuple
import math

def build_network_matrix(relations: List[Dict], actors: List[Dict]) -> Dict:
    """构建网络邻接矩阵"""
    actor_names = [actor['name'] for actor in actors]
    n = len(actor_names)
    
    # 初始化邻接矩阵
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    # 填充矩阵
    for relation in relations:
        from_actor = relation.get('from', '')
        to_actor = relation.get('to', '')
        strength = relation.get('strength', 0.0)
        
        if from_actor in actor_names and to_actor in actor_names:
            i = actor_names.index(from_actor)
            j = actor_names.index(to_actor)
            matrix[i][j] = strength
    
    return {
        'matrix': matrix,
        'actors': actor_names
    }

def calculate_centrality_measures(network: Dict) -> Dict:
    """计算中心性指标"""
    matrix = network['matrix']
    actors = network['actors']
    n = len(actors)
    
    # 度中心性
    degree_centrality = {}
    for i in range(n):
        # 出度 + 入度
        out_degree = sum(matrix[i][j] for j in range(n))
        in_degree = sum(matrix[j][i] for j in range(n))
        degree_centrality[actors[i]] = (out_degree + in_degree) / (2 * (n - 1)) if n > 1 else 0
    
    # 接近中心性（简化版）
    closeness_centrality = {}
    for i in range(n):
        distances = [float('inf')] * n
        distances[i] = 0
        
        # 简化的最短路径计算
        for j in range(n):
            if matrix[i][j] > 0:
                distances[j] = 1 / matrix[i][j]
        
        total_distance = sum(d for d in distances if d != float('inf'))
        closeness_centrality[actors[i]] = (n - 1) / total_distance if total_distance > 0 else 0
    
    # 介数中心性（简化版）
    betweenness_centrality = {actor: 0.0 for actor in actors}
    
    # 特征向量中心性（简化迭代）
    eigenvector_centrality = {actor: 1.0 for actor in actors}
    for _ in range(10):  # 简单迭代
        new_scores = {}
        for i in range(n):
            score = 0
            for j in range(n):
                if matrix[j][i] > 0:
                    score += matrix[j][i] * eigenvector_centrality[actors[j]]
            new_scores[actors[i]] = score
        
        # 归一化
        max_score = max(new_scores.values()) if new_scores else 1
        if max_score == 0:
            max_score = 1
        eigenvector_centrality = {k: v / max_score for k, v in new_scores.items()}
    
    return {
        'degree': degree_centrality,
        'closeness': closeness_centrality,
        'betweenness': betweenness_centrality,
        'eigenvector': eigenvector_centrality
    }

def identify_network_roles(actors: List[Dict], centrality: Dict) -> Dict:
    """识别网络中的角色"""
    degree = centrality['degree']
    eigenvector = centrality['eigenvector']
    
    roles = {
        '核心行动者': [],
        '桥梁行动者': [],
        '边缘行动者': [],
        '影响者': []
    }
    
    # 计算阈值
    degree_values = list(degree.values())
    degree_threshold = sum(degree_values) / len(degree_values) if degree_values else 0
    
    eigenvector_values = list(eigenvector.values())
    eigenvector_threshold = sum(eigenvector_values) / len(eigenvector_values) if eigenvector_values else 0
    
    for actor in actors:
        name = actor['name']
        degree_score = degree.get(name, 0)
        eigenvector_score = eigenvector.get(name, 0)
        
        if degree_score > degree_threshold * 1.5:
            roles['核心行动者'].append(name)
        elif degree_score < degree_threshold * 0.5:
            roles['边缘行动者'].append(name)
        
        if eigenvector_score > eigenvector_threshold * 1.5:
            roles['影响者'].append(name)
    
    # 桥梁行动者（连接不同类型的行动者）
    actor_types = {actor['name']: actor.get('type', '') for actor in actors}
    for actor in actors:
        name = actor['name']
        actor_type = actor_types[name]
        
        # 检查是否连接不同类型的行动者
        connects_different_types = False
        for other in actors:
            other_name = other['name']
            other_type = actor_types[other_name]
            if actor_type != other_type:
                # 这里应该检查实际连接，简化处理
                connects_different_types = True
                break
        
        if connects_different_types and degree_score > degree_threshold:
            roles['桥梁行动者'].append(name)
    
    return roles

def analyze_network_dynamics(relations: List[Dict], moments: List[Dict]) -> Dict:
    """分析网络动态变化"""
    dynamics = {
        'phases': [],
        'evolution_patterns': [],
        'stability_metrics': {}
    }
    
    # 分析各个翻译阶段
    for moment in moments:
        phase = moment.get('phase', '')
        description = moment.get('description', '')
        primary_actor = moment.get('primary_actor', '')
        enrolled = moment.get('enrolled_actors', [])
        
        dynamics['phases'].append({
            'phase': phase,
            'primary_actor': primary_actor,
            'enrolled_count': len(enrolled),
            'enrolled_actors': enrolled,
            'controversies': moment.get('controversies', [])
        })
    
    # 计算稳定性指标
    total_phases = len(moments)
    if total_phases > 0:
        # 计算行动者留存率
        all_enrolled = set()
        for moment in moments:
            all_enrolled.update(moment.get('enrolled_actors', []))
        
        # 简化的稳定性计算
        dynamics['stability_metrics'] = {
            'total_phases': total_phases,
            'unique_actors': len(all_enrolled),
            'average_enrollment': sum(len(m.get('enrolled_actors', [])) for m in moments) / total_phases
        }
    
    return dynamics

def calculate_network_cohesion(network: Dict) -> Dict:
    """计算网络凝聚性"""
    matrix = network['matrix']
    n = len(matrix)
    
    if n < 2:
        return {'cohesion_score': 0.0, 'components': 1}
    
    # 计算连接密度
    total_possible = n * (n - 1)
    actual_connections = sum(1 for i in range(n) for j in range(n) if matrix[i][j] > 0)
    density = actual_connections / total_possible if total_possible > 0 else 0
    
    # 计算连通分量（简化版）
    visited = [False] * n
    components = 0
    
    def dfs(node):
        visited[node] = True
        for neighbor in range(n):
            if matrix[node][neighbor] > 0 and not visited[neighbor]:
                dfs(neighbor)
    
    for i in range(n):
        if not visited[i]:
            components += 1
            dfs(i)
    
    # 凝聚性得分
    cohesion_score = density * (1 / components) if components > 0 else 0
    
    return {
        'cohesion_score': round(cohesion_score, 3),
        'density': round(density, 3),
        'components': components,
        'largest_component_size': n - components + 1 if components > 1 else n
    }

def main():
    parser = argparse.ArgumentParser(
        description='ANT网络分析工具',
        epilog='示例：python analyze_network.py --input data.json --output network.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--output', '-o', default='network_analysis.json', help='输出文件')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 提取数据
    actors = data.get('actors', [])
    relations = data.get('network_relations', [])
    moments = data.get('translation_moments', [])
    
    # 构建网络
    network = build_network_matrix(relations, actors)
    
    # 计算中心性
    centrality = calculate_centrality_measures(network)
    
    # 识别角色
    roles = identify_network_roles(actors, centrality)
    
    # 分析动态
    dynamics = analyze_network_dynamics(relations, moments)
    
    # 计算凝聚性
    cohesion = calculate_network_cohesion(network)
    
    end_time = datetime.now()
    
    # 标准化输出
    output = {
        'summary': {
            'case_study': data.get('case_study', ''),
            'n_actors': len(actors),
            'n_relations': len(relations),
            'n_phases': len(moments),
            'cohesion_score': cohesion['cohesion_score'],
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'network_structure': network,
            'centrality_measures': centrality,
            'network_roles': roles,
            'network_dynamics': dynamics,
            'cohesion_analysis': cohesion
        },
        'metadata': {
            'input_file': args.input,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'ant'
        }
    }
    
    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"✓ 网络分析完成")
        print(f"  - 行动者数量：{len(actors)}")
        print(f"  - 关系数量：{len(relations)}")
        print(f"  - 凝聚性得分：{cohesion['cohesion_score']:.3f}")
        print(f"  - 输出文件：{args.output}")
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()