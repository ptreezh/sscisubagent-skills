#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action Research Reflection Guide
行动研究反思引导工具

使用方法:
    python reflection_guide.py --start
    python reflection_guide.py --stage plan --cycle 1
    python reflection_guide.py --generate-prompts
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import argparse


class ReflectionGuide:
    """行动研究反思引导器"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.reflection_dir = self.project_path / "action-research-workspace" / "reflections"
        self.reflection_dir.mkdir(parents=True, exist_ok=True)
        
        # 反思问题库
        self.reflection_questions = {
            "plan": {
                "descriptive": [
                    "计划中包含了哪些具体行动？",
                    "目标是如何设定的？",
                    "分配了哪些资源？"
                ],
                "explanatory": [
                    "为什么选择这个策略？",
                    "计划基于什么假设？",
                    "预期的障碍是什么？"
                ],
                "critical": [
                    "这个计划是否真正解决了问题根源？",
                    "利益相关者是否参与计划制定？",
                    "计划是否考虑了伦理问题？"
                ],
                "actionable": [
                    "计划需要调整哪些内容？",
                    "下一轮应该如何改进计划过程？",
                    "需要增加哪些参与者的意见？"
                ]
            },
            "act": {
                "descriptive": [
                    "实施了哪些具体活动？",
                    "参与者有哪些反应？",
                    "遇到了什么意外情况？"
                ],
                "explanatory": [
                    "为什么会出现这些反应？",
                    "意外情况的原因是什么？",
                    "调整措施基于什么考虑？"
                ],
                "critical": [
                    "实施是否偏离了原计划？为什么？",
                    "是否有被忽视的声音？",
                    "实施过程中的权力关系如何？"
                ],
                "actionable": [
                    "如何改进实施过程？",
                    "下一轮需要哪些调整？",
                    "如何更好地应对意外？"
                ]
            },
            "observe": {
                "descriptive": [
                    "收集了哪些数据？",
                    "观察到了什么变化？",
                    "参与者提供了什么反馈？"
                ],
                "explanatory": [
                    "数据说明了什么？",
                    "变化的原因是什么？",
                    "反馈背后的深层含义是什么？"
                ],
                "critical": [
                    "数据收集方法是否适当？",
                    "是否有被遗漏的视角？",
                    "观察者偏见如何影响结论？"
                ],
                "actionable": [
                    "下一轮应该收集什么额外数据？",
                    "如何改进数据收集方法？",
                    "如何更全面地捕捉变化？"
                ]
            },
            "reflect": {
                "descriptive": [
                    "本轮的主要发现是什么？",
                    "取得了什么成果？",
                    "遗留了什么问题？"
                ],
                "explanatory": [
                    "为什么会有这样的结果？",
                    "什么因素促成了成功/失败？",
                    "理论与实践有何关联？"
                ],
                "critical": [
                    "我对问题的理解发生了什么变化？",
                    "研究过程中的权力关系如何？",
                    "知识是如何被建构的？"
                ],
                "actionable": [
                    "下一轮应该聚焦什么问题？",
                    "如何应用本轮的学习？",
                    "需要调整哪些假设？"
                ]
            }
        }
        
        # 循环反思问题
        self.cycle_reflection_questions = [
            "这轮循环解决了什么问题？",
            "新发现了什么问题？",
            "对原有问题的理解有什么变化？",
            "什么策略有效？什么无效？",
            "利益相关者的参与程度如何？",
            "伦理问题处理得如何？",
            "从这轮中学到的最重要的经验是什么？",
            "下一轮应该如何调整方向？"
        ]
    
    def start_reflection_session(self, cycle_num: int, stage: str) -> Dict:
        """开始反思会话"""
        stage = stage.lower()
        
        session = {
            "cycle": cycle_num,
            "stage": stage,
            "started_at": datetime.now().isoformat(),
            "questions": self.reflection_questions.get(stage, {}),
            "responses": {}
        }
        
        return session
    
    def generate_reflection_prompts(self, cycle_num: int, stage: str) -> str:
        """生成反思提示"""
        stage = stage.lower()
        questions = self.reflection_questions.get(stage, {})
        
        prompt = f"""# 第 {cycle_num} 轮循环 - {stage.upper()} 阶段反思指南

## 反思框架

使用四层次反思框架进行深度反思：

### 1. 描述性反思 (Descriptive)
*发生了什么？*

"""
        for q in questions.get("descriptive", []):
            prompt += f"- {q}\n"
        
        prompt += f"""
### 2. 解释性反思 (Explanatory)
*为什么发生？*

"""
        for q in questions.get("explanatory", []):
            prompt += f"- {q}\n"
        
        prompt += f"""
### 3. 批判性反思 (Critical)
*意味着什么？*

"""
        for q in questions.get("critical", []):
            prompt += f"- {q}\n"
        
        prompt += f"""
### 4. 行动性反思 (Actionable)
*下一步做什么？*

"""
        for q in questions.get("actionable", []):
            prompt += f"- {q}\n"
        
        prompt += f"""
## 反思要求

1. 每个层次至少回答2个问题
2. 使用具体的数据和证据支撑观点
3. 保持诚实和批判性
4. 关注学习而非评判

## 输出格式

请按以下格式记录反思：

```
## 描述性反思
[你的回答]

## 解释性反思
[你的回答]

## 批判性反思
[你的回答]

## 行动性反思
[你的回答]

## 关键学习
- 学习1
- 学习2
- 学习3
```
"""
        return prompt
    
    def generate_cycle_reflection(self, cycle_num: int) -> str:
        """生成循环整体反思提示"""
        prompt = f"""# 第 {cycle_num} 轮循环整体反思

## 反思问题

请逐一回答以下问题：

