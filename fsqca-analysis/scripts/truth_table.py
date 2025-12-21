#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模糊集定性比较分析(fsQCA) - 模糊真值表构建模块
实现模糊集真值表的构建和分析
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
from itertools import product
from dataclasses import dataclass
import warnings
from calibration import FSCCalibration, consistency_xy, coverage_xy


@dataclass
class TruthTableRow:
    """真值表行数据类"""
    configuration: Tuple[int, ...]  # 配置 (0, 1, 2, ...)
    raw_configuration: Tuple[float, ...]  # 原始模糊集隶属度
    frequency: float  # 频数
    outcome: float  # 结果值
    consistency: float  # 一致性
    cases: List[str]  # 案例列表
    n_cases: int  # 案例数量
    inclusion_score: float  # 包含分数
    PRI_consistency: float  # PRI一致性


class FuzzyTruthTableBuilder:
    """模糊真值表构建器"""
    
    def __init__(self):
        self.calibrator = FSCCalibration()
        self.truth_table: Optional[pd.DataFrame] = None
        self.contradictory_cases = []
        self.logical_remainders = []
        self.properties = {}
    
    def build_truth_table(
        self,
        data: pd.DataFrame,
        conditions: List[str],
        outcome: str,
        incl_threshold: float = 0.8,
        ncut: Optional[float] = None,
        include_remainders: bool = True
    ) -> pd.DataFrame:
        """
        构建模糊集真值表
        
        Args:
            data: 校准后的数据框
            conditions: 条件变量列表
            outcome: 结果变量
            incl_threshold: 包含阈值
            ncut: 必要性阈值
            include_remainders: 是否包含逻辑余项
        
        Returns:
            真值表数据框
        """
        # 计算必要性一致性（如果需要）
        if ncut is not None:
            for condition in conditions:
                necessary_consistency = consistency_xy(data[condition], data[outcome])
                if necessary_consistency < ncut:
                    warnings.warn(f"条件 {condition} 的必要性一致性 ({necessary_consistency:.3f}) 低于阈值 ({ncut})")
        
        # 计算每个案例的包含分数
        data = self._calculate_inclusion_scores(data, conditions, outcome)
        
        # 创建配置
        data = self._create_configurations(data, conditions, incl_threshold)
        
        # 聚合同一配置的案例
        truth_table = self._aggregate_configurations(data, conditions, outcome)
        
        # 计算每行的一致性
        truth_table = self._calculate_row_consistencies(truth_table, data, conditions, outcome)
        
        # 识别矛盾组合
        self._identify_contradictory_rows(truth_table)
        
        # 处理逻辑余项
        if include_remainders:
            truth_table = self._add_logical_remainders(truth_table, conditions)
        
        self.truth_table = truth_table
        return truth_table
    
    def _calculate_inclusion_scores(
        self,
        data: pd.DataFrame,
        conditions: List[str],
        outcome: str
    ) -> pd.DataFrame:
        """计算每个案例的包含分数"""
        # 对于fsQCA，包含分数是条件隶属度的函数
        # 这里使用条件的乘积作为包含分数（也可以使用其他函数如最小值）
        condition_cols = data[conditions]
        
        # 计算包含分数 - 这里使用最小值函数（也可以使用其他t-范数）
        inclusion_scores = condition_cols.min(axis=1)
        
        # 对于结果，使用其原始隶属度
        data = data.copy()
        data['inclusion_score'] = inclusion_scores
        
        return data
    
    def _create_configurations(
        self,
        data: pd.DataFrame,
        conditions: List[str],
        incl_threshold: float
    ) -> pd.DataFrame:
        """为每个案例创建配置"""
        data = data.copy()
        
        # 将条件隶属度转换为配置
        for i, condition in enumerate(conditions):
            # 使用阈值将连续隶属度转换为配置
            # 在fsQCA中，配置通常表示为是否超过阈值
            config_col = f"config_{condition}"
            data[config_col] = (data[condition] >= incl_threshold).astype(int)
        
        return data
    
    def _aggregate_configurations(
        self,
        data: pd.DataFrame,
        conditions: List[str],
        outcome: str
    ) -> pd.DataFrame:
        """聚合同一配置的案例"""
        # 获取配置列
        config_cols = [f"config_{cond}" for cond in conditions]
        
        # 按配置分组
        grouped = data.groupby(config_cols)
        
        # 计算每组的统计信息
        aggregated_data = []
        
        for config, group in grouped:
            # 确保config是元组格式
            if not isinstance(config, tuple):
                config = (config,)
            
            # 计算组内统计
            frequency = len(group)
            avg_outcome = group[outcome].mean()
            consistency = consistency_xy(group[conditions].min(axis=1), group[outcome])
            cases = group.index.tolist()
            n_cases = len(group)
            
            # 计算组内包含分数均值
            avg_inclusion = group['inclusion_score'].mean()
            
            row_data = {
                'configuration': config,
                'frequency': frequency,
                'outcome': avg_outcome,
                'consistency': consistency,
                'cases': cases,
                'n_cases': n_cases,
                'inclusion_score': avg_inclusion,
                'PRI_consistency': consistency  # 暂时使用相同值，后续可优化
            }
            
            # 添加各个条件的平均值
            for condition in conditions:
                row_data[f'avg_{condition}'] = group[condition].mean()
            
            aggregated_data.append(row_data)
        
        # 创建真值表
        df = pd.DataFrame(aggregated_data)
        
        # 添加是否为逻辑余项的标识
        df['remainder'] = False
        
        # 添加是否为矛盾组合的标识
        df['contradictory'] = df['consistency'] < 0.5  # 简化判断
        
        return df
    
    def _calculate_row_consistencies(
        self,
        truth_table: pd.DataFrame,
        data: pd.DataFrame,
        conditions: List[str],
        outcome: str
    ) -> pd.DataFrame:
        """计算每行的一致性"""
        # 重新计算每行的一致性
        for idx, row in truth_table.iterrows():
            # 获取属于该配置的所有案例
            config = row['configuration']
            config_mask = True
            for i, condition in enumerate(conditions):
                config_col = f"config_{condition}"
                config_mask = config_mask & (data[config_col] == config[i])
            
            config_data = data[config_mask]
            
            if len(config_data) > 0:
                # 计算该配置的一致性
                condition_values = config_data[conditions].min(axis=1)  # 使用t-范数（最小值）
                outcome_values = config_data[outcome]
                
                consistency = consistency_xy(condition_values, outcome_values)
                truth_table.at[idx, 'consistency'] = consistency
                
                # 计算PRI一致性（Proportional Reduction in Inconsistency）
                # PRI一致性考虑了该组态对结果的贡献
                if consistency > 0:
                    # 简化的PRI计算，实际实现可能更复杂
                    PRI = consistency
                    truth_table.at[idx, 'PRI_consistency'] = PRI
        
        return truth_table
    
    def _identify_contradictory_rows(self, truth_table: pd.DataFrame):
        """识别矛盾组合"""
        # 矛盾组合是指同一配置在不同案例中产生不同的结果
        contradictory_mask = (
            (truth_table['outcome'] >= 0.5) & 
            (truth_table['consistency'] < 0.8)
        ) | (
            (truth_table['outcome'] < 0.5) & 
            (truth_table['consistency'] >= 0.8)
        )
        
        self.contradictory_cases = truth_table[contradictory_mask].index.tolist()
    
    def _add_logical_remainders(
        self,
        truth_table: pd.DataFrame,
        conditions: List[str]
    ) -> pd.DataFrame:
        """添加逻辑余项"""
        # 生成所有可能的配置组合
        n_conditions = len(conditions)
        all_possible_configs = list(product([0, 1], repeat=n_conditions))
        
        # 获取已存在的配置
        existing_configs = set(truth_table['configuration'].apply(lambda x: tuple(x)))
        
        # 找出缺失的配置（逻辑余项）
        missing_configs = [config for config in all_possible_configs if config not in existing_configs]
        
        # 为每个缺失的配置创建逻辑余项行
        remainder_rows = []
        for config in missing_configs:
            remainder_row = {
                'configuration': config,
                'frequency': 0,  # 逻辑余项没有实际案例
                'outcome': np.nan,  # 结果未知
                'consistency': np.nan,  # 一致性未知
                'cases': [],
                'n_cases': 0,
                'inclusion_score': 0,
                'PRI_consistency': np.nan,
                'remainder': True,
                'contradictory': False
            }
            
            # 添加各个条件的列
            for i, condition in enumerate(conditions):
                remainder_row[f'avg_{condition}'] = float(config[i])
            
            remainder_rows.append(remainder_row)
        
        # 将逻辑余项添加到真值表
        if remainder_rows:
            remainder_df = pd.DataFrame(remainder_rows)
            truth_table = pd.concat([truth_table, remainder_df], ignore_index=True)
        
        self.logical_remainders = missing_configs
        return truth_table
    
    def handle_contradictions(self, method: str = 'remove') -> pd.DataFrame:
        """
        处理矛盾组合
        
        Args:
            method: 处理方法 ('remove', 'merge', 'keep')
        
        Returns:
            处理后的真值表
        """
        if method == 'remove':
            # 移除矛盾组合
            truth_table = self.truth_table[~self.truth_table.index.isin(self.contradictory_cases)]
        elif method == 'merge':
            # 合并矛盾组合（简化实现）
            # 在实际应用中，这可能需要更复杂的逻辑
            truth_table = self.truth_table.copy()
            for idx in self.contradictory_cases:
                # 这里可以实现合并逻辑，例如将矛盾组合与最相似的组合合并
                pass
        else:  # 'keep'
            truth_table = self.truth_table.copy()
        
        return truth_table
    
    def calculate_quality_metrics(self) -> Dict[str, float]:
        """计算真值表质量指标"""
        if self.truth_table is None:
            return {}

        metrics = {}

        # 矛盾率
        total_rows = len(self.truth_table)
        contradiction_count = len(self.contradictory_cases)
        metrics['contradiction_rate'] = contradiction_count / total_rows if total_rows > 0 else 0

        # 平均一致性
        valid_consistency = self.truth_table['consistency'].dropna()
        if len(valid_consistency) > 0:
            # 使用numpy的nanmean来避免空切片警告
            metrics['avg_consistency'] = np.nanmean(valid_consistency.values)
        else:
            metrics['avg_consistency'] = 0

        # 逻辑余项比例
        remainder_count = len(self.logical_remainders)
        metrics['remainder_ratio'] = remainder_count / (total_rows + remainder_count) if (total_rows + remainder_count) > 0 else 0

        # 覆盖度
        total_frequency = self.truth_table['frequency'].sum()
        positive_cases = self.truth_table[self.truth_table['outcome'] >= 0.5]
        if len(positive_cases) > 0:
            positive_frequency = positive_cases['frequency'].sum()
        else:
            positive_frequency = 0
        metrics['coverage'] = positive_frequency / total_frequency if total_frequency > 0 else 0

        return metrics


