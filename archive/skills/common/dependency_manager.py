"""
通用依赖包管理器

提供高级依赖包的自动安装和优雅降级机制
支持多种依赖包的检查、安装和降级
"""

import importlib
import subprocess
import sys
from typing import Dict, List, Callable, Any
from functools import wraps


class DependencyManager:
    """
    依赖包管理器
    提供高级依赖包的自动安装和优雅降级机制
    """
    
    def __init__(self):
        self.installed_packages = {}
        self.failed_packages = set()
    
    def check_and_install(self, package_name: str, import_name: str = None) -> bool:
        """
        检查并尝试安装包
        
        Args:
            package_name: 要安装的包名
            import_name: 导入时使用的名称（如果与包名不同）
            
        Returns:
            bool: 是否成功安装或已存在
        """
        if import_name is None:
            import_name = package_name
            
        # 如果已安装或失败过，直接返回结果
        if import_name in self.installed_packages:
            return self.installed_packages[import_name]
        if import_name in self.failed_packages:
            return False
        
        try:
            # 检查是否已安装
            importlib.import_module(import_name)
            self.installed_packages[import_name] = True
            return True
        except ImportError:
            # 尝试安装
            print(f"正在安装 {package_name}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package_name
                ])
                # 再次检查是否安装成功
                importlib.import_module(import_name)
                self.installed_packages[import_name] = True
                return True
            except subprocess.CalledProcessError:
                print(f"无法安装 {package_name}")
                self.failed_packages.add(import_name)
                return False
            except ImportError:
                print(f"安装后仍无法导入 {import_name}")
                self.failed_packages.add(import_name)
                return False
    
    def require_packages(self, packages: List[tuple]) -> Dict[str, bool]:
        """
        批量检查和安装多个包
        
        Args:
            packages: 包列表，每个元素为 (package_name, import_name) 元组
            
        Returns:
            Dict: 包名到安装状态的映射
        """
        results = {}
        for pkg_info in packages:
            if isinstance(pkg_info, tuple):
                package_name, import_name = pkg_info
            else:
                package_name = import_name = pkg_info
            
            results[import_name] = self.check_and_install(package_name, import_name)
        
        return results
    
    def get_availability(self) -> Dict[str, bool]:
        """获取所有检查过的包的可用性"""
        return {**self.installed_packages, **{pkg: False for pkg in self.failed_packages}}


# 创建全局依赖管理器实例
dep_manager = DependencyManager()


