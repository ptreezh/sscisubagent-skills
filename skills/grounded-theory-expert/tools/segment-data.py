"""
数据分段工具
将文本按意义单元分段
"""

import re
from typing import List, Dict


def segment_by_paragraph(text: str) -> List[Dict]:
    """
    按段落分段
    
    参数:
        text: 原始文本
    
    返回:
        分段列表, 每段包含 id, content, length
    """
    # 按空行分段
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    segments = []
    for i, para in enumerate(paragraphs, 1):
        # 如果段落太长, 进一步细分
        if len(para) > 500:
            sub_segments = segment_by_sentence(para, i)
            segments.extend(sub_segments)
        else:
            segments.append({
                'id': i,
                'content': para,
                'length': len(para)
            })
    
    return segments


def segment_by_sentence(text: str, start_id: int = 1) -> List[Dict]:
    """
    按句子分段
    
    参数:
        text: 原始文本
        start_id: 起始 ID
    
    返回:
        分段列表
    """
    # 中文句子分割(句号、问号、感叹号)
    sentences = re.split(r'[. !？.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    segments = []
    for i, sentence in enumerate(sentences, start_id):
        segments.append({
            'id': i,
            'content': sentence,
            'length': len(sentence)
        })
    
    return segments


def segment_text(text: str, mode: str = 'paragraph') -> Dict:
    """
    分段主函数
    
    参数:
        text: 原始文本
        mode: 分段模式 ('paragraph' | 'sentence' | 'mixed')
    
    返回:
        分段结果和统计信息
    """
    if mode == 'paragraph':
        segments = segment_by_paragraph(text)
    elif mode == 'sentence':
        segments = segment_by_sentence(text)
    elif mode == 'mixed':
        # 混合模式：先按段落, 太长的段落按句子
        segments = segment_by_paragraph(text)
    else:
        raise ValueError(f"Unknown mode: {mode}")
    
    # 创建索引
    index = {seg['id']: seg['content'][:50] + '...' if len(seg['content']) > 50 else seg['content'] 
             for seg in segments}
    
    return {
        'segments': segments,
        'total_segments': len(segments),
        'average_length': sum(s['length'] for s in segments) / len(segments) if segments else 0,
        'index': index,
        'status': 'success'
    }


def segment_file(input_file: str, output_file: str, mode: str = 'paragraph') -> Dict:
    """
    分段文件
    
    参数:
        input_file: 输入文件路径
        output_file: 输出文件路径
        mode: 分段模式
    
    返回:
        分段结果
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    result = segment_text(text, mode)
    
    # 保存分段结果
    with open(output_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) >= 3:
        result = segment_file(sys.argv[1], sys.argv[2])
        print(f"分段完成：共{result['total_segments']}段, 平均长度{result['average_length']:.1f}字")
    else:
        # 测试
        test_text = """这是第一段。这是一个很长的段落, 包含多个句子。这是第二个句子。这是第三个句子。

这是第二段。比较短.

这是第三段."""
        
        result = segment_text(test_text, mode='mixed')
        print(f"分段结果：{result['total_segments']}段")
        for seg in result['segments']:
            print(f"  [{seg['id']}] {seg['content'][:30]}... ({seg['length']}字)")
