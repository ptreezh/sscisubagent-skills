#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多值定性比较分析(msQCA) - 逻辑最小化模块
提供布尔最小化算法和最简路径识别功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Set, Union
import itertools
from collections import defaultdict
import warnings
from dataclasses import dataclass
from enum import Enum


class SolutionType(Enum):
    """解类型枚举"""
    PRIME_IMPLICANT = "prime_implicant"  # 质蕴含项
    COMPLEX_SOLUTION = "complex_solution"  # 复杂解
    MINIMAL_SOLUTION = "minimal_solution"  # 最小解
    PARSIMONIOUS_SOLUTION = "parsimonious_solution"  # 简约解


@dataclass
class PrimeImplicant:
    """质蕴含项数据类"""
    expression: str  # 布尔表达式
    conditions: Dict[str, Union[int, str]]  # 条件组合
    coverage: float  # 覆盖度
    consistency: float  # 一致性
    cases: List[int]  # 覆盖的案例


@dataclass
class QCASolution:
    """QCA解数据类"""
    expression: str  # 完整表达式
    prime_implicants: List[PrimeImplicant]  # 质蕴含项列表
    solution_type: SolutionType  # 解类型
    coverage: float  # 总覆盖度
    consistency: float  # 总一致性
    complexity: int  # 复杂度（条件数量）


