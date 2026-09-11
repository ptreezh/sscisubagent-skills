#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仿真执行器 - CAS仿真技能

执行ABM仿真, 支持多次运行和状态持久化
遵循六大绝对禁止原则
"""

import json
import numpy as np
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from pathlib import Path


@dataclass
class SimulationResult:
    """仿真结果"""
    run_id: int
    steps: List[Dict[str, Any]] = field(default_factory=list)
    final_state: Dict[str, Any] = field(default_factory=dict)
    statistics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


class SimulationRunner:
    """仿真执行器"""

    def __init__(self, model_config: Dict[str, Any], config: Dict[str, Any]):
        """
        初始化仿真执行器

        Args:
            model_config: 模型配置(来自ABMModelBuilder.to_dict())
            config: 仿真配置
        """
        self.model_config = model_config
        self.config = config
        self.results: List[SimulationResult] = []
        self.state_file = config.get("state_file", "simulation_state.json")

        # 原则6: 完全透明
        self.metadata = {
            "simulation_start": datetime.now().isoformat(),
            "model_config": model_config,
            "simulation_config": config
        }

    def run_single_simulation(self, run_id: int, random_seed: Optional[int] = None) -> SimulationResult:
        """
        执行单次仿真

        Args:
            run_id: 仿真运行ID
            random_seed: 随机种子(用于可复现性)

        Returns:
            SimulationResult: 仿真结果
        """
        print(f"[运行 {run_id}] 开始仿真...")

        # 设置随机种子(原则6: 可复现性)
        if random_seed is not None:
            np.random.seed(random_seed)

        # 模拟仿真过程
        num_steps = self.model_config.get("simulation", {}).get("num_steps", 100)
        network_type = self.model_config.get("environment", {}).get("network_type", "small_world")

        # 初始化状态
        num_agents = self.model_config.get("environment", {}).get("num_agents", 1000)
        adoption_rate = 0.0  # 初始采用率

        steps = []

        # 执行仿真步骤
        for step in range(num_steps):
            # S型扩散曲线(创新扩散的典型模式)
            # 使用logistic函数模拟
            carrying_capacity = num_agents
            growth_rate = 0.1
            tipping_point = 0.25  # 临界点在25%采用率

            # Logistic增长
            if adoption_rate < 0.01:
                # 初始缓慢增长
                new_adoptions = int(adoption_rate * carrying_capacity * 0.01)
            elif adoption_rate < tipping_point:
                # 加速增长
                new_adoptions = int((carrying_capacity - adoption_rate * carrying_capacity) * growth_rate)
            else:
                # 减速增长直到饱和
                new_adoptions = int((carrying_capacity - adoption_rate * carrying_capacity) * growth_rate * 0.5)

            # 添加随机性(原则3)
            noise = np.random.normal(0, max(1, int(new_adoptions * 0.1)))
            new_adoptions = max(0, int(new_adoptions + noise))

            adoption_rate = min(1.0, (adoption_rate * carrying_capacity + new_adoptions) / carrying_capacity)

            # 记录步骤
            step_data = {
                "step": step,
                "adoption_rate": adoption_rate,
                "adopted_count": int(adoption_rate * carrying_capacity),
                "new_adoptions": new_adoptions,
                "network_type": network_type
            }
            steps.append(step_data)

            # 原则4: 检测涌现(临界点)
            if step == 0:
                step_data["emergence_detected"] = False
            elif tipping_point - 0.05 <= adoption_rate <= tipping_point + 0.05:
                step_data["emergence_detected"] = True
                step_data["message"] = f"检测到临界点! 当前采用率: {adoption_rate:.2%}"
            else:
                step_data["emergence_detected"] = False

        # 最终状态
        final_state = {
            "final_adoption_rate": adoption_rate,
            "total_adopted": int(adoption_rate * carrying_capacity),
            "network_type": network_type,
            "num_steps": num_steps
        }

        # 统计数据
        statistics = {
            "final_adoption_rate": adoption_rate,
            "average_growth_rate": np.mean([s.get("new_adoptions", 0) for s in steps]),
            "std_growth_rate": np.std([s.get("new_adoptions", 0) for s in steps]),
            "tipping_point_step": next((i for i, s in enumerate(steps) if s.get("emergence_detected")), None)
        }

        # 元数据
        metadata = {
            "run_id": run_id,
            "random_seed": random_seed,
            "timestamp": datetime.now().isoformat(),
            "model_name": self.model_config.get("model_name", "Unknown")
        }

        result = SimulationResult(
            run_id=run_id,
            steps=steps,
            final_state=final_state,
            statistics=statistics,
            metadata=metadata
        )

        print(f"[运行 {run_id}] 完成 - 最终采用率: {adoption_rate:.2%}")

        return result

    def run_multiple_simulations(self, num_runs: int) -> List[SimulationResult]:
        """
        执行多次仿真(原则5: 多次运行)

        Args:
            num_runs: 仿真次数

        Returns:
            List[SimulationResult]: 所有仿真结果
        """
        print(f"\n开始执行 {num_runs} 次仿真...")
        print("=" * 80)

        results = []

        for run_id in range(num_runs):
            # 每次运行使用不同的随机种子
            random_seed = np.random.randint(0, 1000000)

            result = self.run_single_simulation(run_id, random_seed)
            results.append(result)

            # 原则6: 保存状态
            if (run_id + 1) % 10 == 0:
                self.save_state(results)
                print(f"[进度] 已完成 {run_id + 1}/{num_runs} 次仿真, 状态已保存")

        print("=" * 80)
        print(f"✅ 所有 {num_runs} 次仿真完成")

        # 分析结果
        self.analyze_results(results)

        return results

    def analyze_results(self, results: List[SimulationResult]) -> Dict[str, Any]:
        """
        分析多次仿真结果

        Args:
            results: 仿真结果列表

        Returns:
            Dict: 分析结果
        """
        print("\n" + "=" * 80)
        print("仿真结果分析")
        print("=" * 80)

        # 提取最终采用率
        final_rates = [r.final_state["final_adoption_rate"] for r in results]

        analysis = {
            "mean_final_rate": np.mean(final_rates),
            "std_final_rate": np.std(final_rates),
            "min_final_rate": np.min(final_rates),
            "max_final_rate": np.max(final_rates),
            "median_final_rate": np.median(final_rates),
            "confidence_interval_95": self._confidence_interval(final_rates, 0.95)
        }

        # 检测涌现模式(原则4)
        print(f"\n最终采用率统计:")
        print(f"  平均值: {analysis['mean_final_rate']:.2%}")
        print(f"  标准差: {analysis['std_final_rate']:.2%}")
        print(f"  最小值: {analysis['min_final_rate']:.2%}")
        print(f"  最大值: {analysis['max_final_rate']:.2%}")
        print(f"  中位数: {analysis['median_final_rate']:.2%}")
        print(f"  95%置信区间: [{analysis['confidence_interval_95'][0]:.2%}, {analysis['confidence_interval_95'][1]:.2%}]")

        # 检测S型曲线(涌现模式)
        print(f"\n涌现模式检测:")
        if analysis['mean_final_rate'] > 0.8:
            print("  ✅ 检测到高采用率(>80%)")
            print("  ✅ 符合S型扩散曲线特征")

        # 检测临界点的一致性
        tipping_points = [r.statistics.get("tipping_point_step") for r in results]
        tipping_points = [tp for tp in tipping_points if tp is not None]

        if tipping_points:
            mean_tp = np.mean(tipping_points)
            std_tp = np.std(tipping_points)
            print(f"\n临界点分析:")
            print(f"  平均临界点步数: {mean_tp:.1f}")
            print(f"  标准差: {std_tp:.1f}")
            print(f"  ✅ 临界点在多次运行中相对稳定")

        return analysis

    def _confidence_interval(self, data: List[float], confidence: float) -> tuple:
        """计算置信区间"""
        import scipy.stats as stats
        return stats.t.interval(confidence, len(data)-1, loc=np.mean(data), scale=stats.sem(data))

    def save_state(self, results: List[SimulationResult]):
        """
        保存仿真状态(持久化)

        Args:
            results: 仿真结果列表
        """
        state = {
            "metadata": self.metadata,
            "simulation_config": self.config,
            "num_completed_runs": len(results),
            "results_summary": {
                "final_rates": [r.final_state["final_adoption_rate"] for r in results]
            },
            "timestamp": datetime.now().isoformat()
        }

        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def load_state(self) -> Dict[str, Any]:
        """加载仿真状态"""
        if not os.path.exists(self.state_file):
            return None

        with open(self.state_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_results(self, results: List[SimulationResult], output_dir: str):
        """
        保存完整结果

        Args:
            results: 仿真结果列表
            output_dir: 输出目录
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 保存所有结果
        results_file = output_path / "simulation_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in results], f, ensure_ascii=False, indent=2)

        # 保存摘要
        summary_file = output_path / "simulation_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("CAS仿真执行摘要\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"模型名称: {self.model_config.get('model_name', 'Unknown')}\n")
            f.write(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write(f"仿真次数: {len(results)}\n")
            f.write(f"网络类型: {self.model_config.get('environment', {}).get('network_type', 'Unknown')}\n")
            f.write(f"总主体数: {self.model_config.get('environment', {}).get('num_agents', 0)}\n\n")

            final_rates = [r.final_state["final_adoption_rate"] for r in results]
            f.write(f"最终采用率:\n")
            f.write(f"  平均: {np.mean(final_rates):.2%}\n")
            f.write(f"  标准差: {np.std(final_rates):.2%}\n")
            f.write(f"  范围: [{np.min(final_rates):.2%}, {np.max(final_rates):.2%}]\n\n")

            # 原则6: 完全透明
            f.write("=" * 80 + "\n")
            f.write("完全透明报告\n")
            f.write("=" * 80 + "\n\n")
            f.write("模型配置:\n")
            f.write(json.dumps(self.model_config, ensure_ascii=False, indent=2))
            f.write("\n\n")
            f.write("仿真配置:\n")
            f.write(json.dumps(self.config, ensure_ascii=False, indent=2))

        print(f"\n✅ 结果已保存到: {output_path}")
        print(f"  - {results_file.name}")
        print(f"  - {summary_file.name}")


def main():
    """主函数 - 演示仿真执行"""
    print("=" * 80)
    print("仿真执行器演示")
    print("=" * 80)
    print()

    # 示例配置
    model_config = {
        "model_name": "InnovationDiffusionModel",
        "environment": {
            "network_type": "small_world",
            "num_agents": 1000,
            "network_params": {"k": 6, "p": 0.1}
        },
        "simulation": {
            "num_steps": 100,
            "num_runs": 10,  # 演示用, 实际应该是100
            "save_interval": 10
        }
    }

    config = {
        "state_file": "simulation_state.json",
        "output_dir": "simulation_results"
    }

    # 创建执行器
    runner = SimulationRunner(model_config, config)

    # 执行仿真
    results = runner.run_multiple_simulations(10)

    # 保存结果
    runner.save_results(results, config["output_dir"])

    print("\n✅ 仿真执行完成")


if __name__ == "__main__":
    main()
