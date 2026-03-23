#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主题分析专家 - 质量评估工具
Quality Assessor for Thematic Analysis

功能:
- 评估主题分析质量
- 信度检验（编码一致性）
- 效度检验（构念效度、内部效度）
- 生成质量报告

作者: Thematic Analysis Expert v5.0.0
创建时间: 2026-03-15
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import math

# 跨平台兼容
def get_output_dir() -> Path:
    """获取输出目录"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@dataclass
class QualityScore:
    """质量评分"""
    dimension: str
    score: float
    max_score: float = 1.0
    description: str = ""
    evidence: List[str] = None
    
    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []
    
    @property
    def percentage(self) -> float:
        return (self.score / self.max_score) * 100 if self.max_score > 0 else 0
    
    def to_dict(self) -> Dict:
        return {
            "dimension": self.dimension,
            "score": self.score,
            "max_score": self.max_score,
            "percentage": f"{self.percentage:.1f}%",
            "description": self.description,
            "evidence": self.evidence
        }


@dataclass
class QualityReport:
    """质量报告"""
    reliability: QualityScore = None
    validity: QualityScore = None
    transparency: QualityScore = None
    coherence: QualityScore = None
    overall_score: float = 0.0
    recommendations: List[str] = None
    
    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []
    
    def to_dict(self) -> Dict:
        return {
            "reliability": self.reliability.to_dict() if self.reliability else None,
            "validity": self.validity.to_dict() if self.validity else None,
            "transparency": self.transparency.to_dict() if self.transparency else None,
            "coherence": self.coherence.to_dict() if self.coherence else None,
            "overall_score": self.overall_score,
            "recommendations": self.recommendations
        }


class QualityAssessor:
    """质量评估器"""
    
    def __init__(self):
        self.scores: Dict[str, QualityScore] = {}
        self.evidence: Dict[str, List[str]] = defaultdict(list)
        
    def add_evidence(self, dimension: str, evidence: str):
        """添加证据"""
        self.evidence[dimension].append(evidence)
    
    def assess_reliability(
        self,
        coding_data: Dict = None,
        inter_coder_agreement: float = None,
        saturation_level: float = None
    ) -> QualityScore:
        """
        评估信度
        
        Args:
            coding_data: 编码数据
            inter_coder_agreement: 编码者间一致性（如果有多个编码者）
            saturation_level: 饱和度水平
        
        Returns:
            信度评分
        """
        score = 0.0
        evidence = []
        
        # 编码一致性
        if inter_coder_agreement is not None:
            if inter_coder_agreement >= 0.80:
                score += 0.4
                evidence.append(f"编码者间一致性达到{inter_coder_agreement:.1%}（≥80%标准）")
            elif inter_coder_agreement >= 0.70:
                score += 0.3
                evidence.append(f"编码者间一致性达到{inter_coder_agreement:.1%}（接近标准）")
            else:
                evidence.append(f"编码者间一致性仅{inter_coder_agreement:.1%}（低于标准）")
        else:
            # 单一编码者情况
            score += 0.2
            evidence.append("单一编码者分析，建议进行同侪审查")
        
        # 饱和度
        if saturation_level is not None:
            if saturation_level >= 0.80:
                score += 0.4
                evidence.append(f"主题饱和度达到{saturation_level:.1%}（≥80%标准）")
            elif saturation_level >= 0.70:
                score += 0.3
                evidence.append(f"主题饱和度达到{saturation_level:.1%}（接近标准）")
            else:
                evidence.append(f"主题饱和度仅{saturation_level:.1%}（低于标准）")
        else:
            score += 0.2
            evidence.append("未提供饱和度数据")
        
        # 编码过程的系统性
        if coding_data:
            if coding_data.get("systematic_process"):
                score += 0.2
                evidence.append("编码过程系统化执行")
        
        quality_score = QualityScore(
            dimension="信度",
            score=score,
            max_score=1.0,
            description="评估分析结果的一致性和可重复性",
            evidence=evidence
        )
        
        self.scores["reliability"] = quality_score
        return quality_score
    
    def assess_validity(
        self,
        themes: List[Dict] = None,
        triangulation: bool = False,
        member_checking: bool = False,
        negative_case_analysis: bool = False
    ) -> QualityScore:
        """
        评估效度
        
        Args:
            themes: 主题列表
            triangulation: 是否进行三角验证
            member_checking: 是否进行成员检验
            negative_case_analysis: 是否分析负面案例
        
        Returns:
            效度评分
        """
        score = 0.0
        evidence = []
        
        # 构念效度
        if themes:
            # 检查主题定义的清晰度
            well_defined = sum(1 for t in themes if t.get("definition"))
            if well_defined == len(themes):
                score += 0.25
                evidence.append("所有主题都有明确定义")
            elif well_defined / len(themes) >= 0.8:
                score += 0.2
                evidence.append(f"{well_defined}/{len(themes)}个主题有明确定义")
            
            # 检查主题边界
            distinct_themes = sum(1 for t in themes if t.get("distinct"))
            if distinct_themes > 0:
                score += 0.15
                evidence.append(f"{distinct_themes}个主题边界清晰")
        
        # 内部效度
        if triangulation:
            score += 0.2
            evidence.append("进行了三角验证")
        
        if member_checking:
            score += 0.15
            evidence.append("进行了成员检验")
        
        if negative_case_analysis:
            score += 0.1
            evidence.append("分析了负面案例")
        
        # 外部效度（简化评估）
        if themes and len(themes) >= 3:
            score += 0.15
            evidence.append("主题数量适当，有利于理论迁移")
        
        quality_score = QualityScore(
            dimension="效度",
            score=score,
            max_score=1.0,
            description="评估分析结果的准确性和可信度",
            evidence=evidence
        )
        
        self.scores["validity"] = quality_score
        return quality_score
    
    def assess_transparency(
        self,
        process_documented: bool = False,
        decisions_explained: bool = False,
        limitations_acknowledged: bool = False,
        positionality_statement: bool = False
    ) -> QualityScore:
        """
        评估透明度
        
        Args:
            process_documented: 过程是否有文档记录
            decisions_explained: 决策是否有解释
            limitations_acknowledged: 是否承认局限性
            positionality_statement: 是否有位置性声明
        
        Returns:
            透明度评分
        """
        score = 0.0
        evidence = []
        
        if process_documented:
            score += 0.3
            evidence.append("分析过程有详细文档记录")
        else:
            evidence.append("缺少分析过程文档")
        
        if decisions_explained:
            score += 0.25
            evidence.append("关键决策有解释说明")
        else:
            evidence.append("关键决策缺乏解释")
        
        if limitations_acknowledged:
            score += 0.25
            evidence.append("承认了研究局限性")
        else:
            evidence.append("未明确说明局限性")
        
        if positionality_statement:
            score += 0.2
            evidence.append("提供了研究者位置性声明")
        else:
            evidence.append("缺少研究者位置性声明")
        
        quality_score = QualityScore(
            dimension="透明度",
            score=score,
            max_score=1.0,
            description="评估分析过程的开放性和可审查性",
            evidence=evidence
        )
        
        self.scores["transparency"] = quality_score
        return quality_score
    
    def assess_coherence(
        self,
        themes: List[Dict] = None,
        supporting_quotes: Dict = None,
        analytical_depth: str = "medium"
    ) -> QualityScore:
        """
        评估连贯性
        
        Args:
            themes: 主题列表
            supporting_quotes: 支持性引文
            analytical_depth: 分析深度 (low/medium/high)
        
        Returns:
            连贯性评分
        """
        score = 0.0
        evidence = []
        
        if themes:
            # 主题间关系
            if len(themes) >= 2:
                score += 0.2
                evidence.append("存在多个相关主题")
            
            # 引文支持
            if supporting_quotes:
                avg_quotes = sum(len(q) for q in supporting_quotes.values()) / len(supporting_quotes)
                if avg_quotes >= 3:
                    score += 0.3
                    evidence.append(f"每个主题平均有{avg_quotes:.1f}个支持性引文")
                elif avg_quotes >= 2:
                    score += 0.2
                    evidence.append(f"每个主题平均有{avg_quotes:.1f}个支持性引文")
                else:
                    evidence.append("支持性引文不足")
            
            # 分析深度
            depth_scores = {"low": 0.2, "medium": 0.3, "high": 0.4}
            score += depth_scores.get(analytical_depth, 0.2)
            evidence.append(f"分析深度: {analytical_depth}")
            
            # 论证逻辑
            # 简化：检查主题是否有分析性描述
            analytical_themes = sum(
                1 for t in themes 
                if t.get("analysis") or t.get("interpretation")
            )
            if analytical_themes > 0:
                score += 0.1
                evidence.append(f"{analytical_themes}个主题有深度分析")
        
        quality_score = QualityScore(
            dimension="连贯性",
            score=score,
            max_score=1.0,
            description="评估分析的逻辑性和深度",
            evidence=evidence
        )
        
        self.scores["coherence"] = quality_score
        return quality_score
    
    def generate_report(self) -> QualityReport:
        """生成质量报告"""
        report = QualityReport()
        
        # 计算各维度评分
        if "reliability" in self.scores:
            report.reliability = self.scores["reliability"]
        if "validity" in self.scores:
            report.validity = self.scores["validity"]
        if "transparency" in self.scores:
            report.transparency = self.scores["transparency"]
        if "coherence" in self.scores:
            report.coherence = self.scores["coherence"]
        
        # 计算总分
        scores = [s.score for s in self.scores.values() if s]
        if scores:
            report.overall_score = sum(scores) / len(scores)
        
        # 生成建议
        report.recommendations = self._generate_recommendations()
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        for dimension, score in self.scores.items():
            if score.score < 0.6:
                if dimension == "reliability":
                    recommendations.append("建议: 进行编码者间一致性检验或同侪审查")
                elif dimension == "validity":
                    recommendations.append("建议: 进行三角验证、成员检验或负面案例分析")
                elif dimension == "transparency":
                    recommendations.append("建议: 完善分析过程文档、解释关键决策、声明研究者位置")
                elif dimension == "coherence":
                    recommendations.append("建议: 加强主题间关系的分析、增加支持性引文、深化分析阐释")
        
        if not recommendations:
            recommendations.append("分析质量良好，继续保持当前标准")
        
        return recommendations
    
    def get_checklist(self) -> List[Dict]:
        """获取质量检查清单"""
        checklist = [
            {"item": "数据充分熟悉", "category": "过程", "required": True},
            {"item": "编码系统完整", "category": "过程", "required": True},
            {"item": "主题边界清晰", "category": "结果", "required": True},
            {"item": "引文支持充分", "category": "结果", "required": True},
            {"item": "分析论证有力", "category": "结果", "required": True},
            {"item": "过程记录透明", "category": "透明度", "required": True},
            {"item": "局限性已承认", "category": "透明度", "required": True},
            {"item": "负面案例关注", "category": "效度", "required": False},
            {"item": "成员检验完成", "category": "效度", "required": False},
            {"item": "三角验证实施", "category": "效度", "required": False},
        ]
        return checklist
    
    def generate_text_report(self) -> str:
        """生成文本报告"""
        report = self.generate_report()
        
        text = """# 主题分析质量评估报告

