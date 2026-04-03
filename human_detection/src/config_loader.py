#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载模块

支持从 JSON 配置文件加载配置，并提供默认值和验证
"""

import json
import os
from typing import Any, Dict, Optional
from pathlib import Path


class ConfigLoader:
    """
    配置加载器
    
    功能:
    - 从 JSON 文件加载配置
    - 提供默认值
    - 配置验证
    - 运行时动态修改
    """
    
    # 默认配置
    DEFAULT_CONFIG = {
        "system": {
            "name": "智能迎宾机器人",
            "version": "1.0.0",
            "debug": False
        },
        "camera": {
            "source": "/dev/video_header",
            "width": 640,
            "height": 360,
            "fps": 30
        },
        "detection": {
            "yolo_model": "yolov8n.pt",
            "confidence_threshold": 0.5,
            "welcome_distance": 2.0,
            "detect_interval": 3
        },
        "face_recognition": {
            "enabled": True,
            "face_db_path": "data/face_database.pkl",
            "recognition_threshold": 0.6,
            "min_greet_interval": 10
        },
        "ptz": {
            "enabled": True,
            "smooth_factor": 0.3,
            "dead_zone": 0.1,
            "pan_range": [-45, 45],
            "tilt_range": [-30, 30]
        },
        "wave_action": {
            "enabled": True,
            "mode": "mock",  # mock, standalone, disabled
            "interval": 60,
            "script": "/home/aidlux/demo_arm/wave_hand_standalone.py",
            "audio_file": "/home/aidlux/auto.mp3",
            "trigger_conditions": {
                "on_new_visitor": True,
                "on_known_visitor": False,
                "min_distance": 0.5,
                "max_distance": 2.0
            }
        },
        "arm": {
            "enabled": False,
            "ip": "192.168.3.100",
            "mode": "mock"
        },
        "web_gui": {
            "host": "0.0.0.0",
            "port": 5000,
            "jpeg_quality": 60,
            "max_stream_fps": 15
        },
        "logging": {
            "level": "INFO",
            "file": "logs/robot.log",
            "max_size": 10485760,
            "backup_count": 5
        }
    }
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化配置加载器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load()
    
    def _load(self):
        """加载配置"""
        # 从默认配置开始
        self._config = self._deep_copy(self.DEFAULT_CONFIG)
        
        # 如果配置文件存在，合并配置
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                self._merge_config(self._config, user_config)
                print(f"[Config] 已加载配置文件: {self.config_path}")
            except Exception as e:
                print(f"[Config] 加载配置文件失败: {e}，使用默认配置")
        else:
            print(f"[Config] 配置文件不存在: {self.config_path}，使用默认配置")
            # 创建默认配置文件
            self.save()
    
    def _deep_copy(self, obj: Any) -> Any:
        """深拷贝对象"""
        import copy
        return copy.deepcopy(obj)
    
    def _merge_config(self, base: Dict, override: Dict):
        """递归合并配置"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置键，支持点号分隔 (如 "camera.width")
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        设置配置项
        
        Args:
            key: 配置键，支持点号分隔
            value: 配置值
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """保存配置到文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_path) if os.path.dirname(self.config_path) else '.', exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            
            print(f"[Config] 配置已保存: {self.config_path}")
            return True
        except Exception as e:
            print(f"[Config] 保存配置失败: {e}")
            return False
    
    def reload(self):
        """重新加载配置"""
        self._load()
        print("[Config] 配置已重新加载")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self._deep_copy(self._config)
    
    def validate(self) -> list:
        """
        验证配置
        
        Returns:
            错误列表，为空表示验证通过
        """
        errors = []
        
        # 验证摄像头
        camera_source = self.get("camera.source")
        if camera_source and not os.path.exists(str(camera_source)):
            if not str(camera_source).isdigit():  # 不是数字索引
                errors.append(f"摄像头设备不存在: {camera_source}")
        
        # 验证 YOLO 模型
        yolo_model = self.get("detection.yolo_model")
        if yolo_model and not os.path.exists(yolo_model):
            errors.append(f"YOLO 模型不存在: {yolo_model} (将自动下载)")
        
        # 验证挥手脚本
        if self.get("wave_action.enabled"):
            script = self.get("wave_action.script")
            if script and not os.path.exists(script):
                errors.append(f"挥手脚本不存在: {script}")
            
            audio_file = self.get("wave_action.audio_file")
            if audio_file and not os.path.exists(audio_file):
                errors.append(f"音频文件不存在: {audio_file}")
        
        # 验证目录
        face_db_dir = os.path.dirname(self.get("face_recognition.face_db_path", ""))
        if face_db_dir and not os.path.exists(face_db_dir):
            try:
                os.makedirs(face_db_dir, exist_ok=True)
            except Exception as e:
                errors.append(f"无法创建人脸数据库目录: {e}")
        
        log_dir = os.path.dirname(self.get("logging.file", ""))
        if log_dir and not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir, exist_ok=True)
            except Exception as e:
                errors.append(f"无法创建日志目录: {e}")
        
        return errors
    
    def print_config(self):
        """打印当前配置"""
        print("=" * 60)
        print("当前配置")
        print("=" * 60)
        print(json.dumps(self._config, indent=2, ensure_ascii=False))
        print("=" * 60)


# 全局配置实例
_config_instance: Optional[ConfigLoader] = None


def get_config(config_path: str = "config.json") -> ConfigLoader:
    """
    获取全局配置实例
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        ConfigLoader 实例
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader(config_path)
    return _config_instance


def reload_config():
    """重新加载全局配置"""
    global _config_instance
    if _config_instance:
        _config_instance.reload()


if __name__ == "__main__":
    # 测试
    config = ConfigLoader()
    
    print("\n配置测试:")
    print(f"摄像头: {config.get('camera.source')}")
    print(f"分辨率: {config.get('camera.width')}x{config.get('camera.height')}")
    print(f"挥手间隔: {config.get('wave_action.interval')}秒")
    
    # 验证
    errors = config.validate()
    if errors:
        print("\n配置问题:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n配置验证通过!")
    
    # 打印完整配置
    config.print_config()
