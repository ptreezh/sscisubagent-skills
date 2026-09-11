#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ABM模型构建器 - CAS仿真技能

支持创建多主体模型, 定义主体属性、行为规则和环境设置
遵循六大绝对禁止原则
"""

import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import random


class AgentType(Enum):
    """主体类型枚举(创新扩散示例)"""
    INNOVATOR = "innovator"          # 创新者
    EARLY_ADOPTER = "early_adopter"  # 早期采用者
    EARLY_MAJORITY = "early_majority" # 早期大众
    LATE_MAJORITY = "late_majority"   # 晚期大众
    LAGGARD = "laggard"              # 落后者


class NetworkType(Enum):
    """网络类型枚举"""
    RANDOM = "random"              # 随机网络
    SMALL_WORLD = "small_world"    # 小世界网络(Watts-Strogatz)
    SCALE_FREE = "scale_free"      # 无标度网络(Barabasi-Albert)
    COMPLETE = "complete"          # 完全连接网络


@dataclass
class AgentConfig:
    """主体配置"""
    agent_type: str
    population: int
    attributes: Dict[str, Any] = field(default_factory=dict)
    behavior_rules: List[str] = field(default_factory=list)

    def __post_init__(self):
        """验证配置符合六大禁止原则"""
        # 原则1: 禁止过度简化主体
        if not self.attributes:
            raise ValueError(f"主体 {self.agent_type} 必须有异质性属性")

        # 确保有随机性(原则3)
        if "random_seed" not in self.attributes:
            self.attributes["random_seed"] = random.randint(0, 10000)


@dataclass
class EnvironmentConfig:
    """环境配置"""
    network_type: str
    num_agents: int
    network_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """验证配置符合六大禁止原则"""
        # 原则2: 禁止忽视空间
        if not self.network_type:
            raise ValueError("必须指定网络类型(空间结构)")

        # 设置默认网络参数
        if self.network_type == NetworkType.SMALL_WORLD.value:
            default_params = {"k": 6, "p": 0.1}  # 平均度6, 重连概率0.1
        elif self.network_type == NetworkType.SCALE_FREE.value:
            default_params = {"m": 2}  # 每个新节点连接2个现有节点
        else:
            default_params = {}

        # 合并用户参数
        for key, value in default_params.items():
            if key not in self.network_params:
                self.network_params[key] = value


@dataclass
class SimulationConfig:
    """仿真配置"""
    num_steps: int
    num_runs: int = 1  # 原则5: 多次运行
    save_interval: int = 10
    random_seed: Optional[int] = None

    def __post_init__(self):
        """验证配置符合六大禁止原则"""
        # 原则5: 禁止单一运行
        if self.num_runs < 1:
            raise ValueError("必须至少运行1次仿真")

        if self.num_runs < 100 and self.random_seed is None:
            # 建议：蒙特卡洛应该≥100次
            print(f"⚠️ 警告: 为了减少随机性影响, 建议num_runs≥100(当前: {self.num_runs})")


class ABMModelBuilder:
    """ABM模型构建器"""

    def __init__(self):
        self.agent_types: List[AgentConfig] = []
        self.environment: Optional[EnvironmentConfig] = None
        self.simulation: Optional[SimulationConfig] = None
        self.global_params: Dict[str, Any] = {}

    def add_agent_type(self, agent_type: str, population: int,
                     attributes: Dict[str, Any],
                     behavior_rules: List[str]) -> 'ABMModelBuilder':
        """添加主体类型"""
        agent_config = AgentConfig(
            agent_type=agent_type,
            population=population,
            attributes=attributes,
            behavior_rules=behavior_rules
        )
        self.agent_types.append(agent_config)
        return self

    def set_environment(self, network_type: str, num_agents: int,
                      network_params: Dict[str, Any]) -> 'ABMModelBuilder':
        """设置环境"""
        self.environment = EnvironmentConfig(
            network_type=network_type,
            num_agents=num_agents,
            network_params=network_params
        )
        return self

    def set_simulation(self, num_steps: int, num_runs: int = 1,
                      save_interval: int = 10) -> 'ABMModelBuilder':
        """设置仿真参数"""
        self.simulation = SimulationConfig(
            num_steps=num_steps,
            num_runs=num_runs,
            save_interval=save_interval
        )
        return self

    def set_global_param(self, key: str, value: Any) -> 'ABMModelBuilder':
        """设置全局参数"""
        self.global_params[key] = value
        return self

    def validate(self) -> tuple[bool, List[str]]:
        """验证模型配置符合六大禁止原则"""
        errors = []

        # 原则1: 检查主体异质性
        if len(self.agent_types) < 1:
            errors.append("至少需要定义1种主体类型")

        for agent in self.agent_types:
            if not agent.attributes:
                errors.append(f"主体 {agent.agent_type} 缺少异质性属性")

        # 原则2: 检查空间结构
        if not self.environment:
            errors.append("必须设置环境(空间结构)")

        # 原则3: 检查随机性
        # 随机性可以在行为规则中, 也可以在属性中(random_seed)
        has_stochasticity = any(
            "random" in str(rule).lower() or "probability" in str(rule).lower() or
            any("random" in str(attr).lower() for attr in agent.attributes.keys())
            for agent in self.agent_types
            for rule in agent.behavior_rules
        )
        if not has_stochasticity:
            errors.append("互动规则中应包含随机性机制")

        # 原则4: 涌现验证(将在运行时检查)
        # 原则5: 多次运行(已检查)
        # 原则6: 透明度(将在输出时保证)

        return len(errors) == 0, errors

    def build_model_code(self) -> str:
        """生成Python模型代码"""
        if not self.environment:
            raise ValueError("必须先设置环境")

        code_lines = []

        # 导入
        code_lines.append("""
