#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试网页端音频播放功能

验证:
1. 音频文件列表获取
2. 音频文件 HTTP 访问
3. 播放命令发送
"""

import sys
import os
sys.path.insert(0, 'src')

from audio_manager import AudioManager


def test_audio_manager():
    """测试音频管理器"""
    print("="*60)
    print("测试音频管理器")
    print("="*60)
    
    manager = AudioManager()
    
    print("\n音频文件列表:")
    audio_list = manager.get_audio_list()
    for audio in audio_list:
        print(f"  - {audio['name']}")
        print(f"    URL: {audio['url']}")
        print(f"    大小: {audio['size']} bytes")
    
    print(f"\n默认音频: {manager.get_default_audio()}")
    
    return len(audio_list) > 0


def test_http_access():
    """测试 HTTP 访问音频文件"""
    print("\n" + "="*60)
    print("测试 HTTP 访问")
    print("="*60)
    
    import subprocess
    
    # 测试获取音频列表 API
    print("\n测试 /api/audio/list:")
    result = subprocess.run(
        ["curl", "-s", "http://localhost:5000/api/audio/list"],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(result.stdout[:500] if result.stdout else "无响应")
    
    # 测试音频文件访问
    print("\n测试 /music/auto.mp3:")
    result = subprocess.run(
        ["curl", "-s", "-I", "http://localhost:5000/music/auto.mp3"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if "200 OK" in result.stdout or "Content-Type" in result.stdout:
        print("✓ 音频文件可访问")
    else:
        print("✗ 音频文件访问失败")
        print(result.stdout[:200])


def main():
    print("="*60)
    print("网页端音频播放测试")
    print("="*60)
    
    # 测试音频管理器
    if test_audio_manager():
        print("\n✓ 音频管理器工作正常")
    else:
        print("\n✗ 没有找到音频文件")
        print(f"请检查目录: /home/aidlux/human_detection/config/music/")
    
    # 提示启动 Web GUI 后再测试 HTTP 访问
    print("\n" + "="*60)
    print("提示")
    print("="*60)
    print("请先启动 Web GUI: python3 web_gui.py")
    print("然后在浏览器中访问测试")
    print("")
    print("功能说明:")
    print("  1. 网页会显示音频下拉列表")
    print("  2. 检测到人时自动播放选中的音频")
    print("  3. 音频通过 HTML5 Audio 在浏览器端播放")


if __name__ == "__main__":
    main()
