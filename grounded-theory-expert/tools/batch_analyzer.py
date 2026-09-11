#!/usr/bin/env python3
"""
分批渐次分析器 - Batch Analyzer

扎根理论分析的分批处理与渐次整合机制

**解决问题**:
1. 大批量数据(如《西游记》100 回)无法一次性分析
2. 分析中断后无法恢复
3. 没有中间状态持久化
4. 缺乏完整性检查

**核心功能**:
- 分批加载和分析
- 中间状态持久化
- 从中断处恢复
- 渐次整合(每批都合并到累积状态)
- 完整性检查
- 理论饱和度检验

**作者**: grounded-theory-expert
**版本**: 1.0.0
**日期**: 2026-03-07
"""

import os
import sys
import json
import glob
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Set
from datetime import datetime
from dataclasses import dataclass, asdict, field
from enum import Enum
import shutil


# ==================== 枚举和数据类 ====================

class BatchStatus(Enum):
    """批次状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    MERGED = "merged"


class AnalysisPhase(Enum):
    """分析阶段枚举"""
    OPEN_CODING = "open_coding"
    AXIAL_CODING = "axial_coding"
    SELECTIVE_CODING = "selective_coding"
    SATURATION_TEST = "saturation_test"
    FINAL_INTEGRATION = "final_integration"


@dataclass
class BatchState:
    """批次状态数据类"""
    batch_number: int
    file_count: int
    files: List[str]
    status: BatchStatus
    start_time: str
    end_time: Optional[str]
    result_file: str
    error_message: Optional[str]


@dataclass
class CumulativeState:
    """累积状态数据类"""
    total_files: int
    total_batches: int
    completed_batches: int
    current_batch: int
    overall_status: str
    concepts: Set[str]
    categories: Dict[str, Any]
    relationships: List[Dict[str, Any]]
    memos: List[Dict[str, Any]]
    last_updated: str


@dataclass
class AnalysisProgress:
    """分析进度数据类"""
    phase: AnalysisPhase
    current_batch: int
    total_batches: int
    completed_files: int
    total_files: int
    progress_percentage: float
    status: str
    timestamp: str


# ==================== 分批分析器 ====================

class BatchAnalyzer:
    """
    分批渐次分析器
    
    核心逻辑：
    1. 分批加载文件
    2. 分析当前批次
    3. 合并到累积状态
    4. 保存中间状态
    5. 最终整合
    6. 理论饱和度检验
    """

    def __init__(self,
                 data_dir: str,
                 batch_size: int = 10,
                 state_dir: str = "./state/batch_analysis",
                 log_dir: str = "./logs/batch_analysis",
                 file_pattern: str = "*.txt"):
        """
        初始化分批分析器
        
        参数:
            data_dir: 数据文件目录
            batch_size: 每批文件数量
            state_dir: 状态保存目录
            log_dir: 日志目录
            file_pattern: 文件匹配模式
        """
        self.data_dir = Path(data_dir)
        self.batch_size = batch_size
        self.state_dir = Path(state_dir)
        self.log_dir = Path(log_dir)
        self.file_pattern = file_pattern
        
        # 创建目录
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置日志
        self._setup_logging()
        
        # 发现数据文件
        self.all_files = self._discover_files()
        self.total_files = len(self.all_files)
        self.total_batches = (self.total_files + batch_size - 1) // batch_size
        
        # 状态变量
        self.current_batch = 0
        self.cumulative_state = self._initialize_cumulative_state()
        self.batch_states: List[BatchState] = []
        
        # 状态文件路径
        self.state_file = self.state_dir / "batch_analysis_state.json"
        self.progress_file = self.state_dir / "analysis_progress.json"
        
        self.logger.info(f"分批分析器初始化完成")
        self.logger.info(f"  数据目录：{self.data_dir}")
        self.logger.info(f"  文件总数：{self.total_files}")
        self.logger.info(f"  批次大小：{self.batch_size}")
        self.logger.info(f"  总批次数：{self.total_batches}")

    def _setup_logging(self):
        """配置日志"""
        log_file = self.log_dir / f"batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BatchAnalyzer')

    def _discover_files(self) -> List[str]:
        """发现数据文件"""
        pattern = str(self.data_dir / self.file_pattern)
        files = glob.glob(pattern)
        
        # 按文件名排序
        files.sort()
        
        self.logger.info(f"发现 {len(files)} 个数据文件")
        
        return files

    def _initialize_cumulative_state(self) -> CumulativeState:
        """初始化累积状态"""
        return CumulativeState(
            total_files=self.total_files,
            total_batches=self.total_batches,
            completed_batches=0,
            current_batch=0,
            overall_status="initialized",
            concepts=set(),
            categories={},
            relationships=[],
            memos=[],
            last_updated=datetime.now().isoformat()
        )

    def load_batch(self, batch_number: int) -> List[str]:
        """
        加载指定批次的文件
        
        参数:
            batch_number: 批次号(从 1 开始)
            
        返回:
            文件路径列表
        """
        if batch_number < 1 or batch_number > self.total_batches:
            raise ValueError(f"无效的批次号：{batch_number} (1-{self.total_batches})")
        
        start_idx = (batch_number - 1) * self.batch_size
        end_idx = min(start_idx + self.batch_size, self.total_files)
        
        batch_files = self.all_files[start_idx:end_idx]
        
        self.logger.info(f"加载批次 {batch_number}: {len(batch_files)} 个文件")
        for f in batch_files:
            self.logger.debug(f"  - {Path(f).name}")
        
        return batch_files

    def analyze_batch(self, files: List[str], batch_number: int) -> Dict[str, Any]:
        """
        分析单个批次
        
        参数:
            files: 文件列表
            batch_number: 批次号
            
        返回:
            分析结果字典
        """
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"分析批次 {batch_number}/{self.total_batches}")
        self.logger.info(f"{'='*60}")
        
        # 创建批次状态
        batch_state = BatchState(
            batch_number=batch_number,
            file_count=len(files),
            files=[Path(f).name for f in files],
            status=BatchStatus.IN_PROGRESS,
            start_time=datetime.now().isoformat(),
            end_time=None,
            result_file="",
            error_message=None
        )
        
        try:
            # TODO: 调用实际的分析逻辑
            # 这里使用模拟实现
            result = self._perform_batch_analysis(files, batch_number)
            
            # 更新批次状态
            batch_state.status = BatchStatus.COMPLETED
            batch_state.end_time = datetime.now().isoformat()
            batch_state.result_file = str(self.state_dir / f"batch_{batch_number}_result.json")
            
            # 保存批次结果
            self._save_batch_result(batch_number, result)
            
            self.logger.info(f"批次 {batch_number} 分析完成")
            
            return result
            
        except Exception as e:
            self.logger.error(f"批次 {batch_number} 分析失败：{str(e)}")
            batch_state.status = BatchStatus.FAILED
            batch_state.error_message = str(e)
            batch_state.end_time = datetime.now().isoformat()
            
            raise

    def _perform_batch_analysis(self, files: List[str], batch_number: int) -> Dict[str, Any]:
        """
        执行批次分析
        
        参数:
            files: 文件列表
            batch_number: 批次号
            
        返回:
            分析结果
        """
        # TODO: 实现实际的分析逻辑
        # 目前使用模拟实现
        
        self.logger.info(f"执行批次 {batch_number} 的分析...")
        
        # 模拟分析结果
        result = {
            'batch_number': batch_number,
            'files_analyzed': len(files),
            'timestamp': datetime.now().isoformat(),
            'open_coding': {
                'concepts': [f"concept_{batch_number}_{i}" for i in range(5)],
                'codes': [f"code_{batch_number}_{i}" for i in range(10)]
            },
            'axial_coding': {
                'categories': {
                    f"category_{batch_number}_A": {
                        'properties': ['prop1', 'prop2'],
                        'dimensions': ['dim1', 'dim2']
                    }
                }
            },
            'memos': [
                {
                    'id': f"memo_{batch_number}_1",
                    'content': f"批次 {batch_number} 的分析备忘录",
                    'timestamp': datetime.now().isoformat()
                }
            ]
        }
        
        # 模拟处理时间
        import time
        time.sleep(0.5)  # 模拟 0.5 秒处理时间
        
        return result

    def merge_to_cumulative(self, result: Dict[str, Any], batch_number: int):
        """
        将批次结果合并到累积状态
        
        参数:
            result: 批次分析结果
            batch_number: 批次号
        """
        self.logger.info(f"合并批次 {batch_number} 到累积状态")
        
        # 合并概念
        new_concepts = set(result.get('open_coding', {}).get('concepts', []))
        old_concept_count = len(self.cumulative_state.concepts)
        self.cumulative_state.concepts.update(new_concepts)
        new_concept_count = len(self.cumulative_state.concepts)
        self.logger.info(f"  概念：{old_concept_count} → {new_concept_count} (+{new_concept_count - old_concept_count})")
        
        # 合并范畴
        batch_categories = result.get('axial_coding', {}).get('categories', {})
        for cat_name, cat_data in batch_categories.items():
            if cat_name not in self.cumulative_state.categories:
                self.cumulative_state.categories[cat_name] = cat_data
                self.logger.info(f"  新增范畴：{cat_name}")
            else:
                # 更新现有范畴
                existing = self.cumulative_state.categories[cat_name]
                existing['properties'].extend(cat_data.get('properties', []))
                existing['dimensions'].extend(cat_data.get('dimensions', []))
                self.logger.info(f"  更新范畴：{cat_name}")
        
        # 合并关系
        new_relationships = result.get('relationships', [])
        self.cumulative_state.relationships.extend(new_relationships)
        self.logger.info(f"  关系：{len(self.cumulative_state.relationships)} 条")
        
        # 合并备忘录
        batch_memos = result.get('memos', [])
        self.cumulative_state.memos.extend(batch_memos)
        self.logger.info(f"  备忘录：{len(self.cumulative_state.memos)} 条")
        
        # 更新状态
        self.cumulative_state.completed_batches = batch_number
        self.cumulative_state.current_batch = batch_number
        self.cumulative_state.last_updated = datetime.now().isoformat()
        
        # 更新进度
        progress = batch_number / self.total_batches * 100
        self.logger.info(f"  进度：{progress:.1f}%")

    def save_state(self, batch_number: int, status: str = "in_progress"):
        """
        保存中间状态
        
        参数:
            batch_number: 当前批次号
            status: 状态字符串
        """
        self.logger.info(f"保存中间状态 (批次 {batch_number})")
        
        # 准备状态数据
        state_data = {
            'metadata': {
                'version': '1.0',
                'created_at': datetime.now().isoformat(),
                'data_dir': str(self.data_dir),
                'batch_size': self.batch_size,
                'file_pattern': self.file_pattern
            },
            'progress': {
                'total_files': self.total_files,
                'total_batches': self.total_batches,
                'completed_batches': self.cumulative_state.completed_batches,
                'current_batch': batch_number,
                'status': status
            },
            'cumulative_state': {
                'concepts': list(self.cumulative_state.concepts),
                'categories': self.cumulative_state.categories,
                'relationships': self.cumulative_state.relationships,
                'memos': self.cumulative_state.memos
            },
            'batch_history': [
                asdict(bs) for bs in self.batch_states
            ]
        }
        
        # 保存到文件
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, ensure_ascii=False, indent=2)
        
        # 保存进度文件(用于快速查询)
        progress_data = {
            'current_batch': batch_number,
            'total_batches': self.total_batches,
            'completed_files': batch_number * self.batch_size,
            'total_files': self.total_files,
            'progress_percentage': round(batch_number / self.total_batches * 100, 2),
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"状态已保存到：{self.state_file}")

    def load_state(self) -> Optional[Dict[str, Any]]:
        """
        加载之前的状态
        
        返回:
            状态字典, 如果没有之前的状态则返回 None
        """
        if not self.state_file.exists():
            self.logger.info("未找到之前的状态文件")
            return None
        
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            # 恢复累积状态
            self.cumulative_state.concepts = set(state_data['cumulative_state']['concepts'])
            self.cumulative_state.categories = state_data['cumulative_state']['categories']
            self.cumulative_state.relationships = state_data['cumulative_state']['relationships']
            self.cumulative_state.memos = state_data['cumulative_state']['memos']
            
            # 恢复进度
            self.cumulative_state.completed_batches = state_data['progress']['completed_batches']
            self.current_batch = state_data['progress']['current_batch']
            
            self.logger.info(f"已从 {self.state_file} 恢复状态")
            self.logger.info(f"  已完成批次：{self.cumulative_state.completed_batches}/{self.total_batches}")
            self.logger.info(f"  概念数量：{len(self.cumulative_state.concepts)}")
            self.logger.info(f"  范畴数量：{len(self.cumulative_state.categories)}")
            
            return state_data
            
        except Exception as e:
            self.logger.error(f"加载状态失败：{str(e)}")
            return None

    def can_resume(self) -> bool:
        """检查是否可以恢复"""
        return self.state_file.exists()

    def get_resume_info(self) -> Dict[str, Any]:
        """获取恢复信息"""
        if not self.can_resume():
            return {'can_resume': False}
        
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            return {
                'can_resume': True,
                'completed_batches': state_data['progress']['completed_batches'],
                'total_batches': self.total_batches,
                'last_batch': state_data['progress']['current_batch'],
                'concepts_count': len(state_data['cumulative_state']['concepts']),
                'categories_count': len(state_data['cumulative_state']['categories']),
                'status': state_data['progress']['status']
            }
        except:
            return {'can_resume': False}

    def analyze_all_batches(self, resume: bool = False) -> Dict[str, Any]:
        """
        分批分析所有文件
        
        参数:
            resume: 是否从断点恢复
            
        返回:
            最终分析结果
        """
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"开始分批分析")
        self.logger.info(f"{'='*80}")
        self.logger.info(f"总文件数：{self.total_files}")
        self.logger.info(f"批次大小：{self.batch_size}")
        self.logger.info(f"总批次数：{self.total_batches}")
        
        # 尝试恢复
        start_batch = 1
        if resume and self.can_resume():
            resume_info = self.get_resume_info()
            if resume_info['can_resume']:
                self.load_state()
                start_batch = self.cumulative_state.completed_batches + 1
                self.logger.info(f"从批次 {start_batch} 恢复分析")
        
        # 分析每个批次
        for batch_num in range(start_batch, self.total_batches + 1):
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"批次 {batch_num}/{self.total_batches}")
            self.logger.info(f"{'='*60}")
            
            try:
                # 1. 加载当前批次文件
                files = self.load_batch(batch_num)
                
                # 2. 分析当前批次
                result = self.analyze_batch(files, batch_num)
                
                # 3. 合并到累积状态
                self.merge_to_cumulative(result, batch_num)
                
                # 4. 保存中间状态
                self.save_state(batch_num, 'completed')
                
                # 5. 记录批次状态
                batch_state = BatchState(
                    batch_number=batch_num,
                    file_count=len(files),
                    files=[Path(f).name for f in files],
                    status=BatchStatus.COMPLETED,
                    start_time=datetime.now().isoformat(),
                    end_time=datetime.now().isoformat(),
                    result_file=str(self.state_dir / f"batch_{batch_num}_result.json"),
                    error_message=None
                )
                self.batch_states.append(batch_state)
                
            except Exception as e:
                self.logger.error(f"批次 {batch_num} 分析失败：{str(e)}")
                
                # 保存失败状态
                self.save_state(batch_num, 'failed')
                
                # 记录失败状态
                batch_state = BatchState(
                    batch_number=batch_num,
                    file_count=len(files) if 'files' in locals() else 0,
                    files=[Path(f).name for f in files] if 'files' in locals() else [],
                    status=BatchStatus.FAILED,
                    start_time=datetime.now().isoformat(),
                    end_time=datetime.now().isoformat(),
                    result_file="",
                    error_message=str(e)
                )
                self.batch_states.append(batch_state)
                
                # 抛出异常
                raise
        
        # 所有批次完成
        self.cumulative_state.overall_status = "all_batches_completed"
        self.save_state(self.total_batches, 'all_batches_completed')
        
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"所有批次分析完成！")
        self.logger.info(f"{'='*80}")
        
        # 5. 最终整合
        self.logger.info("执行最终整合...")
        final_result = self.final_integration()
        
        # 6. 理论饱和度检验
        self.logger.info("执行理论饱和度检验...")
        saturation_result = self.saturation_test()
        
        return {
            'status': 'completed',
            'total_files': self.total_files,
            'total_batches': self.total_batches,
            'completed_batches': self.cumulative_state.completed_batches,
            'final_result': final_result,
            'saturation_test': saturation_result,
            'cumulative_state': {
                'concepts_count': len(self.cumulative_state.concepts),
                'categories_count': len(self.cumulative_state.categories),
                'relationships_count': len(self.cumulative_state.relationships),
                'memos_count': len(self.cumulative_state.memos)
            }
        }

    def final_integration(self) -> Dict[str, Any]:
        """
        最终整合
        
        整合所有批次的分析结果, 形成完整的理论框架
        
        返回:
            最终整合结果
        """
        self.logger.info("执行最终整合")
        
        # 整合概念
        all_concepts = list(self.cumulative_state.concepts)
        
        # 整合范畴
        all_categories = self.cumulative_state.categories
        
        # 整合关系
        all_relationships = self.cumulative_state.relationships
        
        # 整合备忘录
        all_memos = self.cumulative_state.memos
        
        # 生成整合报告
        integration_result = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'final_integration',
            'summary': {
                'total_concepts': len(all_concepts),
                'total_categories': len(all_categories),
                'total_relationships': len(all_relationships),
                'total_memos': len(all_memos),
                'total_files_analyzed': self.total_files,
                'total_batches': self.total_batches
            },
            'concepts': all_concepts,
            'categories': all_categories,
            'relationships': all_relationships,
            'memos': all_memos,
            'integration_notes': [
                f"整合了 {self.total_batches} 个批次的分析结果",
                f"共分析 {self.total_files} 个文件",
                f"识别出 {len(all_concepts)} 个概念",
                f"形成 {len(all_categories)} 个范畴",
                f"建立 {len(all_relationships)} 条关系"
            ]
        }
        
        # 保存整合结果
        integration_file = self.state_dir / "final_integration_result.json"
        with open(integration_file, 'w', encoding='utf-8') as f:
            json.dump(integration_result, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"最终整合结果已保存到：{integration_file}")
        
        return integration_result

    def saturation_test(self) -> Dict[str, Any]:
        """
        理论饱和度检验
        
        基于累积状态执行理论饱和度检验
        
        返回:
            饱和度检验结果
        """
        self.logger.info("执行理论饱和度检验")
        
        # 导入饱和度评估模块
        from assess_saturation import (
            assess_concept_saturation,
            assess_category_saturation,
            assess_relationship_saturation,
            assess_overall_saturation
        )
        
        # 概念饱和度
        # 使用最后 3 个批次的概念作为"新数据"
        recent_concepts = set()
        if len(self.batch_states) >= 3:
            for bs in self.batch_states[-3:]:
                result_file = Path(bs.result_file)
                if result_file.exists():
                    with open(result_file, 'r', encoding='utf-8') as f:
                        result = json.load(f)
                    recent_concepts.update(result.get('open_coding', {}).get('concepts', []))
        
        existing_concepts = self.cumulative_state.concepts - recent_concepts
        concept_sat = assess_concept_saturation(existing_concepts, recent_concepts)
        
        # 范畴饱和度
        existing_categories = self.cumulative_state.categories
        recent_categories = {}
        if len(self.batch_states) >= 3:
            for bs in self.batch_states[-3:]:
                result_file = Path(bs.result_file)
                if result_file.exists():
                    with open(result_file, 'r', encoding='utf-8') as f:
                        result = json.load(f)
                    recent_categories.update(result.get('axial_coding', {}).get('categories', {}))
        
        category_sat = assess_category_saturation(existing_categories, recent_categories)
        
        # 关系饱和度
        existing_relationships = self.cumulative_state.relationships[:-10] if len(self.cumulative_state.relationships) > 10 else self.cumulative_state.relationships
        recent_relationships = self.cumulative_state.relationships[-10:] if len(self.cumulative_state.relationships) > 10 else []
        
        relationship_sat = assess_relationship_saturation(existing_relationships, recent_relationships)
        
        # 命题饱和度(使用关系作为代理)
        proposition_sat = {
            'score': category_sat['score'],  # 使用范畴饱和度作为代理
            'status': category_sat['status'],
            'total_propositions': len(existing_relationships),
            'new_propositions': len(recent_relationships)
        }
        
        # 整体饱和度
        overall_sat = assess_overall_saturation(
            concept_sat, category_sat, relationship_sat, proposition_sat
        )
        
        # 生成饱和度报告
        saturation_result = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'saturation_test',
            'overall_saturation': overall_sat['overall_saturation'],
            'status': overall_sat['status'],
            'by_dimension': {
                'concept_saturation': concept_sat,
                'category_saturation': category_sat,
                'relationship_saturation': relationship_sat,
                'proposition_saturation': proposition_sat
            },
            'recommendations': overall_sat['recommendations'],
            'summary': f"理论饱和度：{overall_sat['overall_saturation']:.1f}% - {overall_sat['status']}"
        }
        
        # 保存饱和度报告
        saturation_file = self.state_dir / "saturation_test_result.json"
        with open(saturation_file, 'w', encoding='utf-8') as f:
            json.dump(saturation_result, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"饱和度检验结果：{overall_sat['overall_saturation']:.1f}% - {overall_sat['status']}")
        self.logger.info(f"饱和度报告已保存到：{saturation_file}")
        
        return saturation_result

    def check_completeness(self) -> Dict[str, Any]:
        """
        完整性检查
        
        检查是否所有文件都已分析
        
        返回:
            完整性检查结果
        """
        self.logger.info("执行完整性检查")
        
        # 检查已分析的文件
        analyzed_files = []
        for bs in self.batch_states:
            if bs.status == BatchStatus.COMPLETED:
                analyzed_files.extend(bs.files)
        
        # 检查是否有遗漏
        all_file_names = [Path(f).name for f in self.all_files]
        missing_files = set(all_file_names) - set(analyzed_files)
        
        completeness_result = {
            'timestamp': datetime.now().isoformat(),
            'total_files': self.total_files,
            'analyzed_files': len(analyzed_files),
            'missing_files': list(missing_files),
            'is_complete': len(missing_files) == 0,
            'completeness_percentage': round(len(analyzed_files) / self.total_files * 100, 2)
        }
        
        if not completeness_result['is_complete']:
            self.logger.warning(f"发现 {len(missing_files)} 个未分析的文件")
        else:
            self.logger.info("所有文件都已分析, 完整性检查通过")
        
        return completeness_result

    def get_progress(self) -> AnalysisProgress:
        """获取当前进度"""
        completed_files = self.cumulative_state.completed_batches * self.batch_size
        
        return AnalysisProgress(
            phase=AnalysisPhase.OPEN_CODING,  # 简化处理
            current_batch=self.current_batch,
            total_batches=self.total_batches,
            completed_files=min(completed_files, self.total_files),
            total_files=self.total_files,
            progress_percentage=round(self.current_batch / self.total_batches * 100, 2),
            status=self.cumulative_state.overall_status,
            timestamp=datetime.now().isoformat()
        )

    def _save_batch_result(self, batch_number: int, result: Dict[str, Any]):
        """保存批次结果"""
        result_file = self.state_dir / f"batch_{batch_number}_result.json"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        self.logger.debug(f"批次结果已保存到：{result_file}")


# ==================== 主函数 ====================

if __name__ == '__main__':
    # 测试分批分析器
    print("="*80)
    print("分批渐次分析器测试")
    print("="*80)
    print()
    
    # 创建测试数据目录
    test_data_dir = Path("./test_data")
    test_data_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建模拟数据文件
    print("创建测试数据文件...")
    for i in range(1, 26):  # 创建 25 个测试文件
        test_file = test_data_dir / f"chapter_{i:03d}.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(f"第{i}章的测试内容\n")
    
    print(f"已创建 {25} 个测试文件")
    print()
    
    # 创建分批分析器
    analyzer = BatchAnalyzer(
        data_dir=str(test_data_dir),
        batch_size=10,  # 每批 10 个文件
        state_dir="./test_state",
        log_dir="./test_logs"
    )
    
    print(f"总文件数：{analyzer.total_files}")
    print(f"批次大小：{analyzer.batch_size}")
    print(f"总批次数：{analyzer.total_batches}")
    print()
    
    # 测试恢复功能
    print("测试恢复功能...")
    resume_info = analyzer.get_resume_info()
    print(f"可以恢复：{resume_info.get('can_resume', False)}")
    print()
    
    # 运行分批分析
    print("开始分批分析...")
    try:
        result = analyzer.analyze_all_batches(resume=False)
        
        print()
        print("="*80)
        print("分析完成！")
        print("="*80)
        print(f"总文件数：{result['total_files']}")
        print(f"总批次数：{result['total_batches']}")
        print(f"完成批次：{result['completed_batches']}")
        print(f"概念数量：{result['cumulative_state']['concepts_count']}")
        print(f"范畴数量：{result['cumulative_state']['categories_count']}")
        print(f"理论饱和度：{result['saturation_test']['overall_saturation']:.1f}%")
        print(f"饱和度状态：{result['saturation_test']['status']}")
        
    except Exception as e:
        print(f"分析失败：{str(e)}")
        print("可以从中断处恢复分析")
    
    # 清理测试数据
    print()
    print("清理测试数据...")
    shutil.rmtree(test_data_dir, ignore_errors=True)
    shutil.rmtree("./test_state", ignore_errors=True)
    shutil.rmtree("./test_logs", ignore_errors=True)
    print("测试完成！")
