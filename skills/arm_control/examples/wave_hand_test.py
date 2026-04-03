#!/usr/bin/env python3
"""
挥手动作测试（优化版）

功能：测试挥手动作并确保回到 HOME 位
流程：连接 → HOME → 挥手 → HOME → 断开

使用：
    python3 wave_hand_test.py
"""
import time
import atexit
import signal
import sys
from PallasSDK import Controller, LocationJ

ROBOT_IP = "192.168.3.100"
HOME_POSE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
TUCK_POSE = [0.0, 10.0, 0.0, 30.0, 0.0, 0.0]
WAVE_PREPARE = [64.3, 0, 13.2, 85.9, -84.8, 0]

JOINT_LIMITS = {
    "J1": (-70.0, 200.0), "J2": (0.0, 120.0), "J3": (-55.0, 55.0),
    "J4": (0.0, 120.0), "J5": (-85.0, 85.0), "J6": (-20.0, 20.0),
}


def check_limits(angles):
    for i, (name, (lo, hi)) in enumerate(JOINT_LIMITS.items()):
        if not (lo <= angles[i] <= hi):
            return False, f"{name} 超限: {angles[i]}"
    return True, "OK"


def safe_move(robot, angles, wait=1.0):
    ok, msg = check_limits(angles)
    if not ok:
        print(f"  ✗ [限位] {msg}")
        return False
    robot.MoveJ(LocationJ(*angles))
    time.sleep(wait)
    return True


def main():
    print("=" * 50)
    print("机械臂挥手测试")
    print("=" * 50)
    
    ctrl = None
    robot = None
    
    def shutdown():
        """确保回到安全状态"""
        if ctrl and robot:
            print("\n[!] 执行安全关闭...")
            try:
                # 强制回到 HOME
                print("  → 回到 HOME...")
                robot.MoveJ(LocationJ(*HOME_POSE))
                time.sleep(2)
            except:
                pass
            try:
                ctrl.SetPowerEnable(False)
                print("  ✓ 已下电")
            except:
                pass
    
    # 注册退出钩子
    atexit.register(shutdown)
    
    try:
        # 1. 连接
        print(f"\n[1/6] 连接控制器 ({ROBOT_IP})...")
        ctrl = Controller()
        ctrl.Connect(ROBOT_IP)
        print("  ✓ 已连接")
        
        # 2. 初始化
        print(f"\n[2/6] 初始化 (30s)...")
        for i in range(30):
            time.sleep(1)
            if i % 5 == 0:
                print(f"  ... {i}s")
        print("  ✓ 初始化完成")
        
        # 3. 上电
        print("\n[3/6] 伺服上电...")
        ctrl.SetPowerEnable(True)
        robot = ctrl.AddRobot(1)
        robot.SetSpeed(10)
        print("  ✓ 已就绪")
        
        # 4. 回到 HOME
        print("\n[4/6] 回到 HOME...")
        if safe_move(robot, HOME_POSE, wait=2):
            print("  ✓ 已就位")
        
        # 5. 挥手动作
        print("\n[5/6] 执行挥手...")
        print("  → 移动到准备位...")
        if safe_move(robot, WAVE_PREPARE, wait=1.5):
            print("  → 挥手 3 次...")
            for i in range(3):
                # 左摆
                left = [x + o for x, o in zip(WAVE_PREPARE, [0, 0, 10, 0, 0, 0])]
                safe_move(robot, left, wait=0.6)
                # 右摆
                right = [x + o for x, o in zip(WAVE_PREPARE, [0, 0, -10, 0, 0, 0])]
                safe_move(robot, right, wait=0.6)
                print(f"    第 {i+1}/3 次")
            # 回到准备位
            safe_move(robot, WAVE_PREPARE, wait=1)
            print("  ✓ 挥手完成")
        
        # 6. 回到 HOME 并关闭
        print("\n[6/6] 回到 HOME 并关闭...")
        safe_move(robot, HOME_POSE, wait=2)
        
        # 取消钩子，手动关闭
        atexit.unregister(shutdown)
        shutdown()
        
        print("\n" + "=" * 50)
        print("✓ 挥手测试完成！")
        print("=" * 50)
        return 0
        
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
        return 1
    except Exception as e:
        print(f"\n[✗] 错误: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
