#!/usr/bin/env python
"""
网络数据验证工具
验证网络数据的完整性和有效性
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Set
from collections import defaultdict

def validate_edgelist(edges: List[Dict]) -> Dict:
    """验证边列表"""
    issues = []
    warnings = []
    
    # 检查必需字段
    required_fields = ['source', 'target']
    for i, edge in enumerate(edges):
        for field in required_fields:
            if field not in edge or not edge[field]:
                issues.append(f"边{i+1}: 缺少{field}字段")
    
    # 检查权重有效性
    for i, edge in enumerate(edges):
        weight = edge.get('weight')
        if weight is not None:
            try:
                weight_val = float(weight)
                if weight_val < 0 or weight_val > 1:
                    warnings.append(f"边{i+1}: 权重{weight_val}超出[0,1]范围")
            except (ValueError, TypeError):
                issues.append(f"边{i+1}: 权重必须是数值")
    
    # 检查自环
    self_loops = []
    for i, edge in enumerate(edges):
        if edge.get('source') == edge.get('target'):
            self_loops.append(i+1)
    
    if self_loops:
        warnings.append(f"发现{len(self_loops)}个自环边: {self_loops}")
    
    # 检查重复边
    edge_pairs = []
    duplicates = []
    for i, edge in enumerate(edges):
        pair = tuple(sorted([edge.get('source', ''), edge.get('target', '')]))
        if pair in edge_pairs:
            duplicates.append(i+1)
        else:
            edge_pairs.append(pair)
    
    if duplicates:
        warnings.append(f"发现{len(duplicates)}个重复边: {duplicates}")
    
    return {
        'issues': issues,
        'warnings': warnings,
        'n_edges': len(edges),
        'n_self_loops': len(self_loops),
        'n_duplicates': len(duplicates)
    }

def validate_node_attributes(attributes: Dict) -> Dict:
    """验证节点属性"""
    issues = []
    warnings = []
    
    # 检查节点是否为空
    empty_nodes = [node for node in attributes if not node]
    if empty_nodes:
        issues.append(f"发现{len(empty_nodes)}个空节点名")
    
    # 检查数值字段
    numeric_fields = ['age', 'publications', 'h_index', 'grant_amount']
    for node, attrs in attributes.items():
        if node:  # 跳过空节点
            for field in numeric_fields:
                value = attrs.get(field)
                if value is not None:
                    try:
                        val = float(value)
                        # 检查合理性
                        if field == 'age' and (val < 18 or val > 100):
                            warnings.append(f"节点{node}: 年龄{val}可能不合理")
                        elif field == 'publications' and val < 0:
                            issues.append(f"节点{node}: 论文数不能为负")
                        elif field == 'h_index' and val < 0:
                            issues.append(f"节点{node}: H指数不能为负")
                    except (ValueError, TypeError):
                        issues.append(f"节点{node}: {field}必须是数值")
    
    # 检查分类字段
    categorical_fields = ['gender', 'department', 'position']
    valid_values = {
        'gender': ['男', '女', '其他', ''],
        'department': ['', '计算机科学', '软件工程', '人工智能', '数据科学'],
        'position': ['', '教授', '副教授', '讲师', '研究员', '博士生', '硕士生', '博士后']
    }
    
    for node, attrs in attributes.items():
        if node:
            for field in categorical_fields:
                value = attrs.get(field, '')
                if value and value not in valid_values.get(field, []):
                    warnings.append(f"节点{node}: {field}值'{value}'不在常见选项中")
    
    return {
        'issues': issues,
        'warnings': warnings,
        'n_nodes': len(attributes),
        'n_empty_nodes': len(empty_nodes)
    }

def validate_network_consistency(edges: List[Dict], attributes: Dict) -> Dict:
    """验证网络一致性"""
    issues = []
    warnings = []
    
    # 获取边中的所有节点
    edge_nodes = set()
    for edge in edges:
        edge_nodes.add(edge.get('source', ''))
        edge_nodes.add(edge.get('target', ''))
    
    # 获取属性中的所有节点
    attr_nodes = set(attributes.keys())
    
    # 检查边中有但属性中没有的节点
    missing_attrs = edge_nodes - attr_nodes
    if missing_attrs:
        warnings.append(f"边中存在但属性中缺失的节点: {list(missing_attrs)}")
    
    # 检查属性中有但边中没有的节点（孤立节点）
    isolated_nodes = attr_nodes - edge_nodes
    if isolated_nodes:
        warnings.append(f"属性中存在但边中缺失的节点（孤立节点）: {list(isolated_nodes)}")
    
    # 检查连通性（简化版）
    if len(edge_nodes) > 1:
        # 构建邻接表
        adjacency = defaultdict(set)
        for edge in edges:
            source = edge.get('source', '')
            target = edge.get('target', '')
            if source and target:
                adjacency[source].add(target)
                adjacency[target].add(source)
        
        # 简单的连通性检查
        visited = set()
        to_visit = [next(iter(edge_nodes))] if edge_nodes else []
        
        while to_visit:
            node = to_visit.pop()
            if node not in visited:
                visited.add(node)
                to_visit.extend(adjacency[node] - visited)
        
        if len(visited) < len(edge_nodes):
            warnings.append(f"网络不连通，{len(edge_nodes)-len(visited)}个节点无法到达")
    
    return {
        'issues': issues,
        'warnings': warnings,
        'n_edge_nodes': len(edge_nodes),
        'n_attr_nodes': len(attr_nodes),
        'n_missing_attrs': len(missing_attrs),
        'n_isolated': len(isolated_nodes)
    }

def calculate_validation_score(validation_results: Dict) -> float:
    """计算验证得分"""
    total_issues = 0
    total_warnings = 0
    
    # 统计问题和警告
    for category in ['edgelist', 'node_attributes', 'network_consistency']:
        if category in validation_results:
            total_issues += len(validation_results[category].get('issues', []))
            total_warnings += len(validation_results[category].get('warnings', []))
    
    # 计算得分（100分制）
    # 每个问题扣10分，每个警告扣2分
    score = 100 - (total_issues * 10) - (total_warnings * 2)
    return max(0, score)

def generate_validation_recommendations(validation_results: Dict) -> List[str]:
    """生成验证建议"""
    recommendations = []
    
    # 基于问题类型生成建议
    for category, result in validation_results.items():
        issues = result.get('issues', [])
        warnings = result.get('warnings', [])
        
        if category == 'edgelist':
            if '缺少' in str(issues):
                recommendations.append("补充缺失的边字段信息")
            if '权重' in str(issues):
                recommendations.append("检查并修正权重值，确保在[0,1]范围内")
            if '重复' in str(warnings):
                recommendations.append("考虑合并重复边或保留最终权重")
        
        elif category == 'node_attributes':
            if '数值' in str(issues):
                recommendations.append("检查并修正数值字段的格式")
            if '年龄' in str(warnings):
                recommendations.append("核实年龄数据的准确性")
            if '孤立' in str(warnings):
                recommendations.append("检查是否需要包含孤立节点")
        
        elif category == 'network_consistency':
            if '缺失' in str(warnings):
                recommendations.append("为边中存在的节点补充属性信息")
            if '不连通' in str(warnings):
                recommendations.append("考虑网络是否应该是连通的")
    
    if not recommendations:
        recommendations.append("数据质量良好，无明显问题")
    
    return recommendations

def main():
    parser = argparse.ArgumentParser(
        description='网络数据验证工具',
        epilog='示例：python validate_network_data.py --input network.json --output validation.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入网络数据文件（JSON）')
    parser.add_argument('--output', '-o', default='validation_report.json', help='输出文件')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 提取网络数据
    details = data.get('details', {})
    edges = details.get('edges', [])
    attributes = details.get('node_attributes', {})
    
    if not edges and not attributes:
        print("错误：未找到网络数据", file=sys.stderr)
        sys.exit(1)
    
    # 执行验证
    validation_results = {}
    
    # 验证边列表
    if edges:
        validation_results['edgelist'] = validate_edgelist(edges)
    
    # 验证节点属性
    if attributes:
        validation_results['node_attributes'] = validate_node_attributes(attributes)
    
    # 验证网络一致性
    if edges and attributes:
        validation_results['network_consistency'] = validate_network_consistency(edges, attributes)
    
    # 计算验证得分
    validation_score = calculate_validation_score(validation_results)
    
    # 生成建议
    recommendations = generate_validation_recommendations(validation_results)
    
    end_time = datetime.now()
    
    # 统计检查项
    n_checks = sum(1 for result in validation_results.values() if result)
    
    # 准备输出
    output = {
        'summary': {
            'is_valid': validation_score >= 80,  # 80分以上认为有效
            'validation_score': round(validation_score, 2),
            'n_checks': n_checks,
            'n_issues': sum(len(r.get('issues', [])) for r in validation_results.values()),
            'n_warnings': sum(len(r.get('warnings', [])) for r in validation_results.values()),
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'validation_results': validation_results,
            'recommendations': recommendations
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
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 网络数据验证完成")
        print(f"  - 有效性：{'是' if output['summary']['is_valid'] else '否'}")
        print(f"  - 验证得分：{validation_score:.2f}")
        print(f"  - 问题数：{output['summary']['n_issues']}")
        print(f"  - 警告数：{output['summary']['n_warnings']}")
        print(f"  - 输出文件：{args.output}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()