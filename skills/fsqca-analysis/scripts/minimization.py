#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模糊集定性比较分析(fsQCA) - 模糊逻辑最小化模块
实现模糊集的逻辑最小化算法
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any, Set
from dataclasses import dataclass
from enum import Enum
import itertools
from copy import deepcopy


class SolutionType(Enum):
    """解类型枚举"""
    COMPLEX = "complex"      # 复杂解
    INTERMEDIATE = "intermediate"  # 中间解
    PRIMED = "primed"        # 简约解


@dataclass
class FSCSolution:
    """模糊集解数据类"""
    solution_type: SolutionType
    expression: str
    prime_implicants: List[str]
    coverage: float
    consistency: float
    complexity: int
    frequency: float
    raw_solution: Any = None  # 原始解对象


class FSCMinimizer:
    """模糊集逻辑最小化器"""
    
    def __init__(self):
        self.solutions = []
        self.properties = {}
    
    def minimize(
        self,
        truth_table: pd.DataFrame,
        conditions: List[str],
        incl_threshold: float = 0.8,
        PRI_threshold: float = 0.75,
        include_remainders: bool = True
    ) -> List[FSCSolution]:
        """
        执行模糊集逻辑最小化
        
        Args:
            truth_table: 模糊真值表
            conditions: 条件变量列表
            incl_threshold: 包含阈值
            PRI_threshold: PRI阈值
            include_remainders: 是否包含逻辑余项
        
        Returns:
            解列表
        """
        # 首先处理真值表，提取逻辑蕴含项
        prime_implicants = self._extract_prime_implicants(
            truth_table, conditions, incl_threshold, PRI_threshold
        )
        
        # 生成不同类型的解
        solutions = []
        
        # 复杂解（包含所有原始信息）
        complex_solution = self._generate_complex_solution(
            prime_implicants, truth_table, conditions
        )
        solutions.append(complex_solution)
        
        # 简约解（去除冗余项）
        primed_solution = self._generate_primed_solution(
            prime_implicants, truth_table, conditions
        )
        solutions.append(primed_solution)
        
        # 中间解（结合理论知识）
        intermediate_solution = self._generate_intermediate_solution(
            primed_solution, truth_table, conditions
        )
        solutions.append(intermediate_solution)
        
        self.solutions = solutions
        return solutions
    
    def _extract_prime_implicants(
        self,
        truth_table: pd.DataFrame,
        conditions: List[str],
        incl_threshold: float,
        PRI_threshold: float
    ) -> List[Dict[str, Any]]:
        """
        提取质蕴含项
        
        Args:
            truth_table: 真值表
            conditions: 条件变量列表
            incl_threshold: 包含阈值
            PRI_threshold: PRI阈值
        
        Returns:
            质蕴含项列表
        """
        prime_implicants = []
        
        # 选择符合条件的行作为初始蕴含项
        valid_rows = truth_table[
            (truth_table['consistency'] >= incl_threshold) &
            (truth_table['PRI_consistency'] >= PRI_threshold) &
            (truth_table['outcome'] >= 0.5)  # 只考虑结果为正的配置
        ]
        
        for idx, row in valid_rows.iterrows():
            # 从配置创建蕴含项
            config = row['configuration']
            if isinstance(config, (list, tuple)):
                config_dict = {conditions[i]: config[i] for i in range(len(conditions))}
            else:
                # 如果配置是单个值，需要特殊处理
                config_dict = {conditions[0]: config}
            
            # 计算该蕴含项的覆盖度和一致性
            coverage = row['coverage'] if 'coverage' in row else row['frequency'] / truth_table['frequency'].sum()
            consistency = row['consistency']
            
            prime_implicant = {
                'config': config_dict,
                'coverage': coverage,
                'consistency': consistency,
                'frequency': row['frequency'],
                'cases': row['cases']
            }
            
            prime_implicants.append(prime_implicant)
        
        return prime_implicants
    
    def _generate_complex_solution(
        self,
        prime_implicants: List[Dict[str, Any]],
        truth_table: pd.DataFrame,
        conditions: List[str]
    ) -> FSCSolution:
        """生成复杂解"""
        # 复杂解包含所有原始的质蕴含项
        expression_parts = []
        
        for implicant in prime_implicants:
            # 将配置转换为表达式
            config_parts = []
            for condition, value in implicant['config'].items():
                if value == 1:
                    config_parts.append(condition)
                else:
                    config_parts.append(f"~{condition}")  # 否定条件
            
            expression_parts.append(f"({' * '.join(config_parts)})")
        
        expression = ' + '.join(expression_parts)
        
        # 计算整体覆盖度和一致性
        total_coverage = sum(imp['coverage'] for imp in prime_implicants)
        avg_consistency = np.mean([imp['consistency'] for imp in prime_implicants]) if prime_implicants else 0
        
        solution = FSCSolution(
            solution_type=SolutionType.COMPLEX,
            expression=expression,
            prime_implicants=[str(imp['config']) for imp in prime_implicants],
            coverage=min(total_coverage, 1.0),  # 覆盖度不能超过1
            consistency=avg_consistency,
            complexity=len(prime_implicants),
            frequency=sum(imp['frequency'] for imp in prime_implicants)
        )
        
        return solution
    
    def _generate_primed_solution(
        self,
        prime_implicants: List[Dict[str, Any]],
        truth_table: pd.DataFrame,
        conditions: List[str]
    ) -> FSCSolution:
        """生成简约解（通过逻辑运算去除冗余）"""
        # 简约解通过布尔最小化算法去除冗余项
        # 这里使用简化的逻辑最小化方法
        
        if not prime_implicants:
            return FSCSolution(
                solution_type=SolutionType.PRIMED,
                expression="No solution",
                prime_implicants=[],
                coverage=0.0,
                consistency=0.0,
                complexity=0,
                frequency=0.0
            )
        
        # 首先尝试合并相似的蕴含项
        simplified_implicants = self._simplify_implicants(prime_implicants, conditions)
        
        # 构建表达式
        expression_parts = []
        for implicant in simplified_implicants:
            config_parts = []
            for condition, value in implicant['config'].items():
                if value == 1:
                    config_parts.append(condition)
                elif value == 0:
                    config_parts.append(f"~{condition}")
                else:
                    # 对于模糊集，可能有中间值，需要特殊处理
                    config_parts.append(f"{condition}({value:.2f})")
            
            expression_parts.append(f"({' * '.join(config_parts)})")
        
        expression = ' + '.join(expression_parts)
        
        # 计算整体覆盖度和一致性
        total_coverage = sum(imp['coverage'] for imp in simplified_implicants)

        # 使用安全的平均值计算，避免空数组问题
        consistency_values = [imp['consistency'] for imp in simplified_implicants]
        if consistency_values:
            avg_consistency = np.nanmean(consistency_values)  # 使用nanmean避免空数组警告
        else:
            avg_consistency = 0.0

        solution = FSCSolution(
            solution_type=SolutionType.PRIMED,
            expression=expression,
            prime_implicants=[str(imp['config']) for imp in simplified_implicants],
            coverage=min(total_coverage, 1.0),
            consistency=avg_consistency,
            complexity=len(simplified_implicants),
            frequency=sum(imp['frequency'] for imp in simplified_implicants)
        )
        
        return solution
    
    def _simplify_implicants(
        self,
        prime_implicants: List[Dict[str, Any]],
        conditions: List[str]
    ) -> List[Dict[str, Any]]:
        """简化蕴含项，合并相似项"""
        if len(prime_implicants) <= 1:
            return prime_implicants
        
        # 尝试合并可以合并的蕴含项
        simplified = []
        used = [False] * len(prime_implicants)
        
        for i, imp1 in enumerate(prime_implicants):
            if used[i]:
                continue
                
            merged_implicant = deepcopy(imp1)
            merged = False
            
            for j, imp2 in enumerate(prime_implicants[i+1:], i+1):
                if used[j]:
                    continue
                
                # 检查两个蕴含项是否可以合并（只有一个条件不同）
                diff_count = 0
                diff_condition = None
                
                for condition in conditions:
                    if imp1['config'][condition] != imp2['config'][condition]:
                        diff_count += 1
                        diff_condition = condition
                
                if diff_count == 1 and diff_condition is not None:
                    # 可以合并，该条件变为无关项
                    merged_implicant['config'][diff_condition] = '*'  # 表示无关项
                    merged_implicant['coverage'] = max(merged_implicant['coverage'], imp2['coverage'])
                    merged_implicant['consistency'] = min(merged_implicant['consistency'], imp2['consistency'])
                    merged_implicant['frequency'] += imp2['frequency']
                    merged_implicant['cases'].extend(imp2['cases'])
                    
                    used[j] = True
                    merged = True
            
            simplified.append(merged_implicant)
            used[i] = True
        
        # 过滤掉已使用的项
        result = [imp for i, imp in enumerate(simplified) if not used[i]]
        
        # 递归简化直到无法进一步简化
        if len(result) < len(prime_implicants):
            return self._simplify_implicants(result, conditions)
        else:
            return result
    
    def _generate_intermediate_solution(
        self,
        primed_solution: FSCSolution,
        truth_table: pd.DataFrame,
        conditions: List[str]
    ) -> FSCSolution:
        """生成中间解（结合理论知识）"""
        # 中间解通常需要理论指导，这里返回与简约解相同的内容
        # 但在实际应用中，可能会根据理论知识添加或移除某些逻辑余项
        
        intermediate_solution = FSCSolution(
            solution_type=SolutionType.INTERMEDIATE,
            expression=primed_solution.expression,
            prime_implicants=deepcopy(primed_solution.prime_implicants),
            coverage=primed_solution.coverage,
            consistency=primed_solution.consistency,
            complexity=primed_solution.complexity,
            frequency=primed_solution.frequency
        )
        
        # 在实际实现中，这里会根据理论知识调整解
        # 例如，移除理论上不合理但统计上显著的组合
        
        return intermediate_solution
    
    def calculate_solution_quality(
        self,
        solution: FSCSolution,
        truth_table: pd.DataFrame
    ) -> Dict[str, float]:
        """计算解的质量指标"""
        quality_metrics = {
            'coverage': solution.coverage,
            'consistency': solution.consistency,
            'complexity': solution.complexity,
            'frequency': solution.frequency
        }
        
        # 计算PRI（Proportional Reduction in Inconsistency）
        # 这是一个更精细的一致性指标
        if solution.complexity > 0:
            quality_metrics['PRI'] = solution.consistency
        
        # 计算AICc（修正的赤池信息准则）
        # AICc = -2*ln(L) + 2*k + (2*k*(k+1))/(n-k-1)
        # 其中k是参数数量（复杂度），n是观察数
        n_observations = len(truth_table)
        k_params = solution.complexity
        
        if n_observations > k_params + 1:
            # 简化的AICc计算
            aicc = k_params  # 实际计算需要基于似然函数
            quality_metrics['AICc'] = aicc
        else:
            quality_metrics['AICc'] = float('inf')
        
        return quality_metrics
    
    def evaluate_solution(
        self,
        solution: FSCSolution,
        truth_table: pd.DataFrame,
        conditions: List[str],
        outcome: str
    ) -> Dict[str, Any]:
        """评估解的性能"""
        evaluation = {
            'solution_type': solution.solution_type.value,
            'expression': solution.expression,
            'quality_metrics': self.calculate_solution_quality(solution, truth_table),
            'interpretability': self._assess_interpretability(solution),
            'robustness': self._assess_robustness(solution, truth_table)
        }
        
        return evaluation
    
    def _assess_interpretability(self, solution: FSCSolution) -> float:
        """评估解的可解释性"""
        # 可解释性与复杂度成反比，与一致性成正比
        if solution.complexity == 0:
            return 0.0

        # 防止log(0)导致的错误
        if solution.complexity <= 0:
            return 0.0

        interpretability = solution.consistency / (1 + np.log(max(solution.complexity, 1e-10)))
        return min(interpretability, 1.0)
    
    def _assess_robustness(self, solution: FSCSolution, truth_table: pd.DataFrame) -> float:
        """评估解的稳健性"""
        # 稳健性基于覆盖度、一致性和案例数量
        if len(truth_table) == 0:
            return 0.0
        
        # 综合考虑覆盖度、一致性和复杂度
        robustness = (solution.coverage + solution.consistency) / (1 + solution.complexity * 0.1)
        return min(robustness, 1.0)


