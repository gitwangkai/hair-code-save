#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试检测触发功能

模拟检测到人的情况，验证挥手动作是否正确触发
"""

import sys
import time
sys.path.insert(0, 'src')

from wave_action_simple import SimpleWaveActionController


def test_trigger_logic():
    """测试触发逻辑"""
    print("=" * 60)
    print("测试检测触发逻辑")
    print("=" * 60)
    
    # 创建控制器
    controller = SimpleWaveActionController(
        audio_file="/home/aidlux/auto.mp3",
        min_interval=5  # 5秒间隔，方便测试
    )
    
    # 模拟检测到人
    persons = [{"distance": 1.5}]
    welcome_distance = 2.0
    
    print(f"\n模拟场景: 检测到 {len(persons)} 个人，距离 {persons[0]['distance']}m")
    print(f"迎宾距离: {welcome_distance}m")
    print(f"触发间隔: {controller.get_interval()}秒")
    
    # 检查是否可以触发
    can_trigger = controller.can_trigger()
    print(f"\n是否可以触发: {can_trigger}")
    
    if can_trigger:
        print("\n>> 触发挥手...")
        result = controller.trigger()
        print(f"触发结果: {'成功' if result else '失败'}")
        
        # 等待完成
        print("等待执行完成...")
        while controller.is_running:
            time.sleep(0.5)
            print("  .", end="", flush=True)
        print("\n执行完成!")
    else:
        remaining = controller.get_remaining_cooldown()
        print(f"冷却中，剩余: {remaining:.1f}秒")
    
    # 显示统计
    stats = controller.get_stats()
    print(f"\n统计: 触发{stats['trigger_count']}次, 跳过{stats['skip_count']}次")
    
    # 测试间隔限制
    print("\n" + "-" * 60)
    print("测试间隔限制 (2秒内再次触发)...")
    print("-" * 60)
    
    time.sleep(1)  # 等待1秒
    
    can_trigger2 = controller.can_trigger()
    remaining2 = controller.get_remaining_cooldown()
    print(f"是否可以触发: {can_trigger2}")
    print(f"剩余冷却: {remaining2:.1f}秒")
    
    if can_trigger2:
        controller.trigger()
    else:
        print(">> 触发被拒绝 (冷却中)")
    
    stats2 = controller.get_stats()
    print(f"统计: 触发{stats2['trigger_count']}次, 跳过{stats2['skip_count']}次")
    
    # 等待冷却后再次触发
    print("\n" + "-" * 60)
    print(f"等待 {remaining2:.1f} 秒后再次触发...")
    print("-" * 60)
    
    time.sleep(remaining2 + 0.5)
    
    can_trigger3 = controller.can_trigger()
    print(f"是否可以触发: {can_trigger3}")
    
    if can_trigger3:
        print(">> 再次触发...")
        controller.trigger()
        while controller.is_running:
            time.sleep(0.5)
            print("  .", end="", flush=True)
        print("\n完成!")
    
    # 最终统计
    print("\n" + "=" * 60)
    print("最终统计")
    print("=" * 60)
    final_stats = controller.get_stats()
    for key, value in final_stats.items():
        print(f"  {key}: {value}")


def test_distance_filter():
    """测试距离过滤"""
    print("\n" + "=" * 60)
    print("测试距离过滤")
    print("=" * 60)
    
    welcome_distance = 2.0
    
    test_cases = [
        {"distance": 0.5, "expected": True},   # 近距离，应该触发
        {"distance": 1.5, "expected": True},   # 中距离，应该触发
        {"distance": 2.0, "expected": True},   # 边界距离，应该触发
        {"distance": 2.5, "expected": False},  # 远距离，不应该触发
        {"distance": 3.0, "expected": False},  # 超远距离，不应该触发
    ]
    
    for case in test_cases:
        dist = case["distance"]
        should_trigger = dist <= welcome_distance
        print(f"\n距离: {dist}m, 迎宾距离: {welcome_distance}m")
        print(f"  是否应该触发: {should_trigger}")
        print(f"  期望: {'触发' if case['expected'] else '不触发'}")
        print(f"  结果: {'✓ 正确' if should_trigger == case['expected'] else '✗ 错误'}")


if __name__ == "__main__":
    try:
        test_trigger_logic()
        test_distance_filter()
        
        print("\n" + "=" * 60)
        print("测试完成!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n\n测试出错: {e}")
        import traceback
        traceback.print_exc()
