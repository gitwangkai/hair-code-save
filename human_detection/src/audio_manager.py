#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频管理模块

功能:
- 扫描音频文件
- 管理音频列表
- 提供音频文件访问
"""

import os
import glob
from typing import List, Dict
from pathlib import Path


class AudioManager:
    """
    音频管理器
    
    管理音频文件列表，支持扫描和获取
    """
    
    DEFAULT_MUSIC_DIR = "/home/aidlux/human_detection/config/music"
    
    def __init__(self, music_dir: str = None):
        """
        初始化音频管理器
        
        Args:
            music_dir: 音乐文件目录，默认使用 config/music
        """
        self.music_dir = music_dir or self.DEFAULT_MUSIC_DIR
        self.audio_files: List[Dict] = []
        self.default_audio = "auto.mp3"
        
        # 确保目录存在
        os.makedirs(self.music_dir, exist_ok=True)
        
        # 扫描音频文件
        self.scan_audio_files()
    
    def scan_audio_files(self) -> List[Dict]:
        """
        扫描音频文件
        
        Returns:
            音频文件列表
        """
        self.audio_files = []
        
        # 支持的音频格式
        extensions = ['*.mp3', '*.wav', '*.ogg', '*.aac']
        
        for ext in extensions:
            pattern = os.path.join(self.music_dir, ext)
            for filepath in glob.glob(pattern):
                filename = os.path.basename(filepath)
                self.audio_files.append({
                    'name': filename,
                    'path': filepath,
                    'size': os.path.getsize(filepath),
                    'url': f'/music/{filename}'  # HTTP访问路径
                })
        
        # 按文件名排序
        self.audio_files.sort(key=lambda x: x['name'])
        
        return self.audio_files
    
    def get_audio_list(self) -> List[Dict]:
        """
        获取音频列表
        
        Returns:
            音频文件列表
        """
        return self.audio_files
    
    def get_default_audio(self) -> Dict:
        """
        获取默认音频
        
        Returns:
            默认音频信息
        """
        for audio in self.audio_files:
            if audio['name'] == self.default_audio:
                return audio
        
        # 如果没有默认音频，返回第一个
        if self.audio_files:
            return self.audio_files[0]
        
        return None
    
    def get_audio_by_name(self, name: str) -> Dict:
        """
        根据名称获取音频
        
        Args:
            name: 音频文件名
            
        Returns:
            音频信息
        """
        for audio in self.audio_files:
            if audio['name'] == name:
                return audio
        return None
    
    def get_audio_path(self, name: str) -> str:
        """
        获取音频文件的完整路径
        
        Args:
            name: 音频文件名
            
        Returns:
            完整路径
        """
        return os.path.join(self.music_dir, name)
    
    def reload(self):
        """重新扫描音频文件"""
        self.scan_audio_files()


# 单例实例
_audio_manager = None


def get_audio_manager() -> AudioManager:
    """获取音频管理器单例"""
    global _audio_manager
    if _audio_manager is None:
        _audio_manager = AudioManager()
    return _audio_manager


if __name__ == "__main__":
    # 测试
    manager = AudioManager()
    
    print("音频文件列表:")
    for audio in manager.get_audio_list():
        print(f"  - {audio['name']} ({audio['size']} bytes)")
    
    print(f"\n默认音频: {manager.get_default_audio()}")