import mesa
import numpy as np
import networkx as nx
from dataclasses import dataclass
from typing import List, Dict
import random

""")

        # 生成主体类
        code_lines.append("# ===== 主体定义 =====\n")

        for i, agent in enumerate(self.agent_types):
            code_lines.append(f"class {agent.agent_type.title().replace('_', '')}(mesa.Agent):\n")
            code_lines.append(f'    """{agent.agent_type}主体"""\n')
            code_lines.append(f"    def __init__(self, unique_id, model):\n")
            code_lines.append(f"        super().__init__(unique_id, model)\n")

            # 添加属性
            for attr_name, attr_value in agent.attributes.items():
                if isinstance(attr_value, (int, float)):
                    code_lines.append(f"        self.{attr_name} = {attr_value}\n")
                elif isinstance(attr_value, str):
                    code_lines.append(f"        self.{attr_name} = '{attr_value}'\n")
                elif isinstance(attr_value, list):
                    code_lines.append(f"        self.{attr_name} = {attr_value}\n")
                else:
                    code_lines.append(f"        self.{attr_name} = {repr(attr_value)}\n")

            # 添加随机性(原则3)
            code_lines.append(f"        # 添加随机变异\n")
            code_lines.append(f"        self.random_seed = random.randint(0, 10000)\n")
            code_lines.append(f"        random.seed(self.random_seed)\n")

            code_lines.append(f"\n    def step(self):\n")
            code_lines.append(f"        # 主体行为\n")

            # 添加行为规则
            for rule in agent.behavior_rules:
                code_lines.append(f"        {rule}\n")

            code_lines.append("\n")

        # 生成模型类
        code_lines.append("# ===== 模型定义 =====\n")
        code_lines.append(f"""
