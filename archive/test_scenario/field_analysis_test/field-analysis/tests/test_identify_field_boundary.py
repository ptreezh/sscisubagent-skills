"""
场域边界识别工具的单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from identify_field_boundary import (
    identify_core_participants,
    analyze_field_rules,
    assess_autonomy
)


class TestIdentifyCoreParticipants:
    """测试核心参与者识别"""
    
    def test_basic_identification(self):
        """测试基本识别"""
        data = [
            {
                'participant': {
                    'name': '张三',
                    'education': '博士',
                    'position': '教授',
                    'influence': 0.9
                }
            },
            {
                'participant': {
                    'name': '李四',
                    'education': '硕士',
                    'position': '讲师',
                    'influence': 0.6
                }
            },
            {
                'participant': {
                    'name': '王五',
                    'education': '本科',
                    'position': '助教',
                    'influence': 0.3
                }
            }
        ]
        
        result = identify_core_participants(data, threshold=0.5)
        
        assert result['n_core'] == 2
        assert result['n_peripheral'] == 1
        assert len(result['core_participants']) == 2
        assert len(result['peripheral_participants']) == 1
        assert result['influence_threshold'] == 2.4
    
    def test_high_threshold(self):
        """测试高阈值"""
        data = [
            {'participant': {'name': 'P1', 'influence': 0.9}},
            {'participant': {'name': 'P2', 'influence': 0.8}},
            {'participant': {'name': 'P3', 'influence': 0.7}},
            {'participant': {'name': 'P4', 'influence': 0.6}}
        ]
        
        result = identify_core_participants(data, threshold=0.7)
        
        assert result['n_core'] == 3
        assert result['n_peripheral'] == 1
        assert result['influence_threshold'] == 0.7
    
    def test_no_data(self):
        """测试无数据"""
        result = identify_core_participants([])
        
        assert result['n_core'] == 0
        assert result['n_peripheral'] == 0
        assert result['influence_threshold'] == 0.0


class TestAnalyzeFieldRules:
    """测试场域规则分析"""
    
    def test_basic_analysis(self):
        """测试基本分析"""
        data = [
            {
                'participant': {
                    'name': '张三',
                    'education': '博士',
                    'position': '教授'
                }
            },
            {
                'participant': {
                    'name': '李四',
                    'education': '硕士',
                    'position': '讲师'
                }
            }
        ]
        
        result = analyze_field_rules(data, [])
        
        assert 'rules' in result
        assert 'analysis' in result
        assert 'rule_strength' in result
    
    def test_rule_strength_counting(self):
        """测试规则强度统计"""
        data = [
            {
                'participant': {
                    'name': '张三',
                    'education': '博士',
                    'position': '教授',
                    'publications': 10
                }
            } * 5  # 5个教授，都有出版物
        ]
        
        result = analyze_field_rules(data, [])
        
        assert result['rule_strength']['strong'] == 5
        assert result['rule_strength']['moderate'] == 0
        assert result['rule_strength']['weak'] == 0


class TestAssessAutonomy:
    """测试自主性评估"""
    
    def test_high_autonomy(self):
        """测试高自主性"""
        data = [
            {'participant': {'internal_decision_making': 0.9, 'self_governance': 0.8}},
            {'participant': {'internal_decision_making': 0.8, 'self_governance': 0.7}}
        ]
        
        result = assess_autonomy(data)
        
        assert result['autonomy_index'] > 0.7
        assert result['autonomy_level'] in ['高度自主', '中等自主']
        assert result['n_participants'] == 2
    
    def test_low_autonomy(self):
        """测试低自主性"""
        data = [
            {'participant': {'internal_decision_making': 0.3, 'self_governance': 0.2}},
            {'participant': {'internal_decision_making': 0.4, 'self_governance': 0.3}}
        ]
        
        result = assess_autonomy(data)
        
        assert result['autonomy_index'] < 0.5
        assert result['autonomy_level'] in ['低度自主', '高度依赖']
    
    def test_external_factors(self):
        """测试外部因素影响"""
        result = assess_autonomy([], {
            'political_pressure': 0.5,
            'market_forces': 0.3
        })
        
        assert result['autonomy_index'] == 0.2
        assert result['autonomy_level'] == '高度依赖'
        assert result['n_participants'] == 0


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])