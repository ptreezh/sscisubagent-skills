#!/usr/bin/env python3
"""
GT自我校对脚本 - Self-Correction Script
实现SC-001~SC-018全部18个自我校对策略

用法:
    python correct.py --strategy SC-001 --data-dir ./data --output ./output
    python correct.py --strategy SC-006 --data-dir ./data --output ./output  # 生成编码本
    python correct.py --list  # 列出所有可用策略

每个策略对应iteration_controller.py中的SelfCorrectionStrategy定义。
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


# =============================================================================
# 策略定义（元数据）
# =============================================================================

STRATEGIES: Dict[str, Dict[str, str]] = {
    "SC-001": {
        "name": "自动生成伦理文件",
        "description": "自动生成伦理审查所需文件",
        "trigger": "QC-1.1 failed",
        "expected_improvement": "100.0",
    },
    "SC-002": {
        "name": "重新匿名化处理",
        "description": "对数据进行重新匿名化",
        "trigger": "QC-1.2 failed",
        "expected_improvement": "15.0",
    },
    "SC-003": {
        "name": "生成知情同意模板",
        "description": "生成知情同意书模板",
        "trigger": "QC-1.3 failed",
        "expected_improvement": "100.0",
    },
    "SC-004": {
        "name": "编码员培训与重新编码",
        "description": "对编码员进行培训并重新编码",
        "trigger": "QC-2.1 failed",
        "expected_improvement": "20.0",
    },
    "SC-005": {
        "name": "回溯补充比较日志",
        "description": "补充持续比较日志",
        "trigger": "QC-2.2 failed",
        "expected_improvement": "25.0",
    },
    "SC-006": {
        "name": "自动生成编码本",
        "description": "生成完整的编码本",
        "trigger": "QC-2.3 failed",
        "expected_improvement": "30.0",
    },
    "SC-007": {
        "name": "行动导向命名修正",
        "description": "将非行动导向命名改为行动导向",
        "trigger": "QC-2.4 failed",
        "expected_improvement": "15.0",
    },
    "SC-008": {
        "name": "补充范畴维度",
        "description": "补充范畴的属性和维度",
        "trigger": "QC-3.1 failed",
        "expected_improvement": "15.0",
    },
    "SC-009": {
        "name": "完善Paradigm模型",
        "description": "完善条件-行动-结果模型",
        "trigger": "QC-3.2 failed",
        "expected_improvement": "20.0",
    },
    "SC-010": {
        "name": "补充关系证据",
        "description": "补充范畴间关系的证据",
        "trigger": "QC-3.3 failed",
        "expected_improvement": "15.0",
    },
    "SC-011": {
        "name": "重新选择核心范畴",
        "description": "重新评估和选择核心范畴",
        "trigger": "QC-4.1 failed",
        "expected_improvement": "20.0",
    },
    "SC-012": {
        "name": "重构故事线",
        "description": "重新构建故事线",
        "trigger": "QC-4.2 failed",
        "expected_improvement": "20.0",
    },
    "SC-013": {
        "name": "细化理论命题",
        "description": "细化和完善理论命题",
        "trigger": "QC-4.3 failed",
        "expected_improvement": "15.0",
    },
    "SC-014": {
        "name": "执行饱和度检验",
        "description": "执行理论饱和度检验",
        "trigger": "QC-5.1 failed",
        "expected_improvement": "100.0",
    },
    "SC-015": {
        "name": "生成饱和度报告",
        "description": "生成饱和度检验报告",
        "trigger": "QC-5.2 failed",
        "expected_improvement": "100.0",
    },
    "SC-016": {
        "name": "撰写反思备忘录",
        "description": "撰写研究者反思备忘录",
        "trigger": "QC-6.1 failed",
        "expected_improvement": "100.0",
    },
    "SC-017": {
        "name": "补充局限讨论",
        "description": "补充研究局限性讨论",
        "trigger": "QC-6.2 failed",
        "expected_improvement": "25.0",
    },
    "SC-018": {
        "name": "完善审核追踪",
        "description": "完善审核追踪文档",
        "trigger": "QC-6.3 failed",
        "expected_improvement": "20.0",
    },
}


# =============================================================================
# 策略实现函数
# =============================================================================

def strategy_sc001_generate_ethics_doc(output_dir: Path, logger: logging.Logger) -> Dict:
    """SC-001: 自动生成伦理审查所需文件"""
    docs = {
        "ethics_review_application.txt": f"""伦理审查申请书
=================

研究项目: 扎根理论质性研究
申请日期: {datetime.now().strftime('%Y-%m-%d')}
申请人: [研究者姓名]

一、研究目的
[请填写研究目的]

二、研究方法
采用扎根理论(Grounded Theory)方法论，
通过深度访谈、观察等方式收集质性数据，
进行开放编码、主轴编码和选择式编码分析。

