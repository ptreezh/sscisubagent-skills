#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主题分析专家 - 代码提取工具
Code Extractor for Thematic Analysis

功能:
- 从文本数据中提取初始代码
- 支持开放性编码和结构化编码
- 生成编码簿
- 计算编码频率

作者: Thematic Analysis Expert v5.0.0
创建时间: 2026-03-15
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
from dataclasses import dataclass, asdict
import hashlib

# 跨平台兼容
def get_data_dir() -> Path:
    """获取数据目录"""
    return Path(__file__).parent.parent / "test_data"

def get_output_dir() -> Path:
    """获取输出目录"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@dataclass
class Code:
    """代码数据类"""
    code_id: str
    code_name: str
    code_definition: str
    source_quote: str
    source_location: str
    related_codes: List[str] = None
    memo: str = ""
    
    def __post_init__(self):
        if self.related_codes is None:
            self.related_codes = []
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CodedSegment:
    """编码片段数据类"""
    segment_id: str
    text: str
    codes: List[str]
    location: str
    participant: str
    context: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class CodeExtractor:
    """代码提取器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.codes: Dict[str, Code] = {}
        self.coded_segments: List[CodedSegment] = []
        self.code_counter = 0
        self.segment_counter = 0
        
    def generate_code_id(self) -> str:
        """生成代码ID"""
        self.code_counter += 1
        return f"C{self.code_counter:03d}"
    
    def generate_segment_id(self) -> str:
        """生成片段ID"""
        self.segment_counter += 1
        return f"S{self.segment_counter:04d}"
    
    def preprocess_text(self, text: str) -> str:
        """预处理文本"""
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符（保留中文和基本标点）
        text = text.strip()
        return text
    
    def segment_text(self, text: str, mode: str = "sentence") -> List[str]:
        """文本分段"""
        if mode == "sentence":
            # 按句子分割（中英文）
            segments = re.split(r'[。！？.!?]+', text)
            segments = [s.strip() for s in segments if s.strip()]
        elif mode == "paragraph":
            # 按段落分割
            segments = text.split('\n\n')
            segments = [s.strip() for s in segments if s.strip()]
        elif mode == "meaning_unit":
            # 按意义单位分割（简化实现）
            segments = re.split(r'[。！？；;.!?;]+', text)
            segments = [s.strip() for s in segments if s.strip()]
        else:
            segments = [text]
        
        return segments
    
    def extract_codes_from_segment(
        self, 
        segment: str, 
        location: str = "",
        participant: str = "",
        approach: str = "inductive"
    ) -> List[Code]:
        """从片段提取代码"""
        codes = []
        
        # 这里是简化的代码提取逻辑
        # 在实际应用中，可以集成NLP模型或规则系统
        
        # 示例：基于关键词的简单提取
        keywords = self.config.get("keywords", [])
        for keyword in keywords:
            if keyword in segment:
                code = Code(
                    code_id=self.generate_code_id(),
                    code_name=keyword,
                    code_definition=f"包含关键词: {keyword}",
                    source_quote=segment,
                    source_location=location,
                    memo="自动提取"
                )
                codes.append(code)
                self.codes[code.code_id] = code
        
        return codes
    
    def code_text(
        self,
        text: str,
        participant: str = "",
        segment_mode: str = "sentence",
        approach: str = "inductive"
    ) -> Dict:
        """
        编码文本
        
        Args:
            text: 待编码文本
            participant: 参与者标识
            segment_mode: 分段模式 (sentence/paragraph/meaning_unit)
            approach: 编码取向
        
        Returns:
            编码结果字典
        """
        # 预处理
        text = self.preprocess_text(text)
        
        # 分段
        segments = self.segment_text(text, segment_mode)
        
        # 编码每个片段
        results = []
        for i, segment in enumerate(segments):
            location = f"{participant}, 片段{i+1}" if participant else f"片段{i+1}"
            
            # 提取代码
            codes = self.extract_codes_from_segment(
                segment, 
                location, 
                participant,
                approach
            )
            
            # 创建编码片段
            coded_segment = CodedSegment(
                segment_id=self.generate_segment_id(),
                text=segment,
                codes=[c.code_id for c in codes],
                location=location,
                participant=participant
            )
            self.coded_segments.append(coded_segment)
            
            results.append({
                "segment_id": coded_segment.segment_id,
                "text": segment,
                "codes": [c.to_dict() for c in codes]
            })
        
        return {
            "status": "success",
            "total_segments": len(segments),
            "total_codes": len(self.codes),
            "results": results
        }
    
    def add_code_manually(
        self,
        code_name: str,
        code_definition: str,
        source_quote: str,
        source_location: str,
        memo: str = ""
    ) -> Code:
        """手动添加代码"""
        code = Code(
            code_id=self.generate_code_id(),
            code_name=code_name,
            code_definition=code_definition,
            source_quote=source_quote,
            source_location=source_location,
            memo=memo
        )
        self.codes[code.code_id] = code
        return code
    
    def get_code_frequency(self) -> Dict[str, int]:
        """获取代码频率"""
        code_freq = Counter()
        for segment in self.coded_segments:
            for code_id in segment.codes:
                code_freq[code_id] += 1
        return dict(code_freq)
    
    def get_codebook(self) -> List[Dict]:
        """获取编码簿"""
        codebook = []
        for code_id, code in self.codes.items():
            freq = self.get_code_frequency().get(code_id, 0)
            code_dict = code.to_dict()
            code_dict["frequency"] = freq
            codebook.append(code_dict)
        return codebook
    
    def export_results(self, output_format: str = "json") -> str:
        """导出结果"""
        results = {
            "codes": self.get_codebook(),
            "coded_segments": [s.to_dict() for s in self.coded_segments],
            "summary": {
                "total_codes": len(self.codes),
                "total_segments": len(self.coded_segments),
                "code_frequency": self.get_code_frequency()
            }
        }
        
        if output_format == "json":
            output_path = get_output_dir() / "coding_results.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            return str(output_path)
        
        elif output_format == "markdown":
            output_path = get_output_dir() / "coding_results.md"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# 编码结果\n\n")
                f.write("## 代码列表\n\n")
                for code in self.get_codebook():
                    f.write(f"### {code['code_id']}: {code['code_name']}\n")
                    f.write(f"- **定义**: {code['code_definition']}\n")
                    f.write(f"- **频率**: {code['frequency']}\n")
                    f.write(f"- **来源引文**: \"{code['source_quote']}\"\n\n")
            return str(output_path)
        
        return json.dumps(results, ensure_ascii=False, indent=2)


