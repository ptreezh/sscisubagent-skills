#!/usr/bin/env python3
"""
IPA注释指南工具

功能: 指导研究者进行三类注释（描述性、语言性、概念性）
用法: python annotation_guide.py [选项]

选项:
  --guide          显示注释类型指南
  --example        显示注释示例
  --practice       开始注释练习
  --check FILE     检查注释质量
"""

import argparse
import json
from typing import Dict, List, Optional

class IPAAnnotationGuide:
    """IPA注释指南类"""
    
    ANNOTATION_TYPES = {
        "descriptive": {
            "name": "描述性注释",
            "focus": "参与者说了什么",
            "questions": [
                "参与者在这里描述了什么？",
                "主要内容是什么？",
                "有什么事件或情境被提及？"
            ],
            "tips": [
                "使用参与者的语言",
                "不要添加诠释",
                "关注内容本身"
            ]
        },
        "linguistic": {
            "name": "语言性注释",
            "focus": "参与者如何说",
            "questions": [
                "使用了什么隐喻或比喻？",
                "有什么停顿、犹豫或强调？",
                "语言选择有什么意义？"
            ],
            "tips": [
                "注意非语言表达",
                "关注叙述方式",
                "寻找重复模式"
            ]
        },
        "conceptual": {
            "name": "概念性注释",
            "focus": "研究者的诠释性思考",
            "questions": [
                "这可能意味着什么？",
                "这如何与已有概念联系？",
                "研究者有什么诠释性思考？"
            ],
            "tips": [
                "使用心理学术语",
                "承认研究者视角",
                "连接理论概念"
            ]
        }
    }
    
    def __init__(self):
        pass
    
    def show_guide(self) -> str:
        """显示注释类型指南"""
        output = []
        output.append("=" * 60)
        output.append("IPA注释类型指南")
        output.append("=" * 60)
        
        for type_key, type_info in self.ANNOTATION_TYPES.items():
            output.append(f"\n【{type_info['name']}】")
            output.append(f"焦点: {type_info['focus']}")
            output.append("\n引导问题:")
            for q in type_info['questions']:
                output.append(f"  - {q}")
            output.append("\n技巧:")
            for t in type_info['tips']:
                output.append(f"  ✓ {t}")
        
        return "\n".join(output)
    
    def show_example(self) -> str:
        """显示注释示例"""
        example = """
======================================================================
注释示例
======================================================================

原文:
"我觉得...[叹气]...就像被困在一个盒子里，哪儿也去不了，
我想要出去但是...就是...出不去。"

┌──────────────────────────────────────────────────────────────┐
│ 描述性注释:                                                   │
│ 参与者描述被困的感觉，想要逃离但做不到                        │
├──────────────────────────────────────────────────────────────┤
│ 语言性注释:                                                   │
│ - "我觉得..." 犹豫的开场                                     │
│ - "就像..." 隐喻引入                                         │
│ - "盒子" 空间限制意象                                        │
│ - "哪儿也去不了" 绝对化表达                                  │
│ - "就是...出不去" 重复、无力感                               │
│ - [叹气] 无奈情感                                            │
├──────────────────────────────────────────────────────────────┤
│ 概念性注释:                                                   │
│ - 被困感、受限                                               │
│ - 自我与他者/环境的边界                                      │
│ - 无力感、控制丧失                                           │
│ - 可能与"受限自我"概念相关                                   │
└──────────────────────────────────────────────────────────────┘

注意: 三类注释并行进行，不要跳过任何一类！
"""
        return example
    
    def check_annotation(self, annotations: Dict) -> Dict:
        """检查注释质量"""
        results = {
            "complete": True,
            "issues": [],
            "suggestions": []
        }
        
        # 检查是否包含三类注释
        for type_key in ["descriptive", "linguistic", "conceptual"]:
            if type_key not in annotations or not annotations[type_key]:
                results["complete"] = False
                results["issues"].append(f"缺少{self.ANNOTATION_TYPES[type_key]['name']}")
        
        # 检查描述性注释是否过于诠释
        if "descriptive" in annotations:
            desc = annotations["descriptive"]
            interpretive_words = ["意味着", "表明", "显示", "反映"]
            for word in interpretive_words:
                if word in desc:
                    results["suggestions"].append(
                        f"描述性注释应避免诠释性词汇 '{word}'"
                    )
        
        # 检查概念性注释是否过于描述
        if "conceptual" in annotations:
            conc = annotations["conceptual"]
            if len(conc) < 10:
                results["suggestions"].append(
                    "概念性注释可能过于简单，请深化诠释性思考"
                )
        
        return results


def main():
    parser = argparse.ArgumentParser(description="IPA注释指南工具")
    parser.add_argument("--guide", action="store_true", help="显示注释类型指南")
    parser.add_argument("--example", action="store_true", help="显示注释示例")
    parser.add_argument("--practice", action="store_true", help="开始注释练习")
    parser.add_argument("--check", type=str, help="检查注释质量 (JSON文件)")
    
    args = parser.parse_args()
    
    guide = IPAAnnotationGuide()
    
    if args.guide:
        print(guide.show_guide())
    elif args.example:
        print(guide.show_example())
    elif args.practice:
        print("注释练习模式")
        print("请输入原文片段，然后分别进行三类注释...")
        # 交互式练习逻辑
    elif args.check:
        try:
            with open(args.check, 'r', encoding='utf-8') as f:
                annotations = json.load(f)
            results = guide.check_annotation(annotations)
            print(json.dumps(results, ensure_ascii=False, indent=2))
        except FileNotFoundError:
            print(f"文件未找到: {args.check}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
