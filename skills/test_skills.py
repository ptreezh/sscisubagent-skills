"""
Test Suite for Claude Code Skills
Claude Code技能测试套件
"""

import unittest
import pandas as pd
import numpy as np
import os
import sys

# Add the scripts directories to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'mathematical-statistics', 'scripts'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'validity-reliability', 'scripts'))

class TestMathematicalStatisticsSkill(unittest.TestCase):
    """数理统计技能测试"""
    
    def setUp(self):
        """测试设置"""
        from simplified_statistics import SimplifiedStatistics
        self.analyzer = SimplifiedStatistics()
        
        # 创建测试数据
        import random
        random.seed(42)
        n = 100
        self.test_data = [random.gauss(35, 10) for _ in range(n)]
        self.analyzer.load_data(data_list=self.test_data)
    
    def test_data_loading(self):
        """测试数据加载"""
        self.assertIsNotNone(self.analyzer.data)
        self.assertEqual(len(self.analyzer.data['values']), 100)
    
    def test_descriptive_statistics(self):
        """测试描述性统计"""
        result = self.analyzer.descriptive_statistics()
        
        # 检查结果结构
        required_keys = ['count', 'mean', 'median', 'std', 'min', 'max']
        for key in required_keys:
            self.assertIn(key, result)
        
        # 检查数值合理性
        self.assertTrue(20 < result['mean'] < 50)
        self.assertTrue(result['count'] == 100)
        self.assertTrue(result['min'] < result['mean'] < result['max'])
    
    def test_hypothesis_testing(self):
        """测试假设检验"""
        # 单样本t检验
        result = self.analyzer.t_test_one_sample('values', 40, alpha=0.05)
        
        # 检查结果结构
        required_keys = ['test', 'sample_size', 'sample_mean', 't_statistic', 'p_value']
        for key in required_keys:
            self.assertIn(key, result)
        
        # 检查数值类型
        self.assertIsInstance(result['t_statistic'], (int, float))
        self.assertIsInstance(result['p_value'], (int, float))
        self.assertTrue(0 <= result['p_value'] <= 1)

class TestValidityReliabilitySkill(unittest.TestCase):
    """信度效度技能测试"""
    
    def setUp(self):
        """测试设置"""
        from simplified_validity_reliability import SimplifiedValidityReliability
        self.analyzer = SimplifiedValidityReliability()
        
        # 创建测试量表数据
        import random
        random.seed(42)
        n = 50
        self.test_data = {
            'item1': [random.randint(1, 5) for _ in range(n)],
            'item2': [random.randint(1, 5) for _ in range(n)],
            'item3': [random.randint(1, 5) for _ in range(n)],
            'item4': [random.randint(1, 5) for _ in range(n)],
            'item5': [random.randint(1, 5) for _ in range(n)]
        }
        
        self.analyzer.load_data(self.test_data)
    
    def test_data_loading(self):
        """测试数据加载"""
        self.assertIsNotNone(self.analyzer.data)
        self.assertEqual(len(self.analyzer.data['item1']), 50)
        self.assertEqual(len(self.analyzer.data), 5)
    
    def test_reliability_analysis(self):
        """测试信度分析"""
        items = list(self.test_data.keys())
        result = self.analyzer.cronbach_alpha(items)
        
        # 检查结果结构
        required_keys = ['alpha', 'n_items', 'n_respondents', 'interpretation']
        for key in required_keys:
            self.assertIn(key, result)
        
        # 检查数值合理性
        self.assertTrue(0 <= result['alpha'] <= 1)
        self.assertTrue(result['n_items'] == len(items))
        self.assertIsInstance(result['interpretation'], str)
    
    def test_construct_validity_analysis(self):
        """测试构念效度分析（简化版）"""
        items = list(self.test_data.keys())
        
        # 测试项目-总分相关
        result = self.analyzer.item_total_correlation(items)
        
        # 检查结果结构
        for item in items:
            self.assertIn(item, result)
            self.assertIsInstance(result[item], (int, float))
            self.assertTrue(-1 <= result[item] <= 1)
        
        # 测试分半信度
        split_half_result = self.analyzer.split_half_reliability(items)
        
        # 检查结果结构
        required_keys = ['split_half', 'correlation', 'interpretation']
        for key in required_keys:
            self.assertIn(key, split_half_result)
        
        self.assertTrue(0 <= split_half_result['split_half'] <= 1)

class TestSkillStructure(unittest.TestCase):
    """技能结构测试"""
    
    def test_skill_file_structure(self):
        """测试技能文件结构"""
        base_path = os.path.dirname(__file__)
        
        # 检查技能目录
        skills = ['mathematical-statistics', 'validity-reliability', 'conflict-resolution', 'network-computation']
        
        for skill in skills:
            skill_path = os.path.join(base_path, skill)
            self.assertTrue(os.path.exists(skill_path), f"技能目录 {skill} 不存在")
            
            # 检查SKILL.md文件
            skill_md = os.path.join(skill_path, 'SKILL.md')
            self.assertTrue(os.path.exists(skill_md), f"SKILL.md文件在 {skill} 中不存在")
            
            # 检查scripts目录（对于有编程脚本的技能）
            if skill in ['mathematical-statistics', 'validity-reliability']:
                scripts_path = os.path.join(base_path, skill, 'scripts')
                self.assertTrue(os.path.exists(scripts_path), f"scripts目录在 {skill} 中不存在")
    
    def test_skill_metadata(self):
        """测试技能元数据"""
        base_path = os.path.dirname(__file__)
        
        skills = ['mathematical-statistics', 'validity-reliability', 'conflict-resolution', 'network-computation']
        
        for skill in skills:
            skill_md = os.path.join(base_path, skill, 'SKILL.md')
            
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查YAML frontmatter
            self.assertIn('---', content)
            self.assertIn('name:', content)
            self.assertIn('description:', content)
            self.assertIn('version:', content)
            self.assertIn('author:', content)
            self.assertIn('tags:', content)
            
            # 检查技能描述
            self.assertIn('## 技能概述', content)
            self.assertIn('## 核心功能', content)
            self.assertIn('## 使用方法', content)

def run_skill_tests():
    """运行所有技能测试"""
    print("开始运行Claude Code技能测试套件...")
    print("=" * 50)
    
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加测试用例
    suite.addTest(unittest.makeSuite(TestMathematicalStatisticsSkill))
    suite.addTest(unittest.makeSuite(TestValidityReliabilitySkill))
    suite.addTest(unittest.makeSuite(TestSkillStructure))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果总结:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\n测试成功率: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("✅ 技能测试整体通过！")
    else:
        print("❌ 技能测试需要改进！")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_skill_tests()
