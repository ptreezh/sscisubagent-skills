"""
备忘录撰写模块
此模块提供扎根理论备忘录撰写功能
"""

from typing import Dict, List, Any
import json
from datetime import datetime


def memo_writing(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行扎根理论的备忘录撰写
    
    Args:
        data: 包含研究过程数据的字典
    
    Returns:
        包含备忘录撰写结果的字典
    """
    # 从数据中提取研究过程信息
    coding_stage = data.get('coding_stage', 'open')
    process_info = data.get('process_info', {})
    analysis_results = data.get('analysis_results', {})
    
    # 根据编码阶段生成相应类型的备忘录
    if coding_stage == 'open':
        memos = generate_open_coding_memos(process_info, analysis_results)
    elif coding_stage == 'axial':
        memos = generate_axial_coding_memos(process_info, analysis_results)
    elif coding_stage == 'selective':
        memos = generate_selective_coding_memos(process_info, analysis_results)
    else:
        memos = generate_general_memos(process_info, analysis_results)
    
    # 返回备忘录撰写结果
    return {
        "memos": memos,
        "memo_count": len(memos),
        "memo_types": list(set(memo.get('type', 'general') for memo in memos)),
        "memo_writing_process": {
            "coding_stage": coding_stage,
            "memos_generated": len(memos),
            "date": datetime.now().isoformat()
        }
    }


def generate_open_coding_memos(process_info: Dict[str, Any], analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    生成开放编码阶段的备忘录
    
    Args:
        process_info: 过程信息
        analysis_results: 分析结果
    
    Returns:
        备忘录列表
    """
    memos = []
    
    # 过程备忘录
    process_memo = {
        "type": "process_memo",
        "title": f"开放编码会话备忘录 - {datetime.now().strftime('%Y-%m-%d')}",
        "date": datetime.now().isoformat(),
        "content": format_open_process_memo(process_info, analysis_results),
        "coding_stage": "open",
        "related_elements": analysis_results.get("concepts", [])[:3]  # 关联前3个概念
    }
    memos.append(process_memo)
    
    # 理论备忘录
    if analysis_results.get("concepts"):
        theory_memo = {
            "type": "theory_memo",
            "title": f"开放编码理论洞察备忘录 - {datetime.now().strftime('%Y-%m-%d')}",
            "date": datetime.now().isoformat(),
            "content": format_open_theory_memo(analysis_results),
            "coding_stage": "open",
            "related_elements": [c.get("id", "") for c in analysis_results.get("concepts", [])[:3]]
        }
        memos.append(theory_memo)
    
    # 反思备忘录
    reflection_memo = {
        "type": "reflection_memo",
        "title": f"开放编码反思备忘录 - {datetime.now().strftime('%Y-%m-%d')}",
        "date": datetime.now().isoformat(),
        "content": format_open_reflection_memo(process_info, analysis_results),
        "coding_stage": "open",
        "related_elements": []
    }
    memos.append(reflection_memo)
    
    return memos


def format_open_process_memo(process_info: Dict[str, Any], analysis_results: Dict[str, Any]) -> str:
    """
    格式化开放编码过程备忘录内容
    
    Args:
        process_info: 过程信息
        analysis_results: 分析结果
    
    Returns:
        格式化的过程备忘录内容
    """
    content = f"""
# 过程备忘录 - 开放编码会话

## 会话信息
- **日期**: {datetime.now().strftime('%Y-%m-%d')}
- **时间**: {process_info.get('session_duration', 'N/A')}
- **数据来源**: {process_info.get('data_source', 'N/A')}
- **编码类型**: 开放编码

## 编码决策
- **识别的概念数**: {len(analysis_results.get('concepts', []))}
- **编码理由**: {process_info.get('coding_reasons', 'N/A')}
- **遇到的问题**: {process_info.get('challenges', 'N/A')}

## 初步分析
- **观察到的模式**: {process_info.get('patterns', 'N/A')}
- **理论洞察**: {process_info.get('insights', 'N/A')}

## 下一步行动
- **立即行动**: {process_info.get('immediate_actions', 'N/A')}
- **进一步问题**: {process_info.get('follow_up_questions', 'N/A')}
"""
    return content.strip()


def format_open_theory_memo(analysis_results: Dict[str, Any]) -> str:
    """
    格式化开放编码理论备忘录内容
    
    Args:
        analysis_results: 分析结果
    
    Returns:
        格式化的理论备忘录内容
    """
    concepts = analysis_results.get('concepts', [])
    content = f"""
# 理论备忘录 - 开放编码理论洞察

## 当前理论状态
- **研究阶段**: 开放编码
- **识别概念数**: {len(concepts)}
- **概念示例**: {[c.get('code', '') for c in concepts[:3]] if concepts else []}

## 理论洞察
- **新的见解**: 在数据中发现了与{concepts[0].get('code', 'N/A') if concepts else 'N/A'}相关的模式
- **概念演化**: 初始概念逐渐向更抽象的层次发展
- **理论空白**: 需要进一步探索与{concepts[1].get('code', 'N/A') if len(concepts) > 1 else 'N/A'}相关的理论

## 实证支持
- **支持数据**: {len(concepts)}个初始概念提供了基础数据支持
- **案例示例**: 概念来自多个数据源，具有初步代表性

## 未来方向
- **完善需求**: 需要在轴心编码阶段进一步整合概念
- **研究意义**: 为后续理论构建提供基础概念
"""
    return content.strip()


def format_open_reflection_memo(process_info: Dict[str, Any], analysis_results: Dict[str, Any]) -> str:
    """
    格式化开放编码反思备忘录内容
    
    Args:
        process_info: 过程信息
        analysis_results: 分析结果
    
    Returns:
        格式化的反思备忘录内容
    """
    content = f"""
# 反思备忘录 - 开放编码反思

## 反思背景
- **反思触发点**: 完成开放编码阶段
- **当前进展**: 识别了{len(analysis_results.get('concepts', []))}个初始概念
- **遇到的挑战**: {process_info.get('challenges', 'N/A')}

## 批判性反思
- **成功之处**: 成功识别了数据中的初步概念模式
- **不足之处**: 某些概念边界不够清晰
- **原因分析**: 可能由于数据复杂性或编码经验不足
- **经验教训**: 需要更仔细地考虑概念的抽象层次

## 方法反思
- **方法有效性**: 开放编码方法有效识别了初始概念
- **存在局限**: 需要后续阶段进一步整合和精炼
- **适应需求**: 在后续编码中需要更关注概念间关系

## 理论反思
- **理论充分性**: 初步概念为理论构建提供了基础
- **概念清晰性**: 部分概念需要进一步澄清
- **理论贡献**: 为研究领域提供了初步概念框架
"""
    return content.strip()


def generate_axial_coding_memos(process_info: Dict[str, Any], analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    生成轴心编码阶段的备忘录
    
    Args:
        process_info: 过程信息
        analysis_results: 分析结果
    
    Returns:
        备忘录列表
    """
    memos = []
    
    # 过程备忘录
    process_memo = {
        "type": "process_memo",
        "title": f"轴心编码会话备忘录 - {datetime.now().strftime('%Y-%m-%d')}",
        "date": datetime.now().isoformat(),
        "content": format_axial_process_memo(process_info, analysis_results),
        "coding_stage": "axial",
        "related_elements": [cat.get("id", "") for cat in analysis_results.get("categories", [])[:3]]
    }
    memos.append(process_memo)
    
    # 理论备忘录
    if analysis_results.get("categories"):
        theory_memo = {
            "type": "theory_memo",
            "title": f"轴心编码理论洞察备忘录 - {datetime.now().strftime('%Y-%m-%d')}",
            "date": datetime.now().isoformat(),
            "content": format_axial_theory_memo(analysis_results),
            "coding_stage": "axial",
            "related_elements": [cat.get("id", "") for cat in analysis_results.get("categories", [])]
        }
        memos.append(theory_memo)
    
    # 关系备忘录
    if analysis_results.get("relationships"):
        relationship_memo = {
            "type": "relationship_memo",
            "title": f"范畴关系分析备忘录 - {datetime.now().strftime('%Y-%m-%d')}",
            "date": datetime.now().isoformat(),
            "content": format_relationship_memo(analysis_results),
            "coding_stage": "axial",
            "related_elements": [rel.get("id", "") for rel in analysis_results.get("relationships", [])]
        }
        memos.append(relationship_memo)
    
    return memos


def format_axial_process_memo(process_info: Dict[str, Any], analysis_results: Dict[str, Any]) -> str:
    """
    格式化轴心编码过程备忘录内容
    """
    categories = analysis_results.get('categories', [])
    relationships = analysis_results.get('relationships', [])
    
    content = f"""
# 过程备忘录 - 轴心编码会话

## 会话信息
- **日期**: {datetime.now().strftime('%Y-%m-%d')}
- **时间**: {process_info.get('session_duration', 'N/A')}
- **数据来源**: {process_info.get('data_source', 'N/A')}
- **编码类型**: 轴心编码

## 编码决策
- **构建的范畴数**: {len(categories)}
- **建立的关系数**: {len(relationships)}
- **编码理由**: {process_info.get('coding_reasons', 'N/A')}
- **遇到的问题**: {process_info.get('challenges', 'N/A')}

## 初步分析
- **范畴属性**: {process_info.get('properties_analysis', 'N/A')}
- **关系模式**: {process_info.get('relationship_patterns', 'N/A')}

## 下一步行动
- **立即行动**: {process_info.get('immediate_actions', 'N/A')}
- **进一步问题**: {process_info.get('follow_up_questions', 'N/A')}
"""
    return content.strip()


def format_axial_theory_memo(analysis_results: Dict[str, Any]) -> str:
    """
    格式化轴心编码理论备忘录内容
    """
    categories = analysis_results.get('categories', [])
    relationships = analysis_results.get('relationships', [])
    
    content = f"""
# 理论备忘录 - 轴心编码理论洞察

## 当前理论状态
- **研究阶段**: 轴心编码
- **构建范畴数**: {len(categories)}
- **建立关系数**: {len(relationships)}

## 理论洞察
- **新的见解**: 成功将开放编码的概念整合为{len(categories)}个主要范畴
- **概念演化**: 从离散概念发展为相互关联的范畴体系
- **理论空白**: 在范畴关系方面需要进一步探索

## 实证支持
- **支持数据**: {len(categories)}个范畴基于开放编码阶段的概念
- **案例示例**: 范畴间关系在数据中得到初步验证

## 未来方向
- **完善需求**: 需要在选择式编码中确定核心范畴
- **研究意义**: 建立了理论的范畴基础和关系网络
"""
    return content.strip()


def format_relationship_memo(analysis_results: Dict[str, Any]) -> str:
    """
    格式化关系分析备忘录内容
    """
    relationships = analysis_results.get('relationships', [])
    
    content = f"""
# 关系备忘录 - 范畴关系分析

## 关系分析
- **识别关系数**: {len(relationships)}
- **关系类型**: {list(set(rel.get('type', 'N/A') for rel in relationships)) if relationships else []}
- **平均强度**: {sum(rel.get('strength', 0) for rel in relationships) / len(relationships) if relationships else 0:.2f}

## 关系模式
- **主要模式**: {analysis_results.get('relationship_patterns', 'N/A')}
- **关键关系**: {relationships[0].get('description', 'N/A') if relationships else 'N/A'}

## 理论意义
- **理论贡献**: 范畴关系为理论机制提供了基础
- **验证需求**: 需要在后续阶段验证关系的稳定性
"""
    return content.strip()


def generate_selective_coding_memos(process_info: Dict[str, Any], analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    生成选择式编码阶段的备忘录
    
    Args:
        process_info: 过程信息
        analysis_results: 分析结果
    
    Returns:
        备忘录列表
    """
    memos = []
    
    # 核心范畴备忘录
    if analysis_results.get("core_category"):
        core_memo = {
            "type": "core_category_memo",
            "title": f"核心范畴识别备忘录 - {datetime.now().strftime('%Y-%m-%d')}",
            "date": datetime.now().isoformat(),
            "content": format_core_category_memo(analysis_results),
            "coding_stage": "selective",
            "related_elements": [analysis_results["core_category"].get("id", "")]
        }
        memos.append(core_memo)
    
    # 故事线备忘录
    if analysis_results.get("storyline"):
        storyline_memo = {
            "type": "storyline_memo",
            "title": f"故事线构建备忘录 - {datetime.now().strftime('%Y-%m-%d')}",
            "date": datetime.now().isoformat(),
            "content": format_storyline_memo(analysis_results),
            "coding_stage": "selective",
            "related_elements": [elem.get("from_category", "") for elem in analysis_results.get("storyline", {}).get("elements", [])]
        }
        memos.append(storyline_memo)
    
    # 理论框架备忘录
    if analysis_results.get("theory_framework"):
        theory_framework_memo = {
            "type": "theory_framework_memo",
            "title": f"理论框架整合备忘录 - {datetime.now().strftime('%Y-%m-%d')}",
            "date": datetime.now().isoformat(),
            "content": format_theory_framework_memo(analysis_results),
            "coding_stage": "selective",
            "related_elements": [analysis_results.get("theory_framework", {}).get("core_category", {}).get("id", "")]
        }
        memos.append(theory_framework_memo)
    
    return memos


def format_core_category_memo(analysis_results: Dict[str, Any]) -> str:
    """
    格式化核心范畴备忘录内容
    """
    core_cat = analysis_results.get('core_category', {})
    
    content = f"""
# 核心范畴备忘录 - 核心范畴识别

## 核心范畴信息
- **范畴名称**: {core_cat.get('name', 'N/A')}
- **解释力**: {core_cat.get('explanation_power', 'N/A')}
- **数据支持**: {core_cat.get('data_support', 'N/A')}
- **选择理由**: {core_cat.get('rationale', 'N/A')}

## 理论意义
- **中心地位**: 该范畴与最多其他范畴相关，是理论的核心
- **理论贡献**: 为整个理论提供了中心组织原则
- **验证需求**: 需要在饱和度检验中验证其核心地位
"""
    return content.strip()


def format_storyline_memo(analysis_results: Dict[str, Any]) -> str:
    """
    格式化故事线备忘录内容
    """
    storyline = analysis_results.get('storyline', {})
    
    content = f"""
# 故事线备忘录 - 故事线构建

## 故事线信息
- **中心主题**: {storyline.get('central_theme', 'N/A')}
- **元素数量**: {len(storyline.get('elements', []))}
- **连贯性得分**: {storyline.get('coherence_score', 'N/A')}

## 叙事流程
- **流程描述**: {storyline.get('narrative_flow', 'N/A')}

## 理论意义
- **叙事完整性**: 故事线连接了理论的主要组成部分
- **理论贡献**: 提供了现象的完整解释路径
- **验证需求**: 需要更多数据验证叙事的完整性
"""
    return content.strip()


def format_theory_framework_memo(analysis_results: Dict[str, Any]) -> str:
    """
    格式化理论框架备忘录内容
    """
    theory_framework = analysis_results.get('theory_framework', {})
    
    content = f"""
# 理论框架备忘录 - 理论框架整合

## 框架组成
- **核心范畴**: {theory_framework.get('core_category', {}).get('name', 'N/A')}
- **理论命题数**: {len(theory_framework.get('propositions', []))}
- **边界条件**: {theory_framework.get('boundary_conditions', [])}

## 理论贡献
- **主要命题**: {theory_framework.get('propositions', [{}])[0].get('statement', 'N/A') if theory_framework.get('propositions') else 'N/A'}
- **概念框架**: {theory_framework.get('conceptual_framework', {}).get('organizing_principle', 'N/A')}
- **作用机制**: {theory_framework.get('mechanisms', [{}])[0].get('type', 'N/A') if theory_framework.get('mechanisms') else 'N/A'}

## 理论意义
- **学术贡献**: 为研究领域提供了新的理论视角
- **实践意义**: 理论可指导实践中的决策和行动
- **验证需求**: 需要通过饱和度检验验证理论完整性
"""
    return content.strip()


def generate_general_memos(process_info: Dict[str, Any], analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    生成一般性备忘录
    
    Args:
        process_info: 过程信息
        analysis_results: 分析结果
    
    Returns:
        备忘录列表
    """
    memos = []
    
    general_memo = {
        "type": "general_memo",
        "title": f"研究过程备忘录 - {datetime.now().strftime('%Y-%m-%d')}",
        "date": datetime.now().isoformat(),
        "content": f"""
# 一般性研究备忘录

## 研究过程
- **日期**: {datetime.now().strftime('%Y-%m-%d')}
- **阶段**: {process_info.get('stage', 'N/A')}
- **主要活动**: {process_info.get('activity', 'N/A')}

## 结果摘要
- **分析结果**: {analysis_results}

## 反思
- **观察**: {process_info.get('observations', 'N/A')}
- **思考**: {process_info.get('reflections', 'N/A')}
""",
        "coding_stage": process_info.get('stage', 'general'),
        "related_elements": []
    }
    memos.append(general_memo)
    
    return memos