def with_fallback(fallback_func: Callable):
    """
    装饰器：当高级功能不可用时自动降级到基础实现
    
    Args:
        fallback_func: 降级时调用的基础函数
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # 获取函数需要的依赖
                required_deps = getattr(func, '_required_deps', [])
                
                # 检查依赖
                all_available = True
                for dep in required_deps:
                    if not dep_manager.check_and_install(dep):
                        all_available = False
                        break
                
                if all_available:
                    # 尝试执行高级功能
                    try:
                        result = func(*args, **kwargs)
                        # 添加使用高级功能的标记
                        if isinstance(result, dict):
                            result['using_advanced'] = True
                        return result
                    except Exception as e:
                        print(f"高级功能执行出错: {e}，使用降级方案")
                        return fallback_func(*args, **kwargs)
                else:
                    # 依赖不可用，使用降级方案
                    return fallback_func(*args, **kwargs)
            except Exception as e:
                print(f"函数执行出错: {e}，使用降级方案")
                return fallback_func(*args, **kwargs)
        
        return wrapper
    return decorator


def requires_dependencies(*deps):
    """
    装饰器：标记函数需要的依赖包
    
    Args:
        *deps: 依赖包名称列表
    """
    def decorator(func):
        func._required_deps = deps
        return func
    return decorator


# 示例：高级统计函数和降级实现
def basic_mean(data: List[float]) -> float:
    """基础均值计算"""
    if not data:
        return 0
    return sum(data) / len(data)


@requires_dependencies('numpy', 'pandas')
def advanced_mean(data: List[float]) -> float:
    """高级均值计算"""
    import numpy as np
    return float(np.mean(data))


# 使用装饰器的高级均值函数
@with_fallback(basic_mean)
def smart_mean(data: List[float]) -> float:
    """智能均值计算：优先使用高级实现，失败时降级"""
    return advanced_mean(data)


# 示例：高级网络分析函数和降级实现
def basic_network_density(nodes: int, edges: int) -> float:
    """基础网络密度计算"""
    if nodes < 2:
        return 0.0
    max_possible_edges = nodes * (nodes - 1)  # 有向图
    return edges / max_possible_edges if max_possible_edges > 0 else 0


@requires_dependencies('networkx')
def advanced_network_density(nodes: int, edges: int) -> float:
    """高级网络密度计算"""
    import networkx as nx
    # 创建一个简单的图来计算密度
    G = nx.DiGraph()
    for i in range(min(nodes, 100)):  # 限制节点数以避免内存问题
        G.add_node(i)
    for i in range(min(edges, nodes*(nodes-1))):  # 限制边数
        source = i % nodes if nodes > 0 else 0
        target = (i + 1) % nodes if nodes > 0 else 0
        G.add_edge(source, target)
    return nx.density(G)


# 使用装饰器的智能网络密度函数
@with_fallback(basic_network_density)
def smart_network_density(nodes: int, edges: int) -> float:
    """智能网络密度计算：优先使用高级实现，失败时降级"""
    return advanced_network_density(nodes, edges)


# 通用工具函数
def install_required_packages(packages: List[tuple]) -> Dict[str, bool]:
    """
    安装所需的包
    
    Args:
        packages: 包列表，每个元素为 (package_name, import_name) 元组
        
    Returns:
        Dict: 安装结果
    """
    return dep_manager.require_packages(packages)


def get_package_availability() -> Dict[str, bool]:
    """获取包可用性信息"""
    return dep_manager.get_availability()


def ensure_package(package_name: str, import_name: str = None) -> bool:
    """
    确保包已安装
    
    Args:
        package_name: 包名
        import_name: 导入名（可选）
        
    Returns:
        bool: 是否成功
    """
    return dep_manager.check_and_install(package_name, import_name)


# 预定义的包需求配置
PACKAGE_REQUIREMENTS = {
    'statistics': [
        ('statsmodels', 'statsmodels'),
        ('pingouin', 'pingouin'),
        ('scikit-learn', 'sklearn'),
        ('factor-analyzer', 'factor_analyzer')
    ],
    'network_analysis': [
        ('networkx', 'networkx'),
        ('igraph', 'igraph')  # 可选
    ],
    'data_processing': [
        ('pandas', 'pandas'),
        ('numpy', 'numpy')
    ],
    'machine_learning': [
        ('scikit-learn', 'sklearn'),
        ('tensorflow', 'tensorflow'),  # 可选
        ('pytorch', 'torch')  # 可选
    ]
}


def install_skill_packages(skill_type: str) -> Dict[str, bool]:
    """
    为特定技能类型安装所需的包
    
    Args:
        skill_type: 技能类型
        
    Returns:
        Dict: 安装结果
    """
    if skill_type in PACKAGE_REQUIREMENTS:
        return install_required_packages(PACKAGE_REQUIREMENTS[skill_type])
    else:
        print(f"未知的技能类型: {skill_type}")
        return {}


if __name__ == "__main__":
    # 示例使用
    print("=== 依赖管理器测试 ===")
    
    # 测试包安装
    print("1. 测试安装pandas:")
    pandas_available = ensure_package('pandas', 'pandas')
    print(f"   Pandas 可用: {pandas_available}")
    
    print("\n2. 测试智能函数:")
    test_data = [1, 2, 3, 4, 5]
    mean_result = smart_mean(test_data)
    print(f"   智能均值计算结果: {mean_result}")
    
    print("\n3. 测试网络分析:")
    density_result = smart_network_density(10, 15)
    print(f"   智能网络密度计算结果: {density_result}")
    
    print("\n4. 包可用性:")
    availability = get_package_availability()
    for pkg, available in availability.items():
        print(f"   {pkg}: {'✓' if available else '✗'}")
    
    print("\n5. 安装统计分析包:")
    stats_results = install_skill_packages('statistics')
    for pkg, success in stats_results.items():
        print(f"   {pkg}: {'✓' if success else '✗'}")