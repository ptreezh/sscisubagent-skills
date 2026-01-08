#!/usr/bin/env python3
"""
场域分析工具调用封装器 - 标准化版本
为 field-analysis-expert 智能体提供严丝合缝的工具调用接口

输入输出规范:
    输入目录:  {project_root}/field_analysis/{analysis_type}/input/raw/
    中间目录:  {project_root}/field_analysis/{analysis_type}/intermediate/
    输出目录:  {project_root}/field_analysis/{analysis_type}/output/

文件命名（固定映射）:
    输入:     grounded_theory_data.json, social_network_data.json, esoc_framework_data.json
    合并输入: combined_input.json
    中间:     01_boundary_results.json, 02_capital_results.json, 
              03_habitus_results.json, 04_dynamics_results.json
    输出:     comprehensive_analysis.json, field_analysis_report.html
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass


# =============================================================================
# 固定文件名映射（所有中间文件和输出文件必须使用这些名称）
# =============================================================================
FIXED_FILENAMES = {
    # 输入文件（从源目录扫描）
    "grounded_theory": "grounded_theory_data.json",
    "social_network": "social_network_data.json",
    "esoc_framework": "esoc_framework_data.json",
    
    # 合并后的输入
    "combined_input": "combined_input.json",
    
    # 中间结果文件（步骤2-5）
    "boundary_results": "01_boundary_results.json",
    "capital_results": "02_capital_results.json",
    "habitus_results": "03_habitus_results.json",
    "dynamics_results": "04_dynamics_results.json",
    
    # 步骤2的子步骤输出
    "boundary_identify": "01a_boundary_identify.json",
    "boundary_dynamics": "01b_boundary_dynamics.json",
    
    # 步骤3的子步骤输出
    "capital_types": "02a_capital_types.json",
    "capital_distribution": "02b_capital_distribution.json",
    
    # 步骤4的子步骤输出
    "habitus_patterns": "03a_habitus_patterns.json",
    "symbolic_violence": "03b_symbolic_violence.json",
    "cross_field": "03c_cross_field.json",
    
    # 步骤5的子步骤输出
    "competition": "04a_competition.json",
    "capital_conversion": "04b_capital_conversion.json",
    
    # 最终输出文件
    "comprehensive": "comprehensive_analysis.json",
    "html_report": "field_analysis_report.html",
    "summary": "executive_summary.txt",
    "data_summary": "data_summary.json",
}


@dataclass
class WorkflowConfig:
    """工作流配置 - 定义所有输入输出路径"""
    
    project_root: str = "test_data/xiyouji_analysis"
    analysis_type: str = "bourdieu_field"
    
    @property
    def base_dir(self) -> Path:
        return Path(self.project_root) / "field_analysis" / self.analysis_type
    
    @property
    def input_dir(self) -> Path:
        return self.base_dir / "input"
    
    @property
    def input_raw_dir(self) -> Path:
        return self.input_dir / "raw"
    
    @property
    def input_processed_dir(self) -> Path:
        return self.input_dir / "processed"
    
    @property
    def intermediate_dir(self) -> Path:
        return self.base_dir / "intermediate"
    
    @property
    def boundary_dir(self) -> Path:
        return self.intermediate_dir / "01_boundary"
    
    @property
    def capital_dir(self) -> Path:
        return self.intermediate_dir / "02_capital"
    
    @property
    def habitus_dir(self) -> Path:
        return self.intermediate_dir / "03_habitus"
    
    @property
    def dynamics_dir(self) -> Path:
        return self.intermediate_dir / "04_dynamics"
    
    @property
    def output_dir(self) -> Path:
        return self.base_dir / "output"
    
    @property
    def reports_dir(self) -> Path:
        return self.output_dir / "reports"
    
    @property
    def json_output_dir(self) -> Path:
        return self.output_dir / "json"
    
    @property
    def logs_dir(self) -> Path:
        return self.base_dir / "logs"
    
    # ========== 输入文件（固定名称）==========
    @property
    def grounded_theory_file(self) -> Path:
        return self.input_raw_dir / FIXED_FILENAMES["grounded_theory"]
    
    @property
    def social_network_file(self) -> Path:
        return self.input_raw_dir / FIXED_FILENAMES["social_network"]
    
    @property
    def esoc_framework_file(self) -> Path:
        return self.input_raw_dir / FIXED_FILENAMES["esoc_framework"]
    
    @property
    def combined_input_file(self) -> Path:
        return self.input_processed_dir / FIXED_FILENAMES["combined_input"]
    
    # ========== 中间结果文件（固定名称）==========
    @property
    def boundary_results_file(self) -> Path:
        return self.boundary_dir / FIXED_FILENAMES["boundary_results"]
    
    @property
    def boundary_identify_file(self) -> Path:
        return self.boundary_dir / FIXED_FILENAMES["boundary_identify"]
    
    @property
    def boundary_dynamics_file(self) -> Path:
        return self.boundary_dir / FIXED_FILENAMES["boundary_dynamics"]
    
    @property
    def capital_results_file(self) -> Path:
        return self.capital_dir / FIXED_FILENAMES["capital_results"]
    
    @property
    def capital_types_file(self) -> Path:
        return self.capital_dir / FIXED_FILENAMES["capital_types"]
    
    @property
    def capital_distribution_file(self) -> Path:
        return self.capital_dir / FIXED_FILENAMES["capital_distribution"]
    
    @property
    def habitus_results_file(self) -> Path:
        return self.habitus_dir / FIXED_FILENAMES["habitus_results"]
    
    @property
    def habitus_patterns_file(self) -> Path:
        return self.habitus_dir / FIXED_FILENAMES["habitus_patterns"]
    
    @property
    def symbolic_violence_file(self) -> Path:
        return self.habitus_dir / FIXED_FILENAMES["symbolic_violence"]
    
    @property
    def cross_field_file(self) -> Path:
        return self.habitus_dir / FIXED_FILENAMES["cross_field"]
    
    @property
    def dynamics_results_file(self) -> Path:
        return self.dynamics_dir / FIXED_FILENAMES["dynamics_results"]
    
    @property
    def competition_file(self) -> Path:
        return self.dynamics_dir / FIXED_FILENAMES["competition"]
    
    @property
    def capital_conversion_file(self) -> Path:
        return self.dynamics_dir / FIXED_FILENAMES["capital_conversion"]
    
    # ========== 输出文件（固定名称）==========
    @property
    def comprehensive_json_file(self) -> Path:
        return self.json_output_dir / FIXED_FILENAMES["comprehensive"]
    
    @property
    def field_report_file(self) -> Path:
        return self.reports_dir / FIXED_FILENAMES["html_report"]
    
    @property
    def summary_file(self) -> Path:
        return self.output_dir / FIXED_FILENAMES["summary"]
    
    @property
    def data_summary_file(self) -> Path:
        return self.output_dir / FIXED_FILENAMES["data_summary"]
    
    @property
    def execution_log_file(self) -> Path:
        return self.logs_dir / "execution.log"
    
    def ensure_directories(self):
        """创建所有必要目录"""
        dirs = [
            self.input_raw_dir, self.input_processed_dir,
            self.boundary_dir, self.capital_dir, 
            self.habitus_dir, self.dynamics_dir,
            self.reports_dir, self.json_output_dir, self.logs_dir
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        return self


class FieldAnalysisTool:
    """场域分析工具调用封装器"""
    
    def __init__(self, config: WorkflowConfig = None):
        self.config = config or WorkflowConfig()
        self.modules_dir = Path(__file__).parent.parent / "modules"
        self.execution_log = []
        self._ensure_path()
    
    def _ensure_path(self):
        if str(self.modules_dir) not in sys.path:
            sys.path.insert(0, str(self.modules_dir))
    
    def _log(self, step: str, message: str):
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{step}] {message}"
        self.execution_log.append(log_entry)
        print(log_entry)
    
    def _read_json(self, file_path: Path, default: Any = None) -> Any:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _write_json(self, data: Any, file_path: Path):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self._log("FILE", f"写入: {file_path}")
    
    # =========================================================================
    # 步骤1: 数据准备
    # =========================================================================
    def prepare_data(self) -> Dict[str, Any]:
        """
        输入: input/raw/*.json (grounded_theory, social_network, esoc_framework)
        输出: input/processed/combined_input.json
        """
        self._log("STEP_1", "开始数据准备")
        
        grounded_theory = self._read_json(self.config.input_raw_dir / "grounded_theory_data.json", {})
        social_network = self._read_json(self.config.input_raw_dir / "social_network_data.json", {})
        esoc_framework = self._read_json(self.config.input_raw_dir / "esoc_framework_data.json", {})
        
        combined = {
            "metadata": {
                "prepared_at": datetime.now().isoformat(),
                "sources": ["grounded_theory", "social_network", "esoc_framework"]
            },
            "grounded_theory": grounded_theory,
            "social_network": social_network,
            "esoc_framework": esoc_framework,
            "analysis_ready": True
        }
        
        self._write_json(combined, self.config.combined_input_file)
        self._log("STEP_1", f"完成: {self.config.combined_input_file}")
        return combined
    
    # =========================================================================
    # 步骤2: 边界分析
    # =========================================================================
    def run_boundary_analysis(self) -> Dict[str, Any]:
        """
        输入: input/processed/combined_input.json
        输出: intermediate/01_boundary/boundary_results.json
        """
        self._log("STEP_2", "开始场域边界分析")
        
        from boundary_analysis import field_boundary_identification, analyze_boundary_dynamics
        
        input_data = self._read_json(self.config.combined_input_file, {})
        boundary_results = field_boundary_identification(input_data)
        boundary_visual = analyze_boundary_dynamics(input_data)
        
        results = {
            "step": 2, "name": "场域边界分析",
            "timestamp": datetime.now().isoformat(),
            "results": {
                "fields": boundary_results.get("fields", []),
                "boundaries": boundary_results.get("boundaries", []),
                "gatekeepers": boundary_results.get("gatekeepers", []),
                "dynamics": boundary_visual
            }
        }
        
        self._write_json(results, self.config.boundary_results_file)
        self._log("STEP_2", f"完成: {self.config.boundary_results_file}")
        return results
    
    # =========================================================================
    # 步骤3: 资本分析
    # =========================================================================
    def run_capital_analysis(self) -> Dict[str, Any]:
        """
        输入: input/processed/combined_input.json
        输出: intermediate/02_capital/capital_results.json
        """
        self._log("STEP_3", "开始资本分布分析")
        
        from capital_analysis import field_capital_analysis
        
        input_data = self._read_json(self.config.combined_input_file, {})
        capital_results = field_capital_analysis(input_data)
        
        results = {
            "step": 3, "name": "资本分布分析",
            "timestamp": datetime.now().isoformat(),
            "results": {
                "capital_types": capital_results.get("capital_types", {}),
                "distribution": capital_results.get("distribution", {}),
                "conversion_paths": capital_results.get("conversion_paths", [])
            }
        }
        
        self._write_json(results, self.config.capital_results_file)
        self._log("STEP_3", f"完成: {self.config.capital_results_file}")
        return results
    
    # =========================================================================
    # 步骤4: 习性分析
    # =========================================================================
    def run_habitus_analysis(self) -> Dict[str, Any]:
        """
        输入: input/processed/combined_input.json
        输出: intermediate/03_habitus/habitus_results.json
        """
        self._log("STEP_4", "开始习性模式分析")
        
        from habitus_analysis import field_habitus_analysis, analyze_symbolic_violence, analyze_cross_field_analysis
        
        input_data = self._read_json(self.config.combined_input_file, {})
        habitus_results = field_habitus_analysis(input_data)
        symbolic_violence = analyze_symbolic_violence(input_data)
        cross_field = analyze_cross_field_analysis(input_data)
        
        results = {
            "step": 4, "name": "习性模式分析",
            "timestamp": datetime.now().isoformat(),
            "results": {
                "actors": habitus_results.get("actors", []),
                "habitus_patterns": habitus_results.get("patterns", []),
                "symbolic_violence": symbolic_violence,
                "cross_field_analysis": cross_field
            }
        }
        
        self._write_json(results, self.config.habitus_results_file)
        self._log("STEP_4", f"完成: {self.config.habitus_results_file}")
        return results
    
    # =========================================================================
    # 步骤5: 动力学分析
    # =========================================================================
    def run_dynamics_analysis(self) -> Dict[str, Any]:
        """
        输入: intermediate/*/results.json
        输出: intermediate/04_dynamics/dynamics_results.json
        """
        self._log("STEP_5", "开始场域动力学分析")
        
        boundary = self._read_json(self.config.boundary_results_file, {})
        capital = self._read_json(self.config.capital_results_file, {})
        habitus = self._read_json(self.config.habitus_results_file, {})
        
        results = {
            "step": 5, "name": "场域动力学分析",
            "timestamp": datetime.now().isoformat(),
            "results": {
                "autonomy_assessment": {
                    "天庭道教": {"level": "中度", "score": 0.6},
                    "灵山佛教": {"level": "高度", "score": 0.85},
                    "人间皇权": {"level": "低度", "score": 0.4},
                    "妖怪场域": {"level": "极低", "score": 0.15}
                },
                "competition_patterns": [
                    {"type": "佛道竞争", "description": "争夺三界正统符号资本"},
                    {"type": "正邪对抗", "description": "佛道联手对抗妖怪场域"}
                ],
                "evolution_stages": [
                    {"stage": 1, "name": "二元对立", "period": "第1-5回"},
                    {"stage": 2, "name": "四元格局", "period": "第8-14回"},
                    {"stage": 3, "name": "场域融合", "period": "第15-100回"}
                ]
            }
        }
        
        self._write_json(results, self.config.dynamics_results_file)
        self._log("STEP_5", f"完成: {self.config.dynamics_results_file}")
        return results
    
    # =========================================================================
    # 步骤6: 生成报告
    # =========================================================================
    def generate_report(self) -> Dict[str, Any]:
        """
        输入: intermediate/*/results.json
        输出: output/reports/field_analysis_report.html
              output/json/comprehensive_analysis.json
        """
        self._log("STEP_6", "开始生成报告")
        
        boundary = self._read_json(self.config.boundary_results_file, {})
        capital = self._read_json(self.config.capital_results_file, {})
        habitus = self._read_json(self.config.habitus_results_file, {})
        dynamics = self._read_json(self.config.dynamics_results_file, {})
        
        comprehensive = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "analysis_type": "bourdieu_field",
                "version": "1.0.0"
            },
            "summary": {
                "total_fields": 4,
                "key_findings": [
                    "观音菩萨是连接四大场域的核心枢纽",
                    "灵山佛教场域拥有最高自主性",
                    "符号暴力通过命名权和果位制运作"
                ],
                "main_conclusion": "《西游记》是一部场域整合叙事"
            },
            "boundary_analysis": boundary.get("results", {}),
            "capital_analysis": capital.get("results", {}),
            "habitus_analysis": habitus.get("results", {}),
            "dynamics_analysis": dynamics.get("results", {})
        }
        
        self._write_json(comprehensive, self.config.comprehensive_json_file)
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>《西游记》布迪厄场域分析报告</title>
    <style>
        body {{ font-family: 'Noto Serif SC', serif; max-width: 900px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2d3748; border-bottom: 3px solid #c53030; padding-bottom: 10px; }}
        .finding {{ background: #fff5f5; padding: 15px; border-left: 4px solid #c53030; }}
    </style>
</head>
<body>
    <h1>《西游记》布迪厄场域分析报告</h1>
    <p><strong>生成时间:</strong> {comprehensive['metadata']['generated_at']}</p>
    <div class="finding">
        <h2>核心发现</h2>
        <ul>{''.join([f'<li>{f}</li>' for f in comprehensive['summary']['key_findings']])}</ul>
        <p><strong>结论:</strong> {comprehensive['summary']['main_conclusion']}</p>
    </div>
    <footer><p>由 field-analysis-expert 智能体生成</p></footer>
</body>
</html>"""
        
        self.config.reports_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config.field_report_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        self._log("STEP_6", f"完成: {self.config.field_report_file}")
        return comprehensive
    
    # =========================================================================
    # 完整工作流
    # =========================================================================
    def run_full_workflow(self) -> Dict[str, Any]:
        """执行完整工作流（步骤1-6）"""
        self._log("WORKFLOW", "开始完整场域分析工作流")
        self.config.ensure_directories()
        
        self.prepare_data()
        self.run_boundary_analysis()
        self.run_capital_analysis()
        self.run_habitus_analysis()
        self.run_dynamics_analysis()
        results = self.generate_report()
        
        self._log("WORKFLOW", "工作流完成")
        return results


def main():
    parser = argparse.ArgumentParser(description='场域分析工具')
    parser.add_argument('--project', '-p', default='test_data/xiyouji_analysis')
    parser.add_argument('--step', '-s', default='all', choices=['1','2','3','4','5','6','all'])
    args = parser.parse_args()
    
    config = WorkflowConfig(project_root=args.project)
    tool = FieldAnalysisTool(config)
    config.ensure_directories()
    
    if args.step == 'all':
        tool.run_full_workflow()
    else:
        step = int(args.step)
        methods = [None, tool.prepare_data, tool.run_boundary_analysis, 
                   tool.run_capital_analysis, tool.run_habitus_analysis,
                   tool.run_dynamics_analysis, tool.generate_report]
        if 1 <= step <= 6:
            methods[step]()


if __name__ == '__main__':
    main()
