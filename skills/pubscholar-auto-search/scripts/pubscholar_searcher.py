#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PubScholar自动搜索脚本

功能：
1. 在PubScholar平台自动执行文献搜索
2. 精准搜索优先，结果不足5篇时智能扩展
3. 提取文献元数据（标题、作者、期刊等）
4. 支持结果导出（JSON/CSV/Excel）
"""

import asyncio
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import csv

try:
    from playwright.async_api import async_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("警告: Playwright未安装，将使用模拟模式")


class PubScholarSearcher:
    """PubScholar自动搜索器"""

    def __init__(self, debug: bool = False, headless: bool = True):
        """
        初始化搜索器

        Args:
            debug: 是否启用调试模式
            headless: 是否使用无头浏览器（不显示GUI）
        """
        self.debug = debug
        self.headless = headless
        self.base_url = "https://pubscholar.cn/"
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        """异步上下文管理器入口"""
        if PLAYWRIGHT_AVAILABLE:
            await self.start_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if PLAYWRIGHT_AVAILABLE:
            await self.close_browser()

    async def start_browser(self):
        """启动浏览器"""
        if not PLAYWRIGHT_AVAILABLE:
            print("Playwright未安装，使用模拟模式")
            return

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-setuid-sandbox'] if self.headless else []
        )
        self.page = await self.browser.new_page()

        if self.debug:
            print("✓ 浏览器已启动")

    async def close_browser(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
        if self.debug:
            print("✓ 浏览器已关闭")

    async def search(
        self,
        keyword: str,
        auto_expand: bool = True,
        min_results: int = 5,
        max_results: int = 50
    ) -> List[Dict]:
        """
        执行搜索（支持智能扩展）

        Args:
            keyword: 搜索关键词
            auto_expand: 是否启用智能扩展（结果不足时自动扩展）
            min_results: 触发扩展的最小结果数阈值
            max_results: 最大返回结果数

        Returns:
            文献列表，每篇文献包含标题、作者、期刊等信息
        """
        if not PLAYWRIGHT_AVAILABLE:
            return self._mock_search(keyword)

        await self._navigate_to_homepage()

        # 第一阶段：精准搜索
        if self.debug:
            print(f"\n[阶段1] 精准搜索: '{keyword}'")

        results = await self._execute_search(keyword)

        if self.debug:
            print(f"✓ 精准搜索返回 {len(results)} 篇文献")

        # 第二阶段：智能扩展（如果需要）
        if auto_expand and len(results) < min_results:
            if self.debug:
                print(f"\n[阶段2] 结果不足{min_results}篇，启动智能扩展...")

            expanded_results = await self._smart_expansion(
                keyword,
                current_results=len(results),
                target=min_results
            )

            # 合并去重
            seen_urls = {r['url'] for r in results}
            for result in expanded_results:
                if result['url'] not in seen_urls:
                    results.append(result)
                    seen_urls.add(result['url'])

            if self.debug:
                print(f"✓ 扩展后共 {len(results)} 篇文献")

        # 限制返回数量
        results = results[:max_results]

        return results

    async def _navigate_to_homepage(self):
        """导航到首页"""
        await self.page.goto(self.base_url, wait_until='domcontentloaded')
        await self.page.wait_for_timeout(2000)  # 等待页面完全加载

        if self.debug:
            print("✓ 已导航到PubScholar首页")

    async def _execute_search(self, keyword: str) -> List[Dict]:
        """
        执行单次搜索

        Args:
            keyword: 搜索关键词

        Returns:
            文献列表
        """
        # 查找搜索框并输入关键词
        search_box = self.page.locator('textarea[placeholder*="发现你感兴趣的内容"]').or_(
            self.page.locator('input[placeholder*="发现你感兴趣的内容"]')
        )

        await search_box.fill(keyword)
        await self.page.wait_for_timeout(500)

        # 点击搜索按钮
        search_button = self.page.locator('button:has-text("检索")').first
        await search_button.click()

        # 等待结果页面加载
        await self.page.wait_for_url("**/explore", timeout=10000)
        await self.page.wait_for_timeout(3000)

        # 提取结果
        results = await self._extract_results()

        return results

    async def _extract_results(self) -> List[Dict]:
        """
        从结果页面提取文献信息

        Returns:
            文献列表
        """
        papers = []

        try:
            # 等待结果列表加载
            await self.page.wait_for_selector('text=/论文/', timeout=5000)
        except:
            if self.debug:
                print("⚠ 未找到结果列表")
            return papers

        # 获取结果数量
        try:
            count_text = await self.page.locator('text=/\\d+\\/\\d+ 条').text_content()
            if count_text:
                match = re.search(r'(\d+)\s*/\s*(\d+)', count_text)
                if match:
                    displayed, total = match.groups()
                    if self.debug:
                        print(f"✓ 结果统计: 显示 {displayed} 篇，总计 {total} 篇")
        except:
            pass

        # 提取每篇文献的信息
        paper_items = await self.page.locator('generic').all()
        if self.debug:
            print(f"✓ 找到 {len(paper_items)} 个文献条目")

        for i, item in enumerate(paper_items[:50]):  # 最多提取前50篇
            try:
                paper = await self._extract_paper_info(item, i + 1)
                if paper and paper.get('title'):
                    papers.append(paper)
            except Exception as e:
                if self.debug:
                    print(f"⚠ 提取第{i+1}篇文献失败: {e}")
                continue

        return papers

    async def _extract_paper_info(self, item, index: int) -> Optional[Dict]:
        """
        从单个条目提取文献信息

        Args:
            item: 页面元素
            index: 文献序号

        Returns:
            文献信息字典
        """
        paper = {
            'index': index,
            'title': '',
            'authors': [],
            'journal': '',
            'year': '',
            'abstract': '',
            'keywords': [],
            'url': '',
            'source': 'PubScholar'
        }

        try:
            # 提取标题
            title_elem = item.locator('h2').or_(item.locator('[role="heading"]'))
            if await title_elem.count() > 0:
                paper['title'] = await title_elem.first.inner_text()

            # 提取作者
            author_text = await item.locator('text=/Nikanjam|Mina|et al/').or_(
                item.locator('generic:has-text(",")')
            ).all_inner_texts()
            if author_text:
                # 简单提取作者信息
                authors = [t.strip() for t in author_text if t.strip() and ',' in t]
                paper['authors'] = authors[:10]  # 限制作者数量

            # 提取期刊信息
            journal_elem = item.locator('link:has-text("《")').or_(
                item.locator('[role="link"]:has-text("《")')
            )
            if await journal_elem.count() > 0:
                journal_text = await journal_elem.first.inner_text()
                # 解析期刊、年份、卷期、页码
                journal_info = self._parse_journal_info(journal_text)
                paper.update(journal_info)

            # 提取摘要
            abstract_elem = item.locator('generic:has-text("...")')
            if await abstract_elem.count() > 0:
                abstracts = await abstract_elem.all_inner_texts()
                if abstracts:
                    paper['abstract'] = abstracts[0].strip()

            # 提取关键词
            keyword_elems = await item.locator('text=/Keywords:/').all()
            if keyword_elems:
                # 提取关键词（简化处理）
                pass

            # 提取URL
            link_elem = item.locator('a').first
            if await link_elem.count() > 0:
                paper['url'] = await link_elem.get_attribute('href')
                if paper['url'] and not paper['url'].startswith('http'):
                    paper['url'] = 'https://pubscholar.cn' + paper['url']

        except Exception as e:
            if self.debug:
                print(f"⚠ 提取文献{index}信息时出错: {e}")

        return paper if paper['title'] else None

    def _parse_journal_info(self, journal_text: str) -> Dict:
        """
        解析期刊信息字符串

        Args:
            journal_text: 期刊信息文本

        Returns:
            包含期刊、年份、卷期、页码的字典
        """
        info = {'journal': '', 'year': '', 'volume': '', 'issue': '', 'pages': ''}

        # 提取期刊名称（《》之间）
        journal_match = re.search(r'《(.*?)》', journal_text)
        if journal_match:
            info['journal'] = journal_match.group(1)

        # 提取年份（4位数字）
        year_match = re.search(r',\s*(\d{4})\s*,', journal_text)
        if year_match:
            info['year'] = year_match.group(1)

        # 提取卷和页码
        volume_match = re.search(r'Volume\s+(\d+)', journal_text)
        if volume_match:
            info['volume'] = volume_match.group(1)

        pages_match = re.search(r'Pages\s+(\d+)\s*-\s*(\d+)', journal_text)
        if pages_match:
            info['pages'] = f"{pages_match.group(1)}-{pages_match.group(2)}"

        return info

    async def _smart_expansion(
        self,
        original_keyword: str,
        current_results: int,
        target: int
    ) -> List[Dict]:
        """
        智能扩展搜索

        Args:
            original_keyword: 原始关键词
            current_results: 当前结果数
            target: 目标结果数

        Returns:
            扩展搜索的文献列表
        """
        expansion_strategies = self._generate_expansion_strategies(original_keyword)
        all_results = []

        for i, strategy in enumerate(expansion_strategies, 1):
            if self.debug:
                print(f"\n  [扩展策略{i}] 搜索: '{strategy}'")

            results = await self._execute_search(strategy)

            if self.debug:
                print(f"  → 返回 {len(results)} 篇")

            all_results.extend(results)

            # 如果累计结果达到目标，停止扩展
            if current_results + len(all_results) >= target:
                if self.debug:
                    print(f"  ✓ 已达到目标结果数")
                break

            # 避免请求过快
            await asyncio.sleep(2)

        return all_results

    def _generate_expansion_strategies(self, keyword: str) -> List[str]:
        """
        生成扩展搜索策略

        Args:
            keyword: 原始关键词

        Returns:
            扩展关键词列表
        """
        strategies = []

        # 策略1: 添加常见同义词
        synonyms_map = {
            '人工智能': ['AI', '机器学习', '智能系统'],
            '数字鸿沟': ['信息不平等', '数字不平等', '信息分化'],
            '社会网络': ['社交网络', '关系网络'],
            '大数据': ['海量数据', '数据科学'],
            '深度学习': ['神经网络', '深度网络', 'DL'],
            '机器学习': ['ML', '人工智能'],
        }

        # 检查是否有同义词
        for key, synonyms in synonyms_map.items():
            if key in keyword:
                for synonym in synonyms:
                    strategies.append(f"{keyword} {synonym}")

        # 策略2: 添加英文翻译（常见术语）
        english_map = {
            '人工智能': 'artificial intelligence',
            '机器学习': 'machine learning',
            '深度学习': 'deep learning',
            '数据挖掘': 'data mining',
            '社会网络': 'social network',
            '数字鸿沟': 'digital divide',
        }

        for cn, en in english_map.items():
            if cn in keyword:
                strategies.append(f"{keyword} {en}")

        # 策略3: 简化关键词（去除部分修饰词）
        words = keyword.split()
        if len(words) > 1:
            # 使用第一个主要词
            strategies.append(words[0])
            # 使用最后一个主要词
            strategies.append(words[-1])

        # 策略4: 添加相关领域
        if any(word in keyword for word in ['教育', '学习', '教学']):
            strategies.append(f"{keyword} 教育")

        if any(word in keyword for word in ['社会', '社区', '组织']):
            strategies.append(f"{keyword} 社会学")

        # 去重并保持顺序
        seen = set()
        unique_strategies = []
        for s in strategies:
            if s and s != keyword and s not in seen:
                seen.add(s)
                unique_strategies.append(s)

        return unique_strategies[:5]  # 最多5个扩展策略

    def _mock_search(self, keyword: str) -> List[Dict]:
        """
        模拟搜索（当Playwright未安装时）

        Args:
            keyword: 搜索关键词

        Returns:
            模拟的文献列表
        """
        print(f"[模拟模式] 搜索关键词: '{keyword}'")

        # 返回模拟数据
        mock_papers = [
            {
                'index': 1,
                'title': f'关于{keyword}的研究进展',
                'authors': ['张三', '李四'],
                'journal': '示例期刊',
                'year': '2024',
                'abstract': f'本文研究了{keyword}的相关问题...',
                'keywords': [keyword],
                'url': 'https://pubscholar.cn/example',
                'source': 'Mock Data'
            },
            {
                'index': 2,
                'title': f'{keyword}在实践中的应用',
                'authors': ['王五'],
                'journal': '学术期刊',
                'year': '2023',
                'abstract': f'{keyword}在实际场景中的...',
                'keywords': [keyword, '应用'],
                'url': 'https://pubscholar.cn/example2',
                'source': 'Mock Data'
            }
        ]

        return mock_papers

    def export_to_json(self, results: List[Dict], filename: str):
        """导出结果为JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"✓ 结果已导出到 {filename}")

    def export_to_csv(self, results: List[Dict], filename: str):
        """导出结果为CSV"""
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            if not results:
                print("⚠ 没有结果可导出")
                return

            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            for result in results:
                # 处理列表类型字段
                row = {}
                for key, value in result.items():
                    if isinstance(value, list):
                        row[key] = '; '.join(str(v) for v in value)
                    else:
                        row[key] = value
                writer.writerow(row)

        print(f"✓ 结果已导出到 {filename}")

    def generate_citations(self, results: List[Dict]) -> List[str]:
        """
        生成GB/T 7714格式的引用

        Args:
            results: 文献列表

        Returns:
            引用字符串列表
        """
        citations = []

        for paper in results:
            try:
                authors = ', '.join(paper.get('authors', [])[:3])  # 最多3个作者
                if len(paper.get('authors', [])) > 3:
                    authors += ' 等'

                title = paper.get('title', '')
                journal = paper.get('journal', '')
                year = paper.get('year', '')
                pages = paper.get('pages', '')

                citation = f"{authors}. {title}[J]. {journal}, {year}"
                if pages:
                    citation += f": {pages}"

                citations.append(citation)
            except Exception as e:
                if self.debug:
                    print(f"⚠ 生成引用失败: {e}")
                continue

        return citations


