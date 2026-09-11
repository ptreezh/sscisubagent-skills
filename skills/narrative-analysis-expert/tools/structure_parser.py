#!/usr/bin/env python3
"""
Labov叙事结构解析工具

功能：
- 解析叙事的六要素结构
- 识别结构要素位置
- 验证结构完整性

用法：
    python structure_parser.py --input "叙事文本" --parse
    python structure_parser.py --file narrative.txt --identify
    python structure_parser.py --file narrative.txt --validate
"""

import argparse
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class NarrativeElement(Enum):
    """叙事结构要素"""
    ABSTRACT = "摘要"
    ORIENTATION = "定向"
    COMPLICATING_ACTION = "纠葛"
    EVALUATION = "评估"
    RESOLUTION = "结果"
    CODA = "结尾"


@dataclass
class StructureSegment:
    """结构片段"""
    element: str
    element_cn: str
    text: str
    start_pos: int
    end_pos: int
    confidence: float
    markers: List[str]


@dataclass
class NarrativeStructure:
    """叙事结构分析结果"""
    original_text: str
    segments: List[StructureSegment]
    completeness_score: float
    missing_elements: List[str]
    structure_type: str


# 要素识别标记
ELEMENT_MARKERS = {
    NarrativeElement.ABSTRACT: {
        "keywords": ["总之", "简单说", "故事是关于", "事情是这样的"],
        "patterns": [r"^(.{0,20})(?=那天|有一次|记得)"],
        "description": "故事概要，通常在开头"
    },
    NarrativeElement.ORIENTATION: {
        "keywords": ["当时", "那时候", "在", "那年", "有一天"],
        "patterns": [
            r"当时.{0,50}",
            r"那(年|天|次|个).{0,30}",
            r"在.{0,20}(工作|住|学)"
        ],
        "description": "背景设定：时间、地点、人物"
    },
    NarrativeElement.COMPLICATING_ACTION: {
        "keywords": ["但是", "结果", "突然", "没想到", "竟然"],
        "patterns": [
            r"(但是|可是|然而).{0,100}",
            r"突然.{0,50}",
            r"没想到.{0,50}",
            r"结果.{0,30}(出事|出问题|发生)"
        ],
        "description": "核心事件、冲突发生"
    },
    NarrativeElement.EVALUATION: {
        "keywords": ["觉得", "感到", "心想", "认为", "特别", "非常"],
        "patterns": [
            r"(我|心里)?(觉得|感到|心想).{0,50}",
            r"特别(难过|高兴|紧张|生气)",
            r"这对(我|我们)来说"
        ],
        "description": "讲述者的态度和意义阐释"
    },
    NarrativeElement.RESOLUTION: {
        "keywords": ["最后", "终于", "后来", "结局"],
        "patterns": [
            r"(最后|终于).{0,50}",
            r"后来.{0,30}(解决|好|成功)",
            r"结局是"
        ],
        "description": "事件最终结局"
    },
    NarrativeElement.CODA: {
        "keywords": ["让我", "使我", "教会我", "明白", "学到"],
        "patterns": [
            r"(这|那)(件)?事(让我|使我|教会我).{0,50}",
            r"我(明白|学到|懂得)了",
            r"回头看"
        ],
        "description": "回归当下，故事意义"
    }
}


def identify_element(text: str, element: NarrativeElement) -> List[Tuple[int, int, str]]:
    """识别文本中的特定结构要素
    
    Args:
        text: 叙事文本
        element: 要识别的结构要素
        
    Returns:
        匹配位置列表 [(start, end, matched_text), ...]
    """
    matches = []
    markers = ELEMENT_MARKERS[element]
    
    # 关键词匹配
    for keyword in markers["keywords"]:
        for match in re.finditer(re.escape(keyword), text):
            # 扩展匹配范围（前后各20个字符）
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 50)
            matches.append((start, end, text[start:end]))
    
    # 模式匹配
    for pattern in markers["patterns"]:
        for match in re.finditer(pattern, text):
            matches.append((match.start(), match.end(), match.group()))
    
    return matches


