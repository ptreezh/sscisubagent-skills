"""
开放编码模块
此模块提供扎根理论开放编码阶段的各项功能
"""

from typing import Dict, List, Any
import json


def open_coding(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行扎根理论的开放编码阶段
    
    Args:
        data: 包含质性数据的字典
    
    Returns:
        包含开放编码结果的字典
    """
    # 从数据中提取文本数据
    text_data = data.get('text_data', '')
    segments = data.get('segments', [])
    
    # 如果没有分段数据，则从文本数据创建分段
    if not segments and text_data:
        segments = split_text_into_segments(text_data)
    
    # 执行概念识别
    concepts = identify_concepts(segments)
    
    # 执行持续比较
    comparison_results = perform_constant_comparison(concepts)
    
    # 执行编码优化
    optimized_codes = optimize_codes(concepts, comparison_results)
    
    # 返回开放编码结果
    return {
        "concepts": optimized_codes,
        "concept_statistics": calculate_concept_statistics(optimized_codes),
        "coding_process": {
            "segments_processed": len(segments),
            "initial_concepts": len(concepts),
            "merged_concepts": comparison_results.get("merged_pairs", []),
            "refined_concepts": len(optimized_codes)
        },
        "memo_notes": generate_initial_memos(optimized_codes)
    }


def split_text_into_segments(text: str) -> List[str]:
    """
    将文本分割成段落或句子
    
    Args:
        text: 输入文本
    
    Returns:
        分段后的文本列表
    """
    # 简单的分段方法，按句号、问号、感叹号分割
    import re
    segments = re.split(r'[.!?。！？\n]+', text)
    # 过滤掉空段落
    segments = [seg.strip() for seg in segments if seg.strip()]
    return segments


def identify_concepts(segments: List[str]) -> List[Dict[str, Any]]:
    """
    从文本段落中识别概念
    
    Args:
        segments: 文本段落列表
    
    Returns:
        识别出的概念列表
    """
    concepts = []
    concept_id = 1
    
    for i, segment in enumerate(segments):
        # 简化的概念识别逻辑
        # 在实际应用中，这里会使用更复杂的NLP技术
        words = segment.split()
        for j, word in enumerate(words):
            if len(word) > 2:  # 只考虑长度大于2的词
                concept = {
                    "id": f"concept_{concept_id}",
                    "code": word,
                    "definition": f"概念定义：{word}",
                    "examples": [segment],
                    "segment_id": i,
                    "position_in_segment": j
                }
                concepts.append(concept)
                concept_id += 1
    
    return concepts


def perform_constant_comparison(concepts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    执行持续比较分析
    
    Args:
        concepts: 概念列表
    
    Returns:
        比较分析结果
    """
    # 简化的比较逻辑
    # 在实际应用中，这里会使用语义相似度算法
    comparison_results = {
        "similar_pairs": [],
        "merged_pairs": [],
        "relationship_matrix": {}
    }
    
    # 比较概念间的相似性
    for i, concept1 in enumerate(concepts):
        for j, concept2 in enumerate(concepts[i+1:], i+1):
            # 简化的相似性判断
            similarity = calculate_similarity(concept1["code"], concept2["code"])
            if similarity > 0.8:  # 相似度阈值
                comparison_results["similar_pairs"].append({
                    "concept1": concept1["id"],
                    "concept2": concept2["id"],
                    "similarity": similarity
                })
                
                # 合并相似概念
                comparison_results["merged_pairs"].append({
                    "kept": concept1["id"],
                    "merged": concept2["id"],
                    "reason": "High semantic similarity"
                })
    
    return comparison_results


def calculate_similarity(str1: str, str2: str) -> float:
    """
    计算两个字符串的相似度（简化版本）
    
    Args:
        str1: 字符串1
        str2: 字符串2
    
    Returns:
        相似度分数 (0-1)
    """
    # 简化的相似度计算
    if str1 == str2:
        return 1.0
    
    # 计算公共字符数
    common_chars = set(str1) & set(str2)
    total_chars = set(str1) | set(str2)
    
    if len(total_chars) == 0:
        return 0.0
    
    return len(common_chars) / len(total_chars)


def optimize_codes(concepts: List[Dict[str, Any]], comparison_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    优化编码结果
    
    Args:
        concepts: 原始概念列表
        comparison_results: 比较结果
    
    Returns:
        优化后的概念列表
    """
    # 创建概念ID到概念的映射
    concept_map = {concept["id"]: concept for concept in concepts}
    
    # 根据合并结果创建优化的概念列表
    kept_concept_ids = {pair["kept"] for pair in comparison_results.get("merged_pairs", [])}
    merged_concept_ids = {pair["merged"] for pair in comparison_results.get("merged_pairs", [])}
    
    # 保留未被合并的概念
    optimized_concepts = [
        concept_map[concept_id] 
        for concept_id in concept_map 
        if concept_id not in merged_concept_ids
    ]
    
    # 对合并的概念进行处理（简化处理）
    for pair in comparison_results.get("merged_pairs", []):
        kept_concept = concept_map[pair["kept"]]
        merged_concept = concept_map[pair["merged"]]
        
        # 将被合并概念的示例添加到保留概念中
        kept_concept["examples"].extend(merged_concept["examples"])
    
    return optimized_concepts


def calculate_concept_statistics(concepts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    计算概念统计信息
    
    Args:
        concepts: 概念列表
    
    Returns:
        统计信息字典
    """
    total_concepts = len(concepts)
    avg_examples_per_concept = sum(len(c.get("examples", [])) for c in concepts) / total_concepts if total_concepts > 0 else 0
    
    return {
        "total_concepts": total_concepts,
        "avg_examples_per_concept": avg_examples_per_concept,
        "concept_length_distribution": {}  # 简化版本
    }


def generate_initial_memos(concepts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    生成初始备忘录
    
    Args:
        concepts: 概念列表
    
    Returns:
        备忘录列表
    """
    memos = []
    
    for concept in concepts:
        memo = {
            "type": "process_memo",
            "title": f"关于概念 '{concept['code']}' 的备忘录",
            "content": f"在开放编码阶段识别出概念 '{concept['code']}'，定义为 {concept['definition']}。该概念在文本中出现了 {len(concept.get('examples', []))} 次。",
            "date": "2025-12-27",
            "related_concepts": [concept['id']]
        }
        memos.append(memo)
    
    return memos