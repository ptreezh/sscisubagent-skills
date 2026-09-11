#!/usr/bin/env python3
"""
共引分析工具
用于构建和分析文献共引网络

Usage:
    python co_citation_analyzer.py --input data.json --output network.json
"""

import argparse
import json
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import numpy as np

class CoCitationAnalyzer:
    """共引分析器"""
    
    def __init__(self):
        self.citation_data = {}
        self.co_citation_matrix = defaultdict(lambda: defaultdict(int))
        
    def load_data(self, filepath: str) -> None:
        """加载引文数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.citation_data = json.load(f)
    
    def build_co_citation_matrix(self) -> Dict[str, Dict[str, int]]:
        """构建共引矩阵"""
        # 每篇施引文献的参考文献列表
        for paper_id, references in self.citation_data.items():
            ref_list = list(references)
            # 统计两两共引
            for i in range(len(ref_list)):
                for j in range(i + 1, len(ref_list)):
                    ref1, ref2 = ref_list[i], ref_list[j]
                    self.co_citation_matrix[ref1][ref2] += 1
                    self.co_citation_matrix[ref2][ref1] += 1
        
        return dict(self.co_citation_matrix)
    
    def calculate_similarity(self, method: str = 'cosine') -> Dict[Tuple[str, str], float]:
        """计算相似度"""
        similarity = {}
        citations = self.co_citation_matrix
        
        for ref1 in citations:
            for ref2 in citations[ref1]:
                if (ref2, ref1) in similarity:
                    similarity[(ref1, ref2)] = similarity[(ref2, ref1)]
                    continue
                    
                co_count = citations[ref1][ref2]
                count1 = sum(citations[ref1].values())
                count2 = sum(citations[ref2].values())
                
                if method == 'cosine':
                    sim = co_count / np.sqrt(count1 * count2)
                elif method == 'jaccard':
                    sim = co_count / (count1 + count2 - co_count)
                else:
                    sim = co_count
                
                similarity[(ref1, ref2)] = sim
        
        return similarity
    
    def get_top_pairs(self, n: int = 100) -> List[Tuple[str, str, int]]:
        """获取共引频次最高的文献对"""
        pairs = []
        for ref1 in self.co_citation_matrix:
            for ref2, count in self.co_citation_matrix[ref1].items():
                if ref1 < ref2:  # 避免重复
                    pairs.append((ref1, ref2, count))
        
        pairs.sort(key=lambda x: x[2], reverse=True)
        return pairs[:n]
    
    def export_network(self, output_path: str, min_weight: int = 1) -> None:
        """导出网络数据(用于VOSviewer等)"""
        nodes = set()
        edges = []
        
        for ref1 in self.co_citation_matrix:
            for ref2, weight in self.co_citation_matrix[ref1].items():
                if weight >= min_weight and ref1 < ref2:
                    nodes.add(ref1)
                    nodes.add(ref2)
                    edges.append({
                        'source': ref1,
                        'target': ref2,
                        'weight': weight
                    })
        
        network = {
            'nodes': [{'id': n} for n in sorted(nodes)],
            'edges': edges
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(network, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='共引分析工具')
    parser.add_argument('--input', required=True, help='输入数据文件路径')
    parser.add_argument('--output', required=True, help='输出网络文件路径')
    parser.add_argument('--min-weight', type=int, default=1, help='最小共引频次阈值')
    parser.add_argument('--method', choices=['cosine', 'jaccard', 'raw'], 
                       default='cosine', help='相似度计算方法')
    
    args = parser.parse_args()
    
    analyzer = CoCitationAnalyzer()
    analyzer.load_data(args.input)
    analyzer.build_co_citation_matrix()
    analyzer.export_network(args.output, args.min_weight)
    
    # 输出统计信息
    top_pairs = analyzer.get_top_pairs(10)
    print("Top 10 共引文献对:")
    for ref1, ref2, count in top_pairs:
        print(f"  {ref1[:30]}... <-> {ref2[:30]}... : {count}")

if __name__ == '__main__':
    main()
