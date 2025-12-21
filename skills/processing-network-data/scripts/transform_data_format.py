#!/usr/bin/env python
"""
数据格式转换工具
在不同网络数据格式之间进行转换
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

def edgelist_to_adjacency(edges: List[Dict]) -> Dict:
    """将边列表转换为邻接矩阵"""
    # 收集所有节点
    nodes = set()
    for edge in edges:
        nodes.add(edge.get('source', ''))
        nodes.add(edge.get('target', ''))
    nodes = [n for n in nodes if n]  # 移除空值
    
    # 创建节点映射
    node_to_index = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)
    
    # 初始化矩阵
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    # 填充矩阵
    for edge in edges:
        source = edge.get('source', '')
        target = edge.get('target', '')
        weight = edge.get('weight', 1.0)
        
        if source in node_to_index and target in node_to_index:
            i = node_to_index[source]
            j = node_to_index[target]
            
            # 如果有多个边，使用最大权重
            matrix[i][j] = max(matrix[i][j], weight)
            matrix[j][i] = max(matrix[j][i], weight)  # 无向图
    
    return {
        'matrix': matrix,
        'node_labels': nodes,
        'node_to_index': node_to_index,
        'size': n,
        'is_directed': False
    }

def adjacency_to_edgelist(adjacency: Dict) -> List[Dict]:
    """将邻接矩阵转换为边列表"""
    matrix = adjacency.get('matrix', [])
    node_labels = adjacency.get('node_labels', [])
    n = len(matrix)
    
    edges = []
    
    for i in range(n):
        for j in range(i, n):  # 只处理上三角，避免重复
            weight = matrix[i][j]
            if weight > 0:  # 只保留有连接的边
                edge = {
                    'source': node_labels[i],
                    'target': node_labels[j],
                    'weight': weight
                }
                edges.append(edge)
    
    return edges

def edgelist_to_adjlist(edges: List[Dict]) -> Dict:
    """将边列表转换为邻接表"""
    adjlist = {}
    
    for edge in edges:
        source = edge.get('source', '')
        target = edge.get('target', '')
        weight = edge.get('weight', 1.0)
        
        if source not in adjlist:
            adjlist[source] = []
        if target not in adjlist:
            adjlist[target] = []
        
        # 添加到邻接表
        adjlist[source].append({
            'neighbor': target,
            'weight': weight,
            'type': edge.get('type', '')
        })
        
        # 无向图，添加反向连接
        if source != target:
            adjlist[target].append({
                'neighbor': source,
                'weight': weight,
                'type': edge.get('type', '')
            })
    
    return adjlist

def adjlist_to_edgelist(adjlist: Dict) -> List[Dict]:
    """将邻接表转换为边列表"""
    edges = []
    seen_edges = set()  # 用于去重
    
    for source, neighbors in adjlist.items():
        for neighbor_info in neighbors:
            target = neighbor_info.get('neighbor', '')
            weight = neighbor_info.get('weight', 1.0)
            edge_type = neighbor_info.get('type', '')
            
            # 创建边的唯一标识
            edge_id = tuple(sorted([source, target]))
            if edge_id not in seen_edges:
                seen_edges.add(edge_id)
                
                edge = {
                    'source': source,
                    'target': target,
                    'weight': weight,
                    'type': edge_type
                }
                edges.append(edge)
    
    return edges

def save_adjacency_matrix(adjacency: Dict, output_file: str):
    """保存邻接矩阵到文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(adjacency, f, ensure_ascii=False, indent=2)

def save_edgelist(edges: List[Dict], output_file: str):
    """保存边列表到文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(edges, f, ensure_ascii=False, indent=2)

def save_adjlist(adjlist: Dict, output_file: str):
    """保存邻接表到文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(adjlist, f, ensure_ascii=False, indent=2)

def validate_input_format(data: Dict, format_type: str) -> bool:
    """验证输入格式"""
    if format_type == 'edgelist':
        # 检查edges是否在顶层或在details中
        return ('edges' in data and isinstance(data['edges'], list)) or \
               ('details' in data and 'edges' in data['details'] and isinstance(data['details']['edges'], list))
    elif format_type == 'adjacency':
        return ('adjacency_matrix' in data or 'matrix' in data) or \
               ('details' in data and ('adjacency_matrix' in data['details'] or 'matrix' in data['details']))
    elif format_type == 'adjlist':
        return ('adjacency_list' in data and isinstance(data['adjacency_list'], dict)) or \
               ('details' in data and 'adjacency_list' in data['details'] and isinstance(data['details']['adjacency_list'], dict))
    return False

