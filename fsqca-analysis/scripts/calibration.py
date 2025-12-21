#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模糊集定性比较分析(fsQCA) - 模糊集校准模块
实现连续隶属度的校准方法
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
import warnings


class FSCCalibration:
    """模糊集校准类 - 专门处理连续隶属度校准"""
    
    def __init__(self):
        self.calibration_methods = {
            'direct': self._direct_calibration,
            'indirect': self._indirect_calibration,
            'threshold': self._threshold_calibration,
            'interpolation': self._interpolation_calibration,
            'gaussian': self._gaussian_calibration,
            'sigmoid': self._sigmoid_calibration
        }
    
    def calibrate_variable(
        self,
        series: pd.Series,
        method: str = 'auto',
        **kwargs
    ) -> pd.Series:
        """
        校准单个变量为模糊集隶属度
        
        Args:
            series: 原始数据序列
            method: 校准方法 ('auto', 'direct', 'indirect', 'threshold', 'interpolation', 'gaussian', 'sigmoid')
            **kwargs: 校准参数
        
        Returns:
            校准后的模糊集隶属度序列
        """
        if method == 'auto':
            method = self._determine_best_method(series)
        
        if method not in self.calibration_methods:
            raise ValueError(f"不支持的校准方法: {method}")
        
        # 调用相应的校准方法
        calibrated_series = self.calibration_methods[method](series, **kwargs)
        
        # 确保隶属度在[0, 1]范围内
        calibrated_series = np.clip(calibrated_series, 0, 1)
        
        return pd.Series(calibrated_series, index=series.index, name=series.name)
    
    def _determine_best_method(self, series: pd.Series) -> str:
        """自动确定最佳校准方法"""
        # 分析数据特征以选择最佳校准方法
        data_type = series.dtype
        unique_count = series.nunique()
        range_size = series.max() - series.min()
        
        if data_type in ['int64', 'float64']:
            if unique_count > 20 and range_size > 10:
                return 'direct'  # 连续数据，取值丰富
            elif unique_count <= 10:
                return 'threshold'  # 离散数据
            else:
                return 'interpolation'  # 连续数据，取值较少
        else:
            return 'direct'  # 非数值数据
    
    def _direct_calibration(
        self,
        series: pd.Series,
        thresholds: Optional[Tuple[float, float, float]] = None,
        **kwargs
    ) -> np.ndarray:
        """
        直接校准法 - 基于三个锚点的校准
        
        Args:
            series: 原始数据序列
            thresholds: 三个阈值 (完全隶属, 交叉点, 完全不隶属)
        
        Returns:
            校准后的隶属度数组
        """
        # 如果未提供阈值，自动计算
        if thresholds is None:
            # 使用分位数作为默认阈值 (95%, 50%, 5%)
            thresholds = (
                series.quantile(0.95),
                series.quantile(0.50),
                series.quantile(0.05)
            )
        
        full_membership, cross_point, no_membership = thresholds
        
        # 确保阈值顺序正确
        if full_membership < cross_point or cross_point < no_membership:
            warnings.warn("阈值顺序可能不正确，已自动调整")
            full_membership, cross_point, no_membership = sorted([full_membership, cross_point, no_membership], reverse=True)
        
        # 计算隶属度
        result = np.zeros_like(series, dtype=float)
        
        # 完全隶属区间 [full_membership, +inf)
        result[series >= full_membership] = 1.0
        
        # 完全不隶属区间 (-inf, no_membership]
        result[series <= no_membership] = 0.0
        
        # 过渡区间 (no_membership, full_membership)
        mask = (series > no_membership) & (series < full_membership)
        if mask.any():
            if full_membership != cross_point:
                # 使用线性插值
                lower_half = mask & (series <= cross_point)
                if lower_half.any():
                    result[lower_half] = (series[lower_half] - no_membership) / (cross_point - no_membership) * 0.5
                
                upper_half = mask & (series > cross_point)
                if upper_half.any():
                    result[upper_half] = 0.5 + (series[upper_half] - cross_point) / (full_membership - cross_point) * 0.5
            else:
                # 如果全隶属和交叉点相同，使用简化的线性插值
                result[mask] = (series[mask] - no_membership) / (full_membership - no_membership)
        
        return result
    
    def _threshold_calibration(
        self,
        series: pd.Series,
        thresholds: Optional[Tuple[float, float]] = None,
        **kwargs
    ) -> np.ndarray:
        """
        阈值校准法 - 基于两个阈值的校准
        
        Args:
            series: 原始数据序列
            thresholds: 两个阈值 (完全隶属阈值, 完全不隶属阈值)
        
        Returns:
            校准后的隶属度数组
        """
        if thresholds is None:
            # 使用分位数作为默认阈值
            thresholds = (series.quantile(0.8), series.quantile(0.2))
        
        full_membership, no_membership = thresholds
        
        # 确保阈值顺序正确
        if full_membership < no_membership:
            full_membership, no_membership = no_membership, full_membership
        
        # 计算隶属度
        result = np.zeros_like(series, dtype=float)
        
        # 完全隶属区间
        result[series >= full_membership] = 1.0
        
        # 完全不隶属区间
        result[series <= no_membership] = 0.0
        
        # 过渡区间
        mask = (series > no_membership) & (series < full_membership)
        if mask.any():
            result[mask] = (series[mask] - no_membership) / (full_membership - no_membership)
        
        return result
    
    def _interpolation_calibration(
        self,
        series: pd.Series,
        anchor_points: Optional[List[Tuple[float, float]]] = None,
        **kwargs
    ) -> np.ndarray:
        """
        插值校准法 - 基于多个锚点的插值校准

        Args:
            series: 原始数据序列
            anchor_points: 锚点列表 [(原始值, 隶属度), ...]

        Returns:
            校准后的隶属度数组
        """
        if anchor_points is None:
            # 默认使用5个锚点：最小值(0)、25%分位数(0.25)、中位数(0.5)、75%分位数(0.75)、最大值(1)
            anchor_points = [
                (series.min(), 0.0),
                (series.quantile(0.25), 0.25),
                (series.quantile(0.50), 0.50),
                (series.quantile(0.75), 0.75),
                (series.max(), 1.0)
            ]

        # 对锚点按原始值排序
        sorted_anchor_points = sorted(anchor_points, key=lambda x: x[0])

        # 提取原始值和隶属度
        original_values = [point[0] for point in sorted_anchor_points]
        membership_values = [point[1] for point in sorted_anchor_points]

        # 确保隶属度在[0,1]范围内
        membership_values = [max(0.0, min(1.0, val)) for val in membership_values]

        # 对series中的每个值进行插值
        result = np.zeros_like(series.values, dtype=float)

        series_values = series.values
        for i, value in enumerate(series_values):
            # 找到value所属的区间
            if value <= original_values[0]:
                # 小于最小锚点值，使用最小隶属度
                result[i] = membership_values[0]
            elif value >= original_values[-1]:
                # 大于最大锚点值，使用最大隶属度
                result[i] = membership_values[-1]
            else:
                # 在锚点范围内，进行线性插值
                # 找到相邻的两个锚点
                for j in range(len(original_values) - 1):
                    if original_values[j] <= value <= original_values[j+1]:
                        x0, x1 = original_values[j], original_values[j+1]
                        y0, y1 = membership_values[j], membership_values[j+1]

                        # 线性插值公式
                        if x1 != x0:  # 避免除零错误
                            result[i] = y0 + (y1 - y0) * (value - x0) / (x1 - x0)
                        else:
                            result[i] = y0
                        break

        # 确保结果在[0, 1]范围内
        result = np.clip(result, 0, 1)

        return result
    
    def _gaussian_calibration(
        self,
        series: pd.Series,
        center: Optional[float] = None,
        sigma: Optional[float] = None,
        **kwargs
    ) -> np.ndarray:
        """
        高斯校准法 - 基于高斯函数的校准
        
        Args:
            series: 原始数据序列
            center: 高斯函数中心点
            sigma: 高斯函数标准差
        
        Returns:
            校准后的隶属度数组
        """
        if center is None:
            center = series.mean()
        
        if sigma is None:
            sigma = series.std()
            if sigma == 0:
                sigma = 1  # 避免除零错误
        
        # 计算高斯隶属度
        result = np.exp(-0.5 * ((series - center) / sigma) ** 2)
        
        # 归一化到[0, 1]区间（如果中心点在数据范围内）
        if center >= series.min() and center <= series.max():
            max_val = np.exp(0)  # 中心点处的值为1
            min_val = np.exp(-0.5 * ((series - center) / sigma).max() ** 2)
            if max_val != min_val:
                result = (result - min_val) / (max_val - min_val)
        
        return result
    
    def _sigmoid_calibration(
        self,
        series: pd.Series,
        center: Optional[float] = None,
        steepness: Optional[float] = None,
        **kwargs
    ) -> np.ndarray:
        """
        Sigmoid校准法 - 基于Sigmoid函数的校准
        
        Args:
            series: 原始数据序列
            center: Sigmoid函数中心点
            steepness: Sigmoid函数陡峭度
        
        Returns:
            校准后的隶属度数组
        """
        if center is None:
            center = series.median()
        
        if steepness is None:
            steepness = 1.0 / (series.max() - series.min()) * 6  # 使范围覆盖大部分sigmoid曲线
        
        # 计算Sigmoid隶属度
        result = 1.0 / (1.0 + np.exp(-steepness * (series - center)))
        
        return result
    
    def _indirect_calibration(
        self,
        series: pd.Series,
        membership_mapping: Optional[Dict[Any, float]] = None,
        **kwargs
    ) -> np.ndarray:
        """
        间接校准法 - 基于分类到隶属度的映射
        
        Args:
            series: 原始数据序列
            membership_mapping: 分类到隶属度的映射字典
        
        Returns:
            校准后的隶属度数组
        """
        if membership_mapping is None:
            # 如果没有提供映射，尝试基于唯一值自动创建映射
            unique_values = series.unique()
            n_values = len(unique_values)
            
            # 按值大小排序，然后分配隶属度
            sorted_values = sorted(unique_values)
            membership_mapping = {}
            
            for i, value in enumerate(sorted_values):
                # 线性分配隶属度
                membership_mapping[value] = i / (n_values - 1) if n_values > 1 else 0.5
        
        # 应用映射
        result = series.map(membership_mapping).values
        
        # 处理未映射的值（设为0.5）
        if result is None or pd.isna(result).any():
            result = np.where(pd.isna(result), 0.5, result)
        
        return result
    
    def calibrate_dataset(
        self,
        df: pd.DataFrame,
        calibration_plan: Dict[str, Dict[str, Any]]
    ) -> pd.DataFrame:
        """
        校准整个数据集
        
        Args:
            df: 原始数据框
            calibration_plan: 校准计划，包含每个变量的校准方法和参数
        
        Returns:
            校准后的数据框
        """
        calibrated_df = df.copy()
        
        for column, plan in calibration_plan.items():
            if column in df.columns:
                method = plan.get('method', 'auto')
                params = plan.get('params', {})
                
                calibrated_df[column] = self.calibrate_variable(
                    df[column], method=method, **params
                )
        
        return calibrated_df