class BooleanMinimizer:
    """布尔最小化器"""
    
    def __init__(self):
        self.prime_implicants = []
        self.solutions = []
        self.truth_table = None
        self.conditions = []
        
    def minimize(self, 
                truth_table: pd.DataFrame,
                conditions: List[str],
                include_remainders: bool = True,
                complexity_limit: Optional[int] = None) -> List[QCASolution]:
        """
        执行布尔最小化
        
        Parameters:
        -----------
        truth_table : pd.DataFrame
            真值表
        conditions : List[str]
            条件变量列表
        include_remainders : bool
            是否包含逻辑余项
        complexity_limit : Optional[int]
            复杂度限制
            
        Returns:
        --------
        List[QCASolution]
            最小化解列表
        """
        self.truth_table = truth_table
        self.conditions = conditions
        
        # 提取正面结果组合
        positive_combinations = self._extract_positive_combinations()
        
        # 生成质蕴含项
        self.prime_implicants = self._generate_prime_implicants(
            positive_combinations, include_remainders
        )
        
        # 生成不同类型的解
        self.solutions = self._generate_solutions(complexity_limit)
        
        return self.solutions
    
    def _extract_positive_combinations(self) -> List[Tuple]:
        """提取正面结果的条件组合"""
        positive_rows = self.truth_table[
            self.truth_table['result_type'] == 1
        ]
        
        combinations = []
        for _, row in positive_rows.iterrows():
            combo = tuple(row[condition] for condition in self.conditions)
            combinations.append(combo)
            
        return combinations
    
    def _generate_prime_implicants(self, 
                                  positive_combinations: List[Tuple],
                                  include_remainders: bool) -> List[PrimeImplicant]:
        """
        生成质蕴含项
        
        使用Quine-McCluskey算法
        """
        # 第一步：生成所有可能的蕴含项
        implicates = self._quine_mccluskey(positive_combinations)
        
        # 第二步：识别质蕴含项
        prime_implicants = self._identify_prime_implicants(implicates)
        
        # 第三步：计算质蕴含项的统计指标
        prime_implicants = self._calculate_implicant_metrics(prime_implicants)
        
        return prime_implicants
    
    def _quine_mccluskey(self, combinations: List[Tuple]) -> List[Dict]:
        """
        Quine-McCluskey算法实现
        
        Parameters:
        -----------
        combinations : List[Tuple]
            条件组合列表
            
        Returns:
        --------
        List[Dict]
            蕴含项列表
        """
        # 初始化
        implicants = []
        
        # 将组合转换为蕴含项
        for combo in combinations:
            implicant = {
                'expression': self._combo_to_expression(combo),
                'conditions': dict(zip(self.conditions, combo)),
                'covered_cases': [combo],
                'marked': False
            }
            implicants.append(implicant)
        
        # 迭代合并
        changed = True
        while changed:
            changed = False
            new_implicants = []
            marked_indices = set()
            
            # 尝试合并所有蕴含项对
            for i, imp1 in enumerate(implicants):
                for j, imp2 in enumerate(implicants[i+1:], i+1):
                    combined = self._try_combine(imp1, imp2)
                    if combined:
                        new_implicants.append(combined)
                        marked_indices.add(i)
                        marked_indices.add(j)
                        changed = True
            
            # 保留未合并的蕴含项
            for i, imp in enumerate(implicants):
                if i not in marked_indices:
                    new_implicants.append(imp)
            
            implicants = new_implicants
        
        return implicants
    
    def _try_combine(self, imp1: Dict, imp2: Dict) -> Optional[Dict]:
        """
        尝试合并两个蕴含项
        
        Parameters:
        -----------
        imp1, imp2 : Dict
            蕴含项
            
        Returns:
        --------
        Optional[Dict]
            合并后的蕴含项，如果不能合并则返回None
        """
        conditions = {}
        diff_count = 0
        diff_condition = None
        
        # 检查每个条件
        for condition in self.conditions:
            val1 = imp1['conditions'][condition]
            val2 = imp2['conditions'][condition]
            
            if val1 == val2:
                conditions[condition] = val1
            else:
                diff_count += 1
                diff_condition = condition
                
                # 只有一个条件不同且都是具体值时才能合并
                if not (isinstance(val1, int) and isinstance(val2, int)):
                    return None
        
        # 只有一个条件不同时才能合并
        if diff_count != 1:
            return None
        
        # 创建合并后的蕴含项
        combined_conditions = imp1['conditions'].copy()
        combined_conditions[diff_condition] = '*'  # 使用*表示无关项
        
        combined = {
            'expression': self._combo_to_expression([
                combined_conditions[cond] for cond in self.conditions
            ]),
            'conditions': combined_conditions,
            'covered_cases': list(set(imp1['covered_cases']) | set(imp2['covered_cases'])),
            'marked': False
        }
        
        return combined
    
    def _combo_to_expression(self, combo: Tuple) -> str:
        """
        将条件组合转换为布尔表达式
        
        Parameters:
        -----------
        combo : Tuple
            条件组合
            
        Returns:
        --------
        str
            布尔表达式
        """
        terms = []
        for i, (condition, value) in enumerate(zip(self.conditions, combo)):
            if value == '*':
                continue  # 无关项不包含在表达式中
            elif isinstance(value, int):
                if value == 1:
                    terms.append(condition)
                elif value == 0:
                    terms.append(f"~{condition}")
                else:
                    terms.append(f"{condition}={value}")
            else:
                terms.append(f"{condition}={value}")
        
        return " * ".join(terms) if terms else "TRUE"
    
    def _identify_prime_implicants(self, implicants: List[Dict]) -> List[PrimeImplicant]:
        """
        识别质蕴含项
        
        Parameters:
        -----------
        implicants : List[Dict]
            蕴含项列表
            
        Returns:
        --------
        List[PrimeImplicant]
            质蕴含项列表
        """
        prime_implicants = []
        
        for imp in implicants:
            # 创建质蕴含项对象
            pi = PrimeImplicant(
                expression=imp['expression'],
                conditions=imp['conditions'],
                coverage=0.0,  # 稍后计算
                consistency=0.0,  # 稍后计算
                cases=[]  # 稍后填充
            )
            prime_implicants.append(pi)
        
        return prime_implicants
    
    def _calculate_implicant_metrics(self, prime_implicants: List[PrimeImplicant]) -> List[PrimeImplicant]:
        """
        计算质蕴含项的统计指标
        
        Parameters:
        -----------
        prime_implicants : List[PrimeImplicant]
            质蕴含项列表
            
        Returns:
        --------
        List[PrimeImplicant]
            更新指标的质蕴含项列表
        """
        for pi in prime_implicants:
            # 计算覆盖的案例
            covered_cases = []
            total_consistency = 0.0
            
            for _, row in self.truth_table.iterrows():
                if self._case_matches_implicant(row, pi):
                    covered_cases.extend(row['cases'])
                    total_consistency += row['consistency']
            
            pi.cases = list(set(covered_cases))
            
            # 计算覆盖度和一致性
            if len(pi.cases) > 0:
                total_positive_cases = sum(
                    self.truth_table[self.truth_table['result_type'] == 1]['n_cases']
                )
                pi.coverage = len(pi.cases) / total_positive_cases if total_positive_cases > 0 else 0
                pi.consistency = total_consistency / len(self.truth_table[
                    self.truth_table.index.isin(
                        [idx for idx, row in self.truth_table.iterrows() 
                         if self._case_matches_implicant(row, pi)]
                    )
                ]) if len(pi.cases) > 0 else 0
            else:
                pi.coverage = 0.0
                pi.consistency = 0.0
        
        return prime_implicants
    
    def _case_matches_implicant(self, case_row: pd.Series, implicant: PrimeImplicant) -> bool:
        """
        检查案例是否匹配质蕴含项
        
        Parameters:
        -----------
        case_row : pd.Series
            案例行
        implicant : PrimeImplicant
            质蕴含项
            
        Returns:
        --------
        bool
            是否匹配
        """
        for condition, value in implicant.conditions.items():
            if value != '*':  # 无关项匹配任何值
                if case_row[condition] != value:
                    return False
        return True
    
    def _generate_solutions(self, complexity_limit: Optional[int] = None) -> List[QCASolution]:
        """
        生成不同类型的解
        
        Parameters:
        -----------
        complexity_limit : Optional[int]
            复杂度限制
            
        Returns:
        --------
        List[QCASolution]
            解列表
        """
        solutions = []
        
        # 生成复杂解（包含所有质蕴含项）
        complex_solution = self._create_complex_solution()
        if complex_solution:
            solutions.append(complex_solution)
        
        # 生成最小解（使用覆盖表算法）
        minimal_solutions = self._create_minimal_solutions(complexity_limit)
        solutions.extend(minimal_solutions)
        
        # 生成简约解（包含逻辑余项）
        parsimonious_solutions = self._create_parsimonious_solutions()
        solutions.extend(parsimonious_solutions)
        
        # 按复杂度和覆盖度排序
        solutions.sort(key=lambda x: (x.complexity, -x.coverage))
        
        return solutions
    
    def _create_complex_solution(self) -> Optional[QCASolution]:
        """创建复杂解"""
        if not self.prime_implicants:
            return None
        
        expression = " + ".join([pi.expression for pi in self.prime_implicants])
        
        # 计算总指标
        if self.prime_implicants:
            total_coverage = max([pi.coverage for pi in self.prime_implicants])
            # 使用nanmean避免空数组问题
            consistency_values = [pi.consistency for pi in self.prime_implicants]
            if consistency_values:
                total_consistency = np.nanmean(consistency_values)
            else:
                total_consistency = 0.0
        else:
            total_coverage = 0.0
            total_consistency = 0.0
        complexity = len(self.prime_implicants)

        solution = QCASolution(
            expression=expression,
            prime_implicants=self.prime_implicants,
            solution_type=SolutionType.COMPLEX_SOLUTION,
            coverage=total_coverage,
            consistency=total_consistency,
            complexity=complexity
        )
        
        return solution
    
    def _create_minimal_solutions(self, complexity_limit: Optional[int] = None) -> List[QCASolution]:
        """创建最小解"""
        # 这里简化处理，实际应该使用覆盖表算法
        minimal_solutions = []
        
        # 按覆盖度排序质蕴含项
        sorted_implicants = sorted(self.prime_implicants, key=lambda x: -x.coverage)
        
        # 生成不同复杂度的解
        for complexity in range(1, min(len(sorted_implicants), complexity_limit or 5) + 1):
            selected_implicants = sorted_implicants[:complexity]
            
            expression = " + ".join([pi.expression for pi in selected_implicants])
            
            coverage_values = [pi.coverage for pi in selected_implicants]
            consistency_values = [pi.consistency for pi in selected_implicants]

            total_coverage = max(coverage_values) if coverage_values else 0.0
            total_consistency = np.nanmean(consistency_values) if consistency_values else 0.0

            solution = QCASolution(
                expression=expression,
                prime_implicants=selected_implicants,
                solution_type=SolutionType.MINIMAL_SOLUTION,
                coverage=total_coverage,
                consistency=total_consistency,
                complexity=complexity
            )
            
            minimal_solutions.append(solution)
        
        return minimal_solutions
    
    def _create_parsimonious_solutions(self) -> List[QCASolution]:
        """创建简约解"""
        # 这里简化处理，实际应该包含逻辑余项的分析
        parsimonious_solutions = []
        
        # 选择覆盖度最高的质蕴含项
        if self.prime_implicants:
            best_implicant = max(self.prime_implicants, key=lambda x: x.coverage)
            
            solution = QCASolution(
                expression=best_implicant.expression,
                prime_implicants=[best_implicant],
                solution_type=SolutionType.PARSIMONIOUS_SOLUTION,
                coverage=best_implicant.coverage,
                consistency=best_implicant.consistency,
                complexity=1
            )
            
            parsimonious_solutions.append(solution)
        
        return parsimonious_solutions
    
    def export_solutions(self, filename: str, format: str = 'csv') -> bool:
        """
        导出解结果
        
        Parameters:
        -----------
        filename : str
            文件名
        format : str
            导出格式
            
        Returns:
        --------
        bool
            导出是否成功
        """
        if not self.solutions:
            return False
        
        try:
            if format == 'csv':
                # 创建解的数据框
                solutions_data = []
                for sol in self.solutions:
                    solutions_data.append({
                        'expression': sol.expression,
                        'solution_type': sol.solution_type.value,
                        'coverage': sol.coverage,
                        'consistency': sol.consistency,
                        'complexity': sol.complexity
                    })
                
                df = pd.DataFrame(solutions_data)
                df.to_csv(filename, index=False, encoding='utf-8')
                
            elif format == 'json':
                import json
                solutions_json = []
                for sol in self.solutions:
                    sol_dict = {
                        'expression': sol.expression,
                        'solution_type': sol.solution_type.value,
                        'coverage': sol.coverage,
                        'consistency': sol.consistency,
                        'complexity': sol.complexity,
                        'prime_implicants': [
                            {
                                'expression': pi.expression,
                                'coverage': pi.coverage,
                                'consistency': pi.consistency
                            }
                            for pi in sol.prime_implicants
                        ]
                    }
                    solutions_json.append(sol_dict)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(solutions_json, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False


def main():
    """示例用法"""
    # 创建示例真值表数据
    truth_table_data = {
        'A': [0, 0, 1, 1, 0, 1],
        'B': [0, 1, 0, 1, 2, 2],
        'C': [1, 0, 0, 1, 1, 0],
        'result_type': [1, 1, 1, 1, 0, 0],
        'consistency': [0.9, 0.8, 0.85, 0.95, 0.1, 0.2],
        'n_cases': [5, 3, 4, 6, 2, 3],
        'cases': [[1,2,3,4,5], [6,7,8], [9,10,11,12], [13,14,15,16,17,18], [19,20], [21,22,23]]
    }
    
    truth_table = pd.DataFrame(truth_table_data)
    conditions = ['A', 'B', 'C']
    
    # 初始化最小化器
    minimizer = BooleanMinimizer()
    
    # 执行最小化
    solutions = minimizer.minimize(truth_table, conditions)
    
    print("最小化结果:")
    for i, solution in enumerate(solutions):
        print(f"\n解 {i+1} ({solution.solution_type.value}):")
        print(f"表达式: {solution.expression}")
        print(f"覆盖度: {solution.coverage:.3f}")
        print(f"一致性: {solution.consistency:.3f}")
        print(f"复杂度: {solution.complexity}")
    
    print(f"\n质蕴含项数量: {len(minimizer.prime_implicants)}")
    for pi in minimizer.prime_implicants:
        print(f"- {pi.expression} (覆盖度: {pi.coverage:.3f})")


if __name__ == "__main__":
    main()