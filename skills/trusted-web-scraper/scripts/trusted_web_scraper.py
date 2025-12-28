#!/usr/bin/env python3
"""
可信网站爬虫工具 - 专门用于爬取可信网站（企业官网、教育网、政务网）信息

此脚本提供安全、合规的网络数据收集功能，确保数据来源的可靠性和权威性。
"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any

# 导入内部模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))
from core_trusted_scraper import trusted_web_scraper as skill_function


def main():
    parser = argparse.ArgumentParser(
        description='可信网站爬虫工具（专门用于爬取企业官网、教育网、政务网信息）',
        epilog='示例：python trusted_web_scraper.py --url https://example.com --output results.json --content-type text'
    )
    parser.add_argument('--url', '-u', required=True, help='目标网站URL')
    parser.add_argument('--output', '-o', default='trusted_scraping_results.json', help='输出文件')
    parser.add_argument('--content-type', '-ct', 
                       choices=['text', 'tables', 'images', 'documents', 'all'],
                       default='text',
                       help='要提取的内容类型')
    parser.add_argument('--data-fields', '-df', nargs='+', default=[],
                       help='指定要提取的数据字段')
    parser.add_argument('--verification-level', '-vl',
                       choices=['basic', 'standard', 'thorough'],
                       default='standard',
                       help='验证级别')
    parser.add_argument('--rate-limit', '-rl', type=int, default=10,
                       help='请求频率限制（每分钟请求数，默认10）')
    parser.add_argument('--timeout', '-t', type=int, default=30,
                       help='请求超时时间（秒，默认30）')
    parser.add_argument('--retry-attempts', '-ra', type=int, default=3,
                       help='重试次数（默认3次）')
    parser.add_argument('--output-format', '-of',
                       choices=['json', 'csv', 'markdown'],
                       default='json',
                       help='输出格式')
    
    args = parser.parse_args()

    start_time = datetime.now()

    # 准备输入数据
    input_data = {
        'url': args.url,
        'content_type': args.content_type,
        'data_fields': args.data_fields,
        'verification_level': args.verification_level,
        'rate_limit': args.rate_limit,
        'timeout': args.timeout,
        'retry_attempts': args.retry_attempts,
        'output_format': args.output_format
    }

    try:
        # 执行可信网站爬虫
        results = skill_function(input_data)
    except Exception as e:
        print(f"错误：爬取过程中发生异常 - {e}", file=sys.stderr)
        sys.exit(1)

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'url': args.url,
            'status_code': results.get('summary', {}).get('status_code', 'N/A'),
            'trust_level': results.get('summary', {}).get('trust_level', 'N/A'),
            'content_extracted': results.get('summary', {}).get('content_extracted', 0),
            'processing_time': round((end_time - start_time).total_seconds(), 2),
            'verification_level': args.verification_level
        },
        'details': results,
        'metadata': {
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'trusted-web-scraper'
        }
    }

    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ 可信网站爬取完成")
    print(f"  - URL: {args.url}")
    print(f"  - 信任级别: {output['summary']['trust_level']}")
    print(f"  - 提取内容数: {output['summary']['content_extracted']}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()