#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本预处理脚本 - 开放编码

功能：
- 中文分词（jieba）
- 停用词过滤
- 语义分段

使用方式：
  python preprocess_text.py --input raw.txt --output clean.json
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import jieba
import jieba.posseg as pseg

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# 停用词列表
STOPWORDS = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
    '都', '一', '个', '上', '也', '很', '到', '说', '要', '去',
    '而', '着', '你', '会', '看', '能', '下', '对', '这', '来',
    '他', '时', '地', '们', '出', '于', '为', '子', '中', '与'
}

def tokenize_chinese(text: str, keep_pos: List[str] = None) -> List[str]:
    """
    中文分词
    
    Args:
        text: 输入文本
        keep_pos: 保留的词性列表（默认：名词、动词、形容词）
    
    Returns:
        分词结果列表
    """
    if keep_pos is None:
        keep_pos = ['n', 'v', 'a', 'vn', 'an']  # 名词、动词、形容词
    
    words = pseg.cut(text)
    result = []
    
    for word, flag in words:
        # 保留指定词性且长度>1的词
        if any(flag.startswith(pos) for pos in keep_pos) and len(word) > 1:
            result.append(word)
    
    return result

def remove_stopwords(words: List[str], custom_stopwords: set = None) -> List[str]:
    """
    移除停用词
    
    Args:
        words: 分词列表
        custom_stopwords: 自定义停用词集合
    
    Returns:
        过滤后的词列表
    """
    stopwords = STOPWORDS.copy()
    if custom_stopwords:
        stopwords.update(custom_stopwords)
    
    return [w for w in words if w not in stopwords]

def segment_by_meaning(text: str, max_length: int = 500) -> List[str]:
    """
    按语义分段
    
    Args:
        text: 输入文本
        max_length: 每段最大长度
    
    Returns:
        分段列表
    """
    # 按句号、问号、感叹号分句
    import re
    sentences = re.split(r'[。！？\n]+', text)
    
    segments = []
    current_segment = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        if len(current_segment) + len(sentence) <= max_length:
            current_segment += sentence + "。"
        else:
            if current_segment:
                segments.append(current_segment)
            current_segment = sentence + "。"
    
    if current_segment:
        segments.append(current_segment)
    
    return segments

def preprocess_text(text: str) -> Dict:
    """
    完整的文本预处理流程
    
    Returns:
        预处理结果字典
    """
    # 1. 分段
    segments = segment_by_meaning(text)
    
    # 2. 分词
    all_words = []
    segment_words = []
    
    for seg in segments:
        words = tokenize_chinese(seg)
        words_filtered = remove_stopwords(words)
        all_words.extend(words_filtered)
        segment_words.append({
            'text': seg,
            'words': words_filtered,
            'word_count': len(words_filtered)
        })
    
    # 3. 统计
    from collections import Counter
    word_freq = Counter(all_words)
    
    return {
        'segments': segment_words,
        'total_words': len(all_words),
        'unique_words': len(set(all_words)),
        'word_frequency': dict(word_freq.most_common(50))
    }

def main():
    parser = argparse.ArgumentParser(
        description='文本预处理工具 - 开放编码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python preprocess_text.py --input interview.txt --output clean.json
  python preprocess_text.py -i raw.txt -o processed.json --max-length 300
        """
    )
    parser.add_argument('--input', '-i', required=True, help='输入文本文件')
    parser.add_argument('--output', '-o', default='preprocessed.json', help='输出JSON文件')
    parser.add_argument('--max-length', type=int, default=500, help='每段最大长度（默认：500）')
    args = parser.parse_args()
    
    start_time = time.time()
    
    try:
        # 读取文件
        input_path = Path(args.input)
        if not input_path.exists():
            logging.error(f"文件不存在: {args.input}")
            sys.exit(1)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if not text.strip():
            logging.error("输入文件为空")
            sys.exit(2)
        
        logging.info(f"✓ 读取文件: {args.input} ({len(text)} 字符)")
        
        # 预处理
        result = preprocess_text(text)
        processing_time = time.time() - start_time
        
        # 构建输出
        output = {
            'summary': {
                'total_segments': len(result['segments']),
                'total_words': result['total_words'],
                'unique_words': result['unique_words'],
                'processing_time': round(processing_time, 2)
            },
            'details': result,
            'metadata': {
                'input_file': str(input_path.absolute()),
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            }
        }
        
        # 保存
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        logging.info(f"✅ 预处理完成")
        logging.info(f"   分段数: {len(result['segments'])}")
        logging.info(f"   总词数: {result['total_words']}")
        logging.info(f"   独特词: {result['unique_words']}")
        logging.info(f"📄 详细结果: {args.output}")
        
    except Exception as e:
        logging.error(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(99)

if __name__ == "__main__":
    main()