def validate_input(data: Any) -> bool:
    """验证输入数据"""
    if data is None:
        return False
    if isinstance(data, str):
        return len(data.strip()) > 0
    return True


def process_data(data: Any, options: Dict = None) -> Dict:
    """处理数据 - 主入口函数"""
    options = options or {}
    
    if not validate_input(data):
        return {
            "status": "error",
            "message": "输入数据无效"
        }
    
    extractor = CodeExtractor(config=options.get("config", {}))
    result = extractor.code_text(
        text=data,
        participant=options.get("participant", ""),
        segment_mode=options.get("segment_mode", "sentence"),
        approach=options.get("approach", "inductive")
    )
    
    return result


# 示例使用
if __name__ == "__main__":
    # 测试数据
    sample_text = """
    我觉得在线教学最大的挑战是如何保持学生的注意力。
    有时候网络不好，学生就听不清楚，这让我很frustrated。
    但是也有很多好处，比如可以录播，学生可以反复看。
    我认为技术支持很重要，没有好的技术支持什么都做不了。
    """
    
    # 创建提取器
    extractor = CodeExtractor()
    
    # 手动添加一些代码（模拟演绎式分析）
    extractor.add_code_manually(
        code_name="教学挑战",
        code_definition="教师在教学过程中遇到的困难和障碍",
        source_quote="在线教学最大的挑战是如何保持学生的注意力",
        source_location="参与者A, 第1句",
        memo="与技术相关的挑战"
    )
    
    extractor.add_code_manually(
        code_name="技术依赖",
        code_definition="教学活动对技术的依赖性",
        source_quote="技术支持很重要，没有好的技术支持什么都做不了",
        source_location="参与者A, 第4句",
        memo="强调了技术的基础性作用"
    )
    
    # 编码文本
    result = extractor.code_text(
        text=sample_text,
        participant="教师A",
        segment_mode="sentence"
    )
    
    # 输出结果
    print("编码结果:")
    print(f"- 总代码数: {result['total_codes']}")
    print(f"- 总片段数: {result['total_segments']}")
    
    # 导出编码簿
    codebook = extractor.get_codebook()
    print("\n编码簿:")
    for code in codebook:
        print(f"  {code['code_id']}: {code['code_name']} (频率: {code['frequency']})")
    
    print(f"\n主题分析代码提取工具已加载完成")
