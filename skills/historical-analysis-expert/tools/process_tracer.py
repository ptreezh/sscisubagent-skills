#!/usr/bin/env python3
"""过程追踪器 - 追踪历史过程演变"""

import argparse
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

class ProcessTracer:
    """过程追踪器"""
    
    def __init__(self):
        self.phases = []
        self.events = []
        self.mechanisms = []
    
    def add_phase(self, name: str, start: str, end: str, 
                  characteristics: List[str] = None) -> None:
        """添加阶段"""
        self.phases.append({
            "name": name,
            "start": start,
            "end": end,
            "characteristics": characteristics or [],
            "order": len(self.phases)
        })
    
    def add_event(self, name: str, date: str, phase: str = None,
                  significance: str = None) -> None:
        """添加事件"""
        self.events.append({
            "name": name,
            "date": date,
            "phase": phase,
            "significance": significance
        })
    
    def add_mechanism(self, name: str, description: str,
                      evidence: List[str] = None) -> None:
        """添加机制"""
        self.mechanisms.append({
            "name": name,
            "description": description,
            "evidence": evidence or []
        })
    
    def trace(self) -> Dict[str, Any]:
        """
        执行过程追踪
        
        Returns:
            追踪结果
        """
        result = {
            "phase_count": len(self.phases),
            "event_count": len(self.events),
            "mechanism_count": len(self.mechanisms),
            "timeline": self._build_timeline(),
            "critical_junctures": self._identify_junctures(),
            "mechanism_chain": self._build_mechanism_chain(),
            "process_summary": self._summarize_process(),
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _build_timeline(self) -> List[Dict]:
        """构建时间线"""
        timeline = []
        
        # 按阶段组织事件
        for phase in self.phases:
            phase_events = [e for e in self.events if e["phase"] == phase["name"]]
            timeline.append({
                "phase": phase["name"],
                "period": f"{phase['start']} - {phase['end']}",
                "characteristics": phase["characteristics"],
                "events": [{"name": e["name"], "date": e["date"], 
                           "significance": e["significance"]} for e in phase_events]
            })
        
        return timeline
    
    def _identify_junctures(self) -> List[Dict]:
        """识别关键节点"""
        junctures = []
        
        for event in self.events:
            if event["significance"] in ["high", "critical", "关键", "重大"]:
                junctures.append({
                    "event": event["name"],
                    "date": event["date"],
                    "significance": event["significance"]
                })
        
        # 阶段转换点也是关键节点
        for i in range(len(self.phases) - 1):
            junctures.append({
                "event": f"阶段转换: {self.phases[i]['name']} → {self.phases[i+1]['name']}",
                "date": self.phases[i]["end"],
                "significance": "phase_transition"
            })
        
        return junctures
    
    def _build_mechanism_chain(self) -> List[Dict]:
        """构建机制链"""
        return [
            {
                "mechanism": m["name"],
                "description": m["description"],
                "evidence_count": len(m["evidence"])
            }
            for m in self.mechanisms
        ]
    
    def _summarize_process(self) -> Dict:
        """总结过程"""
        if not self.phases:
            return {"summary": "无阶段信息"}
        
        return {
            "total_period": f"{self.phases[0]['start']} - {self.phases[-1]['end']}",
            "phase_names": [p["name"] for p in self.phases],
            "key_mechanisms": [m["name"] for m in self.mechanisms],
            "critical_events": [e["name"] for e in self.events 
                              if e["significance"] in ["high", "critical", "关键", "重大"]]
        }
    
    def identify_path_dependence(self) -> Dict:
        """识别路径依赖"""
        return {
            "early_decisions": [e["name"] for e in self.events[:3]] if len(self.events) >= 3 else [],
            "lock_in_points": [j for j in self._identify_junctures() 
                              if j["significance"] == "critical"],
            "interpretation": "早期事件可能锁定后续发展路径"
        }

def main():
    parser = argparse.ArgumentParser(description="过程追踪器")
    parser.add_argument("--process", "-p", help="过程数据JSON文件")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    tracer = ProcessTracer()
    
    # 默认示例：社会运动过程
    tracer.add_phase("酝酿期", "2010", "2012", ["不满积累", "组织萌芽"])
    tracer.add_phase("爆发期", "2012", "2013", ["大规模动员", "冲突升级"])
    tracer.add_phase("转折期", "2013", "2014", ["政府回应", "运动分化"])
    tracer.add_phase("沉淀期", "2014", "2016", ["制度变革", "影响持续"])
    
    tracer.add_event("经济危机爆发", "2010-05", "酝酿期", "critical")
    tracer.add_event("组织成立", "2011-03", "酝酿期", "high")
    tracer.add_event("大规模游行", "2012-06", "爆发期", "critical")
    tracer.add_event("政府妥协", "2013-09", "转折期", "critical")
    tracer.add_event("新法通过", "2014-06", "沉淀期", "high")
    
    tracer.add_mechanism("经济压力传导", "危机→不满→动员", ["经济数据", "抗议记录"])
    tracer.add_mechanism("政治机会开放", "政府软弱→机会→行动", ["政治分析"])
    
    if args.process:
        with open(args.process, "r", encoding="utf-8") as f:
            data = json.load(f)
            tracer.phases = data.get("phases", [])
            tracer.events = data.get("events", [])
            tracer.mechanisms = data.get("mechanisms", [])
    
    result = tracer.trace()
    result["path_dependence"] = tracer.identify_path_dependence()
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[完成] 结果已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
