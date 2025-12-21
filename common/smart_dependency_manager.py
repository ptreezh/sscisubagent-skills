"""
智能依赖管理模块

该模块提供智能的包依赖管理功能，优先使用高级包提供更强的功能，
如果高级包不可用或安装失败，则自动降级到基础功能实现。
"""

import importlib
import subprocess
import sys
import logging
from typing import Any, Callable, Dict, Optional, Tuple


def check_package_availability(package_name: str) -> bool:
    """检查包是否可用"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False


def install_package(package_name: str) -> bool:
    """尝试安装包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False


def smart_import_with_fallback(
    primary_package: str, 
    fallback_function: Optional[Callable] = None,
    alternative_package: Optional[str] = None
) -> Tuple[Any, bool]:
    """
    智能导入，支持降级
    
    Args:
        primary_package: 主要包名
        fallback_function: 降级时使用的函数
        alternative_package: 替代包名
    
    Returns:
        (导入的对象或降级函数, 是否使用了高级功能)
    """
    # 首先尝试导入主要包
    try:
        module = importlib.import_module(primary_package)
        return module, True
    except ImportError:
        pass
    
    # 如果有替代包，尝试导入替代包
    if alternative_package:
        try:
            module = importlib.import_module(alternative_package)
            return module, True
        except ImportError:
            pass
    
    # 如果有降级函数，返回降级函数
    if fallback_function:
        return fallback_function, False
    
    # 如果都没有，抛出异常
    raise ImportError(f"无法导入 {primary_package} 或其替代品")


def attempt_install_and_import(
    package_name: str,
    import_name: Optional[str] = None,
    fallback_function: Optional[Callable] = None
) -> Tuple[Any, bool]:
    """
    尝试安装并导入包，失败则使用降级功能
    
    Args:
        package_name: 要安装的包名
        import_name: 导入时使用的名称（如果与包名不同）
        fallback_function: 降级时使用的函数
    
    Returns:
        (导入的对象或降级函数, 是否使用了高级功能)
    """
    if import_name is None:
        import_name = package_name
    
    # 首先检查是否已安装
    try:
        module = importlib.import_module(import_name)
        return module, True
    except ImportError:
        pass
    
    # 尝试安装
    print(f"正在尝试安装 {package_name}...")
    success = install_package(package_name)
    
    if success:
        try:
            module = importlib.import_module(import_name)
            print(f"✓ 成功安装并导入 {package_name}")
            return module, True
        except ImportError:
            print(f"⚠️  安装成功但无法导入 {import_name}")
    
    # 如果安装失败或无法导入，返回降级函数
    if fallback_function:
        print(f"ℹ️  降级到基础功能实现")
        return fallback_function, False
    else:
        raise ImportError(f"无法安装和导入 {package_name}，也没有提供降级功能")


# 预定义的包依赖映射
PACKAGE_DEPENDENCIES = {
    'statistics': {
        'advanced': ['statsmodels', 'pingouin'],
        'fallback': 'scipy.stats'  # 使用scipy作为基础统计功能
    },
    'network_analysis': {
        'advanced': ['networkx', 'igraph'],
        'fallback': 'built_in_algorithms'  # 使用内置算法
    },
    'machine_learning': {
        'advanced': ['scikit-learn', 'xgboost'],
        'fallback': 'basic_ml_algorithms'  # 使用基础算法实现
    },
    'nlp': {
        'advanced': ['transformers', 'spacy'],
        'fallback': 'basic_text_processing'  # 使用基础文本处理
    }
}


def get_available_packages_for_domain(domain: str) -> Dict[str, bool]:
    """获取特定领域可用的包"""
    if domain not in PACKAGE_DEPENDENCIES:
        return {}
    
    available = {}
    for pkg in PACKAGE_DEPENDENCIES[domain]['advanced']:
        available[pkg] = check_package_availability(pkg)
    
    return available


def initialize_domain_with_fallbacks(domain: str):
    """初始化特定领域，自动处理依赖包和降级"""
    if domain not in PACKAGE_DEPENDENCIES:
        return None
    
    deps = PACKAGE_DEPENDENCIES[domain]
    
    # 检查高级包的可用性
    available_advanced = []
    for pkg in deps['advanced']:
        if check_package_availability(pkg):
            available_advanced.append(pkg)
    
    if available_advanced:
        # 导入可用的高级包
        modules = {}
        for pkg in available_advanced:
            try:
                modules[pkg] = importlib.import_module(pkg)
            except ImportError:
                continue
        return modules, True
    else:
        # 使用降级功能
        print(f"⚠️  {domain} 领域的高级包不可用，使用降级功能")
        return deps.get('fallback'), False