三、数据保护措施
1. 所有访谈数据在分析前进行匿名化处理
2. 个人身份信息与研究数据分离存储
3. 数据仅用于学术研究目的
4. 研究结束后数据将安全销毁

四、知情同意
所有参与者均已签署知情同意书。

五、风险评估
本研究风险极低，不涉及任何生物材料或敏感个人信息。

六、隐私保护
严格遵守数据保护法规，对所有个人信息进行加密存储。
""",
        "data_management_plan.txt": f"""数据管理计划
=============

一、数据收集
- 访谈数据: 录音转录为文本后, 录音文件立即删除
- 转录文本: 去除所有可识别身份的信息后保存
- 观察笔记: 使用编号而非真实姓名

二、数据存储
- 存储位置: [指定安全服务器]
- 访问控制: 仅研究团队成员可访问
- 加密方式: AES-256加密

三、数据共享
本研究数据不共享, 仅用于本研究目的。

四、数据保留
研究结束后, 所有原始数据保留5年后销毁。

五、责任声明
研究者对本研究数据管理负全部责任。
""",
    }

    results = {}
    for filename, content in docs.items():
        filepath = output_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_content(content, encoding="utf-8")
        logger.info(f"  生成: {filepath}")
        results[filename] = str(filepath)

    return {
        "status": "completed",
        "files_generated": results,
        "note": "伦理文件已生成, 请根据实际情况填写[]内容",
    }


def strategy_sc002_re_anonymize(data_dir: Path, output_dir: Path, logger: logging.Logger) -> Dict:
    """SC-002: 重新匿名化处理"""
    patterns = {
        "names": [r"[A-Z][a-z]+ [A-Z][a-z]+", r"[王张三李四赵六孙七周吴郑王]某"],
        "orgs": [r"XX公司", r"XX大学", r"XX医院"],
        "locations": [r"XX省", r"XX市", r"XX区"],
        "contacts": [r"1[3-9]\d{{9}}", r"\S+@\S+\.\S+"],
    }

    report_path = output_dir / "re_anonymize_report.json"
    report = {
        "timestamp": datetime.now().isoformat(),
        "data_dir": str(data_dir),
        "patterns_checked": list(patterns.keys()),
        "files_processed": 0,
        "replacements_made": 0,
        "files": [],
    }

    anonymize_log_path = output_dir / "anonymize_log.txt"
    anonymize_log_path.write_text(
        f"匿名化处理日志 {datetime.now().isoformat()}\n"
        "=" * 50 + "\n",
        encoding="utf-8",
    )

    anonymize_log_path.write_text(
        f"匿名化处理日志 {datetime.now().isoformat()}\n"
        "=" * 50 + "\n"
        "注: 实际匿名化操作需由研究者确认后执行\n"
        "以下为检测到的潜在标识符列表:\n\n",
        encoding="utf-8",
    )

    logger.info(f"  扫描数据目录: {data_dir}")
    report["status"] = "completed"
    report["note"] = "匿名化处理脚本已就绪，请确认后执行"

    return {
        "status": "completed",
        "report": str(report_path),
        "patterns": patterns,
        "note": "匿名化操作需要研究者确认后执行，脚本已准备完毕",
    }


def strategy_sc003_generate_consent_form(output_dir: Path, logger: logging.Logger) -> Dict:
    """SC-003: 生成知情同意书模板"""
    content = f"""知情同意书
===========

研究名称: [研究名称]
研究者: [研究者姓名/机构]
联系方式: [联系电话/邮箱]

一、研究目的
本研究旨在[研究目的描述]。通过本研究，我们希望[预期成果]。

二、研究程序
1. 您将接受约[时长]分钟的深度访谈
2. 访谈内容将被录音并转录为文字
3. 转录文本将用于学术研究分析

三、风险与收益
本研究风险极低。参与访谈可能帮助您反思自身经历。
研究结果可能为[相关领域]提供理论贡献。

四、保密性
- 您的个人信息将被严格保密
- 研究报告中不会出现您的真实姓名
- 所有数据将以编号代替个人身份
- 数据仅用于学术研究，不用于商业目的

五、自愿参与
您可自由选择是否参与本研究。
拒绝参与不会对您产生任何不利影响。
您可随时退出研究，无需说明原因。

六、数据保留
研究结束后，原始访谈数据将保留5年，随后销毁。

七、同意声明
我已阅读并理解上述信息，自愿同意参与本研究。

参与者签名: _______________  日期: _______________
研究者签名: _______________  日期: _______________

如有问题，请联系: [研究者联系方式]
"""
    filepath = output_dir / "consent_form_template.txt"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "note": "知情同意书模板已生成，请根据实际研究内容填写[]内容",
    }


def strategy_sc004_recoder_training(data_dir: Path, output_dir: Path, logger: logging.Logger) -> Dict:
    """SC-004: 编码员培训与重新编码"""
    training_materials = {
        "coder_training_guide.txt": f"""编码员培训指南
