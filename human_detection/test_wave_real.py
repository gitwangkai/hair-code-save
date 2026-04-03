#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作真实环境测试
用于验证挥手动作和音频播放是否能正常工作
"""

import sys
import os
import subprocess
import time

sys.path.insert(0, 'src')


def test_wave_script():
    """测试挥手脚本"""
    print("=" * 60)
    print("测试1: 挥手脚本执行")
    print("=" * 60)
    
    script = "/home/aidlux/demo_arm/wave_hand_safe.py"
    if not os.path.exists(script):
        print(f"✗ 脚本不存在: {script}")
        return False
    
    print(f"脚本: {script}")
    print("执行中 (最多等待30秒)...")
    
    try:
        result = subprocess.run(
            ["timeout", "30", "python3", script],
            capture_output=True,
            text=True,
            timeout=35
        )
        
        print(f"返回码: {result.returncode}")
        
        if result.stdout:
            print("输出:")
            for line in result.stdout.strip().split('\n')[:20]:
                print(f"  {line}")
        
        if result.returncode == 0:
            print("✓ 挥手执行成功")
            return True
        elif result.returncode == 124:
            print("✗ 执行超时 (机械臂可能未连接)")
            return False
        else:
            print(f"✗ 执行失败 (返回码: {result.returncode})")
            if result.stderr:
                print(f"错误: {result.stderr[:200]}")
            return False
            
    except Exception as e:
        print(f"✗ 执行异常: {e}")
        return False


def test_audio():
    """测试音频播放"""
    print("\n" + "=" * 60)
    print("测试2: 音频播放")
    print("=" * 60)
    
    audio_file = "/home/aidlux/auto.mp3"
    if not os.path.exists(audio_file):
        print(f"✗ 音频文件不存在: {audio_file}")
        return False
    
    print(f"音频文件: {audio_file}")
    
    # 检测播放器
    players = ["ffplay", "mpg123"]
    player = None
    for p in players:
        try:
            subprocess.run(["which", p], check=True, stdout=subprocess.DEVNULL)
            player = p
            break
        except:
            pass
    
    if not player:
        print("✗ 未找到音频播放器")
        return False
    
    print(f"播放器: {player}")
    print("播放中 (最多等待10秒)...")
    
    try:
        if player == "ffplay":
            result = subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", audio_file],
                capture_output=True,
                timeout=10
            )
        else:  # mpg123
            result = subprocess.run(
                ["timeout", "8", "mpg123", "-q", audio_file],
                capture_output=True,
                timeout=10
            )
        
        print(f"返回码: {result.returncode}")
        
        if result.returncode == 0:
            print("✓ 音频播放成功")
            return True
        elif result.returncode == 124:
            print("✗ 播放超时 (音频设备可能不可用)")
            return False
        else:
            print(f"✗ 播放失败 (返回码: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 播放超时")
        return False
    except Exception as e:
        print(f"✗ 播放异常: {e}")
        return False


def test_controller():
    """测试控制器"""
    print("\n" + "=" * 60)
    print("测试3: 控制器集成")
    print("=" * 60)
    
    from wave_action import WaveActionController
    
    print("创建控制器...")
    controller = WaveActionController(min_interval=5)
    
    print(f"音频播放器: {controller.audio_player or '未检测到'}")
    print(f"触发间隔: {controller.get_interval()}秒")
    
    print("\n触发挥手...")
    start_time = time.time()
    
    controller.trigger()
    
    # 等待完成
    while controller.is_running:
        time.sleep(0.5)
    
    elapsed = time.time() - start_time
    
    print(f"\n执行完成，耗时: {elapsed:.1f}秒")
    print(f"统计: {controller.get_stats()}")
    
    return True


def main():
    print("=" * 60)
    print("挥手动作真实环境测试")
    print("=" * 60)
    
    # 测试1: 挥手脚本
    wave_ok = test_wave_script()
    
    # 测试2: 音频播放
    audio_ok = test_audio()
    
    # 测试3: 控制器
    ctrl_ok = test_controller()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果:")
    print(f"  挥手动作: {'✓ 通过' if wave_ok else '✗ 失败'}")
    print(f"  音频播放: {'✓ 通过' if audio_ok else '✗ 失败'}")
    print(f"  控制器: {'✓ 通过' if ctrl_ok else '✗ 失败'}")
    print("=" * 60)
    
    if not wave_ok:
        print("\n挥手脚本失败的可能原因:")
        print("  1. 机械臂电源未开启")
        print("  2. 网络连接问题 (192.168.3.100)")
        print("  3. PallasSDK 未正确安装")
    
    if not audio_ok:
        print("\n音频播放失败的可能原因:")
        print("  1. 音频设备不可用 (在服务器环境中常见)")
        print("  2. 音频播放器未安装")
        print("  3. 音频文件损坏")


if __name__ == "__main__":
    main()
