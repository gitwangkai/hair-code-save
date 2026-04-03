#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本

测试挥手动作从检测到执行的完整流程
"""

import sys
import time
sys.path.insert(0, 'src')


def test_standalone():
    """测试独立脚本"""
    print("="*60)
    print("测试1: 独立脚本执行")
    print("="*60)
    print("说明: 直接执行挥手脚本，验证机械臂连接\n")
    
    import subprocess
    result = subprocess.run(
        ["timeout", "20", "python3", "src/wave_hand_standalone.py"],
        capture_output=True,
        text=True
    )
    
    print("输出:")
    for line in result.stdout.strip().split('\n')[-15:]:
        print(f"  {line}")
    
    print(f"\n返回码: {result.returncode}")
    if result.returncode == 0:
        print("✓ 独立脚本执行成功")
        return True
    else:
        print("✗ 独立脚本执行失败")
        print("  可能原因: 机械臂未连接/电源未开/网络不通")
        return False


def test_controller():
    """测试控制器触发"""
    print("\n" + "="*60)
    print("测试2: 控制器触发")
    print("="*60)
    print("说明: 模拟检测到人，测试触发流程\n")
    
    from wave_action_simple import SimpleWaveActionController
    
    ctrl = SimpleWaveActionController(min_interval=3)
    
    print("模拟检测到人，距离1.5m...")
    print("触发挥手动作...\n")
    
    ctrl.trigger()
    
    print("等待执行完成...")
    while ctrl.is_running:
        time.sleep(1)
        print("  .", end="", flush=True)
    
    print("\n\n执行完成!")
    stats = ctrl.get_stats()
    print(f"统计: 触发{stats['trigger_count']}次, 跳过{stats['skip_count']}次")
    
    return True


def test_detection_simulation():
    """模拟检测循环"""
    print("\n" + "="*60)
    print("测试3: 检测循环模拟")
    print("="*60)
    print("说明: 模拟多次检测，测试触发逻辑\n")
    
    from wave_action_simple import SimpleWaveActionController
    
    ctrl = SimpleWaveActionController(min_interval=5)
    welcome_distance = 2.0
    
    # 模拟8次检测
    for i in range(8):
        print(f"\n检测 #{i+1}:")
        
        # 模拟人在1.5米处
        distance = 1.5
        
        if distance <= welcome_distance:
            print(f"  检测到人，距离: {distance}m")
            
            if ctrl.can_trigger():
                print("  >> 触发")
                ctrl.trigger()
                
                # 等待完成
                while ctrl.is_running:
                    time.sleep(0.5)
            else:
                remaining = ctrl.get_remaining_cooldown()
                print(f"  -- 冷却中 ({remaining:.1f}秒)")
        else:
            print(f"  距离过远: {distance}m")
        
        time.sleep(1)
    
    print("\n" + "="*60)
    print("最终统计")
    print("="*60)
    stats = ctrl.get_stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")


def main():
    print("="*60)
    print("挥手动作快速测试")
    print("="*60)
    print()
    print("请选择测试项目:")
    print("  1) 独立脚本 (验证机械臂)")
    print("  2) 控制器触发 (验证Web端逻辑)")
    print("  3) 检测循环模拟 (完整流程)")
    print("  4) 全部测试")
    print("  5) 退出")
    print()
    
    try:
        choice = input("选择 [1-5]: ").strip()
    except KeyboardInterrupt:
        print("\n退出")
        return
    
    if choice == "1":
        test_standalone()
    elif choice == "2":
        test_controller()
    elif choice == "3":
        test_detection_simulation()
    elif choice == "4":
        test_standalone()
        test_controller()
    else:
        print("退出")
        return
    
    print("\n" + "="*60)
    print("测试完成!")
    print("="*60)


if __name__ == "__main__":
    main()
