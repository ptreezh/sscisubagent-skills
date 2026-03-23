#!/usr/bin/env python3
"""
Soul Agent Creator - 分身创建核心引擎
=======================================

通过自然语言理解，智能推荐并创建研究分身。

用法（通过skill内部调用）:
    python scripts/create_engine.py --skill grounded-theory --name "我的助手"
    python scripts/create_engine.py --interactive  # 交互式
    python scripts/create_engine.py --list         # 列出所有分身

作者: SocienceAI Soul Agent System
版本: 1.0.0
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================================
# 配置
# ============================================================================

AGENTS_METADATA_PATH = Path(__file__).parent.parent / "metadata" / "agents.json"
STORAGE_ROOT = Path.home() / ".stigmergy" / "soul-agents"
TEMPLATE_DIR = Path(__file__).parent.parent / "templates"

# ============================================================================
# 核心类
# ============================================================================


class SoulAgentCreator:
    """分身创建引擎"""

    def __init__(self):
        self.metadata = self._load_metadata()
        self.storage_root = STORAGE_ROOT
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def _load_metadata(self) -> dict:
        """加载分身元数据"""
        with open(AGENTS_METADATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def _get_all_agents(self) -> Dict[str, dict]:
        """获取所有分身定义"""
        agents = {}
        for category in [
            "qualitative_methods",
            "quantitative_methods",
            "mixed_methods",
            "social_theory",
            "business_methods",
        ]:
            if category in self.metadata:
                agents.update(self.metadata[category]["agents"])
        return agents

    def _get_category_info(self) -> Dict[str, str]:
        """获取分类信息"""
        return {
            "qualitative_methods": "📖 质性研究方法",
            "quantitative_methods": "📊 定量研究方法",
            "mixed_methods": "🔄 混合研究方法",
            "social_theory": "🧠 社会理论视角",
            "business_methods": "📈 商业管理方法",
        }

    def understand_request(self, user_input: str) -> Tuple[Optional[str], dict]:
        """
        理解用户请求，返回分身ID和建议

        Returns:
            (skill_id, intent_analysis)
        """
        user_lower = user_input.lower()
        agents = self._get_all_agents()

        # 关键词匹配
        keywords_map = {
            # 质性研究
            "grounded-theory": ["扎根", "grounded", "gt", "理论建构", "质性"],
            "actor-network-theory": ["行动者", "ant", "latour", "actor", "技术社会"],
            "bourdieu-field-analysis": [
                "布迪厄",
                "bourdieu",
                "场域",
                "文化资本",
                "惯习",
            ],
            "discourse-analysis": ["话语", "discourse", "foucault", "批判话语"],
            "content-analysis": ["内容分析", "content", "文本编码", "内容编码"],
            "narrative-analysis": ["叙事", "narrative", "故事", "叙事分析"],
            "phenomenology": ["现象学", "phenomen", "生活世界", "husserl"],
            "ethnography": ["民族志", "ethno", "田野", "geertz", "文化描述"],
            "case-study": ["案例", "case", "yin", "案例研究", "multiple case"],
            # 定量研究
            "regression-analysis": [
                "回归",
                "regression",
                "计量",
                "ols",
                " econometric",
            ],
            "qca-analysis": [
                "qca",
                "定性比较",
                "qualitative comparative",
                "ragin",
                "模糊集",
            ],
            "did-analysis": [
                "did",
                "双重差分",
                "difference-in-difference",
                "政策评估",
                "准实验",
            ],
            "factor-analysis": ["因子", "factor", "efa", "cfa", "维度"],
            "sem-analysis": [
                "sem",
                "结构方程",
                "structural equation",
                "amos",
                "lisrel",
                "路径分析",
            ],
            "multilevel-modeling": ["多层", "multilevel", "hlm", "嵌套", "层次"],
            "longitudinal-analysis": [
                "纵向",
                "追踪",
                "longitudinal",
                "panel",
                "growth",
            ],
            "meta-analysis": [
                "元分析",
                "meta",
                "文献综合",
                "效应量",
                "systematic review",
            ],
            # 混合方法
            "mixed-methods": ["混合方法", "mixed method", "整合", "triangulation"],
            "action-research": [
                "行动研究",
                "action research",
                " participatory",
                "实践",
            ],
            "secondary-analysis": ["二手数据", "secondary", "大型调查", "cgss"],
            # 社会理论
            "digital-marxism": ["马克思", "marx", "剩余价值", "资本", "批判"],
            "digital-durkheim": ["涂尔干", "durkh", "社会整合", "失范", "团结"],
            "digital-weber": ["韦伯", "weber", "理性化", "科层制", "新教伦理"],
            "social-network-analysis": ["社会网络", "network", "sna", "中心性", "社群"],
            # 商业方法
            "swot-analysis": ["swot", "优势劣势", "战略分析"],
            "porter-five-forces": ["五力", "porter", "行业分析", "竞争"],
            "balanced-scorecard": ["平衡计分卡", "bsc", "kpi", "绩效"],
            "business-model": ["商业模式", "business model", "画布", "canvas"],
            "change-management": ["变革管理", "change", "转型", "kotter"],
            "design-thinking": ["设计思维", "design thinking", "创新", "ideation"],
        }

        # 匹配
        for skill_id, keywords in keywords_map.items():
            for keyword in keywords:
                if keyword in user_lower:
                    return skill_id, {"matched_keyword": keyword}

        # 模糊匹配：研究领域
        field_map = {
            "管理学": ["grounded-theory", "case-study", "action-research"],
            "商学": ["business-model", "swot-analysis", "porter-five-forces"],
            "社会学": [
                "social-network-analysis",
                "bourdieu-field-analysis",
                "digital-marxism",
            ],
            "教育学": ["multilevel-modeling", "ethnography", "action-research"],
            "心理学": ["sem-analysis", "factor-analysis", "phenomenology"],
            "传播学": ["content-analysis", "discourse-analysis", "narrative-analysis"],
            "政治学": ["did-analysis", "qca-analysis", "social-network-analysis"],
            "经济学": ["regression-analysis", "did-analysis", "meta-analysis"],
        }

        for field, skills in field_map.items():
            if field in user_lower:
                return skills[0], {"matched_field": field, "alternatives": skills}

        return None, {"intent": "unknown"}

    def create_soul_agent(
        self, skill_id: str, custom_name: Optional[str] = None, verbose: bool = True
    ) -> dict:
        """
        创建Soul Agent分身

        Returns:
            {
                'soul_id': str,
                'display_name': str,
                'path': str,
                'skill': str,
                'master': str
            }
        """
        agents = self._get_all_agents()
        if skill_id not in agents:
            raise ValueError(f"未知的分身ID: {skill_id}")

        meta = agents[skill_id]

        # 生成Soul ID
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        name_part = (custom_name or meta["name"])[:10].replace(" ", "_")
        soul_id = f"soul_{skill_id}_{timestamp}"
        display_name = custom_name or meta["name"]

        # 创建目录
        soul_dir = self.storage_root / soul_id
        soul_dir.mkdir(parents=True, exist_ok=True)

        # 创建子目录
        for subdir in [
            "memory",
            "memory/lessons",
            "memory/patterns",
            "evolution",
            "cases",
            "cases/positive",
            "cases/negative",
            "templates",
            "logs",
            "data",
            "results",
        ]:
            (soul_dir / subdir).mkdir(parents=True, exist_ok=True)

        if verbose:
            print(f"\n🦞 创建分身: {display_name}")
            print(f"   对标学者: {meta['master']}")
            print(f"   路径: {soul_dir}")

        # 生成SOUL.md
        soul_md = self._generate_soul_md(skill_id, soul_id, display_name, meta)
        (soul_dir / "SOUL.md").write_text(soul_md, encoding="utf-8")

        # 生成SOUL_CONFIG.yaml
        config_yaml = self._generate_config_yaml(soul_id, skill_id, display_name, meta)
        (soul_dir / "SOUL_CONFIG.yaml").write_text(config_yaml, encoding="utf-8")

        # 生成METHODOLOGY.md
        methodology_md = self._generate_methodology_md(skill_id, display_name, meta)
        (soul_dir / "METHODOLOGY.md").write_text(methodology_md, encoding="utf-8")

        # 生成README.md
        readme_md = self._generate_readme_md(soul_id, display_name, meta, soul_dir)
        (soul_dir / "README.md").write_text(readme_md, encoding="utf-8")

        # 初始化记忆文件
        self._initialize_memory(soul_dir, display_name)

        # 保存元数据
        metadata = {
            "soul_id": soul_id,
            "skill_id": skill_id,
            "display_name": display_name,
            "created": datetime.now().isoformat(),
            "version": "1.0.0",
            "master": meta["master"],
            "methodology": meta["name"],
            "category": self._get_category_for_skill(skill_id),
            "path": str(soul_dir),
            "status": "active",
        }
        (soul_dir / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        if verbose:
            print(f"   ✅ 分身创建成功!")

        return {
            "soul_id": soul_id,
            "display_name": display_name,
            "path": str(soul_dir),
            "skill": skill_id,
            "master": meta["master"],
        }

    def _get_category_for_skill(self, skill_id: str) -> str:
        """获取技能所属类别"""
        for category, info in self.metadata.items():
            if category.startswith("_"):
                continue
            if "agents" in info and skill_id in info["agents"]:
                return category
        return "unknown"

    def _generate_soul_md(
        self, skill_id: str, soul_id: str, display_name: str, meta: dict
    ) -> str:
        """生成SOUL.md内容"""
        prohibitions = meta.get("prohibitions", [])
        prohibitions_text = "\n".join([f"  - {p}" for p in prohibitions[:5]])

        return f"""---
