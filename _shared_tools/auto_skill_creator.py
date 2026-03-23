#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新技能自动创建系统 - Auto Skill Creator
自动执行技能创建流程，支持断点恢复

使用方法:
    python auto_skill_creator.py              # 继续当前任务
    python auto_skill_creator.py --skill thematic-analysis-expert  # 指定技能
    python auto_skill_creator.py --batch 1    # 执行第一批
    python auto_skill_creator.py --status     # 查看状态
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 跨平台路径处理
BASE_DIR = Path(__file__).parent.parent.absolute()
SKILLS_DIR = BASE_DIR / "agentskills"
MASTER_PLAN = SKILLS_DIR / "NEW_SKILLS_MASTER_PLAN.md"
SHARED_TOOLS = SKILLS_DIR / "_shared_tools"

# 技能批次定义
SKILL_BATCHES = {
    1: [  # 核心技能
        "thematic-analysis-expert",
        "meta-analysis-expert",
        "sem-analysis-expert",
        "regression-analysis-expert",
        "content-analysis-expert",
    ],
    2: [  # 高频技能
        "rct-experimental-design-expert",
        "discourse-analysis-expert",
        "ethnography-expert",
        "factor-analysis-expert",
        "mixed-methods-expert",
        "case-study-expert",
    ],
    3: [  # 常用技能
        "ipa-analysis-expert",
        "narrative-analysis-expert",
        "phenomenology-expert",
        "multilevel-modeling-expert",
        "longitudinal-analysis-expert",
        "action-research-expert",
    ],
    4: [  # 新兴方法
        "nlp-text-mining-expert",
        "machine-learning-research-expert",
        "bibliometric-analysis-expert",
        "social-sequence-analysis-expert",
    ],
}

