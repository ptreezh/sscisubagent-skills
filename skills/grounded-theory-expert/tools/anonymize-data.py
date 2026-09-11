"""
数据匿名化工具
移除文本中的人名、地名、机构名等可识别信息
"""

import re
from typing import Dict, List


def anonymize_text(text: str) -> str:
    """
    匿名化文本数据
    
    参数:
        text: 原始文本
    
    返回:
        匿名化后的文本
    """
    # 中文人名模式(简单匹配)
    text = re.sub(r'[张王李赵刘陈杨黄吴徐孙周郑谢冯于董萧程曹袁邓许傅沈曾彭吕苏卢蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江尹史顾侯邵孟万钱严覃武戴莫孔向汤', '某', text)
    
    # 英文人名(大写字母开头的单词)
    text = re.sub(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', '[姓名]', text)
    
    # 地名(简单匹配)
    place_patterns = [
        r'[北京上海广州深圳]',
        r'[省市县镇乡村]',
    ]
    for pattern in place_patterns:
        text = re.sub(pattern, '[地点]', text)
    
    # 电话号码
    text = re.sub(r'\b\d{3,4}[-\s]?\d{7,8}\b', '[电话]', text)
    text = re.sub(r'\b1[3-9]\d{9}\b', '[手机号]', text)
    
    # 邮箱
    text = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '[邮箱]', text)
    
    # 身份证号
    text = re.sub(r'\b\d{17}[\dXx]\b', '[身份证号]', text)
    
    # 日期(保留年份, 隐藏具体日期)
    text = re.sub(r'(\d{4})年\d{1,2}月\d{1,2}日', r'\1 年 XX 月 XX 日', text)
    
    return text


def anonymize_file(input_file: str, output_file: str) -> Dict:
    """
    匿名化文件
    
    参数:
        input_file: 输入文件路径
        output_file: 输出文件路径
    
    返回:
        匿名化统计信息
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    anonymized_text = anonymize_text(text)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(anonymized_text)
    
    return {
        'original_length': len(text),
        'anonymized_length': len(anonymized_text),
        'status': 'success'
    }


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) >= 3:
        result = anonymize_file(sys.argv[1], sys.argv[2])
        print(f"匿名化完成：{result}")
    else:
        # 测试
        test_text = "张三住在北京市朝阳区, 电话 13800138000"
        result = anonymize_text(test_text)
        print(f"原文：{test_text}")
        print(f"匿名化：{result}")
