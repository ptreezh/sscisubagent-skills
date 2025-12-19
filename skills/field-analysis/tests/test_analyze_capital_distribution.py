"""
资本分布分析工具的单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analyze_capital_distribution import (
    analyze_cultural_capital,
    analyze_social_capital,
    analyze_symbolic_capital,
    analyze_economic_capital
)


class TestCulturalCapital:
    """测试文化资本分析"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
        data = [
            {
                'participant': 'P1',
                'education': '硕士',
                'skills': ['Python', 'R', '论文写作', '数据分析'],
                'cultural_activities': ['读书', '听音乐会', '看展览']
            },
            {
                'participant': 'P2',
                'education': '博士',
                'skills': ['机器学习', '深度学习', 'NLP'],
                'cultural_activities': ['读书', '学术会议']
            }
        ]
        
        result = analyze_cultural_capital(data)
        
        assert result['type'] == 'cultural'
        assert result['n_participants'] == 2
        assert 0 <= result['mean'] <= 1.0
        assert 'distribution' in result
        assert 'inequality_gini' in result
    
    def test_high_cultural_capital(self):
        """测试高文化资本"""
        data = [
            {
                'participant': 'P1',
                'education': '博士',
                'skills': ['Python', 'R', '论文写作', '数据分析', '机器学习', '深度学习'],
                'cultural_activities': ['读书', '听音乐会', '看展览', '学术会议']
            },
            {
                'participant': 'P2',
                'education': '博士',
                'skills': ['机器学习', '深度学习', 'NLP', '论文写作'],
                'cultural_activities': ['读书', '学术会议']
            }
        ]
        
        result = analyze_cultural_capital(data)
        
        assert result['mean'] > 0.7
        assert result['distribution']['高'] >= 1
    
    def test_no_data(self):
        """测试无数据"""
        result = analyze_cultural_capital([])
        
        assert result['type'] == 'cultural'
        assert result['mean'] == 0.0
        assert result['n_participants'] == 0


class TestSocialCapital:
    """测试社会资本分析"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
        data = [
            {
                'participant': 'P1',
                'social_network': {'A': 0.8, 'B': 0.7, 'C': 0.6}
            },
            {
                'participant': 'P2',
                'social_network': {'A': 0.5, 'B': 0.4, 'C': 0.3}
            }
        ]
        
        result = analyze_social_capital(data)
        
        assert result['type'] == 'social'
        assert result['n_participants'] == 2
        assert 0 <= result['mean'] <= 1.0
        assert 'network_stats' in result
    
    def test_large_network(self):
        """测试大网络"""
        data = [
            {
                'participant': 'P1',
                'social_network': {f'P{i}': 0.5 for i in range(20)}
            }
        ]
        
        result = analyze_social_capital(data)
        
        assert result['mean'] > 0.5
        assert result['network_stats']['avg_size'] == 20.0


class TestSymbolicCapital:
    """测试象征资本分析"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
        data = [
            {
                'participant': 'P1',
                'prestige_score': 85,
                'recognitions': ['最佳论文奖', '优秀员工'],
                'honors': ['教授', '博导']
            },
            {
                'participant': 'P2',
                'prestige_score': 60,
                'recognitions': ['参与奖'],
                'honors': ['讲师']
            }
        ]
        
        result = analyze_symbolic_capital(data)
        
        assert result['type'] == 'symbolic'
        assert result['n_participants'] == 2
        assert result['mean'] > 0.5
        assert result['top_10_percent'] >= 0.0
    
    def test_high_recognition(self):
        """测试高认可度"""
        data = [
            {
                'participant': 'P1',
                'prestige_score': 95,
                'recognitions': ['诺奖', '院士', '最佳论文奖', '优秀员工'] * 3,
                'honors': ['教授', '博导', '院士']
            }
        ]
        
        result = analyze_symbolic_capital(data)
        
        assert result['mean'] > 0.8
        assert result['distribution']['高'] >= 1


class TestEconomicCapital:
    """测试经济资本分析"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
        data = [
            {
                'participant': 'P1',
                'annual_income': 100000,
                'total_assets': 1000000,
                'investments': 50000
            },
            {
                'participant': 'P2',
                'annual_income': 50000,
                'total_assets': 500000,
                'investments': 20000
            }
        ]
        
        result = analyze_economic_capital(data)
        
        assert result['type'] == 'economic'
        assert result['n_participants'] == 2
        assert 0 <= result['mean'] <= 1.0
        assert 'wealth_stats' in result
    
    def test_log_transformation(self):
        """测试对数转换处理"""
        data = [
            {
                'participant': 'P1',
                'annual_income': 1000000,
                'total_assets': 10000000,
                'investments': 100000
            }
        ]
        
        result = analyze_economic_capital(data)
        
        # 大数值应该被正确处理
        assert result['mean'] > 0
        assert result['wealth_stats']['avg_income'] == 1000000.0
        assert result['wealth_stats']['avg_assets'] == 10000000.0


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])