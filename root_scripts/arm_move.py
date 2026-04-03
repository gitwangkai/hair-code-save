#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机械臂运动控制脚本
目标：移动到 [10, 10, 10, 10, 30, 10] 然后归位到 [0, 0, 0, 0, 0, 0]
"""

import time
import sys

# 尝试导入PallasSDK
try:
    from PallasSDK import Controller, HiddenDataType, LocationJ
except ImportError:
    print("错误：无法导入PallasSDK。请确保已安装SDK并source了ROS2环境。")
    print("运行: source ~/Haier_robot_ws/install/setup.bash")
    sys.exit(1)

# 配置参数
ROBOT_IP = "192.168.3.100"

# 关节限位（来自SKILL.md）
JOINT_LIMITS = {
    "J1": {"min": -70.0, "max": 200.0},
    "J2": {"min": 0.0, "max": 120.0},
    "J3": {"min": -55.0, "max": 55.0},
    "J4": {"min": 0.0, "max": 120.0},
    "J5": {"min": -85.0, "max": 85.0},
    "J6": {"min": -20.0, "max": 20.0},
}

# 目标位置
TARGET_POSE = [10.0, 10.0, 10.0, 10.0, 30.0, 10.0]
HOME_POSE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def check_joint_limits(angles):
    """检查关节角度是否在限位范围内"""
    keys = ["J1", "J2", "J3", "J4", "J5", "J6"]
    for i, angle in enumerate(angles):
        lo = JOINT_LIMITS[keys[i]]["min"]
        hi = JOINT_LIMITS[keys[i]]["max"]
        if not (lo <= angle <= hi):
            return False, f"{keys[i]} 角度 {angle:.2f}° 超出限位 [{lo}, {hi}]"
    return True, ""


def wait_for_reach(target_angles, timeout=30, tolerance=0.5):
    """等待机械臂到达目标位置"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        max_diff = max(abs(joint_pos[i] - target_angles[i]) for i in range(6))
        if max_diff < tolerance:
            return True
        time.sleep(0.1)
    return False


# 全局关节位置变量
joint_pos = [0.0] * 7


def hidden_callback(data_type, robot, data):
    """隐藏数据回调函数"""
    global joint_pos
    if data_type == HiddenDataType.RobotJointPos:
        received = [float(v) for v in data]
        for i in range(min(len(received), 7)):
            joint_pos[i] = received[i]


def main():
    print("=" * 50)
    print("海尔机器人 NX-7 机械臂运动控制")
    print("=" * 50)

    # 检查目标位置限位
    print("\n[1/5] 检查目标位置限位...")
    ok, msg = check_joint_limits(TARGET_POSE)
    if not ok:
        print(f"[错误] {msg}")
        return 1
    print(f"目标位置 {TARGET_POSE} 限位检查通过")

    ok, msg = check_joint_limits(HOME_POSE)
    if not ok:
        print(f"[错误] {msg}")
        return 1
    print(f"归位位置 {HOME_POSE} 限位检查通过")

    # 初始化控制器
    print(f"\n[2/5] 连接到机械臂控制器 ({ROBOT_IP})...")
    ctrl = Controller()
    ctrl.SetHiddenCallback(hidden_callback)

    try:
        ctrl.Connect(ROBOT_IP)
        print("连接成功！")
    except Exception as e:
        print(f"连接失败: {e}")
        return 1

    # 等待初始化
    print("\n[3/5] 等待初始化完成 (30秒)...")
    ctrl.SetHiddenOn(HiddenDataType.RobotJointPos)
    time.sleep(30)
    print("初始化完成")

    # 伺服上电
    print("\n[4/5] 伺服上电...")
    ctrl.SetPowerEnable(True)
    time.sleep(2)
    print("伺服已上电")

    # 添加机器人
    robot = ctrl.AddRobot(1)
    robot.SetFrameType(1)
    robot.SetSpeed(10)  # 设置为较慢的速度，安全第一
    print(f"当前速度: 10%")

    # 执行目标运动
    print(f"\n[5/5] 执行运动到目标位置: {TARGET_POSE}")
    robot.MoveJ(LocationJ(*TARGET_POSE))

    print("等待到达目标位置...")
    if wait_for_reach(TARGET_POSE, timeout=30):
        print("已到达目标位置！")
    else:
        print("等待超时，但继续执行...")

    time.sleep(2)

    # 执行归位运动
    print(f"\n执行归位运动到: {HOME_POSE}")
    robot.MoveJ(LocationJ(*HOME_POSE))

    print("等待到达归位位置...")
    if wait_for_reach(HOME_POSE, timeout=30):
        print("已到达归位位置！")
    else:
        print("等待超时")

    time.sleep(1)

    # 关闭
    print("\n[清理] 伺服下电...")
    ctrl.SetPowerEnable(False)

    print("\n" + "=" * 50)
    print("运动序列执行完成")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
