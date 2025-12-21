#!/usr/bin/env python3
"""
引用处理工具

功能：
1. 识别不同格式的引用
2. 格式化引用为标准格式
3. 验证引用格式
4. 检测重复引用

标准化接口：argparse + 三层JSON输出
不依赖额外的引用管理包
"""

import argparse
import json
import sys
import re
from datetime import datetime
from typing import Dict, List, Any
from collections import Counter


def detect_citation_format(citation: str) -> str:
    """检测引用格式"""
    citation = citation.strip()
    
    # 定义各种格式的正则模式
    formats = {
        'GB/T 7714': [
            r'.*\\.\s*\\(\\d{4}\\)\\..*\\[J\\]\\..*',  # 期刊文章格式
            r'.*\\.\s*\\(\\d{4}\\)\\..*\\[M\\]\\..*',   # 图书格式
            r'.*\\.\s*\\(\\d{4}\\)\\..*\\[D\\]\\..*',   # 学位论文格式
        ],
        'APA': [
            r'.*,\\s*\\(\\d{4}\\)\\..*',
            r'.*\\s*\\(\\d{4}\\)\\..*',
        ],
        'MLA': [
            r'.*,\\s*vol\\.\\s*\\d+,\\s*no\\.\\s*\\d+,\\s*\\d{4},\\s*pp\\.\\s*\\d+-\\d+',
        ],
        'mixed': [
            r'.*\\[文献类型\\].*',
        ]
    }
    
    for format_name, patterns in formats.items():
        for pattern in patterns:
            if re.search(pattern, citation, re.IGNORECASE):
                return format_name
    
    return 'unknown'


def standardize_gb_format(citation: str) -> str:
    """将引用标准化为GB/T 7714格式"""
    # 这是一个简化的GB格式标准化函数
    # 实际应用中可能需要更复杂的处理逻辑
    
    # 提取作者
    author_match = re.match(r'^([^.,;]+)', citation)
    authors = author_match.group(1).strip() if author_match else ""
    
    # 提取年份
    year_match = re.search(r'\\((\\d{4})\\)', citation) or re.search(r'(\\d{4})', citation)
    year = year_match.group(1) if year_match else "n.d."
    
    # 提取标题
    title_match = re.search(r'[).]([^.,;]+)', citation)
    title = title_match.group(1).strip() if title_match else "Title"
    
    # 提取期刊名
    journal_match = re.search(r'[JMD]\\].*?,\\s*([^,，]+)', citation)
    journal = journal_match.group(1).strip() if journal_match else "Journal"
    
    # 提取卷期页码
    vol_issue_match = re.search(r',\\s*(\\d+)\\s*\\((\\d+)\\)\\s*:\\s*(\\d+-?\\d*)', citation)
    if vol_issue_match:
        vol, issue, pages = vol_issue_match.groups()
        return f"{authors}. {year}. {title}[J]. {journal}, {vol}({issue}): {pages}."
    else:
        return f"{authors}. {year}. {title}[J]. {journal}."


def standardize_apa_format(citation: str) -> str:
    """将引用标准化为APA格式"""
    # 简化的APA格式标准化函数
    return citation  # 暂时返回原格式，实际应用中需要实现转换逻辑


def validate_citation(citation: str) -> Dict[str, Any]:
    """验证引用格式"""
    issues = []
    
    # 检查是否包含必要元素
    if not re.search(r'\\d{4}', citation):  # 检查年份
        issues.append("缺少年份")
    
    if len(citation) < 10:  # 检查长度
        issues.append("引用过短，可能不完整")
    
    # 检查作者格式
    author_pattern = r'^([^.,;]+)'
    author_match = re.match(author_pattern, citation)
    if not author_match:
        issues.append("无法识别作者")
    else:
        author = author_match.group(1).strip()
        if len(author.split()) < 1:
            issues.append("作者信息不完整")
    
    # 检查标点符号
    if not citation.endswith(('.', '?', '!')):
        issues.append("缺少结束标点")
    
    return {
        'is_valid': len(issues) == 0,
        'issues': issues,
        'format': detect_citation_format(citation)
    }


def detect_duplicate_citations(citations: List[str]) -> List[Dict[str, Any]]:
    """检测重复引用"""
    duplicates = []
    seen = {}
    
    for i, citation in enumerate(citations):
        # 创建一个简化的引用标识符，忽略标点和大小写
        simple_citation = re.sub(r'[\\s\\.,;:\\[\\]()]', '', citation.lower())
        
        if simple_citation in seen:
            duplicates.append({
                'original_index': i,
                'duplicate_of': seen[simple_citation],
                'citation': citation
            })
        else:
            seen[simple_citation] = i
    
    return duplicates


def format_citations(citations: List[str], target_format: str = 'GB/T 7714') -> List[str]:
    """格式化引用列表"""
    formatted = []
    
    for citation in citations:
        if target_format == 'GB/T 7714':
            formatted.append(standardize_gb_format(citation))
        elif target_format == 'APA':
            formatted.append(standardize_apa_format(citation))
        else:
            formatted.append(citation)  # 如果格式不支持，返回原格式
    
    return formatted


def main():
    parser = argparse.ArgumentParser(
        description='引用处理工具（不依赖额外引用管理包）',
        epilog='示例：python format_citations.py --input citations.json --output formatted.json --format GB'
    )
    parser.add_argument('--input', '-i', required=True, help='输入引用文件（JSON）')
    parser.add_argument('--output', '-o', default='formatted_citations.json', help='输出文件')
    parser.add_argument('--format', '-f', default='GB/T 7714', 
                       choices=['GB/T 7714', 'APA', 'MLA', 'Chicago', 'none'],
                       help='目标格式')
    parser.add_argument('--action', '-a', default='format',
                       choices=['format', 'validate', 'detect_duplicates', 'all'],
                       help='执行的操作')
    
    args = parser.parse_args()

    # 读取输入数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)

    start_time = datetime.now()

    # 提取引用列表
    if isinstance(data, dict):
        if 'citations' in data:
            citations = data['citations']
        else:
            citations = [data]  # 如果整个对象是一个引用
    elif isinstance(data, list):
        citations = data
    else:
        citations = [str(data)]

    results = {}

    if args.action in ['format', 'all']:
        # 格式化引用
        if args.format != 'none':
            formatted_citations = format_citations(citations, args.format)
            results['formatted_citations'] = formatted_citations
        else:
            results['formatted_citations'] = citations

    if args.action in ['validate', 'all']:
        # 验证引用
        validation_results = []
        for citation in citations:
            validation_results.append({
                'citation': citation,
                'validation': validate_citation(citation)
            })
        results['validation_results'] = validation_results

    if args.action in ['detect_duplicates', 'all']:
        # 检测重复引用
        duplicates = detect_duplicate_citations(citations)
        results['duplicates'] = duplicates

    # 统计信息
    results['statistics'] = {
        'total_citations': len(citations),
        'unique_formats': list(set(detect_citation_format(cit) for cit in citations)),
        'duplicates_count': len(results.get('duplicates', []))
    }

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'total_citations': len(citations),
            'action_performed': args.action,
            'target_format': args.format,
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': results,
        'metadata': {
            'input_file': args.input,
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'processing-citations'
        }
    }

    # 保存输出
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ 引用处理完成")
    print(f"  - 总引用数: {len(citations)}")
    print(f"  - 执行操作: {args.action}")
    print(f"  - 目标格式: {args.format}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()