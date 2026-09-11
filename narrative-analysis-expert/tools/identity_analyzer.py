#!/usr/bin/env python3
"""
叙事认同分析工具

功能：
- 分析叙事基调（救赎性/污染性/进步性/退步性）
- 识别核心情节类型
- 分析身份建构过程

用法：
    python identity_analyzer.py --input "叙事文本" --tone
    python identity_analyzer.py --file narrative.txt --plot
    python identity_analyzer.py --file narrative.txt --identity
"""

import argparse
import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class NarrativeTone(Enum):
    """叙事基调"""
    REDEMPTION = "救赎性"      # 困境→转变→成长
    CONTAMINATION = "污染性"  # 好事被坏事破坏
    PROGRESSIVE = "进步性"    # 持续向上发展
    REGRESSIVE = "退步性"     # 持续下降


class PlotType(Enum):
    """情节类型"""
    HIGH_POINT = "高潮情节"   # 成功与成就
    LOW_POINT = "低谷情节"    # 失败与痛苦
    TURNING_POINT = "转折情节" # 人生方向改变
    NUCLEAR = "留恋情节"      # 深刻记忆


@dataclass
class PlotEpisode:
    """核心情节"""
    plot_type: str
    plot_type_en: str
    content: str
    emotion: str
    identity_implication: str


@dataclass
class IdentityTransformation:
    """身份转变"""
    old_identity: str
    trigger: str
    new_identity: str
    transformation_type: str


@dataclass
class IdentityAnalysisResult:
    """身份分析结果"""
    narrative_tone: str
    tone_confidence: float
    tone_evidence: List[str]
    plot_episodes: List[PlotEpisode]
    identity_transformation: Optional[IdentityTransformation]
    key_phrases: List[str]


# 叙事基调识别模式
TONE_PATTERNS = {
    NarrativeTone.REDEMPTION: {
        "sequence": ["困境", "转折", "成长"],
        "keywords": ["但是后来", "然而最终", "经历之后", "从中学会", "变得更强"],
        "patterns": [
            r"(痛苦|困难|失败).{0,30}(成长|坚强|学到|明白)",
            r"(挫折|打击).{0,30}(机会|转折|动力)",
            r"回头看.{0,20}(值得|正确)"
        ]
    },
    NarrativeTone.CONTAMINATION: {
        "sequence": ["好事", "破坏"],
        "keywords": ["本来很好", "却", "毁了", "破坏", "直到"],
        "patterns": [
            r"(本来|原本).{0,20}(好|幸福|顺利).{0,30}(却|但是).{0,30}(毁|糟|糟)",
            r"直到.{0,20}(出事|发生)",
            r"美好.{0,30}(打破|毁灭)"
        ]
    },
    NarrativeTone.PROGRESSIVE: {
        "sequence": ["持续向上"],
        "keywords": ["一直在进步", "越来越好", "不断提升", "持续成长"],
        "patterns": [
            r"一直(在)?(进步|努力|成长)",
            r"(越来)?越好",
            r"不断(提升|进步)"
        ]
    },
    NarrativeTone.REGRESSIVE: {
        "sequence": ["持续下降"],
        "keywords": ["越来越糟", "每况愈下", "不断下降", "走下坡路"],
        "patterns": [
            r"(越来)?越(糟|差|坏)",
            r"每况愈下",
            r"走下坡路"
        ]
    }
}


# 情节类型识别模式
PLOT_PATTERNS = {
    PlotType.HIGH_POINT: {
        "keywords": ["成功", "胜利", "成就", "高兴", "最骄傲"],
        "patterns": [
            r"(最|特别)(高兴|骄傲|开心)",
            r"(成功|胜利|成就)",
            r"(实现了|达到了).{0,20}(目标|梦想)"
        ],
        "emotion": "积极",
        "identity": "能力确认"
    },
    PlotType.LOW_POINT: {
        "keywords": ["失败", "痛苦", "打击", "难过", "最艰难"],
        "patterns": [
            r"(最|特别)(难过|痛苦|艰难)",
            r"(失败|打击|挫折)",
            r"跌入(谷底|低谷)"
        ],
        "emotion": "消极",
        "identity": "成长契机"
    },
    PlotType.TURNING_POINT: {
        "keywords": ["转折", "改变", "决定", "选择", "从此"],
        "patterns": [
            r"(转折点|分水岭)",
            r"(从那|从此).{0,20}(改变|不同)",
            r"决定了.{0,20}(改变|转变)"
        ],
        "emotion": "中性/复杂",
        "identity": "身份转变"
    },
    PlotType.NUCLEAR: {
        "keywords": ["永远记住", "难以忘怀", "印象深刻", "记得很清楚"],
        "patterns": [
            r"(永远|一直)(记得|记住)",
            r"(难以|无法)(忘怀|忘记)",
            r"印象(特别|非常)深刻"
        ],
        "emotion": "复杂",
        "identity": "情感纽带"
    }
}


