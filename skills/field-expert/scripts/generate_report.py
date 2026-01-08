#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成脚本 - 场域分析技能

功能：
- 读取所有中间分析结果
- 生成HTML格式的分析报告
- 生成综合JSON分析结果
- 生成执行摘要

输入：
- --input: combined_input.json 路径
- --boundary: boundary_results.json 路径
- --capital: capital_results.json 路径
- --habitus: habitus_results.json 路径
- --dynamics: dynamics_results.json 路径
- --output: 输出目录路径

输出：
- output/reports/field_analysis_report.html
- output/json/comprehensive_analysis.json
- output/executive_summary.txt
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


def read_json(file_path: Path) -> Any:
    """安全读取JSON文件"""
    if file_path is None or not file_path.exists():
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"警告: 读取 {file_path} 失败: {e}")
        return None


def load_input_data(input_path: Path) -> Dict[str, Any]:
    """加载输入数据"""
    data = read_json(input_path) or {}
    return {
        "grounded_theory_count": data.get("metadata", {}).get("grounded_theory_count", 0),
        "social_network_count": data.get("metadata", {}).get("social_network_count", 0),
        "esoc_framework_count": data.get("metadata", {}).get("esoc_framework_count", 0),
        "sources": data.get("metadata", {}).get("sources", [])
    }


def extract_fields_info(boundary_data: Optional[Dict]) -> Dict[str, Any]:
    """提取场域信息"""
    if not boundary_data:
        return {"fields": [], "gatekeepers": []}
    
    results = boundary_data.get("results", boundary_data)
    return {
        "fields": results.get("fields", []),
        "gatekeepers": results.get("gatekeepers", []),
        "boundary_dynamics": results.get("boundary_dynamics", {})
    }


def extract_capital_info(capital_data: Optional[Dict]) -> Dict[str, Any]:
    """提取资本分析信息"""
    if not capital_data:
        return {"capital_types": {}, "ranking": []}
    
    results = capital_data.get("results", capital_data)
    return {
        "capital_types": results.get("capital_types", {}),
        "distribution": results.get("distribution", {}),
        "ranking": results.get("ranking", [])
    }


def extract_habitus_info(habitus_data: Optional[Dict]) -> Dict[str, Any]:
    """提取习性分析信息"""
    if not habitus_data:
        return {"actors": [], "symbolic_violence": {}}
    
    results = habitus_data.get("results", habitus_data)
    return {
        "actors": results.get("actors", []),
        "symbolic_violence": results.get("symbolic_violence", {}),
        "cross_field": results.get("cross_field_analysis", {})
    }


def extract_dynamics_info(dynamics_data: Optional[Dict]) -> Dict[str, Any]:
    """提取动力学分析信息"""
    if not dynamics_data:
        return {"competition": {}, "evolution": {}}
    
    results = dynamics_data.get("results", dynamics_data)
    return {
        "competition": results.get("competition_analysis", {}),
        "power": results.get("power_relations", {}),
        "evolution": results.get("field_evolution", {}),
        "theory": results.get("theory_construction", {})
    }


