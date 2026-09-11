#!/usr/bin/env python3
"""
Skill 配置加载器

每个 skill 都应该在自己的目录下查找必要的配置文件
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class SkillConfigLoader:
    """
    Skill 配置加载器
    
    自动查找 skill 目录下的配置文件
    """
    
    def __init__(self, skill_name: str, skill_dir: Optional[str] = None):
        """
        初始化配置加载器
        
        参数:
            skill_name: skill 名称
            skill_dir: skill 目录路径(如果为 None, 则自动查找)
        """
        self.skill_name = skill_name
        
        if skill_dir:
            self.skill_dir = Path(skill_dir)
        else:
            # 自动查找 skill 目录
            self.skill_dir = self._find_skill_directory(skill_name)
        
        self.soul = None
        self.hooks = None
        self.qwen_config = None
    
    def _find_skill_directory(self, skill_name: str) -> Path:
        """
        查找 skill 目录
        
        查找顺序：
        1. 当前目录下的 skill_name 目录
        2. ~/.qwen/skills/skill_name 目录
        3. 环境变量 SKILL_{skill_name}_DIR 指定的目录
        """
        # 1. 当前目录
        current_dir = Path.cwd()
        skill_path = current_dir / skill_name
        if skill_path.exists():
            return skill_path
        
        # 2. ~/.qwen/skills/
        home_dir = Path.home()
        qwen_skill_path = home_dir / '.qwen' / 'skills' / skill_name
        if qwen_skill_path.exists():
            return qwen_skill_path
        
        # 3. 环境变量
        env_var = f'SKILL_{skill_name.upper().replace("-", "_")}_DIR'
        env_path = os.environ.get(env_var)
        if env_path:
            return Path(env_path)
        
        # 如果都找不到, 返回当前目录
        return current_dir / skill_name
    
    def load_soul(self) -> Optional[Dict[str, Any]]:
        """
        加载 soul.md
        
        返回:
            soul.md 的内容(解析为字典)
        """
        soul_path = self.skill_dir / 'soul.md'
        
        if not soul_path.exists():
            print(f"⚠️ 警告：soul.md 不存在于 {self.skill_dir}")
            return None
        
        with open(soul_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 YAML Front Matter
        soul_data = self._parse_yaml_frontmatter(content)
        self.soul = soul_data
        
        return soul_data
    
    def load_hooks(self) -> Optional[Dict[str, Any]]:
        """
        加载 skill-hooks.yaml
        
        返回:
            hooks 配置
        """
        hooks_path = self.skill_dir / 'skill-hooks.yaml'
        
        if not hooks_path.exists():
            print(f"⚠️ 警告：skill-hooks.yaml 不存在于 {self.skill_dir}")
            return None
        
        with open(hooks_path, 'r', encoding='utf-8') as f:
            self.hooks = yaml.safe_load(f)
        
        return self.hooks
    
    def load_qwen_config(self) -> Optional[Dict[str, Any]]:
        """
        加载 qwen-skill.yaml
        
        返回:
            Qwen CLI 配置
        """
        config_path = self.skill_dir / 'qwen-skill.yaml'
        
        if not config_path.exists():
            print(f"⚠️ 警告：qwen-skill.yaml 不存在于 {self.skill_dir}")
            return None
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.qwen_config = yaml.safe_load(f)
        
        return self.qwen_config
    
    def _parse_yaml_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        解析 Markdown 文件的 YAML Front Matter
        
        参数:
            content: Markdown 文件内容
        
        返回:
            解析后的字典
        """
        lines = content.split('\n')
        
        # 查找 Front Matter
        if not lines[0].strip() == '---':
            return {}
        
        frontmatter_lines = []
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                break
            frontmatter_lines.append(line)
        
        # 解析 YAML
        try:
            return yaml.safe_load('\n'.join(frontmatter_lines))
        except:
            return {}
    
    def get_skill_info(self) -> Dict[str, Any]:
        """
        获取 skill 信息
        
        返回:
            包含 skill 名称、目录、配置等信息
        """
        # 加载所有配置
        soul = self.load_soul()
        hooks = self.load_hooks()
        qwen_config = self.load_qwen_config()
        
        return {
            'skill_name': self.skill_name,
            'skill_directory': str(self.skill_dir),
            'soul': soul,
            'hooks': hooks,
            'qwen_config': qwen_config,
            'files_found': {
                'soul.md': (self.skill_dir / 'soul.md').exists(),
                'skill-hooks.yaml': (self.skill_dir / 'skill-hooks.yaml').exists(),
                'qwen-skill.yaml': (self.skill_dir / 'qwen-skill.yaml').exists()
            }
        }


# 使用示例
if __name__ == '__main__':
    # 测试加载 grounded-theory-expert
    loader = SkillConfigLoader('grounded-theory-expert')
    info = loader.get_skill_info()
    
    print(f"Skill: {info['skill_name']}")
    print(f"Directory: {info['skill_directory']}")
    print(f"Files found:")
    for file, found in info['files_found'].items():
        status = '✅' if found else '❌'
        print(f"  {status} {file}")
    
    if info['soul']:
        print(f"\nSoul.md 内容:")
        print(f"  Role: {info['soul'].get('role', 'N/A')}")
        print(f"  Values: {info['soul'].get('values', [])}")
