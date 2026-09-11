#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝海战略分析工具
Blue Ocean Strategy Analyzer

基于W. Chan Kim和Renée Mauborgne的蓝海战略方法论
提供红海诊断、六条路径探索、四步动作框架分析等功能

跨平台兼容: Windows/Linux/macOS
"""

import os
import json
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class CompetitionFactor:
    """竞争要素"""
    name: str
    industry_level: float  # 行业平均水平 (1-10)
    company_level: float   # 企业当前水平 (1-10)
    new_level: Optional[float] = None  # 蓝海战略水平
    action_type: Optional[str] = None  # eliminate/reduce/raise/create
    action_reason: Optional[str] = None


@dataclass
class SixPathsDiscovery:
    """六条路径发现"""
    path_name: str
    key_insights: List[str]
    opportunities: List[str]
    priority: int  # 1-5 优先级


@dataclass
class FourActionsResult:
    """四步动作结果"""
    eliminate: List[Dict]  # 剔除要素
    reduce: List[Dict]     # 减少要素
    raise: List[Dict]      # 增加要素
    create: List[Dict]     # 创造要素


class BlueOceanAnalyzer:
    """蓝海战略分析器"""
    
    def __init__(self, project_path: Optional[str] = None):
        """
        初始化分析器
        
        Args:
            project_path: 项目路径（可选，默认使用临时目录）
        """
        if project_path:
            self.project_path = Path(project_path)
        else:
            self.project_path = Path(tempfile.gettempdir()) / "blue_ocean_analysis"
        
        # 创建目录结构（跨平台兼容）
        self._init_directories()
        
        # 初始化数据
        self.competition_factors: List[CompetitionFactor] = []
        self.six_paths_discoveries: List[SixPathsDiscovery] = []
        self.four_actions_result: Optional[FourActionsResult] = None
    
    def _init_directories(self) -> None:
        """创建项目目录结构"""
        subdirs = ['data', 'results', 'visualizations', 'logs', '.tasks']
        for subdir in subdirs:
            dir_path = self.project_path / subdir
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def add_competition_factor(self, factor: CompetitionFactor) -> None:
        """添加竞争要素"""
        self.competition_factors.append(factor)
    
    def load_industry_data(self, data_path: str) -> Dict:
        """
        加载行业数据
        
        Args:
            data_path: 数据文件路径
            
        Returns:
            行业数据字典
        """
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 加载竞争要素
        if 'competition_factors' in data:
            for factor_data in data['competition_factors']:
                factor = CompetitionFactor(**factor_data)
                self.add_competition_factor(factor)
        
        return data
    
    def analyze_red_ocean(self) -> Dict:
        """
        红海诊断分析
        
        Returns:
            红海诊断结果
        """
        if not self.competition_factors:
            return {"status": "error", "message": "请先加载竞争要素数据"}
        
        # 计算差异度
        differences = []
        for factor in self.competition_factors:
            diff = factor.company_level - factor.industry_level
            differences.append({
                "factor": factor.name,
                "difference": diff,
                "position": "高于行业" if diff > 0 else "低于行业" if diff < 0 else "持平"
            })
        
        # 识别竞争焦点
        high_factors = [f.name for f in self.competition_factors if f.company_level > f.industry_level]
        low_factors = [f.name for f in self.competition_factors if f.company_level < f.industry_level]
        
        # 计算竞争强度指数
        avg_diff = sum(abs(d["difference"]) for d in differences) / len(differences)
        
        return {
            "status": "success",
            "analysis_time": datetime.now().isoformat(),
            "competition_factors_count": len(self.competition_factors),
            "differences": differences,
            "competitive_advantages": high_factors,
            "competitive_disadvantages": low_factors,
            "competition_intensity_index": round(avg_diff, 2),
            "interpretation": self._interpret_red_ocean(differences, avg_diff)
        }
    
    def _interpret_red_ocean(self, differences: List[Dict], avg_diff: float) -> str:
        """解释红海诊断结果"""
        if avg_diff < 1:
            return "企业与行业基准高度一致，处于红海竞争中"
        elif avg_diff < 2:
            return "企业与行业基准有一定差异，但差异化不明显"
        else:
            return "企业与行业基准存在显著差异，具备差异化基础"
    
    def explore_six_paths(self) -> List[Dict]:
        """
        六条路径探索
        
        Returns:
            六条路径分析结果
        """
        paths = [
            {
                "path_id": 1,
                "path_name": "跨越替代性行业",
                "guiding_question": "客户在选择你的产品时，还会考虑哪些替代品？",
                "analysis_steps": [
                    "识别替代性行业",
                    "分析替代品价值主张",
                    "识别融合机会"
                ]
            },
            {
                "path_id": 2,
                "path_name": "跨越战略集团",
                "guiding_question": "行业内不同战略集团的客户为什么选择这家而非那家？",
                "analysis_steps": [
                    "识别战略集团",
                    "分析各集团差异化要素",
                    "探索跨越机会"
                ]
            },
            {
                "path_id": 3,
                "path_name": "跨越买方链",
                "guiding_question": "谁是购买者？谁是使用者？谁是影响者？",
                "analysis_steps": [
                    "梳理买方链各角色",
                    "分析各角色价值诉求",
                    "重新定义目标买方"
                ]
            },
            {
                "path_id": 4,
                "path_name": "跨越互补性产品与服务",
                "guiding_question": "客户在使用你的产品前后，还需要什么？",
                "analysis_steps": [
                    "识别使用场景全流程",
                    "分析互补产品服务",
                    "设计整体解决方案"
                ]
            },
            {
                "path_id": 5,
                "path_name": "跨越功能-情感导向",
                "guiding_question": "行业是功能导向还是情感导向？",
                "analysis_steps": [
                    "评估行业当前导向",
                    "分析转换可能性",
                    "设计转换策略"
                ]
            },
            {
                "path_id": 6,
                "path_name": "跨越时间趋势",
                "guiding_question": "行业正在发生什么趋势变化？",
                "analysis_steps": [
                    "识别行业趋势",
                    "分析趋势影响",
                    "设计前瞻战略"
                ]
            }
        ]
        
        return paths
    
    def apply_four_actions_framework(
        self,
        eliminate_factors: List[str],
        reduce_factors: List[str],
        raise_factors: List[str],
        create_factors: List[str]
    ) -> FourActionsResult:
        """
        应用四步动作框架
        
        Args:
            eliminate_factors: 剔除要素列表
            reduce_factors: 减少要素列表
            raise_factors: 增加要素列表
            create_factors: 创造要素列表
            
        Returns:
            四步动作结果
        """
        result = FourActionsResult(
            eliminate=[{"factor": f, "action": "eliminate"} for f in eliminate_factors],
            reduce=[{"factor": f, "action": "reduce"} for f in reduce_factors],
            raise=[{"factor": f, "action": "raise"} for f in raise_factors],
            create=[{"factor": f, "action": "create"} for f in create_factors]
        )
        
        self.four_actions_result = result
        
        # 更新竞争要素的新水平
        for factor in self.competition_factors:
            if factor.name in eliminate_factors:
                factor.action_type = "eliminate"
                factor.new_level = 0
            elif factor.name in reduce_factors:
                factor.action_type = "reduce"
                factor.new_level = factor.company_level * 0.5
            elif factor.name in raise_factors:
                factor.action_type = "raise"
                factor.new_level = min(factor.company_level * 1.5, 10)
        
        # 添加创造的新要素
        for new_factor in create_factors:
            new_comp = CompetitionFactor(
                name=new_factor,
                industry_level=0,
                company_level=0,
                new_level=8,
                action_type="create"
            )
            self.competition_factors.append(new_comp)
        
        return result
    
    def generate_strategy_canvas_data(self) -> Dict:
        """
        生成战略布局图数据
        
        Returns:
            战略布局图数据
        """
        factors_data = []
        for factor in self.competition_factors:
            factor_dict = {
                "name": factor.name,
                "industry_level": factor.industry_level,
                "company_level": factor.company_level,
                "action": factor.action_type,
                "action_reason": factor.action_reason
            }
            if factor.new_level is not None:
                factor_dict["new_level"] = factor.new_level
            factors_data.append(factor_dict)
        
        return {
            "status": "success",
            "factors": factors_data,
            "chart_type": "strategy_canvas",
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        生成蓝海战略分析报告
        
        Args:
            output_path: 输出路径（可选）
            
        Returns:
            报告内容或保存路径
        """
        report_lines = [
            "# 蓝海战略分析报告",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 一、红海诊断",
            ""
        ]
        
        # 红海诊断
        red_ocean_result = self.analyze_red_ocean()
        if red_ocean_result["status"] == "success":
            report_lines.append("### 1.1 竞争要素分析")
            report_lines.append("")
            report_lines.append("| 要素 | 行业水平 | 企业水平 | 差异 |")
            report_lines.append("|------|---------|---------|------|")
            for diff in red_ocean_result["differences"]:
                factor = next(f for f in self.competition_factors if f.name == diff["factor"])
                report_lines.append(f"| {factor.name} | {factor.industry_level} | {factor.company_level} | {diff['difference']:+.1f} |")
            report_lines.append("")
            report_lines.append(f"**竞争强度指数**: {red_ocean_result['competition_intensity_index']}")
            report_lines.append("")
            report_lines.append(f"**诊断结论**: {red_ocean_result['interpretation']}")
        
        # 四步动作框架
        if self.four_actions_result:
            report_lines.extend([
                "",
                "---",
                "",
                "## 二、四步动作框架",
                "",
                "### 2.1 剔除要素",
                ""
            ])
            for item in self.four_actions_result.eliminate:
                report_lines.append(f"- {item['factor']}")
            
            report_lines.extend(["", "### 2.2 减少要素", ""])
            for item in self.four_actions_result.reduce:
                report_lines.append(f"- {item['factor']}")
            
            report_lines.extend(["", "### 2.3 增加要素", ""])
            for item in self.four_actions_result.raise_action:
                report_lines.append(f"- {item['factor']}")
            
            report_lines.extend(["", "### 2.4 创造要素", ""])
            for item in self.four_actions_result.create:
                report_lines.append(f"- {item['factor']}")
        
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
            filename = f"blue_ocean_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        save_path = self.project_path / 'results' / filename
        
        data = {
            "competition_factors": [asdict(f) for f in self.competition_factors],
            "six_paths_discoveries": [asdict(d) for d in self.six_paths_discoveries],
            "four_actions_result": asdict(self.four_actions_result) if self.four_actions_result else None
        }
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return str(save_path)


def main():
    """示例用法"""
    # 创建分析器
    analyzer = BlueOceanAnalyzer()
    
    # 添加示例竞争要素
    sample_factors = [
        CompetitionFactor("价格", 5.0, 7.0),
        CompetitionFactor("质量", 7.0, 6.0),
        CompetitionFactor("服务", 6.0, 4.0),
        CompetitionFactor("品牌", 8.0, 5.0),
        CompetitionFactor("便利性", 5.0, 6.0),
    ]
    
    for factor in sample_factors:
        analyzer.add_competition_factor(factor)
    
    # 执行红海诊断
    result = analyzer.analyze_red_ocean()
    print("红海诊断结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 应用四步动作框架
    four_actions = analyzer.apply_four_actions_framework(
        eliminate_factors=["品牌"],
        reduce_factors=["服务"],
        raise_factors=["便利性"],
        create_factors=["个性化体验"]
    )
    print("\n四步动作框架结果:")
    print(json.dumps(asdict(four_actions), ensure_ascii=False, indent=2))
    
    # 保存分析
    save_path = analyzer.save_analysis()
    print(f"\n分析数据已保存到: {save_path}")


if __name__ == "__main__":
    main()