name: {soul_id}
version: 1.0.0
created: {datetime.now().strftime("%Y-%m-%d")}
author: SocienceAI Soul Agent System

alignment:
  master: "{meta["master"]}"
  school: "{meta["school"]}"
  philosophy: "{meta["philosophy"]}"
  paradigm: "{meta["paradigm"]}"

personality:
  traits:
    - 学术严谨
    - 方法论精准
    - 开放性思维
  communication:
    style: 学术规范
    tone: 专业严谨

values:
  academic_integrity: 学术诚信是底线，绝不妥协
  methodological_rigor: 方法论严谨性是质量保证
  transparency: 研究过程完全透明可追溯
  evidence_based: 一切结论基于数据证据

academic_discipline:
  field: "{meta.get("paradigm", "社会科学")}"
  methodology: "{meta["name"]}"

core_prohibitions:
{prohibitions_text}

evolution:
  enabled: true
  auto_evolve: true
  storage: "~/.stigmergy/soul-state/{soul_id}/"

status:
  active: true
  tasks_completed: 0
  quality_score: 0.0
---

# {display_name}

## 关于我

我是 **{display_name}**，灵魂对齐 **{meta["master"]}** 的学术思想。

### 学术渊源

- **对标学者**: {meta["master"]}
- **学术流派**: {meta["school"]}
- **哲学立场**: {meta["philosophy"]}

