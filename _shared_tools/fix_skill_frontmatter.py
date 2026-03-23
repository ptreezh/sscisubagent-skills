#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复SKILL.md文件格式以符合agentskills.io规范
- 合并多个YAML frontmatter块为单个块
- 改进description字段
- 添加license、compatibility字段
"""

import re
from pathlib import Path

# 技能目录
SKILLS_DIR = Path(__file__).parent.parent

# 技能描述映射
SKILL_DESCRIPTIONS = {
    'grounded-theory-expert': '扎根理论分析专家。提供开放编码、主轴编码、选择性编码的系统化流程，支持理论饱和度检验和CRCT思维链。适用于质性研究、理论建构、数据深度分析场景。',
    'social-network-analysis-expert': '社会网络分析专家。提供中心性计算、社群检测、结构洞分析、网络可视化功能。适用于组织网络研究、社交网络分析、关系数据挖掘场景。',
    'actor-network-analysis-expert': '行动者网络理论专家。提供行动者识别、转译过程分析、对称性检验、争议映射功能。适用于ANT研究、科技社会学、创新扩散分析场景。',
    'bourdieu-field-analysis-expert': '布迪厄场域分析专家。提供场域边界识别、资本分析、习性分析、场域动力学追踪功能。适用于文化研究、教育社会学、权力结构分析场景。',
    'digital-durkheim-expert': '数字涂尔干专家。提供社会事实识别、团结分析、失范评估、自杀类型分析功能。适用于数字社会研究、社会整合分析、现代性问题研究场景。',
    'digital-marx-expert': '数字马克思主义专家。提供阶级分析、剩余价值计算、异化评估、危机趋势预测功能。适用于数字劳动研究、平台经济分析、批判理论研究场景。',
    'digital-weber-expert': '数字韦伯专家。提供理性化分析、科层制分析、社会行动分类、权威类型分析功能。适用于组织社会学、制度分析、现代性研究场景。',
    'cas-simulation-expert': '复杂适应系统仿真专家。提供ABM建模、涌现检测、参数敏感性分析、模式识别功能。适用于复杂系统研究、社会仿真、政策模拟场景。',
    'system-dynamics-expert': '系统动力学专家。提供因果回路图构建、库存流量建模、反馈循环分析、政策仿真功能。适用于系统分析、政策评估、动态建模场景。',
    'did-analysis-expert': '双重差分分析专家。提供平行趋势检验、处理效应计算、稳健性检验、异质性分析功能。适用于政策评估、因果推断、准实验设计场景。',
    'qca-analysis-expert': '定性比较分析专家。提供数据校准、真值表构建、一致性分析、必要性/充分性检验功能。适用于比较研究、因果组合分析、中小样本研究场景。',
    'business-ecosystem-expert': '商业生态系统专家。提供生态系统映射、共生价值分析、演化动力识别、健康度评估功能。适用于平台生态研究、商业网络分析、生态战略规划场景。',
    'business-model-expert': '商业模式专家。提供商业模式画布、价值主张分析、收入模式设计、竞争分析功能。适用于商业模式创新、战略规划、创业设计场景。',
    'survey-design-expert': '问卷设计专家。提供问卷结构设计、信度效度检验、抽样计算、预测试管理功能。适用于调查研究、量表开发、数据收集设计场景。',
    'data-analysis-expert': '数据分析专家。提供描述性统计、回归分析、假设检验、数据可视化功能。适用于定量研究、统计建模、实证分析场景。',
    'skill-upgrade-expert': '技能升级专家。提供技能诊断、优化建议、子Agent集成、性能评估功能。适用于AI技能开发、技能标准化、质量提升场景。',
}

# 需要修复的技能列表
SKILLS_TO_FIX = list(SKILL_DESCRIPTIONS.keys())

def extract_body_content(content: str) -> str:
    """提取SKILL.md的正文内容（去除所有frontmatter）"""
    # 移除所有YAML frontmatter块
    # 匹配 --- ... --- 格式
    pattern = r'^---\s*\n.*?\n---\s*\n'
    # 使用DOTALL让.匹配换行符
    cleaned = re.sub(pattern, '', content, flags=re.DOTALL)
    return cleaned.strip()

def create_compliant_frontmatter(skill_name: str) -> str:
    """创建符合agentskills.io规范的frontmatter"""
    description = SKILL_DESCRIPTIONS.get(skill_name, f'{skill_name} skill for AI CLI')
    
    # 支持的AI平台列表
    platforms = "Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw"
    
    frontmatter = f'''---
name: {skill_name}
description: |
  {description}
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: {platforms}
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
---'''
    return frontmatter

def fix_skill_md(skill_path: Path) -> dict:
    """修复单个技能的SKILL.md"""
    skill_md_path = skill_path / 'SKILL.md'
    
    if not skill_md_path.exists():
        return {'status': 'error', 'message': 'SKILL.md not found'}
    
    try:
        content = skill_md_path.read_text(encoding='utf-8')
        
        # 提取正文
        body = extract_body_content(content)
        
        # 创建新的frontmatter
        frontmatter = create_compliant_frontmatter(skill_path.name)
        
        # 组合新内容
        new_content = f'{frontmatter}\n\n{body}'
        
        # 写回文件
        skill_md_path.write_text(new_content, encoding='utf-8')
        
        return {'status': 'success', 'message': 'Fixed'}
    
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def main():
    print('=' * 60)
    print('SKILL.md 格式修复工具 - agentskills.io 规范')
    print('=' * 60)
    
    results = {'success': 0, 'error': 0, 'skipped': 0}
    
    for skill_name in SKILLS_TO_FIX:
        skill_path = SKILLS_DIR / skill_name
        
        if not skill_path.exists():
            print(f'⏭️ {skill_name}: 目录不存在，跳过')
            results['skipped'] += 1
            continue
        
        result = fix_skill_md(skill_path)
        
        if result['status'] == 'success':
            print(f'✅ {skill_name}: 修复成功')
            results['success'] += 1
        else:
            print(f'❌ {skill_name}: {result["message"]}')
            results['error'] += 1
    
    print('=' * 60)
    print(f'完成: 成功 {results["success"]}, 失败 {results["error"]}, 跳过 {results["skipped"]}')
    
    return results

if __name__ == '__main__':
    main()