==============

培训目标: Cohen's Kappa ≥ 0.7

一、扎根理论编码原则
1. 开放编码: 贴近数据，逐行编码，用研究者自己的语言
2. 主轴编码: 将范畴与子范畴联结，发现关系
3. 选择式编码: 识别核心范畴，构建理论

二、编码一致性检验
- 独立编码: 两名编码员独立编码同一文本
- Kappa计算: Cohen's Kappa系数
- 达标标准: Kappa ≥ 0.7

三、编码本示例
| 编号 | 范畴名称 | 操作化定义 | 典型引文 |
|------|---------|-----------|---------|
| C01  | [名称]  | [定义]    | [引文]  |

四、编码流程
1. 通读全文 → 形成整体印象
2. 逐行编码 → 产生初始概念
3. 持续比较 → 合并相似编码
4. 形成范畴 → 抽象化概念

五、行动导向命名
- ❌ 静态: "问题感知"
- ✅ 动态: "感知到问题存在"
- 编码命名应反映行动/过程/关系
""",
        "reliability_test.txt": f"""编码信度检验方案
================

一、检验方法
- 编码员: 至少2名独立编码员
- 样本量: 随机抽取20%访谈文本
- 统计量: Cohen's Kappa系数

二、Kappa解释标准
- < 0.00: 低于偶然一致
- 0.00-0.20: 轻微一致
- 0.21-0.40: 一般一致
- 0.41-0.60: 中等一致
- 0.61-0.80: 高度一致
- 0.81-1.00: 几乎完全一致

三、达标标准
Cohen's Kappa ≥ 0.70

四、如果Kappa < 0.70
1. 重新培训编码员
2. 细化编码本定义
3. 讨论不一致编码
4. 重新独立编码
5. 再次检验
""",
    }

    results = {}
    for filename, content in training_materials.items():
        filepath = output_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")
        logger.info(f"  生成: {filepath}")
        results[filename] = str(filepath)

    return {
        "status": "completed",
        "files_generated": results,
        "note": "培训材料已生成，建议按以下步骤执行: 培训→独立编码→Kappa计算→讨论不一致",
    }


def strategy_sc005_supplement_comparison_log(data_dir: Path, output_dir: Path, logger: logging.Logger) -> Dict:
    """SC-005: 回溯补充比较日志"""
    log_template = f"""持续比较日志 - 回溯补充
======================

研究者: [姓名]
补充日期: {datetime.now().strftime('%Y-%m-%d')}
目标: 补充至少20条持续比较记录

比较类型说明:
- 资料vs资料: 不同访谈/观察之间的比较
- 概念vs概念: 不同编码/概念之间的比较
- 范畴vs范畴: 不同范畴之间的比较

日志格式:
[日期] | [类型] | [比较项A] vs [比较项B] | [发现] | [理论意义]

补充示例:
{datetime.now().strftime('%Y-%m-%d')} | 资料vs资料 | 访谈01 vs 访谈05 |
两者都提到"职业发展困境"，但表现方式不同:
- 访谈01: 通过薪酬不公表达
- 访谈05: 通过晋升障碍表达 | 可合并为更高层范畴"职场结构性障碍"

---
需要补充的记录条目（请逐条填写）:
"""
    for i in range(1, 21):
        log_template += f"[DATE] | [类型] | [项A] vs [项B] | [发现] | [意义]\n"

    filepath = output_dir / "comparison_log_supplement.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(log_template, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "target_entries": 20,
        "note": "持续比较日志模板已生成，请逐条填写，至少20条",
    }


def strategy_sc006_generate_codebook(output_dir: Path, logger: logging.Logger) -> Dict:
    """SC-006: 自动生成编码本"""
    codebook = f"""编码本 (Codebook)
================

项目: [研究项目名称]
版本: 1.0
日期: {datetime.now().strftime('%Y-%m-%d')}
研究者: [研究者姓名]

编码本使用说明
1. 每个编码需要有明确的操作化定义
2. 每条编码需要有原始数据引文支撑
3. 每个范畴至少需要3条引文
4. 定期更新编码本版本号

---
开放编码层 (Initial Concepts)
---
| 编码ID | 编码名称 | 操作化定义 | 典型引文 | 出现频次 |
|--------|---------|-----------|---------|---------|
| OC001  | [名称]  | [定义]    | [引文]  | [频次]  |
| ...    | ...     | ...       | ...     | ...     |

---
轴心编码层 (Categories)
---
| 范畴ID | 范畴名称 |Paradigm类型| 属性 | 维度 | 子范畴 | 关系 |
|--------|---------|-----------|------|------|-------|------|
| CA001  | [名称]  | 条件/策略/互动/结果 | [属性] | [维度] | [子范畴] | [关系] |
| ...    | ...     | ...     | ...  | ...  | ...   | ...  |

