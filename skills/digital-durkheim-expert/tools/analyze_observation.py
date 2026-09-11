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

# 详细分析
print("## 社会事实三维特征分析")
print()

# 1. 外在性分析
print("### 1. 外在性 (Externality)")
externality = result["dimensions"]["externality"]
if externality["score"] >= 0.3:
    print(f"✓ 符合 (得分: {externality['score']:.2%})")
    print("  分析: 交通规则独立于个体存在，不以个人意志为转移。")
    print("  证据: '即使个人不认同，也必须执行'表明规则外在于个体。")
else:
    print(f"✗ 不符合 (得分: {externality['score']:.2%})")
print()

# 2. 强制性分析
print("### 2. 强制性 (Coerciveness)")
coerciveness = result["dimensions"]["coerciveness"]
if coerciveness["score"] >= 0.3:
    print(f"✓ 符合 (得分: {coerciveness['score']:.2%})")
    print("  分析: 交通规则对个体施加约束力，违反将面临制裁。")
    print("  证据: '具有明显的强制性'、'必须遵守'、'面临罚款'")
else:
    print(f"✗ 不符合 (得分: {coerciveness['score']:.2%})")
print()

# 3. 普遍性分析
print("### 3. 普遍性 (Generality)")
generality = result["dimensions"]["generality"]
if generality["score"] >= 0.3:
    print(f"✓ 符合 (得分: {generality['score']:.2%})")
    print("  分析: 交通规则在所有现代城市中广泛存在。")
    print("  证据: '所有驾驶员'、'普遍存在于所有现代城市'")
else:
    print(f"✗ 不符合 (得分: {generality['score']:.2%})")
print()

# 总体结论
print("=" * 80)
print("最终结论")
print("=" * 80)
print()

verdict = result["verdict"]
is_social_fact = result["classification"]["is_social_fact"]

if is_social_fact:
    fact_type = result["classification"]["fact_type"]
    print(f"## 判断结果: 是社会事实 ({verdict})")
    print()
    print(f"**分类**: {fact_type}")
    print()
    print("**理由**:")
    print("1. **外在性**: 交通规则独立于驾驶员个体存在，不以个人意志为转移")
    print("2. **强制性**: 违反规则将面临罚款等制裁，对个体产生约束力")
    print("3. **普遍性**: 规则适用于所有驾驶员，在所有现代城市普遍存在")
    print()
    print("根据涂尔干在《社会学方法的准则》中的定义，社会事实是'")
    print("'外在于个体，且具有强制性和普遍性的行为方式、思维方式'")
    print("和存在方式。交通规则完全符合这三个特征。")
    print()
    print("因此，**现代城市中的交通规则是典型的社会事实**，")
    print(f"属于{fact_type}。")
else:
    print(f"## 判断结果: 不是社会事实")
    print()
    print("**理由**: 该现象未完全满足社会事实的三维特征")
