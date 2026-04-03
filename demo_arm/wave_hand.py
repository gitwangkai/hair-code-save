import time
import os
import math
from PallasSDK import Controller, HiddenDataType, ComPort
from PallasSDK import LocationJ

# ========== 关节限位配置（来自 机械臂SKILL.md） ==========
JOINT_LIMITS = {
    "J1": {"min": -70.0,  "max": 200.0,  "max_speed": 120},
    "J2": {"min":   0.0,  "max": 120.0,  "max_speed":  40},
    "J3": {"min": -55.0,  "max":  55.0,  "max_speed":  70},
    "J4": {"min":   0.0,  "max": 120.0,  "max_speed":  65},
    "J5": {"min": -85.0,  "max":  85.0,  "max_speed": 253},
    "J6": {"min": -20.0,  "max":  20.0,  "max_speed": 342},
    "J7": {"min": -10.0,  "max":  10.0,  "max_speed": 342},
}

# 当前关节角度（用于回调更新）
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

# ========== 动作配置（来自 robot_actions.yaml，弧度转为角度） ==========

# 安全位姿
SAFE_HOME_POSE = [0.00, 0.64, -0.02, 0.0, 0.11, -1.01, 0.0]

# WAVE_HAND 挥手动作（来自配置文件）
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

# 动作参数
WAVE_TIMES = 3        # 挥手次数
POSE_DELAY = 0.3      # 每个点位间隔（秒）- 加快速度

def wave_hand(robot):
    """执行挥手动作（WAVE_HAND）- 通过 J3 关节摆动"""
    print("\n" + "="*50)
    print("执行挥手动作 (WAVE_HAND)")
    print("="*50)
    
    # 1. 先运动到准备姿势
    print("\n[1/3] 移动到准备姿势...")
    print(f"      目标角度: {[f'{a:.2f}' for a in WAVE_HAND_PREPARE[:6]]}")
    if not safe_move(robot, WAVE_HAND_PREPARE):
        print("准备姿势移动失败！")
        return False
    time.sleep(1.9)  # 等待到位（增加0.4秒缓冲）
    
    # 2. 开始挥手（通过 J3 关节左右摆动）
    print(f"\n[2/3] 开始挥手 {WAVE_TIMES} 次...")
    for i in range(WAVE_TIMES):
        # 向前摆（J3 正角度）
        print(f"      挥手 {i+1}/{WAVE_TIMES} - 向前摆")
        if not safe_move(robot, WAVE_HAND_SWING_LEFT):
            return False
        time.sleep(POSE_DELAY)
        
        # 向后摆（J3 负角度）
        print(f"      挥手 {i+1}/{WAVE_TIMES} - 向后摆")
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
    print(f"目标角度: {[f'{a:.2f}' for a in SAFE_HOME_POSE[:6]]}")
    safe_move(robot, SAFE_HOME_POSE)
    time.sleep(1.4)  # 增加0.4秒缓冲
    print("已回到安全位")

def main():
    ctrl = Controller()
    ctrl.SetHiddenCallback(hidden_callback)
    
    print("连接机械臂...")
    ctrl.Connect("192.168.3.100")
    print("连接成功")
    
    ctrl.SetHiddenOn(HiddenDataType.RobotJointPos)
    
    serial_name = "COM2"
    try:
        ctrl.ComOpen(serial_name, ComPort.Com_485, 115200, 8, 1, 0, True)
        print("灵巧手连接成功")
    except:
        print("警告：灵巧手未连接")
    
    ctrl.SetPowerEnable(True)
    
    robot = ctrl.AddRobot(1)
    robot.SetFrameType(1)
    robot.SetSpeed(30)  # 设置较快的速度
    
    print("\n机械臂初始化完成！")
    print(f"当前关节角度: {[f'{j:.2f}' for j in joint_pos[:6]]}")
    
    try:
        # 立即执行挥手动作
        wave_hand(robot)
        
        # 挥手完成后立即回到安全位
        go_home(robot)
        
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"\n执行出错: {e}")
    finally:
        # 关闭
        print("\n关闭机械臂...")
        ctrl.SetPowerEnable(False)
        try:
            ctrl.ComClose(serial_name)
        except:
            pass
        print("已关闭")

if __name__ == "__main__":
    main()
