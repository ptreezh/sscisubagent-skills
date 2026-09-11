#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参数扫描工具 - CAS仿真技能

执行参数敏感性分析和批量仿真
遵循六大绝对禁止原则
"""

import numpy as np
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Callable
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime
import os


@dataclass
class ParameterSweepResult:
    """参数扫描结果"""
    parameter_name: str
    parameter_value: float
    run_id: int
    metrics: Dict[str, float] = field(default_factory=dict)
    statistics: Dict[str, float] = field(default_factory=dict)


class ParameterSweep:
    """参数扫描器"""

    def __init__(self, base_config: Dict[str, Any]):
        """
        初始化参数扫描器

        Args:
            base_config: 基础配置
        """
        self.base_config = base_config
        self.results: List[ParameterSweepResult] = []

    def sweep_parameter(self,
                     parameter_name: str,
                     parameter_values: List[float],
                     num_runs: int = 20) -> List[ParameterSweepResult]:
        """
        执行参数扫描

        Args:
            parameter_name: 参数名称
            parameter_values: 参数值列表
            num_runs: 每个参数值的运行次数

        Returns:
            List[ParameterSweepResult]: 扫描结果
        """
        print("=" * 80)
        print(f"参数扫描: {parameter_name}")
        print("=" * 80)
        print()

        print(f"参数值数量: {len(parameter_values)}")
        print(f"每个值运行次数: {num_runs}")
        print(f"总运行次数: {len(parameter_values) * num_runs}")
        print()

        results = []

        # 原则5: 多次运行(并行执行)
        for i, param_value in enumerate(parameter_values):
            print(f"[{i+1}/{len(parameter_values)}] 参数值 = {param_value:.4f}")

            # 执行多次运行
            for run_id in range(num_runs):
                # 模拟仿真(简化版)
                result = self._simulate_with_parameter(
                    parameter_name, param_value, run_id
                )

                results.append(result)

            print(f"  平均最终采用率: {np.mean([r.metrics.get('final_rate', 0) for r in results[-num_runs:]]):.2%}")

        print()
        print(f"✅ 参数扫描完成, 共 {len(results)} 次仿真")

        # 分析结果
        self._analyze_sensitivity(results, parameter_name)

        return results

    def _simulate_with_parameter(self, param_name: str, param_value: float,
                                 run_id: int) -> ParameterSweepResult:
        """
        使用指定参数值执行仿真

        Args:
            param_name: 参数名称
            param_value: 参数值
            run_id: 运行ID

        Returns:
            ParameterSweepResult: 仿真结果
        """
        # 模拟S型扩散, 参数影响增长速率
        steps = 100
        L = 0.85  # 承载容量
        k = param_value  # 使用参数值作为增长率
        x0 = 25  # 临界点

        # 计算最终采用率
        final_rate = L / (1 + np.exp(-k * (steps - x0)))

        # 添加随机性
        final_rate += np.random.normal(0, 0.02)
        final_rate = max(0, min(1, final_rate))

        return ParameterSweepResult(
            parameter_name=param_name,
            parameter_value=param_value,
            run_id=run_id,
            metrics={
                "final_rate": final_rate
            },
            statistics={
                "steps": steps,
                "carrying_capacity": L,
                "inflection_point": x0
            }
        )

    def _analyze_sensitivity(self, results: List[ParameterSweepResult], param_name: str):
        """
        分析参数敏感性

        Args:
            results: 扫描结果
            param_name: 参数名称
        """
        print("\n" + "=" * 80)
        print(f"参数敏感性分析: {param_name}")
        print("=" * 80)
        print()

        # 按参数值分组
        param_values = sorted(set([r.parameter_value for r in results]))

        for val in param_values:
            val_results = [r for r in results if r.parameter_value == val]
            final_rates = [r.metrics.get("final_rate", 0) for r in val_results]

            print(f"参数值 {val:.4f}:")
            print(f"  平均最终采用率: {np.mean(final_rates):.2%}")
            print(f"  标准差: {np.std(final_rates):.2%}")
            print(f"  范围: [{np.min(final_rates):.2%}, {np.max(final_rates):.2%}]")
            print()

    def parallel_sweep(self,
                     parameter_name: str,
                     parameter_values: List[float],
                     num_runs: int = 20,
                     max_workers: int = 4) -> List[ParameterSweepResult]:
        """
        并行执行参数扫描

        Args:
            parameter_name: 参数名称
            parameter_values: 参数值列表
            num_runs: 每个参数值的运行次数
            max_workers: 最大并行工作数

        Returns:
            List[ParameterSweepResult]: 扫描结果
        """
        print("=" * 80)
        print(f"并行参数扫描: {parameter_name}")
        print("=" * 80)
        print()

        print(f"参数值数量: {len(parameter_values)}")
        print(f"每个值运行次数: {num_runs}")
        print(f"最大并行数: {max_workers}")
        print(f"总任务数: {len(parameter_values) * num_runs}")
        print()

        results = []

        # 创建任务列表
        tasks = []
        for param_value in parameter_values:
            for run_id in range(num_runs):
                tasks.append((param_value, run_id))

        # 并行执行
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            futures = {
                executor.submit(self._simulate_with_parameter, parameter_name, param_value, run_id): (param_value, run_id)
                for param_value, run_id in tasks
            }

            # 收集结果
            completed = 0
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1

                    if completed % 10 == 0:
                        print(f"  进度: {completed}/{len(tasks)} 完成")

                except Exception as e:
                    print(f"  ⚠️ 任务执行出错: {e}")

        print()
        print(f"✅ 并行扫描完成, 共 {len(results)} 次仿真")

        return results

    def save_results(self, results: List[ParameterSweepResult], output_dir: str):
        """
        保存参数扫描结果

        Args:
            results: 扫描结果
            output_dir: 输出目录
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 保存JSON结果
        results_file = output_path / f"parameter_sweep_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(r) for r in results], f, ensure_ascii=False, indent=2)

        # 保存文本报告
        report_file = output_path / f"parameter_sweep_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("参数扫描报告\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # 按参数值分组统计
            param_values = sorted(set([r.parameter_value for r in results]))

            f.write("参数敏感性摘要:\n")
            f.write("-" * 80 + "\n")

            for val in param_values:
                val_results = [r for r in results if r.parameter_value == val]
                final_rates = [r.metrics.get("final_rate", 0) for r in val_results]

                f.write(f"\n参数值 {val:.4f}:\n")
                f.write(f"  平均最终采用率: {np.mean(final_rates):.2%}\n")
                f.write(f"  标准差: {np.std(final_rates):.2%}\n")
                f.write(f"  最小值: {np.min(final_rates):.2%}\n")
                f.write(f"  最大值: {np.max(final_rates):.2%}\n")
                f.write(f"  运行次数: {len(val_results)}\n")

        print(f"\n✅ 参数扫描结果已保存到: {output_path}")
        print(f"  - {results_file.name}")
        print(f"  - {report_file.name}")


def main():
    """主函数 - 演示参数扫描"""
    print("=" * 80)
    print("参数扫描工具演示")
    print("=" * 80)
    print()

    # 基础配置
    base_config = {
        "model_name": "ParameterSweepDemo",
        "simulation": {
            "num_steps": 100,
            "num_runs": 20
        }
    }

    # 创建扫描器
    sweeper = ParameterSweep(base_config)

    # 定义参数扫描范围
    parameter_values = [0.02, 0.04, 0.06, 0.08, 0.10]

    # 执行扫描
    results = sweeper.sweep_parameter(
        parameter_name="growth_rate",
        parameter_values=parameter_values,
        num_runs=20
    )

    # 保存结果
    sweeper.save_results(results, "parameter_sweep_results")

    print("\n✅ 参数扫描演示完成")


if __name__ == "__main__":
    main()