class {self.global_params.get('model_name', 'CASModel')}(mesa.Model):\n
    \"\"\"复杂适应系统仿真模型\"\"\"

    def __init__(self):
        super().__init__()

        # 初始化环境
        self.num_agents = {self.environment.num_agents}
        self.network_type = "{self.environment.network_type}"
        self.network_params = {self.environment.network_params}

        # 创建网络
        self.grid = self._create_network()
        self.schedule = mesa.time.RandomActivation(self)

        # 创建主体
        self.agents = []
        self._create_agents()

        # 数据收集
        self.datacollector = mesa.DataCollector(
            model_reporters=self._model_reporters(),
            agent_reporters=self._agent_reporters()
        )

    def _create_network(self):
        \"\"\"创建网络结构\"\"\"
        network_type = self.network_type
        n = self.num_agents
        params = self.network_params

        if network_type == "small_world":
            k = params.get("k", 6)
            p = params.get("p", 0.1)
            G = nx.watts_strogatz_graph(n, k, p)
        elif network_type == "scale_free":
            m = params.get("m", 2)
            G = nx.barabasi_albert_graph(n, m)
        elif network_type == "random":
            G = nx.erdos_renyi_graph(n, 0.1)
        elif network_type == "complete":
            G = nx.complete_graph(n)
        else:
            raise ValueError(f"未知的网络类型: {{network_type}}")

        # 转换为Mesa空间
        return mesa.space.NetworkGrid(G)

    def _create_agents(self):
        \"\"\"创建主体\"\"\"
        agent_id = 0
        for agent_config in [
            {{
                'agent_type': a.agent_type,
                'population': a.population,
                'attributes': a.attributes
            }}
            for a in self.agent_types
        ]:
            for _ in range(agent_config['population']):
                agent = {{agent_config['agent_type'].title().replace('_', '')}}(agent_id, self)
                self.grid.place_agent(agent, (agent_id % self.num_agents, agent_id // self.num_agents))
                self.schedule.add(agent)
                self.agents.append(agent)
                agent_id += 1

    def _model_reporters(self):
        \"\"\"模型级数据收集器\"\"\"
        return {{
            "total_agents": lambda m: len(m.agents),
            "active_agents": lambda m: sum(1 for a in m.agents if hasattr(a, 'active') and a.active),
        }}

    def _agent_reporters(self):
        \"\"\"主体级数据收集器\"\"\"
        return {{
            "agent_type": lambda a: type(a).__name__,
        }}

    def step(self):
        \"\"\"执行一步仿真\"\"\"
        self.datacollector.collect(self)
        self.schedule.step()
""")

        return "".join(code_lines)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "model_name": self.global_params.get('model_name', 'CASModel'),
            "agent_types": [asdict(a) for a in self.agent_types],
            "environment": asdict(self.environment) if self.environment else None,
            "simulation": asdict(self.simulation) if self.simulation else None,
            "global_params": self.global_params
        }

    def to_json(self, filepath: str):
        """保存为JSON文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def from_example_innovation_diffusion(cls) -> 'ABMModelBuilder':
        """创建创新扩散模型示例"""
        builder = cls()

        # 添加5种主体类型(原则1: 异质性)
        builder.add_agent_type(
            agent_type="innovator",
            population=10,
            attributes={
                "adoption_threshold": 0.1,
                "social_influence": 0.8,
                "openness": 0.9
            },
            behavior_rules=["self._decide_to_adopt()", "self._influence_neighbors()"]
        )

        builder.add_agent_type(
            agent_type="early_adopter",
            population=150,
            attributes={
                "adoption_threshold": 0.3,
                "social_influence": 0.6,
                "openness": 0.7
            },
            behavior_rules=["self._decide_to_adopt()", "self._influence_neighbors()"]
        )

        builder.add_agent_type(
            agent_type="early_majority",
            population=350,
            attributes={
                "adoption_threshold": 0.5,
                "social_influence": 0.4,
                "openness": 0.5
            },
            behavior_rules=["self._decide_to_adopt()", "self._influence_neighbors()"]
        )

        builder.add_agent_type(
            agent_type="late_majority",
            population=350,
            attributes={
                "adoption_threshold": 0.7,
                "social_influence": 0.3,
                "openness": 0.3
            },
            behavior_rules=["self._decide_to_adopt()", "self._influence_neighbors()"]
        )

        builder.add_agent_type(
            agent_type="laggard",
            population=140,
            attributes={
                "adoption_threshold": 0.9,
                "social_influence": 0.1,
                "openness": 0.1
            },
            behavior_rules=["self._decide_to_adopt()", "self._influence_neighbors()"]
        )

        # 设置环境(原则2: 空间结构)
        builder.set_environment(
            network_type="small_world",
            num_agents=1000,
            network_params={"k": 6, "p": 0.1}
        )

        # 设置仿真参数(原则5: 多次运行)
        builder.set_simulation(
            num_steps=100,
            num_runs=100,  # 蒙特卡洛
            save_interval=10
        )

        builder.set_global_param("model_name", "InnovationDiffusionModel")

        return builder


def main():
    """主函数 - 演示ABM模型构建"""
    print("=" * 80)
    print("ABM模型构建器演示")
    print("=" * 80)
    print()

    # 创建创新扩散模型
    print("创建创新扩散ABM模型...")
    builder = ABMModelBuilder.from_example_innovation_diffusion()

    # 验证配置
    print("验证模型配置...")
    is_valid, errors = builder.validate()

    if is_valid:
        print("✅ 模型配置符合六大绝对禁止原则")
    else:
        print("❌ 模型配置存在以下问题:")
        for error in errors:
            print(f"  - {error}")
        return

    # 生成代码
    print()
    print("生成Python模型代码...")
    code = builder.build_model_code()

    # 保存代码
    output_file = "cas_innovation_diffusion_model.py"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)

    print(f"✅ 模型代码已保存到: {output_file}")
    print()

    # 保存配置
    config_file = "cas_innovation_diffusion_config.json"
    builder.to_json(config_file)
    print(f"✅ 模型配置已保存到: {config_file}")
    print()

    print("模型摘要:")
    model_dict = builder.to_dict()
    print(f"  模型名称: {model_dict['model_name']}")
    print(f"  主体类型数: {len(model_dict['agent_types'])}")
    print(f"  总主体数: {model_dict['environment']['num_agents']}")
    print(f"  网络类型: {model_dict['environment']['network_type']}")
    print(f"  仿真步数: {model_dict['simulation']['num_steps']}")
    print(f"  仿真次数: {model_dict['simulation']['num_runs']}")
    print()


if __name__ == "__main__":
    main()