# 通用的统计分析函数，使用智能依赖管理
def smart_statistical_analysis(data: list, analysis_type: str = "descriptive"):
    """智能统计分析，根据可用包选择最佳实现"""
    if analysis_type == "descriptive":
        # 尝试使用高级统计包
        try:
            # 优先尝试statsmodels
            statsmodels_available = check_package_availability("statsmodels")
            if statsmodels_available:
                import statsmodels.api as sm
                import pandas as pd
                import numpy as np
                
                series = pd.Series(data)
                desc = series.describe()
                
                # 添加额外统计量
                result = {
                    'count': int(desc['count']),
                    'mean': float(desc['mean']),
                    'std': float(desc['std']),
                    'min': float(desc['min']),
                    'max': float(desc['max']),
                    '25%': float(desc['25%']),
                    '50%': float(desc['50%']),
                    '75%': float(desc['75%']),
                    'skewness': float(sm.stats.stattools.robust.robust_skew_2d(data)[0]),
                    'kurtosis': float(sm.stats.stattools.robust.robust_kurt_2d(data)[0])
                }
                return result, True  # 使用了高级功能
        except:
            pass
        
        # 尝试使用scipy
        try:
            import scipy.stats as stats
            import numpy as np
            
            result = {
                'count': len(data),
                'mean': float(np.mean(data)),
                'std': float(np.std(data)),
                'min': float(np.min(data)),
                'max': float(np.max(data)),
                'skewness': float(stats.skew(data)),
                'kurtosis': float(stats.kurtosis(data))
            }
            return result, True  # 使用了高级功能
        except:
            pass
        
        # 降级到基础实现
        print("ℹ️  降级到基础统计实现")
        result = {}
        if data:
            result['count'] = len(data)
            result['mean'] = sum(data) / len(data)
            result['min'] = min(data)
            result['max'] = max(data)
            
            # 计算标准差
            mean_val = result['mean']
            variance = sum((x - mean_val) ** 2 for x in data) / (len(data) - 1) if len(data) > 1 else 0
            result['std'] = variance ** 0.5
            
            # 简单的偏度和峰度估算
            result['skewness'] = 0  # 降级实现中暂时为0
            result['kurtosis'] = 0  # 降级实现中暂时为0
        return result, False  # 使用了基础功能


# 通用的网络分析函数，使用智能依赖管理
def smart_network_analysis(edges: list, nodes: Optional[list] = None, analysis_type: str = "basic"):
    """智能网络分析，根据可用包选择最佳实现"""
    networkx_available = check_package_availability("networkx")
    
    if networkx_available and analysis_type != "basic":
        try:
            import networkx as nx
            
            G = nx.Graph()
            if nodes:
                G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            
            result = {
                'num_nodes': G.number_of_nodes(),
                'num_edges': G.number_of_edges(),
                'density': nx.density(G),
                'is_connected': nx.is_connected(G),
                'components': nx.number_connected_components(G)
            }
            
            if G.number_of_nodes() > 0:
                result['avg_clustering'] = nx.average_clustering(G)
                if nx.is_connected(G):
                    result['avg_shortest_path'] = nx.average_shortest_path_length(G)
                else:
                    # 对于非连通图，计算各连通分量的平均最短路径
                    components = [G.subgraph(c) for c in nx.connected_components(G)]
                    avg_paths = [nx.average_shortest_path_length(comp) for comp in components if comp.number_of_nodes() > 1]
                    result['avg_shortest_path'] = sum(avg_paths) / len(avg_paths) if avg_paths else float('inf')

                # 中心性指标（仅当节点数大于1时计算）
                if G.number_of_nodes() > 1:
                    result['centrality'] = {
                        'degree': dict(nx.degree_centrality(G)),
                        'betweenness': dict(nx.betweenness_centrality(G)),
                        'closeness': dict(nx.closeness_centrality(G)),
                        'eigenvector': dict(nx.eigenvector_centrality(G, max_iter=1000))
                    }
            
            return result, True  # 使用了高级功能
        except Exception as e:
            print(f"⚠️  NetworkX分析失败: {e}，降级到基础实现")
    
    # 降级到基础实现
    print("ℹ️  降级到基础网络分析实现")
    node_set = set()
    for edge in edges:
        node_set.add(edge[0])
        node_set.add(edge[1])
    
    if nodes:
        node_set.update(nodes)
    
    # 基础网络指标计算
    n_nodes = len(node_set)
    n_edges = len(edges)
    density = n_edges / (n_nodes * (n_nodes - 1) / 2) if n_nodes > 1 else 0
    
    return {
        'num_nodes': n_nodes,
        'num_edges': n_edges,
        'density': density,
        'nodes': list(node_set),
        'edges': edges
    }, False  # 使用了基础功能


if __name__ == "__main__":
    # 测试智能依赖管理
    print("Testing smart dependency management...")
    
    # 测试统计分析
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    stats_result, using_advanced_stats = smart_statistical_analysis(test_data)
    print(f"Statistical analysis - Using advanced: {using_advanced_stats}, Result: {stats_result}")
    
    # 测试网络分析
    test_edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D')]
    network_result, using_advanced_network = smart_network_analysis(test_edges)
    print(f"Network analysis - Using advanced: {using_advanced_network}, Nodes: {network_result['num_nodes']}")