### 我的使命

让 **{meta["name"]}** 研究方法更加：
- ✅ 严谨规范
- ✅ 透明可追溯
- ✅ 易于应用
- ✅ 持续进化

## ⛔ 绝对禁止原则

> 违反以下原则将导致分析结果无效

{self._format_prohibitions(prohibitions)}

## ✅ 承诺书

**本人（{display_name}）郑重承诺**：

1. 严格遵守上述所有"绝对禁止"原则
2. 绝不以效率牺牲质量
3. 绝不未验证就报告完成
4. 绝不追求数量牺牲深度
5. 绝不一知半解就应用方法

## 当前状态

| 指标 | 数值 |
|------|------|
| 已完成任务 | 0 |
| 质量评分 | 0/100 |
| 活跃状态 | ✅ 可接受任务 |

---

*由 Soul Agent Creator 自动生成 | {datetime.now().strftime("%Y-%m-%d")}*
"""

    def _format_prohibitions(self, prohibitions: List[str]) -> str:
        """格式化禁止原则"""
        lines = []
        for i, p in enumerate(prohibitions[:5], 1):
            lines.append(f"### 禁止{i}: {p.split('，')[0] if '，' in p else p}")
            lines.append(f"{p}")
            lines.append("")
        return "\n".join(lines)

    def _generate_config_yaml(
        self, soul_id: str, skill_id: str, display_name: str, meta: dict
    ) -> str:
        """生成SOUL_CONFIG.yaml"""
        return f"""# Soul Agent 配置
