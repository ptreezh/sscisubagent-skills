#!/usr/bin/env python3
"""
生成 Soul Agent 配置文件

用法:
    from tools import generate_soul_config
    result = generate_soul_config.create(
        skill_id="grounded-theory",
        custom_name="我的扎根理论助手",
        output_dir="~/.stigmergy/soul-agents/"
    )
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from .list_skills import get_skill, SKILLS_METADATA


def load_template(template_name: str) -> str:
    """加载模板文件"""
    template_dir = Path(__file__).parent.parent / "templates"
    template_path = template_dir / template_name
    
    if not template_path.exists():
        raise FileNotFoundError(f"模板文件不存在：{template_path}")
    
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def generate_soul_id(skill_id: str, custom_name: str = None) -> str:
    """生成 Soul ID"""
    if custom_name:
        name_part = "".join(c for c in custom_name if c.isalnum())[:10].lower()
    else:
        name_part = skill_id.replace("-", "")[:10]
    
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"soul_{name_part}_{timestamp}"


def fill_soul_template(skill_id: str, meta: Dict, custom_name: str = None) -> str:
    """填充 SOUL.md 模板"""
    template = load_template("SOUL.md.template")
    soul_id = generate_soul_id(skill_id, custom_name)
    display_name = custom_name or meta["name"]
    created_date = datetime.now().strftime("%Y-%m-%d")
    
    replacements = {
        "{SOUL_ID}": soul_id,
        "{SOUL_NAME}": soul_id,
        "{SOUL_DISPLAY_NAME}": display_name,
        "{CREATED_DATE}": created_date,
        "{METHODOLOGY}": meta["name"],
        "{METHODOLOGY_MASTER}": meta["master"],
        "{METHODOLOGY_SCHOOL}": meta["school"],
        "{PARADIGM}": meta["philosophy"],
        "{FIELD}": meta["category"],
        "{SUBFIELD}": meta["name"],
        "{KEY_WORK_1}": meta["key_works"][0] if meta["key_works"] else "",
        "{KEY_WORK_2}": meta["key_works"][1] if len(meta["key_works"]) > 1 else "",
        "{TRAIT_1}": "学术严谨",
        "{TRAIT_2}": "方法论精准",
        "{TRAIT_3}": "开放性思维",
        "{COMMUNICATION_STYLE}": "学术规范",
        "{TONE}": "专业严谨",
        "{COGNITIVE_APPROACH}": "证据驱动",
        "{THINKING_PATTERN}": "归纳与演绎结合",
        "{PROHIBITION_1_NAME}": meta["prohibitions"][0][0] if len(meta["prohibitions"]) > 0 else "",
        "{PROHIBITION_1_DESC}": meta["prohibitions"][0][1] if len(meta["prohibitions"]) > 0 else "",
        "{PROHIBITION_2_NAME}": meta["prohibitions"][1][0] if len(meta["prohibitions"]) > 1 else "",
        "{PROHIBITION_2_DESC}": meta["prohibitions"][1][1] if len(meta["prohibitions"]) > 1 else "",
        "{PROHIBITION_3_NAME}": meta["prohibitions"][2][0] if len(meta["prohibitions"]) > 2 else "",
        "{PROHIBITION_3_DESC}": meta["prohibitions"][2][1] if len(meta["prohibitions"]) > 2 else "",
        "{ANALYSIS_TYPE_1}": meta["applications"][0] if len(meta["applications"]) > 0 else "",
        "{ANALYSIS_TYPE_2}": meta["applications"][1] if len(meta["applications"]) > 1 else "",
        "{ANALYSIS_TYPE_3}": meta["applications"][2] if len(meta["applications"]) > 2 else "",
        "{APPLICATION_1}": meta["applications"][0] if len(meta["applications"]) > 0 else "",
        "{APPLICATION_2}": meta["applications"][1] if len(meta["applications"]) > 1 else "",
        "{APPLICATION_3}": meta["applications"][2] if len(meta["applications"]) > 2 else "",
        "{SKILL_1}": f"{skill_id}-expert",
        "{SKILL_2}": "academic-writing",
        "{VERSION}": "1.0.0",
    }
    
    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)
    
    return result


def fill_config_template(skill_id: str, meta: Dict, custom_name: str = None) -> str:
    """填充 SOUL_CONFIG.yaml 模板"""
    template = load_template("SOUL_CONFIG.yaml.template")
    soul_id = generate_soul_id(skill_id, custom_name)
    display_name = custom_name or meta["name"]
    
    replacements = {
        "{SOUL_ID}": soul_id,
        "{SOUL_NAME}": soul_id,
        "{SOUL_DISPLAY_NAME}": display_name,
        "{METHODOLOGY}": meta["name"],
        "{ANALYSIS_TYPE_1}": meta["applications"][0] if len(meta["applications"]) > 0 else "",
        "{ANALYSIS_TYPE_2}": meta["applications"][1] if len(meta["applications"]) > 1 else "",
        "{ANALYSIS_TYPE_3}": meta["applications"][2] if len(meta["applications"]) > 2 else "",
        "{SKILL_1}": f"{skill_id}-expert",
        "{SKILL_2}": "academic-writing",
    }
    
    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)
    
    return result


def fill_methodology_template(skill_id: str, meta: Dict) -> str:
    """填充 METHODOLOGY.md 模板"""
    template = load_template("METHODOLOGY.md.template")
    created_date = datetime.now().strftime("%Y-%m-%d")
    
    replacements = {
        "{METHODOLOGY_NAME}": meta["name"],
        "{METHODOLOGY_MASTER}": meta["master"],
        "{METHODOLOGY_SCHOOL}": meta["school"],
        "{PARADIGM}": meta["philosophy"],
        "{KEY_WORK_1}": meta["key_works"][0] if meta["key_works"] else "",
        "{KEY_WORK_2}": meta["key_works"][1] if len(meta["key_works"]) > 1 else "",
        "{CONCEPT_1}": meta["concepts"][0][0] if len(meta["concepts"]) > 0 else "",
        "{CONCEPT_1_DEFINITION}": meta["concepts"][0][1] if len(meta["concepts"]) > 0 else "",
        "{CONCEPT_2}": meta["concepts"][1][0] if len(meta["concepts"]) > 1 else "",
        "{CONCEPT_2_DEFINITION}": meta["concepts"][1][1] if len(meta["concepts"]) > 1 else "",
        "{CONCEPT_3}": meta["concepts"][2][0] if len(meta["concepts"]) > 2 else "",
        "{CONCEPT_3_DEFINITION}": meta["concepts"][2][1] if len(meta["concepts"]) > 2 else "",
        "{PROHIBITION_1}": meta["prohibitions"][0][0] if len(meta["prohibitions"]) > 0 else "",
        "{PROHIBITION_1_DESC}": meta["prohibitions"][0][1] if len(meta["prohibitions"]) > 0 else "",
        "{PROHIBITION_2}": meta["prohibitions"][1][0] if len(meta["prohibitions"]) > 1 else "",
        "{PROHIBITION_2_DESC}": meta["prohibitions"][1][1] if len(meta["prohibitions"]) > 1 else "",
        "{PROHIBITION_3}": meta["prohibitions"][2][0] if len(meta["prohibitions"]) > 2 else "",
        "{PROHIBITION_3_DESC}": meta["prohibitions"][2][1] if len(meta["prohibitions"]) > 2 else "",
        "{APPLICATION_1}": meta["applications"][0] if len(meta["applications"]) > 0 else "",
        "{APPLICATION_2}": meta["applications"][1] if len(meta["applications"]) > 1 else "",
        "{APPLICATION_3}": meta["applications"][2] if len(meta["applications"]) > 2 else "",
        "{CREATED_DATE}": created_date,
    }
    
    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)
    
    return result


def generate_readme(skill_id: str, meta: Dict, soul_id: str, custom_name: str = None) -> str:
    """生成 README.md"""
    display_name = custom_name or meta["name"]
    created_date = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# {display_name}

> Soul Agent - {meta["name"]}分身

## 关于

本分身对标 **{meta["master"]}** 的 **{meta["name"]}** 方法论，
严格遵守学术规范，支持自主进化。

## 快速开始

```bash
# 在 OpenClaw 中激活本分身
# 设置环境变量
export SOUL_AGENT_ID="{soul_id}"

# 或直接指定配置文件
opencode --soul-config ~/.stigmergy/soul-agents/{soul_id}/SOUL.md
```

## 配置

详细配置请查看：[SOUL_CONFIG.yaml](SOUL_CONFIG.yaml)

## 进化历史

| 日期 | 事件 |
|------|------|
| {created_date} | Soul Agent 创建 |

## 目录结构

```
{soul_id}/
├── SOUL.md           # 灵魂身份定义
├── SOUL_CONFIG.yaml  # 配置文件
├── METHODOLOGY.md    # 方法论文档
├── memory/           # 记忆系统
│   ├── lessons/      # 教训记忆
│   └── patterns/     # 成功模式
├── evolution/        # 进化记录
├── cases/           # 案例库
│   ├── positive/    # 正面案例
│   └── negative/    # 负面案例
├── templates/       # 工作模板
├── logs/           # 日志
├── data/           # 数据
└── results/        # 结果
```

---
*由 SocienceAI Soul Agent Creator 生成 | {created_date}*
"""