# 技能元数据
SKILL_METADATA = {
    "thematic-analysis-expert": {
        "name_zh": "主题分析专家",
        "priority": 3,
        "description": "主题分析(Thematic Analysis)专家技能，基于Braun & Clarke方法论，提供六步骤分析流程：熟悉数据、生成初始代码、搜索主题、审查主题、定义命名主题、撰写报告。适用于访谈、焦点小组、开放式问卷等质性数据分析。",
        "keywords": ["主题分析", "质性研究", "编码", "Braun Clarke", "访谈分析"],
    },
    "meta-analysis-expert": {
        "name_zh": "元分析专家",
        "priority": 3,
        "description": "元分析(Meta-Analysis)专家技能，提供系统综述和统计整合方法。支持效应量计算、异质性检验、发表偏倚检验、亚组分析、敏感性分析。适用于循证研究、系统综述、研究整合。",
        "keywords": ["元分析", "系统综述", "效应量", "异质性", "循证研究"],
    },
    "sem-analysis-expert": {
        "name_zh": "结构方程模型专家",
        "priority": 3,
        "description": "结构方程模型(SEM)专家技能，整合因子分析和回归分析。支持测量模型验证、结构模型估计、模型拟合评估、中介效应分析、多组比较。适用于复杂变量关系研究、量表验证、路径分析。",
        "keywords": ["结构方程模型", "SEM", "验证性因子分析", "路径分析", "中介效应"],
    },
    "regression-analysis-expert": {
        "name_zh": "回归分析专家",
        "priority": 3,
        "description": "回归分析(Regression Analysis)专家技能，提供全面的回归分析方法。支持线性回归、逻辑回归、多元回归、逐步回归、正则化回归、诊断检验。适用于因果推断、预测建模、关系检验。",
        "keywords": ["回归分析", "线性回归", "逻辑回归", "预测建模", "因果推断"],
    },
    "content-analysis-expert": {
        "name_zh": "内容分析专家",
        "priority": 3,
        "description": "内容分析(Content Analysis)专家技能，提供系统性文本分析方法。支持编码方案设计、信度检验、频率分析、语义分析、比较分析。适用于媒体研究、传播学、文本挖掘。",
        "keywords": ["内容分析", "文本分析", "编码方案", "媒体研究", "传播学"],
    },
    "rct-experimental-design-expert": {
        "name_zh": "实验设计与RCT专家",
        "priority": 2,
        "description": "随机对照试验(RCT)与实验设计专家技能。支持实验设计、随机化方案、样本量计算、盲法设计、偏倚控制、效应评估。适用于因果推断、干预研究、政策评估。",
        "keywords": ["RCT", "实验设计", "随机对照", "因果推断", "干预研究"],
    },
    "discourse-analysis-expert": {
        "name_zh": "话语分析专家",
        "priority": 2,
        "description": "话语分析(Discourse Analysis)专家技能。支持批判话语分析、会话分析、话语心理学、多模态话语分析。适用于语言学研究、政治话语、媒体分析。",
        "keywords": ["话语分析", "批判话语", "会话分析", "语言学", "权力分析"],
    },
    "ethnography-expert": {
        "name_zh": "民族志专家",
        "priority": 2,
        "description": "民族志(Ethnography)专家技能。支持田野调查设计、参与观察、深度访谈、文化描述、理论建构。适用于人类学、社会学、组织研究。",
        "keywords": ["民族志", "田野调查", "参与观察", "文化研究", "人类学"],
    },
    "factor-analysis-expert": {
        "name_zh": "因子分析专家",
        "priority": 2,
        "description": "因子分析(Factor Analysis)专家技能。支持探索性因子分析、验证性因子分析、主成分分析、旋转方法、因子得分。适用于量表开发、构念验证、数据降维。",
        "keywords": ["因子分析", "EFA", "CFA", "量表开发", "数据降维"],
    },
    "mixed-methods-expert": {
        "name_zh": "混合方法研究专家",
        "priority": 2,
        "description": "混合方法研究(Mixed Methods)专家技能。支持汇聚设计、解释序列设计、探索序列设计、嵌入式设计、整合分析。适用于复杂研究问题、全面理解现象。",
        "keywords": ["混合方法", "量化质性整合", "汇聚设计", "序列设计"],
    },
    "case-study-expert": {
        "name_zh": "案例研究专家",
        "priority": 2,
        "description": "案例研究(Case Study)专家技能，基于Yin方法论。支持单案例/多案例设计、案例选择、证据三角验证、模式匹配、逻辑模型。适用于深度理解现象、理论建构。",
        "keywords": ["案例研究", "Yin", "三角验证", "模式匹配", "理论建构"],
    },
    "ipa-analysis-expert": {
        "name_zh": "解释现象学分析专家",
        "priority": 1,
        "description": "解释现象学分析(IPA)专家技能。支持双阶段解释、主题发展、个人体验分析、意义建构。适用于健康心理学、生活体验研究。",
        "keywords": ["IPA", "现象学", "生活体验", "解释性分析", "健康心理学"],
    },
    "narrative-analysis-expert": {
        "name_zh": "叙事分析专家",
        "priority": 1,
        "description": "叙事分析(Narrative Analysis)专家技能。支持故事结构分析、叙事类型分析、生活史研究、叙事身份研究。适用于心理学、教育学、健康研究。",
        "keywords": ["叙事分析", "故事分析", "生活史", "叙事身份"],
    },
    "phenomenology-expert": {
        "name_zh": "现象学专家",
        "priority": 1,
        "description": "现象学(Phenomenology)研究专家技能。支持描述现象学、解释现象学、生活体验描述、本质还原。适用于存在体验研究、意义研究。",
        "keywords": ["现象学", "生活体验", "本质还原", "Husserl", "意义研究"],
    },
    "multilevel-modeling-expert": {
        "name_zh": "多层级模型专家",
        "priority": 1,
        "description": "多层级模型(HLM/MLM)专家技能。支持嵌套数据处理、随机效应模型、跨层级交互、增长曲线模型。适用于教育研究、组织研究、健康研究。",
        "keywords": ["HLM", "多层级", "嵌套数据", "随机效应", "增长曲线"],
    },
    "longitudinal-analysis-expert": {
        "name_zh": "纵向分析专家",
        "priority": 1,
        "description": "纵向数据分析专家技能。支持面板数据分析、时间序列分析、增长模型、事件史分析、潜变量增长模型。适用于发展研究、追踪研究。",
        "keywords": ["纵向分析", "面板数据", "时间序列", "增长模型", "追踪研究"],
    },
    "action-research-expert": {
        "name_zh": "行动研究专家",
        "priority": 1,
        "description": "行动研究(Action Research)专家技能。支持参与式行动研究、实践者研究、变革循环、协作研究。适用于教育改革、社区发展、组织变革。",
        "keywords": ["行动研究", "参与式研究", "实践者研究", "变革", "协作"],
    },
    "nlp-text-mining-expert": {
        "name_zh": "NLP文本挖掘专家",
        "priority": 0,
        "description": "自然语言处理与文本挖掘专家技能。支持情感分析、主题建模(LDA)、命名实体识别、文本分类、词向量分析。适用于社交媒体研究、舆情分析、文本挖掘。",
        "keywords": ["NLP", "文本挖掘", "情感分析", "主题建模", "LDA"],
    },
    "machine-learning-research-expert": {
        "name_zh": "机器学习研究方法专家",
        "priority": 0,
        "description": "机器学习研究方法专家技能。支持监督学习、无监督学习、特征工程、模型评估、交叉验证。适用于预测研究、分类研究、模式识别。",
        "keywords": ["机器学习", "预测建模", "分类", "聚类", "特征工程"],
    },
    "bibliometric-analysis-expert": {
        "name_zh": "文献计量分析专家",
        "priority": 0,
        "description": "文献计量分析专家技能。支持引文分析、共引分析、文献耦合、知识图谱、研究前沿识别。适用于科研评价、领域分析、知识发现。",
        "keywords": ["文献计量", "引文分析", "知识图谱", "VOSviewer", "CiteSpace"],
    },
    "social-sequence-analysis-expert": {
        "name_zh": "社会序列分析专家",
        "priority": 0,
        "description": "社会序列分析专家技能。支持生命历程分析、职业轨迹分析、最优匹配分析、序列可视化。适用于生命历程研究、职业研究、事件序列分析。",
        "keywords": ["序列分析", "生命历程", "职业轨迹", "最优匹配", "事件序列"],
    },
}


