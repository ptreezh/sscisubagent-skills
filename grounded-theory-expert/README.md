# grounded-theory-expert

**grounded-theory-expert** - 符合 agentskills.io v2.0 规范

## 描述

扎根理论分析技能，基于 Glaser & Strauss (1967)

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
grounded-theory-expert/
├── SKILL.md
├── skill.yaml
├── README.md
├── prompts/
├── tools/
├── templates/
└── tests/
```

## 方法论基础

- Glaser & Strauss (1967)
- Strauss & Corbin (1990)
- Charmaz (2006)

## 许可证

MIT License
