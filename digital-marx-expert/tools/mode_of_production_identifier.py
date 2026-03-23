#!/usr/bin/env python3
"""
digital-marx-expert - 生产方式识别工具
识别社会生产方式：资本主义、社会主义、封建主义等
基于马克思历史唯物主义
"""

from typing import Dict, List, Any
import re
import json


# 生产方式指标
MODE_OF_PRODUCTION_INDICATORS = {
    # 资本主义
    "capitalist": {
        "production_relations": [
            "雇佣劳动",
            "私有制",
            "资本",
            "利润",
            "市场",
            " wage labor ",
            " private property ",
            " capital ",
            " profit ",
            " market ",
        ],
        "class_structure": [
            "资产阶级",
            "无产阶级",
            "资本家",
            "工人",
            " bourgeoisie ",
            " proletariat ",
            " capitalist ",
            " worker ",
        ],
        "description": "资本主义生产方式",
    },
    # 社会主义
    "socialist": {
        "production_relations": [
            "公有制",
            "国有制",
            "计划经济",
            "集体所有制",
            " public ownership ",
            " state ownership ",
            " planned economy ",
        ],
        "class_structure": [
            "工人阶级",
            "农民",
            "劳动者",
            " working class ",
            " peasant ",
            " laborer ",
        ],
        "description": "社会主义生产方式",
    },
    # 封建主义
    "feudal": {
        "production_relations": [
            "封建土地所有制",
            "农奴",
            "地主",
            "佃农",
            " feudal land ",
            " serf ",
            " landlord ",
        ],
        "class_structure": [
            "地主",
            "农奴",
            "农民",
            "封建主",
            " lord ",
            " vassal ",
        ],
        "description": "封建主义生产方式",
    },
    # 奴隶制
    "slave": {
        "production_relations": [
            "奴隶制",
            "奴隶主",
            "奴隶",
            "人身依附",
            " slavery ",
            " slave owner ",
            " slave ",
        ],
        "class_structure": [
            "奴隶主",
            "奴隶",
            " slave owner ",
            " slave ",
        ],
        "description": "奴隶制生产方式",
    },
    # 数字资本主义
    "digital_capitalist": {
        "production_relations": [
            "平台",
            "数据",
            "算法",
            "数字劳动",
            "零工",
            " platform ",
            " data ",
            " algorithm ",
            " gig work ",
        ],
        "class_structure": [
            "平台资本家",
            "数字无产阶级",
            "用户",
            "平台劳动者",
            " platform capitalist ",
            " digital proletariat ",
        ],
        "description": "数字资本主义",
    },
}


