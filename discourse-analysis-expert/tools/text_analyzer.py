#!/usr/bin/env python3
"""
文本分析工具

功能: 文本层面的语言学分析（词汇、语法、结构）
用法: python text_analyzer.py [选项]

选项:
  --lexical FILE      词汇分析
  --grammatical FILE  语法分析
  --structure FILE    结构分析
  --full FILE         完整分析
"""

import argparse
import json
import re
from typing import Dict, List, Tuple

class TextAnalyzer:
    """文本分析器"""
    
    # 评价性词汇词典
    POSITIVE_WORDS = ["优秀", "杰出", "成功", "进步", "发展", "贡献", "积极", "创新"]
    NEGATIVE_WORDS = ["失败", "问题", "危机", "威胁", "困难", "挑战", "负面", "严重"]
    
    # 隐喻关键词
    METAPHOR_PATTERNS = {
        "战争隐喻": ["战斗", "抗击", "战胜", "进攻", "防守", "战役"],
        "疾病隐喻": ["病", "症状", "感染", "治疗", "治愈", "污染"],
        "水流隐喻": ["涌入", "流出", "潮流", "波及", "泛滥", "源头"],
        "建筑隐喻": ["构建", "建设", "基础", "结构", "框架", "支撑"]
    }
    
    # 过程类型关键词
    PROCESS_INDICATORS = {
        "物质过程": ["做", "进行", "实施", "推进", "开展", "完成"],
        "心理过程": ["认为", "觉得", "感到", "相信", "希望", "担心"],
        "关系过程": ["是", "成为", "代表", "意味着", "等于"],
        "言语过程": ["说", "表示", "指出", "强调", "声称", "宣称"]
    }
    
    # 情态词
    MODALITY_WORDS = {
        "高认识情态": ["一定", "必然", "肯定", "确定", "绝对"],
        "中认识情态": ["可能", "也许", "或许", "大概"],
        "低认识情态": ["好像", "似乎", "仿佛"],
        "高道义情态": ["必须", "应该", "一定要"],
        "中道义情态": ["需要", "应当", "得"],
        "低道义情态": ["可以", "能够", "可能"]
    }
    
    def __init__(self):
        pass
    
    def lexical_analysis(self, text: str) -> Dict:
        """词汇分析"""
        results = {
            "evaluation": self._analyze_evaluation(text),
            "metaphor": self._analyze_metaphor(text),
            "word_frequency": self._analyze_frequency(text)
        }
        return results
    
    def grammatical_analysis(self, text: str) -> Dict:
        """语法分析"""
        results = {
            "transitivity": self._analyze_transitivity(text),
            "modality": self._analyze_modality(text),
            "voice": self._analyze_voice(text)
        }
        return results
    
    def structure_analysis(self, text: str) -> Dict:
        """结构分析"""
        results = {
            "paragraphs": len(text.split('\n\n')),
            "sentences": len(re.split(r'[。！？]', text)),
            "cohesion": self._analyze_cohesion(text)
        }
        return results
    
    def full_analysis(self, text: str) -> Dict:
        """完整分析"""
        return {
            "lexical": self.lexical_analysis(text),
            "grammatical": self.grammatical_analysis(text),
            "structure": self.structure_analysis(text)
        }
    
    def _analyze_evaluation(self, text: str) -> Dict:
        """评价分析"""
        positive = [w for w in self.POSITIVE_WORDS if w in text]
        negative = [w for w in self.NEGATIVE_WORDS if w in text]
        return {
            "positive_words": positive,
            "negative_words": negative,
            "evaluation_ratio": len(positive) / (len(positive) + len(negative)) if (positive or negative) else 0.5
        }
    
    def _analyze_metaphor(self, text: str) -> Dict:
        """隐喻分析"""
        metaphors = {}
        for metaphor_type, keywords in self.METAPHOR_PATTERNS.items():
            found = [kw for kw in keywords if kw in text]
            if found:
                metaphors[metaphor_type] = found
        return metaphors
    
    def _analyze_frequency(self, text: str) -> Dict:
        """词频分析"""
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True)[:20])
    
    def _analyze_transitivity(self, text: str) -> Dict:
        """及物性分析"""
        processes = {}
        for process_type, indicators in self.PROCESS_INDICATORS.items():
            found = [ind for ind in indicators if ind in text]
            if found:
                processes[process_type] = found
        return processes
    
    def _analyze_modality(self, text: str) -> Dict:
        """情态分析"""
        modality = {}
        for mod_type, words in self.MODALITY_WORDS.items():
            found = [w for w in words if w in text]
            if found:
                modality[mod_type] = found
        return modality
    
    def _analyze_voice(self, text: str) -> Dict:
        """语态分析"""
        passive_pattern = r'被[\u4e00-\u9fa5]+[动词]'
        passive_matches = re.findall(passive_pattern, text)
        
        return {
            "passive_count": len(passive_matches),
            "passive_examples": passive_matches[:5]
        }
    
    def _analyze_cohesion(self, text: str) -> Dict:
        """衔接分析"""
        # 代词
        pronouns = re.findall(r'[他她它我你咱们这那]', text)
        # 连接词
        connectors = re.findall(r'[但是然而因此所以虽然如果]', text)
        
        return {
            "pronoun_count": len(pronouns),
            "connector_count": len(connectors)
        }


def main():
    parser = argparse.ArgumentParser(description="文本分析工具")
    parser.add_argument("--lexical", type=str, help="词汇分析")
    parser.add_argument("--grammatical", type=str, help="语法分析")
    parser.add_argument("--structure", type=str, help="结构分析")
    parser.add_argument("--full", type=str, help="完整分析")
    
    args = parser.parse_args()
    
    analyzer = TextAnalyzer()
    
    if args.lexical:
        with open(args.lexical, 'r', encoding='utf-8') as f:
            text = f.read()
        results = analyzer.lexical_analysis(text)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.grammatical:
        with open(args.grammatical, 'r', encoding='utf-8') as f:
            text = f.read()
        results = analyzer.grammatical_analysis(text)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.structure:
        with open(args.structure, 'r', encoding='utf-8') as f:
            text = f.read()
        results = analyzer.structure_analysis(text)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.full:
        with open(args.full, 'r', encoding='utf-8') as f:
            text = f.read()
        results = analyzer.full_analysis(text)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