# ========== 测试和示例 ==========

async def main():
    """主函数示例"""
    # 使用示例
    async with PubScholarSearcher(debug=True) as searcher:
        # 搜索关键词
        keyword = "人工智能 医疗"
        print(f"\n=== PubScholar自动搜索 ===")
        print(f"搜索关键词: {keyword}\n")

        results = await searcher.search(keyword)

        print(f"\n=== 搜索结果 ===")
        print(f"共找到 {len(results)} 篇文献\n")

        # 显示前5篇
        for i, paper in enumerate(results[:5], 1):
            print(f"{i}. {paper['title']}")
            print(f"   作者: {', '.join(paper.get('authors', [])[:3])}")
            print(f"   期刊: {paper['journal']} ({paper['year']})")
            print()

        # 导出结果
        if results:
            searcher.export_to_json(results, f'pubscholar_{keyword.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.json')
            searcher.export_to_csv(results, f'pubscholar_{keyword.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.csv')


class SynchronousPubScholarSearcher:
    """同步接口包装器（便于非async环境使用）"""

    def __init__(self, debug: bool = False, headless: bool = True):
        self.async_searcher = PubScholarSearcher(debug=debug, headless=headless)

    def search(self, keyword: str, **kwargs) -> List[Dict]:
        """同步搜索方法"""
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.async_searcher.search(keyword, **kwargs))

    def export_to_json(self, results: List[Dict], filename: str):
        """导出JSON"""
        self.async_searcher.export_to_json(results, filename)

    def export_to_csv(self, results: List[Dict], filename: str):
        """导出CSV"""
        self.async_searcher.export_to_csv(results, filename)


if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())