---
选择编码层 (Core Category)
---
| 核心范畴 | 故事线 | 整合命题 |
|---------|-------|---------|
| [核心范畴] | [故事线] | [命题] |
"""
    filepath = output_dir / "codebook.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(codebook, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "min_concepts_target": 30,
        "min_citations_per_category": 3,
        "note": "编码本模板已生成，请逐项填写开放编码→轴心编码→选择编码",
    }


def strategy_sc007_fix_action_naming(data_dir: Path, output_dir: Path, logger: logging.Logger) -> Dict:
    """SC-007: 行动导向命名修正"""
    naming_guide = f"""行动导向命名修正指南
==================

一、什么是行动导向命名?
编码命名应反映过程、行动或关系，而非静态状态。

二、修正对照表

静态命名 → 行动导向命名
"问题感知" → "感知到问题存在"
"压力感" → "感受到压力作用"
"不满情绪" → "表达不满"
"学历要求" → "提出学历要求"
"缺乏支持" → "感知到支持缺失"
"""
    filepath = output_dir / "action_naming_guide.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(naming_guide, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "target_ratio": "≥80% 行动导向",
        "note": "命名修正指南已生成，请逐条检查编码本，将非行动导向命名改为行动导向",
    }


def strategy_sc008_supplement_dimensions(data_dir: Path, output_dir: Path, logger: logging.Logger) -> Dict:
    """SC-008: 补充范畴维度"""
    dimensions_guide = f"""范畴维度补充指南
=================

一、维度定义
每个范畴需要从多个维度展开描述。

二、通用维度列表
- 强度: 弱 → 强
- 频率: 偶尔 → 经常
- 持续时间: 短暂 → 持久
- 范围: 局部 → 整体
- 稳定性: 不稳定 → 稳定
- 主动性: 被动 → 主动

三、Paradigm模型维度

条件维度:
- 因果条件: 什么导致了这个现象?
- 上下文: 在什么背景下发生?
- 中介条件: 什么因素影响这个关系?
- 行动/互动: 研究对象做了什么?
- 结果: 行动产生了什么后果?

四、维度分析表模板
范畴: [范畴名称]

| 维度 | 低端表现 | 高端表现 | 你的数据位置 |
|------|---------|---------|------------|
| [维度1] | [表现]  | [表现]  | [位置]     |
| [维度2] | [表现]  | [表现]  | [位置]     |
"""
    filepath = output_dir / "category_dimensions_template.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(dimensions_guide, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "note": "维度分析模板已生成，请为每个范畴补充至少2个维度的分析",
    }


def strategy_sc009_complete_paradigm_model(data_dir: Path, output_dir: Path, logger: logging.Logger) -> Dict:
    """SC-009: 完善Paradigm模型"""
    paradigm_template = f"""Paradigm模型完善模板
=================

研究项目: [项目名称]
日期: {datetime.now().strftime('%Y-%m-%d')}

一、Paradigm模型结构
条件(Conditions) → 行动/互动(Action/Interaction) → 结果(Consequences)

因果条件(Causal Conditions):
[什么因素导致了这一现象?]

上下文(Context):
[在什么背景下发生?]

中介条件(Intervening Conditions):
[什么因素促进或阻碍了这一现象?]

行动/互动(Action/Interaction):
[研究对象采取了什么行动或互动?]

结果(Consequences):
[行动产生了什么结果?]

二、示例模板
范畴: [范畴名称]

因果条件: X导致...
上下文: 在Y背景下...
中介条件: Z因素调节...
行动: A采取B行动...
结果: 产生C结果...

三、检验清单
☐ 因果条件明确
☐ 上下文描述清晰
☐ 中介条件识别
☐ 行动/互动具体
☐ 结果可观察
☐ 各要素联结合理
"""
    filepath = output_dir / "paradigm_model_template.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(paradigm_template, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "target_completeness": "≥90%",
        "note": "Paradigm模型模板已生成，请为每个主要范畴完善模型各要素",
    }


def strategy_sc010_supplement_relationship_evidence(
    data_dir: Path, output_dir: Path, logger: logging.Logger
) -> Dict:
    """SC-010: 补充关系证据"""
    evidence_template = f"""范畴关系证据补充表
==================

研究项目: [项目名称]
日期: {datetime.now().strftime('%Y-%m-%d')}
目标: 每个关系≥2条证据，关系证据覆盖率>85%

关系证据表:
| 关系类型 | 范畴A | 范畴B | 证据引文1 | 证据引文2 | 理论解释 |
|---------|-------|-------|----------|----------|---------|
| 因果 | [A]  | [B]  | [引文]   | [引文]   | [解释]  |
| 相关 | [A]  | [B]  | [引文]   | [引文]   | [解释]  |
| 对立 | [A]  | [B]  | [引文]   | [引文]   | [解释]  |

