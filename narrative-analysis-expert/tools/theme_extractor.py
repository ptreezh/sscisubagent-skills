#!/usr/bin/env python3
"""
叙事主题提取工具

功能：
- 从叙事中提取主题
- 聚类相关主题
- 跨叙事比较主题

用法：
    python theme_extractor.py --input "叙事文本" --extract
    python theme_extractor.py --file narratives.txt --cluster
    python theme_extractor.py --dir narratives/ --compare
"""

import argparse
import json
import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, asdict
from collections import Counter
from pathlib import Path


@dataclass
class Theme:
    """叙事主题"""
    name: str
    keywords: List[str]
    occurrences: List[str]  # 原文片段
    frequency: int
    related_themes: List[str]


@dataclass
class ThemeAnalysisResult:
    """主题分析结果"""
    main_themes: List[Theme]
    sub_themes: List[Theme]
    theme_network: Dict[str, List[str]]


# 预设主题类别（可根据研究需要扩展）
THEME_CATEGORIES = {
    "转变与成长": {
        "keywords": ["改变", "转变", "成长", "变化", "不同", "新生"],
        "sub_themes": ["自我发现", "价值观转变", "身份转变"]
    },
    "关系与联结": {
        "keywords": ["家人", "朋友", "支持", "陪伴", "孤独", "理解"],
        "sub_themes": ["家庭关系", "友谊", "社会支持"]
    },
    "意义与价值": {
        "keywords": ["意义", "价值", "重要", "值得", "珍惜", "宝贵"],
        "sub_themes": ["人生意义", "价值重塑", "意义追寻"]
    },
    "挑战与应对": {
        "keywords": ["困难", "挑战", "压力", "克服", "坚持", "努力"],
        "sub_themes": ["困境经历", "应对策略", "韧性成长"]
    },
    "时间与记忆": {
        "keywords": ["过去", "回忆", "曾经", "那时候", "怀念", "铭记"],
        "sub_themes": ["童年记忆", "重要事件", "时间感悟"]
    },
    "情感与体验": {
        "keywords": ["感动", "幸福", "悲伤", "恐惧", "焦虑", "喜悦"],
        "sub_themes": ["积极情感", "消极情感", "复杂情感"]
    }
}


def extract_keywords_from_text(text: str) -> List[str]:
    """从文本中提取关键词
    
    Args:
        text: 叙事文本
        
    Returns:
        关键词列表
    """
    # 简单的关键词提取（实际应用中可使用jieba等工具）
    words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
    return words


def find_theme_occurrences(text: str, theme_keywords: List[str]) -> List[Tuple[str, str]]:
    """查找主题在文本中的出现
    
    Args:
        text: 叙事文本
        theme_keywords: 主题关键词
        
    Returns:
        [(关键词, 上下文片段), ...]
    """
    occurrences = []
    
    for keyword in theme_keywords:
        # 查找关键词及其上下文
        pattern = re.compile(
            r'(.{0,30})' + re.escape(keyword) + r'(.{0,30})',
            re.DOTALL
        )
        
        for match in pattern.finditer(text):
            context = match.group(0)
            occurrences.append((keyword, context))
    
    return occurrences


def extract_themes(text: str) -> ThemeAnalysisResult:
    """从叙事中提取主题
    
    Args:
        text: 叙事文本
        
    Returns:
        ThemeAnalysisResult: 主题分析结果
    """
    main_themes = []
    sub_themes = []
    theme_network = {}
    
    for category, info in THEME_CATEGORIES.items():
        occurrences = find_theme_occurrences(text, info["keywords"])
        
        if occurrences:
            theme = Theme(
                name=category,
                keywords=info["keywords"],
                occurrences=[ctx for _, ctx in occurrences[:5]],
                frequency=len(occurrences),
                related_themes=[]
            )
            main_themes.append(theme)
            
            # 检查子主题
            for sub_theme in info["sub_themes"]:
                sub_keywords = [sub_theme.split("与")[-1]]  # 简化处理
                sub_occurrences = find_theme_occurrences(text, sub_keywords)
                
                if sub_occurrences:
                    sub = Theme(
                        name=sub_theme,
                        keywords=sub_keywords,
                        occurrences=[ctx for _, ctx in sub_occurrences[:3]],
                        frequency=len(sub_occurrences),
                        related_themes=[category]
                    )
                    sub_themes.append(sub)
            
            # 建立主题网络
            theme_network[category] = info["sub_themes"]
    
    # 按频率排序
    main_themes.sort(key=lambda t: t.frequency, reverse=True)
    sub_themes.sort(key=lambda t: t.frequency, reverse=True)
    
    return ThemeAnalysisResult(
        main_themes=main_themes,
        sub_themes=sub_themes,
        theme_network=theme_network
    )


