#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频播放脚本

功能: 播放音频文件，支持多种方式
用法: python3 play_audio.py [音频文件路径]

示例:
    python3 play_audio.py                    # 播放默认音频
    python3 play_audio.py /path/to/audio.mp3 # 播放指定音频
"""

import sys
import os
import subprocess
import time


def detect_audio_player():
    """检测可用的音频播放器"""
    players = [
        ("ffplay", ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]),
        ("mpg123", ["mpg123", "-q"]),
        ("aplay", None),  # 需要特殊处理
    ]
    
    for name, cmd in players:
        try:
            subprocess.run(["which", name], check=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return name, cmd
        except:
            continue
    
    return None, None


def play_audio(audio_file: str, timeout: int = 10) -> bool:
    """
    播放音频文件
    
    Args:
        audio_file: 音频文件路径
        timeout: 超时时间(秒)
        
    Returns:
        是否成功播放
    """
    # 检查文件是否存在
    if not os.path.exists(audio_file):
        print(f"[错误] 音频文件不存在: {audio_file}")
        return False
    
    # 获取音频时长
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
             "-of", "csv=p=0", audio_file],
            capture_output=True,
            text=True,
            timeout=2
        )
        duration = float(result.stdout.strip()) if result.returncode == 0 else 5.0
    except:
        duration = 5.0
    
    # 检测播放器
    player_name, player_cmd = detect_audio_player()
    
    if not player_name:
        print("[错误] 未找到音频播放器")
        print("请安装: sudo apt-get install ffmpeg 或 mpg123")
        return False
    
    print(f"[播放] 使用 {player_name} 播放: {os.path.basename(audio_file)} (时长: {duration:.1f}秒)")
    
    try:
        if player_name == "ffplay":
            # 使用 timeout 限制播放时间，避免挂起
            # ffplay 在 headless 环境可能有问题，使用 ffmpeg 直接输出到 null
            play_timeout = min(int(duration) + 2, timeout)
            result = subprocess.run(
                ["timeout", str(play_timeout), "ffplay", "-nodisp", "-autoexit", 
                 "-loglevel", "error", audio_file],
                capture_output=True,
                timeout=play_timeout + 2
            )
            # timeout 命令返回 124 表示正常超时(播放完成)
            success = result.returncode == 0 or result.returncode == 124
            
        elif player_name == "mpg123":
            # mpg123 通常更稳定
            play_timeout = min(int(duration) + 2, timeout)
            result = subprocess.run(
                ["timeout", str(play_timeout), "mpg123", "-q", audio_file],
                capture_output=True,
                timeout=play_timeout + 2
            )
            success = result.returncode == 0 or result.returncode == 124
            
        elif player_name == "aplay":
            # aplay 需要转换格式
            print("[转换] 正在转换为WAV格式...")
            temp_wav = "/tmp/temp_audio.wav"
            convert_result = subprocess.run(
                ["ffmpeg", "-y", "-i", audio_file, "-ar", "44100", "-ac", "2", temp_wav],
                capture_output=True,
                timeout=10
            )
            
            if convert_result.returncode == 0:
                play_timeout = min(int(duration) + 2, timeout)
                result = subprocess.run(
                    ["timeout", str(play_timeout), "aplay", "-q", temp_wav],
                    capture_output=True,
                    timeout=play_timeout + 2
                )
                success = result.returncode == 0 or result.returncode == 124
                # 清理临时文件
                try:
                    os.remove(temp_wav)
                except:
                    pass
            else:
                print("[错误] 音频格式转换失败")
                success = False
        
        else:
            print(f"[错误] 不支持的播放器: {player_name}")
            return False
        
        if success:
            print("[播放] 播放完成")
        else:
            print(f"[警告] 播放异常 (返回码: {result.returncode})")
            # 即使返回码异常，也可能已经播放了一部分
            success = True
        
        return success
        
    except subprocess.TimeoutExpired:
        print("[警告] 播放超时，但可能已部分播放")
        return True  # 超时也算部分成功
    except Exception as e:
        print(f"[错误] 播放异常: {e}")
        return False


def test_loop():
    """循环播放测试"""
    audio_file = "/home/aidlux/auto.mp3"
    
    print("="*60)
    print("音频播放循环测试")
    print("="*60)
    print(f"音频文件: {audio_file}")
    print("按 Ctrl+C 停止\n")
    
    count = 0
    try:
        while True:
            count += 1
            print(f"\n--- 播放 #{count} ---")
            play_audio(audio_file)
            print("等待3秒...")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n\n停止测试")


def main():
    # 获取音频文件路径
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        audio_file = "/home/aidlux/auto.mp3"
    
    print("="*60)
    print("音频播放工具")
    print("="*60)
    print(f"音频文件: {audio_file}")
    
    # 检测播放器
    player_name, _ = detect_audio_player()
    if player_name:
        print(f"播放器: {player_name}")
    else:
        print("播放器: 未找到")
    
    print("-"*60)
    
    # 播放音频
    success = play_audio(audio_file)
    
    # 返回结果
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
