#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
范畴识别脚本 - 轴心编码

功能：
- 从开放编码结果聚类为范畴
- 范畴命名和定义
- 构建范畴层级

使用方式：
  python identify_categories.py --input codes.json --output categories.json
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def cluster_codes_to_categories(codes: List[Dict], n_categories: int = None, min_codes: int = 3) -> List[Dict]:
    """
    将编码聚类为范畴
    
    Args:
        codes: 编码列表
        n_categories: 范畴数量（None则自动确定）
        min_codes: 每个范畴最少编码数
    
    Returns:
        范畴列表
    """
    if len(codes) < min_codes:
        raise ValueError(f"编码数量不足（至少需要{min_codes}个）")
    
    # 自动确定范畴数
    if n_categories is None:
        n_categories = max(2, min(len(codes) // 5, 15))
        logging.info(f"自动确定范畴数: {n_categories}")
    
    # 提取编码文本
    code_texts = [c.get('concept') or c.get('code', '') for c in codes]
    
    # 使用TF-IDF向量化（简单实现，不依赖jieba）
    vectorizer = TfidfVectorizer(max_features=100)
    try:
        tfidf_matrix = vectorizer.fit_transform(code_texts)
    except Exception as e:
        logging.error(f"向量化失败: {e}")
        raise
    
    # K-means聚类
    kmeans = KMeans(n_clusters=n_categories, random_state=42, n_init=10)
    labels = kmeans.fit_predict(tfidf_matrix)
    
    # 组织范畴
    category_groups = {}
    for i, label in enumerate(labels):
        label = int(label)
        if label not in category_groups:
            category_groups[label] = []
        category_groups[label].append(codes[i])
    
    # 过滤小范畴
    categories = []
    for cat_id, cat_codes in category_groups.items():
        if len(cat_codes) >= min_codes:
            category = {
                'category_id': cat_id,
                'codes': cat_codes,
                'size': len(cat_codes),
                'total_frequency': sum(c.get('frequency', 1) for c in cat_codes)
            }
            categories.append(category)
    
    return sorted(categories, key=lambda x: x['total_frequency'], reverse=True)

def name_category(codes: List[Dict]) -> str:
    """
    为范畴命名
    
    策略：使用最高频编码作为范畴名
    
    Returns:
        范畴名称
    """
    if not codes:
        return "未命名范畴"
    
    # 选择频率最高的编码
    top_code = max(codes, key=lambda c: c.get('frequency', 1))
    return top_code.get('concept') or top_code.get('code', '未命名')

def define_category(codes: List[Dict]) -> str:
    """
    定义范畴
    
    策略：综合所有编码的定义
    
    Returns:
        范畴定义
    """
    if not codes:
        return ""
    
    # 提取所有编码的关键词
    all_words = []
    for code in codes:
        concept = code.get('concept') or code.get('code', '')
        all_words.extend(concept.split())
    
    # 统计高频词
    word_freq = Counter(all_words)
    top_words = [w for w, _ in word_freq.most_common(5)]
    
    # 生成定义
    definition = f"涉及{', '.join(top_words[:3])}等相关概念的范畴"
    return definition

def build_category_hierarchy(categories: List[Dict]) -> Dict:
    """
    构建范畴层级结构
    
    策略：基于包含关系和频率
    
    Returns:
        层级结构字典
    """
    # 简单实现：按频率分为核心范畴和次要范畴
    total_freq = sum(c['total_frequency'] for c in categories)
    
    core_categories = []
    secondary_categories = []
    
    for category in categories:
        proportion = category['total_frequency'] / total_freq
        if proportion > 0.15:  # 占比>15%为核心范畴
            core_categories.append(category['category_id'])
        else:
            secondary_categories.append(category['category_id'])
    
    return {
        'core': core_categories,
        'secondary': secondary_categories,
        'hierarchy_type': 'frequency_based'
    }

def calculate_category_importance(categories: List[Dict]) -> List[Dict]:
    """
    计算范畴重要性
    
    Returns:
        添加了importance字段的范畴列表
    """
    total_freq = sum(c['total_frequency'] for c in categories)
    
    for category in categories:
        category['importance'] = round(category['total_frequency'] / total_freq, 3)
    
    return categories

def main():
    parser = argparse.ArgumentParser(
        description='范畴识别工具 - 轴心编码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python identify_categories.py --input codes.json --output categories.json
  python identify_categories.py -i codes.json -o result.json --n-categories 8
        """
    )
    parser.add_argument('--input', '-i', required=True, help='输入的编码JSON文件')
    parser.add_argument('--output', '-o', default='categories.json', help='输出JSON文件')
    parser.add_argument('--n-categories', '-n', type=int, help='范畴数量（默认自动确定）')
    parser.add_argument('--min-codes', type=int, default=3, help='每个范畴最少编码数（默认：3）')
    args = parser.parse_args()
    
    start_time = time.time()
    
    try:
        # 读取编码数据
        input_path = Path(args.input)
        if not input_path.exists():
            logging.error(f"文件不存在: {args.input}")
            sys.exit(1)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取编码列表
        if 'details' in data and 'concepts' in data['details']:
            codes = data['details']['concepts']
        elif isinstance(data, list):
            codes = data
        else:
            logging.error("无法识别的数据格式")
            sys.exit(2)
        
        if len(codes) < args.min_codes:
            logging.error(f"编码数量不足（至少需要{args.min_codes}个）")
            sys.exit(3)
        
        logging.info(f"✓ 读取编码: {len(codes)} 个")
        
        # 聚类为范畴
        categories = cluster_codes_to_categories(codes, args.n_categories, args.min_codes)
        
        # 为每个范畴命名和定义
        for category in categories:
            category['name'] = name_category(category['codes'])
            category['definition'] = define_category(category['codes'])
        
        # 计算重要性
        categories = calculate_category_importance(categories)
        
        # 构建层级
        hierarchy = build_category_hierarchy(categories)
        
        processing_time = time.time() - start_time
        
        # 构建输出
        output = {
            'summary': {
                'total_categories': len(categories),
                'total_codes': len(codes),
                'core_categories': len(hierarchy['core']),
                'top_categories': [c['name'] for c in categories[:5]],
                'processing_time': round(processing_time, 2)
            },
            'details': {
                'categories': categories,
                'hierarchy': hierarchy
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
        
        logging.info(f"✅ 范畴识别完成")
        logging.info(f"   识别范畴: {len(categories)} 个")
        logging.info(f"   核心范畴: {len(hierarchy['core'])} 个")
        logging.info(f"   主要范畴: {', '.join([c['name'] for c in categories[:3]])}")
        logging.info(f"📄 详细结果: {args.output}")
        
    except Exception as e:
        logging.error(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(99)

if __name__ == "__main__":
    main()