def cluster_themes(themes_list: List[ThemeAnalysisResult]) -> Dict:
    """聚类多个叙事的主题
    
    Args:
        themes_list: 多个叙事的主题分析结果
        
    Returns:
        聚类结果
    """
    theme_counter = Counter()
    theme_occurrences_map = {}
    
    for result in themes_list:
        for theme in result.main_themes:
            theme_counter[theme.name] += theme.frequency
            
            if theme.name not in theme_occurrences_map:
                theme_occurrences_map[theme.name] = []
            theme_occurrences_map[theme.name].extend(theme.occurrences)
    
    # 识别共同主题
    common_themes = [
        {
            "name": name,
            "total_frequency": count,
            "sample_occurrences": theme_occurrences_map[name][:3]
        }
        for name, count in theme_counter.most_common(10)
    ]
    
    # 识别独特主题
    all_themes = set(theme_counter.keys())
    themes_by_narrative = []
    
    for i, result in enumerate(themes_list):
        narrative_themes = {t.name for t in result.main_themes}
        unique_themes = narrative_themes - (all_themes - narrative_themes)
        themes_by_narrative.append({
            "narrative_id": i,
            "themes": list(narrative_themes),
            "unique_themes": list(unique_themes)
        })
    
    return {
        "common_themes": common_themes,
        "themes_by_narrative": themes_by_narrative,
        "theme_distribution": dict(theme_counter)
    }


def compare_narratives(narratives: List[str]) -> Dict:
    """跨叙事比较主题
    
    Args:
        narratives: 叙事文本列表
        
    Returns:
        比较结果
    """
    themes_results = [extract_themes(n) for n in narratives]
    clustered = cluster_themes(themes_results)
    
    # 计算主题共现
    co_occurrence = Counter()
    for result in themes_results:
        theme_names = [t.name for t in result.main_themes]
        for i, t1 in enumerate(theme_names):
            for t2 in theme_names[i+1:]:
                pair = tuple(sorted([t1, t2]))
                co_occurrence[pair] += 1
    
    return {
        "individual_results": [
            {
                "main_themes": [t.name for t in r.main_themes],
                "sub_themes": [t.name for t in r.sub_themes]
            }
            for r in themes_results
        ],
        "clustered": clustered,
        "co_occurrence": {
            f"{pair[0]} + {pair[1]}": count 
            for pair, count in co_occurrence.most_common(10)
        }
    }


def print_theme_report(result: ThemeAnalysisResult):
    """打印主题分析报告"""
    print("\n" + "="*60)
    print("叙事主题分析报告")
    print("="*60)
    
    print("\n【主要主题】")
    print("-"*60)
    for theme in result.main_themes:
        print(f"\n▶ {theme.name} (出现{theme.frequency}次)")
        print(f"  关键词: {', '.join(theme.keywords[:5])}")
        if theme.occurrences:
            print(f"  示例: 「{theme.occurrences[0][:50]}...」")
    
    if result.sub_themes:
        print("\n【子主题】")
        print("-"*60)
        for theme in result.sub_themes[:5]:
            print(f"  • {theme.name} (关联主题: {', '.join(theme.related_themes)})")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description="叙事主题提取工具")
    parser.add_argument("--input", type=str, help="直接输入叙事文本")
    parser.add_argument("--file", type=str, help="从文件读取叙事文本")
    parser.add_argument("--dir", type=str, help="从目录读取多个叙事文件")
    parser.add_argument("--extract", action="store_true", help="提取主题")
    parser.add_argument("--cluster", action="store_true", help="聚类主题")
    parser.add_argument("--compare", action="store_true", help="跨叙事比较")
    parser.add_argument("--output", type=str, help="输出文件路径（JSON格式）")
    
    args = parser.parse_args()
    
    if args.extract:
        # 单叙事主题提取
        if args.input:
            text = args.input
        elif args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            text = "生病让我重新思考人生，以前总是忙工作，现在学会了慢下来。家人的支持是我最大的力量，没有他们我撑不下来。我觉得这场病是一次提醒，提醒我要照顾好自己。"
        
        result = extract_themes(text)
        print_theme_report(result)
        
        if args.output:
            output_data = {
                "main_themes": [
                    {"name": t.name, "frequency": t.frequency, "occurrences": t.occurrences}
                    for t in result.main_themes
                ],
                "sub_themes": [
                    {"name": t.name, "related_themes": t.related_themes}
                    for t in result.sub_themes
                ]
            }
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    if args.cluster and args.dir:
        # 多叙事主题聚类
        narratives = []
        dir_path = Path(args.dir)
        for file_path in dir_path.glob("*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                narratives.append(f.read())
        
        if narratives:
            themes_results = [extract_themes(n) for n in narratives]
            clustered = cluster_themes(themes_results)
            
            print("\n【主题聚类结果】")
            for theme in clustered["common_themes"]:
                print(f"  • {theme['name']}: {theme['total_frequency']}次")
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(clustered, f, ensure_ascii=False, indent=2)
    
    if args.compare and args.dir:
        # 跨叙事比较
        narratives = []
        dir_path = Path(args.dir)
        for file_path in sorted(dir_path.glob("*.txt")):
            with open(file_path, "r", encoding="utf-8") as f:
                narratives.append(f.read())
        
        if narratives:
            comparison = compare_narratives(narratives)
            
            print("\n【跨叙事主题比较】")
            print(f"共分析 {len(narratives)} 篇叙事")
            print("\n共同主题:")
            for theme in comparison["clustered"]["common_themes"][:5]:
                print(f"  • {theme['name']}")
            
            print("\n主题共现:")
            for pair, count in comparison["co_occurrence"].items():
                print(f"  • {pair}: {count}次")
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(comparison, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
