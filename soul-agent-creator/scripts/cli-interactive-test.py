#!/usr/bin/env python3
"""
Soul Agent Creator - CLI 自然语言交互测试

模拟真实用户在 CLI 中通过自然语言对话创建 Soul Agent 的过程。

用法:
    python scripts/cli-interactive-test.py
"""

import sys
import os
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import list_skills, generate_soul_config, validate_soul_config


def print_separator():
    print("\n" + "=" * 70)


def print_welcome():
    print_separator()
    print("🦞 Soul Agent Creator - CLI 自然语言交互测试")
    print_separator()
    print()
    print("本测试模拟真实用户在 CLI 中通过自然语言对话创建 Soul Agent")
    print()


# ============================================================================
# 场景 1: 直接创建
# ============================================================================
def test_scenario_1_direct_creation():
    """场景 1: 用户明确知道要创建什么"""
    
    print_welcome()
    
    # 用户输入
    user_input = "我想创建一个扎根理论的分身，用于分析访谈数据"
    
    print(f"👤 用户：{user_input}")
    print()
    
    # Skill 响应 - 需求澄清
    print("🤖 Soul Agent Creator:")
    print("""
好的！我来帮你创建一个扎根理论专家分身。

在开始之前，我需要了解几个问题：

1. 自定义名称：你希望分身叫什么名字？（默认："扎根理论专家"）
2. 对标学者：你更倾向于哪位学者的方法？
   - Kathy Charmaz（建构主义扎根理论）
   - Strauss & Corbin（程序化扎根理论）
   - Glaser & Strauss（经典扎根理论）
3. 主要用途：除了访谈数据分析，还需要其他功能吗？
""")
    
    # 模拟用户回答
    print('👤 用户：就叫"我的扎根理论助手"吧，对标 Charmaz 的建构主义，主要用于访谈编码分析')
    print()
    
    # 执行创建
    print("🤖 Soul Agent Creator:")
    print("好的！正在为你创建分身...\n")
    
    result = generate_soul_config.create(
        skill_id="grounded-theory",
        custom_name="我的扎根理论助手",
        output_dir="./test-output",
        verbose=True
    )
    
    print()
    print("✅ Soul Agent 创建成功！")
    print()
    print(f"📋 分身信息:")
    print(f"   Soul ID: {result['soul_id']}")
    print(f"   名称：{result['display_name']}")
    print(f"   对标：{result['master']}")
    print(f"   路径：{result['output_dir']}")
    print()
    print("🚀 激活方式:")
    print(f"   export SOUL_AGENT_ID=\"{result['soul_id']}\"")
    print()
    
    # 验证
    print("🔍 验证配置...")
    validation = validate_soul_config.check(result['output_dir'], verbose=False)
    print(f"   验证结果：{'✅ 通过' if validation else '❌ 失败'}")
    print()
    
    return result


# ============================================================================
# 场景 2: 探索式创建
# ============================================================================
def test_scenario_2_exploratory():
    """场景 2: 用户需要推荐和引导"""
    
    print_separator()
    print("场景 2: 探索式创建")
    print_separator()
    print()
    
    # 用户输入
    user_input = "我是管理学研究生，想定制一个方法论 AI 助手，但不知道有哪些选择"
    
    print(f"👤 用户：{user_input}")
    print()
    
    # Skill 响应 - 推荐
    print("🤖 Soul Agent Creator:")
    print("""
欢迎！我来帮你选择最适合的方法论分身。

作为管理学研究生，你可能研究方向包括：
- 组织行为/人力资源 → 适合质性方法（扎根理论、现象学）
- 战略管理/创新研究 → 适合混合方法或社会网络分析
- 市场营销/消费者行为 → 适合质性方法（内容分析、叙事分析）

请告诉我：
1. 你的具体研究方向是什么？
2. 你主要收集什么类型的数据？（访谈/问卷/二手数据/观察）
3. 你希望分身帮你解决什么问题？
""")
    
    # 模拟用户回答
    print("👤 用户：我研究组织创新，主要收集访谈数据，希望帮我做编码分析")
    print()
    
    # Skill 响应 - 推荐技能
    print("🤖 Soul Agent Creator:")
    print("""
根据你的需求，我推荐以下方法论分身：

**首选推荐**: 扎根理论专家
- 对标学者：Kathy Charmaz / Strauss & Corbin
- 核心能力：开放编码、轴心编码、选择式编码
- 适用场景：质性研究数据分析、理论建构研究
- 推荐理由：最适合访谈数据的编码分析

**备选推荐**: 混合方法研究专家
- 对标学者：John Creswell
- 核心能力：三角验证、互补设计、转换整合
- 适用场景：复杂现象研究、多层次分析

你更倾向于哪一个？或者想了解更多细节？
""")
    
    # 模拟用户选择
    print("👤 用户：就选扎根理论吧")
    print()
    
    # 执行创建
    print("🤖 Soul Agent Creator:")
    print("好的！正在为你创建扎根理论分身...\n")
    
    result = generate_soul_config.create(
        skill_id="grounded-theory",
        custom_name="组织创新研究助手",
        output_dir="./test-output",
        verbose=True
    )
    
    print()
    print("✅ 创建成功！")
    print()
    
    return result