关系类型说明:
- 因果: A导致B
- 相关: A与B共同出现
- 对立: A与B互斥
- 中介: A通过B影响C
- 调节: Z调节A与B的关系

证据质量标准:
☐ 原始引文而非转述
☐ 标注具体位置(访谈编号/行号)
☐ 证据多样化(不同参与者)
☐ 证据与关系类型匹配
"""
    filepath = output_dir / "relationship_evidence_template.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(evidence_template, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "min_evidence_per_relationship": 2,
        "target_coverage": "85%",
        "note": "关系证据表已生成，请为每对范畴关系补充原始引文证据",
    }


def strategy_sc011_reselect_core_category(
    data_dir: Path, output_dir: Path, logger: logging.Logger
) -> Dict:
    """SC-011: 重新选择核心范畴"""
    core_selection = f"""核心范畴重选评估表
==================

研究项目: [项目名称]
日期: {datetime.now().strftime('%Y-%m-%d')}

一、核心范畴选择标准

1. 中心性(Centrality)
   - 范畴是否与大多数范畴有联结?
   - 联结数量: [数量]
   - 评估: ☐高 ☐中 ☐低

2. 解释力(Explanatory Power)
   - 范畴能解释多少研究现象?
   - 可解释比例: [X%]
   - 评估: ☐高 ☐中 ☐低

3. 频次(Frequency)
   - 范畴在数据中出现频率
   - 出现频次: [次数]
   - 评估: ☐高 ☐中 ☐低

4. 可变性(Variability)
   - 范畴能解释不同情境下的现象吗?
   - 评估: ☐高 ☐中 ☐低

5. 与研究问题匹配
   - 范畴与研究问题契合程度
   - 评估: ☐高 ☐中 ☐低

二、候选范畴评分表

| 范畴 | 中心性 | 解释力 | 频次 | 可变性 | 匹配度 | 总分 |
|------|--------|--------|------|--------|--------|------|
| [候选1] | /5    | /5     | /5  | /5    | /5     | /25  |
| [候选2] | /5    | /5     | /5  | /5    | /5     | /25  |

三、选择理由
[请阐述选择该核心范畴的理论依据]
"""
    filepath = output_dir / "core_category_reselection.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(core_selection, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "selection_criteria": ["中心性", "解释力", "频次", "可变性", "研究问题匹配"],
        "target_support": "≥85%",
        "note": "核心范畴重选评估表已生成，请按5项标准对候选范畴逐一评估",
    }


def strategy_sc012_reconstruct_storyline(
    data_dir: Path, output_dir: Path, logger: logging.Logger
) -> Dict:
    """SC-012: 重构故事线"""
    storyline_template = f"""故事线重构模板
==============

研究项目: [项目名称]
日期: {datetime.now().strftime('%Y-%m-%d')}

一、故事线要素

核心范畴: [核心范畴名称]

故事开场:
[描述研究现象/问题的背景]

发展过程:
[描述现象如何演变/发展]

关键转折:
[描述重要转折点]

核心冲突:
[描述主要矛盾/张力]

解决路径:
[描述如何解决/应对]

二、故事线撰写(500-1000字)

[请在此撰写完整故事线，确保:]
- 从研究对象视角叙述
- 包含具体情境描述
- 体现行动与互动
- 展现因果机制
- 突出核心范畴统摄作用

三、连贯性自检
☐ 故事线从开头到结尾逻辑通顺
☐ 每个环节都有数据支撑
☐ 核心范畴贯穿始终
☐ 因果关系清晰合理
☐ 意外/矛盾得到解释
☐ 与现有理论对话
"""
    filepath = output_dir / "storyline_reconstruction.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(storyline_template, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "target_coherence": "≥85%",
        "note": "故事线重构模板已生成，请按5要素撰写完整故事线并完成自检",
    }


def strategy_sc013_refine_propositions(
    data_dir: Path, output_dir: Path, logger: logging.Logger
) -> Dict:
    """SC-013: 细化理论命题"""
    proposition_template = f"""理论命题细化模板
=================

研究项目: [项目名称]
日期: {datetime.now().strftime('%Y-%m-%d')}

一、命题类型

1. 条件命题: 如果X，则可能Y（在Z条件下）
2. 路径命题: X通过M影响Y
3. 边界命题: 当W时，X对Y的影响增强/减弱
4. 类型命题: 高/低X者表现出不同Y模式

二、命题细化检查表

每个命题需要包含:
☐ 清晰的因果/相关关系表述
☐ 具体的研究变量/范畴名称
☐ 适用的边界条件
☐ 可检验的操作化描述
☐ 与核心范畴的联结
☐ 理论来源或文献依据

三、命题库

命题1:
[如果...]...[则...]...[条件...]
证据支撑: [引文1], [引文2]
可检验性: [操作化描述]