def consistency_xy(X: pd.Series, Y: pd.Series) -> float:
    """
    计算X对Y的一致性

    Args:
        X: 前提条件的模糊集隶属度
        Y: 结果的模糊集隶属度

    Returns:
        一致性分数
    """
    # 确保X和Y不为空
    if len(X) == 0 or len(Y) == 0:
        return 0.0

    # 一致性 = min(X, Y)的和 / X的和
    min_vals = np.minimum(X, Y)
    numerator = np.nansum(min_vals)  # 使用nansum处理NaN值
    denominator = np.nansum(X)  # 使用nansum处理NaN值

    if denominator == 0 or np.isnan(denominator):
        return 0.0

    result = numerator / denominator
    return result if not np.isnan(result) else 0.0


def coverage_xy(X: pd.Series, Y: pd.Series) -> float:
    """
    计算X对Y的覆盖度

    Args:
        X: 前提条件的模糊集隶属度
        Y: 结果的模糊集隶属度

    Returns:
        覆盖度分数
    """
    # 确保X和Y不为空
    if len(X) == 0 or len(Y) == 0:
        return 0.0

    # 覆盖度 = min(X, Y)的和 / Y的和
    min_vals = np.minimum(X, Y)
    numerator = np.nansum(min_vals)  # 使用nansum处理NaN值
    denominator = np.nansum(Y)  # 使用nansum处理NaN值

    if denominator == 0 or np.isnan(denominator):
        return 0.0

    result = numerator / denominator
    return result if not np.isnan(result) else 0.0


