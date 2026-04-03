#!/usr/bin/env python3
"""
快速挥手（3次）- 适用于已预热的机械臂

使用：python3 wave_quick.py
"""
import time
import atexit
from PallasSDK import Controller, LocationJ

ROBOT_IP = "192.168.3.100"
HOME = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
WAVE_PREPARE = [64.3, 0, 13.2, 85.9, -84.8, 0]

def shutdown(ctrl, robot):
    """安全关闭"""
    try:
        print("\n→ 回到 HOME...")
        robot.MoveJ(LocationJ(*HOME))
        time.sleep(2)
        ctrl.SetPowerEnable(False)
        print("✓ 已安全关闭")
    except:
        pass

def main():
    print("=" * 40)
    print("机械臂挥手 x 3")
    print("=" * 40)
    
    ctrl = Controller()
    print("→ 连接...")
    ctrl.Connect(ROBOT_IP)
    
    print("→ 等待初始化 (15s)...")
    time.sleep(15)  # 已预热，减少等待
    
    print("→ 伺服上电...")
    ctrl.SetPowerEnable(True)
    robot = ctrl.AddRobot(1)
    robot.SetSpeed(10)
    
    atexit.register(shutdown, ctrl, robot)
    
    print("→ 回到 HOME...")
    robot.MoveJ(LocationJ(*HOME))
    time.sleep(2)
    
    print("→ 移动到挥手位...")
    robot.MoveJ(LocationJ(*WAVE_PREPARE))
    time.sleep(1.5)
    
    print("→ 挥手 3 次...")
    for i in range(3):
        # 左摆
        left = [x + o for x, o in zip(WAVE_PREPARE, [0, 0, 10, 0, 0, 0])]
        robot.MoveJ(LocationJ(*left))
        time.sleep(0.5)
        # 右摆
        right = [x + o for x, o in zip(WAVE_PREPARE, [0, 0, -10, 0, 0, 0])]
        robot.MoveJ(LocationJ(*right))
        time.sleep(0.5)
        print(f"  第 {i+1}/3 次")
    
    print("→ 回到准备位...")
    robot.MoveJ(LocationJ(*WAVE_PREPARE))
    time.sleep(1)
    
    print("→ 回到 HOME...")
    robot.MoveJ(LocationJ(*HOME))
    time.sleep(2)
    
    atexit.unregister(shutdown)
    shutdown(ctrl, robot)
    
    print("=" * 40)
    print("✓ 挥手完成！")
    print("=" * 40)

if __name__ == "__main__":
    main()
