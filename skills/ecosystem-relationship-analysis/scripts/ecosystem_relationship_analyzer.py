import json
import sys
from datetime import datetime

# 导入独立的算法模块
from algorithms.network_analysis import (calculate_network_topology, calculate_degree_centrality, 
                                       calculate_closeness_centrality, calculate_betweenness_centrality)
from algorithms.community_detection import find_communities_greedy_modularity
from algorithms.health_assessment import assess_ecosystem_health

def identify_key_relationships(relationships, degree_centrality):
    """
    识别关键关系
    """
    key_relationships = []
    for rel in relationships:
        source = rel.get('source', '')
        target = rel.get('target', '')
        rel_type = rel.get('type', '')
        strength = rel.get('strength', 0.5)
        
        # 计算关键分数：基于连接的实体的重要性
        source_degree = degree_centrality.get(source, 0)
        target_degree = degree_centrality.get(target, 0)
        
        # 关键分数 = (源实体重要性 + 目标实体重要性) * 关系强度
        key_score = (source_degree + target_degree) * strength
        source_importance = source_degree / max(degree_centrality.values()) if degree_centrality else 0
        target_importance = target_degree / max(degree_centrality.values()) if degree_centrality else 0
        
        key_relationships.append({
            'source': source,
            'target': target,
            'type': rel_type,
            'strength': strength,
            'keyScore': key_score,
            'sourceImportance': source_importance,
            'targetImportance': target_importance
        })
    
    return key_relationships

def analyze_relationships(ecosystem_data):
    """
    分析生态系统中实体间的关系
    """
    entities = ecosystem_data.get('entities', [])
    relationships = ecosystem_data.get('relationships', [])
    
    # 使用算法模块进行网络分析
    network_topology = calculate_network_topology(entities, relationships)
    
    # 计算各种中心性
    degree_centrality = calculate_degree_centrality(entities, relationships)
    closeness_centrality = calculate_closeness_centrality(entities, relationships, degree_centrality)
    betweenness_centrality = calculate_betweenness_centrality(entities, relationships, degree_centrality)
    
    # 识别关键关系
    key_relationships = identify_key_relationships(relationships, degree_centrality)
    
    # 社区检测
    communities = find_communities_greedy_modularity(entities, relationships)
    
    # 健康度评估
    health_assessment = assess_ecosystem_health(network_topology, {
        'degree': degree_centrality,
        'closeness': closeness_centrality,
        'betweenness': betweenness_centrality
    }, communities, relationships)
    
    # 更新网络拓扑中的平均度
    network_topology['averageDegree'] = sum(degree_centrality.values()) / max(1, len(degree_centrality))
    
    return {
        "relationshipAnalysis": {
            "summary": {
                "totalRelationships": len(relationships),
                "averageStrength": sum(rel.get('strength', 0.5) for rel in relationships) / max(1, len(relationships)) if relationships else 0.0,
                "relationshipTypeCount": len(set(rel.get('type', '') for rel in relationships)),
                "keyRelationshipCount": len([r for r in relationships if r.get('strength', 0.5) > 0.6]),
                "primaryTypes": list(set(rel.get('type', '') for rel in relationships))
            },
            "relationshipTypes": {
                rel_type: {
                    "count": len([r for r in relationships if r.get('type', '') == rel_type]),
                    "avgStrength": sum(r.get('strength', 0.5) for r in relationships if r.get('type', '') == rel_type) / len([r for r in relationships if r.get('type', '') == rel_type]) if [r for r in relationships if r.get('type', '') == rel_type] else 0
                } for rel_type in set(rel.get('type', '') for rel in relationships)
            },
            "keyRelationships": sorted(key_relationships, key=lambda x: x['keyScore'], reverse=True)[:10]  # 仅返回前10个关键关系
        },
        "networkProperties": {
            "topology": network_topology,
            "centralities": {
                "degree": degree_centrality,
                "closeness": closeness_centrality,
                "betweenness": betweenness_centrality
            },
            "communities": {
                "count": len(communities),
                "communities": communities,
                "entityToCommunity": {entity_id: i for i, comm in enumerate(communities) for entity_id in comm['entities']}
            },
            "health": health_assessment
        }
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: python ecosystem_relationship_analyzer.py <function> --input_file <input_file>")
        sys.exit(1)

    function_name = sys.argv[1]
    input_file = None

    # 解析参数
    for i, arg in enumerate(sys.argv):
        if arg == "--input_file" and i + 1 < len(sys.argv):
            input_file = sys.argv[i + 1]
            break

    if not input_file:
        print("Input file is required")
        sys.exit(1)

    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    # 执行关系分析
    if function_name == "ecosystem-relationship-analysis":
        # 使用输入数据进行关系分析
        result = analyze_relationships(input_data)
        
        # 构建完整的输出结果
        final_result = {
            "summary": {
                "total_entities": len(input_data.get('entities', [])),
                "total_relationships": len(input_data.get('relationships', [])),
                "relationship_types": list(set(rel.get('type', '') for rel in input_data.get('relationships', []))),
                "ecosystem_health_score": result["networkProperties"]["health"]["score"],
                "key_relationships_count": len(result["relationshipAnalysis"]["keyRelationships"])
            },
            "details": result,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "skill": "ecosystem-relationship-analysis",
                "validationScore": result["networkProperties"]["health"]["score"]
            }
        }

        print(json.dumps(final_result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()