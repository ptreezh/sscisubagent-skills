#!/usr/bin/env python3
"""
分析用户提供的交通规则观察记录
"""

from social_facts_identifier import SocialFactsIdentifier
import json

# 用户观察记录
observation = """在现代城市中，交通规则具有明显的强制性。所有驾驶员必须遵守红绿灯，违反会面临罚款。即使个人不认同，也必须执行。这种现象普遍存在于所有现代城市。"""

# 使用社会事实识别工具
identifier = SocialFactsIdentifier()
result = identifier.identify_social_facts(observation, "traffic_rules_analysis")

# 生成报告
report = identifier.generate_report(result)

# 输出结果
print("=" * 80)
print("涂尔干社会事实分析报告")
print("=" * 80)
print()
print(report)

# 保存结果
with open("D:\\socienceAI\\agentskills\\digital-durkheim-expert\\tools\\digital-durkheim-workspace\\iteration-1\\eval-1-with_skill\\outputs\\analysis_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print()
print("=" * 80)
print("详细分析结论")
print("=" * 80)
print()

# 详细分析（硬编码阈值判断已禁用）
# ⚠️ 0.3阈值判断已禁用：社会事实判断由LLM基于涂尔干理论完成
print("## 社会事实三维特征分析")
print()
print("⚠️ 注意：以下判断应由LLM基于涂尔干《社会学方法的准则》完成")
print("    0.3阈值仅为定量信号，不是判断社会事实的绝对标准")
print()

# 1. 外在性分析
print("### 1. 外在性 (Externality)")
externality = result["dimensions"]["externality"]
print(f"  得分: {externality['score']}")
print("  → LLM判断: 外在性是否满足涂尔干社会事实标准")
print()

# 2. 强制性分析
print("### 2. 强制性 (Coerciveness)")
coerciveness = result["dimensions"]["coerciveness"]
print(f"  得分: {coerciveness['score']}")
print("  → LLM判断: 强制性是否满足涂尔干社会事实标准")
print()

# 3. 普遍性分析
print("### 3. 普遍性 (Generality)")
generality = result["dimensions"]["generality"]
print(f"  得分: {generality['score']}")
print("  → LLM判断: 普遍性是否满足涂尔干社会事实标准")
print()

# 总体结论
print("=" * 80)
print("最终结论")
print("=" * 80)
print()
print("⚠️ 社会事实判断和分类应由LLM基于涂尔干理论完成")
print("    禁止：仅因 score >= 0.3 就自动判定为社会事实")
print("    正确做法：LLM综合三维特征 + 理论原则做诠释判断")
