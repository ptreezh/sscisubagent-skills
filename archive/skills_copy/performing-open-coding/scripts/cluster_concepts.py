#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
概念聚类脚本 - 开放编码

功能：
- K-means聚类
- 层次聚类
- 聚类可视化

使用方式：
  python cluster_concepts.py --input concepts.json --output clusters.json --n-clusters 5
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def cluster_by_kmeans(concepts: List[Dict], n_clusters: int) -> Dict:
    """
    使用K-means聚类
    
    Args:
        concepts: 概念列表
        n_clusters: 聚类数量
    
    Returns:
        聚类结果字典
    """
    if len(concepts) < n_clusters:
        logging.warning(f"概念数量({len(concepts)})少于聚类数({n_clusters})，调整为{len(concepts)}")
        n_clusters = len(concepts)
    
    # 提取概念文本
    concept_texts = [c.get('concept') or c.get('code', '') for c in concepts]
    
    # TF-IDF向量化
    vectorizer = TfidfVectorizer(tokenizer=lambda x: jieba.lcut(x))
    try:
        tfidf_matrix = vectorizer.fit_transform(concept_texts)
    except Exception as e:
        logging.error(f"向量化失败: {e}")
        return {'clusters': [], 'error': str(e)}
    
    # K-means聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(tfidf_matrix)
    
    # 组织聚类结果
    clusters = {}
    for i, label in enumerate(labels):
        label = int(label)
        if label not in clusters:
            clusters[label] = []
        clusters[label].append({
            'concept': concept_texts[i],
            'frequency': concepts[i].get('frequency', 1),
            'type': concepts[i].get('type', '一般概念')
        })
    
    # 为每个聚类命名
    cluster_list = []
    for cluster_id, items in clusters.items():
        # 使用最高频的概念作为聚类名称
        representative = max(items, key=lambda x: x['frequency'])
        cluster_list.append({
            'cluster_id': cluster_id,
            'cluster_name': representative['concept'],
            'size': len(items),
            'concepts': items,
            'total_frequency': sum(c['frequency'] for c in items)
        })
    
    return {
        'method': 'kmeans',
        'n_clusters': n_clusters,
        'clusters': sorted(cluster_list, key=lambda x: x['total_frequency'], reverse=True)
    }