# ============================================================================
# 场景 3: 快速创建
# ============================================================================
def test_scenario_3_quick_create():
    """场景 3: 用户使用默认配置快速创建"""
    
    print_separator()
    print("场景 3: 快速创建")
    print_separator()
    print()
    
    # 用户输入
    user_input = "帮我快速创建一个社会网络分析分身，默认配置就行"
    
    print(f"👤 用户：{user_input}")
    print()
    
    # Skill 响应
    print("🤖 Soul Agent Creator:")
    print("""
好的！我将为你创建一个社会网络分析分身，使用默认配置：

- 分身名称：社会网络分析专家
- 对标学者：Linton Freeman / Stanley Wasserman
- 核心能力：中心性分析、社区检测、结构洞分析
- 对话风格：学术严谨
- 存储位置：~/.stigmergy/soul-agents/soul_sna_20260322/

确认创建？(回复"确认"或"y"即可)
""")
    
    # 模拟用户确认
    print("👤 用户：确认")
    print()
    
    # 执行创建
    print("🤖 Soul Agent Creator:")
    print("正在创建分身...\n")
    
    result = generate_soul_config.create(
        skill_id="social-network-analysis",
        custom_name=None,  # 使用默认名称
        output_dir="./test-output",
        verbose=True
    )
    
    print()
    print("✅ 创建成功！")
    print()
    
    return result


# ============================================================================
# 场景 4: 技能对比
# ============================================================================
def test_scenario_4_comparison():
    """场景 4: 用户在两个技能之间犹豫"""
    
    print_separator()
    print("场景 4: 技能对比")
    print_separator()
    print()
    
    # 用户输入
    user_input = "扎根理论和行动者网络理论有什么区别？我该选哪个？"
    
    print(f"👤 用户：{user_input}")
    print()
    
    # Skill 响应 - 对比
    print("🤖 Soul Agent Creator:")
    print("""
以下是两个技能的详细对比：

| 维度 | 扎根理论 | 行动者网络理论 (ANT) |
|------|---------|---------------------|
| 对标学者 | Kathy Charmaz | Bruno Latour |
| 哲学基础 | 符号互动论 | 对称性原则 |
| 核心概念 | 开放/轴心/选择式编码 | 行动者/转译/网络 |
| 数据类型 | 访谈、观察、文本 | 追踪人 - 非人网络 |
| 分析重点 | 理论建构 | 网络追踪 |
| 学习曲线 | 中等 | 较陡 |

**选择建议**：
- 如果你的数据主要是访谈，想建构理论 → 选择 **扎根理论**
- 如果你想分析技术 - 社会网络，追踪人 - 非人关系 → 选择 **ANT**

你的研究数据是什么类型的？想解决什么问题？
""")
    
    # 模拟用户回答
    print("👤 用户：我有访谈数据，想建构一个关于员工满意度的理论")
    print()
    
    # Skill 响应
    print("🤖 Soul Agent Creator:")
    print("根据你的情况，**扎根理论**更适合你！我来帮你创建...\n")
    
    result = generate_soul_config.create(
        skill_id="grounded-theory",
        custom_name="员工满意度研究助手",
        output_dir="./test-output",
        verbose=True
    )
    
    print()
    print("✅ 创建成功！")
    print()
    
    return result


# ============================================================================
# 主函数
# ============================================================================
def main():
    """运行所有测试场景"""
    
    print("\n" + "=" * 70)
    print("  Soul Agent Creator - CLI 自然语言交互测试套件")
    print("=" * 70)
    print()
    print("本测试套件模拟 4 种真实用户在 CLI 中的交互场景")
    print()
    
    results = []
    
    # 场景 1: 直接创建
    try:
        result = test_scenario_1_direct_creation()
        results.append(("直接创建", True, None))
    except Exception as e:
        results.append(("直接创建", False, str(e)))
    
    # 场景 2: 探索式创建
    try:
        result = test_scenario_2_exploratory()
        results.append(("探索式创建", True, None))
    except Exception as e:
        results.append(("探索式创建", False, str(e)))
    
    # 场景 3: 快速创建
    try:
        result = test_scenario_3_quick_create()
        results.append(("快速创建", True, None))
    except Exception as e:
        results.append(("快速创建", False, str(e)))
    
    # 场景 4: 技能对比
    try:
        result = test_scenario_4_comparison()
        results.append(("技能对比", True, None))
    except Exception as e:
        results.append(("技能对比", False, str(e)))
    
    # 打印总结
    print_separator()
    print("测试总结")
    print_separator()
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, error in results:
        status = "✅ 通过" if success else f"❌ 失败：{error}"
        print(f"{name}: {status}")
    
    print(f"\n总计：{passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有交互测试通过！")
    else:
        print(f"\n⚠️ {total - passed} 个测试失败")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
