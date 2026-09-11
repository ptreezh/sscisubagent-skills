#!/usr/bin/env python3
"""
关键词共现分析工具
用于构建和分析关键词共现网络

Usage:
    python keyword_cooccurrence.py --input data.json --output network.json
"""

import argparse
import json
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
import numpy as np

class KeywordCooccurrenceAnalyzer:
    """关键词共现分析器"""
    
    def __init__(self):
        self.papers = []
        self.cooccurrence_matrix = defaultdict(lambda: defaultdict(int))
        self.keyword_freq = Counter()
        
    def load_data(self, filepath: str) -> None:
        """加载文献数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.papers = json.load(f)
    
    def preprocess_keywords(self, keywords: List[str]) -> List[str]:
        """关键词预处理"""
        processed = []
        for kw in keywords:
            # 小写化
            kw = kw.lower().strip()
            # 去除标点
            kw = ''.join(c for c in kw if c.isalnum() or c in ' -')
            # 统一同义词
            # ...
            if kw:
                processed.append(kw)
        return processed
    
    def build_cooccurrence_matrix(self) -> None:
        """构建共现矩阵"""
        for paper in self.papers:
            keywords = self.preprocess_keywords(paper.get('keywords', []))
            
            # 更新频次
            self.keyword_freq.update(keywords)
            
            # 统计共现
            for i in range(len(keywords)):
                for j in range(i + 1, len(keywords)):
                    kw1, kw2 = keywords[i], keywords[j]
                    if kw1 != kw2:
                        self.cooccurrence_matrix[kw1][kw2] += 1
                        self.cooccurrence_matrix[kw2][kw1] += 1
    
    def get_high_freq_keywords(self, min_freq: int = 5) -> List[Tuple[str, int]]:
        """获取高频关键词"""
        return [(kw, freq) for kw, freq in self.keyword_freq.most_common() 
                if freq >= min_freq]
    
    def calculate_salton_index(self, kw1: str, kw2: str) -> float:
        """计算Salton指数(余弦相似度)"""
        co_count = self.cooccurrence_matrix[kw1][kw2]
        freq1 = self.keyword_freq[kw1]
        freq2 = self.keyword_freq[kw2]
        
        if freq1 == 0 or freq2 == 0:
            return 0.0
        
        return co_count / np.sqrt(freq1 * freq2)
    
    def calculate_jaccard_index(self, kw1: str, kw2: str) -> float:
        """计算Jaccard指数"""
        co_count = self.cooccurrence_matrix[kw1][kw2]
        freq1 = self.keyword_freq[kw1]
        freq2 = self.keyword_freq[kw2]
        
        union = freq1 + freq2 - co_count
        if union == 0:
            return 0.0
        
        return co_count / union
    
    def detect_burst_keywords(self, time_windows: int = 5) -> List[Dict]:
        """检测突发关键词(Kleinberg算法简化版)"""
        # 按年份分组统计
        year_counts = defaultdict(lambda: Counter())
        
        for paper in self.papers:
            year = paper.get('year')
            if year:
                keywords = self.preprocess_keywords(paper.get('keywords', []))
                year_counts[year].update(keywords)
        
        # 计算增长率
        bursts = []
        years = sorted(year_counts.keys())
        
        for i in range(1, len(years)):
            prev_year, curr_year = years[i-1], years[i]
            prev_counts = year_counts[prev_year]
            curr_counts = year_counts[curr_year]
            
            for kw in set(prev_counts.keys()) | set(curr_counts.keys()):
                prev_count = prev_counts.get(kw, 0)
                curr_count = curr_counts.get(kw, 0)
                
                if prev_count > 0:
                    growth_rate = (curr_count - prev_count) / prev_count
                    if growth_rate > 2.0:  # 增长超过2倍
                        bursts.append({
                            'keyword': kw,
                            'year': curr_year,
                            'prev_count': prev_count,
                            'curr_count': curr_count,
                            'growth_rate': growth_rate
                        })
        
        bursts.sort(key=lambda x: x['growth_rate'], reverse=True)
        return bursts
    
    def export_for_vosviewer(self, output_path: str, 
                             min_freq: int = 5,
                             min_cooccur: int = 1) -> None:
        """导出VOSviewer格式"""
        # 筛选高频关键词
        high_freq_kw = {kw for kw, freq in self.get_high_freq_keywords(min_freq)}
        
        nodes = []
        edges = []
        node_id_map = {}
        
        # 创建节点
        for i, kw in enumerate(sorted(high_freq_kw)):
            node_id_map[kw] = i
            nodes.append({
                'id': i,
                'label': kw,
                'weight': self.keyword_freq[kw]
            })
        
        # 创建边
        for kw1 in high_freq_kw:
            for kw2 in high_freq_kw:
                if kw1 < kw2:
                    co_count = self.cooccurrence_matrix[kw1][kw2]
                    if co_count >= min_cooccur:
                        edges.append({
                            'source': node_id_map[kw1],
                            'target': node_id_map[kw2],
                            'weight': co_count
                        })
        
        # VOSviewer格式
        vos_data = {
            'items': nodes,
            'links': edges
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(vos_data, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='关键词共现分析工具')
    parser.add_argument('--input', required=True, help='输入数据文件')
    parser.add_argument('--output', required=True, help='输出网络文件')
    parser.add_argument('--min-freq', type=int, default=5, help='最小关键词频次')
    parser.add_argument('--min-cooccur', type=int, default=1, help='最小共现频次')
    parser.add_argument('--detect-burst', action='store_true', help='检测突发关键词')
    
    args = parser.parse_args()
    
    analyzer = KeywordCooccurrenceAnalyzer()
    analyzer.load_data(args.input)
    analyzer.build_cooccurrence_matrix()
    
    # 输出高频关键词
    print("高频关键词(Top 20):")
    for kw, freq in analyzer.get_high_freq_keywords(5)[:20]:
        print(f"  {kw}: {freq}")
    
    # 导出网络
    analyzer.export_for_vosviewer(args.output, args.min_freq, args.min_cooccur)
    print(f"\n网络已导出至: {args.output}")
    
    # 检测突发词
    if args.detect_burst:
        bursts = analyzer.detect_burst_keywords()
        print("\n突发关键词(Top 10):")
        for b in bursts[:10]:
            print(f"  {b['keyword']} ({b['year']}): {b['prev_count']} -> {b['curr_count']}")

if __name__ == '__main__':
    main()
