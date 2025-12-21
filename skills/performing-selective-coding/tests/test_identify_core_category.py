"""
核心范畴识别工具的单元测试
"""

import sys
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from identify_core_category import (
    calculate_explanatory_power,
    calculate_connectivity,
    calculate_data_support,
    rank_categories,
    validate_core_category
)


class TestCalculateExplanatoryPower:
    """测试解释力计算"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
        category = {'data_support': 30}
        all_data = [
            {'data_support': 30},
            {'data_support': 20},
            {'data_support': 50}
        ]
        
        result = calculate_explanatory_power(category, all_data)
        assert result == 0.3  # 30/100
    
    def test_zero_total(self):
        """测试总数为0的情况"""
        category = {'data_support': 0}
        all_data = []
        
        result = calculate_explanatory_power(category, all_data)
        assert result == 0.0


class TestCalculateConnectivity:
    """测试连接度计算"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
        category = {'id': 'C1', 'name': '范畴1'}
        relations = [
            {'source': 'C1', 'target': 'C2'},
            {'source': 'C2', 'target': 'C1'},
            {'source': 'C2', 'target': 'C3'}
        ]
        
        result = calculate_connectivity(category, relations)
        assert result == 2/3  # 2个关系涉及C1，总共3个关系
    
    def test_no_relations(self):
        """测试无关系的情况"""
        category = {'id': 'C1'}
        relations = []
        
        result = calculate_connectivity(category, relations)
        assert result == 0.0


class TestCalculateDataSupport:
    """测试数据支持度计算"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
        category = {'data_support': 40}
        all_data = [
            {'data_support': 50},  # 最大值
            {'data_support': 40},
            {'data_support': 30}
        ]
        
        result = calculate_data_support(category, all_data)
        assert result == 0.8  # 40/50


class TestRankCategories:
    """测试范畴排序"""
    
    def test_basic_ranking(self):
        """测试基本排序"""
        categories = [
            {'id': 'C1', 'name': '范畴1', 'data_support': 30},
            {'id': 'C2', 'name': '范畴2', 'data_support': 50},
            {'id': 'C3', 'name': '范畴3', 'data_support': 20}
        ]
        relations = [
            {'source': 'C2', 'target': 'C1'},
            {'source': 'C2', 'target': 'C3'}
        ]
        
        result = rank_categories(categories, relations)
        
        # C2应该排第一（数据支持最多，连接度最高）
        assert result[0]['id'] == 'C2'
        assert 'scores' in result[0]
        assert 'overall' in result[0]['scores']


class TestValidateCoreCategory:
    """测试核心范畴验证"""
    
    def test_valid_category(self):
        """测试有效的核心范畴"""
        category = {
            'scores': {
                'explanatory_power': 0.30,
                'connectivity': 0.40,
                'data_support': 0.80,
                'overall': 0.70
            }
        }
        criteria = {
            'min_explanatory': 0.15,
            'min_connectivity': 0.20,
            'min_data_support': 0.50,
            'min_overall': 0.60
        }
        
        is_valid, issues = validate_core_category(category, criteria)
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_invalid_category(self):
        """测试无效的核心范畴"""
        category = {
            'scores': {
                'explanatory_power': 0.10,  # 不足
                'connectivity': 0.15,  # 不足
                'data_support': 0.80,
                'overall': 0.50  # 不足
            }
        }
        criteria = {
            'min_explanatory': 0.15,
            'min_connectivity': 0.20,
            'min_data_support': 0.50,
            'min_overall': 0.60
        }
        
        is_valid, issues = validate_core_category(category, criteria)
        
        assert is_valid is False
        assert len(issues) == 3  # 解释力、连接度、综合分数不足


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
