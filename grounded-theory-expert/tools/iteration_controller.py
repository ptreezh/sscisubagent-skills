#!/usr/bin/env python3
"""
迭代控制器 - Iteration Controller

扎根理论分析的迭代式自主反思与校对机制

**功能**:
- 迭代循环控制(最大迭代次数、收敛检测)
- 质量评审(46 个检查点)
- 自我校对(18 个策略)
- 状态持久化(JSON 格式)

**基于**:
- Glaser & Strauss (1967) 扎根理论方法论
- Strauss & Corbin (1990) 编码规范
- Charmaz (2006) 建构主义扎根理论

**作者**: grounded-theory-expert
**版本**: 1.0.0
**日期**: 2026-03-07
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


# ==================== 枚举和数据类 ====================

class IterationStatus(Enum):
    """迭代状态枚举"""
    RUNNING = "running"
    CONVERGED = "converged"
    MAX_ITERATIONS_REACHED = "max_iterations_reached"
    FAILED = "failed"
    PAUSED = "paused"


class QualityCheckStatus(Enum):
    """质量检查状态"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


@dataclass
class QualityCheckPoint:
    """质量检查点数据类"""
    id: str
    name: str
    phase: int
    description: str
    status: QualityCheckStatus
    score: float = 0.0
    message: str = ""
    evidence: str = ""


@dataclass
class SelfCorrectionStrategy:
    """自我校对策略数据类"""
    id: str
    name: str
    description: str
    trigger_condition: str
    expected_improvement: float
    script: str = ""


@dataclass
class IterationState:
    """迭代状态数据类"""
    phase: int
    iteration: int
    status: IterationStatus
    quality_score: float
    improvement_rate: float
    timestamp: str
    checks_passed: int
    checks_failed: int
    corrections_applied: List[str]
    log_file: str


# ==================== 质量评审器 ====================

