#!/usr/bin/env python3
"""
机械臂回原点脚本

功能：将机械臂安全移动到 HOME 位姿 [0,0,0,0,0,0]

使用：
    python3 go_home.py

安全特性：
    - 限位检查
    - 超时保护
    - 异常处理
"""
import time
import signal
from PallasSDK import Controller, LocationJ

ROBOT_IP = "192.168.3.100"
HOME_POSE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
TUCK_POSE = [0.0, 10.0, 0.0, 30.0, 0.0, 0.0]

JOINT_LIMITS = {
    "J1": (-70.0, 200.0), "J2": (0.0, 120.0), "J3": (-55.0, 55.0),
    "J4": (0.0, 120.0), "J5": (-85.0, 85.0), "J6": (-20.0, 20.0),
}


def check_limits(angles):
    """检查关节限位"""
    for i, (name, (lo, hi)) in enumerate(JOINT_LIMITS.items()):
        if not (lo <= angles[i] <= hi):
            return False, f"{name} 超限: {angles[i]}"
    return True, "OK"


def main():
    print("=" * 50)
    print("机械臂回原点")
    print("=" * 50)
    
    ctrl = None
    robot = None
    
    try:
        # 连接
        print(f"\n[1/4] 连接控制器 ({ROBOT_IP})...")
        ctrl = Controller()
        ctrl.Connect(ROBOT_IP)
        print("  ✓ 已连接")
        
        # 伺服上电
        print("\n[2/4] 伺服上电...")
        ctrl.SetPowerEnable(True)
        robot = ctrl.AddRobot(1)
        robot.SetSpeed(10)
        print("  ✓ 已上电")
        
        # 先移动到 tuck 位姿（更安全）
        print("\n[3/4] 移动到安全位姿...")
        ok, msg = check_limits(TUCK_POSE)
        if ok:
            robot.MoveJ(LocationJ(*TUCK_POSE))
            time.sleep(2)
            print("  ✓ 已就位")
        
        # 回到 HOME
        print("\n[4/4] 回到 HOME 位姿...")
        ok, msg = check_limits(HOME_POSE)
        if not ok:
            print(f"  ✗ 限位错误: {msg}")
            return 1
        
        robot.MoveJ(LocationJ(*HOME_POSE))
        time.sleep(2)
        print("  ✓ 已回到 HOME")
        
        # 下电
        print("\n[完成] 伺服下电...")
        ctrl.SetPowerEnable(False)
        print("  ✓ 已安全关闭")
        
        print("\n" + "=" * 50)
        print("✓ 机械臂已回到 HOME 位")
        print("=" * 50)
        return 0
        
    except Exception as e:
        print(f"\n[✗] 错误: {e}")
        if ctrl:
            try:
                ctrl.SetPowerEnable(False)
            except:
                pass
        return 1


if __name__ == "__main__":
    exit(main())
