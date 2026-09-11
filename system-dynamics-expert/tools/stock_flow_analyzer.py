#!/usr/bin/env python3
"""
system-dynamics-expert - 库存流分析工具
分析系统动力学中的库存和流量
"""

from typing import Dict, List
import json


class StockFlowAnalyzer:
    """库存流分析器"""

    def __init__(self):
        pass

    def analyze(self, stocks: List[Dict], flows: List[Dict]) -> Dict:
        """分析库存流结构"""
        # 构建库存方程
        equations = self._build_equations(stocks, flows)

        # 识别时间延迟
        delays = self._find_delays(flows)

        # 识别非线性关系
        nonlinear = self._find_nonlinear(flows)

        return {
            "stocks": stocks,
            "flows": flows,
            "equations": equations,
            "delays": delays,
            "nonlinearities": nonlinear,
            "summary": f"分析{len(stocks)}个库存和{len(flows)}个流量",
        }

    def _build_equations(self, stocks: List[Dict], flows: List[Dict]) -> Dict:
        equations = {}
        for stock in stocks:
            in_flows = [f for f in flows if f.get("to") == stock.get("name")]
            out_flows = [f for f in flows if f.get("from") == stock.get("name")]

            eq = f"d({stock.get('name')})/dt = "
            if in_flows:
                eq += " + ".join(f.get("name", "") for f in in_flows) + " - "
            if out_flows:
                eq += " - ".join(f.get("name", "") for f in out_flows)
            else:
                eq = eq.rstrip(" - ")

            equations[stock.get("name")] = eq
        return equations

    def _find_delays(self, flows: List[Dict]) -> List[Dict]:
        return [f for f in flows if f.get("delay")]

    def _find_nonlinear(self, flows: List[Dict]) -> List[Dict]:
        return [f for f in flows if f.get("type") == "nonlinear"]


def analyze_stock_flow(stocks: List[Dict], flows: List[Dict]) -> Dict:
    return StockFlowAnalyzer().analyze(stocks, flows)


if __name__ == "__main__":
    test_stocks = [{"name": "population"}]
    test_flows = [{"name": "births", "to": "population"}]
    result = analyze_stock_flow(test_stocks, test_flows)
    print(json.dumps(result, ensure_ascii=False, indent=2))
