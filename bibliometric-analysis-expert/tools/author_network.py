#!/usr/bin/env python3
"""
作者合作网络分析工具
用于构建和分析作者合作网络

Usage:
    python author_network.py --input data.json --output network.json
"""

import argparse
import json
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
import numpy as np

class AuthorNetworkAnalyzer:
    """作者合作网络分析器"""
    
    def __init__(self):
        self.papers = []
        self.author_papers = defaultdict(list)
        self.collaboration_matrix = defaultdict(lambda: defaultdict(int))
        
    def load_data(self, filepath: str) -> None:
        """加载文献数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.papers = json.load(f)
    
    def preprocess_author(self, name: str) -> str:
        """作者名预处理"""
        # 标准化姓名格式
        name = name.strip()
        # 统一大小写
        name = name.title()
        return name
    
    def build_collaboration_network(self) -> None:
        """构建合作网络"""
        for paper in self.papers:
            authors = [self.preprocess_author(a) for a in paper.get('authors', [])]
            paper_id = paper.get('id')
            
            # 记录每位作者的论文
            for author in authors:
                self.author_papers[author].append(paper_id)
            
            # 统计合作关系
            for i in range(len(authors)):
                for j in range(i + 1, len(authors)):
                    a1, a2 = authors[i], authors[j]
                    if a1 != a2:
                        self.collaboration_matrix[a1][a2] += 1
                        self.collaboration_matrix[a2][a1] += 1
    
    def calculate_productivity(self) -> Dict[str, int]:
        """计算作者产出"""
        return {author: len(papers) for author, papers in self.author_papers.items()}
    
    def calculate_degree_centrality(self) -> Dict[str, float]:
        """计算度中心性"""
        centrality = {}
        total_authors = len(self.collaboration_matrix)
        
        for author in self.collaboration_matrix:
            degree = len(self.collaboration_matrix[author])
            centrality[author] = degree / (total_authors - 1) if total_authors > 1 else 0
        
        return centrality
    
    def calculate_betweenness_centrality(self) -> Dict[str, float]:
        """计算中介中心性(简化版)"""
        # 使用Brandes算法的简化版本
        betweenness = defaultdict(float)
        authors = list(self.collaboration_matrix.keys())
        
        for source in authors[:50]:  # 限制计算规模
            # BFS计算最短路径
            visited = {source}
            queue = [(source, [source])]
            paths = {a: [] for a in authors}
            paths[source] = [[source]]
            
            while queue:
                current, path = queue.pop(0)
                for neighbor in self.collaboration_matrix[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_path = path + [neighbor]
                        queue.append((neighbor, new_path))
                        paths[neighbor] = [new_path]
                    elif len(path) + 1 == len(paths[neighbor][0]):
                        paths[neighbor].append(path + [neighbor])
            
            # 计算中介值
            for target in authors:
                if source != target and paths[target]:
                    for path in paths[target]:
                        for node in path[1:-1]:
                            betweenness[node] += 1 / len(paths[target])
        
        # 标准化
        n = len(authors)
        if n > 2:
            for author in betweenness:
                betweenness[author] /= ((n-1) * (n-2))
        
        return dict(betweenness)
    
    def find_core_authors(self, min_papers: int = 5, 
                          min_collaborators: int = 3) -> List[Tuple[str, Dict]]:
        """识别核心作者"""
        productivity = self.calculate_productivity()
        centrality = self.calculate_degree_centrality()
        
        core_authors = []
        for author in self.collaboration_matrix:
            if (productivity.get(author, 0) >= min_papers and
                len(self.collaboration_matrix[author]) >= min_collaborators):
                core_authors.append((
                    author,
                    {
                        'papers': productivity[author],
                        'collaborators': len(self.collaboration_matrix[author]),
                        'centrality': centrality[author]
                    }
                ))
        
        core_authors.sort(key=lambda x: x[1]['papers'], reverse=True)
        return core_authors
    
    def detect_research_teams(self, min_team_size: int = 3) -> List[Set[str]]:
        """检测研究团队(连通分量)"""
        visited = set()
        teams = []
        
        def dfs(author, team):
            visited.add(author)
            team.add(author)
            for collaborator in self.collaboration_matrix[author]:
                if collaborator not in visited:
                    dfs(collaborator, team)
        
        for author in self.collaboration_matrix:
            if author not in visited:
                team = set()
                dfs(author, team)
                if len(team) >= min_team_size:
                    teams.append(team)
        
        teams.sort(key=len, reverse=True)
        return teams
    
    def export_network(self, output_path: str, min_collab: int = 1) -> None:
        """导出网络数据"""
        nodes = []
        edges = []
        node_id_map = {}
        productivity = self.calculate_productivity()
        
        # 创建节点
        for i, author in enumerate(sorted(self.collaboration_matrix.keys())):
            node_id_map[author] = i
            nodes.append({
                'id': i,
                'label': author,
                'weight': productivity.get(author, 1)
            })
        
        # 创建边
        added = set()
        for a1 in self.collaboration_matrix:
            for a2, weight in self.collaboration_matrix[a1].items():
                if weight >= min_collab and (a2, a1) not in added:
                    edges.append({
                        'source': node_id_map[a1],
                        'target': node_id_map[a2],
                        'weight': weight
                    })
                    added.add((a1, a2))
        
        network = {
            'nodes': nodes,
            'edges': edges
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(network, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='作者合作网络分析')
    parser.add_argument('--input', required=True, help='输入数据文件')
    parser.add_argument('--output', required=True, help='输出网络文件')
    parser.add_argument('--min-collab', type=int, default=1, help='最小合作次数')
    parser.add_argument('--find-teams', action='store_true', help='检测研究团队')
    
    args = parser.parse_args()
    
    analyzer = AuthorNetworkAnalyzer()
    analyzer.load_data(args.input)
    analyzer.build_collaboration_network()
    
    # 输出核心作者
    core = analyzer.find_core_authors()
    print("核心作者(Top 10):")
    for author, info in core[:10]:
        print(f"  {author}: {info['papers']}篇, {info['collaborators']}位合作者")
    
    # 检测研究团队
    if args.find_teams:
        teams = analyzer.detect_research_teams()
        print(f"\n检测到{len(teams)}个研究团队:")
        for i, team in enumerate(teams[:5], 1):
            print(f"  团队{i}: {len(team)}人 - {', '.join(list(team)[:5])}...")
    
    # 导出网络
    analyzer.export_network(args.output, args.min_collab)
    print(f"\n网络已导出至: {args.output}")

if __name__ == '__main__':
    main()