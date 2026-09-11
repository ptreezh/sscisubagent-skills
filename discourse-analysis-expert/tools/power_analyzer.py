#!/usr/bin/env python3
"""
权力与意识形态分析工具

功能: 分析话语中的权力关系和意识形态效果
用法: python power_analyzer.py [选项]

选项:
  --ideology FILE     意识形态分析
  --power FILE        权力关系分析
  --discourse-strategy FILE  话语策略分析
"""

import argparse
import json
import re
from typing import Dict, List, Tuple

class PowerAnalyzer:
    """权力与意识形态分析器"""
    
    # 内群体/外群体词汇
    INGROUP_MARKERS = ["我们", "咱们", "我国", "我党", "人民"]
    OUTGROUP_MARKERS = ["他们", "那些", "敌对", "异己", "外来"]
    
    # 合法化策略词汇
    LEGITIMATION_PATTERNS = {
        "权威合法化": ["专家", "研究", "证明", "数据", "官方"],
        "道德合法化": ["应该", "责任", "义务", "道德", "正义"],
        "历史合法化": ["历史", "传统", "一贯", "历来", "始终"],
        "理性合法化": ["理性", "科学", "客观", "合理", "正确"]
    }
    
    # 自然化词汇
    NATURALIZATION_MARKERS = ["自然", "正常", "显然", "当然", "必然", "理所当然"]
    
    # 排除机制词汇
    EXCLUSION_PATTERNS = {
        "边缘化": ["少数", "边缘", "非主流", "异端"],
        "沉默": ["不予置评", "未提及", "被忽视"],
        "否定": ["不可能", "不存在", "错误", "荒谬"]
    }
    
    def __init__(self):
        pass
    
    def ideology_analysis(self, text: str) -> Dict:
        """意识形态分析"""
        return {
            "naturalization": self._analyze_naturalization(text),
            "commonsense": self._analyze_commonsense(text),
            "legitimation": self._analyze_legitimation(text),
            "exclusion": self._analyze_exclusion(text)
        }
    
    def power_analysis(self, text: str) -> Dict:
        """权力关系分析"""
        return {
            "group_construction": self._analyze_group_construction(text),
            "voice_distribution": self._analyze_voice_distribution(text),
            "power_asymmetry": self._analyze_power_asymmetry(text)
        }
    
    def discourse_strategy_analysis(self, text: str) -> Dict:
        """话语策略分析（Wodak框架）"""
        return {
            "referential": self._analyze_referential_strategy(text),
            "predicational": self._analyze_predicational_strategy(text),
            "argumentation": self._analyze_argumentation_strategy(text),
            "perspectivization": self._analyze_perspectivization_strategy(text),
            "intensification": self._analyze_intensification_strategy(text)
        }
    
    def _analyze_naturalization(self, text: str) -> Dict:
        """自然化分析"""
        found = [marker for marker in self.NATURALIZATION_MARKERS if marker in text]
        return {
            "naturalization_markers": found,
            "naturalization_count": len(found),
            "interpretation": "话语尝试将特定观点自然化为'常识'" if found else "未检测到明显自然化策略"
        }
    
    def _analyze_commonsense(self, text: str) -> Dict:
        """常识建构分析"""
        commonsense_patterns = [
            r'大家都知道[，。]',
            r'众所周知[，。]',
            r'谁都清楚[，。]',
            r'不言而喻[，。]'
        ]
        
        found = []
        for pattern in commonsense_patterns:
            matches = re.findall(pattern, text)
            found.extend(matches)
        
        return {
            "commonsense_patterns": found,
            "function": "建构话语权威，封闭质疑空间" if found else "未检测到明显常识建构"
        }
    
    def _analyze_legitimation(self, text: str) -> Dict:
        """合法化策略分析"""
        strategies = {}
        for strategy, keywords in self.LEGITIMATION_PATTERNS.items():
            found = [kw for kw in keywords if kw in text]
            if found:
                strategies[strategy] = found
        return strategies
    
    def _analyze_exclusion(self, text: str) -> Dict:
        """排除机制分析"""
        exclusion = {}
        for mechanism, patterns in self.EXCLUSION_PATTERNS.items():
            found = [p for p in patterns if p in text]
            if found:
                exclusion[mechanism] = found
        return exclusion
    
    def _analyze_group_construction(self, text: str) -> Dict:
        """群体建构分析"""
        ingroup = [m for m in self.INGROUP_MARKERS if m in text]
        outgroup = [m for m in self.OUTGROUP_MARKERS if m in text]
        
        return {
            "ingroup_markers": ingroup,
            "outgroup_markers": outgroup,
            "binary_construction": bool(ingroup and outgroup),
            "interpretation": "话语建构了'我们-他们'二元对立" if (ingroup and outgroup) else "未检测到明显二元对立"
        }
    
    def _analyze_voice_distribution(self, text: str) -> Dict:
        """声音分布分析"""
        # 引用分析
        direct_quotes = re.findall(r'"[^"]+"', text)
        indirect_quotes = re.findall(r'据[^，。]+[，。]', text)
        
        return {
            "direct_quotes": len(direct_quotes),
            "indirect_quotes": len(indirect_quotes),
            "quote_examples": direct_quotes[:3]
        }
    
    def _analyze_power_asymmetry(self, text: str) -> Dict:
        """权力不对称分析"""
        # 施事分析
        agent_patterns = [
            (r'政府[^\s]*[推进实施开展]', "政府作为施事"),
            (r'人民[^\s]*[要求希望期待]', "人民作为主体"),
            (r'专家[^\s]*[指出认为建议]', "专家权威")
        ]
        
        findings = []
        for pattern, interpretation in agent_patterns:
            if re.search(pattern, text):
                findings.append(interpretation)
        
        return {
            "power_patterns": findings,
            "interpretation": "检测到话语权力分布模式" if findings else "需进一步语境分析"
        }
    
    def _analyze_referential_strategy(self, text: str) -> Dict:
        """指称策略分析"""
        ingroup = [m for m in self.INGROUP_MARKERS if m in text]
        outgroup = [m for m in self.OUTGROUP_MARKERS if m in text]
        
        return {
            "ingroup_naming": ingroup,
            "outgroup_naming": outgroup,
            "function": "建构群体身份边界"
        }
    
    def _analyze_predicational_strategy(self, text: str) -> Dict:
        """谓语策略分析"""
        # 正面定性
        positive_predicates = re.findall(r'[\u4e00-\u9fa5]+是[优秀杰出积极成功稳定]', text)
        # 负面定性
        negative_predicates = re.findall(r'[\u4e00-\u9fa5]+是[问题威胁危险困难]', text)
        
        return {
            "positive_predicates": positive_predicates[:3],
            "negative_predicates": negative_predicates[:3]
        }
    
    def _analyze_argumentation_strategy(self, text: str) -> Dict:
        """论证策略分析"""
        argumentation = {}
        
        # 诉诸权威
        if re.search(r'专家|研究|数据|证明', text):
            argumentation["诉诸权威"] = True
        # 诉诸因果
        if re.search(r'因为|所以|导致|造成', text):
            argumentation["诉诸因果"] = True
        # 诉诸历史
        if re.search(r'历史|传统|历来', text):
            argumentation["诉诸历史"] = True
        
        return argumentation
    
    def _analyze_perspectivization_strategy(self, text: str) -> Dict:
        """视角策略分析"""
        # 显性立场
        explicit_stance = re.findall(r'我认为|我相信|在我看来|我的观点', text)
        # 隐性立场
        implicit_stance = re.findall(r'显然|当然|毫无疑问', text)
        
        return {
            "explicit_stance": explicit_stance,
            "implicit_stance": implicit_stance,
            "stance_type": "显性" if explicit_stance else ("隐性" if implicit_stance else "需进一步分析")
        }
    
    def _analyze_intensification_strategy(self, text: str) -> Dict:
        """强化/弱化策略分析"""
        # 强化词
        intensifiers = re.findall(r'非常|极其|绝对|完全|一定', text)
        # 弱化词
        mitigators = re.findall(r'可能|也许|或许|似乎|大约', text)
        
        return {
            "intensifiers": intensifiers,
            "mitigators": mitigators,
            "strategy_type": "强化" if len(intensifiers) > len(mitigators) else ("弱化" if mitigators else "中性")
        }


def main():
    parser = argparse.ArgumentParser(description="权力与意识形态分析工具")
    parser.add_argument("--ideology", type=str, help="意识形态分析")
    parser.add_argument("--power", type=str, help="权力关系分析")
    parser.add_argument("--discourse-strategy", type=str, help="话语策略分析")
    
    args = parser.parse_args()
    
    analyzer = PowerAnalyzer()
    
    if args.ideology:
        with open(args.ideology, 'r', encoding='utf-8') as f:
            text = f.read()
        results = analyzer.ideology_analysis(text)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.power:
        with open(args.power, 'r', encoding='utf-8') as f:
            text = f.read()
        results = analyzer.power_analysis(text)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.discourse_strategy:
        with open(args.discourse_strategy, 'r', encoding='utf-8') as f:
            text = f.read()
        results = analyzer.discourse_strategy_analysis(text)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
