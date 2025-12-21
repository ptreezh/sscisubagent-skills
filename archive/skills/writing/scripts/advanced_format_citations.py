#!/usr/bin/env python3
"""
高级引用处理工具（支持高级依赖包，提供优雅降级）

功能：
1. 识别不同格式的引用
2. 格式化引用为标准格式
3. 验证引用格式
4. 检测重复引用
5. 生成引用统计报告

优先使用高级依赖包（pandas），若不可用则降级到基础实现
"""

import argparse
import json
import sys
import re
import importlib
from datetime import datetime
from typing import Dict, List, Any
from collections import Counter
import subprocess


def check_and_install_package(package_name: str) -> bool:
    """检查并尝试安装包"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        print(f"正在安装 {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            return True
        except subprocess.CalledProcessError:
            print(f"无法安装 {package_name}，将使用降级功能")
            return False


# 检查高级包是否可用
PANDAS_AVAILABLE = check_and_install_package("pandas")


# 高级包导入（如果可用）
if PANDAS_AVAILABLE:
    try:
        import pandas as pd
    except ImportError:
        PANDAS_AVAILABLE = False


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


def validate_citation_basic(citation: str) -> Dict[str, Any]:
    """基础引用验证"""
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


def validate_citation_advanced(citations: List[str]) -> List[Dict[str, Any]]:
    """高级引用验证（使用pandas）"""
    if not PANDAS_AVAILABLE:
        # 降级到基础验证
        return [validate_citation_basic(cit) for cit in citations]
    
    try:
        # 创建DataFrame进行批量处理
        df = pd.DataFrame({'citation': citations})
        
        # 检查年份
        df['has_year'] = df['citation'].apply(lambda x: bool(re.search(r'\\d{4}', x)))
        
        # 检查长度
        df['is_long_enough'] = df['citation'].apply(lambda x: len(x) >= 10)
        
        # 检查作者
        df['has_author'] = df['citation'].apply(lambda x: bool(re.match(r'^([^.,;]+)', x)))
        df['author_valid'] = df['citation'].apply(lambda x: len(re.match(r'^([^.,;]+)', x).group(1).strip().split()) >= 1 if re.match(r'^([^.,;]+)', x) else False)
        
        # 检查标点
        df['has_punctuation'] = df['citation'].apply(lambda x: x.endswith(('.', '?', '!')))
        
        # 生成验证结果
        results = []
        for i, citation in enumerate(citations):
            issues = []
            if not df.iloc[i]['has_year']:
                issues.append("缺少年份")
            if not df.iloc[i]['is_long_enough']:
                issues.append("引用过短，可能不完整")
            if not df.iloc[i]['has_author']:
                issues.append("无法识别作者")
            elif not df.iloc[i]['author_valid']:
                issues.append("作者信息不完整")
            if not df.iloc[i]['has_punctuation']:
                issues.append("缺少结束标点")
            
            results.append({
                'is_valid': len(issues) == 0,
                'issues': issues,
                'format': detect_citation_format(citation)
            })
        
        return results
    except Exception as e:
        print(f"高级引用验证出错，使用降级方案: {e}")
        # 降级到基础验证
        return [validate_citation_basic(cit) for cit in citations]


def detect_duplicate_citations_basic(citations: List[str]) -> List[Dict[str, Any]]:
    """基础重复引用检测"""
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


def detect_duplicate_citations_advanced(citations: List[str]) -> List[Dict[str, Any]]:
    """高级重复引用检测（使用pandas）"""
    if not PANDAS_AVAILABLE:
        # 降级到基础检测
        return detect_duplicate_citations_basic(citations)
    
    try:
        # 使用pandas进行重复检测
        df = pd.DataFrame({'citation': citations})
        df['simple_citation'] = df['citation'].apply(
            lambda x: re.sub(r'[\\s\\.,;:\\[\\]()]', '', x.lower())
        )
        
        # 找到重复项
        duplicated_mask = df['simple_citation'].duplicated(keep='first')
        duplicates = []
        
        for i in df[duplicated_mask].index:
            original_idx = df[df['simple_citation'] == df.iloc[i]['simple_citation']].index[0]
            if original_idx != i:  # 确保不是第一个
                duplicates.append({
                    'original_index': int(i),
                    'duplicate_of': int(original_idx),
                    'citation': citations[i]
                })
        
        return duplicates
    except Exception as e:
        print(f"高级重复检测出错，使用降级方案: {e}")
        # 降级到基础检测
        return detect_duplicate_citations_basic(citations)


def format_citations(citations: List[str], target_format: str = 'GB/T 7714') -> List[str]:
    """格式化引用列表"""
    formatted = []
    
    for citation in citations:
        if target_format == 'GB/T 7714':
            formatted.append(standardize_gb_format(citation))
        elif target_format == 'APA':
            # 暂时返回原格式，实际应用中需要实现转换逻辑
            formatted.append(citation)
        else:
            formatted.append(citation)  # 如果格式不支持，返回原格式
    
    return formatted


def generate_citation_report_basic(citations: List[str]) -> Dict[str, Any]:
    """基础引用报告生成"""
    if not citations:
        return {'error': '没有引用数据'}
    
    # 统计格式分布
    format_counts = Counter(detect_citation_format(cit) for cit in citations)
    
    # 统计长度分布
    lengths = [len(cit) for cit in citations]
    avg_length = sum(lengths) / len(lengths) if lengths else 0
    
    # 验证结果
    validation_results = [validate_citation_basic(cit) for cit in citations]
    valid_count = sum(1 for v in validation_results if v['is_valid'])
    
    return {
        'total_citations': len(citations),
        'valid_citations': valid_count,
        'invalid_citations': len(citations) - valid_count,
        'format_distribution': dict(format_counts),
        'average_length': avg_length,
        'length_range': (min(lengths) if lengths else 0, max(lengths) if lengths else 0)
    }


def generate_citation_report_advanced(citations: List[str]) -> Dict[str, Any]:
    """高级引用报告生成（使用pandas）"""
    if not PANDAS_AVAILABLE:
        # 降级到基础报告
        return generate_citation_report_basic(citations)
    
    try:
        # 使用pandas进行数据分析
        df = pd.DataFrame({'citation': citations})
        
        # 检测格式
        df['format'] = df['citation'].apply(detect_citation_format)
        
        # 统计格式分布
        format_counts = df['format'].value_counts().to_dict()
        
        # 计算长度
        df['length'] = df['citation'].apply(len)
        avg_length = df['length'].mean()
        length_range = (df['length'].min(), df['length'].max())
        
        # 验证引用
        validation_results = validate_citation_advanced(citations)
        df['is_valid'] = [v['is_valid'] for v in validation_results]
        valid_count = df['is_valid'].sum()
        
        # 更多统计信息
        length_stats = {
            'mean': float(df['length'].mean()),
            'median': float(df['length'].median()),
            'std': float(df['length'].std()),
            'min': int(df['length'].min()),
            'max': int(df['length'].max())
        }
        
        return {
            'total_citations': len(citations),
            'valid_citations': int(valid_count),
            'invalid_citations': len(citations) - int(valid_count),
            'format_distribution': format_counts,
            'average_length': float(avg_length),
            'length_range': (int(length_range[0]), int(length_range[1])),
            'length_statistics': length_stats,
            'using_advanced': True
        }
    except Exception as e:
        print(f"高级报告生成出错，使用降级方案: {e}")
        # 降级到基础报告
        return generate_citation_report_basic(citations)


def main():
    parser = argparse.ArgumentParser(
        description='高级引用处理工具（支持高级依赖包，提供优雅降级）',
        epilog='示例：python advanced_format_citations.py --input citations.json --output formatted.json --format GB'
    )
    parser.add_argument('--input', '-i', required=True, help='输入引用文件（JSON）')
    parser.add_argument('--output', '-o', default='formatted_citations.json', help='输出文件')
    parser.add_argument('--format', '-f', default='GB/T 7714', 
                       choices=['GB/T 7714', 'APA', 'MLA', 'Chicago', 'none'],
                       help='目标格式')
    parser.add_argument('--action', '-a', default='all',
                       choices=['format', 'validate', 'detect_duplicates', 'report', 'all'],
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

    # 检查可用包
    available_packages = {
        'pandas': PANDAS_AVAILABLE
    }

    if args.action in ['format', 'all']:
        # 格式化引用
        if args.format != 'none':
            formatted_citations = format_citations(citations, args.format)
            results['formatted_citations'] = formatted_citations
        else:
            results['formatted_citations'] = citations

    if args.action in ['validate', 'all']:
        # 验证引用
        validation_results = validate_citation_advanced(citations)
        results['validation_results'] = validation_results

    if args.action in ['detect_duplicates', 'all']:
        # 检测重复引用
        duplicates = detect_duplicate_citations_advanced(citations)
        results['duplicates'] = duplicates

    if args.action in ['report', 'all']:
        # 生成引用报告
        report = generate_citation_report_advanced(citations)
        results['report'] = report

    # 统计信息
    results['statistics'] = {
        'total_citations': len(citations),
        'unique_formats': list(set(detect_citation_format(cit) for cit in citations)),
        'duplicates_count': len(results.get('duplicates', [])),
        'valid_citations_count': sum(1 for v in results.get('validation_results', []) if v.get('is_valid', True)),
        'available_packages': available_packages
    }

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'total_citations': len(citations),
            'action_performed': args.action,
            'target_format': args.format,
            'using_advanced': PANDAS_AVAILABLE,
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
    print(f"  - 使用高级分析: {PANDAS_AVAILABLE}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()