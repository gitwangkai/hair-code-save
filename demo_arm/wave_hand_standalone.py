#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作脚本 - 完全独立版本

此脚本完全独立执行，不与其他 Python 进程共享内存空间
用于避免 PallasSDK 与 Flask 的冲突

用法:
    python3 wave_hand_standalone.py [选项]

选项:
    --check     仅检查机械臂连接，不执行动作
    --home      执行后回到原点
    --timeout N 设置超时时间(秒)
"""

import sys
import os
import time
import math
import signal

# 立即设置超时，防止无限等待
def setup_timeout(seconds=25):
    def timeout_handler(signum, frame):
        print("[错误] 执行超时", file=sys.stderr)
        sys.exit(2)
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)

# 解析命令行参数
timeout_seconds = 25
go_home = False
check_only = False

for i, arg in enumerate(sys.argv[1:]):
    if arg == '--timeout' and i + 1 < len(sys.argv[1:]):
        timeout_seconds = int(sys.argv[i + 2])
    elif arg == '--home':
        go_home = True
    elif arg == '--check':
        check_only = True

setup_timeout(timeout_seconds)

# 关节限位
JOINT_LIMITS = {
    "J1": {"min": -70.0,  "max": 200.0},
    "J2": {"min":   0.0,  "max": 120.0},
    "J3": {"min": -55.0,  "max":  55.0},
    "J4": {"min":   0.0,  "max": 120.0},
    "J5": {"min": -85.0,  "max":  85.0},
    "J6": {"min": -20.0,  "max":  20.0},
}

def check_joint_limits(angles):
    """校验关节角度"""
    keys = ["J1", "J2", "J3", "J4", "J5", "J6"]
    for i, angle in enumerate(angles[:6]):
        lo = JOINT_LIMITS[keys[i]]["min"]
        hi = JOINT_LIMITS[keys[i]]["max"]
        if not (lo <= angle <= hi):
            return False, f"{keys[i]} 角度 {angle:.2f}° 超出限位"
    return True, ""

def rad2deg(rad):
    """弧度转角度"""
    return rad * 180.0 / math.pi

# 动作配置
SAFE_HOME_POSE = [0.00, 36.7, -1.1, 0.0, 6.3, -57.9]

WAVE_HAND_PREPARE = [
    rad2deg(1.122),   # J1
    0.0,              # J2
    rad2deg(0.231),   # J3
    rad2deg(1.50),    # J4
    rad2deg(-1.480),  # J5
    0.0,              # J6
]

WAVE_HAND_SWING_LEFT = [
    rad2deg(1.122),
    0.0,
    rad2deg(0.231),   # 向前
    rad2deg(1.50),
    rad2deg(-1.480),
    0.0,
]

WAVE_HAND_SWING_RIGHT = [
    rad2deg(1.122),
    0.0,
    rad2deg(-0.231),  # 向后
    rad2deg(1.50),
    rad2deg(-1.480),
    0.0,
]

def main():
    try:
        # 延迟导入 PallasSDK，确保超时机制先生效
        from PallasSDK import Controller, HiddenDataType
        from PallasSDK import LocationJ
    except ImportError as e:
        print(f"[错误] 无法导入 PallasSDK: {e}", file=sys.stderr)
        return 1
    
    joint_pos = [0.0] * 7
    
    def hidden_callback(type, robot, data):
        nonlocal joint_pos
        if type == HiddenDataType.RobotJointPos:
            joint_pos = [float(i) for i in data[:7]]
    
    ctrl = None
    
    try:
        print("=" * 50)
        print("挥手动作 - 独立进程版本")
        print("=" * 50)
        
        ctrl = Controller()
        ctrl.SetHiddenCallback(hidden_callback)
        
        print("\n连接机械臂 (192.168.3.100)...")
        ctrl.Connect("192.168.3.100")
        print("✓ 连接成功")
        
        # 取消超时
        signal.alarm(0)
        
        ctrl.SetHiddenOn(HiddenDataType.RobotJointPos)
        
        print("\n伺服上电...")
        ctrl.SetPowerEnable(True)
        time.sleep(0.5)
        
        robot = ctrl.AddRobot(1)
        robot.SetFrameType(1)
        robot.SetSpeed(30)
        
        print("✓ 机械臂就绪")
        
        if check_only:
            print("\n连接检查通过")
            return 0
        
        # 执行挥手动作
        print("\n" + "-" * 50)
        print("开始挥手动作")
        print("-" * 50)
        
        # 1. 准备姿势
        print("\n[1/3] 移动到准备姿势...")
        ok, msg = check_joint_limits(WAVE_HAND_PREPARE)
        if not ok:
            print(f"[错误] {msg}")
            return 1
        
        robot.MoveJ(LocationJ(*WAVE_HAND_PREPARE[:6]))
        time.sleep(1.5)
        print("✓ 到位")
        
        # 2. 挥手
        print("\n[2/3] 挥手 3 次...")
        for i in range(3):
            print(f"  挥手 {i+1}/3")
            robot.MoveJ(LocationJ(*WAVE_HAND_SWING_LEFT[:6]))
            time.sleep(0.3)
            robot.MoveJ(LocationJ(*WAVE_HAND_SWING_RIGHT[:6]))
            time.sleep(0.3)
        print("✓ 完成")
        
        # 3. 回到准备位置
        print("\n[3/3] 回到准备位置...")
        robot.MoveJ(LocationJ(*WAVE_HAND_PREPARE[:6]))
        time.sleep(0.5)
        print("✓ 到位")
        
        # 4. 回到安全位 (可选)
        if go_home:
            print("\n回到安全位...")
            robot.MoveJ(LocationJ(*SAFE_HOME_POSE[:6]))
            time.sleep(1.2)
            print("✓ 到位")
        
        print("\n" + "=" * 50)
        print("挥手动作执行完成!")
        print("=" * 50)
        
        return 0
        
    except Exception as e:
        print(f"\n[错误] {e}", file=sys.stderr)
        return 1
    finally:
        if ctrl:
            print("\n关闭机械臂...")
            try:
                ctrl.SetPowerEnable(False)
            except:
                pass
            print("✓ 已关闭")

if __name__ == "__main__":
    sys.exit(main())