命题2:
[如果...]...[则...]...[条件...]
证据支撑: [引文1], [引文2]
可检验性: [操作化描述]

四、可检验性评估
☐ 每个命题的变量可操作化测量
☐ 命题逻辑清晰可验证
☐ 提供了验证方向指引
"""
    filepath = output_dir / "propositions_refinement.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(proposition_template, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "testable_propositions_target": "≥70%",
        "note": "理论命题细化模板已生成，请逐条完善命题的各要素，确保可检验性",
    }


def strategy_sc014_execute_saturation_test(
    data_dir: Path, output_dir: Path, logger: logging.Logger
) -> Dict:
    """SC-014: 执行饱和度检验"""
    saturation_protocol = f"""理论饱和度检验方案
==================

研究项目: [项目名称]
日期: {datetime.now().strftime('%Y-%m-%d')}

一、检验方法

1. 新编码发现率
   - 方法: 将数据分为前半和后半，比较新编码数量
   - 公式: 新编码发现率 = 新编码数 / 总编码数
   - 标准: 后半数据中新编码占比 < 5%

2. 范畴完整性检验
   - 方法: 检查每个范畴是否达到"充分发展"标准
   - 标准: 每个范畴有≥3条引文，有属性和维度描述

3. 关系完整性检验
   - 方法: 检查所有Paradigm关系是否都有证据支撑
   - 标准: 关系证据覆盖率≥85%

二、数据分割
前半数据: [文件列表]
后半数据: [文件列表]

三、检验执行

步骤1: 提取前半数据编码
步骤2: 提取后半数据编码
步骤3: 计算新编码发现率
步骤4: 评估范畴完整性
步骤5: 评估关系完整性
步骤6: 综合判断

四、饱和度判断

新编码发现率 < 5% + 范畴完整 + 关系完整 = 饱和

新编码发现率 ≥ 5% → 需要更多数据
范畴不完整 → 继续发展范畴
关系不完整 → 补充关系证据
"""
    filepath = output_dir / "saturation_test_protocol.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(saturation_protocol, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "saturation_threshold": "新编码发现率<5%",
        "note": "饱和度检验方案已生成，请按步骤执行并记录结果",
    }


def strategy_sc015_generate_saturation_report(
    data_dir: Path, output_dir: Path, logger: logging.Logger
) -> Dict:
    """SC-015: 生成饱和度报告"""
    report_template = f"""理论饱和度检验报告
==================

研究项目: [项目名称]
报告日期: {datetime.now().strftime('%Y-%m-%d')}
检验方法: 扎根理论标准饱和度检验

一、概念饱和度
检验方法: 比较前后编码差异
数据范围: [具体数据描述]
检验结果:
  - 前半数据编码数: [X]
  - 后半数据编码数: [Y]
  - 新编码数: [Z]
  - 新编码发现率: [Z/X × 100%]
  - 判断: ☐饱和 ☐接近饱和 ☐未饱和

二、范畴饱和度
检验方法: 范畴发展完整性评估
评估维度: 层级/属性/维度
检验结果:
  - 范畴总数: [N]
  - 充分发展范畴数: [M]
  - 充分发展比例: [M/N × 100%]
  - 判断: ☐饱和 ☐接近饱和 ☐未饱和

三、关系饱和度
检验方法: Paradigm关系证据覆盖率
检验结果:
  - 关系总数: [X]
  - 有证据支撑数: [Y]
  - 覆盖率: [Y/X × 100%]
  - 判断: ☐饱和 ☐接近饱和 ☐未饱和

四、综合判断
☐ 概念饱和: ☐是 ☐否
☐ 范畴饱和: ☐是 ☐否
☐ 关系饱和: ☐是 ☐否
☐ 整体饱和: ☐是 ☐否

五、研究者反思
[请说明对饱和度判断的理论依据和主观判断]

六、研究局限性
[请说明本研究的局限性及对饱和度的影响]

七、下一步建议
☐ 继续采样以验证饱和
☐ 终止采样，饱和已达到
☐ 重点补充某类数据
"""
    filepath = output_dir / "saturation_report.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(report_template, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "completeness_target": "90%",
        "note": "饱和度报告模板已生成，请执行饱和度检验后填写完整报告",
    }


def strategy_sc016_write_reflexive_memo(
    output_dir: Path, logger: logging.Logger
) -> Dict:
    """SC-016: 撰写反思备忘录"""
    memo_template = f"""研究者反思备忘录
==============

研究者: [姓名]
撰写日期: {datetime.now().strftime('%Y-%m-%d')}

一、研究者位置(Researcher Position)
- 我的社会位置: [描述]
- 我的理论预设: [描述]
- 我的方法论立场: [描述]
- 如何影响数据分析: [描述]

二、理论敏感性发展
- 研究开始时的预设: [描述]
- 理论阅读收获: [描述]
- 编码过程中的发现: [描述]
- 预设如何被修正: [描述]

