#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作脚本 - 安全版本
带错误处理和超时机制
"""

import time
import os
import math
import sys

# 设置超时，避免无限等待
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("操作超时")

# 10秒超时
signal.signal(signal.SIGALRM, timeout_handler)

try:
    from PallasSDK import Controller, HiddenDataType, ComPort
    from PallasSDK import LocationJ
except ImportError as e:
    print(f"[错误] 无法导入 PallasSDK: {e}")
    sys.exit(1)

# ========== 关节限位配置 ==========
JOINT_LIMITS = {
    "J1": {"min": -70.0,  "max": 200.0,  "max_speed": 120},
    "J2": {"min":   0.0,  "max": 120.0,  "max_speed":  40},
    "J3": {"min": -55.0,  "max":  55.0,  "max_speed":  70},
    "J4": {"min":   0.0,  "max": 120.0,  "max_speed":  65},
    "J5": {"min": -85.0,  "max":  85.0,  "max_speed": 253},
    "J6": {"min": -20.0,  "max":  20.0,  "max_speed": 342},
    "J7": {"min": -10.0,  "max":  10.0,  "max_speed": 342},
}

# 当前关节角度
joint_pos = [0.0] * 7

def hidden_callback(type, robot, data):
    global joint_pos
    if type == HiddenDataType.RobotJointPos:
        joint_pos = [float(i) for i in data[:7]]

def check_joint_limits(angles):
    """校验关节角度是否在硬限位范围内"""
    keys = ["J1", "J2", "J3", "J4", "J5", "J6", "J7"]
    for i, angle in enumerate(angles):
        lo = JOINT_LIMITS[keys[i]]["min"]
        hi = JOINT_LIMITS[keys[i]]["max"]
        if not (lo <= angle <= hi):
            return False, f"{keys[i]} 角度 {angle:.2f}° 超出限位 [{lo}, {hi}]"
    return True, ""

def safe_move(robot, angles):
    """限位校验通过后再执行 MoveJ"""
    ok, msg = check_joint_limits(angles)
    if not ok:
        print(f"[限位拦截] {msg}")
        return False
    robot.MoveJ(LocationJ(*angles[:6]))
    return True

def rad2deg(rad):
    """弧度转角度"""
    return rad * 180.0 / math.pi

# ========== 动作配置 ==========
SAFE_HOME_POSE = [0.00, 0.64, -0.02, 0.0, 0.11, -1.01, 0.0]

WAVE_HAND_PREPARE = [
    rad2deg(1.122),   # J1 = 64.3°
    0.0,              # J2 = 0°
    rad2deg(0.231),   # J3 = 13.2°
    rad2deg(1.50),    # J4 = 85.9°
    rad2deg(-1.480),  # J5 = -84.8°
    0.0,              # J6 = 0°
    0.0               # J7 = 0°
]

WAVE_HAND_SWING_LEFT = [
    rad2deg(1.122),    # J1
    0.0,               # J2
    rad2deg(0.231),    # J3 = 13.2° (向前)
    rad2deg(1.50),     # J4
    rad2deg(-1.480),   # J5
    0.0,               # J6
    0.0                # J7
]

WAVE_HAND_SWING_RIGHT = [
    rad2deg(1.122),    # J1
    0.0,               # J2
    rad2deg(-0.231),   # J3 = -13.2° (向后)
    rad2deg(1.50),     # J4
    rad2deg(-1.480),   # J5
    0.0,               # J6
    0.0                # J7
]

WAVE_TIMES = 3        # 挥手次数
POSE_DELAY = 0.3      # 每个点位间隔

def wave_hand(robot):
    """执行挥手动作"""
    print("\n" + "="*50)
    print("执行挥手动作")
    print("="*50)
    
    # 1. 先运动到准备姿势
    print("\n[1/3] 移动到准备姿势...")
    if not safe_move(robot, WAVE_HAND_PREPARE):
        print("准备姿势移动失败！")
        return False
    time.sleep(1.5)
    
    # 2. 开始挥手
    print(f"\n[2/3] 开始挥手 {WAVE_TIMES} 次...")
    for i in range(WAVE_TIMES):
        print(f"      挥手 {i+1}/{WAVE_TIMES}")
        if not safe_move(robot, WAVE_HAND_SWING_LEFT):
            return False
        time.sleep(POSE_DELAY)
        
        if not safe_move(robot, WAVE_HAND_SWING_RIGHT):
            return False
        time.sleep(POSE_DELAY)
    
    # 3. 回到中立位置
    print(f"\n[3/3] 回到准备位置...")
    if not safe_move(robot, WAVE_HAND_PREPARE):
        return False
    time.sleep(0.5)
    
    print("\n挥手动作执行完成！")
    return True

def go_home(robot):
    """回到安全位姿"""
    print("\n回到安全位...")
    safe_move(robot, SAFE_HOME_POSE)
    time.sleep(1.2)
    print("已回到安全位")

def main():
    ctrl = None
    robot = None
    
    try:
        print("="*50)
        print("挥手动作 - 安全版本")
        print("="*50)
        
        # 设置连接超时
        signal.alarm(10)
        
        ctrl = Controller()
        ctrl.SetHiddenCallback(hidden_callback)
        
        print("\n连接机械臂...")
        ctrl.Connect("192.168.3.100")
        print("✓ 连接成功")
        
        ctrl.SetHiddenOn(HiddenDataType.RobotJointPos)
        
        # 取消超时
        signal.alarm(0)
        
        serial_name = "COM2"
        try:
            ctrl.ComOpen(serial_name, ComPort.Com_485, 115200, 8, 1, 0, True)
            print("✓ 灵巧手连接成功")
        except:
            print("! 灵巧手未连接")
        
        print("\n伺服上电...")
        ctrl.SetPowerEnable(True)
        time.sleep(0.5)
        
        robot = ctrl.AddRobot(1)
        robot.SetFrameType(1)
        robot.SetSpeed(30)
        
        print("\n机械臂初始化完成！")
        
        # 执行挥手
        success = wave_hand(robot)
        
        # 回到安全位
        go_home(robot)
        
        return 0 if success else 1
        
    except TimeoutError:
        print("\n[错误] 连接超时，请检查:")
        print("  1. 机械臂电源是否开启")
        print("  2. 网络连接是否正常 (192.168.3.100)")
        return 1
    except Exception as e:
        print(f"\n[错误] 执行失败: {e}")
        return 1
    finally:
        if ctrl:
            print("\n关闭机械臂...")
            try:
                ctrl.SetPowerEnable(False)
            except:
                pass
            try:
                ctrl.ComClose("COM2")
            except:
                pass
            print("已关闭")

if __name__ == "__main__":
    sys.exit(main())