def calculate_necessary_consistency(data: pd.DataFrame, condition: str, outcome: str) -> float:
    """
    计算必要性一致性

    Args:
        data: 数据框
        condition: 条件变量名
        outcome: 结果变量名

    Returns:
        必要性一致性分数
    """
    if condition not in data.columns or outcome not in data.columns:
        return 0.0

    X = data[condition]
    Y = data[outcome]

    # 确保X和Y不为空
    if len(X) == 0 or len(Y) == 0:
        return 0.0

    # 必要性一致性 = min(X, Y)的和 / X的和
    min_vals = np.minimum(X, Y)
    numerator = np.nansum(min_vals)
    denominator = np.nansum(X)

    if denominator == 0 or np.isnan(denominator):
        return 0.0

    result = numerator / denominator
    return result if not np.isnan(result) else 0.0


def calculate_necessary_coverage(data: pd.DataFrame, condition: str, outcome: str) -> float:
    """
    计算必要性覆盖度

    Args:
        data: 数据框
        condition: 条件变量名
        outcome: 结果变量名

    Returns:
        必要性覆盖度分数
    """
    if condition not in data.columns or outcome not in data.columns:
        return 0.0

    X = data[condition]
    Y = data[outcome]

    # 确保X和Y不为空
    if len(X) == 0 or len(Y) == 0:
        return 0.0

    # 必要性覆盖度 = min(X, Y)的和 / Y的和
    min_vals = np.minimum(X, Y)
    numerator = np.nansum(min_vals)
    denominator = np.nansum(Y)

    if denominator == 0 or np.isnan(denominator):
        return 0.0

    result = numerator / denominator
    return result if not np.isnan(result) else 0.0


