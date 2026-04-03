#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手功能诊断工具

检查为什么检测到人无法触发挥手
"""

import sys
import os
sys.path.insert(0, 'src')


def check_files():
    """检查必要文件是否存在"""
    print("="*60)
    print("1. 检查必要文件")
    print("="*60)
    
    files = {
        "挥手脚本": "/home/aidlux/human_detection/src/wave_hand_standalone.py",
        "基础模块": "/home/aidlux/human_detection/src/wave_hand_safe.py",
        "控制器": "/home/aidlux/human_detection/src/wave_action_simple.py",
        "音频文件": "/home/aidlux/auto.mp3",
    }
    
    all_ok = True
    for name, path in files.items():
        exists = os.path.exists(path)
        status = "✓" if exists else "✗"
        print(f"  {status} {name}: {path}")
        if not exists:
            all_ok = False
    
    return all_ok


def check_wave_standalone():
    """测试独立脚本"""
    print("\n" + "="*60)
    print("2. 测试独立挥手脚本")
    print("="*60)
    print("说明: 这会直接调用挥手脚本，测试机械臂连接\n")
    
    import subprocess
    
    script = "/home/aidlux/human_detection/src/wave_hand_standalone.py"
    
    print("执行: python3 src/wave_hand_standalone.py")
    print("等待10秒...")
    print("-"*60)
    
    result = subprocess.run(
        ["timeout", "10", "python3", script],
        capture_output=True,
        text=True
    )
    
    # 输出最后10行
    if result.stdout:
        lines = result.stdout.strip().split('\n')
        for line in lines[-10:]:
            print(f"  {line}")
    
    print("-"*60)
    print(f"返回码: {result.returncode}")
    
    if result.returncode == 0:
        print("✓ 独立脚本执行成功")
        return True
    elif result.returncode == 124:
        print("! 超时 (机械臂可能未连接)")
        return False
    else:
        print("✗ 执行失败")
        return False


def test_controller():
    """测试控制器"""
    print("\n" + "="*60)
    print("3. 测试挥手控制器")
    print("="*60)
    
    from wave_action_simple import SimpleWaveActionController
    
    print("创建控制器...")
    ctrl = SimpleWaveActionSimpleController(min_interval=3)
    
    print(f"  触发间隔: {ctrl.get_interval()}秒")
    print(f"  是否可以触发: {ctrl.can_trigger()}")
    print(f"  音频播放器: {ctrl.audio_player or '未检测到'}")
    
    # 测试触发
    print("\n测试触发...")
    result = ctrl.trigger()
    print(f"  触发结果: {'成功' if result else '失败'}")
    
    if result:
        import time
        print("等待3秒...")
        time.sleep(3)
        print(f"  是否正在运行: {ctrl.is_running}")
        print(f"  统计: {ctrl.get_stats()}")
    
    return result


def check_webgui_config():
    """检查 Web GUI 配置"""
    print("\n" + "="*60)
    print("4. 检查 Web GUI 配置")
    print("="*60)
    
    # 读取 web_gui.py 中的配置
    import re
    
    with open("web_gui.py", "r") as f:
        content = f.read()
    
    # 查找配置
    patterns = {
        "enable_wave_action": r'"enable_wave_action":\s*(\w+)',
        "wave_interval": r'"wave_interval":\s*(\d+)',
        "welcome_distance": r'"welcome_distance":\s*([\d.]+)',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            print(f"  {key}: {match.group(1)}")
        else:
            print(f"  {key}: 未找到")


def simulate_detection():
    """模拟检测流程"""
    print("\n" + "="*60)
    print("5. 模拟检测触发流程")
    print("="*60)
    
    from wave_action_simple import SimpleWaveActionController
    
    ctrl = SimpleWaveActionController(min_interval=3)
    
    print("\n模拟检测到人:")
    print("  距离: 1.5m")
    print("  迎宾距离: 2.0m")
    print(f"  是否可以触发: {ctrl.can_trigger()}")
    
    # 触发
    if ctrl.can_trigger():
        print("\n>> 正在触发...")
        ctrl.trigger()
        
        import time
        count = 0
        while ctrl.is_running and count < 10:
            time.sleep(1)
            count += 1
            print(f"  执行中... ({count}s)")
        
        print(f"\n执行完成!")
        print(f"统计: {ctrl.get_stats()}")
    else:
        print("  无法触发 (冷却中或已在运行)")


def main():
    print("="*60)
    print("挥手功能诊断工具")
    print("="*60)
    print()
    print("此工具将检查:")
    print("  1. 必要文件是否存在")
    print("  2. 独立脚本是否可以执行")
    print("  3. 控制器是否正常工作")
    print("  4. Web GUI 配置是否正确")
    print("  5. 模拟检测触发流程")
    print()
    
    try:
        input("按回车开始诊断，或按 Ctrl+C 退出...")
    except KeyboardInterrupt:
        print("\n退出")
        return
    
    # 执行检查
    check_files()
    check_wave_standalone()
    check_webgui_config()
    
    try:
        test_controller()
    except Exception as e:
        print(f"控制器测试出错: {e}")
    
    try:
        simulate_detection()
    except Exception as e:
        print(f"模拟检测出错: {e}")
    
    print("\n" + "="*60)
    print("诊断完成")
    print("="*60)
    print()
    print("常见问题:")
    print("  1. 如果独立脚本测试失败，检查机械臂电源和网络")
    print("  2. 如果控制器测试失败，检查Python模块导入")
    print("  3. 如果模拟检测失败，检查触发间隔配置")
    print()


if __name__ == "__main__":
    main()