def main():
    parser = argparse.ArgumentParser(
        description='数据格式转换工具',
        epilog='示例：python transform_data_format.py --input network.json --output adj.json --from edgelist --to adjacency'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--output', '-o', required=True, help='输出文件')
    parser.add_argument('--from', '-f', dest='from_format',
                       choices=['edgelist', 'adjacency', 'adjlist'],
                       required=True,
                       help='输入格式')
    parser.add_argument('--to', '-t', dest='to_format',
                       choices=['edgelist', 'adjacency', 'adjlist'],
                       required=True,
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
    
    # 验证输入格式
    if not validate_input_format(data, args.from_format):
        print(f"错误：输入数据格式不符合{args.from_format}要求", file=sys.stderr)
        sys.exit(1)
    
    # 提取数据
    if args.from_format == 'edgelist':
        edges = data.get('edges', []) or data.get('details', {}).get('edges', [])
        if not edges:
            print("错误：未找到边列表数据", file=sys.stderr)
            sys.exit(1)
    elif args.from_format == 'adjacency':
        adjacency = data.get('adjacency_matrix') or data.get('matrix', {}) or \
                   data.get('details', {}).get('adjacency_matrix', {}) or \
                   data.get('details', {}).get('matrix', {})
        if not adjacency:
            print("错误：未找到邻接矩阵数据", file=sys.stderr)
            sys.exit(1)
    elif args.from_format == 'adjlist':
        adjlist = data.get('adjacency_list', {}) or data.get('details', {}).get('adjacency_list', {})
        if not adjlist:
            print("错误：未找到邻接表数据", file=sys.stderr)
            sys.exit(1)
    
    # 执行转换
    result = None
    result_type = None
    
    # 边列表 -> 其他格式
    if args.from_format == 'edgelist':
        if args.to_format == 'adjacency':
            result = edgelist_to_adjacency(edges)
            result_type = 'adjacency_matrix'
        elif args.to_format == 'adjlist':
            result = edgelist_to_adjlist(edges)
            result_type = 'adjacency_list'
        elif args.to_format == 'edgelist':
            result = edges
            result_type = 'edges'
    
    # 邻接矩阵 -> 其他格式
    elif args.from_format == 'adjacency':
        if args.to_format == 'edgelist':
            result = adjacency_to_edgelist(adjacency)
            result_type = 'edges'
        elif args.to_format == 'adjlist':
            edges = adjacency_to_edgelist(adjacency)
            result = edgelist_to_adjlist(edges)
            result_type = 'adjacency_list'
        elif args.to_format == 'adjacency':
            result = adjacency
            result_type = 'adjacency_matrix'
    
    # 邻接表 -> 其他格式
    elif args.from_format == 'adjlist':
        if args.to_format == 'edgelist':
            result = adjlist_to_edgelist(adjlist)
            result_type = 'edges'
        elif args.to_format == 'adjacency':
            edges = adjlist_to_edgelist(adjlist)
            result = edgelist_to_adjacency(edges)
            result_type = 'adjacency_matrix'
        elif args.to_format == 'adjlist':
            result = adjlist
            result_type = 'adjacency_list'
    
    end_time = datetime.now()
    
    # 准备输出
    if result_type == 'adjacency_matrix':
        output_data = {
            'summary': {
                'matrix_size': result.get('size', 0),
                'from_format': args.from_format,
                'to_format': args.to_format,
                'processing_time': round((end_time - start_time).total_seconds(), 2)
            },
            'details': {
                result_type: result
            },
            'metadata': {
                'input_file': args.input,
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'skill': 'processing-network-data'
            }
        }
    elif result_type == 'edges':
        output_data = {
            'summary': {
                'n_edges': len(result),
                'from_format': args.from_format,
                'to_format': args.to_format,
                'processing_time': round((end_time - start_time).total_seconds(), 2)
            },
            'details': {
                result_type: result
            },
            'metadata': {
                'input_file': args.input,
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'skill': 'processing-network-data'
            }
        }
    elif result_type == 'adjacency_list':
        output_data = {
            'summary': {
                'n_nodes': len(result),
                'from_format': args.from_format,
                'to_format': args.to_format,
                'processing_time': round((end_time - start_time).total_seconds(), 2)
            },
            'details': {
                result_type: result
            },
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
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 数据格式转换完成")
        print(f"  - 源格式：{args.from_format}")
        print(f"  - 目标格式：{args.to_format}")
        
        if result_type == 'adjacency_matrix':
            print(f"  - 矩阵大小：{result.get('size', 0)}×{result.get('size', 0)}")
        elif result_type == 'edges':
            print(f"  - 边数：{len(result)}")
        elif result_type == 'adjacency_list':
            print(f"  - 节点数：{len(result)}")
        
        print(f"  - 输出文件：{args.output}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()