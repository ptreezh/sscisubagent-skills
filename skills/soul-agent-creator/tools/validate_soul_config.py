#!/usr/bin/env python3
"""
验证 Soul Agent 配置完整性

用法:
    from tools import validate_soul_config
    result = validate_soul_config.check(soul_dir)
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple


def check_yaml_format(file_path: Path) -> Tuple[bool, str]:
    """检查 YAML 格式"""
    try:
        import yaml
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        return True, "YAML 格式有效"
    except Exception as e:
        return False, f"YAML 格式错误：{str(e)}"


def check_soul_config(soul_dir: str) -> Dict:
    """验证 Soul Agent 配置完整性"""
    
    soul_path = Path(soul_dir)
    
    results = {
        "soul_id": soul_path.name,
        "checks": [],
        "passed": 0,
        "failed": 0,
        "warnings": 0,
        "overall": "pass",
    }
    
    # 必需文件检查
    required_files = [
        ("SOUL.md", "SOUL.md 文件存在性", "critical"),
        ("SOUL_CONFIG.yaml", "SOUL_CONFIG.yaml 文件存在性", "critical"),
        ("METHODOLOGY.md", "METHODOLOGY.md 文件存在性", "critical"),
        ("README.md", "README.md 文件存在性", "high"),
        ("metadata.json", "metadata.json 文件存在性", "high"),
    ]
    
    for filename, check_name, severity in required_files:
        file_path = soul_path / filename
        exists = file_path.exists()
        
        check_result = {
            "name": check_name,
            "file": filename,
            "passed": exists,
            "severity": severity,
        }
        
        if exists:
            results["passed"] += 1
            check_result["message"] = "✅ 文件存在"
        else:
            results["failed"] += 1
            check_result["message"] = f"❌ 文件缺失"
            if severity == "critical":
                results["overall"] = "fail"
        
        results["checks"].append(check_result)
    
    # 目录结构检查
    required_dirs = [
        ("memory/lessons", "教训记忆目录", "medium"),
        ("memory/patterns", "成功模式目录", "medium"),
        ("evolution", "进化记录目录", "medium"),
        ("cases/positive", "正面案例目录", "low"),
        ("cases/negative", "负面案例目录", "low"),
    ]
    
    for dirname, check_name, severity in required_dirs:
        dir_path = soul_path / dirname
        exists = dir_path.exists()
        
        check_result = {
            "name": check_name,
            "directory": dirname,
            "passed": exists,
            "severity": severity,
        }
        
        if exists:
            results["passed"] += 1
            check_result["message"] = "✅ 目录存在"
        else:
            results["warnings"] += 1
            check_result["message"] = f"⚠️ 目录缺失"
        
        results["checks"].append(check_result)
    
    # YAML 格式检查
    yaml_files = ["SOUL_CONFIG.yaml"]
    for filename in yaml_files:
        file_path = soul_path / filename
        if file_path.exists():
            valid, message = check_yaml_format(file_path)
            
            check_result = {
                "name": f"{filename} YAML 格式有效性",
                "file": filename,
                "passed": valid,
                "severity": "critical",
                "message": "✅ " + message if valid else "❌ " + message,
            }
            
            if valid:
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["overall"] = "fail"
            
            results["checks"].append(check_result)
    
    # metadata.json 检查
    metadata_path = soul_path / "metadata.json"
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # 检查必需字段
            required_fields = ["soul_id", "skill_id", "display_name", "created", "storage_path"]
            missing_fields = [f for f in required_fields if f not in metadata]
            
            check_result = {
                "name": "metadata.json 完整性",
                "file": "metadata.json",
                "passed": len(missing_fields) == 0,
                "severity": "high",
            }
            
            if len(missing_fields) == 0:
                results["passed"] += 1
                check_result["message"] = "✅ 所有必需字段存在"
            else:
                results["warnings"] += 1
                check_result["message"] = f"⚠️ 缺失字段：{', '.join(missing_fields)}"
            
            results["checks"].append(check_result)
        except json.JSONDecodeError as e:
            results["failed"] += 1
            results["overall"] = "fail"
            results["checks"].append({
                "name": "metadata.json JSON 格式",
                "file": "metadata.json",
                "passed": False,
                "severity": "high",
                "message": f"❌ JSON 格式错误：{str(e)}",
            })
    
    # SOUL.md 内容检查
    soul_md_path = soul_path / "SOUL.md"
    if soul_md_path.exists():
        with open(soul_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含必需的 sections
        required_sections = ["name:", "personality:", "values:", "capabilities:"]
        missing_sections = [s for s in required_sections if s not in content]
        
        check_result = {
            "name": "SOUL.md 内容完整性",
            "file": "SOUL.md",
            "passed": len(missing_sections) == 0,
            "severity": "high",
        }
        
        if len(missing_sections) == 0:
            results["passed"] += 1
            check_result["message"] = "✅ 所有必需部分存在"
        else:
            results["warnings"] += 1
            check_result["message"] = f"⚠️ 缺失部分：{', '.join(missing_sections)}"
        
        results["checks"].append(check_result)
    
    return results


def format_report(results: Dict) -> str:
    """格式化验证报告"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"Soul Agent 配置验证报告")
    lines.append("=" * 60)
    lines.append(f"\nSoul ID: {results['soul_id']}")
    lines.append(f"总体结果: {'✅ 通过' if results['overall'] == 'pass' else '❌ 失败'}")
    lines.append(f"\n统计:")
    lines.append(f"  通过：{results['passed']}")
    lines.append(f"  失败：{results['failed']}")
    lines.append(f"  警告：{results['warnings']}")
    lines.append(f"\n详细检查:")
    lines.append("-" * 60)
    
    for check in results["checks"]:
        status = "✅" if check["passed"] else ("⚠️" if check["severity"] != "critical" else "❌")
        lines.append(f"{status} {check['name']}: {check['message']}")
    
    lines.append("-" * 60)
    
    return "\n".join(lines)


def check(soul_dir: str, verbose: bool = True) -> bool:
    """执行验证并打印报告"""
    results = check_soul_config(soul_dir)
    
    if verbose:
        print(format_report(results))
    
    return results["overall"] == "pass"