class AutoSkillCreator:
    """自动技能创建器"""
    
    def __init__(self):
        self.base_dir = BASE_DIR
        self.skills_dir = SKILLS_DIR
        self.current_skill = None
        self.current_step = 0
        
    def get_status(self) -> Dict:
        """获取当前状态"""
        status = {
            "total_skills": 21,
            "completed": 0,
            "in_progress": 0,
            "pending": 0,
            "skills": {}
        }
        
        for batch_num, skills in SKILL_BATCHES.items():
            for skill_name in skills:
                skill_dir = self.skills_dir / skill_name
                if skill_dir.exists():
                    task_plan = skill_dir / "TASK_PLAN.md"
                    if task_plan.exists():
                        content = task_plan.read_text(encoding='utf-8')
                        if "Step 6: 验证对齐 | complete" in content or "Step 6: 验证对齐|complete" in content:
                            status["completed"] += 1
                            status["skills"][skill_name] = "complete"
                        else:
                            status["in_progress"] += 1
                            status["skills"][skill_name] = "in_progress"
                            if not self.current_skill:
                                self.current_skill = skill_name
                    else:
                        status["pending"] += 1
                        status["skills"][skill_name] = "pending"
                        if not self.current_skill:
                            self.current_skill = skill_name
                else:
                    status["pending"] += 1
                    status["skills"][skill_name] = "pending"
                    if not self.current_skill:
                        self.current_skill = skill_name
        
        return status
    
    def create_skill_structure(self, skill_name: str) -> bool:
        """Step 1: 创建技能目录结构"""
        skill_dir = self.skills_dir / skill_name
        subdirs = ["prompts", "tools", "references", "test_data"]
        
        try:
            # 创建主目录
            skill_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建子目录
            for subdir in subdirs:
                (skill_dir / subdir).mkdir(exist_ok=True)
            
            print(f"✅ Step 1: 目录结构创建完成 - {skill_name}")
            return True
        except Exception as e:
            print(f"❌ Step 1 失败: {e}")
            return False
    
    def create_skill_md(self, skill_name: str) -> bool:
        """Step 2: 创建SKILL.md"""
        skill_dir = self.skills_dir / skill_name
        metadata = SKILL_METADATA.get(skill_name, {})
        
        skill_md_content = f'''---
name: {skill_name}
description: |
  {metadata.get("description", f"{skill_name}技能")}
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
  name-zh: "{metadata.get("name_zh", skill_name)}"
  priority: {metadata.get("priority", 1)}
  keywords: {json.dumps(metadata.get("keywords", []), ensure_ascii=False)}
---

# {metadata.get("name_zh", skill_name)}

## 技能概述

{metadata.get("description", f"{skill_name}技能描述待完善")}

## 核心能力

### 能力1: 分析框架
- 支持主流分析方法论
- 遵循学术规范
- 提供系统化流程

### 能力2: 质量保障
- 信度效度检验
- 过程透明化
- 结果可验证

### 能力3: 应用场景
- 学术研究
- 实践应用
- 教学培训

## 使用方法

### 基本调用
```
在AI CLI中激活此技能后，描述您的分析需求
```

### 分析流程
1. 数据准备
2. 方法选择
3. 分析执行
4. 结果解读
5. 报告撰写

## 理论基础

本技能基于相关学科的经典方法论和最新研究成果。

## 注意事项

- 确保数据质量
- 遵循伦理规范
- 保持方法论一致性

## 更新日志

- v5.0.0 (2026-03-15): 初始版本创建
'''
        
        try:
            (skill_dir / "SKILL.md").write_text(skill_md_content, encoding='utf-8')
            print(f"✅ Step 2a: SKILL.md创建完成 - {skill_name}")
            return True
        except Exception as e:
            print(f"❌ Step 2a 失败: {e}")
            return False
    
    def create_skill_yaml(self, skill_name: str) -> bool:
        """Step 2b: 创建skill.yaml"""
        skill_dir = self.skills_dir / skill_name
        metadata = SKILL_METADATA.get(skill_name, {})
        
        yaml_content = f'''# {metadata.get("name_zh", skill_name)}配置文件
name: {skill_name}
version: "5.0.0"
description: |
  {metadata.get("description", "")}

# 技能类型
type: research_methodology
category: social_science

# 优先级 (3=最高, 2=高, 1=中, 0=新兴)
priority: {metadata.get("priority", 1)}

# 关键词
keywords: {json.dumps(metadata.get("keywords", []), ensure_ascii=False)}

# 支持的分析类型
analysis_types:
  - exploratory
  - confirmatory
  - descriptive
  - inferential

# 输入格式
input_formats:
  - text
  - json
  - csv

# 输出格式
output_formats:
  - markdown
  - json
  - html

# 依赖
dependencies:
  python: ">=3.8"
  packages:
    - numpy
    - pandas

# 子智能体
subagents: []

# 工具函数
tools: []

# 提示词模板
prompts:
  system: prompts/system-prompt.md

# 参考文档
references:
  - references/detailed-guide.md
'''
        
        try:
            (skill_dir / "skill.yaml").write_text(yaml_content, encoding='utf-8')
            print(f"✅ Step 2b: skill.yaml创建完成 - {skill_name}")
            return True
        except Exception as e:
            print(f"❌ Step 2b 失败: {e}")
            return False
    
    def create_subagents_yaml(self, skill_name: str) -> bool:
        """Step 2c: 创建subagents.yaml"""
        skill_dir = self.skills_dir / skill_name
        
        yaml_content = f'''# {skill_name} 子智能体配置

# 方法论专家
methodology_expert:
  name: 方法论专家
  role: 提供方法论指导和规范检验
  prompts:
    - prompts/system-prompt.md

# 数据分析专家
analysis_expert:
  name: 分析专家
  role: 执行核心分析任务
  prompts:
    - prompts/system-prompt.md

# 质量控制专家
quality_expert:
  name: 质量控制专家
  role: 检验分析质量和结果可靠性
  prompts:
    - prompts/system-prompt.md
'''
        
        try:
            (skill_dir / "subagents.yaml").write_text(yaml_content, encoding='utf-8')
            print(f"✅ Step 2c: subagents.yaml创建完成 - {skill_name}")
            return True
        except Exception as e:
            print(f"❌ Step 2c 失败: {e}")
            return False
    
    def create_system_prompt(self, skill_name: str) -> bool:
        """Step 3: 创建系统提示词"""
        skill_dir = self.skills_dir / skill_name
        metadata = SKILL_METADATA.get(skill_name, {})
        
        prompt_content = f'''# {metadata.get("name_zh", skill_name)} - 系统提示词

## 角色定义

你是一位专业的{metadata.get("name_zh", skill_name)}，具备深厚的{metadata.get("keywords", ["研究"])[0] if metadata.get("keywords") else "研究"}方法论素养和丰富的实践经验。

## 核心职责

1. **方法论指导**: 提供规范的研究方法论指导
2. **分析执行**: 系统化执行分析流程
3. **质量保障**: 确保分析过程的严谨性和结果的可靠性
4. **结果解释**: 清晰解释分析结果的理论意义和实践价值

## 分析流程

### 阶段1: 问题界定
- 明确研究问题
- 确定分析目标
- 选择适当方法

### 阶段2: 数据准备
- 数据质量评估
- 数据清洗处理
- 数据结构整理

### 阶段3: 分析执行
- 遵循方法论规范
- 系统化执行步骤
- 记录分析过程

### 阶段4: 结果解读
- 统计/理论解释
- 意义建构
- 局限性说明

### 阶段5: 报告撰写
- 结构化呈现
- 规范化引用
- 可复现性保障

## 质量标准

### 信度要求
- 过程可重复
- 结果可验证
- 判断有依据

### 效度要求
- 方法适切性
- 结论合理性
- 解释充分性

### 伦理要求
- 数据隐私保护
- 利益冲突声明
- 研究伦理遵循

## 输出格式

分析报告应包含以下部分：

1. **方法说明**: 使用的方法及理由
2. **分析过程**: 关键步骤和决策
3. **主要发现**: 核心结果呈现
4. **结果解读**: 理论意义阐述
5. **局限性**: 研究局限说明
6. **建议**: 后续研究建议

## 交互原则

1. **渐进式披露**: 根据用户需求逐步深入
2. **透明化**: 明确说明分析过程和判断依据
3. **可追溯**: 所有结论可追溯到原始数据
4. **可验证**: 提供验证方法供用户检验

## 注意事项

- 始终遵循方法论规范
- 保持学术严谨性
- 注意分析边界
- 承认不确定性

---

**技能版本**: v5.0.0
**创建时间**: 2026-03-15
**方法论基准**: 学术界主流方法论标准
'''
        
        try:
            (skill_dir / "prompts" / "system-prompt.md").write_text(prompt_content, encoding='utf-8')
            print(f"✅ Step 3: 系统提示词创建完成 - {skill_name}")
            return True
        except Exception as e:
            print(f"❌ Step 3 失败: {e}")
            return False
    
    def create_tools(self, skill_name: str) -> bool:
        """Step 4: 创建工具函数"""
        skill_dir = self.skills_dir / skill_name
        
        # 创建基础工具模板
        tool_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{skill_name} - 工具函数模块
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# 跨平台兼容
def get_data_dir() -> Path:
    """获取数据目录"""
    return Path(__file__).parent.parent / "test_data"

