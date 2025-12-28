# 数据收集模块

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import threading
import time


class DataCollector:
    """收集用户使用数据和反馈"""
    
    def __init__(self, logs_dir: str = "cli-intent-matcher/data/user_logs"):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_file = self.logs_dir / "feedback.json"
        self.usage_log_file = self.logs_dir / "usage_log.json"
        self.lock = threading.Lock()  # 线程安全
    
    def log_user_interaction(self, user_input: str, predicted_tool: str, actual_tool: str = None, 
                           success: bool = True, feedback: str = None, timestamp: str = None) -> bool:
        """记录用户交互"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        interaction = {
            "timestamp": timestamp,
            "user_input": user_input,
            "predicted_tool": predicted_tool,
            "actual_tool": actual_tool,
            "success": success,
            "feedback": feedback
        }
        
        try:
            with self.lock:
                # 读取现有日志
                usage_logs = []
                if self.usage_log_file.exists():
                    with open(self.usage_log_file, 'r', encoding='utf-8') as f:
                        try:
                            usage_logs = json.load(f)
                        except json.JSONDecodeError:
                            usage_logs = []
                
                # 添加新日志
                usage_logs.append(interaction)
                
                # 限制日志数量，防止文件过大
                if len(usage_logs) > 1000:  # 保留最近1000条记录
                    usage_logs = usage_logs[-1000:]
                
                # 写入文件
                with open(self.usage_log_file, 'w', encoding='utf-8') as f:
                    json.dump(usage_logs, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"记录用户交互失败: {e}")
            return False
    
    def log_feedback(self, user_input: str, expected_tool: str, actual_tool: str, 
                    rating: int, comments: str = None) -> bool:
        """记录用户反馈"""
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "expected_tool": expected_tool,
            "actual_tool": actual_tool,
            "rating": rating,  # 1-5星评分
            "comments": comments
        }
        
        try:
            with self.lock:
                # 读取现有反馈
                feedback_logs = []
                if self.feedback_file.exists():
                    with open(self.feedback_file, 'r', encoding='utf-8') as f:
                        try:
                            feedback_logs = json.load(f)
                        except json.JSONDecodeError:
                            feedback_logs = []
                
                # 添加新反馈
                feedback_logs.append(feedback_entry)
                
                # 限制反馈数量
                if len(feedback_logs) > 500:  # 保留最近500条反馈
                    feedback_logs = feedback_logs[-500:]
                
                # 写入文件
                with open(self.feedback_file, 'w', encoding='utf-8') as f:
                    json.dump(feedback_logs, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"记录反馈失败: {e}")
            return False
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """获取使用统计信息"""
        stats = {
            "total_interactions": 0,
            "successful_interactions": 0,
            "failed_interactions": 0,
            "tool_usage": {},
            "time_range": {"start": None, "end": None},
            "avg_feedback_rating": 0.0
        }
        
        # 获取使用日志统计
        if self.usage_log_file.exists():
            with open(self.usage_log_file, 'r', encoding='utf-8') as f:
                try:
                    usage_logs = json.load(f)
                except json.JSONDecodeError:
                    usage_logs = []
            
            stats["total_interactions"] = len(usage_logs)
            stats["successful_interactions"] = sum(1 for log in usage_logs if log.get("success", False))
            stats["failed_interactions"] = stats["total_interactions"] - stats["successful_interactions"]
            
            # 统计工具使用情况
            for log in usage_logs:
                tool = log.get("predicted_tool", "unknown")
                if tool in stats["tool_usage"]:
                    stats["tool_usage"][tool] += 1
                else:
                    stats["tool_usage"][tool] = 1
            
            # 时间范围
            if usage_logs:
                stats["time_range"]["start"] = min(log["timestamp"] for log in usage_logs)
                stats["time_range"]["end"] = max(log["timestamp"] for log in usage_logs)
        
        # 获取反馈统计
        if self.feedback_file.exists():
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                try:
                    feedback_logs = json.load(f)
                except json.JSONDecodeError:
                    feedback_logs = []
            
            if feedback_logs:
                total_rating = sum(feedback.get("rating", 0) for feedback in feedback_logs)
                stats["avg_feedback_rating"] = total_rating / len(feedback_logs) if feedback_logs else 0.0
        
        return stats
    
    def get_recent_interactions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取最近的交互记录"""
        if not self.usage_log_file.exists():
            return []
        
        with open(self.usage_log_file, 'r', encoding='utf-8') as f:
            try:
                usage_logs = json.load(f)
            except json.JSONDecodeError:
                usage_logs = []
        
        # 按时间倒序排列并返回最近的记录
        usage_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return usage_logs[:limit]
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """获取反馈摘要"""
        if not self.feedback_file.exists():
            return {"total_feedback": 0, "avg_rating": 0.0, "rating_distribution": {}}
        
        with open(self.feedback_file, 'r', encoding='utf-8') as f:
            try:
                feedback_logs = json.load(f)
            except json.JSONDecodeError:
                feedback_logs = []
        
        if not feedback_logs:
            return {"total_feedback": 0, "avg_rating": 0.0, "rating_distribution": {}}
        
        total_rating = sum(feedback.get("rating", 0) for feedback in feedback_logs)
        avg_rating = total_rating / len(feedback_logs)
        
        # 评分分布
        rating_dist = {i: 0 for i in range(1, 6)}
        for feedback in feedback_logs:
            rating = feedback.get("rating", 0)
            if 1 <= rating <= 5:
                rating_dist[rating] += 1
        
        return {
            "total_feedback": len(feedback_logs),
            "avg_rating": round(avg_rating, 2),
            "rating_distribution": rating_dist
        }
    
    def clear_logs(self) -> bool:
        """清空日志（保留最近的几条用于演示）"""
        try:
            # 清空使用日志
            if self.usage_log_file.exists():
                with open(self.usage_log_file, 'r', encoding='utf-8') as f:
                    try:
                        usage_logs = json.load(f)
                    except json.JSONDecodeError:
                        usage_logs = []
                
                # 保留最近5条记录用于演示
                recent_logs = usage_logs[-5:] if len(usage_logs) > 5 else usage_logs
                with open(self.usage_log_file, 'w', encoding='utf-8') as f:
                    json.dump(recent_logs, f, indent=2, ensure_ascii=False)
            
            # 清空反馈日志
            if self.feedback_file.exists():
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    try:
                        feedback_logs = json.load(f)
                    except json.JSONDecodeError:
                        feedback_logs = []
                
                # 保留最近5条记录用于演示
                recent_feedback = feedback_logs[-5:] if len(feedback_logs) > 5 else feedback_logs
                with open(self.feedback_file, 'w', encoding='utf-8') as f:
                    json.dump(recent_feedback, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"清空日志失败: {e}")
            return False


def main():
    collector = DataCollector()
    
    # 演示记录交互
    collector.log_user_interaction(
        user_input="帮我写一份项目申请书",
        predicted_tool="stigmergy",
        actual_tool="stigmergy",
        success=True,
        feedback="很好，推荐的工具很合适"
    )
    
    # 演示记录反馈
    collector.log_feedback(
        user_input="帮我写一份项目申请书",
        expected_tool="stigmergy",
        actual_tool="stigmergy",
        rating=5,
        comments="推荐很准确"
    )
    
    # 获取统计信息
    stats = collector.get_usage_statistics()
    print("使用统计:", stats)
    
    # 获取反馈摘要
    feedback_summary = collector.get_feedback_summary()
    print("反馈摘要:", feedback_summary)


if __name__ == "__main__":
    main()