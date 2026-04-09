#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超声波感知测试程序
"""

import sys
import time
sys.path.insert(0, '/home/aidlux/skills/ultrasonic_perception')

from ultrasonic_perception import UltrasonicPerception


def test_basic_reading():
    """测试基本读取功能"""
    print("\n" + "=" * 50)
    print("测试1: 基本距离读取")
    print("=" * 50)
    
    perception = UltrasonicPerception()
    time.sleep(1)  # 等待数据
    
    # 获取距离
    dist = perception.get_distance()
    if dist:
        print(f"\n前方距离: {dist:.2f} m")
    else:
        print("\n无有效数据")
    
    perception.close()
    print("\n✓ 测试通过")


def test_obstacle_detection():
    """测试障碍物检测"""
    print("\n" + "=" * 50)
    print("测试2: 障碍物检测")
    print("=" * 50)
    
    perception = UltrasonicPerception()
    time.sleep(1)
    
    # 安全状态检测
    status = perception.get_safe_status()
    print(f"\n安全状态: {status}")
    
    # 距离判断
    dist = perception.get_distance()
    if dist:
        if dist < 0.3:
            print(f"  ✗ 危险! 距离过近: {dist:.2f}m")
        elif dist < 0.6:
            print(f"  ⚠ 警告! 距离较近: {dist:.2f}m")
        else:
            print(f"  ✓ 安全! 距离充足: {dist:.2f}m")
    
    perception.close()
    print("\n✓ 测试通过")


def test_continuous_monitoring():
    """测试持续监控"""
    print("\n" + "=" * 50)
    print("测试3: 持续监控 (按Ctrl+C停止)")
    print("=" * 50)
    
    perception = UltrasonicPerception()
    
    try:
        for i in range(20):  # 监控10秒
            print("\033[2J\033[H")  # 清屏
            print(perception.get_status_report())
            print(f"\n监控中... {i+1}/20")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n监控已停止")
    
    perception.close()
    print("\n✓ 测试通过")


def main():
    """主测试程序"""
    print("\n" + "=" * 60)
    print("       超声波感知技能测试套件")
    print("       (单路前向超声波)")
    print("=" * 60)
    
    print("""
请选择测试项目:
  1. 基本距离读取
  2. 障碍物检测
  3. 持续监控
  4. 全部测试
  0. 退出
    """)
    
    choice = input("请输入选项 (0-4): ").strip()
    
    if choice == '1':
        test_basic_reading()
    elif choice == '2':
        test_obstacle_detection()
    elif choice == '3':
        test_continuous_monitoring()
    elif choice == '4':
        test_basic_reading()
        test_obstacle_detection()
        test_continuous_monitoring()
    else:
        print("退出测试")


if __name__ == "__main__":
    main()
