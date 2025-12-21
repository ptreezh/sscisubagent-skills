#!/usr/bin/env python3
"""
行动者识别工具

功能：
1. 识别人类行动者
2. 识别非人类行动者
3. 分析行动者关系
4. 构建行动者网络

标准化接口：argparse + 三层JSON输出
不依赖额外的网络分析包
"""

import argparse
import json
import sys
import re
from datetime import datetime
from typing import Dict, List, Any, Set
from collections import defaultdict


def extract_human_actors(text: str) -> List[Dict[str, Any]]:
    """从文本中识别人类行动者"""
    # 使用正则表达式匹配可能的人名
    # 匹配中文姓名（2-4个汉字）
    human_patterns = [
        r'[\\u4e00-\\u9fa5]{2,4}(?:\\s*[，,]\\s*[\\u4e00-\\u9fa5]{2,4})*',  # 中文姓名
        r'[A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*',  # 英文姓名
    ]
    
    human_actors = set()
    for pattern in human_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # 分割多个名称
            names = re.split(r'[，,\\s]+', match.strip())
            for name in names:
                name = name.strip()
                if len(name) >= 2 and len(name) <= 10:  # 合理的姓名长度
                    human_actors.add(name)
    
    # 过滤掉常见的非人名词汇
    common_non_names = {
        '中国', '北京', '上海', '公司', '政府', '组织', '机构', '系统', '技术', 
        '方法', '研究', '论文', '报告', '数据', '信息', '服务', '平台', '网站'
    }
    
    human_actors = human_actors - common_non_names
    
    return [{'id': name, 'type': 'human', 'properties': {}} for name in human_actors]


def extract_nonhuman_actors(text: str) -> List[Dict[str, Any]]:
    """从文本中识别非人类行动者"""
    # 定义非人类行动者的常见类型
    nonhuman_patterns = {
        'technology': [
            r'\\b(?:计算机|电脑|手机|软件|系统|平台|APP|网站|互联网|AI|人工智能|机器学习|大数据|云计算|物联网|区块链)\\b',
            r'\\b(?:Computer|Software|System|Platform|Website|Internet|AI|Artificial Intelligence|Machine Learning|Big Data|Cloud Computing|IoT|Blockchain)\\b'
        ],
        'document': [
            r'\\b(?:文件|文档|报告|论文|书籍|期刊|杂志|报纸|资料|信息)\\b',
            r'\\b(?:Document|Report|Paper|Book|Journal|Magazine|Newspaper|Information)\\b'
        ],
        'organization': [
            r'\\b(?:公司|企业|组织|机构|部门|政府|学校|医院|协会|团体)\\b',
            r'\\b(?:Company|Enterprise|Organization|Institution|Department|Government|School|Hospital|Association|Group)\\b'
        ],
        'concept': [
            r'\\b(?:理论|概念|思想|观点|方法|模式|框架|模型|制度|政策|法规)\\b',
            r'\\b(?:Theory|Concept|Idea|Method|Pattern|Framework|Model|System|Policy|Regulation)\\b'
        ],
        'artifact': [
            r'\\b(?:工具|设备|仪器|产品|设备|设施|建筑|场所|空间)\\b',
            r'\\b(?:Tool|Device|Instrument|Product|Facility|Building|Place|Space)\\b'
        ]
    }
    
    nonhuman_actors = []
    used_spans = set()  # 记录已使用的文本位置，避免重复
    
    for category, patterns in nonhuman_patterns.items():
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                start, end = match.span()
                # 检查是否与已识别的实体重叠
                if not any(s < end and start < e for s, e in used_spans):
                    entity = match.group().strip()
                    if len(entity) > 1:  # 过滤掉单字符
                        nonhuman_actors.append({
                            'id': entity,
                            'type': 'nonhuman',
                            'category': category,
                            'properties': {}
                        })
                        used_spans.add((start, end))
    
    return nonhuman_actors


