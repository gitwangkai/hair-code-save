#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作脚本 - 快速版

特点:
- 更快的执行速度
- 确保每次回到原点
- 简化流程，提高可靠性
"""

import sys
import os
import time
import signal

# 添加路径
sys.path.insert(0, os.path.dirname(__file__))


def main():
    """主函数 - 执行挥手动作"""
    try:
        from PallasSDK import Controller, LocationJ
    except ImportError:
        print("[错误] 无法导入 PallasSDK")
        return 1
    
    ctrl = None
    
    try:
        print("="*50)
        print("挥手动作 - 快速执行")
        print("="*50)
        
        # 连接
        print("\n[1/4] 连接机械臂...")
        ctrl = Controller()
        ctrl.Connect("192.168.3.100")
        ctrl.SetPowerEnable(True)
        time.sleep(0.3)
        
        robot = ctrl.AddRobot(1)
        robot.SetFrameType(1)
        robot.SetSpeed(50)  # 较快速度
        print("[1/4] ✓ 已连接")
        
        # 确保在原点
        print("\n[2/4] 回到原点 [0,0,0,0,0,0]...")
        robot.MoveJ(LocationJ(0, 0, 0, 0, 0, 0))
        time.sleep(1.0)  # 等待到位
        print("[2/4] ✓ 已到达原点")
        
        # 移动到准备姿势 (简化版)
        print("\n[3/4] 挥手动作...")
        # 准备姿势
        robot.MoveJ(LocationJ(64.3, 0, 13.2, 85.9, -84.8, 0))
        time.sleep(0.8)
        
        # 快速挥手3次
        for i in range(3):
            robot.MoveJ(LocationJ(64.3, 0, 20, 85.9, -84.8, 0))   # 左
            time.sleep(0.2)
            robot.MoveJ(LocationJ(64.3, 0, -20, 85.9, -84.8, 0))  # 右
            time.sleep(0.2)
        
        # 回到准备姿势
        robot.MoveJ(LocationJ(64.3, 0, 13.2, 85.9, -84.8, 0))
        time.sleep(0.3)
        print("[3/4] ✓ 挥手完成")
        
        # 必须回到原点
        print("\n[4/4] 回到原点 [0,0,0,0,0,0]...")
        robot.MoveJ(LocationJ(0, 0, 0, 0, 0, 0))
        time.sleep(1.0)  # 确保到位
        print("[4/4] ✓ 已到达原点")
        
        # 下电
        ctrl.SetPowerEnable(False)
        
        print("\n" + "="*50)
        print("  完成 - 已回到原点 [0,0,0,0,0,0]")
        print("="*50)
        
        return 0
        
    except Exception as e:
        print(f"\n[错误] {e}")
        # 出错也要回到原点
        if ctrl:
            try:
                print("[恢复] 紧急回到原点...")
                ctrl.SetPowerEnable(True)
                robot = ctrl.AddRobot(1)
                robot.SetFrameType(1)
                robot.MoveJ(LocationJ(0, 0, 0, 0, 0, 0))
                time.sleep(1.0)
                ctrl.SetPowerEnable(False)
                print("[恢复] ✓ 已回到原点")
            except:
                pass
        return 1


if __name__ == "__main__":
    sys.exit(main())
