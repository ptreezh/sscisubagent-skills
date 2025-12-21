#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开放编码技能自动加载器
为Claude提供快速的数据预处理支持
"""

import jieba
import re
from collections import Counter
from typing import List, Dict, Any

class OpenCodingAutoLoader:
    """开放编码自动处理工具"""

    def __init__(self):
        self.stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
            '都', '一', '个', '上', '也', '很', '到', '说', '要', '去'
        }

    def quick_concept_extract(self, text: str) -> List[Dict[str, Any]]:
        """快速概念提取"""
        # 中文分词
        words = jieba.lcut(text)

        # 过滤停用词和单字
        filtered_words = [
            word for word in words
            if word not in self.stop_words and len(word) > 1
        ]

        # 统计词频
        word_freq = Counter(filtered_words)

        # 提取高频概念
        concepts = []
        for word, freq in word_freq.most_common(20):
            concepts.append({
                'concept': word,
                'frequency': freq,
                'type': self._classify_concept(word)
            })

        return concepts

    def _classify_concept(self, word: str) -> str:
        """简单概念分类"""
        action_patterns = ['寻求', '建立', '适应', '应对', '处理', '解决']
        emotion_patterns = ['感受', '体验', '情绪', '态度']
        relation_patterns = ['关系', '联系', '影响', '作用']

        for pattern in action_patterns:
            if pattern in word:
                return '行动概念'

        for pattern in emotion_patterns:
            if pattern in word:
                return '情感概念'

        for pattern in relation_patterns:
            if pattern in word:
                return '关系概念'

        return '一般概念'

    def generate_coding_suggestions(self, concepts: List[Dict]) -> List[str]:
        """生成编码建议"""
        suggestions = []

        # 按类型分组
        action_concepts = [c for c in concepts if c['type'] == '行动概念']
        emotion_concepts = [c for c in concepts if c['type'] == '情感概念']

        # 生成建议
        if action_concepts:
            suggestions.append(f"重点关注行动概念：{', '.join([c['concept'] for c in action_concepts[:5]])}")

        if emotion_concepts:
            suggestions.append(f"注意情感体验：{', '.join([c['concept'] for c in emotion_concepts[:5]])}")

        # 高频概念
        top_concepts = [c['concept'] for c in concepts[:10]]
        suggestions.append(f"高频概念建议编码：{', '.join(top_concepts)}")

        return suggestions

def main():
    """命令行接口（标准化）"""
    import argparse
    import json
    import sys
    import logging
    from datetime import datetime
    from pathlib import Path
    import time
    
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='开放编码快速概念提取工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python auto_loader.py --input interview.txt --output concepts.json
  python auto_loader.py -i data.txt -o result.json --top 30
        """
    )
    parser.add_argument('--input', '-i', required=True, help='输入的文本文件路径')
    parser.add_argument('--output', '-o', default='concepts.json', help='输出JSON文件路径（默认：concepts.json）')
    parser.add_argument('--top', '-t', type=int, default=20, help='提取的高频概念数量（默认：20）')
    args = parser.parse_args()
    
    # 记录开始时间
    start_time = time.time()
    
    try:
        # 读取输入文件
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
        
        # 处理文本
        loader = OpenCodingAutoLoader()
        concepts = loader.quick_concept_extract(text)
        suggestions = loader.generate_coding_suggestions(concepts)
        
        # 计算处理时间
        processing_time = time.time() - start_time
        
        # 构建标准化输出
        output = {
            'summary': {
                'total_concepts': len(concepts),
                'text_length': len(text),
                'top_concepts': [c['concept'] for c in concepts[:5]],
                'processing_time': round(processing_time, 2)
            },
            'details': {
                'concepts': concepts[:args.top],
                'suggestions': suggestions,
                'concept_types': {
                    '行动概念': len([c for c in concepts if c['type'] == '行动概念']),
                    '情感概念': len([c for c in concepts if c['type'] == '情感概念']),
                    '关系概念': len([c for c in concepts if c['type'] == '关系概念']),
                    '一般概念': len([c for c in concepts if c['type'] == '一般概念'])
                }
            },
            'metadata': {
                'input_file': str(input_path.absolute()),
                'output_file': args.output,
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'skill': 'performing-open-coding'
            }
        }
        
        # 保存JSON输出
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        # 控制台输出摘要
        logging.info(f"✅ 概念提取完成")
        logging.info(f"   识别概念: {len(concepts)} 个")
        logging.info(f"   高频概念: {', '.join([c['concept'] for c in concepts[:5]])}")
        logging.info(f"   处理时间: {processing_time:.2f} 秒")
        logging.info(f"📄 详细结果: {args.output}")
        
    except FileNotFoundError as e:
        logging.error(f"文件未找到: {e}")
        sys.exit(1)
    except PermissionError as e:
        logging.error(f"权限错误: {e}")
        sys.exit(3)
    except Exception as e:
        logging.error(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(99)

if __name__ == "__main__":
    main()