def identify_relationships(text: str, actors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """识别行动者之间的关系"""
    relationships = []
    actor_ids = [actor['id'] for actor in actors]
    
    # 定义关系模式
    relationship_patterns = [
        (r'(\\w+)\\s*支持\\s*(\\w+)', 'supports'),
        (r'(\\w+)\\s*影响\\s*(\\w+)', 'affects'),
        (r'(\\w+)\\s*控制\\s*(\\w+)', 'controls'),
        (r'(\\w+)\\s*依赖\\s*(\\w+)', 'depends_on'),
        (r'(\\w+)\\s*协作\\s*(\\w+)', 'collaborates_with'),
        (r'(\\w+)\\s*连接\\s*(\\w+)', 'connects'),
        (r'(\\w+)\\s*作用于\\s*(\\w+)', 'acts_on'),
        (r'(\\w+)\\s*与\\s*(\\w+)\\s*合作', 'collaborates_with'),
        (r'(\\w+)\\s*与\\s*(\\w+)\\s*相关', 'related_to'),
        (r'(\\w+)\\s*使用\\s*(\\w+)', 'uses'),
        (r'(\\w+)\\s*包含\\s*(\\w+)', 'contains'),
        (r'(\\w+)\\s*促进\\s*(\\w+)', 'facilitates'),
    ]
    
    for pattern, rel_type in relationship_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            actor1, actor2 = match.group(1), match.group(2)
            
            # 验证是否为已识别的行动者
            if actor1 in actor_ids and actor2 in actor_ids and actor1 != actor2:
                rel = {
                    'source': actor1,
                    'target': actor2,
                    'type': rel_type,
                    'properties': {
                        'text_evidence': match.group(0),
                        'confidence': 0.8  # 基于模式匹配的置信度
                    }
                }
                relationships.append(rel)
    
    # 去重
    unique_rels = []
    seen = set()
    for rel in relationships:
        rel_key = (rel['source'], rel['target'], rel['type'])
        if rel_key not in seen:
            unique_rels.append(rel)
            seen.add(rel_key)
    
    return unique_rels


def analyze_network_properties(actors: List[Dict[str, Any]], relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
    """分析网络基本属性"""
    if not actors:
        return {'error': '没有识别到行动者'}
    
    # 计算度数
    degree_count = defaultdict(int)
    for rel in relationships:
        degree_count[rel['source']] += 1
        degree_count[rel['target']] += 1
    
    # 计算网络密度
    n_actors = len(actors)
    n_relationships = len(relationships)
    max_possible_rels = n_actors * (n_actors - 1)  # 有向图
    density = n_relationships / max_possible_rels if max_possible_rels > 0 else 0
    
    # 识别关键节点（度数最高的节点）
    sorted_degrees = sorted(degree_count.items(), key=lambda x: x[1], reverse=True)
    key_actors = [actor_id for actor_id, _ in sorted_degrees[:min(5, len(sorted_degrees))]]
    
    return {
        'n_actors': n_actors,
        'n_relationships': n_relationships,
        'density': round(density, 4),
        'average_degree': sum(degree_count.values()) / n_actors if n_actors > 0 else 0,
        'key_actors': key_actors,
        'degree_distribution': dict(sorted_degrees)
    }


def main():
    parser = argparse.ArgumentParser(
        description='行动者识别工具（不依赖额外网络分析包）',
        epilog='示例：python identify_actors.py --input data.json --output actors.json'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--output', '-o', default='actors.json', help='输出文件')
    
    args = parser.parse_args()

    # 读取输入数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)

    start_time = datetime.now()

    # 确定要分析的文本
    if isinstance(data, dict):
        if 'text' in data:
            text = data['text']
        elif 'content' in data:
            text = data['content']
        else:
            # 尝试将整个字典转换为字符串
            text = json.dumps(data, ensure_ascii=False)
    elif isinstance(data, list):
        text = ' '.join(str(item) for item in data)
    elif isinstance(data, str):
        text = data
    else:
        text = str(data)

    # 识别人类行动者
    human_actors = extract_human_actors(text)
    
    # 识别非人类行动者
    nonhuman_actors = extract_nonhuman_actors(text)
    
    # 合并所有行动者
    all_actors = human_actors + nonhuman_actors
    
    # 识别关系
    relationships = identify_relationships(text, all_actors)
    
    # 分析网络属性
    network_properties = analyze_network_properties(all_actors, relationships)

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'n_actors': len(all_actors),
            'n_human_actors': len(human_actors),
            'n_nonhuman_actors': len(nonhuman_actors),
            'n_relationships': len(relationships),
            'network_density': network_properties.get('density', 0),
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'actors': all_actors,
            'relationships': relationships,
            'network_properties': network_properties
        },
        'metadata': {
            'input_file': args.input,
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'ant'
        }
    }

    # 保存输出
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ 行动者识别完成")
    print(f"  - 总行动者数: {len(all_actors)}")
    print(f"  - 人类行动者: {len(human_actors)}")
    print(f"  - 非人类行动者: {len(nonhuman_actors)}")
    print(f"  - 关系数: {len(relationships)}")
    print(f"  - 网络密度: {network_properties.get('density', 0):.4f}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()