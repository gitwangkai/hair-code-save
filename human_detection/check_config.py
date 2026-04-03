#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置检查脚本
验证挥手动作联动所需文件和环境
"""

import os
import sys

def check_file(path, name):
    """检查文件是否存在"""
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"  ✓ {name}: {path} ({size} bytes)")
        return True
    else:
        print(f"  ✗ {name}: {path} (不存在)")
        return False

def check_command(cmd):
    """检查命令是否可用"""
    import subprocess
    try:
        subprocess.run(['which', cmd], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  ✓ {cmd}: 已安装")
        return True
    except:
        print(f"  ✗ {cmd}: 未安装")
        return False

def main():
    print("=" * 60)
    print("智能迎宾机器人 - 配置检查")
    print("=" * 60)
    
    all_ok = True
    
    # 1. 检查挥手脚本
    print("\n[1] 挥手脚本检查:")
    scripts = [
        ("/home/aidlux/demo_arm/wave_hand.py", "原始脚本"),
        ("/home/aidlux/demo_arm/wave_hand_safe.py", "安全版本脚本"),
    ]
    for path, name in scripts:
        if check_file(path, name):
            all_ok = True
    
    # 2. 检查音频文件
    print("\n[2] 音频文件检查:")
    if not check_file("/home/aidlux/auto.mp3", "音频文件"):
        all_ok = False
    
    # 3. 检查音频播放器
    print("\n[3] 音频播放器检查:")
    players = ['mpg123', 'ffplay', 'aplay']
    found_player = False
    for player in players:
        if check_command(player):
            found_player = True
    
    if not found_player:
        print("  ! 警告: 未找到任何音频播放器")
        print("  请安装: sudo apt-get install mpg123")
        all_ok = False
    
    # 4. 检查 Python 模块
    print("\n[4] Python 模块检查:")
    try:
        sys.path.insert(0, 'src')
        from wave_action import WaveActionController
        print("  ✓ wave_action 模块: 可导入")
    except Exception as e:
        print(f"  ✗ wave_action 模块: {e}")
        all_ok = False
    
    # 5. 检查 PallasSDK (可选)
    print("\n[5] PallasSDK 检查 (机械臂控制):")
    try:
        from PallasSDK import Controller
        print("  ✓ PallasSDK: 已安装")
    except ImportError:
        print("  ! PallasSDK: 未安装 (仅在连接真实机械臂时需要)")
    
    # 6. 网络检查
    print("\n[6] 网络检查:")
    import subprocess
    result = subprocess.run(['ping', '-c', '1', '-W', '2', '192.168.3.100'], 
                          capture_output=True)
    if result.returncode == 0:
        print("  ✓ 机械臂控制器 (192.168.3.100): 可连接")
    else:
        print("  ! 机械臂控制器 (192.168.3.100): 无法连接")
        print("    请检查:")
        print("    - 机械臂电源是否开启")
        print("    - 网络连接是否正常")
    
    # 总结
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ 基础配置检查通过")
        print("\n可以启动系统:")
        print("  python3 web_gui.py")
    else:
        print("✗ 部分检查未通过")
        print("\n请修复上述问题后再启动")
    print("=" * 60)

if __name__ == "__main__":
    main()