def analyze_tone(text: str) -> Tuple[str, float, List[str]]:
    """分析叙事基调
    
    Args:
        text: 叙事文本
        
    Returns:
        (基调类型, 置信度, 证据列表)
    """
    scores = {}
    evidences = {}
    
    for tone, info in TONE_PATTERNS.items():
        score = 0
        evidence = []
        
        # 关键词匹配
        for keyword in info["keywords"]:
            if keyword in text:
                score += 1
                evidence.append(f"关键词: {keyword}")
        
        # 模式匹配
        for pattern in info["patterns"]:
            matches = re.findall(pattern, text)
            if matches:
                score += len(matches)
                evidence.append(f"模式匹配: {matches[0][:30]}...")
        
        scores[tone] = score
        evidences[tone] = evidence
    
    if max(scores.values()) == 0:
        return "无法确定", 0.0, []
    
    best_tone = max(scores, key=scores.get)
    total_score = sum(scores.values())
    confidence = scores[best_tone] / total_score if total_score > 0 else 0
    
    return best_tone.value, confidence, evidences[best_tone]


def identify_plots(text: str) -> List[PlotEpisode]:
    """识别核心情节
    
    Args:
        text: 叙事文本
        
    Returns:
        情节列表
    """
    plots = []
    
    for plot_type, info in PLOT_PATTERNS.items():
        # 查找匹配的情节
        for pattern in info["patterns"]:
            matches = re.finditer(pattern, text)
            for match in matches:
                # 提取上下文
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 50)
                content = text[start:end]
                
                plot = PlotEpisode(
                    plot_type=plot_type.value,
                    plot_type_en=plot_type.name,
                    content=content,
                    emotion=info["emotion"],
                    identity_implication=info["identity"]
                )
                plots.append(plot)
    
    # 去重（按内容相似性）
    unique_plots = []
    seen_content = set()
    for plot in plots:
        if plot.content[:30] not in seen_content:
            seen_content.add(plot.content[:30])
            unique_plots.append(plot)
    
    return unique_plots


def analyze_identity(text: str) -> Optional[IdentityTransformation]:
    """分析身份建构
    
    Args:
        text: 叙事文本
        
    Returns:
        身份转变分析
    """
    # 寻找身份转变模式
    patterns = [
        # "从...变成..."
        (r"从.{0,20}(变成|变为|转变为).{0,20}", "became"),
        # "以前..., 现在..."
        (r"以前.{0,30}现在.{0,30}", "temporal"),
        # "让我(明白/懂得/认识到)"
        (r"让我(明白|懂得|认识到).{0,30}", "realization"),
        # "真正的我"
        (r"这才是(真正的|真实的)我", "self-discovery"),
    ]
    
    for pattern, trans_type in patterns:
        match = re.search(pattern, text)
        if match:
            matched_text = match.group(0)
            
            # 尝试提取旧身份和新身份
            if trans_type == "became":
                parts = re.split(r"变成|变为|转变为", matched_text)
                if len(parts) == 2:
                    return IdentityTransformation(
                        old_identity=parts[0].strip(),
                        trigger="转变过程",
                        new_identity=parts[1].strip(),
                        transformation_type="主动转变"
                    )
            
            elif trans_type == "temporal":
                parts = re.split(r"现在", matched_text)
                if len(parts) == 2:
                    return IdentityTransformation(
                        old_identity=parts[0].replace("以前", "").strip(),
                        trigger="时间推移",
                        new_identity=parts[1].strip(),
                        transformation_type="渐进转变"
                    )
            
            elif trans_type == "realization":
                return IdentityTransformation(
                    old_identity="认知转变前",
                    trigger=matched_text,
                    new_identity="认知转变后",
                    transformation_type="认知转变"
                )
            
            elif trans_type == "self-discovery":
                return IdentityTransformation(
                    old_identity="虚假自我",
                    trigger="自我发现",
                    new_identity="真实自我",
                    transformation_type="自我发现"
                )
    
    return None


