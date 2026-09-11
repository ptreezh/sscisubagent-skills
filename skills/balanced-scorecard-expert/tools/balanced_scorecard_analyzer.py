#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平衡计分卡分析工具
Balanced Scorecard Analyzer

基于Robert S. Kaplan和David P. Norton的平衡计分卡方法论
提供战略地图构建、指标体系设计、因果链分析等功能

跨平台兼容: Windows/Linux/macOS
"""

import os
import json
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum


class Dimension(Enum):
    """平衡计分卡四维度"""
    FINANCIAL = "financial"
    CUSTOMER = "customer"
    INTERNAL_PROCESS = "internal_process"
    LEARNING_GROWTH = "learning_growth"


class IndicatorType(Enum):
    """指标类型"""
    LEADING = "leading"  # 领先指标
    LAGGING = "lagging"  # 滞后指标


@dataclass
class StrategicObjective:
    """战略目标"""
    id: str
    name: str
    dimension: str
    description: str
    causes: List[str]  # 因果来源（上层目标ID）
    effects: List[str]  # 因果影响（下层目标ID）
    indicators: List[str]  # 关联指标ID
    strategic_theme: Optional[str] = None


@dataclass
class Indicator:
    """绩效指标"""
    id: str
    name: str
    dimension: str
    objective_id: str  # 关联的战略目标ID
    indicator_type: str  # leading/lagging
    definition: str
    formula: str
    data_source: str
    update_frequency: str
    target_value: float
    actual_value: Optional[float] = None
    unit: str = ""
    owner: str = ""


@dataclass
class CausalLink:
    """因果关系"""
    from_objective: str  # 因
    to_objective: str    # 果
    hypothesis: str      # 假设
    validation_method: str  # 验证方法
    validated: bool = False


class BalancedScorecardAnalyzer:
    """平衡计分卡分析器"""
    
    def __init__(self, project_path: Optional[str] = None):
        """
        初始化分析器
        
        Args:
            project_path: 项目路径（可选，默认使用临时目录）
        """
        if project_path:
            self.project_path = Path(project_path)
        else:
            self.project_path = Path(tempfile.gettempdir()) / "balanced_scorecard_analysis"
        
        # 创建目录结构（跨平台兼容）
        self._init_directories()
        
        # 初始化数据
        self.objectives: List[StrategicObjective] = []
        self.indicators: List[Indicator] = []
        self.causal_links: List[CausalLink] = []
        self.strategic_themes: List[str] = []
    
    def _init_directories(self) -> None:
        """创建项目目录结构"""
        subdirs = ['data', 'results', 'visualizations', 'logs', '.tasks']
        for subdir in subdirs:
            dir_path = self.project_path / subdir
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def add_objective(self, objective: StrategicObjective) -> None:
        """添加战略目标"""
        self.objectives.append(objective)
    
    def add_indicator(self, indicator: Indicator) -> None:
        """添加绩效指标"""
        self.indicators.append(indicator)
    
    def add_causal_link(self, link: CausalLink) -> None:
        """添加因果关系"""
        self.causal_links.append(link)
    
    def load_strategy_data(self, data_path: str) -> Dict:
        """
        加载战略数据
        
        Args:
            data_path: 数据文件路径
            
        Returns:
            战略数据字典
        """
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 加载战略目标
        if 'objectives' in data:
            for obj_data in data['objectives']:
                objective = StrategicObjective(**obj_data)
                self.add_objective(objective)
        
        # 加载指标
        if 'indicators' in data:
            for ind_data in data['indicators']:
                indicator = Indicator(**ind_data)
                self.add_indicator(indicator)
        
        # 加载因果关系
        if 'causal_links' in data:
            for link_data in data['causal_links']:
                link = CausalLink(**link_data)
                self.add_causal_link(link)
        
        return data
    
    def build_strategy_map(self) -> Dict:
        """
        构建战略地图
        
        Returns:
            战略地图数据结构
        """
        # 按维度组织目标
        dimensions = {
            "financial": [],
            "customer": [],
            "internal_process": [],
            "learning_growth": []
        }
        
        for obj in self.objectives:
            if obj.dimension in dimensions:
                dimensions[obj.dimension].append({
                    "id": obj.id,
                    "name": obj.name,
                    "description": obj.description,
                    "causes": obj.causes,
                    "effects": obj.effects,
                    "strategic_theme": obj.strategic_theme
                })
        
        # 构建因果链
        causal_chains = self._build_causal_chains()
        
        return {
            "status": "success",
            "generated_at": datetime.now().isoformat(),
            "dimensions": dimensions,
            "causal_chains": causal_chains,
            "strategic_themes": self.strategic_themes
        }
    
    def _build_causal_chains(self) -> List[Dict]:
        """构建因果链条"""
        chains = []
        
        for link in self.causal_links:
            from_obj = next((o for o in self.objectives if o.id == link.from_objective), None)
            to_obj = next((o for o in self.objectives if o.id == link.to_objective), None)
            
            if from_obj and to_obj:
                chains.append({
                    "from": {
                        "id": from_obj.id,
                        "name": from_obj.name,
                        "dimension": from_obj.dimension
                    },
                    "to": {
                        "id": to_obj.id,
                        "name": to_obj.name,
                        "dimension": to_obj.dimension
                    },
                    "hypothesis": link.hypothesis,
                    "validated": link.validated
                })
        
        return chains
    
    def analyze_indicator_balance(self) -> Dict:
        """
        分析指标平衡性
        
        Returns:
            指标平衡性分析结果
        """
        # 按维度统计
        dimension_counts = {
            "financial": 0,
            "customer": 0,
            "internal_process": 0,
            "learning_growth": 0
        }
        
        # 按类型统计
        type_counts = {
            "leading": 0,
            "lagging": 0
        }
        
        for indicator in self.indicators:
            if indicator.dimension in dimension_counts:
                dimension_counts[indicator.dimension] += 1
            if indicator.indicator_type in type_counts:
                type_counts[indicator.indicator_type] += 1
        
        total = len(self.indicators)
        
        # 平衡性评估
        balance_assessment = {
            "dimension_balance": self._assess_dimension_balance(dimension_counts, total),
            "type_balance": self._assess_type_balance(type_counts, total),
            "total_indicators": total,
            "recommendation": self._generate_balance_recommendation(dimension_counts, type_counts)
        }
        
        return {
            "status": "success",
            "dimension_counts": dimension_counts,
            "type_counts": type_counts,
            "balance_assessment": balance_assessment
        }
    
    def _assess_dimension_balance(self, counts: Dict, total: int) -> Dict:
        """评估维度平衡性"""
        if total == 0:
            return {"score": 0, "status": "无指标"}
        
        # 理想比例：每个维度25%
        ideal_ratio = 0.25
        max_deviation = 0
        
        for count in counts.values():
            actual_ratio = count / total if total > 0 else 0
            deviation = abs(actual_ratio - ideal_ratio)
            max_deviation = max(max_deviation, deviation)
        
        # 偏差越小，平衡性越好
        score = max(0, 100 - max_deviation * 200)
        
        return {
            "score": round(score, 1),
            "status": "良好" if score >= 70 else "需改进" if score >= 50 else "不平衡"
        }
    
    def _assess_type_balance(self, counts: Dict, total: int) -> Dict:
        """评估类型平衡性"""
        if total == 0:
            return {"score": 0, "status": "无指标"}
        
        # 理想比例：领先60%，滞后40%
        leading_ratio = counts["leading"] / total if total > 0 else 0
        ideal_leading = 0.6
        
        deviation = abs(leading_ratio - ideal_leading)
        score = max(0, 100 - deviation * 150)
        
        return {
            "score": round(score, 1),
            "leading_ratio": round(leading_ratio * 100, 1),
            "status": "良好" if score >= 70 else "需调整"
        }
    
    def _generate_balance_recommendation(self, dim_counts: Dict, type_counts: Dict) -> str:
        """生成平衡性改进建议"""
        recommendations = []
        
        total = sum(dim_counts.values())
        if total == 0:
            return "请先添加指标"
        
        # 维度建议
        for dim, count in dim_counts.items():
            ratio = count / total
            if ratio < 0.15:
                recommendations.append(f"建议增加{dim}维度的指标")
            elif ratio > 0.35:
                recommendations.append(f"建议精简{dim}维度的指标")
        
        # 类型建议
        leading_ratio = type_counts["leading"] / total
        if leading_ratio < 0.5:
            recommendations.append("建议增加更多领先指标以增强预测能力")
        elif leading_ratio > 0.75:
            recommendations.append("建议增加滞后指标以验证结果")
        
        return "；".join(recommendations) if recommendations else "指标体系平衡性良好"
    
    def validate_causal_chains(self) -> Dict:
        """
        验证因果链条完整性
        
        Returns:
            因果链验证结果
        """
        issues = []
        validated_chains = []
        
        # 检查每个目标是否在因果链中
        linked_objectives = set()
        for link in self.causal_links:
            linked_objectives.add(link.from_objective)
            linked_objectives.add(link.to_objective)
        
        for obj in self.objectives:
            if obj.id not in linked_objectives:
                issues.append({
                    "type": "isolated_objective",
                    "objective": obj.name,
                    "message": f"目标'{obj.name}'未纳入因果链，可能影响战略一致性"
                })
        
        # 检查因果链是否从学习成长到财务完整
        dimensions_order = ["learning_growth", "internal_process", "customer", "financial"]
        for i in range(len(dimensions_order) - 1):
            from_dim = dimensions_order[i]
            to_dim = dimensions_order[i + 1]
            
            has_link = any(
                next((o.dimension for o in self.objectives if o.id == link.from_objective), None) == from_dim
                and next((o.dimension for o in self.objectives if o.id == link.to_objective), None) == to_dim
                for link in self.causal_links
            )
            
            if not has_link:
                issues.append({
                    "type": "missing_causal_link",
                    "from_dimension": from_dim,
                    "to_dimension": to_dim,
                    "message": f"缺少从{from_dim}到{to_dim}的因果链"
                })
        
        return {
            "status": "success",
            "total_objectives": len(self.objectives),
            "total_causal_links": len(self.causal_links),
            "linked_objectives": len(linked_objectives),
            "issues": issues,
            "validation_passed": len(issues) == 0
        }
    
    def generate_scorecard_report(self, output_path: Optional[str] = None) -> str:
        """
        生成平衡计分卡报告
        
        Args:
            output_path: 输出路径（可选）
            
        Returns:
            报告内容或保存路径
        """
        report_lines = [
            "# 平衡计分卡分析报告",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 一、战略地图概览",
            ""
        ]
        
        # 战略地图
        strategy_map = self.build_strategy_map()
        for dim_name, objectives in strategy_map["dimensions"].items():
            dim_names = {
                "financial": "财务维度",
                "customer": "客户维度",
                "internal_process": "内部流程维度",
                "learning_growth": "学习与成长维度"
            }
            report_lines.append(f"### {dim_names.get(dim_name, dim_name)}")
            report_lines.append("")
            for obj in objectives:
                report_lines.append(f"- **{obj['name']}**: {obj['description']}")
            report_lines.append("")
        
        # 指标体系
        report_lines.extend([
            "---",
            "",
            "## 二、指标体系",
            ""
        ])
        
        for dim_name in ["financial", "customer", "internal_process", "learning_growth"]:
            dim_names = {
                "financial": "财务维度",
                "customer": "客户维度",
                "internal_process": "内部流程维度",
                "learning_growth": "学习与成长维度"
            }
            dim_indicators = [i for i in self.indicators if i.dimension == dim_name]
            if dim_indicators:
                report_lines.append(f"### {dim_names.get(dim_name, dim_name)}")
                report_lines.append("")
                report_lines.append("| 指标名称 | 类型 | 目标值 | 实际值 |")
                report_lines.append("|---------|------|--------|--------|")
                for ind in dim_indicators:
                    type_name = "领先" if ind.indicator_type == "leading" else "滞后"
                    report_lines.append(f"| {ind.name} | {type_name} | {ind.target_value}{ind.unit} | {ind.actual_value or 'N/A'} |")
                report_lines.append("")
        
        # 平衡性分析
        balance = self.analyze_indicator_balance()
        report_lines.extend([
            "---",
            "",
            "## 三、平衡性分析",
            "",
            f"- **维度平衡评分**: {balance['balance_assessment']['dimension_balance']['score']}分",
            f"- **类型平衡评分**: {balance['balance_assessment']['type_balance']['score']}分",
            f"- **改进建议**: {balance['balance_assessment']['recommendation']}",
            ""
        ])
        
        report_content = "\n".join(report_lines)
        
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            return str(output_file)
        
        return report_content
    
    def save_analysis(self, filename: Optional[str] = None) -> str:
        """
        保存分析数据
        
        Args:
            filename: 文件名（可选）
            
        Returns:
            保存路径
        """
        if filename is None:
            filename = f"bsc_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        save_path = self.project_path / 'results' / filename
        
        data = {
            "objectives": [asdict(o) for o in self.objectives],
            "indicators": [asdict(i) for i in self.indicators],
            "causal_links": [asdict(l) for l in self.causal_links],
            "strategic_themes": self.strategic_themes
        }
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return str(save_path)


def main():
    """示例用法"""
    # 创建分析器
    analyzer = BalancedScorecardAnalyzer()
    
    # 添加示例战略目标
    sample_objectives = [
        StrategicObjective(
            id="F1",
            name="提高资本回报率",
            dimension="financial",
            description="将ROCE从7%提升到12%",
            causes=["C1"],
            effects=[],
            indicators=["I1"]
        ),
        StrategicObjective(
            id="C1",
            name="提高客户满意度",
            dimension="customer",
            description="目标客户满意度达到行业第一",
            causes=["P1"],
            effects=["F1"],
            indicators=["I2"]
        ),
        StrategicObjective(
            id="P1",
            name="提升运营效率",
            dimension="internal_process",
            description="运营可靠性提升到95%",
            causes=["L1"],
            effects=["C1"],
            indicators=["I3"]
        ),
        StrategicObjective(
            id="L1",
            name="提升员工能力",
            dimension="learning_growth",
            description="员工技能认证率达到90%",
            causes=[],
            effects=["P1"],
            indicators=["I4"]
        )
    ]
    
    for obj in sample_objectives:
        analyzer.add_objective(obj)
    
    # 添加示例指标
    sample_indicators = [
        Indicator("I1", "ROCE", "financial", "F1", "lagging", 
                  "资本回报率", "净利润/投入资本", "财务系统", "月度", 12.0, None, "%"),
        Indicator("I2", "客户满意度", "customer", "C1", "lagging",
                  "客户满意度评分", "调研评分", "客户调研", "季度", 90.0, None, "分"),
        Indicator("I3", "运营可靠性", "internal_process", "P1", "leading",
                  "设备正常运行时间比例", "运行时间/计划时间", "生产系统", "日", 95.0, None, "%"),
        Indicator("I4", "技能认证率", "learning_growth", "L1", "leading",
                  "持证员工比例", "持证人数/总人数", "HR系统", "月度", 90.0, None, "%")
    ]
    
    for ind in sample_indicators:
        analyzer.add_indicator(ind)
    
    # 添加因果关系
    sample_links = [
        CausalLink("L1", "P1", "员工能力提升驱动运营改善", "对比分析", True),
        CausalLink("P1", "C1", "运营效率提升改善客户体验", "相关性分析", True),
        CausalLink("C1", "F1", "客户满意带来财务回报", "回归分析", False)
    ]
    
    for link in sample_links:
        analyzer.add_causal_link(link)
    
    # 执行分析
    print("=== 战略地图构建 ===")
    strategy_map = analyzer.build_strategy_map()
    print(json.dumps(strategy_map, ensure_ascii=False, indent=2))
    
    print("\n=== 平衡性分析 ===")
    balance = analyzer.analyze_indicator_balance()
    print(json.dumps(balance, ensure_ascii=False, indent=2))
    
    print("\n=== 因果链验证 ===")
    validation = analyzer.validate_causal_chains()
    print(json.dumps(validation, ensure_ascii=False, indent=2))
    
    # 保存分析
    save_path = analyzer.save_analysis()
    print(f"\n分析数据已保存到: {save_path}")


if __name__ == "__main__":
    main()
