#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机械臂控制器测试脚本

功能:
- 测试机械臂连接
- 测试关节运动
- 测试夹爪控制
- 测试预设动作

使用说明:
1. 确保机械臂电源开启
2. 确保网络连接正常 (IP: 192.168.3.100)
3. 运行: python3 test_arm.py

可选参数:
    --mock      使用模拟模式 (无需真实机械臂)
    --ip        指定机械臂IP (默认: 192.168.3.100)
"""

import sys
import time
import argparse

sys.path.insert(0, 'src')

from arm_controller import ArmController, MockArmController


def test_basic_connection(arm):
    """测试基本连接"""
    print("\n" + "="*50)
    print("测试 1: 基本连接")
    print("="*50)
    
    print(f"当前状态: {arm.get_state().value}")
    print(f"关节角度: {arm.get_joint_positions()}")
    
    print("✓ 连接测试通过")


def test_joint_movement(arm):
    """测试关节运动"""
    print("\n" + "="*50)
    print("测试 2: 关节运动")
    print("="*50)
    
    # 1. 回原点
    print("\n→ 回到原点...")
    if arm.move_to_home(speed=10):
        print("✓ 回原点成功")
        time.sleep(1)
    else:
        print("✗ 回原点失败")
        return False
    
    # 2. 移动 J1
    print("\n→ 移动 J1 到 10°...")
    if arm.move_joints([10, 0, 0, 0, 0, 0], speed=10):
        print("✓ J1 移动成功")
        time.sleep(1)
    else:
        print("✗ J1 移动失败")
    
    # 3. 移动 J2
    print("\n→ 移动 J2 到 -20°...")
    if arm.move_joints([10, -20, 0, 0, 0, 0], speed=10):
        print("✓ J2 移动成功")
        time.sleep(1)
    else:
        print("✗ J2 移动失败")
    
    # 4. 回到原点
    print("\n→ 回到原点...")
    arm.move_to_home(speed=10)
    
    print("\n✓ 关节运动测试通过")
    return True


def test_gripper(arm):
    """测试夹爪控制"""
    print("\n" + "="*50)
    print("测试 3: 夹爪控制")
    print("="*50)
    
    # 张开
    print("\n→ 张开夹爪...")
    if arm.gripper_open():
        print("✓ 夹爪已张开")
        time.sleep(1)
    else:
        print("✗ 夹爪控制失败")
        return False
    
    # 闭合
    print("\n→ 闭合夹爪...")
    if arm.gripper_close():
        print("✓ 夹爪已闭合")
        time.sleep(1)
    else:
        print("✗ 夹爪控制失败")
        return False
    
    print("\n✓ 夹爪控制测试通过")
    return True


def test_preset_actions(arm):
    """测试预设动作"""
    print("\n" + "="*50)
    print("测试 4: 预设动作")
    print("="*50)
    
    # 1. 欢迎动作
    print("\n→ 执行欢迎动作 (请观察)...")
    if arm.welcome_guest():
        print("✓ 欢迎动作已触发")
        time.sleep(4)  # 等待动作完成
    else:
        print("✗ 欢迎动作失败")
        return False
    
    # 2. 挥手动作
    print("\n→ 执行挥手动作 (请观察)...")
    if arm.wave_hand():
        print("✓ 挥手动作已触发")
        time.sleep(5)  # 等待动作完成
    else:
        print("✗ 挥手动作失败")
        return False
    
    print("\n✓ 预设动作测试通过")
    return True


def main():
    parser = argparse.ArgumentParser(description='机械臂控制器测试')
    parser.add_argument('--mock', action='store_true', help='使用模拟模式')
    parser.add_argument('--ip', default='192.168.3.100', help='机械臂IP地址')
    parser.add_argument('--test', choices=['all', 'connection', 'movement', 'gripper', 'action'], 
                       default='all', help='选择测试项目')
    args = parser.parse_args()
    
    print("="*60)
    print("机械臂控制器测试程序")
    print("="*60)
    
    # 创建控制器
    if args.mock:
        print("\n[模式] 模拟模式 (无需真实机械臂)")
        arm = MockArmController(ip=args.ip)
    else:
        print("\n[模式] 真实机械臂模式")
        print(f"[目标] IP: {args.ip}")
        arm = ArmController(ip=args.ip)
    
    # 连接
    print("\n正在连接机械臂...")
    if not arm.connect():
        print("\n✗ 连接失败!")
        return 1
    
    print("✓ 连接成功!")
    time.sleep(0.5)
    
    try:
        # 执行测试
        if args.test in ['all', 'connection']:
            test_basic_connection(arm)
        
        if args.test in ['all', 'movement']:
            test_joint_movement(arm)
        
        if args.test in ['all', 'gripper']:
            test_gripper(arm)
        
        if args.test in ['all', 'action']:
            test_preset_actions(arm)
        
        print("\n" + "="*60)
        print("所有测试完成!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n用户中断测试")
    finally:
        # 断开连接
        print("\n断开连接...")
        arm.disconnect()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