def calculate_fsQCA_consistency(data: pd.DataFrame, conditions: List[str], outcome: str) -> float:
    """
    计算fsQCA的一致性
    
    Args:
        data: 数据框
        conditions: 条件变量列表
        outcome: 结果变量
    
    Returns:
        一致性分数
    """
    # 使用t-范数（通常是最小值）计算条件组合
    condition_combination = data[conditions].min(axis=1)
    
    # 计算一致性
    consistency = consistency_xy(condition_combination, data[outcome])
    
    return consistency


def calculate_fsQCA_coverage(data: pd.DataFrame, conditions: List[str], outcome: str) -> float:
    """
    计算fsQCA的覆盖度
    
    Args:
        data: 数据框
        conditions: 条件变量列表
        outcome: 结果变量
    
    Returns:
        覆盖度分数
    """
    # 使用t-范数（通常是最小值）计算条件组合
    condition_combination = data[conditions].min(axis=1)
    
    # 计算覆盖度
    coverage = coverage_xy(condition_combination, data[outcome])
    
    return coverage


if __name__ == "__main__":
    # 示例用法
    print("模糊真值表构建模块测试")
    
    # 创建示例数据
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'condition1': np.random.uniform(0, 1, 20),
        'condition2': np.random.uniform(0, 1, 20),
        'condition3': np.random.uniform(0, 1, 20),
        'outcome': np.random.uniform(0, 1, 20)
    })
    
    # 初始化真值表构建器
    tt_builder = FuzzyTruthTableBuilder()
    
    # 构建真值表
    conditions = ['condition1', 'condition2', 'condition3']
    outcome = 'outcome'
    
    truth_table = tt_builder.build_truth_table(
        sample_data,
        conditions,
        outcome,
        incl_threshold=0.5
    )
    
    print(f"真值表形状: {truth_table.shape}")
    print(f"矛盾组合数量: {len(tt_builder.contradictory_cases)}")
    print(f"逻辑余项数量: {len(tt_builder.logical_remainders)}")
    
    # 显示真值表的前几行
    print("\n真值表前5行:")
    print(truth_table.head())
    
    # 计算质量指标
    quality_metrics = tt_builder.calculate_quality_metrics()
    print(f"\n质量指标: {quality_metrics}")
    
    # 计算整体一致性
    overall_consistency = calculate_fsQCA_consistency(sample_data, conditions, outcome)
    print(f"\n整体一致性: {overall_consistency:.3f}")
    
    # 计算整体覆盖度
    overall_coverage = calculate_fsQCA_coverage(sample_data, conditions, outcome)
    print(f"整体覆盖度: {overall_coverage:.3f}")