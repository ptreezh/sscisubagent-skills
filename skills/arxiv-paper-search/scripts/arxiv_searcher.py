#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv论文检索与下载技能 - 核心实现

功能:
1. 论文检索（基于arXiv API）
2. 摘要批量下载（支持10/20/50/100篇）
3. PDF全文下载（单篇/批量）
4. 结果导出（JSON/CSV）

依赖（最小化）:
- requests: HTTP请求
- feedparser: 解析arXiv API的Atom/RSS响应
- 标准库: time, json, csv, pathlib, typing, datetime, urllib

作者: socienceAI.com
版本: 1.0.0
"""

import requests
import feedparser
import time
import json
import csv
import urllib.parse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class ArxivPaperSearcher:
    """arXiv论文检索与下载器"""

    # arXiv API配置
    ARXIV_API_URL = "http://export.arxiv.org/api/query?"
    ARXIV_BASE_URL = "https://arxiv.org/"

    # 支持的返回数量
    MAX_RESULTS_OPTIONS = [10, 20, 50, 100]

    # 请求延迟（遵守arXiv API条款）
    REQUEST_DELAY = 3  # 秒

    def __init__(self, debug: bool = False):
        """
        初始化搜索器

        Args:
            debug: 是否启用调试模式
        """
        self.debug = debug
        self.last_request_time = 0

    def _log(self, message: str):
        """打印调试日志"""
        if self.debug:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {message}")

    def _respect_rate_limit(self):
        """遵守API请求频率限制"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.REQUEST_DELAY:
            sleep_time = self.REQUEST_DELAY - time_since_last_request
            self._log(f"等待 {sleep_time:.1f} 秒以遵守API限制")
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def search(
        self,
        query: str,
        max_results: int = 20,
        sort_by: str = "relevance",
        categories: Optional[List[str]] = None,
        date_range: Optional[Dict[str, str]] = None
    ) -> List[Dict]:
        """
        搜索arXiv论文

        Args:
            query: 搜索关键词
            max_results: 返回结果数（10/20/50/100）
            sort_by: 排序方式（relevance/lastUpdatedDate/submittedDate）
            categories: arXiv分类列表（如["cs.AI", "cs.LG"]）
            date_range: 日期范围 {"start": "2024-01-01", "end": "2024-12-31"}

        Returns:
            论文列表
        """
        # 验证max_results
        if max_results not in self.MAX_RESULTS_OPTIONS:
            self._log(f"max_results必须是{self.MAX_RESULTS_OPTIONS}之一，使用默认值20")
            max_results = 20

        self._log(f"搜索查询: '{query}'")
        self._log(f"最大结果数: {max_results}")
        self._log(f"排序方式: {sort_by}")

        # 构建搜索查询
        search_query = self._build_search_query(
            query, categories, date_range
        )

        # 构建URL
        url_params = {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results,
            "sortBy": sort_by,
            "sortOrder": "descending"
        }

        url = self.ARXIV_API_URL + urllib.parse.urlencode(url_params)
        self._log(f"请求URL: {url}")

        # 发送请求（遵守频率限制）
        self._respect_rate_limit()

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            self._log(f"请求失败: {e}")
            return []

        # 解析结果
        feed = feedparser.parse(response.content)

        self._log(f"找到 {len(feed.entries)} 篇论文")

        # 提取论文信息
        papers = []
        for i, entry in enumerate(feed.entries, 1):
            paper = self._parse_entry(entry, i)
            if paper:
                papers.append(paper)

        return papers

    def _build_search_query(
        self,
        query: str,
        categories: Optional[List[str]],
        date_range: Optional[Dict[str, str]]
    ) -> str:
        """构建arXiv搜索查询字符串"""

        # 基础查询（搜索标题、摘要、作者）
        search_query = f"all:{query}"

        # 添加分类筛选
        if categories:
            cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
            search_query = f"({search_query}) AND ({cat_query})"

        # 添加日期范围（使用arXiv的日期过滤）
        if date_range:
            start_date = date_range.get("start", "")
            end_date = date_range.get("end", "")
            if start_date and end_date:
                # arXiv API日期格式: YYYYMMDD
                start_formatted = start_date.replace("-", "")
                end_formatted = end_date.replace("-", "")
                date_filter = f"submittedDate:[{start_formatted} TO {end_formatted}]"
                search_query = f"({search_query}) AND {date_filter}"

        return search_query

    def _parse_entry(self, entry, index: int) -> Optional[Dict]:
        """解析单个论文条目"""

        try:
            # 提取arXiv ID
            arxiv_id = entry.id.split("/")[-1]

            # 提取作者
            authors = []
            if hasattr(entry, 'authors'):
                authors = [author.name for author in entry.authors]

            # 提取分类
            categories = []
            if hasattr(entry, 'tags'):
                categories = [tag.term for tag in entry.tags]

            # 提取PDF链接
            pdf_url = entry.link.replace('/abs/', '/pdf/') + '.pdf'

            # 提取DOI（如果有）
            doi = None
            if hasattr(entry, 'arxiv_doi'):
                doi = entry.arxiv_doi

            # 构建论文信息
            paper = {
                "index": index,
                "title": entry.title,
                "authors": authors,
                "summary": entry.summary.replace('\n', ' ').strip(),
                "published": entry.get('published', ''),
                "updated": entry.get('updated', ''),
                "arxiv_id": arxiv_id,
                "pdf_url": pdf_url,
                "categories": categories,
                "doi": doi,
                "comment": entry.get('arxiv_comment', ''),
                "journal_ref": entry.get('arxiv_journal_ref', '')
            }

            self._log(f"解析论文 #{index}: {paper['title'][:50]}...")

            return paper

        except Exception as e:
            self._log(f"解析条目失败: {e}")
            return None

    def download_pdf(
        self,
        arxiv_id: str,
        output_dir: str = "papers/",
        filename: Optional[str] = None
    ) -> Optional[str]:
        """
        下载单篇论文PDF

        Args:
            arxiv_id: arXiv ID（如"2312.11805"或完整URL）
            output_dir: 输出目录
            filename: 自定义文件名（可选）

        Returns:
            保存的文件路径，失败返回None
        """
        # 清理arXiv ID
        arxiv_id = arxiv_id.split("/")[-1].replace(".pdf", "")

        # 构建PDF URL
        pdf_url = f"{self.ARXIV_BASE_URL}pdf/{arxiv_id}.pdf"

        # 生成文件名
        if not filename:
            filename = f"{arxiv_id.replace('/', '_')}.pdf"

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / filename

        self._log(f"下载PDF: {arxiv_id}")
        self._log(f"URL: {pdf_url}")
        self._log(f"保存到: {file_path}")

        # 遵守频率限制
        self._respect_rate_limit()

        try:
            # 流式下载
            response = requests.get(pdf_url, stream=True, timeout=60)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # 显示进度（每1MB）
                        if total_size > 0 and downloaded % (1024*1024) == 0:
                            progress = (downloaded / total_size) * 100
                            self._log(f"下载进度: {progress:.1f}%")

            self._log(f"✓ PDF下载完成: {file_path}")

            return str(file_path)

        except requests.RequestException as e:
            self._log(f"✗ 下载失败: {e}")
            return None

    def batch_download_pdfs(
        self,
        papers: List[Dict],
        output_dir: str = "papers/",
        max_papers: Optional[int] = None,
        delay: float = 3.0
    ) -> List[str]:
        """
        批量下载论文PDF

        Args:
            papers: 论文列表（来自search方法）
            output_dir: 输出目录
            max_papers: 最大下载数量
            delay: 每次下载间隔（秒）

        Returns:
            成功下载的文件路径列表
        """
        if max_papers:
            papers = papers[:max_papers]

        self._log(f"批量下载 {len(papers)} 篇论文")

        downloaded_files = []

        for i, paper in enumerate(papers, 1):
            arxiv_id = paper['arxiv_id']
            filename = f"{arxiv_id.replace('/', '_')}_{paper['title'][:30].replace(' ', '_')}.pdf"

            self._log(f"\n[{i}/{len(papers)}] 下载: {paper['title'][:50]}")

            file_path = self.download_pdf(arxiv_id, output_dir, filename)

            if file_path:
                downloaded_files.append(file_path)

            # 延迟（最后一次不需要）
            if i < len(papers):
                self._log(f"等待 {delay} 秒...")
                time.sleep(delay)

        self._log(f"\n✓ 成功下载 {len(downloaded_files)}/{len(papers)} 篇论文")

        return downloaded_files

    def save_abstracts(
        self,
        papers: List[Dict],
        output_file: str = "abstracts.json"
    ):
        """
        保存论文摘要到JSON文件

        Args:
            papers: 论文列表
            output_file: 输出文件名
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)

        self._log(f"✓ 摘要已保存到: {output_file}")

    def export_to_csv(
        self,
        papers: List[Dict],
        output_file: str = "papers.csv"
    ):
        """
        导出论文信息到CSV文件

        Args:
            papers: 论文列表
            output_file: 输出文件名
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            if not papers:
                return

            writer = csv.DictWriter(f, fieldnames=papers[0].keys())
            writer.writeheader()

            for paper in papers:
                # 处理列表字段（作者、分类）
                row = {}
                for key, value in paper.items():
                    if isinstance(value, list):
                        row[key] = "; ".join(value)
                    else:
                        row[key] = value
                writer.writerow(row)

        self._log(f"✓ CSV已导出到: {output_file}")

    def get_recent_ai_papers(
        self,
        days: int = 7,
        max_results: int = 20
    ) -> List[Dict]:
        """
        获取最近AI领域的论文

        Args:
            days: 最近几天
            max_results: 最大结果数

        Returns:
            论文列表
        """
        from datetime import timedelta

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        date_range = {
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d")
        }

        ai_categories = ["cs.AI", "cs.LG", "cs.CL", "cs.NE", "stat.ML"]

        self._log(f"获取最近{days}天的AI论文")

        return self.search(
            query="artificial intelligence OR machine learning",
            max_results=max_results,
            categories=ai_categories,
            date_range=date_range,
            sort_by="submittedDate"
        )


# 便捷的同步接口
class SynchronousArxivSearcher(ArxivPaperSearcher):
    """同步接口的简化版（与ArxivPaperSearcher相同，提供命名一致性）"""

    pass


if __name__ == "__main__":
    # 测试代码
    print("arXiv论文检索与下载技能 - 核心模块")
    print("版本: 1.0.0")
    print("\n使用示例:")
    print("from skills.arxiv_paper_search.scripts.arxiv_searcher import ArxivPaperSearcher")
    print("searcher = ArxivPaperSearcher()")
    print("results = searcher.search('large language models', max_results=20)")