def extract_key_phrases(text: str) -> List[str]:
    """提取关键短语
    
    Args:
        text: 叙事文本
        
    Returns:
        关键短语列表
    """
    phrases = []
    
    # 身份相关短语
    identity_patterns = [
        r"我是.{0,10}",
        r"我觉得.{0,15}",
        r"我学到了.{0,15}",
        r"这让我.{0,15}",
        r"(真正的|真实的)我"
    ]
    
    for pattern in identity_patterns:
        matches = re.findall(pattern, text)
        phrases.extend(matches[:2])
    
    return phrases[:10]


def analyze_identity_full(text: str) -> IdentityAnalysisResult:
    """完整身份分析
    
    Args:
        text: 叙事文本
        
    Returns:
        完整分析结果
    """
    tone, confidence, evidence = analyze_tone(text)
    plots = identify_plots(text)
    transformation = analyze_identity(text)
    key_phrases = extract_key_phrases(text)
    
    return IdentityAnalysisResult(
        narrative_tone=tone,
        tone_confidence=confidence,
        tone_evidence=evidence,
        plot_episodes=plots,
        identity_transformation=transformation,
        key_phrases=key_phrases
    )


def print_identity_report(result: IdentityAnalysisResult):
    """打印身份分析报告"""
    print("\n" + "="*60)
    print("叙事认同分析报告 (McAdams框架)")
    print("="*60)
    
    print("\n【叙事基调】")
    print(f"  类型: {result.narrative_tone}")
    print(f"  置信度: {result.tone_confidence:.1%}")
    if result.tone_evidence:
        print("  证据:")
        for e in result.tone_evidence[:3]:
            print(f"    • {e[:50]}...")
    
    if result.plot_episodes:
        print("\n【核心情节】")
        for plot in result.plot_episodes[:5]:
            print(f"\n  ▶ {plot.plot_type}")
            print(f"    情感: {plot.emotion}")
            print(f"    身份意义: {plot.identity_implication}")
            print(f"    内容: {plot.content[:40]}...")
    
    if result.identity_transformation:
        t = result.identity_transformation
        print("\n【身份转变】")
        print(f"  旧身份: {t.old_identity}")
        print(f"  触发: {t.trigger}")
        print(f"  新身份: {t.new_identity}")
        print(f"  转变类型: {t.transformation_type}")
    
    if result.key_phrases:
        print("\n【关键短语】")
        for phrase in result.key_phrases:
            print(f"  • {phrase}")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description="叙事认同分析工具")
    parser.add_argument("--input", type=str, help="直接输入叙事文本")
    parser.add_argument("--file", type=str, help="从文件读取叙事文本")
    parser.add_argument("--tone", action="store_true", help="分析叙事基调")
    parser.add_argument("--plot", action="store_true", help="识别核心情节")
    parser.add_argument("--identity", action="store_true", help="分析身份建构")
    parser.add_argument("--output", type=str, help="输出文件路径（JSON格式）")
    
    args = parser.parse_args()
    
    # 获取输入文本
    if args.input:
        text = args.input
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = """
        我在IT行业干了十五年，做到了技术总监的位置。表面看起来很成功，薪水也不错。
        但说实话，那种日子很空虚。每天面对代码和项目，感觉自己在消耗生命。
        转折点是2020年疫情期间，我在线上给一些年轻人做职业辅导。
        有个学生后来给我发信息说，我的建议改变了他的人生方向。
        那一刻我突然意识到，我真正想要的是影响人，而不是影响代码。
        后来我辞掉了总监职位，去一所大学做职业发展导师。
        现在收入确实比以前少，但每天早上醒来都充满期待。
        回头看，那个决定是对的。这才是真正的我。
        """
    
    if args.tone or args.plot or args.identity:
        result = analyze_identity_full(text.strip())
        print_identity_report(result)
        
        if args.output:
            output_data = asdict(result)
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"\n结果已保存到: {args.output}")
    else:
        # 默认：完整分析
        result = analyze_identity_full(text.strip())
        print_identity_report(result)


if __name__ == "__main__":
    main()
