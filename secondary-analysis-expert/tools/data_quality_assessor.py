#!/usr/bin/env python3
"""数据质量评估器 - 评估二手数据质量"""

import argparse
import json
from datetime import datetime
from typing import Dict, Any, List

class DataQualityAssessor:
    """数据质量评估器"""
    
    def __init__(self):
        self.quality_dimensions = {
            "conceptual_validity": {
                "name": "概念效度",
                "weight": 0.25,
                "indicators": ["测量是否有效", "概念是否匹配", "效度检验结果"]
            },
            "sample_representativeness": {
                "name": "样本代表性",
                "weight": 0.25,
                "indicators": ["抽样方法", "响应率", "样本量"]
            },
            "data_completeness": {
                "name": "数据完整性",
                "weight": 0.20,
                "indicators": ["缺失率", "变量完整性", "记录完整性"]
            },
            "measurement_reliability": {
                "name": "测量可靠性",
                "weight": 0.15,
                "indicators": ["信度系数", "测量一致性", "重测信度"]
            },
            "documentation_quality": {
                "name": "文档质量",
                "weight": 0.15,
                "indicators": ["文档完整性", "编码说明", "技术报告"]
            }
        }
    
    def assess(self, data_info: Dict) -> Dict[str, Any]:
        """
        评估数据质量
        
        Args:
            data_info: 数据信息字典
            
        Returns:
            质量评估结果
        """
        result = {
            "overall_score": 0,
            "dimensions": {},
            "suitability": {},
            "limitations": [],
            "recommendations": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # 评估各维度
        for dim_key, dim_info in self.quality_dimensions.items():
            score = data_info.get(dim_key, 0.5)  # 默认中等
            if isinstance(score, bool):
                score = 1.0 if score else 0.0
            
            result["dimensions"][dim_key] = {
                "name": dim_info["name"],
                "score": score,
                "weight": dim_info["weight"],
                "weighted_score": score * dim_info["weight"],
                "indicators": dim_info["indicators"]
            }
        
        # 计算总分
        result["overall_score"] = sum(
            d["weighted_score"] for d in result["dimensions"].values()
        )
        
        # 评估适用性
        result["suitability"] = self._assess_suitability(result["overall_score"])
        
        # 识别限制
        result["limitations"] = self._identify_limitations(result)
        
        # 提出建议
        result["recommendations"] = self._generate_recommendations(result)
        
        return result
    
    def _assess_suitability(self, score: float) -> Dict:
        """评估适用性"""
        if score >= 0.8:
            return {
                "level": "high",
                "description": "数据质量高，适合研究使用"
            }
        elif score >= 0.6:
            return {
                "level": "medium",
                "description": "数据质量中等，需注意限制"
            }
        else:
            return {
                "level": "low",
                "description": "数据质量较低，需谨慎使用"
            }
    
    def _identify_limitations(self, result: Dict) -> List[str]:
        """识别数据限制"""
        limitations = []
        
        for dim_key, dim_data in result["dimensions"].items():
            if dim_data["score"] < 0.6:
                limitations.append(f"{dim_data['name']}较低")
        
        return limitations
    
    def _generate_recommendations(self, result: Dict) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if result["dimensions"]["sample_representativeness"]["score"] < 0.6:
            recommendations.append("建议评估样本偏差对结论的影响")
        
        if result["dimensions"]["data_completeness"]["score"] < 0.6:
            recommendations.append("建议处理缺失数据或报告缺失情况")
        
        if result["dimensions"]["measurement_reliability"]["score"] < 0.6:
            recommendations.append("建议检验测量可靠性或使用替代指标")
        
        return recommendations

def main():
    parser = argparse.ArgumentParser(description="数据质量评估器")
    parser.add_argument("--data-info", "-d", help="数据信息JSON文件")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 默认数据信息
    data_info = {
        "conceptual_validity": 0.8,
        "sample_representativeness": 0.7,
        "data_completeness": 0.9,
        "measurement_reliability": 0.75,
        "documentation_quality": 0.85
    }
    
    if args.data_info:
        with open(args.data_info, "r", encoding="utf-8") as f:
            data_info = json.load(f)
    
    assessor = DataQualityAssessor()
    result = assessor.assess(data_info)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[完成] 结果已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