# {display_name}

general:
  soul_id: "{soul_id}"
  name: "{display_name}"
  version: "1.0.0"
  language: "zh-CN"

storage:
  root: "~/.stigmergy/soul-agents"
  state: "~/.stigmergy/soul-state/{soul_id}"
  memory: "~/.stigmergy/soul-state/{soul_id}/memory"

behavior:
  execution:
    auto_start: true
    break_down_tasks: true
  quality:
    enforce_prohibitions: true
    strict_mode: true
    verify_before_report: true
  evolution:
    enabled: true
    auto_evolve: true
    evolve_after_tasks: 10

integrations:
  openclaw:
    enabled: true
    soul_evolution: true
"""

    def _generate_methodology_md(
        self, skill_id: str, display_name: str, meta: dict
    ) -> str:
        """生成METHODOLOGY.md"""
        key_works = meta.get("key_works", [])
        works_text = "\n".join([f"- {w}" for w in key_works])

        applications = meta.get("applications", [])
        apps_text = "\n".join([f"- {a}" for a in applications])

        return f"""# {display_name} - 方法论核心

## 理论渊源

**代表学者**: {meta["master"]}

**学术流派**: {meta["school"]}

**核心范式**: {meta["philosophy"]}

### 代表作

{works_text}

## 适用场景

{apps_text}

## 核心禁止原则

{meta.get("prohibitions", ["无特定禁止原则"])}

---

*由 Soul Agent Creator 生成 | {datetime.now().strftime("%Y-%m-%d")}*
"""

    def _generate_readme_md(
        self, soul_id: str, display_name: str, meta: dict, soul_dir: Path
    ) -> str:
        """生成README.md"""
        return f"""# {display_name}

> Soul Agent 分身 - {meta["master"]} 方法论

## 快速开始

```bash
# 设置环境变量激活分身
export SOUL_AGENT_ID="{soul_id}"

# 或在OpenClaw中说
"使用 {display_name} 帮我分析数据"
```

## 配置

详细配置请查看: [SOUL_CONFIG.yaml](SOUL_CONFIG.yaml)

## 目录结构

```
{soul_dir.name}/
├── SOUL.md           # 灵魂身份
├── SOUL_CONFIG.yaml  # 配置文件
├── METHODOLOGY.md    # 方法论
├── metadata.json     # 元数据
├── memory/          # 记忆系统
├── evolution/       # 进化记录
└── cases/          # 案例库
```

---
*由 Soul Agent Creator 生成*
"""

    def _initialize_memory(self, soul_dir: Path, display_name: str):
        """初始化记忆文件"""
        now = datetime.now().strftime("%Y-%m-%d")

        # 教训记忆
        lessons_init = f"""# 教训记忆 - {display_name}

## 记录格式

```markdown
## [日期] 教训标题
### 问题 / 原因 / 教训 / 防止措施
```

## 历史记录

暂无记录

*初始化: {now}*
"""
        (soul_dir / "memory" / "lessons" / "README.md").write_text(
            lessons_init, encoding="utf-8"
        )

        # 成功模式
        patterns_init = f"""# 成功模式 - {display_name}

## 记录格式

```markdown
## 模式名称
### 适用场景 / 执行步骤 / 成功案例 / 关键要点
```

## 模式库

暂无记录