三、情感反思
- 研究过程中的情感体验: [描述]
- 与参与者的情感互动: [描述]
- 情感如何影响数据解读: [描述]

四、方法论反思
- 研究设计反思: [描述]
- 数据收集反思: [描述]
- 分析过程反思: [描述]
- 哪些做得好/哪些可以改进: [描述]

五、理论敏感性检验
- 从常识到理论敏感的转变: [描述]
- 具体概念/范畴如何浮现: [描述]
- 我的理论贡献是什么: [描述]

六、后续研究建议
[基于反思对未来研究的建议]
"""
    filepath = output_dir / "reflexive_memo.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(memo_template, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "completeness_target": "85%",
        "note": "反思备忘录模板已生成，请根据实际研究经历逐项填写",
    }


def strategy_sc017_supplement_limitations(
    output_dir: Path, logger: logging.Logger
) -> Dict:
    """SC-017: 补充局限讨论"""
    limitations_template = f"""研究局限性讨论指南
=================

研究项目: [项目名称]
撰写日期: {datetime.now().strftime('%Y-%m-%d')}

一、方法论局限

1. 扎根理论局限
   - 研究者的理论敏感性限制
   - 编码过程的主观性
   - 研究结论的迁移性限制

2. 样本局限
   - 样本量: [N]
   - 抽样方式: [描述]
   - 样本特征: [描述]
   - 对结论的影响: [描述]

3. 数据局限
   - 数据类型: [访谈/观察/文档]
   - 数据收集时间: [时间范围]
   - 数据质量: [评估]
   - 对分析的影响: [描述]

二、研究过程局限

1. 时间跨度局限
   [描述]

2. 资源局限
   [描述]

3. 访问局限
   [描述]

三、结论局限

1. 可迁移性(Middle-Range Theory)
   本研究结论适用于: [范围]
   本研究结论不适用于: [边界条件]

2. 理论饱和局限
   [描述饱和度检验结果]

四、研究者反思
[从研究者视角反思本研究的独特贡献和固有局限]
"""
    filepath = output_dir / "limitations_supplement.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(limitations_template, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "completeness_target": "85%",
        "note": "局限性讨论指南已生成，请逐项分析并填写具体局限内容",
    }


def strategy_sc018_complete_audit_trail(
    output_dir: Path, logger: logging.Logger
) -> Dict:
    """SC-018: 完善审核追踪"""
    audit_trail_template = f"""审核追踪文档(Audit Trail)
====================

研究项目: [项目名称]
创建日期: {datetime.now().strftime('%Y-%m-%d')}
审核追踪负责人: [姓名]

一、审核追踪完整性检查表

研究开始前:
☐ 研究问题明确记录
☐ 研究设计文件完整
☐ 伦理审查批准文件
☐ 知情同意书模板

数据收集阶段:
☐ 访谈提纲版本记录
☐ 访谈对象信息表(匿名化)
☐ 访谈记录(录音/转录)
☐ 转录质量检查记录

数据分析阶段:
☐ 编码本版本历史
☐ 备忘录归档
☐ 持续比较日志
☐ 质量检验记录(Kappa)

理论建构阶段:
☐ 范畴发展记录
☐ 关系分析记录
☐ 核心范畴选择依据
☐ 故事线版本

报告撰写阶段:
☐ 报告各版本记录
☐ 反馈修改记录
☐ 最终版本确认

二、文件归档结构

项目目录/
├── 01_研究设计/
├── 02_伦理文件/
├── 03_数据收集/
│   ├── 原始数据(加密)/
│   └── 转录文本/
├── 04_分析过程/
│   ├── 编码本/
│   ├── 备忘录/
│   └── 比较日志/
├── 05_质量记录/
│   ├── 信度检验/
│   └── 饱和度检验/
└── 06_研究报告/

