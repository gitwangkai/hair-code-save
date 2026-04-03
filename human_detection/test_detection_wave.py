#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检测触发挥手测试

模拟检测到人的场景，测试完整的挥手流程
"""

import sys
import time
sys.path.insert(0, 'src')

from wave_action_simple import SimpleWaveActionController


def test_detection_to_wave():
    """测试从检测到挥手的完整流程"""
    print("="*70)
    print("  检测触发挥手测试")
    print("="*70)
    print()
    print("流程: 检测到人 → 触发挥手 → 执行动作 → 回到初始位姿")
    print()
    
    # 创建控制器
    controller = SimpleWaveActionController(
        audio_file="/home/aidlux/auto.mp3",
        min_interval=5  # 5秒间隔，方便测试
    )
    
    welcome_distance = 2.0  # 迎宾距离2米
    
    # 模拟10次检测
    for i in range(10):
        print(f"\n{'-'*70}")
        print(f"检测 #{i+1}")
        print('-'*70)
        
        # 模拟检测到人在1.5米处
        person_distance = 1.5
        
        # 判断是否在迎宾范围内
        if person_distance <= welcome_distance:
            print(f"✓ 检测到人，距离: {person_distance}m (在迎宾范围 {welcome_distance}m 内)")
            
            # 检查是否可以触发
            if controller.can_trigger():
                print(">> 触发挥手动作")
                print("   流程: 连接 → 初始位姿 → 准备 → 挥手 → 初始位姿 → 断开")
                
                triggered = controller.trigger()
                if triggered:
                    print("   [状态] 已触发，等待执行...")
                    
                    # 等待执行完成
                    while controller.is_running:
                        time.sleep(1)
                        print("   .", end="", flush=True)
                    
                    print("\n   [状态] 执行完成")
                else:
                    print("   [错误] 触发失败")
            else:
                remaining = controller.get_remaining_cooldown()
                print(f"-- 冷却中，剩余 {remaining:.1f} 秒 (防止频繁触发)")
        else:
            print(f"○ 检测到人，距离: {person_distance}m (超出迎宾范围 {welcome_distance}m)")
        
        # 模拟检测间隔
        time.sleep(1)
    
    # 最终统计
    print(f"\n{'='*70}")
    print("  测试完成 - 统计")
    print('='*70)
    
    stats = controller.get_stats()
    print(f"  触发次数: {stats['trigger_count']}")
    print(f"  跳过次数: {stats['skip_count']} (冷却中)")
    print(f"  触发间隔: {stats['min_interval']} 秒")
    
    print(f"\n说明:")
    print(f"  - 每次触发执行完整动作: 初始位姿[0,0,0,0,0,0] → 准备 → 挥手 → 初始位姿[0,0,0,0,0,0]")
    print(f"  - 无论成功或失败，机械臂都会回到初始位姿 [0,0,0,0,0,0]")
    print(f"  - 触发间隔保护: {stats['min_interval']}秒内不会重复触发")


def test_single_trigger():
    """测试单次触发"""
    print("\n" + "="*70)
    print("  单次触发测试")
    print("="*70)
    
    controller = SimpleWaveActionController(min_interval=3)
    
    print("\n模拟: 检测到人，距离1.5m")
    print("触发: 挥手动作 (将回到初始位姿 [0,0,0,0,0,0])")
    print()
    
    controller.trigger()
    
    print("等待执行完成...")
    while controller.is_running:
        time.sleep(1)
        print("  .", end="", flush=True)
    
    print("\n\n完成!")


def main():
    print("="*70)
    print("  挥手动作 - 检测触发测试")
    print("  功能: 检测到人 → 挥手 → 回到初始位姿 [0,0,0,0,0,0]")
    print("="*70)
    print()
    print("请选择测试项目:")
    print("  1) 检测循环测试 (模拟10次检测)")
    print("  2) 单次触发测试")
    print("  3) 退出")
    print()
    
    try:
        choice = input("选择 [1-3]: ").strip()
    except KeyboardInterrupt:
        print("\n退出")
        return
    
    if choice == "1":
        test_detection_to_wave()
    elif choice == "2":
        test_single_trigger()
    else:
        print("退出")
        return
    
    print("\n" + "="*70)
    print("  测试完成!")
    print("="*70)


if __name__ == "__main__":
    main()
