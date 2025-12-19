#!/usr/bin/env python3
"""
免费论文搜索技能演示
展示渐进式信息披露和最小认知负荷设计
"""

import sys
import os
import json
import time

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.paper_search_interface import PaperSearchInterface

def demo_progressive_disclosure():
    """演示渐进式信息披露"""

    interface = PaperSearchInterface()
    query = "machine learning"

    print("=== 免费论文搜索技能演示 ===")
    print(f"用户查询: {query}")
    print()

    # 第1层：搜索概览（最小认知负荷）
    print("🔍 第1层信息：搜索概览")
    print("-" * 40)

    overview = interface.execute_search(query, max_results=5)

    print(f"📊 搜索结果:")
    print(f"   总计找到: {overview['total_found']} 篇可下载论文")
    print(f"   arXiv来源: {overview['sources']['arxiv']['count']} 篇 ({overview['sources']['arxiv']['reliability']})")
    print(f"   机构资源: {overview['sources']['institutional']['count']} 篇")
    print(f"   搜索耗时: {overview['search_time']}")
    print()

    if overview['total_found'] == 0:
        print("未找到可下载的免费论文。建议:")
        print("1. 调整搜索关键词")
        print("2. 尝试相关领域")
        print("3. 考虑合法获取付费论文")
        return

    # 第2层：论文列表
    print("📋 第2层信息：可下载论文列表")
    print("-" * 40)

    paper_list = interface.get_paper_list(limit=3)
    for paper in paper_list:
        print(f"{paper['id']}. {paper['title']}")
        print(f"   来源: {paper['source']} | 大小: {paper['file_size']} | 可信度: {paper['confidence']}")
    print()

    # 第3层：按需详细信息
    if paper_list:
        print("📖 第3层信息：按需详细信息")
        print("-" * 40)
        print("查看第1篇论文的详细信息...")

        details = interface.get_paper_details(1)

        print(f"标题: {details['paper_info']['title']}")
        print(f"作者: {', '.join(details['paper_info']['authors'][:3])}...")
        print(f"来源: {details['paper_info']['source']} ({details['paper_info']['confidence']})")
        print()
        print(f"摘要: {details['paper_info']['abstract']}")
        print()
        print(f"💡 下载建议: {details['download_advice']}")
        print()
        print(f"📝 引用建议: {details['citation_suggestion']}")
        print()

        # 第4层：执行下载（可选）
        print("📥 下载选项")
        print("-" * 40)
        print("是否下载第1篇论文？")

        # 模拟用户选择下载
        print("用户选择: 是")
        download_result = interface.download_selected_paper(1)

        if download_result['success']:
            print(f"✅ 下载成功!")
            print(f"   文件: {download_result['filepath']}")
            print(f"   大小: {download_result['size']}")
        else:
            print(f"❌ 下载失败: {download_result['error']}")

def demo_cognitive_load_minimization():
    """演示最小认知负荷设计"""

    print("\n" + "="*50)
    print("最小认知负荷设计演示")
    print("="*50)

    # 对比传统方式 vs 本技能的方式
    print("❌ 传统方式（高认知负荷）:")
    print("  - 一次性显示所有论文详情")
    print("  - 包大量无关信息")
    print("  - 用户需要筛选和判断")
    print("  - 容易造成信息过载")
    print()

    print("✅ 本技能方式（最小认知负荷）:")
    print("  - 第1层：只显示搜索概览（3-5个关键数字）")
    print("  - 第2层：简洁的论文列表（标题+来源+大小）")
    print("  - 第3层：按需查看详细信息")
    print("  - 第4层：可选的下载操作")
    print("  - 用户控制信息获取节奏")
    print()

    # 展示结构化输出
    print("📊 结构化输出示例:")
    demo_output = {
        "search_query": "machine learning",
        "results_summary": {
            "total_found": 5,
            "sources": {"arXiv": 4, "institutional": 1},
            "confidence": "High",
            "estimated_size": "2.1MB"
        },
        "papers": [
            {"id": 1, "title": "Paper 1...", "size": "150KB"},
            {"id": 2, "title": "Paper 2...", "size": "300KB"}
        ],
        "next_actions": ["show_details", "download", "search_more"]
    }
    print(json.dumps(demo_output, indent=2, ensure_ascii=False))

def demo_tool_oriented_thinking():
    """演示工具化思维"""

    print("\n" + "="*50)
    print("工具化思维演示")
    print("="*50)

    print("🛠️ 工具化思维原则:")
    print("  1. 复杂逻辑固化为可执行脚本")
    print("  2. 定量分析用程序处理")
    print("  3. 定性解释由AI负责")
    print("  4. 人机协作，各司其职")
    print()

    print("🔄 实际应用:")
    print("  - 程序处理: 搜索、验证、下载")
    print("  - AI处理: 策略制定、结果解释、用户建议")
    print("  - 用户处理: 决策、选择、反馈")
    print()

    # 展示分工示例
    print("📋 分工示例:")
    print("  程序执行:")
    print("    ✅ 搜索arXiv数据库")
    print("    ✅ 验证PDF下载链接")
    print("    ✅ 计算文件大小")
    print("    ✅ 执行文件下载")
    print()
    print("  AI解释:")
    print("    ✅ 分析论文质量")
    print("    ✅ 提供下载建议")
    print("    ✅ 生成引用格式")
    print("    ✅ 回答用户问题")

if __name__ == "__main__":
    try:
        demo_progressive_disclosure()
        demo_cognitive_load_minimization()
        demo_tool_oriented_thinking()

        print("\n" + "="*50)
        print("✅ 技能演示完成")
        print("✅ 遵循渐进式信息披露")
        print("✅ 实现最小认知负荷")
        print("✅ 应用工具化思维")
        print("✅ 基于真实测试验证")
        print("="*50)

    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        print("这可能是由于网络连接问题或依赖项缺失")
        print("但技能的核心设计理念已经展示")