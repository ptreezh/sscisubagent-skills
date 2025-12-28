import json
import sys
from datetime import datetime

# 导入独立的算法模块
from algorithms.entity_recognition import extract_entities_from_input, standardize_entity_format
from algorithms.relationship_mapping import map_relationships_from_input, validate_relationship_integrity
from algorithms.data_validation import validate_data

def main():
    if len(sys.argv) < 3:
        print("Usage: python ecosystem_data_collector.py <function> --input_file <input_file>")
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

    target_industry = input_data.get("targetIndustry", "unknown")
    search_scope = input_data.get("search_scope", {})
    data_types = input_data.get("data_types", ["company_info", "relationships", "industry_trends"])
    collection_depth = input_data.get("collection_depth", "standard")
    verification_required = input_data.get("verification_required", True)

    # 根据函数名执行相应操作
    if function_name == "business-ecosystem-data-collection":
        # 使用算法模块提取实体和关系
        entities = extract_entities_from_input(input_data)
        relationships = map_relationships_from_input(input_data)
        
        # 标准化实体格式
        standardized_entities = [standardize_entity_format(entity) for entity in entities]
        
        # 验证关系完整性
        entity_ids = [e['id'] for e in standardized_entities]
        validated_relationships = validate_relationship_integrity(relationships, entity_ids)
        
        industry_info = input_data.get('industry_info', {})
        
        if verification_required:
            validated_results = validate_data(standardized_entities, validated_relationships, industry_info)
        else:
            validated_results = {
                "entities": standardized_entities,
                "relationships": validated_relationships,
                "industry_info": industry_info,
                "validation_score": 0.8,
                "validation_details": {
                    "entity_uniqueness": 1.0,
                    "relationship_validity": 1.0,
                    "entity_count": len(standardized_entities),
                    "relationship_count": len(validated_relationships)
                }
            }

        # 构建输出结果
        result = {
            "summary": {
                "entities_found": len(validated_results["entities"]),
                "relationships_found": len(validated_results["relationships"]),
                "data_quality_score": validated_results["validation_score"],
                "collection_time": datetime.now().isoformat()
            },
            "details": {
                "collected_entities": validated_results["entities"],
                "relationships": validated_results["relationships"],
                "industry_info": validated_results["industry_info"],
                "collection_metrics": {
                    "target_industry": target_industry,
                    "search_scope": search_scope,
                    "data_types": data_types,
                    "collection_depth": collection_depth
                },
                "data_quality_report": {
                    "validation_score": validated_results["validation_score"],
                    "validation_details": validated_results["validation_details"],
                    "verification_performed": verification_required
                }
            },
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "skill": "business-ecosystem-data-collection"
            }
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()