def solve_logic_expression(expression: str, condition_values: Dict[str, float]) -> float:
    """
    计算逻辑表达式的值
    
    Args:
        expression: 逻辑表达式
        condition_values: 条件值字典
    
    Returns:
        表达式结果（0到1之间的值）
    """
    # 简化的表达式求值器，适用于模糊集
    # 这里使用t-范数（最小值）作为AND操作，s-范数（最大值）作为OR操作
    
    # 为了简化，我们假设表达式是标准形式，如 "(A * B) + (C * ~D)"
    # 实际实现需要更复杂的解析器
    
    # 示例实现：计算简单的表达式
    # 在实际应用中，这需要一个完整的表达式解析器
    
    # 作为示例，这里返回一个占位符实现
    if expression == "No solution":
        return 0.0
    
    # 简化的计算：返回条件值的某种组合
    # 这里只是一个示例，实际实现需要完整的布尔代数运算
    if condition_values:
        # 使用最小值作为AND，最大值作为OR的简单示例
        values = list(condition_values.values())
        if values:
            return max(values)  # 简化的OR操作
        else:
            return 0.0
    else:
        return 0.0


def calculate_essential_conditions(
    solutions: List[FSCSolution],
    conditions: List[str]
) -> Dict[str, float]:
    """
    计算必要条件
    
    Args:
        solutions: 解列表
        conditions: 条件列表
    
    Returns:
        每个条件作为必要条件的分数
    """
    essential_scores = {condition: 0.0 for condition in conditions}
    
    for solution in solutions:
        # 检查解中每个条件的出现频率和重要性
        expression = solution.expression
        for condition in conditions:
            if condition in expression:
                # 条件在解中出现，增加其必要性分数
                essential_scores[condition] += solution.coverage * solution.consistency
    
    # 归一化分数
    max_score = max(essential_scores.values()) if essential_scores else 1.0
    if max_score > 0:
        for condition in essential_scores:
            essential_scores[condition] /= max_score
    
    return essential_scores


