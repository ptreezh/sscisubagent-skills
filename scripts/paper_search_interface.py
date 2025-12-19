#!/usr/bin/env python3
"""
免费论文搜索接口
实现渐进式信息披露和最小认知负荷设计
"""

import sys
import json
from typing import Dict, List
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from tools.paper_search_tools import VerifiedPaperSearcher

class PaperSearchInterface:
    """渐进式信息披露的论文搜索接口"""

    def __init__(self):
        self.searcher = VerifiedPaperSearcher()
        self.current_results = None
        self.selected_papers = []

    def execute_search(self, query: str, max_results: int = 10) -> Dict:
        """
        执行搜索 - 工具化思维
        返回渐进式显示的结构化信息
        """

        print(f"🔍 搜索免费论文: {query}")

        # 执行搜索（工具执行）
        results = self.searcher.search_papers(query, max_results)
        self.current_results = results

        # 渐进式信息披露 - 第1层：概览
        overview = {
            'status': 'success',
            'total_found': results['total_downloadable'],
            'summary': self.searcher.get_search_summary(results),
            'sources': self._get_source_breakdown(results),
            'search_time': f"{results['search_time']:.1f}s"
        }

        return overview

    def get_paper_list(self, limit: int = 5) -> List[Dict]:
        """
        获取论文列表 - 第2层信息
        最小认知负荷：只显示必要信息
        """
        if not self.current_results:
            return []

        all_papers = self.current_results['arxiv_results'] + self.current_results['institutional_results']

        # 结构化简化信息
        simplified_papers = []
        for i, paper in enumerate(all_papers[:limit], 1):
            simplified_papers.append({
                'id': i,
                'title': paper['title'][:80] + '...' if len(paper['title']) > 80 else paper['title'],
                'source': paper['source'],
                'confidence': paper['confidence'],
                'file_size': paper['file_size'],
                'downloadable': True
            })

        return simplified_papers

    def get_paper_details(self, paper_id: int) -> Dict:
        """
        获取论文详细信息 - 第3层信息
        按需加载详细信息
        """
        if not self.current_results:
            return {'error': 'No search results available'}

        all_papers = self.current_results['arxiv_results'] + self.current_results['institutional_results']

        if 1 <= paper_id <= len(all_papers):
            paper = all_papers[paper_id - 1]

            # 添加下载建议（AI解释）
            download_advice = self._generate_download_advice(paper)

            return {
                'paper_info': paper,
                'download_advice': download_advice,
                'citation_suggestion': self._generate_citation_suggestion(paper)
            }
        else:
            return {'error': 'Invalid paper ID'}

    def download_selected_paper(self, paper_id: int) -> Dict:
        """下载选定的论文"""
        if not self.current_results:
            return {'success': False, 'error': 'No search results available'}

        all_papers = self.current_results['arxiv_results'] + self.current_results['institutional_results']

        if 1 <= paper_id <= len(all_papers):
            paper = all_papers[paper_id - 1]

            print(f"📥 开始下载: {paper['title'][:50]}...")
            filepath = self.searcher.download_paper(paper)

            if filepath:
                return {
                    'success': True,
                    'filepath': filepath,
                    'title': paper['title'],
                    'size': paper['file_size']
                }
            else:
                return {
                    'success': False,
                    'error': 'Download failed'
                }
        else:
            return {'success': False, 'error': 'Invalid paper ID'}

    def _get_source_breakdown(self, results: Dict) -> Dict:
        """获取来源分布 - 定量分析"""
        arxiv_count = len(results['arxiv_results'])
        inst_count = len(results['institutional_results'])

        return {
            'arxiv': {
                'count': arxiv_count,
                'reliability': '100%',
                'description': '预印本论文，完全免费'
            },
            'institutional': {
                'count': inst_count,
                'reliability': '已验证',
                'description': '机构发布的研究报告'
            }
        }

    def _generate_download_advice(self, paper: Dict) -> str:
        """生成下载建议 - AI解释和决策"""
        if paper['source'] == 'arXiv':
            return (
                "arXiv论文是预印本，完全免费且合法下载。"
                f"文件大小约{paper['file_size']}。"
                "注意这是未正式发表的版本，引用时请标注为预印本。"
            )
        else:
            return (
                f"来自{paper['source']}的机构研究报告，已验证可下载。"
                "通常质量较高，但可能需要特殊引用格式。"
            )

    def _generate_citation_suggestion(self, paper: Dict) -> str:
        """生成引用建议 - 工具化输出"""
        if paper['source'] == 'arXiv':
            # 简化的arXiv引用格式
            authors = paper['authors'][:3]
            if len(paper['authors']) > 3:
                authors.append('et al.')
            return f"{' '.join(authors)}. {paper['title']}. arXiv preprint. {paper['published']}."
        else:
            return f"Consult standard citation format for institutional reports. Source: {paper['source']}."

def interactive_demo():
    """交互式演示 - 展示渐进式信息披露"""
    interface = PaperSearchInterface()

    print("=== 免费论文搜索演示 ===\n")

    # 第1步：搜索
    query = "machine learning"
    overview = interface.execute_search(query, max_results=5)

    print("📊 搜索概览:")
    print(json.dumps(overview, indent=2, ensure_ascii=False))
    print()

    # 第2步：显示论文列表
    paper_list = interface.get_paper_list(limit=3)
    print("📋 论文列表:")
    for paper in paper_list:
        print(f"{paper['id']}. {paper['title']} ({paper['source']}, {paper['file_size']})")
    print()

    # 第3步：获取详细信息（按需）
    if paper_list:
        print("📖 选择论文 1 查看详情...")
        details = interface.get_paper_details(1)
        print("详细信息:")
        print(f"标题: {details['paper_info']['title']}")
        print(f"下载建议: {details['download_advice']}")
        print(f"引用建议: {details['citation_suggestion']}")
        print()

        # 第4步：下载（可选）
        print("📥 尝试下载论文 1...")
        download_result = interface.download_selected_paper(1)
        if download_result['success']:
            print(f"✅ 下载成功: {download_result['filepath']}")
        else:
            print(f"❌ 下载失败: {download_result['error']}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        query = sys.argv[1]
        max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5

        interface = PaperSearchInterface()
        overview = interface.execute_search(query, max_results)
        paper_list = interface.get_paper_list()

        print(json.dumps({
            'overview': overview,
            'papers': paper_list
        }, indent=2, ensure_ascii=False))
    else:
        # 交互式演示
        interactive_demo()