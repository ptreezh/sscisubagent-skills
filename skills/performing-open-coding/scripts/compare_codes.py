#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持续比较脚本 - 开放编码

功能：
- 计算编码间相似度
- 识别重复编码
- 建议合并编码

使用方式：
  python compare_codes.py --input codes.json --output comparison.json
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def calculate_similarity(code1: str, code2: str) -> float:
    """
    计算两个编码的语义相似度
    
    Args:
        code1: 编码1
        code2: 编码2
    
    Returns:
        相似度分数（0-1）
    """
    # 使用TF-IDF + 余弦相似度
    vectorizer = TfidfVectorizer(tokenizer=lambda x: jieba.lcut(x))
    try:
        tfidf_matrix = vectorizer.fit_transform([code1, code2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except:
        return 0.0

def identify_duplicates(codes: List[Dict], threshold: float = 0.8) -> List[Tuple]:
    """
    识别重复或高度相似的编码
    
    Args:
        codes: 编码列表
        threshold: 相似度阈值（默认0.8）
    
    Returns:
        重复编码对列表 [(code1, code2, similarity), ...]
    """
    duplicates = []
    n = len(codes)
    
    for i in range(n):
        for j in range(i + 1, n):
            # 兼容'code'和'concept'字段
            code1 = codes[i].get('code') or codes[i].get('concept', '')
            code2 = codes[j].get('code') or codes[j].get('concept', '')
            
            if not code1 or not code2:
                continue
            
            similarity = calculate_similarity(code1, code2)
            
            if similarity >= threshold:
                duplicates.append({
                    'code1': code1,
                    'code2': code2,
                    'similarity': round(similarity, 3),
                    'index1': i,
                    'index2': j
                })
    
    return duplicates

def suggest_merges(codes: List[Dict], duplicates: List[Dict]) -> List[Dict]:
    """
    建议合并编码
    
    Args:
        codes: 编码列表
        duplicates: 重复编码列表
    
    Returns:
        合并建议列表
    """
    suggestions = []
    
    for dup in duplicates:
        code1_data = codes[dup['index1']]
        code2_data = codes[dup['index2']]
        
        # 选择频率更高的作为主编码
        if code1_data.get('frequency', 0) >= code2_data.get('frequency', 0):
            primary = code1_data
            secondary = code2_data
        else:
            primary = code2_data
            secondary = code1_data
        
        # 兼容字段名
        primary_code = primary.get('code') or primary.get('concept', '')
        secondary_code = secondary.get('code') or secondary.get('concept', '')
        
        suggestions.append({
            'action': 'merge',
            'primary_code': primary_code,
            'secondary_code': secondary_code,
            'similarity': dup['similarity'],
            'reason': f"相似度 {dup['similarity']:.1%}，建议合并",
            'combined_frequency': primary.get('frequency', 0) + secondary.get('frequency', 0)
        })
    
    return suggestions

def analyze_code_relationships(codes: List[Dict]) -> Dict:
    """
    分析编码间的关系
    
    Returns:
        关系分析结果
    """
    n = len(codes)
    similarity_matrix = np.zeros((n, n))
    
    # 计算相似度矩阵
    for i in range(n):
        for j in range(i + 1, n):
            code_i = codes[i].get('code') or codes[i].get('concept', '')
            code_j = codes[j].get('code') or codes[j].get('concept', '')
            if not code_i or not code_j:
                continue
            sim = calculate_similarity(code_i, code_j)
            similarity_matrix[i][j] = sim
            similarity_matrix[j][i] = sim
    
    # 找出每个编码最相关的编码
    relationships = []
    for i in range(n):
        related_indices = np.argsort(similarity_matrix[i])[::-1][1:4]  # 前3个相关编码
        related_codes = [
            {
                'code': codes[j].get('code') or codes[j].get('concept', ''),
                'similarity': round(float(similarity_matrix[i][j]), 3)
            }
            for j in related_indices if similarity_matrix[i][j] > 0.3
        ]
        
        if related_codes:
            relationships.append({
                'code': codes[i].get('code') or codes[i].get('concept', ''),
                'related_codes': related_codes
            })
    
    return {
        'similarity_matrix': similarity_matrix.tolist(),
        'relationships': relationships
    }

def main():
    parser = argparse.ArgumentParser(
        description='编码持续比较工具 - 开放编码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python compare_codes.py --input codes.json --output comparison.json
  python compare_codes.py -i codes.json -o result.json --threshold 0.75
        """
    )
    parser.add_argument('--input', '-i', required=True, help='输入的编码JSON文件')
    parser.add_argument('--output', '-o', default='comparison.json', help='输出JSON文件')
    parser.add_argument('--threshold', '-t', type=float, default=0.8, help='相似度阈值（默认：0.8）')
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
        
        if len(codes) < 2:
            logging.error("编码数量不足（至少需要2个）")
            sys.exit(3)
        
        logging.info(f"✓ 读取编码: {len(codes)} 个")
        
        # 执行比较分析
        duplicates = identify_duplicates(codes, args.threshold)
        suggestions = suggest_merges(codes, duplicates)
        relationships = analyze_code_relationships(codes)
        
        processing_time = time.time() - start_time
        
        # 构建输出
        output = {
            'summary': {
                'total_codes': len(codes),
                'duplicate_pairs': len(duplicates),
                'merge_suggestions': len(suggestions),
                'similarity_threshold': args.threshold,
                'processing_time': round(processing_time, 2)
            },
            'details': {
                'duplicates': duplicates,
                'merge_suggestions': suggestions,
                'relationships': relationships['relationships'][:20]  # 前20个关系
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
        
        logging.info(f"✅ 比较分析完成")
        logging.info(f"   编码总数: {len(codes)}")
        logging.info(f"   重复对数: {len(duplicates)}")
        logging.info(f"   合并建议: {len(suggestions)}")
        logging.info(f"📄 详细结果: {args.output}")
        
    except Exception as e:
        logging.error(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(99)

if __name__ == "__main__":
    main()