## 总体评分: {overall:.1%}

## 维度评分

### 1. 信度
**评分**: {rel_score:.1%}

**证据**:
{rel_evidence}

### 2. 效度
**评分**: {val_score:.1%}

**证据**:
{val_evidence}

### 3. 透明度
**评分**: {trans_score:.1%}

**证据**:
{trans_evidence}

### 4. 连贯性
**评分**: {coh_score:.1%}

**证据**:
{coh_evidence}

## 改进建议

{recommendations}

## 质量检查清单

{checklist}
""".format(
            overall=report.overall_score,
            rel_score=report.reliability.percentage if report.reliability else 0,
            rel_evidence="\n".join([f"- {e}" for e in report.reliability.evidence]) if report.reliability else "无",
            val_score=report.validity.percentage if report.validity else 0,
            val_evidence="\n".join([f"- {e}" for e in report.validity.evidence]) if report.validity else "无",
            trans_score=report.transparency.percentage if report.transparency else 0,
            trans_evidence="\n".join([f"- {e}" for e in report.transparency.evidence]) if report.transparency else "无",
            coh_score=report.coherence.percentage if report.coherence else 0,
            coh_evidence="\n".join([f"- {e}" for e in report.coherence.evidence]) if report.coherence else "无",
            recommendations="\n".join([f"- {r}" for r in report.recommendations]),
            checklist="\n".join([
                f"- [{'x' if item['required'] else ' '}] {item['item']} ({item['category']})"
                for item in self.get_checklist()
            ])
        )
        
        return text


def assess_quality(analysis_data: Dict) -> Dict:
    """
    评估分析质量 - 主入口函数
    
    Args:
        analysis_data: 分析数据，包含主题、编码、过程等信息
    
    Returns:
        质量评估结果
    """
    assessor = QualityAssessor()
    
    # 评估信度
    assessor.assess_reliability(
        inter_coder_agreement=analysis_data.get("inter_coder_agreement"),
        saturation_level=analysis_data.get("saturation_level"),
        coding_data=analysis_data.get("coding_data")
    )
    
    # 评估效度
    assessor.assess_validity(
        themes=analysis_data.get("themes"),
        triangulation=analysis_data.get("triangulation", False),
        member_checking=analysis_data.get("member_checking", False),
        negative_case_analysis=analysis_data.get("negative_case_analysis", False)
    )
    
    # 评估透明度
    assessor.assess_transparency(
        process_documented=analysis_data.get("process_documented", False),
        decisions_explained=analysis_data.get("decisions_explained", False),
        limitations_acknowledged=analysis_data.get("limitations_acknowledged", False),
        positionality_statement=analysis_data.get("positionality_statement", False)
    )
    
    # 评估连贯性
    assessor.assess_coherence(
        themes=analysis_data.get("themes"),
        supporting_quotes=analysis_data.get("supporting_quotes"),
        analytical_depth=analysis_data.get("analytical_depth", "medium")
    )
    
    return assessor.generate_report().to_dict()


# 示例使用
if __name__ == "__main__":
    # 模拟分析数据
    sample_data = {
        "themes": [
            {"name": "主题1", "definition": "定义1", "distinct": True, "analysis": "分析内容"},
            {"name": "主题2", "definition": "定义2", "distinct": True},
            {"name": "主题3", "definition": "定义3", "distinct": True, "analysis": "分析内容"},
        ],
        "inter_coder_agreement": 0.85,
        "saturation_level": 0.82,
        "triangulation": True,
        "member_checking": False,
        "negative_case_analysis": True,
        "process_documented": True,
        "decisions_explained": True,
        "limitations_acknowledged": True,
        "positionality_statement": False,
        "supporting_quotes": {
            "主题1": ["引文1", "引文2", "引文3"],
            "主题2": ["引文4", "引文5"],
            "主题3": ["引文6", "引文7", "引文8"],
        },
        "analytical_depth": "high"
    }
    
    # 创建评估器
    assessor = QualityAssessor()
    
    # 执行评估
    result = assess_quality(sample_data)
    
    print("质量评估结果:")
    print(f"总体评分: {result['overall_score']:.1%}")
    print("\n各维度评分:")
    for dim in ['reliability', 'validity', 'transparency', 'coherence']:
        if result[dim]:
            print(f"  {result[dim]['dimension']}: {result[dim]['percentage']}")
    
    print("\n建议:")
    for rec in result['recommendations']:
        print(f"  - {rec}")
    
    print("\n" + "="*50)
    print(assessor.generate_text_report())
