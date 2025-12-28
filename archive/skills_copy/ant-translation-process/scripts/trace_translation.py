#!/usr/bin/env python3
"""
ANT转译过程分析工具 - 智能依赖管理和功能降级系统

此脚本专门用于分析行动者网络中的转译过程，优先使用高级功能，如不可用则降级到基础实现
"""

import argparse
import json
import sys
import importlib
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Any, Optional


def install_package(package_name: str) -> bool:
    """尝试安装包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False


def check_and_import(module_name: str, package_name: Optional[str] = None) -> Any:
    """检查并导入模块，如失败则返回None"""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        if package_name:
            print(f"模块 {module_name} 未找到，正在尝试安装 {package_name}...")
            if install_package(package_name):
                try:
                    return importlib.import_module(module_name)
                except ImportError:
                    print(f"安装后仍然无法导入 {module_name}")
                    return None
            else:
                print(f"无法安装 {package_name}")
                return None
        return None


# 尝试导入高级包
np = check_and_import("numpy")
pd = check_and_import("pandas")
nx = check_and_import("networkx", "networkx")
sns = check_and_import("seaborn", "seaborn")
plt = check_and_import("matplotlib.pyplot", "matplotlib")

# 检查高级功能是否可用
ADVANCED_AVAILABLE = all([np, pd, nx])


def identify_problematization_phase(text: str) -> List[Dict[str, Any]]:
    """识别问题化阶段"""
    # 问题化阶段通常涉及问题定义、挑战识别、目标设定等
    problematization_patterns = [
        r'需要解决(.+?)[问题|挑战|难题]',
        r'面临(.+?)[问题|挑战|困难]',
        r'如何(.+?)[解决|应对|处理]',
        r'存在(.+?)[问题|缺陷|不足]',
        r'针对(.+?)[问题|挑战|议题]',
        r'problem of (.+?)',
        r'challenge of (.+?)',
        r'need to address (.+?)'
    ]

    problems = []
    for pattern in problematization_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            problems.append({
                'problem': match.strip(),
                'type': 'problematization',
                'evidence': match.strip()
            })

    return problems


def identify_interestement_phase(text: str) -> List[Dict[str, Any]]:
    """识别利益化阶段"""
    # 利益化阶段涉及利益协商、角色分配、利益绑定等
    interessement_patterns = [
        r'使(.+?)[感兴趣|关注|在意]',
        r'让(.+?)[参与|加入|支持]',
        r'将(.+?)[纳入|吸引|招募]',
        r'与(.+?)[合作|协作|配合]',
        r'使(.+?)[同意|接受|认可]',
        r'make (.+?) interested',
        r'engage (.+?) in',
        r'involve (.+?) in'
    ]

    interests = []
    for pattern in interessement_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            interests.append({
                'actor': match.strip(),
                'type': 'interessement',
                'evidence': match.strip()
            })

    return interests


def identify_enrollment_phase(text: str) -> List[Dict[str, Any]]:
    """识别征召阶段"""
    # 征召阶段涉及招募、代表、代言等
    enrolment_patterns = [
        r'代表(.+?)[说话|行动|发声]',
        r'代言(.+?)[利益|观点|立场]',
        r'使(.+?)[成为|担任|充当]',
        r'招募(.+?)[参与|加入|参加]',
        r'委托(.+?)[代表|代理|代言]',
        r'represent (.+?)',
        r'appoint (.+?) as',
        r'enroll (.+?) in'
    ]

    enrolments = []
    for pattern in enrolment_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            enrolments.append({
                'actor': match.strip(),
                'type': 'enrolment',
                'evidence': match.strip()
            })

    return enrolments


def identify_mobilization_phase(text: str) -> List[Dict[str, Any]]:
    """识别动员阶段"""
    # 动员阶段涉及行动协调、资源调动、集体行动等
    mobilization_patterns = [
        r'动员(.+?)[行动|参与|努力]',
        r'协调(.+?)[行动|资源|力量]',
        r'调动(.+?)[积极性|资源|力量]',
        r'促使(.+?)[采取|实施|执行]',
        r'推动(.+?)[实现|完成|达成]',
        r'mobilize (.+?) to',
        r'coordinate (.+?) to',
        r'facilitate (.+?)'
    ]

    mobilizations = []
    for pattern in mobilization_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            mobilizations.append({
                'actor': match.strip(),
                'type': 'mobilization',
                'evidence': match.strip()
            })

    return mobilizations


def analyze_translation_chains(problems: List[Dict], interests: List[Dict], 
                              enrolments: List[Dict], mobilizations: List[Dict]) -> List[Dict[str, Any]]:
    """分析转译链条"""
    chains = []

    # 尝试连接不同阶段的元素形成转译链
    for problem in problems:
        chain = {
            'start': problem,
            'phases': [problem],
            'continuity': 0  # 连续性指标
        }

        # 查找相关的利益化元素
        for interest in interests:
            # 简单的文本相似度匹配
            if any(token in interest['evidence'] for token in problem['evidence'].split()[:3]):
                chain['phases'].append(interest)
                chain['continuity'] += 1

        # 查找相关的征召元素
        for enrolment in enrolments:
            if any(token in enrolment['evidence'] for token in problem['evidence'].split()[:3]):
                chain['phases'].append(enrolment)
                chain['continuity'] += 1

        # 查找相关的动员元素
        for mobilization in mobilizations:
            if any(token in mobilization['evidence'] for token in problem['evidence'].split()[:3]):
                chain['phases'].append(mobilization)
                chain['continuity'] += 1

        if len(chain['phases']) > 1:  # 至少有两个阶段才构成链条
            chains.append(chain)

    return chains


def identify_controversies_and_failures(text: str) -> List[Dict[str, Any]]:
    """识别争议和失败"""
    controversy_patterns = [
        r'争议|分歧|争论|辩论|冲突',
        r'失败|挫折|困难|障碍|阻力',
        r'反对|抵制|拒绝|不接受',
        r'质疑|怀疑|挑战|批评',
        r'conflict|dispute|controversy|debate',
        r'failure|difficulty|obstacle|resistance',
        r'rejection|refusal|opposition'
    ]

    controversies = []
    sentences = re.split(r'[。！？\\n]', text)
    for sentence in sentences:
        for pattern in controversy_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                controversies.append({
                    'type': 'controversy' if any(word in pattern for word in ['争议', '分歧', '争论', 'conflict', 'dispute', 'controversy', 'debate']) else 'failure',
                    'evidence': sentence.strip(),
                    'context': text[max(0, text.find(sentence)-100):text.find(sentence)+len(sentence)+100].strip()
                })
                break  # 找到一个匹配就跳出

    return controversies


def calculate_translation_metrics(chains: List[Dict]) -> Dict[str, Any]:
    """计算转译指标"""
    if ADVANCED_AVAILABLE:
        try:
            import networkx as nx

            # 将转译链转换为网络进行分析
            G = nx.DiGraph()

            for chain in chains:
                phases = chain['phases']
                for i in range(len(phases)-1):
                    source = f"{phases[i]['type']}_{i}"
                    target = f"{phases[i+1]['type']}_{i+1}"
                    G.add_edge(source, target, **phases[i+1])

            metrics = {
                'n_chains': len(chains),
                'avg_chain_length': sum(len(chain['phases']) for chain in chains) / len(chains) if chains else 0,
                'chain_continuity': sum(chain['continuity'] for chain in chains) / len(chains) if chains else 0,
                'network_density': nx.density(G) if G.number_of_nodes() > 1 else 0,
                'is_connected': nx.is_connected(G.to_undirected()) if G.number_of_nodes() > 0 else False
            }

            return metrics
        except Exception as e:
            print(f"高级转译分析失败: {e}，使用基础分析")

    # 降级到基础实现
    return {
        'n_chains': len(chains),
        'avg_chain_length': sum(len(chain['phases']) for chain in chains) / len(chains) if chains else 0,
        'chain_continuity': sum(chain['continuity'] for chain in chains) / len(chains) if chains else 0,
        'chains': chains  # 返回原始链条数据
    }


def main():
    parser = argparse.ArgumentParser(
        description='ANT转译过程分析工具（支持高级功能，提供优雅降级）',
        epilog='示例：python ant_translation_analysis.py --input data.json --output results.json'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON格式）')
    parser.add_argument('--output', '-o', default='ant_translation.json', help='输出文件')

    args = parser.parse_args()

    start_time = datetime.now()

    # 读取输入数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)

    # 确定要分析的文本
    if isinstance(data, dict):
        if 'text' in data:
            text = data['text']
        elif 'content' in data:
            text = data['content']
        else:
            text = json.dumps(data, ensure_ascii=False)
    elif isinstance(data, list):
        text = ' '.join(str(item) for item in data)
    elif isinstance(data, str):
        text = data
    else:
        text = str(data)

    # 识别四个转译阶段
    problems = identify_problematization_phase(text)
    interests = identify_interestement_phase(text)
    enrolments = identify_enrolment_phase(text)
    mobilizations = identify_mobilization_phase(text)

    # 分析转译链条
    chains = analyze_translation_chains(problems, interests, enrolments, mobilizations)

    # 识别争议和失败
    controversies = identify_controversies_and_failures(text)

    # 计算转译指标
    metrics = calculate_translation_metrics(chains)

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'n_problems': len(problems),
            'n_interests': len(interests),
            'n_enrolments': len(enrolments),
            'n_mobilizations': len(mobilizations),
            'n_chains': len(chains),
            'n_controversies': len(controversies),
            'processing_time': round((end_time - start_time).total_seconds(), 2),
            'using_advanced': ADVANCED_AVAILABLE
        },
        'details': {
            'problematization': problems,
            'interessement': interests,
            'enrolment': enrolments,
            'mobilization': mobilizations,
            'translation_chains': chains,
            'controversies': controversies,
            'metrics': metrics
        },
        'metadata': {
            'input_file': args.input,
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'ant-translation-process'
        }
    }

    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ ANT转译过程分析完成")
    print(f"  - 问题化阶段: {len(problems)} 个")
    print(f"  - 利益化阶段: {len(interests)} 个")
    print(f"  - 征召阶段: {len(enrolments)} 个")
    print(f"  - 动员阶段: {len(mobilizations)} 个")
    print(f"  - 转译链条: {len(chains)} 条")
    print(f"  - 争议识别: {len(controversies)} 个")
    print(f"  - 使用高级功能: {output['summary']['using_advanced']}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()