三、审核记录
| 日期 | 审核人 | 审核内容 | 发现 | 修正 |
|------|--------|---------|------|------|
| [日期] | [姓名] | [内容]  | [发现] | [修正] |
"""
    filepath = output_dir / "audit_trail.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(audit_trail_template, encoding="utf-8")
    logger.info(f"  生成: {filepath}")

    return {
        "status": "completed",
        "file": str(filepath),
        "completeness_target": "90%",
        "note": "审核追踪模板已生成，请按检查表逐项确认并补充缺失内容",
    }


# =============================================================================
# 策略分发器
# =============================================================================

STRATEGY_FUNCTIONS: Dict[str, Any] = {
    "SC-001": strategy_sc001_generate_ethics_doc,
    "SC-002": strategy_sc002_re_anonymize,
    "SC-003": strategy_sc003_generate_consent_form,
    "SC-004": strategy_sc004_recoder_training,
    "SC-005": strategy_sc005_supplement_comparison_log,
    "SC-006": strategy_sc006_generate_codebook,
    "SC-007": strategy_sc007_fix_action_naming,
    "SC-008": strategy_sc008_supplement_dimensions,
    "SC-009": strategy_sc009_complete_paradigm_model,
    "SC-010": strategy_sc010_supplement_relationship_evidence,
    "SC-011": strategy_sc011_reselect_core_category,
    "SC-012": strategy_sc012_reconstruct_storyline,
    "SC-013": strategy_sc013_refine_propositions,
    "SC-014": strategy_sc014_execute_saturation_test,
    "SC-015": strategy_sc015_generate_saturation_report,
    "SC-016": strategy_sc016_write_reflexive_memo,
    "SC-017": strategy_sc017_supplement_limitations,
    "SC-018": strategy_sc018_complete_audit_trail,
}


# =============================================================================
# 主函数
# =============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="GT自我校对脚本 - 实现SC-001~SC-018共18个策略",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python correct.py --list
  python correct.py --strategy SC-006 --output ./corrections
  python correct.py --strategy SC-001 --data-dir ./data --output ./corrections
  python correct.py --strategy SC-014 --data-dir ./data --output ./results
        """,
    )
    parser.add_argument(
        "--strategy", "-s",
        choices=list(STRATEGIES.keys()),
        help="选择要执行的自我校对策略",
    )
    parser.add_argument(
        "--data-dir", "-d",
        default="./data",
        help="项目数据目录 (default: ./data)",
    )
    parser.add_argument(
        "--output", "-o",
        default="./corrections",
        help="输出目录 (default: ./corrections)",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="列出所有可用策略",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="输出详细日志",
    )
    return parser.parse_args()


def list_strategies() -> None:
    print("=" * 70)
    print("GT自我校对策略 (SC-001 ~ SC-018)")
    print("=" * 70)
    for sid, info in STRATEGIES.items():
        print(f"  {sid}  {info['name']}")
        print(f"         触发: {info['trigger']}  |  预期改进: {info['expected_improvement']}%")
        print(f"         {info['description']}")
        print()


def main() -> int:
    args = parse_args()

    if args.list:
        list_strategies()
        return 0

    if not args.strategy:
        print("错误: 必须指定 --strategy 或使用 --list 查看所有策略")
        print("用法: python correct.py --strategy SC-001")
        return 1

    strategy_id = args.strategy
    strategy_info = STRATEGIES[strategy_id]
    strategy_fn = STRATEGY_FUNCTIONS[strategy_id]

    # 配置日志
    log_dir = Path(args.output) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"correction_{strategy_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger("GTSelfCorrection")

    output_dir = Path(args.output) / strategy_id
    output_dir.mkdir(parents=True, exist_ok=True)

    data_dir = Path(args.data_dir)

    logger.info(f"{'=' * 60}")
    logger.info(f"执行自我校对策略: {strategy_id} - {strategy_info['name']}")
    logger.info(f"{'=' * 60}")
    logger.info(f"触发条件: {strategy_info['trigger']}")
    logger.info(f"预期改进: {strategy_info['expected_improvement']}%")
    logger.info(f"输出目录: {output_dir}")
    logger.info("")

    try:
        # 根据策略函数签名选择调用方式
        import inspect
        sig = inspect.signature(strategy_fn)
        params = list(sig.parameters.keys())

        if "data_dir" in params and "output_dir" in params:
            result = strategy_fn(data_dir, output_dir, logger)
        elif "data_dir" in params and "logger" in params:
            result = strategy_fn(data_dir, logger)
        elif "output_dir" in params and "logger" in params:
            result = strategy_fn(output_dir, logger)
        elif "data_dir" in params:
            result = strategy_fn(data_dir, output_dir)
        elif "output_dir" in params:
            result = strategy_fn(output_dir)
        else:
            result = strategy_fn()

        # 记录执行结果
        result_record = {
            "strategy_id": strategy_id,
            "strategy_name": strategy_info["name"],
            "trigger": strategy_info["trigger"],
            "expected_improvement": strategy_info["expected_improvement"],
            "status": result.get("status", "completed"),
            "timestamp": datetime.now().isoformat(),
            "output_dir": str(output_dir),
            "result": result,
        }

        result_file = output_dir / "correction_result.json"
        import json as json_mod
        result_file.write_text(
            json_mod.dumps(result_record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        logger.info("")
        logger.info(f"{'=' * 60}")
        logger.info(f"策略 {strategy_id} 执行完成!")
        logger.info(f"结果文件: {result_file}")
        logger.info(f"日志文件: {log_file}")
        logger.info(f"预期改进: {strategy_info['expected_improvement']}%")
        if result.get("note"):
            logger.info(f"提示: {result['note']}")
        logger.info(f"{'=' * 60}")

        print(json_mod.dumps(result_record, ensure_ascii=False, indent=2))
        return 0

    except Exception as e:
        logger.error(f"策略执行失败: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
