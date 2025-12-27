#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多值定性比较分析(msQCA) - 真值表构建模块
提供真值表生成、逻辑余项识别和矛盾组合处理功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Set
import itertools
from collections import defaultdict, Counter
import warnings


class TruthTableBuilder:
    """QCA真值表构建类"""
    
    def __init__(self):
        self.truth_table = None
        self.logical_remainders = []
        self.contradictory_cases = []
        self.consistency_scores = {}
        
    def build_truth_table(self, 
                         data: pd.DataFrame, 
                         conditions: List[str], 
                         outcome: str,
                         outcome_threshold: float = 0.8) -> pd.DataFrame:
        """
        构建真值表
        
        Parameters:
        -----------
        data : pd.DataFrame
            校准后的数据
        conditions : List[str]
            条件变量列表
        outcome : str
            结果变量
        outcome_threshold : float
            结果一致性阈值
            
        Returns:
        --------
        pd.DataFrame
            构建的真值表
        """
        # 按条件组合分组
        grouped = data.groupby(conditions)
        
        truth_table_data = []
        
        for condition_combo, group in grouped:
            # 计算每个组合的一致性
            consistency = self._calculate_consistency(group[outcome], outcome_threshold)
            
            # 计算案例数量
            n_cases = len(group)
            
            # 识别结果类型
            if consistency >= outcome_threshold:
                result_type = 1  # 正面结果
            elif consistency <= (1 - outcome_threshold):
                result_type = 0  # 负面结果
            else:
                result_type = -1  # 矛盾结果
            
            row_data = {
                'condition_combo': condition_combo if len(conditions) > 1 else [condition_combo],
                'consistency': consistency,
                'n_cases': n_cases,
                'result_type': result_type,
                'cases': group.index.tolist()
            }
            
            # 添加条件列
            if len(conditions) == 1:
                row_data[conditions[0]] = condition_combo
            else:
                for i, condition in enumerate(conditions):
                    row_data[condition] = condition_combo[i]
            
            truth_table_data.append(row_data)
        
        self.truth_table = pd.DataFrame(truth_table_data)
        
        # 识别逻辑余项和矛盾组合
        self._identify_logical_remainders(conditions)
        self._identify_contradictory_cases()
        
        return self.truth_table
    
    def _calculate_consistency(self, outcome_values: pd.Series, threshold: float) -> float:
        """
        计算一致性分数

        Parameters:
        -----------
        outcome_values : pd.Series
            结果变量值
        threshold : float
            阈值

        Returns:
        --------
        float
            一致性分数
        """
        if len(outcome_values) == 0 or outcome_values.isna().all():
            return 0.0

        # 计算达到阈值的案例比例
        consistent_cases = (outcome_values >= threshold).sum()
        total_cases = len(outcome_values.dropna())  # 只考虑非空值

        consistency = consistent_cases / total_cases if total_cases > 0 else 0.0

        # 确保结果是有效的数值
        if np.isnan(consistency) or np.isinf(consistency):
            consistency = 0.0

        return consistency
    
    def _identify_logical_remainders(self, conditions: List[str]):
        """
        识别逻辑余项（未观察到的条件组合）
        
        Parameters:
        -----------
        conditions : List[str]
            条件变量列表
        """
        if self.truth_table is None:
            return
        
        # 获取每个条件的所有可能值
        condition_values = {}
        for condition in conditions:
            unique_values = sorted(self.truth_table[condition].unique())
            condition_values[condition] = unique_values
        
        # 生成所有可能的组合
        all_combinations = list(itertools.product(*[
            condition_values[condition] for condition in conditions
        ]))
        
        # 获取已观察到的组合
        observed_combinations = set()
        for _, row in self.truth_table.iterrows():
            if len(conditions) == 1:
                combo = (row[conditions[0]],)
            else:
                combo = tuple(row[condition] for condition in conditions)
            observed_combinations.add(combo)
        
        # 识别逻辑余项
        self.logical_remainders = [
            combo for combo in all_combinations 
            if combo not in observed_combinations
        ]
    
    def _identify_contradictory_cases(self):
        """识别矛盾组合"""
        if self.truth_table is None:
            return
        
        contradictory_rows = self.truth_table[
            self.truth_table['result_type'] == -1
        ]
        
        self.contradictory_cases = contradictory_rows.to_dict('records')
    
    def handle_contradictions(self, 
                            method: str = 'remove',
                            consistency_threshold: float = 0.6) -> pd.DataFrame:
        """
        处理矛盾组合
        
        Parameters:
        -----------
        method : str
            处理方法: 'remove', 'recode', 'split'
        consistency_threshold : float
            一致性阈值
            
        Returns:
        --------
        pd.DataFrame
            处理后的真值表
        """
        if self.truth_table is None or len(self.contradictory_cases) == 0:
            return self.truth_table
        
        if method == 'remove':
            # 移除矛盾组合
            filtered_table = self.truth_table[
                self.truth_table['result_type'] != -1
            ].copy()
            
        elif method == 'recode':
            # 重新编码为最接近的结果类型
            filtered_table = self.truth_table.copy()
            for idx, row in self.contradictory_cases:
                if row['consistency'] >= consistency_threshold:
                    filtered_table.loc[idx, 'result_type'] = 1
                else:
                    filtered_table.loc[idx, 'result_type'] = 0
                    
        elif method == 'split':
            # 分裂矛盾组合为正负两种结果
            new_rows = []
            for idx, row in self.contradictory_cases:
                # 创建正面结果行
                pos_row = row.copy()
                pos_row['result_type'] = 1
                pos_row['n_cases'] = int(row['n_cases'] * row['consistency'])
                new_rows.append(pos_row)
                
                # 创建负面结果行
                neg_row = row.copy()
                neg_row['result_type'] = 0
                neg_row['n_cases'] = int(row['n_cases'] * (1 - row['consistency']))
                new_rows.append(neg_row)
            
            # 移除原始矛盾行并添加新行
            filtered_table = self.truth_table[
                self.truth_table['result_type'] != -1
            ].copy()
            filtered_table = pd.concat([filtered_table, pd.DataFrame(new_rows)], 
                                     ignore_index=True)
        else:
            raise ValueError(f"不支持的矛盾处理方法: {method}")
        
        self.truth_table = filtered_table
        return self.truth_table
    
    def add_logical_remainders(self, 
                             method: str = 'all',
                             consistency: float = 0.0) -> pd.DataFrame:
        """
        添加逻辑余项到真值表
        
        Parameters:
        -----------
        method : str
            添加方法: 'all', 'positive', 'negative'
        consistency : float
            逻辑余项的一致性分数
            
        Returns:
        --------
        pd.DataFrame
            包含逻辑余项的真值表
        """
        if self.truth_table is None:
            return pd.DataFrame()
        
        new_rows = []
        
        for combo in self.logical_remainders:
            # 确定结果类型
            if method == 'all':
                result_type = -1  # 逻辑余项
            elif method == 'positive':
                result_type = 1
            elif method == 'negative':
                result_type = 0
            else:
                raise ValueError(f"不支持的逻辑余项添加方法: {method}")
            
            # 创建新行
            row_data = {
                'condition_combo': combo,
                'consistency': consistency,
                'n_cases': 0,  # 逻辑余项没有实际案例
                'result_type': result_type,
                'cases': []
            }
            
            # 添加条件列
            for i, condition in enumerate(self.get_condition_columns()):
                row_data[condition] = combo[i]
            
            new_rows.append(row_data)
        
        # 添加到真值表
        if new_rows:
            extended_table = pd.concat([self.truth_table, pd.DataFrame(new_rows)], 
                                     ignore_index=True)
        else:
            extended_table = self.truth_table.copy()
        
        return extended_table
    
    def get_condition_columns(self) -> List[str]:
        """获取条件变量列名"""
        if self.truth_table is None:
            return []
        
        # 排除非条件列
        exclude_columns = {
            'condition_combo', 'consistency', 'n_cases', 
            'result_type', 'cases'
        }
        
        condition_columns = [
            col for col in self.truth_table.columns 
            if col not in exclude_columns
        ]
        
        return condition_columns
    
    def calculate_quality_metrics(self) -> Dict:
        """
        计算真值表质量指标

        Returns:
        --------
        Dict
            质量指标字典
        """
        if self.truth_table is None:
            return {}

        # 安全计算各项指标
        total_cases = self.truth_table['n_cases'].sum() if 'n_cases' in self.truth_table.columns else 0
        positive_cases = 0
        negative_cases = 0
        contradictory_cases = 0

        if 'result_type' in self.truth_table.columns and 'n_cases' in self.truth_table.columns:
            positive_cases = self.truth_table[
                self.truth_table['result_type'] == 1
            ]['n_cases'].sum()
            negative_cases = self.truth_table[
                self.truth_table['result_type'] == 0
            ]['n_cases'].sum()
            contradictory_cases = self.truth_table[
                self.truth_table['result_type'] == -1
            ]['n_cases'].sum()

        # 计算矛盾率和覆盖度，避免除零错误
        contradiction_rate = contradictory_cases / total_cases if total_cases > 0 else 0
        coverage = (positive_cases + negative_cases) / total_cases if total_cases > 0 else 0

        metrics = {
            'total_cases': total_cases,
            'positive_cases': positive_cases,
            'negative_cases': negative_cases,
            'contradictory_cases': contradictory_cases,
            'contradiction_rate': contradiction_rate,
            'coverage': coverage,
            'logical_remainders_count': len(self.logical_remainders),
            'unique_combinations': len(self.truth_table) if self.truth_table is not None else 0
        }

        return metrics
    
    def export_truth_table(self, 
                          filename: str,
                          format: str = 'csv') -> bool:
        """
        导出真值表
        
        Parameters:
        -----------
        filename : str
            文件名
        format : str
            导出格式: 'csv', 'excel', 'json'
            
        Returns:
        --------
        bool
            导出是否成功
        """
        if self.truth_table is None:
            return False
        
        try:
            if format == 'csv':
                self.truth_table.to_csv(filename, index=False, encoding='utf-8')
            elif format == 'excel':
                self.truth_table.to_excel(filename, index=False)
            elif format == 'json':
                self.truth_table.to_json(filename, orient='records', force_ascii=False, indent=2)
            else:
                raise ValueError(f"不支持的导出格式: {format}")
            
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False


def main():
    """示例用法"""
    # 创建示例数据
    np.random.seed(42)
    n_cases = 100
    
    data = pd.DataFrame({
        'A': np.random.choice([0, 1, 2], n_cases),
        'B': np.random.choice([0, 1, 2], n_cases),
        'C': np.random.choice([0, 1, 2], n_cases),
        'Y': np.random.uniform(0, 1, n_cases)
    })
    
    # 初始化真值表构建器
    builder = TruthTableBuilder()
    
    # 构建真值表
    truth_table = builder.build_truth_table(
        data=data,
        conditions=['A', 'B', 'C'],
        outcome='Y',
        outcome_threshold=0.8
    )
    
    print("真值表:")
    print(truth_table[['A', 'B', 'C', 'consistency', 'n_cases', 'result_type']].head(10))
    
    # 处理矛盾组合
    filtered_table = builder.handle_contradictions(method='remove')
    print(f"\n移除矛盾组合后: {len(filtered_table)} 行")
    
    # 计算质量指标
    metrics = builder.calculate_quality_metrics()
    print("\n质量指标:")
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    print(f"\n逻辑余项数量: {len(builder.logical_remainders)}")


if __name__ == "__main__":
    main()