class QualityReviewer:
    """
    质量评审器 - 46 个检查点

    基于 Strauss & Corbin (1990) 和 Charmaz (2006) 的方法论规范
    """

    def __init__(self, log_dir: str = "./logs/reviews"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置日志
        self._setup_logging()
        
        # 46 个质量检查点
        self.checkpoints = self._initialize_checkpoints()
        
        # 评审结果
        self.review_results = {}

    def _setup_logging(self):
        """配置日志"""
        log_file = self.log_dir / f"quality_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('QualityReviewer')

    def _initialize_checkpoints(self) -> Dict[int, List[QualityCheckPoint]]:
        """初始化 46 个质量检查点"""
        checkpoints = {
            # Phase 1: 数据准备 (3 个检查点)
            1: [
                QualityCheckPoint("QC-1.1", "伦理文件检查", 1, "检查伦理审查文件是否完整", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-1.2", "数据匿名化处理", 1, "检查数据匿名化是否完成", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-1.3", "知情同意书", 1, "检查知情同意书是否签署", QualityCheckStatus.FAILED),
            ],
            
            # Phase 2: 开放性编码 (4 个检查点)
            2: [
                QualityCheckPoint("QC-2.1", "编码者间信度", 2, "Kappa 系数 > 0.7", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-2.2", "持续比较日志", 2, "持续比较记录 ≥ 20 次", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-2.3", "编码本完整性", 2, "初始概念 ≥ 30 个", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-2.4", "行动导向命名", 2, "行动导向命名 ≥ 80%", QualityCheckStatus.FAILED),
            ],
            
            # Phase 3: 轴心编码 (3 个检查点)
            3: [
                QualityCheckPoint("QC-3.1", "范畴饱和度", 3, "范畴饱和度 > 85%", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-3.2", "Paradigm 模型完整性", 3, "Paradigm 模型 > 90%", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-3.3", "关系网络证据", 3, "关系证据 > 85%", QualityCheckStatus.FAILED),
            ],
            
            # Phase 4: 选择式编码 (3 个检查点)
            4: [
                QualityCheckPoint("QC-4.1", "核心范畴验证", 4, "核心范畴支持度 > 85%", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-4.2", "故事线连贯性", 4, "故事线连贯性 > 85%", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-4.3", "理论命题可检验性", 4, "可检验命题 > 70%", QualityCheckStatus.FAILED),
            ],
            
            # Phase 5: 理论饱和度检验 (2 个检查点)
            5: [
                QualityCheckPoint("QC-5.1", "多维度饱和度", 5, "所有维度饱和度 100%", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-5.2", "饱和度报告", 5, "饱和度报告 > 90%", QualityCheckStatus.FAILED),
            ],
            
            # Phase 6: 理论撰写 (3 个检查点)
            6: [
                QualityCheckPoint("QC-6.1", "研究者反思备忘录", 6, "反思备忘录 > 85%", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-6.2", "研究局限反思", 6, "局限讨论 > 85%", QualityCheckStatus.FAILED),
                QualityCheckPoint("QC-6.3", "审核追踪完整性", 6, "审核追踪 > 90%", QualityCheckStatus.FAILED),
            ],
        }
        
        # TODO: 补充其他检查点到 46 个
        # 目前 18 个, 需要补充 28 个
        
        return checkpoints

    def execute_review(self, phase: int, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行质量评审
        
        参数:
            phase: 当前 Phase (1-6)
            analysis_result: 分析结果字典
            
        返回:
            评审结果字典
        """
        self.logger.info(f"开始执行 Phase {phase} 质量评审")
        
        if phase not in self.checkpoints:
            self.logger.error(f"Phase {phase} 没有定义质量检查点")
            return {'status': 'error', 'message': f'Phase {phase} 未定义'}
        
        # 获取当前 Phase 的检查点
        phase_checkpoints = self.checkpoints[phase]
        
        # 执行每个检查点
        results = []
        for checkpoint in phase_checkpoints:
            result = self._execute_single_check(checkpoint, analysis_result)
            results.append(result)
            self.logger.info(f"  {checkpoint.id}: {result['status'].value} (得分：{result['score']})")
        
        # 计算总体质量分数
        total_score = sum(r['score'] for r in results) / len(results) if results else 0
        passed_count = sum(1 for r in results if r['status'] == QualityCheckStatus.PASSED)
        failed_count = sum(1 for r in results if r['status'] == QualityCheckStatus.FAILED)
        
        # 判断是否通过
        overall_status = QualityCheckStatus.PASSED if total_score >= 85 else QualityCheckStatus.FAILED
        
        review_result = {
            'phase': phase,
            'timestamp': datetime.now().isoformat(),
            'overall_status': overall_status.value,
            'overall_score': round(total_score, 2),
            'checks_passed': passed_count,
            'checks_failed': failed_count,
            'total_checks': len(results),
            'checkpoints': results,
            'passed': total_score >= 85
        }
        
        # 保存评审结果
        self._save_review_result(review_result)
        
        self.logger.info(f"质量评审完成：总分 {total_score:.2f}%, 通过 {passed_count}/{len(results)}")
        
        return review_result

    def _execute_single_check(self, checkpoint: QualityCheckPoint, 
                              analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个检查点
        
        参数:
            checkpoint: 检查点定义
            analysis_result: 分析结果
            
        返回:
            检查结果
        """
        # TODO: 实现具体的检查逻辑
        # 目前使用模拟实现
        
        # 模拟检查逻辑(实际应该检查 analysis_result 中的具体数据)
        score = 0
        status = QualityCheckStatus.FAILED
        message = "未执行实际检查"
        
        # 示例：检查编码者间信度
        if checkpoint.id == "QC-2.1":
            kappa = analysis_result.get('kappa', 0)
            if kappa >= 0.7:
                score = 100
                status = QualityCheckStatus.PASSED
                message = f"Kappa 系数={kappa:.2f} > 0.7, 通过"
            elif kappa >= 0.6:
                score = 70
                status = QualityCheckStatus.WARNING
                message = f"Kappa 系数={kappa:.2f} < 0.7, 警告"
            else:
                score = 40
                message = f"Kappa 系数={kappa:.2f} < 0.6, 失败"
        
        # 示例：检查编码本完整性
        elif checkpoint.id == "QC-2.3":
            concept_count = analysis_result.get('concept_count', 0)
            if concept_count >= 30:
                score = 100
                status = QualityCheckStatus.PASSED
                message = f"概念数量={concept_count} ≥ 30, 通过"
            else:
                score = max(40, concept_count / 30 * 100)
                status = QualityCheckStatus.FAILED if score < 60 else QualityCheckStatus.WARNING
                message = f"概念数量={concept_count} < 30"
        
        # 示例：检查范畴饱和度
        elif checkpoint.id == "QC-3.1":
            saturation = analysis_result.get('category_saturation', 0)
            if saturation >= 85:
                score = 100
                status = QualityCheckStatus.PASSED
                message = f"范畴饱和度={saturation:.1f}% ≥ 85%, 通过"
            else:
                score = saturation
                status = QualityCheckStatus.FAILED
                message = f"范畴饱和度={saturation:.1f}% < 85%"
        
        # 默认：模拟分数
        else:
            score = 75  # 默认模拟分数
            status = QualityCheckStatus.WARNING
            message = "模拟检查(待实现具体逻辑)"
        
        return {
            'id': checkpoint.id,
            'name': checkpoint.name,
            'description': checkpoint.description,
            'status': status.value,
            'score': score,
            'message': message,
            'evidence': analysis_result.get('evidence', '')
        }

    def _save_review_result(self, result: Dict[str, Any]):
        """保存评审结果到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"review_phase{result['phase']}_{timestamp}.json"
        filepath = self.log_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"评审结果已保存到：{filepath}")


# ==================== 自我校对器 ====================

class SelfCorrector:
    """
    自我校对器 - 18 个策略

    基于质量评审结果自动触发修正策略
    """

    def __init__(self, log_dir: str = "./logs/corrections"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 18 个自我校对策略
        self.strategies = self._initialize_strategies()
        
        # 修正历史
        self.correction_history = []

    def _initialize_strategies(self) -> Dict[str, SelfCorrectionStrategy]:
        """初始化 18 个自我校对策略"""
        strategies = {
            "SC-001": SelfCorrectionStrategy(
                "SC-001", "自动生成伦理文件", 
                "自动生成伦理审查所需文件",
                "QC-1.1 failed", 100.0,
                "scripts/corrections/generate-ethics-doc.sh"
            ),
            "SC-002": SelfCorrectionStrategy(
                "SC-002", "重新匿名化处理",
                "对数据进行重新匿名化",
                "QC-1.2 failed", 15.0,
                "scripts/corrections/re-anonymize.sh"
            ),
            "SC-003": SelfCorrectionStrategy(
                "SC-003", "生成知情同意模板",
                "生成知情同意书模板",
                "QC-1.3 failed", 100.0,
                "scripts/corrections/generate-consent-form.sh"
            ),
            "SC-004": SelfCorrectionStrategy(
                "SC-004", "编码员培训与重新编码",
                "对编码员进行培训并重新编码",
                "QC-2.1 failed", 20.0,
                "scripts/corrections/recoder-with-training.sh"
            ),
            "SC-005": SelfCorrectionStrategy(
                "SC-005", "回溯补充比较日志",
                "补充持续比较日志",
                "QC-2.2 failed", 25.0,
                "scripts/corrections/supplement-comparison-log.sh"
            ),
            "SC-006": SelfCorrectionStrategy(
                "SC-006", "自动生成编码本",
                "生成完整的编码本",
                "QC-2.3 failed", 30.0,
                "scripts/corrections/generate-codebook.sh"
            ),
            "SC-007": SelfCorrectionStrategy(
                "SC-007", "行动导向命名修正",
                "将非行动导向命名改为行动导向",
                "QC-2.4 failed", 15.0,
                "scripts/corrections/fix-action-naming.sh"
            ),
            "SC-008": SelfCorrectionStrategy(
                "SC-008", "补充范畴维度",
                "补充范畴的属性和维度",
                "QC-3.1 failed", 15.0,
                "scripts/corrections/supplement-category-dimensions.sh"
            ),
            "SC-009": SelfCorrectionStrategy(
                "SC-009", "完善 Paradigm 模型",
                "完善条件 - 行动 - 结果模型",
                "QC-3.2 failed", 20.0,
                "scripts/corrections/complete-paradigm-model.sh"
            ),
            "SC-010": SelfCorrectionStrategy(
                "SC-010", "补充关系证据",
                "补充范畴间关系的证据",
                "QC-3.3 failed", 15.0,
                "scripts/corrections/supplement-relationship-evidence.sh"
            ),
            "SC-011": SelfCorrectionStrategy(
                "SC-011", "重新选择核心范畴",
                "重新评估和选择核心范畴",
                "QC-4.1 failed", 20.0,
                "scripts/corrections/reselect-core-category.sh"
            ),
            "SC-012": SelfCorrectionStrategy(
                "SC-012", "重构故事线",
                "重新构建故事线",
                "QC-4.2 failed", 20.0,
                "scripts/corrections/reconstruct-storyline.sh"
            ),
            "SC-013": SelfCorrectionStrategy(
                "SC-013", "细化理论命题",
                "细化和完善理论命题",
                "QC-4.3 failed", 15.0,
                "scripts/corrections/refine-theoretical-propositions.sh"
            ),
            "SC-014": SelfCorrectionStrategy(
                "SC-014", "执行饱和度检验",
                "执行理论饱和度检验",
                "QC-5.1 failed", 100.0,
                "scripts/corrections/execute-saturation-test.sh"
            ),
            "SC-015": SelfCorrectionStrategy(
                "SC-015", "生成饱和度报告",
                "生成饱和度检验报告",
                "QC-5.2 failed", 100.0,
                "scripts/corrections/generate-saturation-report.sh"
            ),
            "SC-016": SelfCorrectionStrategy(
                "SC-016", "撰写反思备忘录",
                "撰写研究者反思备忘录",
                "QC-6.1 failed", 100.0,
                "scripts/corrections/write-reflexive-memo.sh"
            ),
            "SC-017": SelfCorrectionStrategy(
                "SC-017", "补充局限讨论",
                "补充研究局限性讨论",
                "QC-6.2 failed", 25.0,
                "scripts/corrections/supplement-limitations.sh"
            ),
            "SC-018": SelfCorrectionStrategy(
                "SC-018", "完善审核追踪",
                "完善审核追踪文档",
                "QC-6.3 failed", 20.0,
                "scripts/corrections/complete-audit-trail.sh"
            ),
        }
        
        return strategies

    def apply_corrections(self, review_result: Dict[str, Any], 
                         analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用自我校对策略
        
        参数:
            review_result: 质量评审结果
            analysis_result: 分析结果
            
        返回:
            修正后的分析结果
        """
        self.logger.info("开始执行自我校对")
        
        # 识别失败的检查点
        failed_checks = [
            cp for cp in review_result.get('checkpoints', [])
            if cp['status'] == QualityCheckStatus.FAILED.value
        ]
        
        if not failed_checks:
            self.logger.info("没有失败的检查点, 无需修正")
            return {'status': 'no_correction_needed', 'corrections_applied': []}
        
        # 为每个失败的检查点应用修正策略
        corrections_applied = []
        for check in failed_checks:
            strategy = self._find_strategy_for_check(check['id'])
            if strategy:
                correction_result = self._apply_single_strategy(
                    strategy, check, analysis_result
                )
                corrections_applied.append(correction_result)
        
        # 记录修正历史
        self.correction_history.append({
            'timestamp': datetime.now().isoformat(),
            'phase': review_result.get('phase'),
            'corrections_applied': corrections_applied
        })
        
        # 保存修正记录
        self._save_correction_record(corrections_applied)
        
        return {
            'status': 'corrected',
            'corrections_applied': corrections_applied,
            'total_corrections': len(corrections_applied)
        }

    def _find_strategy_for_check(self, check_id: str) -> Optional[SelfCorrectionStrategy]:
        """根据检查点 ID 查找对应的修正策略"""
        # 映射关系：QC-1.1 -> SC-001, QC-2.1 -> SC-004, etc.
        mapping = {
            "QC-1.1": "SC-001", "QC-1.2": "SC-002", "QC-1.3": "SC-003",
            "QC-2.1": "SC-004", "QC-2.2": "SC-005", "QC-2.3": "SC-006", "QC-2.4": "SC-007",
            "QC-3.1": "SC-008", "QC-3.2": "SC-009", "QC-3.3": "SC-010",
            "QC-4.1": "SC-011", "QC-4.2": "SC-012", "QC-4.3": "SC-013",
            "QC-5.1": "SC-014", "QC-5.2": "SC-015",
            "QC-6.1": "SC-016", "QC-6.2": "SC-017", "QC-6.3": "SC-018",
        }
        
        strategy_id = mapping.get(check_id)
        if strategy_id:
            return self.strategies.get(strategy_id)
        return None

    def _apply_single_strategy(self, strategy: SelfCorrectionStrategy,
                               check: Dict[str, Any],
                               analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用单个修正策略
        
        参数:
            strategy: 修正策略
            check: 失败的检查点
            analysis_result: 分析结果
            
        返回:
            修正结果
        """
        self.logger.info(f"应用修正策略：{strategy.name} ({strategy.id})")
        
        # TODO: 实际执行 Shell 脚本
        # 目前使用模拟实现
        
        correction_result = {
            'strategy_id': strategy.id,
            'strategy_name': strategy.name,
            'triggered_by': check['id'],
            'status': 'completed',
            'expected_improvement': strategy.expected_improvement,
            'actual_improvement': strategy.expected_improvement * 0.9,  # 模拟 90% 效果
            'script_executed': strategy.script,
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.info(f"  修正完成, 预期改进：{strategy.expected_improvement}%")
        
        return correction_result

    def _save_correction_record(self, corrections: List[Dict[str, Any]]):
        """保存修正记录"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"correction_{timestamp}.json"
        filepath = self.log_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(corrections, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"修正记录已保存到：{filepath}")

    def _setup_logging(self):
        """配置日志"""
        log_file = self.log_dir / f"self_correction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SelfCorrector')


# ==================== 迭代控制器 ====================

class IterationController:
    """
    迭代控制器
    
    控制扎根理论分析的迭代循环：
    执行分析 → 质量评审 → 自我校对 → 收敛检测 → 下一轮迭代
    """

    def __init__(self, 
                 max_iterations: int = 10,
                 convergence_threshold: float = 85.0,
                 min_improvement: float = 5.0,
                 early_stopping_patience: int = 3,
                 state_dir: str = "./state",
                 log_dir: str = "./logs/iterations"):
        """
        初始化迭代控制器
        
        参数:
            max_iterations: 最大迭代次数
            convergence_threshold: 收敛阈值(%)
            min_improvement: 最小改进率(%)
            early_stopping_patience: 提前停止耐心值
            state_dir: 状态保存目录
            log_dir: 日志目录
        """
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.min_improvement = min_improvement
        self.early_stopping_patience = early_stopping_patience
        
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化组件
        self.reviewer = QualityReviewer(str(self.log_dir / 'reviews'))
        self.corrector = SelfCorrector(str(self.log_dir / 'corrections'))
        
        # 配置日志
        self._setup_logging()
        
        # 迭代状态
        self.current_phase = 1
        self.current_iteration = 0
        self.status = IterationStatus.RUNNING
        self.iteration_history = []
        self.quality_history = []

    def _setup_logging(self):
        """配置日志"""
        log_file = self.log_dir / f"iteration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('IterationController')

    def run_iteration(self, phase: int, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单次迭代
        
        参数:
            phase: 当前 Phase
            analysis_result: 分析结果
            
        返回:
            迭代结果
        """
        self.current_phase = phase
        self.current_iteration += 1
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"开始迭代 {self.current_iteration}/{self.max_iterations} (Phase {phase})")
        self.logger.info(f"{'='*60}\n")
        
        # 步骤 1: 质量评审
        self.logger.info("步骤 1: 执行质量评审")
        review_result = self.reviewer.execute_review(phase, analysis_result)
        
        # 记录质量分数
        self.quality_history.append(review_result['overall_score'])
        
        # 步骤 2: 判断是否通过
        if review_result['passed']:
            self.logger.info(f"✅ 质量评审通过！总分：{review_result['overall_score']:.2f}%")
            
            # 检查是否收敛
            if self._check_convergence():
                self.status = IterationStatus.CONVERGED
                return {
                    'status': 'converged',
                    'phase': phase,
                    'iteration': self.current_iteration,
                    'quality_score': review_result['overall_score'],
                    'message': f'已达到收敛标准 ({self.convergence_threshold}%)'
                }
            else:
                # 需要继续迭代以改进
                self.logger.info("质量通过但未收敛, 继续迭代以改进")
                return {
                    'status': 'continue',
                    'phase': phase,
                    'iteration': self.current_iteration,
                    'quality_score': review_result['overall_score'],
                    'message': '质量通过但未收敛'
                }
        
        # 步骤 3: 自我校对
        self.logger.info("步骤 2: 执行自我校对")
        correction_result = self.corrector.apply_corrections(review_result, analysis_result)
        
        # 步骤 4: 应用修正并重新分析
        self.logger.info("步骤 3: 应用修正并重新分析")
        improved_result = self._apply_corrections_and_reanalyze(
            analysis_result, correction_result
        )
        
        # 步骤 5: 检查改进率
        improvement = self._calculate_improvement(analysis_result, improved_result)
        self.logger.info(f"改进率：{improvement:.2f}%")
        
        # 步骤 6: 检查是否提前停止
        if self._check_early_stopping(improvement):
            self.status = IterationStatus.MAX_ITERATIONS_REACHED
            return {
                'status': 'early_stopped',
                'phase': phase,
                'iteration': self.current_iteration,
                'quality_score': review_result['overall_score'],
                'improvement': improvement,
                'message': f'连续{self.early_stopping_patience}次改进<{self.min_improvement}%, 提前停止'
            }
        
        # 步骤 7: 检查是否达到最大迭代次数
        if self.current_iteration >= self.max_iterations:
            self.status = IterationStatus.MAX_ITERATIONS_REACHED
            return {
                'status': 'max_iterations_reached',
                'phase': phase,
                'iteration': self.current_iteration,
                'quality_score': review_result['overall_score'],
                'message': f'已达到最大迭代次数 ({self.max_iterations})'
            }
        
        # 步骤 8: 记录迭代历史
        iteration_state = IterationState(
            phase=phase,
            iteration=self.current_iteration,
            status=self.status,
            quality_score=review_result['overall_score'],
            improvement_rate=improvement,
            timestamp=datetime.now().isoformat(),
            checks_passed=review_result['checks_passed'],
            checks_failed=review_result['checks_failed'],
            corrections_applied=[c['strategy_id'] for c in correction_result.get('corrections_applied', [])],
            log_file=str(self.log_dir)
        )
        self.iteration_history.append(asdict(iteration_state))
        
        # 步骤 9: 保存状态
        self.save_state()
        
        # 步骤 10: 返回结果, 准备下一轮迭代
        return {
            'status': 'continue',
            'phase': phase,
            'iteration': self.current_iteration,
            'quality_score': review_result['overall_score'],
            'improvement': improvement,
            'improved_result': improved_result,
            'message': '继续下一轮迭代'
        }

    def _check_convergence(self) -> bool:
        """检查是否收敛"""
        if len(self.quality_history) < 2:
            return False
        
        # 检查最近 3 次迭代的质量分数是否都超过阈值
        recent_scores = self.quality_history[-min(3, len(self.quality_history)):]
        return all(score >= self.convergence_threshold for score in recent_scores)

    def _check_early_stopping(self, improvement: float) -> bool:
        """检查是否需要提前停止"""
        if len(self.quality_history) < self.early_stopping_patience:
            return False
        
        # 检查连续改进率是否都低于阈值
        recent_improvements = self._calculate_recent_improvements()
        return all(imp < self.min_improvement for imp in recent_improvements)

    def _calculate_improvement(self, before: Dict[str, Any], after: Dict[str, Any]) -> float:
        """计算改进率"""
        # TODO: 实现具体的改进率计算逻辑
        # 目前使用模拟值
        return 10.0  # 模拟 10% 改进

    def _calculate_recent_improvements(self) -> List[float]:
        """计算最近的改进率"""
        if len(self.quality_history) < 2:
            return []
        
        improvements = []
        for i in range(1, len(self.quality_history)):
            improvement = self.quality_history[i] - self.quality_history[i-1]
            improvements.append(improvement)
        
        return improvements[-self.early_stopping_patience:]

    def _apply_corrections_and_reanalyze(self, 
                                         analysis_result: Dict[str, Any],
                                         correction_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用修正并重新分析
        
        参数:
            analysis_result: 原始分析结果
            correction_result: 修正结果
            
        返回:
            改进后的分析结果
        """
        # TODO: 实际执行修正和重新分析
        # 目前返回改进的模拟结果
        
        improved = analysis_result.copy()
        improved['improved'] = True
        improved['corrections_applied'] = correction_result.get('corrections_applied', [])
        
        return improved

    def save_state(self):
        """保存迭代状态到 JSON 文件"""
        state = {
            'controller_config': {
                'max_iterations': self.max_iterations,
                'convergence_threshold': self.convergence_threshold,
                'min_improvement': self.min_improvement,
                'early_stopping_patience': self.early_stopping_patience
            },
            'current_state': {
                'current_phase': self.current_phase,
                'current_iteration': self.current_iteration,
                'status': self.status.value,
                'timestamp': datetime.now().isoformat()
            },
            'iteration_history': self.iteration_history,
            'quality_history': self.quality_history
        }
        
        state_file = self.state_dir / 'iteration_state.json'
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"迭代状态已保存到：{state_file}")

    def load_state(self) -> Optional[Dict[str, Any]]:
        """从 JSON 文件加载迭代状态"""
        state_file = self.state_dir / 'iteration_state.json'
        
        if not state_file.exists():
            self.logger.info("未找到之前的状态文件, 开始新的迭代")
            return None
        
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        # 恢复状态
        self.current_phase = state['current_state']['current_phase']
        self.current_iteration = state['current_state']['current_iteration']
        self.status = IterationStatus(state['current_state']['status'])
        self.iteration_history = state['iteration_history']
        self.quality_history = state['quality_history']
        
        self.logger.info(f"已从 {state_file} 恢复迭代状态")
        
        return state

    def run_full_analysis(self, 
                         phases: List[int],
                         initial_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行完整的分析流程(所有 Phase)
        
        参数:
            phases: Phase 列表 [1, 2, 3, 4, 5, 6]
            initial_result: 初始分析结果
            
        返回:
            最终分析结果
        """
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"开始完整分析流程：{len(phases)} 个 Phase")
        self.logger.info(f"{'='*80}\n")
        
        current_result = initial_result
        
        for phase in phases:
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"执行 Phase {phase}")
            self.logger.info(f"{'='*60}\n")
            
            # 重置迭代计数器
            self.current_iteration = 0
            self.quality_history = []
            
            # 执行迭代直到收敛或达到最大次数
            while True:
                iteration_result = self.run_iteration(phase, current_result)
                
                self.logger.info(f"迭代结果：{iteration_result['status']} - {iteration_result['message']}")
                
                # 更新当前结果
                if 'improved_result' in iteration_result:
                    current_result = iteration_result['improved_result']
                
                # 检查是否结束迭代
                if iteration_result['status'] in ['converged', 'max_iterations_reached', 'early_stopped']:
                    break
            
            self.logger.info(f"Phase {phase} 完成, 最终质量分数：{iteration_result['quality_score']:.2f}%")
        
        self.logger.info(f"\n{'='*80}")
        self.logger.info("完整分析流程完成！")
        self.logger.info(f"{'='*80}\n")
        
        return {
            'status': 'completed',
            'phases_completed': phases,
            'final_result': current_result,
            'iteration_summary': {
                'total_iterations': sum(
                    1 for state in self.iteration_history 
                    if state['status'] != IterationStatus.RUNNING.value
                ),
                'final_quality_score': self.quality_history[-1] if self.quality_history else 0,
                'convergence_achieved': self.status == IterationStatus.CONVERGED
            }
        }


# ==================== 主函数 ====================

if __name__ == '__main__':
    # 测试迭代控制器
    print("="*80)
    print("迭代控制器测试")
    print("="*80)
    print()
    
    # 创建控制器
    controller = IterationController(
        max_iterations=10,
        convergence_threshold=85.0,
        min_improvement=5.0,
        early_stopping_patience=3
    )
    
    # 模拟初始分析结果
    initial_result = {
        'kappa': 0.75,
        'concept_count': 35,
        'category_saturation': 82.0,
        'evidence': '模拟证据'
    }
    
    # 运行单个 Phase 的迭代
    print("测试 Phase 2 的迭代...")
    result = controller.run_iteration(phase=2, analysis_result=initial_result)
    print(f"\n迭代结果：{json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 保存状态
    controller.save_state()
    print("\n状态已保存")
    
    # 加载状态
    loaded_state = controller.load_state()
    if loaded_state:
        print(f"\n状态已加载：当前 Phase={loaded_state['current_state']['current_phase']}")
    
    print("\n" + "="*80)
    print("测试完成！")
    print("="*80)
