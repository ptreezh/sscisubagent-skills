#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paradigm模型构建脚本 - 轴心编码

功能：
- 识别条件维度
- 识别行动/互动
- 识别结果维度
- 构建完整Paradigm模型

使用方式：
  python construct_paradigm.py --input relationships.json --output paradigm.json
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def identify_conditions(categories: List[Dict], relations: List[Dict]) -> List[str]:
    """
    识别条件维度
    
    策略：查找作为因果关系源头的范畴
    
    Returns:
        条件范畴列表
    """
    conditions = []
    
    # 查找条件关系
    conditional_sources = [r['source'] for r in relations if r['type'] == 'CONDITIONAL']
    
    # 查找因果关系的源头
    causal_sources = [r['source'] for r in relations if r['type'] == 'CAUSAL']
    
    # 合并并去重
    all_conditions = set(conditional_sources + causal_sources)
    
    return list(all_conditions)

def identify_actions(categories: List[Dict], relations: List[Dict]) -> List[str]:
    """
    识别行动/互动维度
    
    策略：查找策略关系的范畴
    
    Returns:
        行动范畴列表
    """
    actions = []
    
    # 查找策略关系
    strategy_categories = [r['category'] for r in relations if r['type'] == 'STRATEGY']
    
    # 查找互动关系
    interaction_categories = []
    for r in relations:
        if r['type'] == 'INTERACTION':
            interaction_categories.extend([r['source'], r['target']])
    
    # 合并并去重
    all_actions = set(strategy_categories + interaction_categories)
    
    return list(all_actions)

def identify_consequences(categories: List[Dict], relations: List[Dict]) -> List[str]:
    """
    识别结果维度
    
    策略：查找作为因果关系目标的范畴
    
    Returns:
        结果范畴列表
    """
    consequences = []
    
    # 查找因果关系的目标
    causal_targets = [r['target'] for r in relations if r['type'] == 'CAUSAL']
    
    return list(set(causal_targets))

def identify_phenomenon(categories: List[Dict], relations: List[Dict]) -> str:
    """
    识别核心现象
    
    策略：选择连接最多的范畴
    
    Returns:
        核心现象范畴名称
    """
    if not relations:
        # 如果没有关系，选择频率最高的范畴
        return max(categories, key=lambda c: c.get('total_frequency', 0))['name']
    
    # 统计每个范畴的连接数
    category_connections = {}
    for rel in relations:
        if 'source' in rel:
            category_connections[rel['source']] = category_connections.get(rel['source'], 0) + 1
        if 'target' in rel:
            category_connections[rel['target']] = category_connections.get(rel['target'], 0) + 1
    
    # 选择连接最多的
    if category_connections:
        phenomenon = max(category_connections.items(), key=lambda x: x[1])[0]
        return phenomenon
    
    return categories[0]['name'] if categories else "未识别"

def build_paradigm_model(categories: List[Dict], relations: List[Dict]) -> Dict:
    """
    构建完整Paradigm模型
    
    Returns:
        Paradigm模型字典
    """
    # 识别核心现象
    phenomenon = identify_phenomenon(categories, relations)
    
    # 识别各维度
    conditions = identify_conditions(categories, relations)
    actions = identify_actions(categories, relations)
    consequences = identify_consequences(categories, relations)
    
    # 识别语境（不在条件、行动、结果中的范畴）
    all_categories = set(c['name'] for c in categories)
    used_categories = set(conditions + actions + consequences + [phenomenon])
    context = list(all_categories - used_categories)
    
    return {
        'phenomenon': phenomenon,
        'causal_conditions': conditions,
        'context': context,
        'intervening_conditions': [],  # 需要更复杂的分析
        'action_strategies': actions,
        'consequences': consequences
    }

def validate_paradigm(model: Dict) -> Dict:
    """
    验证Paradigm模型完整性
    
    Returns:
        验证结果
    """
    issues = []
    
    if not model['phenomenon']:
        issues.append("缺少核心现象")
    
    if not model['causal_conditions']:
        issues.append("缺少因果条件")
    
    if not model['action_strategies']:
        issues.append("缺少行动策略")
    
    if not model['consequences']:
        issues.append("缺少结果维度")
    
    completeness = 1.0 - (len(issues) / 4.0)
    
    return {
        'is_complete': len(issues) == 0,
        'completeness_score': round(completeness, 2),
        'issues': issues
    }

def main():
    parser = argparse.ArgumentParser(
        description='Paradigm模型构建工具 - 轴心编码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python construct_paradigm.py --input relationships.json --output paradigm.json
        """
    )
    parser.add_argument('--input', '-i', required=True, help='输入的关系JSON文件')
    parser.add_argument('--output', '-o', default='paradigm.json', help='输出JSON文件')
    args = parser.parse_args()
    
    start_time = time.time()
    
    try:
        # 读取关系数据
        input_path = Path(args.input)
        if not input_path.exists():
            logging.error(f"文件不存在: {args.input}")
            sys.exit(1)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取范畴和关系
        if 'details' not in data:
            logging.error("数据格式错误：缺少details字段")
            sys.exit(2)
        
        # 从之前的categories.json读取范畴
        categories_file = input_path.parent / 'categories_test.json'
        if categories_file.exists():
            with open(categories_file, 'r', encoding='utf-8') as f:
                cat_data = json.load(f)
                categories = cat_data.get('details', {}).get('categories', [])
        else:
            categories = []
        
        # 提取关系
        all_relations = []
        for rel_type in ['causal_relations', 'conditional_relations', 'interaction_relations']:
            if rel_type in data['details']:
                all_relations.extend(data['details'][rel_type])
        
        logging.info(f"✓ 读取关系: {len(all_relations)} 个")
        logging.info(f"✓ 读取范畴: {len(categories)} 个")
        
        # 构建Paradigm模型
        paradigm = build_paradigm_model(categories, all_relations)
        
        # 验证模型
        validation = validate_paradigm(paradigm)
        
        processing_time = time.time() - start_time
        
        # 构建输出
        output = {
            'summary': {
                'phenomenon': paradigm['phenomenon'],
                'conditions_count': len(paradigm['causal_conditions']),
                'actions_count': len(paradigm['action_strategies']),
                'consequences_count': len(paradigm['consequences']),
                'completeness': validation['completeness_score'],
                'processing_time': round(processing_time, 2)
            },
            'details': {
                'paradigm': paradigm,
                'validation': validation
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
        
        logging.info(f"✅ Paradigm构建完成")
        logging.info(f"   核心现象: {paradigm['phenomenon']}")
        logging.info(f"   完整度: {validation['completeness_score']*100:.0f}%")
        if validation['issues']:
            logging.warning(f"   问题: {', '.join(validation['issues'])}")
        logging.info(f"📄 详细结果: {args.output}")
        
    except Exception as e:
        logging.error(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(99)

if __name__ == "__main__":
    main()
