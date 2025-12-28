# 模型管理模块

import joblib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import os


class ModelManager:
    """管理模型的加载、保存和版本控制"""
    
    def __init__(self, model_path: str = "cli-intent-matcher/data/models"):
        self.model_path = Path(model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        # 默认模型名称
        self.current_model_name = "intent_classifier"
        self.model_metadata_file = self.model_path / f"{self.current_model_name}_metadata.json"
    
    def load_model(self, model_name: str = None) -> Optional[Dict[str, Any]]:
        """加载模型"""
        if model_name is None:
            model_name = self.current_model_name
        
        try:
            vectorizer_path = self.model_path / f"{model_name}_vectorizer.pkl"
            classifier_path = self.model_path / f"{model_name}_classifier.pkl"
            metadata_path = self.model_path / f"{model_name}_metadata.json"
            
            if not all(Path(p).exists() for p in [vectorizer_path, classifier_path]):
                print(f"模型文件不存在: {model_name}")
                return None
            
            # 加载模型组件
            vectorizer = joblib.load(vectorizer_path)
            classifier = joblib.load(classifier_path)
            
            # 加载元数据
            metadata = {}
            if metadata_path.exists():
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            
            model_data = {
                'vectorizer': vectorizer,
                'classifier': classifier,
                'metadata': metadata,
                'model_name': model_name
            }
            
            print(f"模型 {model_name} 加载成功")
            return model_data
            
        except Exception as e:
            print(f"加载模型失败: {e}")
            return None
    
    def save_model(self, model_data: Dict[str, Any], model_name: str = None) -> bool:
        """保存模型"""
        if model_name is None:
            model_name = self.current_model_name
        
        try:
            # 保存模型组件
            joblib.dump(model_data['vectorizer'], self.model_path / f"{model_name}_vectorizer.pkl")
            joblib.dump(model_data['classifier'], self.model_path / f"{model_name}_classifier.pkl")
            
            # 保存元数据
            metadata = model_data.get('metadata', {})
            metadata['save_time'] = datetime.now().isoformat()
            metadata['model_name'] = model_name
            
            with open(self.model_path / f"{model_name}_metadata.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"模型 {model_name} 保存成功")
            return True
            
        except Exception as e:
            print(f"保存模型失败: {e}")
            return False
    
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """获取所有可用模型"""
        models = {}
        
        for model_file in self.model_path.glob("*_vectorizer.pkl"):
            model_name = model_file.name.replace("_vectorizer.pkl", "")
            metadata_file = self.model_path / f"{model_name}_metadata.json"
            
            metadata = {}
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    try:
                        metadata = json.load(f)
                    except json.JSONDecodeError:
                        metadata = {}
            
            models[model_name] = metadata
        
        return models
    
    def get_current_model_info(self) -> Dict[str, Any]:
        """获取当前模型信息"""
        model_data = self.load_model()
        if model_data:
            return {
                "current_model": self.current_model_name,
                "loaded": True,
                "metadata": model_data['metadata']
            }
        else:
            return {
                "current_model": self.current_model_name,
                "loaded": False,
                "metadata": {}
            }
    
    def switch_model(self, model_name: str) -> bool:
        """切换到指定模型"""
        available_models = self.get_available_models()
        if model_name in available_models:
            self.current_model_name = model_name
            print(f"已切换到模型: {model_name}")
            return True
        else:
            print(f"模型不存在: {model_name}")
            return False
    
    def delete_model(self, model_name: str) -> bool:
        """删除模型"""
        if model_name == self.current_model_name:
            print("不能删除当前使用的模型")
            return False
        
        try:
            files_to_delete = [
                self.model_path / f"{model_name}_vectorizer.pkl",
                self.model_path / f"{model_name}_classifier.pkl",
                self.model_path / f"{model_name}_metadata.json"
            ]
            
            for file_path in files_to_delete:
                if file_path.exists():
                    file_path.unlink()
            
            print(f"模型 {model_name} 删除成功")
            return True
            
        except Exception as e:
            print(f"删除模型失败: {e}")
            return False
    
    def backup_current_model(self, backup_name: str = None) -> bool:
        """备份当前模型"""
        if backup_name is None:
            backup_name = f"{self.current_model_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 加载当前模型
        current_model = self.load_model()
        if not current_model:
            print("当前模型未加载，无法备份")
            return False
        
        # 保存为备份模型
        return self.save_model(current_model, backup_name)
    
    def restore_model(self, backup_name: str) -> bool:
        """从备份恢复模型"""
        return self.switch_model(backup_name)


def main():
    manager = ModelManager()
    
    # 获取可用模型
    available_models = manager.get_available_models()
    print("可用模型:", list(available_models.keys()))
    
    # 获取当前模型信息
    current_info = manager.get_current_model_info()
    print("当前模型信息:", current_info)


if __name__ == "__main__":
    main()