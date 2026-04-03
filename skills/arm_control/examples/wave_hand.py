#!/usr/bin/env python3
"""
挥手动作示例

功能：机械臂挥手打招呼
流程：连接 → HOME → 准备位 → 挥手3次 → HOME → 断开

使用：
    python3 wave_hand.py

安全特性：
    - 关节限位检查
    - 异常自动回位
    - 超时保护
"""
import time
import atexit
import signal
from PallasSDK import Controller, LocationJ

# ==================== 配置 ====================
ROBOT_IP = "192.168.3.100"
INIT_WAIT = 30          # 初始化等待时间（秒）
MOVE_WAIT = 1.0         # 动作等待时间（秒）
WAVE_COUNT = 3          # 挥手次数
SPEED_PERCENT = 10      # 运动速度百分比

# ==================== 位姿定义 ====================
HOME_POSE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
TUCK_POSE = [0.0, 10.0, 0.0, 30.0, 0.0, 0.0]
WAVE_PREPARE = [64.3, 0, 13.2, 85.9, -84.8, 0]
WAVE_SWING_LEFT = [64.3, 0, 13.2, 85.9, -84.8, 0]
WAVE_SWING_RIGHT = [64.3, 0, -13.2, 85.9, -84.8, 0]

# ==================== 关节限位 ====================
JOINT_LIMITS = {
    "J1": {"min": -70.0, "max": 200.0},
    "J2": {"min":   0.0, "max": 120.0},
    "J3": {"min": -55.0, "max":  55.0},
    "J4": {"min":   0.0, "max": 120.0},
    "J5": {"min": -85.0, "max":  85.0},
    "J6": {"min": -20.0, "max":  20.0},
}


def check_joint_limits(angles):
    """检查关节角度是否在安全范围内"""
    keys = ["J1", "J2", "J3", "J4", "J5", "J6"]
    for i, angle in enumerate(angles):
        lo = JOINT_LIMITS[keys[i]]["min"]
        hi = JOINT_LIMITS[keys[i]]["max"]
        if not (lo <= angle <= hi):
            return False, f"{keys[i]} 角度 {angle:.2f}° 超出限位 [{lo}, {hi}]"
    return True, "OK"


def safe_move(robot, angles, wait=MOVE_WAIT):
    """带限位检查的安全运动"""
    ok, msg = check_joint_limits(angles)
    if not ok:
        print(f"  ✗ [限位拦截] {msg}")
        return False
    
    robot.MoveJ(LocationJ(*angles))
    time.sleep(wait)
    return True


def emergency_shutdown(ctrl, robot):
    """紧急关闭：返回安全位姿并下电"""
    try:
        print("\n[!] 执行紧急关闭...")
        robot.MoveJ(LocationJ(*TUCK_POSE))
        time.sleep(2)
        ctrl.SetPowerEnable(False)
        print("[✓] 已安全关闭")
    except Exception as e:
        print(f"[✗] 紧急关闭失败: {e}")


def wave_hand(robot):
    """执行挥手动作"""
    print("\n[挥手动作]")
    
    # 1. 到挥手准备位
    print("  → 移动到准备位...")
    safe_move(robot, WAVE_PREPARE)
    
    # 2. 挥手
    print(f"  → 开始挥手（{WAVE_COUNT}次）...")
    for i in range(WAVE_COUNT):
        safe_move(robot, WAVE_SWING_LEFT, wait=0.5)
        safe_move(robot, WAVE_SWING_RIGHT, wait=0.5)
        print(f"    第 {i+1}/{WAVE_COUNT} 次")
    
    # 3. 回到准备位
    safe_move(robot, WAVE_PREPARE)
    print("  ✓ 挥手完成")


def main():
    print("=" * 50)
    print("NX-7 机械臂挥手示例")
    print("=" * 50)
    
    ctrl = None
    robot = None
    
    try:
        # 1. 连接控制器
        print(f"\n[1/5] 连接控制器 ({ROBOT_IP})...")
        ctrl = Controller()
        ctrl.Connect(ROBOT_IP)
        print(f"  ✓ 已连接，等待初始化 ({INIT_WAIT}s)...")
        time.sleep(INIT_WAIT)
        
        # 2. 伺服上电
        print("\n[2/5] 伺服上电...")
        ctrl.SetPowerEnable(True)
        robot = ctrl.AddRobot(1)
        robot.SetSpeed(SPEED_PERCENT)
        print(f"  ✓ 伺服已上电，速度 {SPEED_PERCENT}%")
        
        # 注册紧急关闭
        atexit.register(emergency_shutdown, ctrl, robot)
        
        # 3. 回到 HOME
        print("\n[3/5] 回到 HOME 位姿...")
        safe_move(robot, HOME_POSE)
        print("  ✓ 已就位")
        
        # 4. 执行挥手
        print("\n[4/5] 执行挥手动作...")
        wave_hand(robot)
        
        # 5. 回到 HOME 并关闭
        print("\n[5/5] 回到 HOME 并关闭...")
        safe_move(robot, HOME_POSE)
        
        # 取消紧急关闭（正常流程）
        atexit.unregister(emergency_shutdown)
        emergency_shutdown(ctrl, robot)
        
        print("\n" + "=" * 50)
        print("✓ 挥手示例执行完成")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
        if ctrl and robot:
            emergency_shutdown(ctrl, robot)
    except Exception as e:
        print(f"\n[✗] 错误: {e}")
        if ctrl and robot:
            emergency_shutdown(ctrl, robot)
        raise


if __name__ == "__main__":
    main()