if __name__ == "__main__":
    # 示例用法
    print("模糊逻辑最小化模块测试")
    
    # 创建示例真值表（模拟从truth_table.py模块获得的数据）
    np.random.seed(42)
    
    # 模拟真值表数据
    sample_configs = [
        (1, 0, 1),  # 配置1
        (1, 1, 0),  # 配置2
        (0, 1, 1),  # 配置3
        (1, 1, 1),  # 配置4
    ]
    
    sample_data = []
    for i, config in enumerate(sample_configs):
        sample_data.append({
            'configuration': config,
            'frequency': np.random.randint(1, 5),
            'outcome': np.random.uniform(0.6, 1.0),  # 正面结果
            'consistency': np.random.uniform(0.8, 1.0),
            'cases': [f'case_{i*3+j}' for j in range(np.random.randint(1, 4))],
            'n_cases': np.random.randint(1, 4),
            'inclusion_score': np.random.uniform(0.7, 1.0),
            'PRI_consistency': np.random.uniform(0.75, 1.0),
            'remainder': False,
            'contradictory': False
        })
    
    truth_table = pd.DataFrame(sample_data)
    
    # 添加条件列的平均值
    for i, condition in enumerate(['A', 'B', 'C']):
        truth_table[f'avg_{condition}'] = [config[i] for config in sample_configs]
    
    print(f"模拟真值表形状: {truth_table.shape}")
    
    # 初始化最小化器
    minimizer = FSCMinimizer()
    
    # 执行最小化
    conditions = ['A', 'B', 'C']
    solutions = minimizer.minimize(truth_table, conditions)
    
    print(f"\n生成了 {len(solutions)} 个解:")
    for i, solution in enumerate(solutions):
        print(f"\n解 {i+1} ({solution.solution_type.value}):")
        print(f"  表达式: {solution.expression}")
        print(f"  覆盖度: {solution.coverage:.3f}")
        print(f"  一致性: {solution.consistency:.3f}")
        print(f"  复杂度: {solution.complexity}")
        print(f"  频数: {solution.frequency:.3f}")
    
    # 评估第一个解
    if solutions:
        evaluation = minimizer.evaluate_solution(solutions[0], truth_table, conditions, 'outcome')
        print(f"\n解评估: {evaluation}")
        
        # 计算必要条件
        essential_conditions = calculate_essential_conditions(solutions, conditions)
        print(f"\n必要条件分数: {essential_conditions}")