class ModeOfProductionIdentifier:
    """生产方式识别器"""

    def __init__(self):
        self.identification_results = []

    def identify_mode_of_production(
        self, data: Any, historical_context: str = None
    ) -> Dict:
        """
        识别生产方式

        参数:
            data: 分析数据
            historical_context: 历史背景

        返回:
            生产方式识别结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 分析各生产方式指标
        capitalist = self._analyze_capitalist(text)
        socialist = self._analyze_socialist(text)
        feudal = self._analyze_feudal(text)
        slave = self._analyze_slave(text)
        digital = self._analyze_digital_capitalist(text)

        # 确定主导生产方式
        dominant = self._determine_dominant(
            capitalist, socialist, feudal, slave, digital
        )

        # 计算过渡特征
        transitional_features = self._identify_transitional_features(
            capitalist, socialist, feudal, digital
        )

        # 生成理论解释
        explanation = self._generate_explanation(dominant, transitional_features)

        return {
            "data_type": type(data).__name__,
            "historical_context": historical_context,
            "modes": {
                "capitalist": capitalist,
                "socialist": socialist,
                "feudal": feudal,
                "slave": slave,
                "digital_capitalist": digital,
            },
            "dominant_mode": dominant,
            "transitional_features": transitional_features,
            "explanation": explanation,
        }

    def _convert_to_text(self, data: Any) -> str:
        """将数据转换为文本"""
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            return json.dumps(data, ensure_ascii=False)
        elif isinstance(data, list):
            return " ".join(str(item) for item in data)
        else:
            return str(data)

    def _analyze_mode(self, mode_data: Dict, text: str) -> Dict:
        """分析特定生产方式"""
        prod_relations = mode_data.get("production_relations", [])
        class_structure = mode_data.get("class_structure", [])

        prod_count = sum(
            len(re.findall(kw, text, re.IGNORECASE)) for kw in prod_relations
        )
        class_count = sum(
            len(re.findall(kw, text, re.IGNORECASE)) for kw in class_structure
        )

        total_count = prod_count + class_count
        score = min(1.0, total_count / 5)

        return {
            "score": score,
            "evidence_count": total_count,
            "production_relations_evidence": prod_count,
            "class_structure_evidence": class_count,
            "description": mode_data.get("description", ""),
        }

    def _analyze_capitalist(self, text: str) -> Dict:
        return self._analyze_mode(MODE_OF_PRODUCTION_INDICATORS["capitalist"], text)

    def _analyze_socialist(self, text: str) -> Dict:
        return self._analyze_mode(MODE_OF_PRODUCTION_INDICATORS["socialist"], text)

    def _analyze_feudal(self, text: str) -> Dict:
        return self._analyze_mode(MODE_OF_PRODUCTION_INDICATORS["feudal"], text)

    def _analyze_slave(self, text: str) -> Dict:
        return self._analyze_mode(MODE_OF_PRODUCTION_INDICATORS["slave"], text)

    def _analyze_digital_capitalist(self, text: str) -> Dict:
        return self._analyze_mode(
            MODE_OF_PRODUCTION_INDICATORS["digital_capitalist"], text
        )

    def _determine_dominant(
        self,
        capitalist: Dict,
        socialist: Dict,
        feudal: Dict,
        slave: Dict,
        digital: Dict,
    ) -> str:
        """确定主导生产方式"""
        scores = {
            "资本主义": capitalist.get("score", 0),
            "社会主义": socialist.get("score", 0),
            "封建主义": feudal.get("score", 0),
            "奴隶制": slave.get("score", 0),
            "数字资本主义": digital.get("score", 0),
        }

        max_mode = max(scores, key=scores.get)
        max_score = scores[max_mode]

        if max_score < 0.2:
            return "未确定"
        return max_mode

    def _identify_transitional_features(
        self,
        capitalist: Dict,
        socialist: Dict,
        feudal: Dict,
        digital: Dict,
    ) -> List[str]:
        """识别过渡特征"""
        features = []

        # 检查是否存在过渡
        if feudal.get("score", 0) > 0.2 and capitalist.get("score", 0) > 0.2:
            features.append("封建主义向资本主义过渡")
        if capitalist.get("score", 0) > 0.2 and digital.get("score", 0) > 0.2:
            features.append("资本主义向数字资本主义转型")
        if socialist.get("score", 0) > 0.2 and capitalist.get("score", 0) > 0.2:
            features.append("社会主义与资本主义共存")

        return features

    def _generate_explanation(
        self, dominant: str, transitional_features: List[str]
    ) -> str:
        """生成理论解释"""
        explanations = {
            "资本主义": "以私有制为基础，通过雇佣劳动进行生产，追求利润最大化。",
            "社会主义": "以公有制为基础，计划经济为主导，追求社会公平。",
            "封建主义": "以封建土地所有制为基础，存在人身依附关系。",
            "奴隶制": "以奴隶主对奴隶的人身所有权为基础。",
            "数字资本主义": "以平台为中介，数据为核心生产资料，数字劳动为特征。",
            "未确定": "数据不足以确定生产方式。",
        }

        base = explanations.get(dominant, "")

        if transitional_features:
            base += f" 过渡特征: {'; '.join(transitional_features)}"

        return base


def identify_mode_of_production(data: Any, historical_context: str = None) -> Dict:
    """生产方式识别入口函数"""
    identifier = ModeOfProductionIdentifier()
    return identifier.identify_mode_of_production(data, historical_context)


if __name__ == "__main__":
    # 测试
    test_data = """
    该社会以雇佣劳动为基础，资本家占有生产资料，
    通过市场进行商品交换。存在资产阶级和无产阶级的对立。
    工人为资本家生产剩余价值。
    同时，平台经济发展迅速，数据成为新的生产资料。
    """

    result = identify_mode_of_production(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