*初始化: {now}*
"""
        (soul_dir / "memory" / "patterns" / "README.md").write_text(
            patterns_init, encoding="utf-8"
        )

        # 进化日志
        evolution_init = f"""# 进化日志 - {display_name}

| 日期 | 事件 | 经验值 |
|------|------|--------|
| {now} | Soul创建 | +0 |

---
*初始化: {now}*
"""
        (soul_dir / "evolution" / "log.md").write_text(evolution_init, encoding="utf-8")

    def list_agents(self) -> List[dict]:
        """列出所有可用的分身"""
        agents = self._get_all_agents()
        result = []

        for skill_id, meta in agents.items():
            result.append(
                {
                    "skill_id": skill_id,
                    "name": meta["name"],
                    "master": meta["master"],
                    "applications": meta.get("applications", [])[:2],
                    "download_size": meta.get("download_size", "N/A"),
                }
            )

        return result

    def recommend_agents(self, user_profile: str) -> List[dict]:
        """根据用户画像推荐分身"""
        agents = self._get_all_agents()
        recommendations = []

        user_lower = user_profile.lower()

        # 分析关键词
        for skill_id, meta in agents.items():
            score = 0
            reasons = []

            # 名称匹配
            if meta["name"].lower() in user_lower:
                score += 10
                reasons.append(f"名称匹配: {meta['name']}")

            # 关键词匹配
            for keyword in meta.get("applications", []):
                if keyword.lower() in user_lower:
                    score += 5
                    reasons.append(f"应用匹配: {keyword}")

            # 大师名匹配
            if meta["master"].lower().split()[0] in user_lower:
                score += 8
                reasons.append(f"学者匹配: {meta['master']}")

            if score > 0:
                recommendations.append(
                    {
                        "skill_id": skill_id,
                        "name": meta["name"],
                        "master": meta["master"],
                        "score": score,
                        "reasons": reasons,
                    }
                )

        # 按分数排序
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:5]


# ============================================================================
# 主程序
# ============================================================================


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Soul Agent Creator")
    parser.add_argument("--skill", "-s", help="指定分身ID")
    parser.add_argument("--name", "-n", help="自定义分身名称")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有分身")
    parser.add_argument("--recommend", "-r", help="根据用户画像推荐")

    args = parser.parse_args()

    creator = SoulAgentCreator()

    if args.list:
        print("\n📚 可用的研究分身:\n")
        for agent in creator.list_agents():
            print(f"  • {agent['skill_id']:30} - {agent['name']} ({agent['master']})")
        return

    if args.recommend:
        print(f"\n🎯 根据您的描述: '{args.recommend}'")
        print("推荐分身:\n")
        for i, agent in enumerate(creator.recommend_agents(args.recommend), 1):
            print(f"  {i}. {agent['name']} (分数: {agent['score']})")
            print(f"     对标: {agent['master']}")
            print(f"     原因: {', '.join(agent['reasons'][:2])}")
            print()
        return

    if args.interactive:
        print("\n🦞 Soul Agent Creator - 交互式创建")
        print("\n请告诉我您的研究需求，或输入分身ID直接创建。")
        user_input = input("\n您的需求: ").strip()

        if not user_input:
            print("未输入任何内容")
            return

        # 理解意图
        skill_id, analysis = creator.understand_request(user_input)

        if skill_id:
            confirm = input(f"\n是否创建分身 '{skill_id}'? (y/n): ").strip().lower()
            if confirm == "y":
                name = input("分身名称（直接回车使用默认）: ").strip() or None
                result = creator.create_soul_agent(skill_id, name)
                print(f"\n✅ 创建成功! Soul ID: {result['soul_id']}")
        else:
            print("\n未能识别您的需求。请尝试:")
            print("  - 直接输入分身ID，如: grounded-theory")
            print("  - 使用 --list 查看所有可用分身")
        return

    if args.skill:
        result = creator.create_soul_agent(args.skill, args.name)
        print(f"\n✅ 分身创建成功!")
        print(f"   Soul ID: {result['soul_id']}")
        print(f"   路径: {result['path']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