"""
        for i, q in enumerate(self.cycle_reflection_questions, 1):
            prompt += f"{i}. {q}\n\n"
        
        prompt += f"""
## 反思深度检查

在完成反思后，请检查：

- [ ] 是否使用了数据支撑观点？
- [ ] 是否识别了假设和偏见？
- [ ] 是否考虑了多重视角？
- [ ] 是否提出了可行的改进方向？
- [ ] 是否记录了可迁移的经验？

## 循环总结模板

```
## 成果总结
[本轮取得的具体成果]

## 问题发现
[新发现的问题或原有问题的新理解]

## 经验提取
[可迁移的经验和教训]

## 下一轮规划
[基于反思的下一轮调整方向]
```
"""
        return prompt
    
    def assess_reflection_depth(self, reflection_text: str) -> Dict:
        """评估反思深度"""
        # 检查各层次的存在性
        has_descriptive = any(kw in reflection_text for kw in 
            ["发生了", "观察到", "实施", "收集", "参与者"])
        has_explanatory = any(kw in reflection_text for kw in 
            ["因为", "由于", "原因是", "导致", "使得"])
        has_critical = any(kw in reflection_text for kw in 
            ["假设", "偏见", "权力", "伦理", "质疑", "重新理解"])
        has_actionable = any(kw in reflection_text for kw in 
            ["下一轮", "改进", "调整", "建议", "应该"])
        
        # 计算深度分数
        depth_score = sum([
            has_descriptive * 1,
            has_explanatory * 2,
            has_critical * 3,
            has_actionable * 1
        ])
        
        # 检查数据支撑
        has_data = any(char.isdigit() for char in reflection_text)
        has_evidence = "数据" in reflection_text or "证据" in reflection_text
        
        # 检查字数
        word_count = len(reflection_text)
        
        assessment = {
            "depth_score": depth_score,
            "max_score": 7,
            "depth_level": "深度" if depth_score >= 5 else "中等" if depth_score >= 3 else "浅层",
            "has_descriptive": has_descriptive,
            "has_explanatory": has_explanatory,
            "has_critical": has_critical,
            "has_actionable": has_actionable,
            "has_data_support": has_data and has_evidence,
            "word_count": word_count,
            "meets_minimum": word_count >= 200 and depth_score >= 3
        }
        
        return assessment
    
    def save_reflection(self, cycle_num: int, stage: str, content: str):
        """保存反思记录"""
        filename = f"reflection_cycle{cycle_num}_{stage}.md"
        filepath = self.reflection_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 反思记录已保存: {filepath}")
        
        # 评估反思深度
        assessment = self.assess_reflection_depth(content)
        
        if not assessment["meets_minimum"]:
            print(f"⚠️ 反思深度不足建议:")
            if assessment["word_count"] < 200:
                print("  - 建议增加反思内容，至少200字")
            if not assessment["has_critical"]:
                print("  - 建议增加批判性反思层次")
            if not assessment["has_data_support"]:
                print("  - 建议使用数据支撑观点")
        
        return assessment
    
    def generate_reflection_template(self) -> str:
        """生成反思日志模板"""
        template = """# 行动研究反思日志

## 基本信息
- **日期**: [YYYY-MM-DD]
- **循环轮次**: 第 [X] 轮
- **当前阶段**: [计划/行动/观察/反思]
- **反思者**: [姓名]

---

## 一、描述性反思
*发生了什么？描述具体事件、行为、数据*

[请在此记录...]

---

## 二、解释性反思
*为什么发生？分析原因、动机、影响因素*

[请在此记录...]

---

## 三、批判性反思
*意味着什么？质疑假设、审视权力、反思价值观*

[请在此记录...]

---

## 四、行动性反思
*下一步做什么？提出改进方向、具体行动*

[请在此记录...]

---

## 五、关键学习

### 成功经验
1. ...
2. ...

### 问题发现
1. ...
2. ...

### 可迁移经验
1. ...
2. ...

---

## 六、下一轮计划调整

基于本轮反思，下一轮将调整：
1. ...
2. ...

---

**反思字数**: [自动统计]
**反思深度**: [自动评估]
"""
        return template


def main():
    parser = argparse.ArgumentParser(description="行动研究反思引导工具")
    
    parser.add_argument("--start", action="store_true", help="开始反思会话")
    parser.add_argument("--cycle", type=int, default=1, help="循环轮次")
    parser.add_argument("--stage", type=str, default="reflect", 
                       choices=["plan", "act", "observe", "reflect"],
                       help="反思阶段")
    parser.add_argument("--generate-prompts", action="store_true", help="生成反思提示")
    parser.add_argument("--generate-cycle", action="store_true", help="生成循环反思")
    parser.add_argument("--generate-template", action="store_true", help="生成反思模板")
    parser.add_argument("--save", type=str, help="保存反思内容")
    parser.add_argument("--assess", type=str, help="评估反思深度")
    
    args = parser.parse_args()
    
    guide = ReflectionGuide()
    
    if args.start:
        session = guide.start_reflection_session(args.cycle, args.stage)
        print(json.dumps(session, ensure_ascii=False, indent=2))
    
    if args.generate_prompts:
        prompts = guide.generate_reflection_prompts(args.cycle, args.stage)
        print(prompts)
    
    if args.generate_cycle:
        prompts = guide.generate_cycle_reflection(args.cycle)
        print(prompts)
    
    if args.generate_template:
        template = guide.generate_reflection_template()
        print(template)
    
    if args.save:
        assessment = guide.save_reflection(args.cycle, args.stage, args.save)
        print(f"\n反思深度评估: {json.dumps(assessment, ensure_ascii=False, indent=2)}")
    
    if args.assess:
        assessment = guide.assess_reflection_depth(args.assess)
        print(json.dumps(assessment, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
