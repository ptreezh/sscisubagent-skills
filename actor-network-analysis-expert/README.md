# actor-network-analysis-expert

**actor-network-analysis-expert** - 符合 agentskills.io v2.0 规范

## 描述

行动者网络理论(ANT)分析技能，基于 Latour (2005), Callon (1986), Law (1992)

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```python
from tools.analyze import SkillExpert
expert = SkillExpert()
result = expert.analyze(data)
```

## 目录结构

```
actor-network-analysis-expert/
├── SKILL.md
├── skill.yaml
├── README.md
├── prompts/
├── tools/
├── templates/
└── tests/
```

## 方法论基础

- Latour (2005) - Reassembling the Social
- Callon (1986) - Some Elements of a Sociology of Translation
- Law (1992) - Notes on the Theory of the Actor-Network

## 6大绝对禁止原则

1. 禁止人为/非人二分法 (非人行动者≥30%)
2. 禁止未追踪到底就停止
3. 禁止预设网络边界
4. 禁止静态网络观
5. 禁止功能主义解释
6. 禁止黑箱化

## 可用工具

- actor_extractor.py - 从异质性数据中提取行动者
- translation_stage_controller.py - 管理4阶段转译过程
- symmetry_checker.py - 验证人类/非人对称性
- controversy_recorder.py - 记录网络争议和失败
- assess_network_saturation.py - 评估网络饱和度
- blackbox_opener.py - 打开黑箱揭示内部结构

- Scott (2017) - Social Network Analysis
- Wasserman & Faust (1994)

## 许可证

MIT License