def generate_html_report(
    input_info: Dict,
    fields_info: Dict,
    capital_info: Dict,
    habitus_info: Dict,
    dynamics_info: Dict
) -> str:
    """生成HTML分析报告"""
    
    fields = fields_info.get("fields", [])
    gatekeepers = fields_info.get("gatekeepers", [])
    capital_types = capital_info.get("capital_types", {})
    ranking = capital_info.get("ranking", [])
    actors = habitus_info.get("actors", [])
    theory = dynamics_info.get("theory", {})
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>布迪厄场域分析报告</title>
    <style>
        :root {{
            --primary: #2d3748;
            --accent: #c53030;
            --buddha: #805ad5;
            --bg: #f7fafc;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Noto Serif SC', serif; background: var(--bg); color: var(--primary); line-height: 1.9; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, var(--primary) 0%, #1a202c 100%); color: white; padding: 50px 20px; text-align: center; }}
        header h1 {{ font-size: 2.2em; margin-bottom: 10px; }}
        header .meta {{ font-size: 0.9em; opacity: 0.9; margin-top: 15px; }}
        .nav {{ background: white; padding: 15px; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .nav ul {{ display: flex; justify-content: center; gap: 25px; list-style: none; flex-wrap: wrap; }}
        .nav a {{ color: var(--primary); text-decoration: none; font-weight: 500; }}
        .nav a:hover {{ color: var(--accent); }}
        section {{ background: white; margin: 25px 0; padding: 35px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        h2 {{ color: var(--primary); border-bottom: 3px solid var(--accent); padding-bottom: 10px; margin-bottom: 25px; font-size: 1.6em; }}
        h3 {{ color: var(--buddha); margin: 25px 0 15px; font-size: 1.3em; }}
        h4 {{ margin: 15px 0 10px; color: var(--accent); }}
        p {{ margin-bottom: 15px; text-align: justify; }}
        ul {{ padding-left: 25px; margin: 15px 0; }}
        li {{ margin: 10px 0; }}
        .field-card {{ background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%); padding: 20px; border-radius: 8px; margin: 15px 0; border-left: 4px solid var(--accent); }}
        .field-card.buddha {{ border-left-color: var(--buddha); }}
        .finding {{ background: linear-gradient(135deg, #fff5f5 0%, #fffaf0 100%); padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .proposition {{ background: #f7fafc; padding: 18px; border-radius: 8px; margin: 15px 0; border-left: 4px solid var(--buddha); }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 14px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background: var(--primary); color: white; }}
        footer {{ text-align: center; padding: 40px; color: #718096; font-size: 0.9em; }}
    </style>
</head>
<body>
    <header>
        <h1>布迪厄场域分析报告</h1>
        <div class="meta">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </header>

    <nav class="nav">
        <ul>
            <li><a href="#overview">分析概览</a></li>
            <li><a href="#fields">场域边界</a></li>
            <li><a href="#capital">资本分布</a></li>
            <li><a href="#habitus">习性分析</a></li>
            <li><a href="#dynamics">场域动力学</a></li>
            <li><a href="#theory">理论建构</a></li>
        </ul>
    </nav>

    <div class="container">
        <section id="overview">
            <h2>📊 分析概览</h2>
            <p>本报告基于扎根理论方法论，运用布迪厄场域理论对文本数据进行深度分析。</p>
            <table>
                <tr><th>数据类型</th><th>文件数量</th></tr>
                <tr><td>扎根理论数据</td><td>{input_info.get('grounded_theory_count', 0)}</td></tr>
                <tr><td>社会网络数据</td><td>{input_info.get('social_network_count', 0)}</td></tr>
                <tr><td>ESOC框架数据</td><td>{input_info.get('esoc_framework_count', 0)}</td></tr>
            </table>
        </section>

        <section id="fields">
            <h2>🏛️ 场域边界分析</h2>
            <p>识别并界定了以下 {len(fields)} 个核心场域：</p>
'''
    
    for i, field in enumerate(fields[:5]):
        html += f'''
            <div class="field-card">
                <h4>{field.get('name', '未命名场域')}</h4>
                <p><strong>核心行动者:</strong> {', '.join(field.get('core_actors', []))}</p>
                <p><strong>边界标识:</strong> {', '.join(field.get('boundary_markers', []))}</p>
            </div>
'''
    
    if gatekeepers:
        html += '''
            <h3>守门人分析</h3>
            <p>以下是场域边界的守门人角色：</p>
'''
        for gk in gatekeepers[:3]:
            html += f'''
            <div class="field-card">
                <h4>{gk.get('actor', '未命名')}</h4>
                <p><strong>守门场域:</strong> {', '.join(gk.get('fields', []))}</p>
                <p><strong>角色:</strong> {gk.get('role', '')}</p>
            </div>
'''
    
    html += '''
        </section>

        <section id="capital">
            <h2>💎 资本分布分析</h2>
'''
    
    for capital_type, info in capital_types.items():
        html += f'''
            <h3>{capital_type.get('description', capital_type)}</h3>
            <p>{', '.join(info.get('manifestations', []))}</p>
'''
    
    if ranking:
        html += '''
            <h3>资本排名</h3>
            <table>
                <tr><th>排名</th><th>行动者</th><th>主导资本</th></tr>
'''
        for i, item in enumerate(ranking[:5], 1):
            html += f'''
                <tr><td>{i}</td><td>{item.get('actor', '')}</td><td>{item.get('dominant_type', '')}</td></tr>
'''
        html += '''
            </table>
'''
    
    html += '''
        </section>

        <section id="habitus">
            <h2>🧠 习性模式分析</h2>
'''
    
    for actor in actors[:3]:
        html += f'''
            <div class="field-card">
                <h4>{actor.get('actor', '未命名行动者')}</h4>
                <p><strong>行为模式:</strong> {', '.join(actor.get('behavior_patterns', {}).get('daily_behavior', []))}</p>
                <p><strong>认知结构:</strong> {actor.get('cognitive_structure', {}).get('thinking_mode', '')}</p>
            </div>
'''
    
    sv = habitus_info.get('symbolic_violence', {})
    if sv:
        html += '''
            <h3>符号暴力分析</h3>
'''
        for violence in sv.get('dominant_violence', [])[:2]:
            html += f'''
            <div class="proposition">
                <strong>{violence.get('form', '')}</strong>: {violence.get('mechanism', '')}
            </div>
'''
    
    html += '''
        </section>

        <section id="dynamics">
            <h2>⚡ 场域动力学分析</h2>
'''
    
    evolution = dynamics_info.get('evolution', {})
    if evolution:
        html += f'''
            <h3>场域演变</h3>
            <p>发展阶段数: {len(evolution.get('development_stages', []))}</p>
            <p>演变动力: {', '.join(evolution.get('driving_forces', []))}</p>
'''
    
    competition = dynamics_info.get('competition', {})
    if competition:
        html += f'''
            <h3>竞争格局</h3>
            <p>竞争趋势: {competition.get('competition_trends', '')}</p>
'''
    
    html += '''
        </section>

        <section id="theory">
            <h2>📝 理论建构</h2>
'''
    
    findings = theory.get('core_findings', [])
    for finding in findings[:3]:
        html += f'''
            <div class="proposition">
                <strong>核心发现:</strong> {finding}
            </div>
'''
    
    propositions = theory.get('theoretical_propositions', [])
    for prop in propositions[:2]:
        html += f'''
            <div class="proposition">
                <strong>理论命题:</strong> {prop.get('proposition', '')}
            </div>
'''
    
    html += '''
        </section>
    </div>

    <footer>
        <p>布迪厄场域分析报告 | 基于扎根理论方法论</p>
    </footer>
</body>
</html>
'''
    
    return html


def generate_comprehensive_json(
    input_info: Dict,
    fields_info: Dict,
    capital_info: Dict,
    habitus_info: Dict,
    dynamics_info: Dict
) -> Dict[str, Any]:
    """生成综合JSON结果"""
    
    return {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "analysis_type": "field_analysis",
            "theoretical_framework": "Bourdieu Field Theory",
            "methodology": "Grounded Theory"
        },
        "input_summary": input_info,
        "field_analysis": {
            "fields": fields_info.get("fields", []),
            "gatekeepers": fields_info.get("gatekeepers", []),
            "boundary_dynamics": fields_info.get("boundary_dynamics", {})
        },
        "capital_analysis": {
            "capital_types": capital_info.get("capital_types", {}),
            "distribution": capital_info.get("distribution", {}),
            "ranking": capital_info.get("ranking", [])
        },
        "habitus_analysis": {
            "actors": habitus_info.get("actors", []),
            "symbolic_violence": habitus_info.get("symbolic_violence", {}),
            "cross_field": habitus_info.get("cross_field", {})
        },
        "dynamics_analysis": {
            "competition": dynamics_info.get("competition", {}),
            "power": dynamics_info.get("power", {}),
            "evolution": dynamics_info.get("evolution", {}),
            "theory": dynamics_info.get("theory", {})
        }
    }


def generate_executive_summary(
    input_info: Dict,
    fields_info: Dict,
    capital_info: Dict,
    habitus_info: Dict,
    dynamics_info: Dict
) -> str:
    """生成执行摘要"""
    
    fields_count = len(fields_info.get("fields", []))
    capital_types = len(capital_info.get("capital_types", {}))
    actors_count = len(habitus_info.get("actors", []))
    findings = dynamics_info.get("theory", {}).get("core_findings", [])
    
    summary = f'''布迪厄场域分析执行摘要
========================

分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

一、数据概况
------------
- 扎根理论数据: {input_info.get('grounded_theory_count', 0)} 个文件
- 社会网络数据: {input_info.get('social_network_count', 0)} 个文件
- ESOC框架数据: {input_info.get('esoc_framework_count', 0)} 个文件

二、核心发现
------------
1. 场域识别: 共识别 {fields_count} 个核心场域
2. 资本类型: 涵盖 {capital_types} 种资本类型
3. 习性分析: 分析了 {actors_count} 个行动者的习性模式
4. 理论建构: 提出了 {len(findings)} 个核心发现

三、主要结论
------------
'''
    
    for i, finding in enumerate(findings[:3], 1):
        summary += f"{i}. {finding}\n"
    
    summary += '''
四、分析方法
------------
- 理论框架: 布迪厄场域理论
- 分析方法: 扎根理论
- 分析维度: 场域边界、资本分布、习性模式、场域动力学

五、后续建议
------------
1. 深化场域间关系分析
2. 追踪场域演变的历史脉络
3. 验证理论命题的实证性

========================
报告生成完成
'''
    
    return summary


def main():
    """主函数"""
    # 解析命令行参数
    args = {
        "--input": None,
        "--boundary": None,
        "--capital": None,
        "--habitus": None,
        "--dynamics": None,
        "--output": None
    }
    
    for i, arg in enumerate(sys.argv):
        if arg in args and i + 1 < len(sys.argv):
            args[arg] = Path(sys.argv[i + 1])
    
    # 验证必要参数
    if not args["--output"]:
        print("错误: 必须指定 --output 参数")
        return 1
    
    output_dir = args["--output"]
    output_dir = Path(output_dir)
    
    # 创建输出目录
    reports_dir = output_dir / "reports"
    json_dir = output_dir / "json"
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("  场域分析技能 - 报告生成脚本")
    print("=" * 60)
    
    # 加载数据
    print("\n📂 加载分析结果...")
    input_info = load_input_data(args["--input"])
    fields_info = extract_fields_info(read_json(args["--boundary"]))
    capital_info = extract_capital_info(read_json(args["--capital"]))
    habitus_info = extract_habitus_info(read_json(args["--habitus"]))
    dynamics_info = extract_dynamics_info(read_json(args["--dynamics"]))
    
    print(f"   场域数量: {len(fields_info.get('fields', []))}")
    print(f"   资本类型: {len(capital_info.get('capital_types', {}))}")
    print(f"   习性分析: {len(habitus_info.get('actors', []))} 个行动者")
    
    # 生成HTML报告
    print("\n📝 生成HTML报告...")
    html_content = generate_html_report(
        input_info, fields_info, capital_info, habitus_info, dynamics_info
    )
    html_file = reports_dir / "field_analysis_report.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"   ✓ {html_file}")
    
    # 生成综合JSON
    print("\n📊 生成综合JSON...")
    comprehensive = generate_comprehensive_json(
        input_info, fields_info, capital_info, habitus_info, dynamics_info
    )
    json_file = json_dir / "comprehensive_analysis.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(comprehensive, f, ensure_ascii=False, indent=2)
    print(f"   ✓ {json_file}")
    
    # 生成执行摘要
    print("\n📋 生成执行摘要...")
    summary = generate_executive_summary(
        input_info, fields_info, capital_info, habitus_info, dynamics_info
    )
    summary_file = output_dir / "executive_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"   ✓ {summary_file}")
    
    print("\n" + "=" * 60)
    print("  ✅ 报告生成完成!")
    print("=" * 60)
    print(f"\n📁 输出目录: {output_dir}")
    print(f"   - HTML报告: {html_file}")
    print(f"   - 综合JSON: {json_file}")
    print(f"   - 执行摘要: {summary_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
