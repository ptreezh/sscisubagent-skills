#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扎根理论智能体核心推理引擎
负责用户请求分析、策略制定和技能调度
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UrgencyLevel(Enum):
    """紧急程度枚举"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

class ResearchStage(Enum):
    """研究阶段枚举"""
    INITIAL = "initial"
    DATA_PREPARATION = "data_preparation"
    OPEN_CODING = "open_coding"
    AXIAL_CODING = "axial_coding"
    SELECTIVE_CODING = "selective_coding"
    THEORY_BUILDING = "theory_building"
    SATURATION_CHECK = "saturation_check"
    COMPLETED = "completed"

class TaskType(Enum):
    """任务类型枚举"""
    CODING = "coding"
    ANALYSIS = "analysis"
    THEORY_BUILDING = "theory_building"
    QUALITY_CHECK = "quality_check"
    MEMO_WRITING = "memo_writing"
    COLLABORATION = "collaboration"

@dataclass
class UserContext:
    """用户上下文信息"""
    user_id: str
    urgency: UrgencyLevel
    stage: ResearchStage
    task_type: TaskType
    data_type: str
    data_size: int
    deadline: Optional[str] = None
    has_supervisor: bool = False
    collaboration_mode: bool = False

@dataclass
class ProcessingStrategy:
    """处理策略"""
    priority: int
    skills_to_use: List[str]
    quality_checks: List[str]
    output_format: str
    estimated_time: int
    requires_human_review: bool

class GroundedTheoryEngine:
    """扎根理论推理引擎"""
    
    def __init__(self):
        self.urgent_keywords = [
            "明天", "紧急", "催", "立即", "马上", "急", "赶紧", 
            "快点", "尽快", "deadline", "截止", " overdue"
        ]
        
        self.critical_keywords = [
            "今天", "现在", "立刻", "马上就要", "等不及", 
            "救急", "救命", "火烧眉毛"
        ]
        
        self.stage_keywords = {
            ResearchStage.DATA_PREPARATION: [
                "准备数据", "处理文本", "清洗数据", "格式化", "预处理"
            ],
            ResearchStage.OPEN_CODING: [
                "开放编码", "初始编码", "概念识别", "逐行编码", "编码"
            ],
            ResearchStage.AXIAL_CODING: [
                "轴心编码", "范畴", "归类", "属性维度", "关系"
            ],
            ResearchStage.SELECTIVE_CODING: [
                "选择式编码", "核心范畴", "故事线", "理论构建"
            ],
            ResearchStage.THEORY_BUILDING: [
                "理论", "模型", "框架", "整合", "构建"
            ],
            ResearchStage.SATURATION_CHECK: [
                "饱和度", "检验", "验证", "充分性", "完善"
            ]
        }
        
        self.task_keywords = {
            TaskType.CODING: ["编码", "coding", "概念", "范畴"],
            TaskType.ANALYSIS: ["分析", "analysis", "解读", "解释"],
            TaskType.THEORY_BUILDING: ["理论", "theory", "模型", "框架"],
            TaskType.QUALITY_CHECK: ["检查", "验证", "质量", "审核"],
            TaskType.MEMO_WRITING: ["备忘录", "memo", "记录", "反思"],
            TaskType.COLLABORATION: ["协作", "合作", "团队", "多人"]
        }
        
        # 加载策略规则
        self.strategy_rules = self._load_strategy_rules()
    
    def analyze_user_request(self, request: str, user_id: str) -> Tuple[UserContext, ProcessingStrategy]:
        """
        分析用户请求，生成上下文和处理策略
        
        Args:
            request: 用户请求文本
            user_id: 用户ID
            
        Returns:
            Tuple[UserContext, ProcessingStrategy]: 用户上下文和处理策略
        """
        logger.info(f"分析用户请求: {request[:50]}...")
        
        # 1. 检测紧急程度
        urgency = self._detect_urgency(request)
        
        # 2. 检测研究阶段
        stage = self._detect_research_stage(request)
        
        # 3. 检测任务类型
        task_type = self._detect_task_type(request)
        
        # 4. 提取数据信息
        data_info = self._extract_data_info(request)
        
        # 5. 构建用户上下文
        context = UserContext(
            user_id=user_id,
            urgency=urgency,
            stage=stage,
            task_type=task_type,
            data_type=data_info["type"],
            data_size=data_info["size"],
            deadline=data_info.get("deadline"),
            has_supervisor=data_info.get("has_supervisor", False),
            collaboration_mode=data_info.get("collaboration", False)
        )
        
        # 6. 生成处理策略
        strategy = self._generate_strategy(context)
        
        logger.info(f"生成策略: 优先级={strategy.priority}, 技能={strategy.skills_to_use}")
        
        return context, strategy
    
    def _detect_urgency(self, request: str) -> UrgencyLevel:
        """检测紧急程度"""
        request_lower = request.lower()
        
        # 检查关键紧急词
        if any(keyword in request_lower for keyword in self.critical_keywords):
            return UrgencyLevel.CRITICAL
        
        if any(keyword in request_lower for keyword in self.urgent_keywords):
            return UrgencyLevel.HIGH
        
        # 检查时间表达式
        time_patterns = [
            r"今天.*?要", r"明天.*?要", r"\d+小时.*?要", 
            r"下午.*?要", r"晚上.*?要"
        ]
        
        for pattern in time_patterns:
            if re.search(pattern, request):
                return UrgencyLevel.HIGH
        
        return UrgencyLevel.NORMAL
    
    def _detect_research_stage(self, request: str) -> ResearchStage:
        """检测研究阶段"""
        request_lower = request.lower()
        
        # 计算每个阶段的匹配分数
        stage_scores = {}
        for stage, keywords in self.stage_keywords.items():
            score = sum(1 for keyword in keywords if keyword in request_lower)
            stage_scores[stage] = score
        
        # 返回得分最高的阶段
        if stage_scores:
            best_stage = max(stage_scores, key=stage_scores.get)
            if stage_scores[best_stage] > 0:
                return best_stage
        
        return ResearchStage.INITIAL
    
    def _detect_task_type(self, request: str) -> TaskType:
        """检测任务类型"""
        request_lower = request.lower()
        
        # 计算每个任务类型的匹配分数
        task_scores = {}
        for task_type, keywords in self.task_keywords.items():
            score = sum(1 for keyword in keywords if keyword in request_lower)
            task_scores[task_type] = score
        
        # 返回得分最高的任务类型
        if task_scores:
            best_task = max(task_scores, key=task_scores.get)
            if task_scores[best_task] > 0:
                return best_task
        
        return TaskType.ANALYSIS
    
    def _extract_data_info(self, request: str) -> Dict:
        """提取数据信息"""
        data_info = {"type": "unknown", "size": 0}
        
        # 检测数据类型
        data_types = {
            "访谈": ["访谈", "interview", "采访", "谈话"],
            "观察": ["观察", "observation", "记录", "现场"],
            "文档": ["文档", "document", "资料", "文献"],
            "问卷": ["问卷", "survey", "调查", "问答"]
        }
        
        for data_type, keywords in data_types.items():
            if any(keyword in request for keyword in keywords):
                data_info["type"] = data_type
                break
        
        # 提取数量信息
        number_patterns = [
            r"(\d+)个", r"(\d+)份", r"(\d+)位", r"(\d+)人",
            r"(\d+)篇", r"(\d+)章", r"(\d+)节"
        ]
        
        for pattern in number_patterns:
            match = re.search(pattern, request)
            if match:
                data_info["size"] = int(match.group(1))
                break
        
        # 检测截止时间
        deadline_patterns = [
            r"明天.*?前", r"今天.*?前", r"(\d+)号.*?前",
            r"周.*?前", r"月.*?前"
        ]
        
        for pattern in deadline_patterns:
            match = re.search(pattern, request)
            if match:
                data_info["deadline"] = match.group(0)
                break
        
        # 检测导师和协作
        data_info["has_supervisor"] = any(word in request for word in ["导师", "老师", "教授"])
        data_info["collaboration"] = any(word in request for word in ["团队", "合作", "协作", "多人"])
        
        return data_info
    
    def _generate_strategy(self, context: UserContext) -> ProcessingStrategy:
        """生成处理策略"""
        # 基础策略配置
        strategy = ProcessingStrategy(
            priority=1,
            skills_to_use=[],
            quality_checks=[],
            output_format="standard",
            estimated_time=30,
            requires_human_review=True
        )
        
        # 根据紧急程度调整策略
        if context.urgency == UrgencyLevel.CRITICAL:
            strategy.priority = 10
            strategy.estimated_time = 5
            strategy.requires_human_review = False
            strategy.output_format = "quick"
        elif context.urgency == UrgencyLevel.HIGH:
            strategy.priority = 7
            strategy.estimated_time = 15
            strategy.output_format = "concise"
        
        # 根据研究阶段选择技能
        stage_skills = {
            ResearchStage.DATA_PREPARATION: ["text_preprocessing"],
            ResearchStage.OPEN_CODING: ["performing-open-coding", "writing-grounded-theory-memos"],
            ResearchStage.AXIAL_CODING: ["performing-axial-coding", "writing-grounded-theory-memos"],
            ResearchStage.SELECTIVE_CODING: ["performing-selective-coding", "writing-grounded-theory-memos"],
            ResearchStage.THEORY_BUILDING: ["performing-selective-coding", "checking-theory-saturation"],
            ResearchStage.SATURATION_CHECK: ["checking-theory-saturation"]
        }
        
        if context.stage in stage_skills:
            strategy.skills_to_use.extend(stage_skills[context.stage])
        
        # 根据任务类型添加技能
        task_skills = {
            TaskType.CODING: ["performing-open-coding"],
            TaskType.ANALYSIS: ["performing-axial-coding"],
            TaskType.THEORY_BUILDING: ["performing-selective-coding"],
            TaskType.QUALITY_CHECK: ["checking-theory-saturation"],
            TaskType.MEMO_WRITING: ["writing-grounded-theory-memos"],
            TaskType.COLLABORATION: ["collaborative-coding"]
        }
        
        if context.task_type in task_skills:
            for skill in task_skills[context.task_type]:
                if skill not in strategy.skills_to_use:
                    strategy.skills_to_use.append(skill)
        
        # 添加质量检查
        quality_checks = ["naming_conventions", "definition_completeness", "example_sufficiency"]
        if context.urgency != UrgencyLevel.CRITICAL:
            strategy.quality_checks.extend(quality_checks)
        
        return strategy
    
    def _load_strategy_rules(self) -> Dict:
        """加载策略规则"""
        return {
            "urgency_multipliers": {
                UrgencyLevel.CRITICAL: 0.2,
                UrgencyLevel.HIGH: 0.5,
                UrgencyLevel.NORMAL: 1.0,
                UrgencyLevel.LOW: 1.5
            },
            "stage_complexity": {
                ResearchStage.DATA_PREPARATION: 1,
                ResearchStage.OPEN_CODING: 3,
                ResearchStage.AXIAL_CODING: 4,
                ResearchStage.SELECTIVE_CODING: 5,
                ResearchStage.THEORY_BUILDING: 6,
                ResearchStage.SATURATION_CHECK: 2
            },
            "task_priorities": {
                TaskType.CODING: 3,
                TaskType.ANALYSIS: 2,
                TaskType.THEORY_BUILDING: 4,
                TaskType.QUALITY_CHECK: 1,
                TaskType.MEMO_WRITING: 2,
                TaskType.COLLABORATION: 3
            }
        }

# 使用示例
if __name__ == "__main__":
    engine = GroundedTheoryEngine()
    
    # 测试用例
    test_requests = [
        "我明天就要交开放编码结果，有20份访谈需要编码",
        "导师催我交轴心编码，需要建立范畴体系",
        "我们团队正在进行理论构建，需要整合所有编码结果",
        "请帮我检查理论饱和度，确保数据充分性"
    ]
    
    for i, request in enumerate(test_requests):
        print(f"\n测试用例 {i+1}: {request}")
        context, strategy = engine.analyze_user_request(request, f"user_{i}")
        
        print(f"紧急程度: {context.urgency.value}")
        print(f"研究阶段: {context.stage.value}")
        print(f"任务类型: {context.task_type.value}")
        print(f"数据类型: {context.data_type}")
        print(f"数据规模: {context.data_size}")
        print(f"策略优先级: {strategy.priority}")
        print(f"使用技能: {strategy.skills_to_use}")
        print(f"预计时间: {strategy.estimated_time}分钟")