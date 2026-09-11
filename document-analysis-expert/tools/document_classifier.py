#!/usr/bin/env python3
"""文档分类器 - 识别和分类文档类型"""

import argparse
import json
import re
from datetime import datetime
from typing import Dict, Any, List, Tuple

class DocumentClassifier:
    """文档分类器"""
    
    def __init__(self):
        self.doc_types = {
            "policy": ["政策", "规定", "条例", "办法", "通知", "policy", "regulation", "act"],
            "organizational": ["报告", "纪要", "备忘录", "计划", "report", "memo", "minutes"],
            "personal": ["日记", "信件", "回忆录", "diary", "letter", "memoir"],
            "media": ["新闻", "报道", "评论", "news", "article", "commentary"],
            "academic": ["论文", "研究报告", "paper", "study", "research"]
        }
        
        self.authenticity_indicators = {
            "official_seal": r"印章|盖章|official seal",
            "signature": r"签名|签字|signature",
            "date": r"\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2}",
            "reference_number": r"[编号|文号|No\.].*"
        }
    
    def classify(self, text: str, metadata: Dict = None) -> Dict[str, Any]:
        """
        分类文档
        
        Args:
            text: 文档文本
            metadata: 元数据
            
        Returns:
            分类结果
        """
        result = {
            "document_type": self._identify_type(text),
            "authenticity": self._assess_authenticity(text, metadata),
            "formality": self._assess_formality(text),
            "authority_level": self._assess_authority(text),
            "target_audience": self._identify_audience(text),
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _identify_type(self, text: str) -> Tuple[str, float]:
        """识别文档类型"""
        scores = {}
        
        for doc_type, keywords in self.doc_types.items():
            score = sum(1 for kw in keywords if kw.lower() in text.lower())
            scores[doc_type] = score / len(keywords)
        
        if max(scores.values()) == 0:
            return ("unknown", 0.0)
        
        best_type = max(scores, key=scores.get)
        return (best_type, scores[best_type])
    
    def _assess_authenticity(self, text: str, metadata: Dict = None) -> Dict:
        """评估真实性"""
        indicators = {}
        
        for indicator, pattern in self.authenticity_indicators.items():
            match = re.search(pattern, text)
            indicators[indicator] = bool(match)
        
        authenticity_score = sum(indicators.values()) / len(indicators)
        
        return {
            "score": authenticity_score,
            "indicators": indicators,
            "assessment": "high" if authenticity_score > 0.6 else "medium" if authenticity_score > 0.3 else "low"
        }
    
    def _assess_formality(self, text: str) -> str:
        """评估正式程度"""
        formal_markers = ["兹", "鉴于", "特此", "如下", "根据", "现将"]
        informal_markers = ["呵呵", "哈哈", "吧", "呢", "嘛"]
        
        formal_count = sum(1 for m in formal_markers if m in text)
        informal_count = sum(1 for m in informal_markers if m in text)
        
        if formal_count > informal_count:
            return "formal"
        elif informal_count > formal_count:
            return "informal"
        else:
            return "semi-formal"
    
    def _assess_authority(self, text: str) -> str:
        """评估权威程度"""
        authority_markers = ["政府", "部委", "公司", "机构", "部门"]
        
        for marker in authority_markers:
            if marker in text:
                return "institutional"
        
        personal_markers = ["我", "本人", "笔者"]
        for marker in personal_markers:
            if marker in text:
                return "personal"
        
        return "unknown"
    
    def _identify_audience(self, text: str) -> List[str]:
        """识别目标受众"""
        audiences = []
        
        if "广大市民" in text or "公众" in text:
            audiences.append("general_public")
        if "员工" in text or "职工" in text:
            audiences.append("employees")
        if "学生" in text:
            audiences.append("students")
        if "领导" in text or "上级" in text:
            audiences.append("superiors")
        
        return audiences if audiences else ["unspecified"]

def main():
    parser = argparse.ArgumentParser(description="文档分类器")
    parser.add_argument("--text", "-t", help="文档文本")
    parser.add_argument("--file", "-f", help="文档文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    text = args.text or ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as file:
            text = file.read()
    
    if not text:
        text = "这是一份关于政策规定的正式文件，特此通知所有员工。"
    
    classifier = DocumentClassifier()
    result = classifier.classify(text)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[完成] 结果已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
