#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整挥手动作测试

测试完整的动作流程:
1. 检测到人
2. 触发挥手
3. 执行: 原点→准备→挥手→原点
4. 播放音频
"""

import sys
import time
sys.path.insert(0, 'src')


def test_with_mock():
    """使用模拟模式测试"""
    print("="*60)
    print("测试1: 模拟模式 (无需机械臂)")
    print("="*60)
    
    from wave_action import MockWaveActionController
    
    ctrl = MockWaveActionController(min_interval=3)
    
    print("\n模拟检测到人...")
    print("触发动作流程: 原点→准备→挥手→原点+音频")
    
    ctrl.trigger()
    
    while ctrl.is_running:
        time.sleep(1)
        print("  .", end="", flush=True)
    
    print("\n\n完成!")
    print(f"统计: {ctrl.get_stats()}")
    return True


def test_with_real():
    """使用真实机械臂测试"""
    print("\n" + "="*60)
    print("测试2: 真实机械臂")
    print("="*60)
    
    from wave_action_simple import SimpleWaveActionController
    
    ctrl = SimpleWaveActionController(min_interval=5)
    
    print("\n注意: 这会尝试连接真实机械臂")
    print("如果机械臂未连接，会在15秒后超时\n")
    
    input("按回车开始测试，或按 Ctrl+C 取消...")
    
    print("\n触发动作...")
    ctrl.trigger()
    
    while ctrl.is_running:
        time.sleep(1)
        print("  .", end="", flush=True)
    
    print("\n\n完成!")
    print(f"统计: {ctrl.get_stats()}")
    return True


def test_detection_to_wave():
    """测试从检测到挥手的完整流程"""
    print("\n" + "="*60)
    print("测试3: 检测→挥手完整流程")
    print("="*60)
    
    from wave_action_simple import SimpleWaveActionController
    
    ctrl = SimpleWaveActionController(min_interval=3)
    
    # 模拟检测循环
    print("\n模拟检测循环 (间隔1秒):")
    for i in range(8):
        print(f"\n--- 检测 #{i+1} ---")
        
        # 模拟检测到人在1.5米处
        person_distance = 1.5
        welcome_distance = 2.0
        
        if person_distance <= welcome_distance:
            print(f"检测到人，距离: {person_distance}m")
            
            if ctrl.can_trigger():
                print(">> 触发挥手动作")
                ctrl.trigger()
                
                # 等待完成
                while ctrl.is_running:
                    time.sleep(0.5)
                    print(".", end="", flush=True)
                print()
            else:
                remaining = ctrl.get_remaining_cooldown()
                print(f"冷却中 ({remaining:.1f}秒)，跳过")
        else:
            print(f"距离过远 ({person_distance}m)，不触发")
        
        time.sleep(1)
    
    print("\n" + "="*60)
    print("最终统计")
    print("="*60)
    stats = ctrl.get_stats()
    print(f"  触发次数: {stats['trigger_count']}")
    print(f"  跳过次数: {stats['skip_count']}")
    print(f"  当前间隔: {stats['min_interval']}秒")


def main():
    print("="*60)
    print("完整挥手动作测试")
    print("="*60)
    print()
    print("请选择测试项目:")
    print("  1) 模拟模式 (推荐)")
    print("  2) 真实机械臂")
    print("  3) 检测→挥手完整流程")
    print("  4) 全部测试")
    print("  5) 退出")
    print()
    
    try:
        choice = input("选择 [1-5]: ").strip()
    except KeyboardInterrupt:
        print("\n退出")
        return
    
    if choice == "1":
        test_with_mock()
    elif choice == "2":
        test_with_real()
    elif choice == "3":
        test_detection_to_wave()
    elif choice == "4":
        test_with_mock()
        test_detection_to_wave()
    else:
        print("退出")
        return
    
    print("\n" + "="*60)
    print("测试完成!")
    print("="*60)


if __name__ == "__main__":
    main()
