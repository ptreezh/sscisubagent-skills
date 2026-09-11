#!/usr/bin/env python3
"""文档语境追踪器 - 追踪文档生产和使用语境"""

import argparse
import json
import re
from datetime import datetime
from typing import Dict, Any, List

class DocumentContextTracer:
    """文档语境追踪器"""
    
    def __init__(self):
        self.production_indicators = {
            "author": r"作者|编写|起草|制定",
            "organization": r"单位|机构|部门|委员会",
            "date": r"\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2}",
            "purpose": r"目的|为|为了|根据|依据",
            "authorization": r"批准|审定|审核|同意"
        }
        
        self.circulation_indicators = {
            "distribution": r"印发|发布|公开|传达",
            "audience": r"各|有关|全体|相关人员",
            "scope": r"范围内|内部|公开|保密"
        }
        
        self.usage_indicators = {
            "implementation": r"执行|实施|落实|贯彻",
            "reference": r"参照|依据|根据|按照",
            "modification": r"修改|修订|补充|调整"
        }
    
    def trace(self, text: str, metadata: Dict = None) -> Dict[str, Any]:
        """
        追踪文档语境
        
        Args:
            text: 文档文本
            metadata: 元数据
            
        Returns:
            语境追踪结果
        """
        result = {
            "production": self._trace_production(text),
            "circulation": self._trace_circulation(text),
            "usage": self._trace_usage(text),
            "power_relations": self._analyze_power(text),
            "document_life": self._assess_life_stage(text),
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _trace_production(self, text: str) -> Dict:
        """追踪生产语境"""
        production = {}
        
        # 作者/起草者
        author_match = re.search(self.production_indicators["author"] + r"[:：]?\s*(.+?)(?:\n|$)", text)
        production["author"] = author_match.group(1).strip() if author_match else "未明确"
        
        # 组织
        org_match = re.search(self.production_indicators["organization"] + r"[:：]?\s*(.+?)(?:\n|$)", text)
        production["organization"] = org_match.group(1).strip() if org_match else "未明确"
        
        # 日期
        date_match = re.search(self.production_indicators["date"], text)
        production["date"] = date_match.group() if date_match else "未明确"
        
        # 目的
        purpose_matches = re.findall(self.production_indicators["purpose"] + r"[，,]?(.+?)(?:[，,。]|$)", text)
        production["purpose"] = purpose_matches[:3] if purpose_matches else ["未明确"]
        
        # 授权
        auth_match = re.search(self.production_indicators["authorization"] + r"[:：]?\s*(.+?)(?:\n|$)", text)
        production["authorization"] = auth_match.group(1).strip() if auth_match else "未明确"
        
        return production
    
    def _trace_circulation(self, text: str) -> Dict:
        """追踪流通过程"""
        circulation = {}
        
        # 分发方式
        dist_match = re.search(self.circulation_indicators["distribution"] + r"[:：]?\s*(.+?)(?:\n|$)", text)
        circulation["distribution_method"] = dist_match.group(1).strip() if dist_match else "未明确"
        
        # 受众
        audience_matches = re.findall(self.circulation_indicators["audience"] + r"(.+?)(?:[，,：:]|$)", text)
        circulation["target_audience"] = audience_matches[:3] if audience_matches else ["未明确"]
        
        # 范围
        scope_match = re.search(self.circulation_indicators["scope"], text)
        circulation["scope"] = scope_match.group() if scope_match else "未明确"
        
        return circulation
    
    def _trace_usage(self, text: str) -> Dict:
        """追踪使用语境"""
        usage = {}
        
        # 实施指示
        impl_matches = re.findall(self.usage_indicators["implementation"] + r"(.+?)(?:[，,。]|$)", text)
        usage["implementation_directives"] = impl_matches[:3] if impl_matches else []
        
        # 参照依据
        ref_matches = re.findall(self.usage_indicators["reference"] + r"(.+?)(?:[，,。]|$)", text)
        usage["reference_points"] = ref_matches[:3] if ref_matches else []
        
        # 修改记录
        mod_matches = re.findall(self.usage_indicators["modification"] + r"(.+?)(?:[，,。]|$)", text)
        usage["modification_history"] = mod_matches[:3] if mod_matches else []
        
        return usage
    
    def _analyze_power(self, text: str) -> Dict:
        """分析权力关系"""
        power = {}
        
        # 权威来源
        authority_sources = []
        if "政府" in text:
            authority_sources.append("政府权威")
        if "法律" in text:
            authority_sources.append("法律权威")
        if "制度" in text:
            authority_sources.append("制度权威")
        if "专业" in text:
            authority_sources.append("专业权威")
        
        power["authority_sources"] = authority_sources if authority_sources else ["未明确"]
        
        # 权力指向
        power_direction = "top-down" if "必须" in text or "应当" in text else \
                         "bottom-up" if "建议" in text or "请" in text else "neutral"
        power["power_direction"] = power_direction
        
        return power
    
    def _assess_life_stage(self, text: str) -> str:
        """评估文档生命阶段"""
        if "废止" in text or "失效" in text:
            return "archived"
        elif "修订" in text or "修改" in text:
            return "revised"
        elif "实施" in text or "执行" in text:
            return "active"
        elif "草案" in text or "征求意见" in text:
            return "draft"
        else:
            return "unknown"

def main():
    parser = argparse.ArgumentParser(description="文档语境追踪器")
    parser.add_argument("--text", "-t", help="文档文本")
    parser.add_argument("--file", "-f", help="文档文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    text = args.text or ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as file:
            text = file.read()
    
    if not text:
        text = "根据国务院规定，本部门制定以下办法。现印发各单位执行。"
    
    tracer = DocumentContextTracer()
    result = tracer.trace(text)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[完成] 结果已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
