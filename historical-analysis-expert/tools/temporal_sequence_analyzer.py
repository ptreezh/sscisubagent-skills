#!/usr/bin/env python3
"""时序序列分析器 - 分析历史事件的时序关系"""

import argparse
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple

class TemporalSequenceAnalyzer:
    """时序序列分析器"""
    
    def __init__(self):
        self.sequence = []
        self.temporal_relations = {
            "before": [],    # A在B之前
            "after": [],     # A在B之后
            "during": [],    # A发生在B期间
            "simultaneous": []  # A与B同时发生
        }
    
    def add_event(self, name: str, date: str, 
                  duration: int = 1, attributes: Dict = None) -> None:
        """添加事件"""
        self.sequence.append({
            "name": name,
            "date": date,
            "duration": duration,
            "attributes": attributes or {},
            "order": len(self.sequence)
        })
    
    def analyze_sequence(self) -> Dict[str, Any]:
        """
        分析事件序列
        
        Returns:
            序列分析结果
        """
        result = {
            "event_count": len(self.sequence),
            "sequence_order": [],
            "temporal_patterns": self._identify_patterns(),
            "critical_transitions": self._find_transitions(),
            "rhythm_analysis": self._analyze_rhythm(),
            "sequence_type": self._classify_sequence(),
            "timestamp": datetime.now().isoformat()
        }
        
        # 排序后的事件列表
        sorted_events = sorted(self.sequence, key=lambda x: x["date"])
        result["sequence_order"] = [
            {"name": e["name"], "date": e["date"], "duration": e["duration"]}
            for e in sorted_events
        ]
        
        return result
    
    def _identify_patterns(self) -> List[Dict]:
        """识别时序模式"""
        patterns = []
        
        if len(self.sequence) < 2:
            return patterns
        
        sorted_events = sorted(self.sequence, key=lambda x: x["date"])
        
        # 识别连续事件
        for i in range(len(sorted_events) - 1):
            current = sorted_events[i]
            next_event = sorted_events[i + 1]
            
            if current["duration"] > 1:
                patterns.append({
                    "type": "overlapping",
                    "events": [current["name"], next_event["name"]],
                    "description": f"{current['name']}与{next_event['name']}时间重叠"
                })
        
        # 识别聚集事件
        date_groups = {}
        for event in sorted_events:
            year = event["date"][:4] if len(event["date"]) >= 4 else event["date"]
            if year not in date_groups:
                date_groups[year] = []
            date_groups[year].append(event["name"])
        
        for year, events in date_groups.items():
            if len(events) > 2:
                patterns.append({
                    "type": "clustering",
                    "period": year,
                    "events": events,
                    "description": f"{year}年发生{len(events)}个重要事件"
                })
        
        return patterns
    
    def _find_transitions(self) -> List[Dict]:
        """识别关键转折"""
        transitions = []
        
        sorted_events = sorted(self.sequence, key=lambda x: x["date"])
        
        for i in range(len(sorted_events) - 1):
            current = sorted_events[i]
            next_event = sorted_events[i + 1]
            
            # 事件属性变化指示转折
            if current["attributes"].get("type") != next_event["attributes"].get("type"):
                transitions.append({
                    "position": i + 1,
                    "from": current["name"],
                    "to": next_event["name"],
                    "type": "attribute_change"
                })
        
        return transitions
    
    def _analyze_rhythm(self) -> Dict:
        """分析变化节奏"""
        if len(self.sequence) < 3:
            return {"rhythm": "insufficient_data"}
        
        sorted_events = sorted(self.sequence, key=lambda x: x["date"])
        
        # 计算事件间隔
        intervals = []
        for i in range(len(sorted_events) - 1):
            # 简化：假设日期格式为YYYY或YYYY-MM
            try:
                year1 = int(sorted_events[i]["date"][:4])
                year2 = int(sorted_events[i + 1]["date"][:4])
                intervals.append(year2 - year1)
            except (ValueError, IndexError):
                continue
        
        if not intervals:
            return {"rhythm": "unknown"}
        
        avg_interval = sum(intervals) / len(intervals)
        
        if avg_interval < 1:
            rhythm = "rapid"
        elif avg_interval < 3:
            rhythm = "moderate"
        else:
            rhythm = "slow"
        
        return {
            "rhythm": rhythm,
            "average_interval": avg_interval,
            "min_interval": min(intervals),
            "max_interval": max(intervals)
        }
    
    def _classify_sequence(self) -> str:
        """分类序列类型"""
        if len(self.sequence) < 3:
            return "short_sequence"
        
        transitions = self._find_transitions()
        patterns = self._identify_patterns()
        
        if len(transitions) > len(self.sequence) / 2:
            return "episodic"
        elif any(p["type"] == "clustering" for p in patterns):
            return "clustered"
        else:
            return "linear"
    
    def check_sequence_necessity(self) -> Dict:
        """检查序列必要性"""
        return {
            "sequence_length": len(self.sequence),
            "necessary_sequence": True,  # 简化假设
            "interpretation": "事件顺序对结果有重要影响"
        }

def main():
    parser = argparse.ArgumentParser(description="时序序列分析器")
    parser.add_argument("--sequence", "-s", help="序列数据JSON文件")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    analyzer = TemporalSequenceAnalyzer()
    
    # 默认示例
    analyzer.add_event("危机爆发", "2010-05", 1, {"type": "trigger"})
    analyzer.add_event("初步应对", "2010-06", 2, {"type": "response"})
    analyzer.add_event("事态升级", "2011-03", 3, {"type": "escalation"})
    analyzer.add_event("关键转折", "2011-09", 1, {"type": "turning_point"})
    analyzer.add_event("制度变革", "2012-06", 12, {"type": "outcome"})
    
    if args.sequence:
        with open(args.sequence, "r", encoding="utf-8") as f:
            data = json.load(f)
            analyzer.sequence = data.get("sequence", [])
    
    result = analyzer.analyze_sequence()
    result["necessity_check"] = analyzer.check_sequence_necessity()
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[完成] 结果已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
