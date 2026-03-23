#!/usr/bin/env python3
"""内容结构分析器 - 分析文档内容和结构"""

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from typing import Dict, Any, List, Tuple

class ContentStructureAnalyzer:
    """内容结构分析器"""
    
    def __init__(self):
        self.stopwords = {"的", "是", "在", "了", "和", "与", "或", "等", "这", "那"}
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        分析文档内容和结构
        
        Args:
            text: 文档文本
            
        Returns:
            分析结果
        """
        result = {
            "structure": self._analyze_structure(text),
            "content": self._analyze_content(text),
            "themes": self._extract_themes(text),
            "narrative": self._analyze_narrative(text),
            "discourse": self._analyze_discourse(text),
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _analyze_structure(self, text: str) -> Dict:
        """分析文档结构"""
        # 章节识别
        sections = re.split(r'\n\n+|\n第[一二三四五六七八九十]+[章节部]|\n\d+\.', text)
        sections = [s.strip() for s in sections if s.strip()]
        
        # 段落统计
        paragraphs = [p for p in text.split('\n') if p.strip()]
        
        # 句子统计
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s for s in sentences if s.strip()]
        
        return {
            "section_count": len(sections),
            "paragraph_count": len(paragraphs),
            "sentence_count": len(sentences),
            "char_count": len(text),
            "sections": sections[:5] if sections else []  # 前5个章节
        }
    
    def _analyze_content(self, text: str) -> Dict:
        """分析内容特征"""
        # 关键词提取
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        words = [w for w in words if w not in self.stopwords]
        word_freq = Counter(words).most_common(10)
        
        # 实体识别（简化）
        dates = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2}', text)
        numbers = re.findall(r'\d+(?:\.\d+)?(?:万|亿|%)?', text)
        
        return {
            "top_words": word_freq,
            "date_mentions": dates[:5],
            "number_mentions": numbers[:5]
        }
    
    def _extract_themes(self, text: str) -> List[Dict]:
        """提取主题"""
        themes = []
        
        theme_patterns = {
            "政策主题": r"政策|规定|办法|条例",
            "经济主题": r"经济|发展|投资|市场",
            "社会主题": r"社会|民生|群众|人民",
            "技术主题": r"技术|创新|数字化|智能",
            "管理主题": r"管理|组织|制度|流程"
        }
        
        for theme, pattern in theme_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                themes.append({
                    "name": theme,
                    "frequency": len(matches),
                    "keywords": list(set(matches))
                })
        
        return sorted(themes, key=lambda x: x["frequency"], reverse=True)
    
    def _analyze_narrative(self, text: str) -> Dict:
        """分析叙事特征"""
        # 时态分析
        past_markers = ["曾", "已经", "曾经", "过去"]
        present_markers = ["正在", "现在", "目前"]
        future_markers = ["将", "将要", "未来", "预计"]
        
        past_count = sum(1 for m in past_markers if m in text)
        present_count = sum(1 for m in present_markers if m in text)
        future_count = sum(1 for m in future_markers if m in text)
        
        # 视角分析
        first_person = len(re.findall(r'我|我们|本人', text))
        third_person = len(re.findall(r'他|她|他们|其', text))
        
        return {
            "temporal_focus": {
                "past": past_count,
                "present": present_count,
                "future": future_count,
                "dominant": "past" if past_count > max(present_count, future_count) else
                           "present" if present_count > future_count else "future"
            },
            "perspective": {
                "first_person": first_person,
                "third_person": third_person,
                "dominant": "first" if first_person > third_person else "third"
            }
        }
    
    def _analyze_discourse(self, text: str) -> Dict:
        """分析话语特征"""
        # 情态分析
        necessity = len(re.findall(r'必须|应当|需要|要', text))
        possibility = len(re.findall(r'可能|可以|能够|也许', text))
        
        # 语气分析
        declarative = len(re.findall(r'[。]', text))
        interrogative = len(re.findall(r'[？?]', text))
        imperative = len(re.findall(r'[！!]', text))
        
        return {
            "modality": {
                "necessity": necessity,
                "possibility": possibility
            },
            "mood": {
                "declarative": declarative,
                "interrogative": interrogative,
                "imperative": imperative,
                "dominant": "declarative" if declarative > max(interrogative, imperative) else
                           "interrogative" if interrogative > imperative else "imperative"
            }
        }

def main():
    parser = argparse.ArgumentParser(description="内容结构分析器")
    parser.add_argument("--text", "-t", help="文档文本")
    parser.add_argument("--file", "-f", help="文档文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    text = args.text or ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as file:
            text = file.read()
    
    if not text:
        text = "这是一份关于政策规定的正式文件。我们必须认真执行各项规定。未来将继续推进改革发展。"
    
    analyzer = ContentStructureAnalyzer()
    result = analyzer.analyze(text)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[完成] 结果已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