if __name__ == "__main__":
    # 示例用法
    print("模糊集校准模块测试")
    
    # 创建示例数据
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'condition1': np.random.uniform(0, 10, 20),
        'condition2': np.random.uniform(0, 10, 20),
        'outcome': np.random.uniform(0, 1, 20)
    })
    
    # 初始化校准器
    calibrator = FSCCalibration()
    
    # 测试直接校准
    calibrated_c1 = calibrator.calibrate_variable(
        sample_data['condition1'],
        method='direct',
        thresholds=(8, 5, 2)
    )
    
    print(f"原始数据范围: {sample_data['condition1'].min():.2f} - {sample_data['condition1'].max():.2f}")
    print(f"校准后范围: {calibrated_c1.min():.2f} - {calibrated_c1.max():.2f}")
    
    # 测试阈值校准
    calibrated_c2 = calibrator.calibrate_variable(
        sample_data['condition2'],
        method='threshold',
        thresholds=(7, 3)
    )
    
    print(f"阈值校准后范围: {calibrated_c2.min():.2f} - {calibrated_c2.max():.2f}")
    
    # 计算一致性
    consistency = consistency_xy(calibrated_c1, sample_data['outcome'])
    print(f"一致性分数: {consistency:.3f}")
    
    # 计算覆盖度
    coverage = coverage_xy(calibrated_c1, sample_data['outcome'])
    print(f"覆盖度分数: {coverage:.3f}")