def parse_structure(text: str) -> NarrativeStructure:
    """解析叙事结构
    
    Args:
        text: 叙事文本
        
    Returns:
        NarrativeStructure: 结构分析结果
    """
    segments = []
    found_elements = set()
    
    for element in NarrativeElement:
        matches = identify_element(text, element)
        
        if matches:
            # 选择最相关的匹配（最长且靠前）
            best_match = max(matches, key=lambda m: (len(m[2]), -m[0]))
            start, end, matched_text = best_match
            
            # 计算置信度
            confidence = min(1.0, len(matched_text) / 30)
            
            segment = StructureSegment(
                element=element.name,
                element_cn=element.value,
                text=matched_text,
                start_pos=start,
                end_pos=end,
                confidence=confidence,
                markers=ELEMENT_MARKERS[element]["keywords"]
            )
            segments.append(segment)
            found_elements.add(element)
    
    # 计算完整性分数
    completeness_score = len(found_elements) / len(NarrativeElement)
    
    # 识别缺失要素
    missing_elements = [
        e.value for e in NarrativeElement if e not in found_elements
    ]
    
    # 判断结构类型
    if completeness_score >= 0.8:
        structure_type = "完整叙事"
    elif completeness_score >= 0.5:
        structure_type = "部分叙事"
    else:
        structure_type = "叙事片段"
    
    return NarrativeStructure(
        original_text=text,
        segments=segments,
        completeness_score=completeness_score,
        missing_elements=missing_elements,
        structure_type=structure_type
    )


def validate_structure(structure: NarrativeStructure) -> Dict:
    """验证叙事结构完整性
    
    Args:
        structure: 结构分析结果
        
    Returns:
        验证报告
    """
    report = {
        "is_valid": structure.completeness_score >= 0.5,
        "completeness": f"{structure.completeness_score:.1%}",
        "structure_type": structure.structure_type,
        "found_elements": [s.element_cn for s in structure.segments],
        "missing_elements": structure.missing_elements,
        "recommendations": []
    }
    
    # 生成改进建议
    if "摘要" in structure.missing_elements:
        report["recommendations"].append(
            "建议在开头添加故事概要，帮助听众快速了解叙事主题"
        )
    
    if "评估" in structure.missing_elements:
        report["recommendations"].append(
            "建议添加讲述者的主观评价，增强叙事的情感深度"
        )
    
    if "结尾" in structure.missing_elements:
        report["recommendations"].append(
            "建议添加结尾反思，明确叙事的意义"
        )
    
    return report


def print_structure_report(structure: NarrativeStructure):
    """打印结构分析报告"""
    print("\n" + "="*60)
    print("Labov叙事结构分析报告")
    print("="*60)
    
    print(f"\n【原始文本】\n{structure.original_text[:200]}...")
    
    print(f"\n【结构类型】{structure.structure_type}")
    print(f"【完整性分数】{structure.completeness_score:.1%}")
    
    print("\n【结构要素分析】")
    print("-"*60)
    
    for segment in sorted(structure.segments, key=lambda s: s.start_pos):
        print(f"\n▶ {segment.element_cn} ({segment.element})")
        print(f"  内容: {segment.text[:50]}...")
        print(f"  位置: {segment.start_pos}-{segment.end_pos}")
        print(f"  置信度: {segment.confidence:.1%}")
    
    if structure.missing_elements:
        print(f"\n【缺失要素】{', '.join(structure.missing_elements)}")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description="Labov叙事结构解析工具")
    parser.add_argument("--input", type=str, help="直接输入叙事文本")
    parser.add_argument("--file", type=str, help="从文件读取叙事文本")
    parser.add_argument("--parse", action="store_true", help="解析叙事结构")
    parser.add_argument("--identify", action="store_true", help="识别结构要素")
    parser.add_argument("--validate", action="store_true", help="验证结构完整性")
    parser.add_argument("--output", type=str, help="输出文件路径（JSON格式）")
    
    args = parser.parse_args()
    
    # 获取输入文本
    if args.input:
        text = args.input
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        # 示例文本
        text = """
        面试那天，我提前半小时到了公司楼下。天气特别热，我在星巴克买了杯咖啡等着。
        到了约定时间，我走进办公室，结果前台说面试官临时有事改期了。
        我当时特别生气，觉得白跑了。不过后来想想，也许这是老天在考验我的耐心吧。
        """
    
    # 执行分析
    structure = parse_structure(text.strip())
    
    if args.parse:
        print_structure_report(structure)
    
    if args.identify:
        print("\n【要素识别结果】")
        for element in NarrativeElement:
            matches = identify_element(text.strip(), element)
            if matches:
                print(f"\n{element.value}:")
                for start, end, matched in matches[:2]:
                    print(f"  - {matched[:50]}...")
    
    if args.validate:
        report = validate_structure(structure)
        print("\n【验证报告】")
        print(json.dumps(report, ensure_ascii=False, indent=2))
    
    if args.output:
        output_data = {
            "original_text": structure.original_text,
            "segments": [asdict(s) for s in structure.segments],
            "completeness_score": structure.completeness_score,
            "missing_elements": structure.missing_elements,
            "structure_type": structure.structure_type
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {args.output}")


if __name__ == "__main__":
    main()
