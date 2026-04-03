#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作联动集成测试

测试内容:
1. 挥手动作控制器初始化
2. 触发间隔控制
3. 与检测系统联动
"""

import sys
import time
sys.path.insert(0, 'src')
sys.path.insert(0, 'utils')

from wave_action import MockWaveActionController


def test_interval_control():
    """测试触发间隔控制"""
    print("=" * 60)
    print("测试: 触发间隔控制")
    print("=" * 60)
    
    # 创建控制器，间隔5秒
    controller = MockWaveActionController(min_interval=5)
    
    print("\n1. 初始状态")
    print(f"   触发间隔: {controller.get_interval()}秒")
    print(f"   是否可以触发: {controller.can_trigger()}")
    
    print("\n2. 第一次触发")
    result = controller.trigger()
    print(f"   结果: {'成功' if result else '失败'}")
    print(f"   是否可以触发: {controller.can_trigger()}")
    
    print("\n3. 间隔内再次触发 (应失败)")
    result = controller.trigger()
    print(f"   结果: {'成功' if result else '失败'} (预期: 失败)")
    print(f"   剩余冷却: {controller.get_remaining_cooldown():.1f}秒")
    
    print("\n4. 等待5秒...")
    for i in range(5, 0, -1):
        print(f"   倒计时: {i}秒 (剩余: {controller.get_remaining_cooldown():.1f}秒)")
        time.sleep(1)
    
    print("\n5. 间隔后触发 (应成功)")
    result = controller.trigger()
    print(f"   结果: {'成功' if result else '失败'} (预期: 成功)")
    
    print("\n6. 查看统计")
    stats = controller.get_stats()
    print(f"   触发次数: {stats['trigger_count']}")
    print(f"   跳过次数: {stats['skip_count']}")
    
    print("\n✓ 触发间隔控制测试通过")


def test_dynamic_interval():
    """测试动态修改间隔"""
    print("\n" + "=" * 60)
    print("测试: 动态修改间隔")
    print("=" * 60)
    
    controller = MockWaveActionController(min_interval=10)
    print(f"\n初始间隔: {controller.get_interval()}秒")
    
    # 修改间隔
    controller.set_interval(3)
    print(f"修改后间隔: {controller.get_interval()}秒")
    
    # 触发一次
    controller.trigger()
    print(f"触发后剩余冷却: {controller.get_remaining_cooldown():.1f}秒")
    
    # 缩短间隔
    controller.set_interval(1)
    print(f"缩短间隔后: {controller.get_interval()}秒")
    print(f"是否可以触发: {controller.can_trigger()}")
    
    print("\n✓ 动态修改间隔测试通过")


def test_integration_simulation():
    """模拟集成测试"""
    print("\n" + "=" * 60)
    print("测试: 模拟检测联动")
    print("=" * 60)
    
    controller = MockWaveActionController(min_interval=3)
    
    print("\n模拟检测循环 (间隔3秒):")
    for i in range(10):
        print(f"\n--- 第 {i+1} 次检测 ---")
        
        # 模拟检测到人在范围内
        if controller.can_trigger():
            result = controller.trigger()
            print(f"检测结果: 有人 | 触发挥手: {'成功' if result else '失败'}")
        else:
            remaining = controller.get_remaining_cooldown()
            print(f"检测结果: 有人 | 冷却中: {remaining:.1f}秒 | 跳过")
        
        time.sleep(1)
    
    print("\n最终统计:")
    stats = controller.get_stats()
    print(f"  触发: {stats['trigger_count']}次")
    print(f"  跳过: {stats['skip_count']}次")
    
    print("\n✓ 模拟联动测试通过")


def main():
    print("=" * 60)
    print("挥手动作联动集成测试")
    print("=" * 60)
    
    try:
        test_interval_control()
        test_dynamic_interval()
        test_integration_simulation()
        
        print("\n" + "=" * 60)
        print("所有测试通过!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n测试被中断")
    except Exception as e:
        print(f"\n测试出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
