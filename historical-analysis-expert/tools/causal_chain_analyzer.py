#!/usr/bin/env python3
"""因果链分析器 - 分析历史事件的因果链"""

import argparse
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple

class CausalChainAnalyzer:
    """因果链分析器"""
    
    def __init__(self):
        self.chain = []
        self.evidence = {}
    
    def add_link(self, cause: str, effect: str, 
                 evidence: List[str] = None, 
                 mechanism: str = None) -> None:
        """添加因果链环节"""
        link = {
            "cause": cause,
            "effect": effect,
            "evidence": evidence or [],
            "mechanism": mechanism,
            "order": len(self.chain)
        }
        self.chain.append(link)
    
    def analyze(self) -> Dict[str, Any]:
        """
        分析因果链
        
        Returns:
            分析结果
        """
        result = {
            "chain_length": len(self.chain),
            "chain_summary": [],
            "completeness": self._assess_completeness(),
            "alternative_paths": self._identify_alternatives(),
            "critical_links": self._identify_critical_links(),
            "timestamp": datetime.now().isoformat()
        }
        
        for link in self.chain:
            result["chain_summary"].append({
                "step": link["order"] + 1,
                "cause": link["cause"],
                "effect": link["effect"],
                "evidence_count": len(link["evidence"]),
                "mechanism": link["mechanism"]
            })
        
        return result
    
    def _assess_completeness(self) -> Dict:
        """评估证据完整性"""
        total_links = len(self.chain)
        links_with_evidence = sum(1 for link in self.chain if link["evidence"])
        links_with_mechanism = sum(1 for link in self.chain if link["mechanism"])
        
        return {
            "evidence_coverage": links_with_evidence / total_links if total_links > 0 else 0,
            "mechanism_coverage": links_with_mechanism / total_links if total_links > 0 else 0,
            "assessment": "complete" if links_with_evidence == total_links else "incomplete"
        }
    
    def _identify_alternatives(self) -> List[Dict]:
        """识别替代路径"""
        alternatives = []
        
        for i, link in enumerate(self.chain):
            if len(link["evidence"]) < 2:
                alternatives.append({
                    "at_step": i + 1,
                    "from": link["cause"],
                    "note": "证据不足，存在替代解释可能"
                })
        
        return alternatives
    
    def _identify_critical_links(self) -> List[int]:
        """识别关键环节"""
        critical = []
        
        for i, link in enumerate(self.chain):
            if link["mechanism"] and len(link["evidence"]) >= 2:
                critical.append(i + 1)
        
        return critical
    
    def counterfactual(self, step: int, remove: bool = True) -> Dict:
        """
        反事实推理
        
        Args:
            step: 要修改的步骤
            remove: 是否移除该步骤
            
        Returns:
            反事实分析结果
        """
        if step < 1 or step > len(self.chain):
            return {"error": "无效步骤"}
        
        original_chain = [link["effect"] for link in self.chain]
        
        if remove:
            # 移除该步骤后的链条
            remaining = original_chain[:step-1]
            lost_effects = original_chain[step-1:]
        
        return {
            "original_outcome": original_chain[-1] if original_chain else None,
            "counterfactual_outcome": "不确定" if len(remaining) < len(original_chain) else remaining[-1],
            "removed_step": step,
            "lost_effects": lost_effects if remove else [],
            "interpretation": f"如果步骤{step}没有发生，后续{len(lost_effects)}个环节可能不会发生"
        }

def main():
    parser = argparse.ArgumentParser(description="因果链分析器")
    parser.add_argument("--chain", "-c", help="因果链JSON文件")
    parser.add_argument("--counterfactual", "-f", type=int, help="反事实推理步骤")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    analyzer = CausalChainAnalyzer()
    
    # 默认示例
    analyzer.add_link("经济危机", "政治动荡", ["档案记录", "报刊报道"], "经济压力传导")
    analyzer.add_link("政治动荡", "社会运动", ["参与者的回忆录"], "政治机会开放")
    analyzer.add_link("社会运动", "制度变革", ["官方文件", "法律文本"], "压力倒逼改革")
    
    if args.chain:
        with open(args.chain, "r", encoding="utf-8") as f:
            chain_data = json.load(f)
            analyzer.chain = chain_data.get("chain", [])
    
    result = analyzer.analyze()
    
    if args.counterfactual:
        result["counterfactual_analysis"] = analyzer.counterfactual(args.counterfactual)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[完成] 结果已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
