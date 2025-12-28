#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
literature-expert 集成示例代码

展示文献智能体如何协调调用 pubscholar-auto-search 和 arxiv-paper-search 技能

作者: socienceAI.com
版本: 1.0.0
日期: 2025-12-28
"""

import sys
from pathlib import Path

# 添加技能路径 - 修复导入路径问题
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# 添加各个技能的scripts目录到路径
pubscholar_scripts = project_root / 'skills' / 'pubscholar-auto-search' / 'scripts'
arxiv_scripts = project_root / 'skills' / 'arxiv-paper-search' / 'scripts'

if pubscholar_scripts.exists():
    sys.path.insert(0, str(pubscholar_scripts))
if arxiv_scripts.exists():
    sys.path.insert(0, str(arxiv_scripts))


class LiteratureExpertIntegrator:
    """
    文献智能体集成器

    功能：
    1. 自动识别用户需求（语言、平台、数量）
    2. 调用合适的检索技能
    3. 整合中英文文献结果
    4. 提供综合分析报告
    """

    def __init__(self, debug=False):
        self.debug = debug

    def detect_language(self, query):
        """
        检测查询语言

        Args:
            query: 用户查询字符串

        Returns:
            'chinese', 'english', 或 'both'
        """
        # 中文检测
        chinese_chars = sum(1 for c in query if '\u4e00' <= c <= '\u9fff')
        total_chars = len(query)

        # 英文检测
        english_words = sum(1 for word in query.split() if word.isalpha() and word.isascii())

        if chinese_chars > 0 and english_words > 0:
            return 'both'
        elif chinese_chars > 0:
            return 'chinese'
        else:
            return 'english'

    def detect_platform(self, query):
        """
        检测用户指定的平台

        Args:
            query: 用户查询字符串

        Returns:
            'pubscholar', 'arxiv', 或 None
        """
        query_lower = query.lower()

        if 'pubscholar' in query_lower or '公益学术平台' in query:
            return 'pubscholar'
        elif 'arxiv' in query_lower:
            return 'arxiv'
        else:
            return None

    def parse_quantity(self, query):
        """
        解析用户需要的文献数量

        Args:
            query: 用户查询字符串

        Returns:
            整数数量（10/20/50/100）或默认值20
        """
        # 数量关键词映射
        quantity_keywords = {
            '10': 10, '十': 10,
            '20': 20, '二十': 20,
            '50': 50, '五十': 50,
            '100': 100, '一百': 100
        }

        for keyword, value in quantity_keywords.items():
            if keyword in query:
                return value

        # 默认值
        return 20

    def search_papers(self, query, max_results=20, language='auto'):
        """
        智能文献检索主入口

        Args:
            query: 搜索关键词
            max_results: 最大结果数
            language: 语言('chinese', 'english', 'both', 'auto')

        Returns:
            检索结果字典
        """
        # 自动检测语言
        if language == 'auto':
            language = self.detect_language(query)

        # 检测平台
        platform = self.detect_platform(query)

        results = {
            'query': query,
            'language': language,
            'platform': platform,
            'chinese_papers': [],
            'english_papers': [],
            'total': 0
        }

        # 根据检测调用对应技能
        if platform == 'pubscholar' or language in ['chinese', 'both']:
            if self.debug:
                print(f"[检索] 中文文献: {query}")

            cn_results = self._search_chinese(query, max_results)
            results['chinese_papers'] = cn_results
            results['total'] += len(cn_results)

        if platform == 'arxiv' or language in ['english', 'both']:
            if self.debug:
                print(f"[检索] 英文文献: {query}")

            en_results = self._search_english(query, max_results)
            results['english_papers'] = en_results
            results['total'] += len(en_results)

        return results

    def _search_chinese(self, query, max_results):
        """调用中文检索技能"""
        try:
            from pubscholar_searcher import SynchronousPubScholarSearcher

            searcher = SynchronousPubScholarSearcher(debug=self.debug)
            results = searcher.search(query, max_results=max_results, auto_expand=True)

            return results

        except ImportError as e:
            print(f"[错误] 无法导入中文检索技能: {e}")
            return []
        except Exception as e:
            print(f"[错误] 中文检索失败: {e}")
            return []

    def _search_english(self, query, max_results):
        """调用英文检索技能"""
        try:
            from arxiv_searcher import ArxivPaperSearcher

            searcher = ArxivPaperSearcher(debug=self.debug)
            results = searcher.search(query, max_results=max_results)

            return results

        except ImportError as e:
            print(f"[错误] 无法导入英文检索技能: {e}")
            return []
        except Exception as e:
            print(f"[错误] 英文检索失败: {e}")
            return []

    def generate_report(self, results):
        """
        生成综合检索报告

        Args:
            results: search_papers()返回的结果字典

        Returns:
            格式化的报告字符串
        """
        report = []
        report.append("=" * 60)
        report.append("文献检索报告")
        report.append("=" * 60)
        report.append(f"\n查询关键词: {results['query']}")
        report.append(f"语言类型: {results['language']}")
        report.append(f"平台指定: {results['platform'] or '未指定'}")
        report.append(f"\n检索统计:")
        report.append(f"  中文文献: {len(results['chinese_papers'])} 篇")
        report.append(f"  英文文献: {len(results['english_papers'])} 篇")
        report.append(f"  总计: {results['total']} 篇")

        # 中文文献列表
        if results['chinese_papers']:
            report.append("\n" + "-" * 60)
            report.append("中文文献列表:")
            report.append("-" * 60)
            for i, paper in enumerate(results['chinese_papers'][:5], 1):
                report.append(f"\n{i}. {paper['title']}")
                report.append(f"   作者: {', '.join(paper['authors'][:3])}")
                report.append(f"   期刊: {paper['journal']}")

            if len(results['chinese_papers']) > 5:
                report.append(f"\n... 还有 {len(results['chinese_papers']) - 5} 篇")

        # 英文文献列表
        if results['english_papers']:
            report.append("\n" + "-" * 60)
            report.append("英文文献列表:")
            report.append("-" * 60)
            for i, paper in enumerate(results['english_papers'][:5], 1):
                report.append(f"\n{i}. {paper['title']}")
                report.append(f"   作者: {', '.join(paper['authors'][:3])}")
                report.append(f"   arXiv: {paper['arxiv_id']}")

            if len(results['english_papers']) > 5:
                report.append(f"\n... 还有 {len(results['english_papers']) - 5} 篇")

        report.append("\n" + "=" * 60)

        return "\n".join(report)


def demo_scenario_1_chinese_only():
    """场景1: 纯中文文献检索"""
    print("\n[场景1] 用户: '搜索关于数字鸿沟的中文论文，需要20篇'\n")

    integrator = LiteratureExpertIntegrator(debug=True)
    results = integrator.search_papers(
        query="数字鸿沟",
        max_results=20,
        language='chinese'
    )

    report = integrator.generate_report(results)
    print(report)


def demo_scenario_2_english_only():
    """场景2: 纯英文文献检索"""
    print("\n[场景2] 用户: '在arXiv搜索transformer architecture，要50篇'\n")

    integrator = LiteratureExpertIntegrator(debug=True)
    results = integrator.search_papers(
        query="transformer architecture",
        max_results=50,
        language='english'
    )

    report = integrator.generate_report(results)
    print(report)


def demo_scenario_3_both_languages():
    """场景3: 中英文综合检索"""
    print("\n[场景3] 用户: '帮我找关于社会网络分析的文献'\n")

    integrator = LiteratureExpertIntegrator(debug=True)
    results = integrator.search_papers(
        query="社会网络分析",
        max_results=30,
        language='both'
    )

    report = integrator.generate_report(results)
    print(report)


def demo_scenario_4_auto_detect():
    """场景4: 自动检测语言"""
    print("\n[场景4] 用户: '搜索人工智能教育相关研究'\n")

    integrator = LiteratureExpertIntegrator(debug=True)

    # 自动检测语言和平台
    results = integrator.search_papers(
        query="人工智能教育应用",
        max_results=20
    )

    report = integrator.generate_report(results)
    print(report)


def test_integration():
    """测试集成效果"""
    print("\n" + "=" * 60)
    print(" literature-expert 集成测试")
    print("=" * 60)

    # 测试场景1：中文检索
    try:
        print("\n[测试1] 中文文献检索")
        integrator = LiteratureExpertIntegrator(debug=False)

        # 快速测试（只检索5篇）
        results = integrator.search_papers(
            query="人工智能",
            max_results=5,
            language='chinese'
        )

        print(f"  中文文献: {len(results['chinese_papers'])} 篇")
        print(f"  英文文献: {len(results['english_papers'])} 篇")
        print(f"  状态: {'成功' if results['total'] > 0 else '失败'}")

    except Exception as e:
        print(f"  错误: {e}")

    # 测试场景2：英文检索
    try:
        print("\n[测试2] 英文文献检索")
        integrator = LiteratureExpertIntegrator(debug=False)

        # 快速测试（只检索5篇）
        results = integrator.search_papers(
            query="machine learning",
            max_results=5,
            language='english'
        )

        print(f"  中文文献: {len(results['chinese_papers'])} 篇")
        print(f"  英文文献: {len(results['english_papers'])} 篇")
        print(f"  状态: {'成功' if results['total'] > 0 else '失败'}")

    except Exception as e:
        print(f"  错误: {e}")

    print("\n" + "=" * 60)
    print("集成测试完成")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="literature-expert 集成示例")
    parser.add_argument('--demo', type=int, choices=[1, 2, 3, 4],
                       help='运行指定场景演示')
    parser.add_argument('--test', action='store_true',
                       help='运行集成测试')

    args = parser.parse_args()

    if args.test:
        test_integration()
    elif args.demo == 1:
        demo_scenario_1_chinese_only()
    elif args.demo == 2:
        demo_scenario_2_english_only()
    elif args.demo == 3:
        demo_scenario_3_both_languages()
    elif args.demo == 4:
        demo_scenario_4_auto_detect()
    else:
        print("使用方法:")
        print("  python literature_expert_integration.py --test    # 运行测试")
        print("  python literature_expert_integration.py --demo 1  # 场景1")
        print("  python literature_expert_integration.py --demo 2  # 场景2")
        print("  python literature_expert_integration.py --demo 3  # 场景3")
        print("  python literature_expert_integration.py --demo 4  # 场景4")
