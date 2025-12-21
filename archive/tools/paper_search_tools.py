#!/usr/bin/env python3
"""
免费学术论文搜索工具集
基于真实测试验证的可搜索方法
遵循工具化思维原则
"""

import arxiv
import requests
import os
import time
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import re

class VerifiedPaperSearcher:
    """基于真实验证的论文搜索器"""

    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = download_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # 确保下载目录存在
        os.makedirs(download_dir, exist_ok=True)

    def search_papers(self, query: str, max_results: int = 10) -> Dict:
        """
        主搜索函数 - 工具化思维
        返回结构化结果供AI决策
        """
        results = {
            'query': query,
            'arxiv_results': [],
            'institutional_results': [],
            'total_downloadable': 0,
            'search_time': time.time()
        }

        # 第1步：arXiv搜索（最高优先级）
        print(f"搜索arXiv: {query}")
        arxiv_results = self._search_arxiv(query, max_results // 2)
        results['arxiv_results'] = arxiv_results

        # 第2步：机构资源搜索（补充）
        if len(arxiv_results) < max_results:
            print("搜索机构资源...")
            institutional_results = self._search_institutional(query, max_results - len(arxiv_results))
            results['institutional_results'] = institutional_results

        # 第3步：统计可下载数量
        all_results = arxiv_results + results['institutional_results']
        results['total_downloadable'] = len(all_results)
        results['search_time'] = time.time() - results['search_time']

        return results

    def _search_arxiv(self, query: str, max_results: int) -> List[Dict]:
        """arXiv搜索 - 100%验证可用"""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            results = []
            for paper in search.results():
                # 验证PDF可下载性
                if self._verify_pdf_downloadable(paper.pdf_url):
                    # 估算文件大小
                    file_size = self._get_file_size(paper.pdf_url)

                    results.append({
                        'title': paper.title,
                        'authors': [author.name for author in paper.authors],
                        'abstract': paper.summary[:500] + '...' if len(paper.summary) > 500 else paper.summary,
                        'pdf_url': paper.pdf_url,
                        'source': 'arXiv',
                        'confidence': 'High',
                        'file_size': file_size,
                        'published': paper.published.strftime('%Y-%m-%d') if paper.published else 'Unknown'
                    })

            print(f"arXiv找到 {len(results)} 篇可下载论文")
            return results

        except Exception as e:
            print(f"arXiv搜索失败: {e}")
            return []

    def _search_institutional(self, query: str, max_results: int) -> List[Dict]:
        """机构资源搜索 - 仅搜索已验证的机构"""
        verified_institutions = [
            {
                'name': 'MIT DSpace',
                'base_url': 'https://dspace.mit.edu',
                'search_url': f'https://dspace.mit.edu/simple-search?query={query}',
                'pdf_pattern': r'dspace\.mit\.edu/bitstream/[^"\\s]+\.pdf',
                'confidence': 'Medium'
            }
        ]

        results = []
        for institution in verified_institutions:
            try:
                papers = self._search_single_institution(institution, max_results // len(verified_institutions))
                results.extend(papers)
                time.sleep(2)  # 避免请求过快
            except Exception as e:
                print(f"{institution['name']}搜索失败: {e}")

        print(f"机构资源找到 {len(results)} 篇可下载论文")
        return results

    def _search_single_institution(self, institution: Dict, max_results: int) -> List[Dict]:
        """搜索单个机构"""
        try:
            response = self.session.get(institution['search_url'], timeout=20)
            if response.status_code == 200:

                # 查找PDF链接
                pdf_matches = re.findall(institution['pdf_pattern'], response.text)
                unique_pdfs = list(set(pdf_matches))[:max_results]

                results = []
                for pdf_url in unique_pdfs:
                    if not pdf_url.startswith('http'):
                        pdf_url = urljoin(institution['base_url'], pdf_url)

                    # 验证PDF可下载性
                    if self._verify_pdf_downloadable(pdf_url):
                        file_size = self._get_file_size(pdf_url)

                        results.append({
                            'title': f"Institution Paper from {institution['name']}",
                            'authors': ['Various'],
                            'abstract': 'Available from institutional repository',
                            'pdf_url': pdf_url,
                            'source': institution['name'],
                            'confidence': institution['confidence'],
                            'file_size': file_size,
                            'published': 'Unknown'
                        })

                return results
            else:
                return []

        except Exception as e:
            print(f"机构搜索出错: {e}")
            return []

    def _verify_pdf_downloadable(self, url: str) -> bool:
        """验证PDF链接是否可下载"""
        if not url:
            return False

        try:
            response = self.session.head(url, timeout=10)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').lower()
                return 'pdf' in content_type
        except:
            pass
        return False

    def _parse_file_size(self, size_str: str) -> int:
        """解析文件大小字符串为KB数值"""
        try:
            if 'KB' in size_str:
                return int(float(size_str.replace('KB', '')))
            elif 'MB' in size_str:
                return int(float(size_str.replace('MB', ''))) * 1000
            elif 'B' in size_str:
                return int(float(size_str.replace('B', ''))) // 1000
            else:
                return 0
        except:
            return 0

    def _get_file_size(self, url: str) -> str:
        """获取文件大小的友好显示"""
        try:
            response = self.session.head(url, timeout=5)
            if response.status_code == 200:
                size = int(response.headers.get('content-length', 0))
                if size > 0:
                    if size < 1024:
                        return f"{size}B"
                    elif size < 1024*1024:
                        return f"{size/1024:.1f}KB"
                    else:
                        return f"{size/(1024*1024):.1f}MB"
        except:
            pass
        return "Unknown"

    def download_paper(self, paper_info: Dict, custom_filename: Optional[str] = None) -> Optional[str]:
        """下载论文 - 工具化执行"""
        pdf_url = paper_info['pdf_url']

        if not self._verify_pdf_downloadable(pdf_url):
            return None

        try:
            response = self.session.get(pdf_url, stream=True, timeout=30)
            if response.status_code == 200:

                # 生成文件名
                if not custom_filename:
                    safe_title = re.sub(r'[^\w\s-]', '', paper_info['title'])[:50]
                    custom_filename = f"{safe_title}_{paper_info['source']}.pdf"

                filepath = os.path.join(self.download_dir, custom_filename)

                # 验证PDF内容
                content = next(response.iter_content(chunk_size=1024))
                if content.startswith(b'%PDF'):

                    # 写入文件
                    with open(filepath, 'wb') as f:
                        f.write(content)
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    actual_size = os.path.getsize(filepath)
                    print(f"下载成功: {filepath} ({actual_size} bytes)")
                    return filepath
                else:
                    print(f"文件不是有效PDF格式")
                    return None
            else:
                print(f"下载失败: HTTP {response.status_code}")
                return None

        except Exception as e:
            print(f"下载出错: {e}")
            return None

    def get_search_summary(self, results: Dict) -> str:
        """生成搜索摘要 - AI解释辅助"""
        summary_parts = []

        total = results['total_downloadable']
        arxiv_count = len(results['arxiv_results'])
        inst_count = len(results['institutional_results'])

        if total > 0:
            summary_parts.append(f"找到 {total} 篇可下载论文")

            if arxiv_count > 0:
                summary_parts.append(f"arXiv: {arxiv_count} 篇（100%可下载）")

            if inst_count > 0:
                summary_parts.append(f"机构资源: {inst_count} 篇（已验证）")

            # 计算总文件大小估算
            total_size = sum(
                self._parse_file_size(paper.get('file_size', '0'))
                for paper in results['arxiv_results'] + results['institutional_results']
                if paper.get('file_size') != 'Unknown'
            )

            if total_size > 1000:
                summary_parts.append(f"总计约 {total_size/1000:.1f}MB")

        else:
            summary_parts.append("未找到可下载的免费论文")
            summary_parts.append("建议调整关键词或考虑合法获取途径")

        return " | ".join(summary_parts)

def main():
    """命令行使用示例"""
    searcher = VerifiedPaperSearcher()

    # 示例搜索
    query = "machine learning"
    results = searcher.search_papers(query, max_results=5)

    print("\n=== 搜索结果 ===")
    print(searcher.get_search_summary(results))

    # 显示找到的论文
    all_papers = results['arxiv_results'] + results['institutional_results']
    for i, paper in enumerate(all_papers, 1):
        print(f"\n{i}. {paper['title'][:80]}...")
        print(f"   来源: {paper['source']} | 大小: {paper['file_size']} | 可信度: {paper['confidence']}")

if __name__ == "__main__":
    main()