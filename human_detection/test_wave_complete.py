#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作完整测试

测试三种模式:
1. 模拟模式 (无需机械臂)
2. 独立脚本模式 (通过子进程)
3. 直接调用模式 (模块导入)
"""

import sys
import time
sys.path.insert(0, 'src')


def test_mock_mode():
    """测试模拟模式"""
    print("=" * 60)
    print("测试1: 模拟模式")
    print("=" * 60)
    
    from wave_action import MockWaveActionController
    
    controller = MockWaveActionController(min_interval=3)
    
    print("\n触发挥手...")
    controller.trigger()
    
    while controller.is_running:
        time.sleep(0.5)
        print("  .", end="", flush=True)
    
    print("\n完成!")
    stats = controller.get_stats()
    print(f"统计: 触发{stats['trigger_count']}次")
    return True


def test_script_mode():
    """测试独立脚本模式"""
    print("\n" + "=" * 60)
    print("测试2: 独立脚本模式 (通过子进程)")
    print("=" * 60)
    
    import subprocess
    import os
    
    script = "/home/aidlux/human_detection/src/wave_hand_safe.py"
    
    if not os.path.exists(script):
        print(f"✗ 脚本不存在: {script}")
        return False
    
    print(f"执行脚本: {script}")
    print("注意: 这会尝试连接真实机械臂，如果机械臂未连接会超时\n")
    
    try:
        # 使用 timeout 命令，最多等待15秒
        result = subprocess.run(
            ["timeout", "15", "python3", script],
            capture_output=True,
            text=True,
            timeout=20
        )
        
        print("输出:")
        for line in result.stdout.strip().split('\n')[-10:]:
            print(f"  {line}")
        
        if result.returncode == 0:
            print("\n✓ 脚本执行成功")
            return True
        elif result.returncode == 124:
            print("\n! 脚本执行超时 (机械臂可能未连接)")
            return False
        else:
            print(f"\n✗ 脚本执行失败 (返回码: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"\n✗ 执行异常: {e}")
        return False


def test_module_mode():
    """测试直接模块调用"""
    print("\n" + "=" * 60)
    print("测试3: 直接模块调用 (在当前进程)")
    print("=" * 60)
    
    try:
        from wave_hand_safe import WaveHandController
        
        print("创建控制器...")
        controller = WaveHandController(timeout=5)
        
        print("连接机械臂 (5秒超时)...")
        if controller.connect():
            print("✓ 连接成功")
            
            print("\n执行挥手动作...")
            if controller.wave_hand(times=2, go_home_after=True):
                print("✓ 挥手完成")
                controller.disconnect()
                return True
            else:
                print("✗ 挥手失败")
                controller.disconnect()
                return False
        else:
            print("✗ 连接失败 (机械臂可能未开启)")
            return False
            
    except Exception as e:
        print(f"✗ 异常: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("挥手动作完整测试")
    print("=" * 60)
    print()
    print("请选择测试模式:")
    print("  1) 模拟模式 (安全，推荐)")
    print("  2) 独立脚本模式 (测试子进程执行)")
    print("  3) 直接模块调用 (可能受 Flask 影响)")
    print("  4) 全部测试")
    print("  5) 退出")
    print()
    
    try:
        choice = input("选择 [1-5]: ").strip()
    except KeyboardInterrupt:
        print("\n退出")
        return
    
    if choice == "1":
        test_mock_mode()
    elif choice == "2":
        test_script_mode()
    elif choice == "3":
        test_module_mode()
    elif choice == "4":
        test_mock_mode()
        test_script_mode()
        print("\n跳过直接模块调用测试 (避免与当前环境冲突)")
    else:
        print("退出")
        return
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