def validate_input(data: Any) -> bool:
    """验证输入数据"""
    if data is None:
        return False
    return True

def process_data(data: Any, options: Dict = None) -> Dict:
    """处理数据"""
    options = options or {{}}
    return {{
        "status": "success",
        "message": "数据处理完成",
        "results": {{}}
    }}

if __name__ == "__main__":
    print(f"{skill_name} 工具模块已加载")
'''
        
        try:
            (skill_dir / "tools" / "__init__.py").write_text(tool_content, encoding='utf-8')
            print(f"✅ Step 4: 工具函数创建完成 - {skill_name}")
            return True
        except Exception as e:
            print(f"❌ Step 4 失败: {e}")
            return False
    
    def create_references(self, skill_name: str) -> bool:
        """Step 5: 创建参考文档"""
        skill_dir = self.skills_dir / skill_name
        metadata = SKILL_METADATA.get(skill_name, {})
        
        ref_content = f'''# {metadata.get("name_zh", skill_name)} - 详细指南

## 概述

{metadata.get("description", "")}

## 方法论基础

本技能基于以下方法论框架：

### 理论来源
- 相关学科经典文献
- 国际主流方法论标准
- 最新研究进展

### 方法特点
- 系统性：完整的分析流程
- 科学性：基于证据的方法
- 实用性：可操作的实施步骤

