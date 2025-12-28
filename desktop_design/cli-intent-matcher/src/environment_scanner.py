# 环境扫描模块

import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import os


class EnvironmentScanner:
    """扫描用户本地CLI环境"""
    
    def __init__(self):
        self.scan_results = {}
    
    def scan_all(self) -> Dict[str, Any]:
        """扫描所有环境信息"""
        print("开始扫描本地环境...")
        
        environment_info = {
            "timestamp": datetime.now().isoformat(),
            "system_info": self._get_system_info(),
            "cli_tools": self._scan_cli_tools(),
            "skills": self._scan_skills(),
            "available_models": []
        }
        
        self.scan_results = environment_info
        
        # 保存扫描结果
        self._save_scan_results(environment_info)
        
        print(f"环境扫描完成！找到 {len(environment_info['cli_tools'])} 个CLI工具和 {len(environment_info['skills'])} 个技能")
        return environment_info
    
    def _get_system_info(self) -> Dict[str, str]:
        """获取系统信息"""
        import platform
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": platform.python_version(),
            "architecture": platform.architecture()[0]
        }
    
    def _scan_cli_tools(self) -> Dict[str, Any]:
        """扫描CLI工具"""
        cli_list = ["stigmergy", "claude", "qwen", "gemini", "codebuddy", "iflow", "codex", "qodercli", "copilot"]
        cli_tools = {}
        
        for cli_name in cli_list:
            try:
                # 获取CLI帮助信息
                result = subprocess.run([cli_name, "--help"], 
                                      capture_output=True, text=True, timeout=10, shell=True,
                                      encoding='utf-8', errors='ignore')
                if result.returncode == 0 or result.returncode == 1:
                    cli_tools[cli_name] = {
                        "available": True,
                        "parameters": self._extract_parameters(result.stdout or ""),
                        "help_preview": (result.stdout or "")[:500]  # 仅保存前500个字符作为预览
                    }
                else:
                    # 尝试不带参数的命令
                    result2 = subprocess.run([cli_name], 
                                           capture_output=True, text=True, timeout=5, shell=True,
                                           encoding='utf-8', errors='ignore')
                    if result2.returncode != 2:  # 通常2表示命令不存在
                        cli_tools[cli_name] = {
                            "available": True,
                            "parameters": self._extract_parameters(result2.stdout or ""),
                            "help_preview": (result2.stdout or "")[:500]
                        }
                    else:
                        cli_tools[cli_name] = {"available": False, "error": "Command not found"}
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
                cli_tools[cli_name] = {"available": False, "error": str(e)}
        
        return cli_tools
    
    def _extract_parameters(self, help_text: str) -> List[str]:
        """从帮助文本中提取参数"""
        if not help_text:
            return []
        parameters = []
        lines = help_text.split('\n')
        for line in lines:
            if ' -' in line and ('--' in line or len(line.split()[0]) > 1):
                parts = line.strip().split()
                for part in parts:
                    if part.startswith('--') or part.startswith('-'):
                        param = part.split('=')[0].split('[')[0]
                        if param not in parameters:
                            parameters.append(param)
        return parameters
    
    def _scan_skills(self) -> Dict[str, Any]:
        """扫描可用的技能"""
        skills = {}
        
        try:
            # 使用stigmergy命令获取技能列表
            result = subprocess.run(["stigmergy", "skill", "list"], 
                                  capture_output=True, text=True, timeout=10, shell=True)
            if result.returncode == 0:
                skills = self._parse_skills_list(result.stdout)
            else:
                # 尝试使用另一个命令
                result2 = subprocess.run(["stigmergy", "skill-l"], 
                                       capture_output=True, text=True, timeout=10, shell=True)
                if result2.returncode == 0:
                    skills = self._parse_skills_list(result2.stdout)
        except Exception:
            # 如果命令行方式失败，尝试直接从stigmergy目录读取
            skills = self._load_skills_from_directory()
        
        return skills
    
    def _parse_skills_list(self, skills_text: str) -> Dict[str, Any]:
        """解析技能列表文本"""
        skills = {}
        if not skills_text:
            return skills
            
        lines = skills_text.split('\n')
        current_category = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('['):
                current_category = line.split(']')[0] + ']'
            elif line.startswith('  • ') and len(line) > 3:
                parts = line[4:].split('                ')
                skill_name = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ""
                skills[skill_name] = {
                    "description": description,
                    "category": current_category
                }
        
        return skills
    
    def _load_skills_from_directory(self) -> Dict[str, Any]:
        """从本地目录加载技能信息"""
        skills = {}
        try:
            from pathlib import Path
            home_dir = Path.home()
            skill_dir = home_dir / ".stigmergy" / "skills"
            
            if skill_dir.exists():
                for skill_path in skill_dir.iterdir():
                    if skill_path.is_dir():
                        skill_name = skill_path.name
                        readme_path = skill_path / "README.md"
                        if readme_path.exists():
                            with open(readme_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # 简单提取描述信息
                                lines = content.split('\n')
                                description = "No description available"
                                for line in lines[:10]:  # 只检查前10行
                                    if line.strip().startswith("description:") or ':' in line and 'description' in line.lower():
                                        description = line.strip().split(':', 1)[1].strip()
                                        break
                                    elif line.strip().startswith("---"):
                                        continue
                                    elif line.strip() and not line.strip().startswith('#'):
                                        description = line.strip()
                                        break
                                skills[skill_name] = {
                                    "description": description,
                                    "category": "local"
                                }
                        else:
                            skills[skill_name] = {
                                "description": "Local skill",
                                "category": "local"
                            }
        except Exception:
            pass
        
        return skills
    
    def _save_scan_results(self, environment_info: Dict[str, Any]):
        """保存扫描结果"""
        config_dir = Path("cli-intent-matcher/config")
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_path = config_dir / "environment_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(environment_info, f, indent=2, ensure_ascii=False)
    
    def get_scan_results(self) -> Dict[str, Any]:
        """获取扫描结果"""
        return self.scan_results if self.scan_results else self._load_previous_scan()
    
    def _load_previous_scan(self) -> Dict[str, Any]:
        """加载之前的扫描结果"""
        config_path = Path("cli-intent-matcher/config/environment_config.json")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}


def main():
    scanner = EnvironmentScanner()
    results = scanner.scan_all()
    print("扫描结果:")
    print(f"系统信息: {results['system_info']}")
    print(f"CLI工具: {list(results['cli_tools'].keys())}")
    print(f"技能: {list(results['skills'].keys())}")


if __name__ == "__main__":
    main()