def create(
    skill_id: str,
    custom_name: str = None,
    output_dir: str = None,
    verbose: bool = True
) -> Dict:
    """创建 Soul Agent 分身"""
    
    if skill_id not in SKILLS_METADATA:
        raise ValueError(f"未知的技能 ID: {skill_id}")
    
    meta = SKILLS_METADATA[skill_id]
    soul_id = generate_soul_id(skill_id, custom_name)
    display_name = custom_name or meta["name"]
    created_date = datetime.now().strftime("%Y-%m-%d")
    
    # 确定输出目录
    if output_dir is None:
        output_dir = Path.home() / ".stigmergy" / "soul-agents"
    else:
        output_dir = Path(output_dir)
    
    soul_dir = output_dir / soul_id
    
    # 创建目录结构
    dirs_to_create = [
        soul_dir,
        soul_dir / "memory",
        soul_dir / "memory" / "lessons",
        soul_dir / "memory" / "patterns",
        soul_dir / "evolution",
        soul_dir / "cases",
        soul_dir / "cases" / "positive",
        soul_dir / "cases" / "negative",
        soul_dir / "templates",
        soul_dir / "logs",
        soul_dir / "data",
        soul_dir / "results",
    ]
    
    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
    
    if verbose:
        print(f"\n📁 创建目录结构：{soul_dir}")
    
    # 生成并保存文件
    files_to_generate = [
        ("SOUL.md", fill_soul_template(skill_id, meta, custom_name)),
        ("SOUL_CONFIG.yaml", fill_config_template(skill_id, meta, custom_name)),
        ("METHODOLOGY.md", fill_methodology_template(skill_id, meta)),
        ("README.md", generate_readme(skill_id, meta, soul_id, custom_name)),
    ]
    
    for filename, content in files_to_generate:
        output_path = soul_dir / filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        if verbose:
            print(f"  ✅ 创建：{filename}")
    
    # 生成初始化文件
    lessons_init = f"""# 教训记忆 - {display_name}

> 记录分析过程中的教训和错误

## 记录格式

```markdown
## [日期] 教训标题

### 问题
描述遇到的问题

### 原因
根本原因分析

### 教训
从中学到的经验

### 防止措施
如何避免再次发生
```

## 历史记录

暂无记录

---
*初始化：{created_date}*
"""
    
    patterns_init = f"""# 成功模式 - {display_name}

> 记录成功的分析模式和最佳实践

## 记录格式

```markdown
## 模式名称

### 适用场景
何时使用此模式

### 执行步骤
具体操作步骤

### 成功案例
相关案例引用

### 关键要点
核心成功因素
```

## 模式库

暂无记录

---
*初始化：{created_date}*
"""
    
    evolution_init = f"""# 进化日志 - {display_name}

> 记录 Soul Agent 的进化历史

## 进化事件

| 日期 | 事件类型 | 描述 | 经验值变化 |
|------|----------|------|------------|
| {created_date} | 创建 | Soul Agent 初始化 | +0 |

## 统计

- 总进化次数：0
- 总经验值：0
- 最高质量评分：0

---
*初始化：{created_date}*
"""
    
    with open(soul_dir / "memory" / "lessons" / "README.md", "w", encoding="utf-8") as f:
        f.write(lessons_init)
    
    with open(soul_dir / "memory" / "patterns" / "README.md", "w", encoding="utf-8") as f:
        f.write(patterns_init)
    
    with open(soul_dir / "evolution" / "log.md", "w", encoding="utf-8") as f:
        f.write(evolution_init)
    
    if verbose:
        print(f"  ✅ 创建：memory/ & evolution/")
    
    # 生成元数据文件
    import json
    metadata = {
        "soul_id": soul_id,
        "skill_id": skill_id,
        "display_name": display_name,
        "created": created_date,
        "version": "1.0.0",
        "master": meta["master"],
        "methodology": meta["name"],
        "category": meta["category"],
        "storage_path": str(soul_dir),
        "status": "active",
    }
    
    metadata_path = soul_dir / "metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    if verbose:
        print(f"  ✅ 创建：metadata.json")
    
    return {
        "soul_id": soul_id,
        "display_name": display_name,
        "output_dir": str(soul_dir),
        "skill": skill_id,
        "master": meta["master"],
        "files": [f[0] for f in files_to_generate] + ["memory/", "evolution/", "metadata.json"],
    }
