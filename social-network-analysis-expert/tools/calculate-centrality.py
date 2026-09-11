"""
中心性分析工具
计算多种中心性指标
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Optional


def calculate_degree_centrality(G: nx.Graph, normalized: bool = True) -> Dict[str, float]:
    """
    计算度中心性
    
    参数:
        G: NetworkX 网络对象
        normalized: 是否归一化
    
    返回:
        度中心性字典 {node: centrality}
    """
    if G.is_directed():
        centrality = nx.degree_centrality(G)
    else:
        centrality = nx.degree_centrality(G)
    
    return centrality


def calculate_betweenness_centrality(G: nx.Graph, 
                                     normalized: bool = True,
                                     endpoints: bool = False) -> Dict[str, float]:
    """
    计算中介中心性
    
    参数:
        G: NetworkX 网络对象
        normalized: 是否归一化
        endpoints: 是否包含端点
    
    返回:
        中介中心性字典
    """
    centrality = nx.betweenness_centrality(G, normalized=normalized, endpoints=endpoints)
    return centrality


def calculate_closeness_centrality(G: nx.Graph,
                                   normalized: bool = True,
                                   wf_improved: bool = True) -> Dict[str, float]:
    """
    计算接近中心性
    
    参数:
        G: NetworkX 网络对象
        normalized: 是否归一化
        wf_improved: 是否使用 Wasserman-Faust 改进版本
    
    返回:
        接近中心性字典
    """
    centrality = nx.closeness_centrality(G)
    return centrality


def calculate_eigenvector_centrality(G: nx.Graph,
                                     max_iter: int = 1000,
                                     tol: float = 1e-06) -> Dict[str, float]:
    """
    计算特征向量中心性
    
    参数:
        G: NetworkX 网络对象
        max_iter: 最大迭代次数
        tol: 收敛容差
    
    返回:
        特征向量中心性字典
    """
    try:
        centrality = nx.eigenvector_centrality(G, max_iter=max_iter, tol=tol)
    except nx.PowerIterationFailedConvergence:
        # 如果不收敛, 返回空字典
        centrality = {node: 0.0 for node in G.nodes()}
    
    return centrality


def calculate_pagerank(G: nx.Graph,
                       alpha: float = 0.85,
                       personalization: Optional[Dict] = None,
                       max_iter: int = 100,
                       tol: float = 1e-06) -> Dict[str, float]:
    """
    计算 PageRank 中心性
    
    参数:
        G: NetworkX 网络对象
        alpha: 阻尼系数
        personalization: 个性化向量
        max_iter: 最大迭代次数
        tol: 收敛容差
    
    返回:
        PageRank 字典
    """
    centrality = nx.pagerank(G, alpha=alpha, personalization=personalization, 
                            max_iter=max_iter, tol=tol)
    return centrality


def calculate_katz_centrality(G: nx.Graph,
                              alpha: float = 0.1,
                              beta: float = 1.0,
                              max_iter: int = 1000,
                              tol: float = 1e-06) -> Dict[str, float]:
    """
    计算 Katz 中心性
    
    参数:
        G: NetworkX 网络对象
        alpha: 衰减因子
        beta: 权重
        max_iter: 最大迭代次数
        tol: 收敛容差
    
    返回:
        Katz 中心性字典
    """
    try:
        centrality = nx.katz_centrality(G, alpha=alpha, beta=beta, 
                                       max_iter=max_iter, tol=tol)
    except nx.PowerIterationFailedConvergence:
        centrality = {node: 0.0 for node in G.nodes()}
    
    return centrality


def calculate_all_centrality(G: nx.Graph) -> Dict:
    """
    计算所有中心性指标
    
    参数:
        G: NetworkX 网络对象
    
    返回:
        包含所有中心性指标的结果字典
    """
    results = {
        'degree_centrality': calculate_degree_centrality(G),
        'betweenness_centrality': calculate_betweenness_centrality(G),
        'closeness_centrality': calculate_closeness_centrality(G),
        'eigenvector_centrality': calculate_eigenvector_centrality(G),
        'pagerank': calculate_pagerank(G),
        'katz_centrality': calculate_katz_centrality(G)
    }
    
    # 生成排名
    ranking = generate_centrality_ranking(results)
    results['ranking'] = ranking
    
    return results


def generate_centrality_ranking(centrality_results: Dict) -> List[Dict]:
    """
    生成中心性排名
    
    参数:
        centrality_results: 中心性结果字典
    
    返回:
        排名列表
    """
    nodes = list(centrality_results['degree_centrality'].keys())
    
    ranking = []
    for node in nodes:
        node_ranking = {
            'node': node,
            'degree': centrality_results['degree_centrality'].get(node, 0),
            'betweenness': centrality_results['betweenness_centrality'].get(node, 0),
            'closeness': centrality_results['closeness_centrality'].get(node, 0),
            'eigenvector': centrality_results['eigenvector_centrality'].get(node, 0),
            'pagerank': centrality_results['pagerank'].get(node, 0),
            'katz': centrality_results['katz_centrality'].get(node, 0)
        }
        ranking.append(node_ranking)
    
    # 按综合得分排序
    for r in ranking:
        r['composite_score'] = (
            r['degree'] * 0.2 +
            r['betweenness'] * 0.2 +
            r['closeness'] * 0.2 +
            r['eigenvector'] * 0.2 +
            r['pagerank'] * 0.2
        )
    
    ranking.sort(key=lambda x: x['composite_score'], reverse=True)
    
    # 添加排名
    for i, r in enumerate(ranking):
        r['rank'] = i + 1
    
    return ranking


def validate_centrality(centrality_results: Dict) -> Dict:
    """
    验证中心性计算结果
    
    参数:
        centrality_results: 中心性结果字典
    
    返回:
        验证结果
    """
    issues = []
    
    # 检查值范围 (应该在 0-1 之间)
    for metric_name, centrality in centrality_results.items():
        if metric_name == 'ranking':
            continue
        
        for node, value in centrality.items():
            if value < 0 or value > 1:
                issues.append({
                    'code': 'CENTRALITY_OUT_OF_RANGE',
                    'message': f'{metric_name} 在节点 {node} 的值为 {value}, 超出 0-1 范围',
                    'severity': 'warning'
                })
    
    return {
        'valid': len([i for i in issues if i['severity'] == 'error']) == 0,
        'issues': issues
    }


if __name__ == '__main__':
    # 测试
    import networkx as nx
    
    # 创建测试网络
    G = nx.karate_club_graph()
    
    # 计算所有中心性
    results = calculate_all_centrality(G)
    
    print("中心性分析结果:")
    print(f"节点数：{G.number_of_nodes()}")
    print(f"边数：{G.number_of_edges()}")
    print("\n前 5 名节点:")
    for r in results['ranking'][:5]:
        print(f"  {r['node']}: 排名{r['rank']}, 综合得分{r['composite_score']:.3f}")