def cluster_hierarchical(concepts: List[Dict], n_clusters: int = None) -> Dict:
    """
    使用层次聚类
    
    Args:
        concepts: 概念列表
        n_clusters: 聚类数量（None则自动确定）
    
    Returns:
        聚类结果字典
    """
    if n_clusters is None:
        n_clusters = max(2, len(concepts) // 3)  # 自动确定
    
    if len(concepts) < 2:
        return {'clusters': [], 'error': '概念数量不足'}
    
    # 提取概念文本
    concept_texts = [c.get('concept') or c.get('code', '') for c in concepts]
    
    # TF-IDF向量化
    vectorizer = TfidfVectorizer(tokenizer=lambda x: jieba.lcut(x))
    try:
        tfidf_matrix = vectorizer.fit_transform(concept_texts)
    except Exception as e:
        logging.error(f"向量化失败: {e}")
        return {'clusters': [], 'error': str(e)}
    
    # 层次聚类
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    labels = hierarchical.fit_predict(tfidf_matrix.toarray())
    
    # 组织聚类结果
    clusters = {}
    for i, label in enumerate(labels):
        label = int(label)
        if label not in clusters:
            clusters[label] = []
        clusters[label].append({
            'concept': concept_texts[i],
            'frequency': concepts[i].get('frequency', 1),
            'type': concepts[i].get('type', '一般概念')
        })
    
    # 为每个聚类命名
    cluster_list = []
    for cluster_id, items in clusters.items():
        representative = max(items, key=lambda x: x['frequency'])
        cluster_list.append({
            'cluster_id': cluster_id,
            'cluster_name': representative['concept'],
            'size': len(items),
            'concepts': items,
            'total_frequency': sum(c['frequency'] for c in items)
        })
    
    return {
        'method': 'hierarchical',
        'n_clusters': n_clusters,
        'clusters': sorted(cluster_list, key=lambda x: x['total_frequency'], reverse=True)
    }

def generate_cluster_summary(clusters: List[Dict]) -> Dict:
    """
    生成聚类摘要统计
    
    Returns:
        统计信息字典
    """
    total_concepts = sum(c['size'] for c in clusters)
    
    # 聚类大小分布
    sizes = [c['size'] for c in clusters]
    
    # 概念类型分布
    type_distribution = {}
    for cluster in clusters:
        for concept in cluster['concepts']:
            concept_type = concept['type']
            type_distribution[concept_type] = type_distribution.get(concept_type, 0) + 1
    
    return {
        'total_clusters': len(clusters),
        'total_concepts': total_concepts,
        'average_cluster_size': round(np.mean(sizes), 2),
        'max_cluster_size': max(sizes),
        'min_cluster_size': min(sizes),
        'type_distribution': type_distribution,
        'top_clusters': [
            {
                'name': c['cluster_name'],
                'size': c['size'],
                'frequency': c['total_frequency']
            }
            for c in clusters[:5]
        ]
    }

def main():
    parser = argparse.ArgumentParser(
        description='概念聚类工具 - 开放编码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python cluster_concepts.py --input concepts.json --output clusters.json
  python cluster_concepts.py -i concepts.json -o result.json --n-clusters 5 --method kmeans
        """
    )
    parser.add_argument('--input', '-i', required=True, help='输入的概念JSON文件')
    parser.add_argument('--output', '-o', default='clusters.json', help='输出JSON文件')
    parser.add_argument('--n-clusters', '-n', type=int, help='聚类数量（默认自动确定）')
    parser.add_argument('--method', '-m', choices=['kmeans', 'hierarchical', 'both'], 
                       default='kmeans', help='聚类方法（默认：kmeans）')
    args = parser.parse_args()
    
    start_time = time.time()
    
    try:
        # 读取概念数据
        input_path = Path(args.input)
        if not input_path.exists():
            logging.error(f"文件不存在: {args.input}")
            sys.exit(1)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取概念列表
        if 'details' in data and 'concepts' in data['details']:
            concepts = data['details']['concepts']
        elif isinstance(data, list):
            concepts = data
        else:
            logging.error("无法识别的数据格式")
            sys.exit(2)
        
        if len(concepts) < 2:
            logging.error("概念数量不足（至少需要2个）")
            sys.exit(3)
        
        logging.info(f"✓ 读取概念: {len(concepts)} 个")
        
        # 自动确定聚类数
        if args.n_clusters is None:
            args.n_clusters = max(2, min(len(concepts) // 3, 10))
            logging.info(f"自动确定聚类数: {args.n_clusters}")
        
        # 执行聚类
        results = {}
        
        if args.method in ['kmeans', 'both']:
            logging.info("执行K-means聚类...")
            kmeans_result = cluster_by_kmeans(concepts, args.n_clusters)
            results['kmeans'] = kmeans_result
        
        if args.method in ['hierarchical', 'both']:
            logging.info("执行层次聚类...")
            hierarchical_result = cluster_hierarchical(concepts, args.n_clusters)
            results['hierarchical'] = hierarchical_result
        
        processing_time = time.time() - start_time
        
        # 选择主要结果
        if args.method == 'both':
            primary_result = results['kmeans']
        else:
            primary_result = results.get('kmeans') or results.get('hierarchical')
        
        # 生成摘要
        summary = generate_cluster_summary(primary_result['clusters'])
        
        # 构建输出
        output = {
            'summary': {
                **summary,
                'method': args.method,
                'processing_time': round(processing_time, 2)
            },
            'details': results,
            'metadata': {
                'input_file': str(input_path.absolute()),
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            }
        }
        
        # 保存
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        logging.info(f"✅ 聚类完成")
        logging.info(f"   聚类数量: {summary['total_clusters']}")
        logging.info(f"   概念总数: {summary['total_concepts']}")
        logging.info(f"   平均大小: {summary['average_cluster_size']}")
        logging.info(f"📄 详细结果: {args.output}")
        
    except Exception as e:
        logging.error(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(99)

if __name__ == "__main__":
    main()
