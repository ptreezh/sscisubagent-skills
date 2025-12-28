# 自适应训练模块

import json
import os
import subprocess
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np


class AdaptiveTrainer:
    """自适应训练模块 - 根据用户环境和使用数据训练模型"""
    
    def __init__(self, model_path: str = "cli-intent-matcher/data/models"):
        self.model_path = model_path
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.classifier = MultiOutputClassifier(
            RandomForestClassifier(n_estimators=100, random_state=42)
        )
        self.user_logs_path = "cli-intent-matcher/data/user_logs"
        self.training_history_path = "cli-intent-matcher/data/training_history"
        
        # 确保目录存在
        Path(self.user_logs_path).mkdir(parents=True, exist_ok=True)
        Path(self.training_history_path).mkdir(parents=True, exist_ok=True)
    
    def scan_environment(self) -> Dict[str, Any]:
        """扫描用户本地环境"""
        environment_info = {
            "timestamp": datetime.now().isoformat(),
            "cli_tools": {},
            "skills": {},
            "available_models": []
        }
        
        # 扫描CLI工具
        cli_list = ["stigmergy", "claude", "qwen", "gemini", "codebuddy", "iflow", "codex", "qodercli", "copilot"]
        
        for cli_name in cli_list:
            try:
                result = subprocess.run([cli_name, "--help"], 
                                      capture_output=True, text=True, timeout=10, shell=True,
                                      encoding='utf-8', errors='ignore')
                if result.returncode == 0 or result.returncode == 1:
                    environment_info["cli_tools"][cli_name] = {
                        "available": True,
                        "parameters": self._extract_parameters(result.stdout or "")
                    }
                else:
                    environment_info["cli_tools"][cli_name] = {"available": False}
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                environment_info["cli_tools"][cli_name] = {"available": False}
        
        # 扫描技能
        try:
            result = subprocess.run(["stigmergy", "skill", "list"], 
                                  capture_output=True, text=True, timeout=10, shell=True)
            if result.returncode == 0:
                skills = self._parse_skills_list(result.stdout)
                environment_info["skills"] = skills
        except Exception:
            # 如果命令失败，尝试从本地目录加载
            environment_info["skills"] = self._load_skills_from_directory()
        
        # 保存环境配置
        env_config_path = "cli-intent-matcher/config/environment_config.json"
        Path(env_config_path).parent.mkdir(parents=True, exist_ok=True)
        with open(env_config_path, 'w', encoding='utf-8') as f:
            json.dump(environment_info, f, indent=2, ensure_ascii=False)
        
        return environment_info
    
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
            import os
            from pathlib import Path
            home_dir = Path.home()
            skill_dir = home_dir / ".stigmergy" / "skills"
            
            if skill_dir.exists():
                for skill_path in skill_dir.iterdir():
                    if skill_path.is_dir():
                        skill_name = skill_path.name
                        skills[skill_name] = {
                            "description": "Local skill",
                            "category": "local"
                        }
        except Exception:
            pass
        
        return skills
    
    def collect_user_data(self) -> List[Dict[str, Any]]:
        """收集用户使用数据"""
        user_logs = []
        logs_dir = Path(self.user_logs_path)
        
        for log_file in logs_dir.glob("*.json"):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        user_logs.extend(data)
                    else:
                        user_logs.append(data)
            except Exception:
                continue
        
        return user_logs
    
    def create_training_data(self, environment_info: Dict[str, Any], user_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """基于环境信息和用户数据创建训练数据"""
        training_data = []
        
        # 基于环境信息生成基础训练样本
        for tool_name, tool_info in environment_info.get("cli_tools", {}).items():
            if tool_info.get("available", False):
                # 为每个可用工具生成样本
                tool_samples = self._generate_tool_samples(tool_name, tool_info)
                training_data.extend(tool_samples)
        
        # 基于技能生成样本
        for skill_name, skill_info in environment_info.get("skills", {}).items():
            skill_samples = self._generate_skill_samples(skill_name, skill_info)
            training_data.extend(skill_samples)
        
        # 基于用户数据生成样本
        for user_entry in user_data:
            user_sample = self._generate_user_sample(user_entry)
            if user_sample:
                training_data.append(user_sample)
        
        # 转换为DataFrame
        if training_data:
            df = pd.DataFrame(training_data)
            # 确保必要的列存在
            for col in ['user_intent', 'cli_tool', 'skill_used', 'parameters', 'expected_output_format']:
                if col not in df.columns:
                    df[col] = ''
            return df
        else:
            # 如果没有数据，使用默认数据
            return self._create_default_training_data()
    
    def _generate_tool_samples(self, tool_name: str, tool_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """为CLI工具生成训练样本"""
        samples = []
        
        # 定义工具功能描述
        tool_functions = {
            "claude": ["code review", "programming help", "software engineering", "debug code", 
                      "write documentation", "explain code", "refactor code", "create test"],
            "qwen": ["code generation", "programming assistance", "algorithm design", 
                    "system design", "code optimization"],
            "gemini": ["research", "information lookup", "data analysis", "content creation", 
                      "summarization", "translation"],
            "codebuddy": ["code help", "programming tips", "debugging", "best practices", 
                         "code explanation"],
            "stigmergy": ["skill management", "agent coordination", "cross-cli workflow", 
                         "project coordination", "multi-agent collaboration"]
        }
        
        functions = tool_functions.get(tool_name, ["general task"])
        
        for func in functions:
            # 英文表达
            samples.append({
                "user_intent": f"Help me with {func} using {tool_name}",
                "cli_tool": tool_name,
                "skill_used": "",
                "parameters": " ".join(tool_info.get("parameters", [])),
                "expected_output_format": "text"
            })
            samples.append({
                "user_intent": f"I need {tool_name} to {func}",
                "cli_tool": tool_name,
                "skill_used": "",
                "parameters": " ".join(tool_info.get("parameters", [])),
                "expected_output_format": "text"
            })
            
            # 中文表达
            chinese_funcs = {
                "code review": ["代码审查", "代码检查", "代码审核"],
                "programming help": ["编程帮助", "编程指导", "编程支持"],
                "research": ["研究", "调研", "分析"],
                "content creation": ["内容创作", "内容生成", "创作内容"],
                "skill management": ["技能管理", "技能操作", "管理技能"]
            }
            
            chinese_func_list = chinese_funcs.get(func.split()[0], [func.split()[0]])
            for chinese_func in chinese_func_list:
                samples.append({
                    "user_intent": f"帮我{chinese_func}，使用{tool_name}",
                    "cli_tool": tool_name,
                    "skill_used": "",
                    "parameters": " ".join(tool_info.get("parameters", [])),
                    "expected_output_format": "text"
                })
        
        return samples
    
    def _generate_skill_samples(self, skill_name: str, skill_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """为技能生成训练样本"""
        samples = []
        
        # 根据技能描述生成样本
        description = skill_info.get("description", "").lower()
        
        # 定义技能类型和对应功能
        skill_actions = {
            "document": ["create document", "edit document", "format document", "write report"],
            "pdf": ["extract text", "merge PDFs", "split PDF", "fill form"],
            "xlsx": ["create spreadsheet", "analyze data", "create chart", "calculate formulas"],
            "design": ["create UI component", "design web page", "build interface"],
            "research": ["analyze data", "research analysis", "data interpretation"],
            "testing": ["test web app", "debug UI", "test functionality"]
        }
        
        # 根据描述匹配技能类型
        matched_actions = []
        for skill_type, actions in skill_actions.items():
            if skill_type in description:
                matched_actions.extend(actions)
        
        # 如果没有匹配到，使用通用动作
        if not matched_actions:
            matched_actions = ["use skill", "apply skill", "execute skill"]
        
        for action in matched_actions:
            # 英文表达
            samples.append({
                "user_intent": f"Use {skill_name} to {action}",
                "cli_tool": "stigmergy",
                "skill_used": skill_name,
                "parameters": f"skill {skill_name}",
                "expected_output_format": "text"
            })
            
            # 中文表达
            chinese_actions = {
                "create document": ["创建文档", "生成文档", "制作文档"],
                "analyze data": ["分析数据", "数据分析", "数据研究"],
                "use skill": ["使用技能", "应用技能", "执行技能"]
            }
            
            chinese_action_list = chinese_actions.get(action, [action])
            for chinese_action in chinese_action_list:
                samples.append({
                    "user_intent": f"用{skill_name}{chinese_action}",
                    "cli_tool": "stigmergy",
                    "skill_used": skill_name,
                    "parameters": f"skill {skill_name}",
                    "expected_output_format": "text"
                })
        
        return samples
    
    def _generate_user_sample(self, user_entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """基于用户数据生成样本"""
        if "user_intent" in user_entry and "cli_tool" in user_entry:
            return {
                "user_intent": user_entry["user_intent"],
                "cli_tool": user_entry["cli_tool"],
                "skill_used": user_entry.get("skill_used", ""),
                "parameters": user_entry.get("parameters", ""),
                "expected_output_format": user_entry.get("expected_output_format", "text")
            }
        return None
    
    def _create_default_training_data(self) -> pd.DataFrame:
        """创建默认训练数据"""
        default_data = []
        for i in range(10):  # 创建10个默认样本
            default_data.append({
                "user_intent": f"sample intent {i}",
                "cli_tool": "stigmergy",
                "skill_used": "",
                "parameters": "",
                "expected_output_format": "text"
            })
        return pd.DataFrame(default_data)
    
    def train_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """训练模型"""
        print(f"开始训练模型，使用 {len(df)} 个样本")
        
        # 准备特征
        X = df['user_intent']
        
        # 准备标签
        y_cli = df['cli_tool']
        y_skill = df.get('skill_used', pd.Series([''] * len(df)))
        y_params = df.get('parameters', pd.Series([''] * len(df)))
        
        # 向量化文本
        X_vectorized = self.vectorizer.fit_transform(X)
        
        # 分割训练/测试数据
        X_train, X_test, y_cli_train, y_cli_test = train_test_split(
            X_vectorized, y_cli, test_size=0.2, random_state=42
        )
        
        # 训练CLI工具分类器
        self.classifier.fit(X_train, np.column_stack([y_cli_train]))
        
        # 评估模型
        y_pred = self.classifier.predict(X_test)
        cli_pred = y_pred[:, 0] if y_pred.ndim > 1 else y_pred
        
        accuracy = accuracy_score(y_cli_test, cli_pred)
        print(f"模型准确率: {accuracy:.3f}")
        
        # 生成分类报告
        print("\n分类报告:")
        print(classification_report(y_cli_test, cli_pred))
        
        return {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'accuracy': accuracy,
            'feature_names': self.vectorizer.get_feature_names_out(),
            'training_size': len(df)
        }
    
    def save_model(self, model_data: Dict[str, Any], model_name: str = "adaptive_model"):
        """保存训练好的模型"""
        model_dir = Path(self.model_path)
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存模型组件
        joblib.dump(model_data['vectorizer'], f"{self.model_path}/{model_name}_vectorizer.pkl")
        joblib.dump(model_data['classifier'], f"{self.model_path}/{model_name}_classifier.pkl")
        
        # 保存模型元数据
        metadata = {
            'accuracy': model_data['accuracy'],
            'feature_count': len(model_data['feature_names']),
            'training_size': model_data['training_size'],
            'training_date': datetime.now().isoformat(),
            'model_version': 'adaptive-v1'
        }
        
        with open(f"{self.model_path}/{model_name}_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"模型已保存到: {self.model_path}/{model_name}")
        
        # 记录训练历史
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "model_name": model_name,
            "accuracy": metadata['accuracy'],
            "training_size": metadata['training_size'],
            "feature_count": metadata['feature_count']
        }
        
        history_file = Path(self.training_history_path) / f"{model_name}_history.json"
        history_data = []
        if history_file.exists():
            with open(history_file, 'r') as f:
                history_data = json.load(f)
        
        history_data.append(history_entry)
        
        with open(history_file, 'w') as f:
            json.dump(history_data, f, indent=2)
    
    def run_adaptive_training(self) -> Dict[str, Any]:
        """运行完整的自适应训练流程"""
        print("开始自适应训练流程...")
        
        # 1. 扫描环境
        print("1. 扫描本地环境...")
        environment_info = self.scan_environment()
        print(f"   扫描到 {len(environment_info['cli_tools'])} 个CLI工具和 {len(environment_info['skills'])} 个技能")
        
        # 2. 收集用户数据
        print("2. 收集用户使用数据...")
        user_data = self.collect_user_data()
        print(f"   收集到 {len(user_data)} 条用户数据")
        
        # 3. 创建训练数据
        print("3. 创建训练数据...")
        df = self.create_training_data(environment_info, user_data)
        print(f"   生成了 {len(df)} 个训练样本")
        
        # 4. 训练模型
        print("4. 训练模型...")
        model_data = self.train_model(df)
        
        # 5. 保存模型
        print("5. 保存模型...")
        model_name = f"adaptive_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.save_model(model_data, model_name)
        
        print("自适应训练完成！")
        
        return {
            "status": "success",
            "model_name": model_name,
            "accuracy": model_data['accuracy'],
            "training_size": len(df),
            "environment_info": environment_info,
            "user_data_count": len(user_data)
        }


def main():
    trainer = AdaptiveTrainer()
    result = trainer.run_adaptive_training()
    print(f"训练结果: {result}")


if __name__ == "__main__":
    main()