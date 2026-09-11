#!/usr/bin/env python3
"""在线社区分析器 - 分析在线社区结构和互动模式"""

import argparse
import json
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any, Tuple

def analyze_community_structure(members: List[Dict], interactions: List[Dict]) -> Dict[str, Any]:
    """
    分析社区结构
    
    Args:
        members: 成员列表
        interactions: 互动列表
        
    Returns:
        社区结构分析结果
    """
    structure = {
        "member_count": len(members),
        "interaction_count": len(interactions),
        "density": 0,
        "clusters": [],
        "roles": {},
        "hierarchy": {}
    }
    
    # 构建互动网络
    interaction_graph = defaultdict(set)
    for interaction in interactions:
        source = interaction.get("source")
        target = interaction.get("target")
        if source and target:
            interaction_graph[source].add(target)
            interaction_graph[target].add(source)
    
    # 计算密度
    possible_edges = len(members) * (len(members) - 1) / 2
    actual_edges = sum(len(neighbors) for neighbors in interaction_graph.values()) / 2
    structure["density"] = actual_edges / possible_edges if possible_edges > 0 else 0
    
    # 识别角色
    member_interactions = defaultdict(int)
    for interaction in interactions:
        source = interaction.get("source")
        if source:
            member_interactions[source] += 1
    
    # 基于互动量识别角色
    for member_id, count in member_interactions.items():
        if count > len(interactions) * 0.1:
            structure["roles"][member_id] = "核心成员"
        elif count > len(interactions) * 0.05:
            structure["roles"][member_id] = "活跃成员"
        else:
            structure["roles"][member_id] = "边缘成员"
    
    return structure

def analyze_interaction_patterns(interactions: List[Dict]) -> Dict[str, Any]:
    """
    分析互动模式
    
    Args:
        interactions: 互动列表
        
    Returns:
        互动模式分析结果
    """
    patterns = {
        "by_type": defaultdict(int),
        "by_time": defaultdict(int),
        "by_member": defaultdict(int),
        "reciprocity": 0,
        "avg_chain_length": 0
    }
    
    # 按类型统计
    for interaction in interactions:
        itype = interaction.get("type", "unknown")
        patterns["by_type"][itype] += 1
        
        member = interaction.get("source")
        if member:
            patterns["by_member"][member] += 1
    
    # 计算互惠性
    pairs = set()
    reciprocal_pairs = set()
    for interaction in interactions:
        source = interaction.get("source")
        target = interaction.get("target")
        if source and target:
            pair = tuple(sorted([source, target]))
            if pair in pairs:
                reciprocal_pairs.add(pair)
            pairs.add(pair)
    
    patterns["reciprocity"] = len(reciprocal_pairs) / len(pairs) if pairs else 0
    
    return patterns

def identify_subcommunities(members: List[Dict], interactions: List[Dict]) -> List[Dict]:
    """
    识别子社区
    
    Args:
        members: 成员列表
        interactions: 互动列表
        
    Returns:
        子社区列表
    """
    # 简化的社区检测
    interaction_counts = defaultdict(lambda: defaultdict(int))
    
    for interaction in interactions:
        source = interaction.get("source")
        target = interaction.get("target")
        if source and target:
            interaction_counts[source][target] += 1
    
    # 基于互动强度聚类
    subcommunities = []
    assigned = set()
    
    for member, neighbors in interaction_counts.items():
        if member in assigned:
            continue
        
        # 创建新子社区
        subcomm = {"core": member, "members": [member]}
        assigned.add(member)
        
        for neighbor, count in neighbors.items():
            if neighbor not in assigned and count > 1:
                subcomm["members"].append(neighbor)
                assigned.add(neighbor)
        
        if len(subcomm["members"]) > 1:
            subcommunities.append(subcomm)
    
    return subcommunities

def main():
    parser = argparse.ArgumentParser(description="在线社区分析器")
    parser.add_argument("--members", "-m", help="成员数据文件")
    parser.add_argument("--interactions", "-i", help="互动数据文件")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 模拟数据
    members = [
        {"id": "user_1", "join_date": "2024-01-01"},
        {"id": "user_2", "join_date": "2024-01-15"},
        {"id": "user_3", "join_date": "2024-02-01"},
    ]
    
    interactions = [
        {"source": "user_1", "target": "user_2", "type": "reply"},
        {"source": "user_2", "target": "user_1", "type": "reply"},
        {"source": "user_1", "target": "user_3", "type": "mention"},
    ]
    
    # 分析社区结构
    structure = analyze_community_structure(members, interactions)
    
    # 分析互动模式
    patterns = analyze_interaction_patterns(interactions)
    
    # 识别子社区
    subcommunities = identify_subcommunities(members, interactions)
    
    result = {
        "structure": structure,
        "patterns": patterns,
        "subcommunities": subcommunities,
        "timestamp": datetime.now().isoformat()
    }
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[完成] 结果已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