## 应用场景

### 适用领域
{chr(10).join([f"- {kw}" for kw in metadata.get("keywords", ["研究"])[:5]])}

### 典型任务
1. 数据分析
2. 结果解释
3. 报告撰写

## 实施流程

### 准备阶段
1. 明确研究问题
2. 收集相关数据
3. 选择分析方法

### 执行阶段
1. 数据处理
2. 分析执行
3. 结果验证

### 报告阶段
1. 结果整理
2. 意义阐释
3. 报告撰写

## 质量控制

### 过程质量
- 方法选择适当
- 步骤执行完整
- 过程记录清晰

### 结果质量
- 结论有依据
- 解释充分
- 局限性明确

## 常见问题

### Q1: 如何选择分析方法？
根据研究问题、数据特征和研究目的综合判断。

### Q2: 如何确保分析质量？
遵循方法论规范，进行过程记录和结果验证。

### Q3: 如何解读分析结果？
结合理论框架和实践背景，注意解释边界。

## 参考资源

- 相关教材
- 学术论文
- 在线课程

---

**版本**: v5.0.0
**更新时间**: 2026-03-15
'''
        
        try:
            (skill_dir / "references" / "detailed-guide.md").write_text(ref_content, encoding='utf-8')
            print(f"✅ Step 5: 参考文档创建完成 - {skill_name}")
            return True
        except Exception as e:
            print(f"❌ Step 5 失败: {e}")
            return False
    
    def create_test_data(self, skill_name: str) -> bool:
        """Step 5b: 创建测试数据"""
        skill_dir = self.skills_dir / skill_name
        
        test_data = {
            "skill": skill_name,
            "version": "5.0.0",
            "test_cases": [
                {
                    "id": "test_001",
                    "name": "基础测试案例",
                    "input": {
                        "data": "示例数据",
                        "options": {}
                    },
                    "expected": {
                        "status": "success"
                    }
                }
            ]
        }
        
        try:
            import json
            (skill_dir / "test_data" / "test_cases.json").write_text(
                json.dumps(test_data, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            print(f"✅ Step 5b: 测试数据创建完成 - {skill_name}")
            return True
        except Exception as e:
            print(f"❌ Step 5b 失败: {e}")
            return False
    
    def update_task_plan(self, skill_name: str, step: int, status: str) -> bool:
        """更新任务计划"""
        skill_dir = self.skills_dir / skill_name
        task_plan = skill_dir / "TASK_PLAN.md"
        
        try:
            if task_plan.exists():
                content = task_plan.read_text(encoding='utf-8')
                # 更新步骤状态
                old_status = f"Step {step}:"
                for s in ["目录结构", "核心文件", "提示词系统", "工具函数", "测试数据", "验证对齐"]:
                    old_line = f"| Step {step}: {s} | pending"
                    new_line = f"| Step {step}: {s} | {status}"
                    content = content.replace(old_line, new_line)
                task_plan.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"更新任务计划失败: {e}")
            return False
    
    def create_skill(self, skill_name: str) -> bool:
        """完整创建一个技能"""
        print(f"\n{'='*60}")
        print(f"开始创建技能: {skill_name}")
        print(f"{'='*60}\n")
        
        steps = [
            ("Step 1: 目录结构", self.create_skill_structure),
            ("Step 2a: SKILL.md", self.create_skill_md),
            ("Step 2b: skill.yaml", self.create_skill_yaml),
            ("Step 2c: subagents.yaml", self.create_subagents_yaml),
            ("Step 3: 系统提示词", self.create_system_prompt),
            ("Step 4: 工具函数", self.create_tools),
            ("Step 5: 参考文档", self.create_references),
            ("Step 5b: 测试数据", self.create_test_data),
        ]
        
        for step_name, step_func in steps:
            print(f"\n执行: {step_name}")
            if not step_func(skill_name):
                print(f"❌ 技能创建失败于: {step_name}")
                return False
        
        print(f"\n✅ 技能创建完成: {skill_name}\n")
        return True
    
    def run_batch(self, batch_num: int) -> Dict:
        """执行一批技能创建"""
        skills = SKILL_BATCHES.get(batch_num, [])
        results = {"total": len(skills), "success": 0, "failed": 0, "skills": {}}
        
        for skill_name in skills:
            if self.create_skill(skill_name):
                results["success"] += 1
                results["skills"][skill_name] = "success"
            else:
                results["failed"] += 1
                results["skills"][skill_name] = "failed"
        
        return results
    
    def run_auto(self) -> Dict:
        """自动运行 - 从第一个未完成的技能开始"""
        status = self.get_status()
        
        # 找到第一个未完成的技能
        next_skill = None
        for batch_num in [1, 2, 3, 4]:
            for skill_name in SKILL_BATCHES[batch_num]:
                skill_status = status["skills"].get(skill_name, "pending")
                if skill_status != "complete":
                    next_skill = skill_name
                    break
            if next_skill:
                break
        
        if not next_skill:
            return {"status": "all_complete", "message": "所有技能已创建完成"}
        
        return {"status": "creating", "skill": next_skill, "result": self.create_skill(next_skill)}


def main():
    """主函数"""
    creator = AutoSkillCreator()
    
    if len(sys.argv) == 1:
        # 默认：继续当前任务
        print("Auto Skill Creator - 自动技能创建系统")
        print("=" * 50)
        result = creator.run_auto()
        print(f"\n执行结果: {result}")
    
    elif sys.argv[1] == "--status":
        # 查看状态
        status = creator.get_status()
        print(f"\n技能创建状态:")
        print(f"  总计: {status['total_skills']}")
        print(f"  已完成: {status['completed']}")
        print(f"  进行中: {status['in_progress']}")
        print(f"  待处理: {status['pending']}")
        print(f"\n下一个待处理技能: {creator.current_skill}")
    
    elif sys.argv[1] == "--skill" and len(sys.argv) > 2:
        # 指定技能
        skill_name = sys.argv[2]
        creator.create_skill(skill_name)
    
    elif sys.argv[1] == "--batch" and len(sys.argv) > 2:
        # 执行批次
        batch_num = int(sys.argv[2])
        results = creator.run_batch(batch_num)
        print(f"\n批次 {batch_num} 执行结果:")
        print(f"  成功: {results['success']}/{results['total']}")
        print(f"  失败: {results['failed']}/{results['total']}")
    
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
