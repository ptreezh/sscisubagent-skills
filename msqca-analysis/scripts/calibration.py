#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多值定性比较分析(msQCA) - 校准模块
提供多种校准方法和一致性检验功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
import warnings
import math
from collections import Counter


class QCACalibration:
    """QCA校准类，支持多种校准方法"""
    
    def __init__(self):
        self.calibration_methods = {
            'direct': self._direct_calibration,
            'indirect': self._indirect_calibration,
            'multi_value': self._multi_value_calibration,
            'auto': self._auto_calibration
        }
        self.calibration_results = {}
        
    def calibrate_variable(self, 
                         data: pd.Series, 
                         method: str = 'direct',
                         thresholds: Optional[Union[float, List[float]]] = None,
                         fuzzy_sets: bool = False) -> pd.Series:
        """
        校准单个变量
        
        Parameters:
        -----------
        data : pd.Series
            原始数据
        method : str
            校准方法: 'direct', 'indirect', 'multi_value', 'auto'
        thresholds : Union[float, List[float], None]
            校准阈值
        fuzzy_sets : bool
            是否使用模糊集校准
            
        Returns:
        --------
        pd.Series
            校准后的数据
        """
        if method not in self.calibration_methods:
            raise ValueError(f"不支持的校准方法: {method}")
            
        return self.calibration_methods[method](data, thresholds, fuzzy_sets)
    
    def _direct_calibration(self, 
                           data: pd.Series, 
                           thresholds: Optional[Union[float, List[float]]] = None,
                           fuzzy_sets: bool = False) -> pd.Series:
        """
        直接校准方法
        
        基于理论或经验阈值直接将连续变量转换为分类变量
        """
        if thresholds is None:
            # 自动确定阈值
            thresholds = self._auto_thresholds(data)
        
        if isinstance(thresholds, (int, float)):
            thresholds = [thresholds]
            
        if fuzzy_sets:
            return self._fuzzy_calibration(data, thresholds)
        else:
            return pd.cut(data, 
                         bins=[-np.inf] + thresholds + [np.inf],
                         labels=range(len(thresholds) + 1),
                         include_lowest=True)
    
    def _indirect_calibration(self, 
                             data: pd.Series, 
                             thresholds: Optional[Union[float, List[float]]] = None,
                             fuzzy_sets: bool = False) -> pd.Series:
        """
        间接校准方法
        
        通过隶属函数进行渐进式转换
        """
        if thresholds is None:
            thresholds = self._auto_thresholds(data)
            
        if isinstance(thresholds, (int, float)):
            thresholds = [thresholds]
            
        calibrated = pd.Series(index=data.index, dtype=float)
        
        for i, threshold in enumerate(thresholds):
            if i == 0:
                # 第一个阈值以下的区域
                calibrated[data <= threshold] = 0.0
            elif i == len(thresholds) - 1:
                # 最后一个阈值以上的区域
                calibrated[data > threshold] = 1.0
            else:
                # 中间区域使用线性插值
                prev_threshold = thresholds[i-1]
                mask = (data > prev_threshold) & (data <= threshold)
                calibrated[mask] = (data[mask] - prev_threshold) / (threshold - prev_threshold)
        
        return calibrated
    
    def _multi_value_calibration(self, 
                                data: pd.Series, 
                                thresholds: Optional[Union[float, List[float]]] = None,
                                fuzzy_sets: bool = False) -> pd.Series:
        """
        多值校准方法
        
        处理具有多个类别的变量
        """
        unique_values = sorted(data.unique())
        
        if len(unique_values) <= 3:
            # 如果值较少，使用直接校准
            return self._direct_calibration(data, thresholds, fuzzy_sets)
        
        # 对多值变量进行重新编码
        value_mapping = {val: i for i, val in enumerate(unique_values)}
        return data.map(value_mapping)
    
    def _auto_calibration(self, 
                         data: pd.Series, 
                         thresholds: Optional[Union[float, List[float]]] = None,
                         fuzzy_sets: bool = False) -> pd.Series:
        """
        自动校准方法
        
        基于数据分布自动确定最优校准方案
        """
        # 检测数据类型和分布特征
        data_type = self._detect_data_type(data)
        
        if data_type == 'categorical':
            return self._multi_value_calibration(data, thresholds, fuzzy_sets)
        elif data_type == 'continuous':
            # 使用分位数确定阈值
            n_categories = min(3, len(data.unique()) // 3)  # 最多3个类别
            if n_categories < 2:
                n_categories = 2
                
            quantiles = np.linspace(0, 1, n_categories + 1)[1:-1]
            auto_thresholds = [data.quantile(q) for q in quantiles]
            
            return self._direct_calibration(data, auto_thresholds, fuzzy_sets)
        else:
            # 默认使用直接校准
            return self._direct_calibration(data, thresholds, fuzzy_sets)
    
    def _fuzzy_calibration(self, 
                          data: pd.Series, 
                          thresholds: List[float]) -> pd.Series:
        """
        模糊集校准
        
        使用模糊隶属函数进行校准
        """
        calibrated = pd.Series(index=data.index, dtype=float)
        
        for i, threshold in enumerate(thresholds):
            if i == 0:
                # 完全不属于集合
                calibrated[data <= threshold] = 0.0
            else:
                # 使用S型隶属函数
                prev_threshold = thresholds[i-1]
                x = data[(data > prev_threshold) & (data <= threshold)]
                
                # S型函数参数
                a = prev_threshold
                b = threshold
                c = (a + b) / 2
                
                # 计算隶属度
                membership = 1 / (1 + np.exp(-4 * (x - c) / (b - a)))
                calibrated[x.index] = membership
        
        # 最后一个阈值以上的区域
        calibrated[data > thresholds[-1]] = 1.0
        
        return calibrated
    
    def _auto_thresholds(self, data: pd.Series) -> List[float]:
        """
        自动确定校准阈值

        基于数据分布特征自动选择最优阈值
        """
        # 使用分位数方法
        q25, q75 = data.quantile([0.25, 0.75])
        median = data.median()

        # 使用分位数作为阈值
        thresholds = [q25, median, q75]

        return thresholds[:2]  # 返回最多2个阈值
    
    def _detect_data_type(self, data: pd.Series) -> str:
        """
        检测数据类型
        
        Returns:
        --------
        str: 'continuous', 'categorical', 'ordinal'
        """
        unique_count = data.nunique()
        total_count = len(data)
        
        # 如果唯一值比例小于10%，认为是分类变量
        if unique_count / total_count < 0.1:
            return 'categorical'
        
        # 检查是否为有序变量
        if data.dtype in ['int64', 'float64']:
            if unique_count <= 10:
                return 'ordinal'
            else:
                return 'continuous'
        
        return 'categorical'
    
    def validate_calibration(self, 
                           original_data: pd.Series, 
                           calibrated_data: pd.Series) -> Dict:
        """
        验证校准质量
        
        Parameters:
        -----------
        original_data : pd.Series
            原始数据
        calibrated_data : pd.Series
            校准后数据
            
        Returns:
        --------
        Dict
            验证结果指标
        """
        validation_results = {
            'consistency_score': self._calculate_consistency(original_data, calibrated_data),
            'coverage_score': self._calculate_coverage(calibrated_data),
            'information_loss': self._calculate_information_loss(original_data, calibrated_data),
            'thresholds_used': self._extract_thresholds(original_data, calibrated_data)
        }
        
        return validation_results
    
    def _calculate_consistency(self, original: pd.Series, calibrated: pd.Series) -> float:
        """计算校准一致性分数"""
        # 这里简化处理，实际应该基于理论一致性
        orig_unique = len(original.unique())
        cal_unique = len(calibrated.unique())

        if orig_unique == 0:
            return 0.0

        consistency = min(1.0, cal_unique / max(1, orig_unique))

        # 确保结果是有效的数值
        if np.isnan(consistency) or np.isinf(consistency):
            consistency = 0.0

        return consistency
    
    def _calculate_coverage(self, calibrated: pd.Series) -> float:
        """计算覆盖度分数"""
        return 1.0 - (calibrated.isna().sum() / len(calibrated))
    
    def _calculate_information_loss(self, original: pd.Series, calibrated: pd.Series) -> float:
        """计算信息损失"""
        # 使用熵的变化来衡量信息损失
        orig_entropy = self._calculate_entropy(original)
        cal_entropy = self._calculate_entropy(calibrated)

        return max(0, orig_entropy - cal_entropy)

    def _calculate_entropy(self, series: pd.Series) -> float:
        """计算序列的熵值"""
        # 计算值的频率
        value_counts = series.value_counts()
        total_count = len(series)

        if total_count == 0:
            return 0.0

        # 计算概率分布
        probabilities = value_counts / total_count

        # 计算熵值 (使用自然对数)
        entropy = 0.0
        for prob in probabilities:
            if prob > 0:  # 避免log(0)的错误
                entropy -= prob * math.log(prob)

        return entropy
    
    def _extract_thresholds(self, original: pd.Series, calibrated: pd.Series) -> List[float]:
        """提取使用的阈值"""
        if calibrated.dtype in ['int64', 'float64']:
            if len(calibrated.unique()) <= 3:
                return sorted(original.groupby(calibrated).mean().values)
        return []


def main():
    """示例用法"""
    # 创建示例数据
    np.random.seed(42)
    sample_data = pd.Series(np.random.normal(50, 15, 100))
    
    # 初始化校准器
    calibrator = QCACalibration()
    
    # 执行校准
    calibrated = calibrator.calibrate_variable(sample_data, method='auto')
    
    # 验证校准质量
    validation = calibrator.validate_calibration(sample_data, calibrated)
    
    print("原始数据统计:")
    print(sample_data.describe())
    print("\n校准后数据分布:")
    print(calibrated.value_counts().sort_index())
    print("\n校准验证结果:")
    for key, value in validation.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()