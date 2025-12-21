#!/usr/bin/env python3
"""
故事线构建工具

功能：
1. 提取时间线（timeline extraction）
2. 识别关键事件（key events identification）
3. 识别行动者（actors identification）
4. 构建因果链条（causal chain construction）
5. 生成故事线叙述（storyline narrative generation）

标准化接口：argparse + 三层JSON输出
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple


def extract_timeline(data: List[Dict]) -> List[Dict]:
    """提取时间线"""
    timeline = []
    
    for item in data:
        # 提取时间信息（如果有）
        time_info = item.get('time') or item.get('stage') or item.get('phase')
        if time_info:
            timeline.append({
                'time': time_info,
                'event': item.get('event') or item.get('action') or item.get('name'),
                'data': item
            })
    
    # 按时间排序
    timeline.sort(key=lambda x: x['time'])
    
    return timeline


def identify_key_events(timeline: List[Dict], categories: List[Dict]) -> List[Dict]:
    """识别关键事件"""
    key_events = []
    
    for item in timeline:
        # 判断是否为关键事件
        # 标准：与核心范畴相关、有重要影响
        event = item['event']
        
        # 检查是否与核心范畴相关
        is_key = False
        for category in categories:
            if category.get('type') == '核心范畴':
                category_name = category.get('name', '')
                if category_name in event or event in category_name:
                    is_key = True
                    break
        
        if is_key:
            key_events.append({
                **item,
                'is_key_event': True,
                'importance': 'high'
            })
    
    return key_events


def identify_actors(data: List[Dict]) -> List[str]:
    """识别行动者"""
    actors = set()
    
    for item in data:
        # 提取行动者信息
        actor = item.get('actor') or item.get('participant') or item.get('subject')
        if actor:
            actors.add(actor)
    
    return sorted(list(actors))


def build_causal_chain(events: List[Dict], relations: List[Dict]) -> List[Tuple]:
    """构建因果链条"""
    causal_chain = []
    
    for rel in relations:
        if rel.get('type') == 'causal':
            source = rel.get('source')
            target = rel.get('target')
            strength = rel.get('strength', 0)
            
            causal_chain.append((source, target, strength))
    
    # 按强度排序
    causal_chain.sort(key=lambda x: x[2], reverse=True)
    
    return causal_chain


def generate_storyline(timeline: List[Dict], key_events: List[Dict], 
                      actors: List[str], causal_chain: List[Tuple],
                      core_category: str) -> str:
    """生成故事线叙述"""
    
    # 构建故事线文本
    storyline_parts = []
    
    # 开头：介绍核心现象和行动者
    storyline_parts.append(f"本研究聚焦于'{core_category}'这一核心现象。")
    if actors:
        actors_str = '、'.join(actors[:3])
        storyline_parts.append(f"主要行动者包括{actors_str}等。")
    
    # 中间：关键事件和因果链条
    if key_events:
        storyline_parts.append("\n故事发展经历了以下关键阶段：")
        for i, event in enumerate(key_events[:5], 1):
            storyline_parts.append(f"{i}. {event['event']}（{event['time']}）")
    
    if causal_chain:
        storyline_parts.append("\n核心因果链条为：")
        for i, (source, target, strength) in enumerate(causal_chain[:3], 1):
            storyline_parts.append(f"{i}. {source} → {target}（强度：{strength:.2f}）")
    
    # 结尾：总结
    storyline_parts.append(f"\n通过这一过程，'{core_category}'现象得以展现和发展。")
    
    return '\n'.join(storyline_parts)


def main():
    parser = argparse.ArgumentParser(
        description='故事线构建工具',
        epilog='示例：python construct_storyline.py -i data.json -c categories.json -r relations.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--categories', '-c', required=True, help='范畴文件（JSON）')
    parser.add_argument('--relations', '-r', required=True, help='关系文件（JSON）')
    parser.add_argument('--output', '-o', default='storyline.json', help='输出文件名')
    parser.add_argument('--core-category', default=None, help='核心范畴名称（可选）')
    
    args = parser.parse_args()
    
    # 读取输入
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
            data = input_data.get('details', {}).get('data', []) or input_data.get('data', [])
    except Exception as e:
        print(f"错误：无法读取数据文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(args.categories, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
            categories = categories_data.get('details', {}).get('categories', [])
    except Exception as e:
        print(f"错误：无法读取范畴文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(args.relations, 'r', encoding='utf-8') as f:
            relations_data = json.load(f)
            relations = relations_data.get('details', {}).get('relations', [])
    except Exception as e:
        print(f"错误：无法读取关系文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 确定核心范畴
    core_category = args.core_category
    if not core_category:
        # 自动选择第一个核心范畴
        for cat in categories:
            if cat.get('type') == '核心范畴':
                core_category = cat.get('name')
                break
        if not core_category:
            core_category = categories[0].get('name') if categories else '未知现象'
    
    # 构建故事线
    timeline = extract_timeline(data)
    key_events = identify_key_events(timeline, categories)
    actors = identify_actors(data)
    causal_chain = build_causal_chain(key_events, relations)
    storyline_text = generate_storyline(timeline, key_events, actors, causal_chain, core_category)
    
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()
    
    # 标准化输出
    output = {
        'summary': {
            'core_category': core_category,
            'total_events': len(timeline),
            'key_events_count': len(key_events),
            'actors_count': len(actors),
            'causal_chain_length': len(causal_chain),
            'processing_time': round(processing_time, 2)
        },
        'details': {
            'timeline': timeline,
            'key_events': key_events,
            'actors': actors,
            'causal_chain': [{'source': s, 'target': t, 'strength': st} 
                            for s, t, st in causal_chain],
            'storyline_text': storyline_text
        },
        'metadata': {
            'input_file': args.input,
            'categories_file': args.categories,
            'relations_file': args.relations,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'performing-selective-coding'
        }
    }
    
    # 写入输出
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"✓ 故事线构建完成")
        print(f"  - 核心范畴：{core_category}")
        print(f"  - 关键事件：{len(key_events)}个")
        print(f"  - 行动者：{len(actors)}个")
        print(f"  - 输出文件：{args.output}")
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
