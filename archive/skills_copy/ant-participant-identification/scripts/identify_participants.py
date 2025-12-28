#!/usr/bin/env python3
"""
ANT参与者识别工具 - 智能依赖管理和功能降级系统

此脚本专门用于识别行动者网络中的参与者，优先使用高级功能，如不可用则降级到基础实现
"""

import argparse
import json
import sys
import importlib
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging


def install_package(package_name: str) -> bool:
    """尝试安装包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False


def check_and_import(module_name: str, package_name: Optional[str] = None) -> Any:
    """检查并导入模块，如失败则返回None"""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        if package_name:
            print(f"模块 {module_name} 未找到，正在尝试安装 {package_name}...")
            if install_package(package_name):
                try:
                    return importlib.import_module(module_name)
                except ImportError:
                    print(f"安装后仍然无法导入 {module_name}")
                    return None
            else:
                print(f"无法安装 {package_name}")
                return None
        return None


# 尝试导入高级包
np = check_and_import("numpy")
pd = check_and_import("pandas")
nx = check_and_import("networkx", "networkx")
sns = check_and_import("seaborn", "seaborn")
plt = check_and_import("matplotlib.pyplot", "matplotlib")

# 检查高级功能是否可用
ADVANCED_AVAILABLE = all([np, pd, nx])


def identify_human_actors(text: str) -> List[Dict[str, Any]]:
    """识别人类行动者"""
    # 使用正则表达式匹配可能的人名
    human_patterns = [
        r'[\\u4e00-\\u9fa5]{2,4}',  # 中文姓名（2-4个汉字）
        r'[A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*'  # 英文姓名
    ]

    human_actors = set()
    for pattern in human_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # 分割多个名称
            names = re.split(r'[，,\\s]+', match.strip())
            for name in names:
                name = name.strip()
                if 2 <= len(name) <= 10:  # 合理的姓名长度
                    human_actors.add(name)

    return [{'id': name, 'type': 'human', 'properties': {}} for name in human_actors]


def identify_nonhuman_actors(text: str) -> List[Dict[str, Any]]:
    """识别非人类行动者"""
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
            r'\\b(?:工具|设备|仪器|产品|设施|场所|空间)\\b',
            r'\\b(?:Tool|Device|Instrument|Product|Facility|Place|Space)\\b'
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


def analyze_actor_relationships(human_actors: List[Dict], nonhuman_actors: List[Dict], text: str) -> List[Dict[str, Any]]:
    """分析行动者关系"""
    relationships = []
    all_actors = [actor['id'] for actor in human_actors + nonhuman_actors]

    # 识别行动者之间的关系（基于共同出现、动作关系等）
    for i, actor1 in enumerate(all_actors):
        for j, actor2 in enumerate(all_actors):
            if i < j:  # 避免重复
                # 检查是否在同一句子中出现
                sentences = re.split(r'[。！？\\n]', text)
                for sentence in sentences:
                    if actor1 in sentence and actor2 in sentence:
                        # 简单的关系类型识别
                        if any(action in sentence for action in ['使用', '开发', '影响', '连接', '合作', 'interaction', 'use', 'develop', 'affect']):
                            rel_type = 'affects'
                        elif any(action in sentence for action in ['支持', '帮助', '协助', 'assist', 'support']):
                            rel_type = 'supports'
                        elif any(action in sentence for action in ['反对', '抵制', 'oppose', 'resist']):
                            rel_type = 'opposes'
                        else:
                            rel_type = 'associated_with'

                        relationships.append({
                            'source': actor1,
                            'target': actor2,
                            'type': rel_type,
                            'properties': {
                                'context': sentence.strip(),
                                'confidence': 0.7
                            }
                        })
                        break  # 找到一个关系就够了

    return relationships


def calculate_network_metrics(actors: List[Dict], relationships: List[Dict]) -> Dict[str, Any]:
    """计算网络指标（如果高级功能可用）"""
    if ADVANCED_AVAILABLE:
        try:
            import networkx as nx

            # 创建网络图
            G = nx.Graph()
            for actor in actors:
                G.add_node(actor['id'], **actor.get('properties', {}))

            for rel in relationships:
                G.add_edge(rel['source'], rel['target'], **rel.get('properties', {}))

            # 计算网络指标
            metrics = {
                'num_nodes': G.number_of_nodes(),
                'num_edges': G.number_of_edges(),
                'density': nx.density(G),
                'is_connected': nx.is_connected(G),
                'components': nx.number_connected_components(G)
            }

            if G.number_of_nodes() > 0:
                metrics['avg_clustering'] = nx.average_clustering(G)
                if nx.is_connected(G):
                    metrics['avg_shortest_path'] = nx.average_shortest_path_length(G)
                else:
                    # 对于非连通图，计算各连通分量的平均最短路径
                    components = [G.subgraph(c) for c in nx.connected_components(G)]
                    avg_paths = [nx.average_shortest_path_length(comp) for comp in components if comp.number_of_nodes() > 1]
                    metrics['avg_shortest_path'] = sum(avg_paths) / len(avg_paths) if avg_paths else float('inf')

                # 中心性指标（仅当节点数大于1时计算）
                if G.number_of_nodes() > 1:
                    metrics['centrality'] = {
                        'degree': dict(nx.degree_centrality(G)),
                        'betweenness': dict(nx.betweenness_centrality(G)),
                        'closeness': dict(nx.closeness_centrality(G)),
                        'eigenvector': dict(nx.eigenvector_centrality(G, max_iter=1000))
                    }

            return metrics
        except Exception as e:
            print(f"高级网络分析失败: {e}，使用基础分析")

    # 降级到基础实现
    return {
        'num_nodes': len(actors),
        'num_edges': len(relationships),
        'density': len(relationships) / (len(actors) * (len(actors) - 1) / 2) if len(actors) > 1 else 0,
        'actors': [actor['id'] for actor in actors],
        'relationships': [(rel['source'], rel['target']) for rel in relationships]
    }


def main():
    parser = argparse.ArgumentParser(
        description='ANT参与者识别工具（支持高级功能，提供优雅降级）',
        epilog='示例：python ant_participant_identification.py --input data.json --output results.json'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON格式）')
    parser.add_argument('--output', '-o', default='ant_participants.json', help='输出文件')

    args = parser.parse_args()

    start_time = datetime.now()

    # 读取输入数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)

    # 确定要分析的文本
    if isinstance(data, dict):
        if 'text' in data:
            text = data['text']
        elif 'content' in data:
            text = data['content']
        else:
            text = json.dumps(data, ensure_ascii=False)
    elif isinstance(data, list):
        text = ' '.join(str(item) for item in data)
    elif isinstance(data, str):
        text = data
    else:
        text = str(data)

    # 识别人类行动者
    human_actors = identify_human_actors(text)

    # 识别非人类行动者
    nonhuman_actors = identify_nonhuman_actors(text)

    # 分析关系
    relationships = analyze_actor_relationships(human_actors, nonhuman_actors, text)

    # 计算网络指标
    network_metrics = calculate_network_metrics(human_actors + nonhuman_actors, relationships)

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'n_actors': len(human_actors + nonhuman_actors),
            'n_human_actors': len(human_actors),
            'n_nonhuman_actors': len(nonhuman_actors),
            'n_relationships': len(relationships),
            'network_density': network_metrics.get('density', 0),
            'processing_time': round((end_time - start_time).total_seconds(), 2),
            'using_advanced': ADVANCED_AVAILABLE
        },
        'details': {
            'actors': {
                'human': human_actors,
                'nonhuman': nonhuman_actors
            },
            'relationships': relationships,
            'network_metrics': network_metrics
        },
        'metadata': {
            'input_file': args.input,
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'ant-participant-identification'
        }
    }

    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ ANT参与者识别完成")
    print(f"  - 总行动者数: {len(human_actors + nonhuman_actors)}")
    print(f"  - 人类行动者: {len(human_actors)}")
    print(f"  - 非人类行动者: {len(nonhuman_actors)}")
    print(f"  - 关系数: {len(relationships)}")
    print(f"  - 使用高级功能: {output['summary']['using_advanced']}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()