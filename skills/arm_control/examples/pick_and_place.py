#!/usr/bin/env python3
"""
抓取-放置示例

功能：演示完整的抓取-移动-放置流程
流程：准备 → 抓取 → 提起 → 移动 → 放置 → 返回

使用：
    python3 pick_and_place.py

安全特性：
    - 完整的限位检查
    - 分阶段移动，避免碰撞
    - 异常自动回位
"""
import time
import atexit
from PallasSDK import Controller, LocationJ

# ==================== 配置 ====================
ROBOT_IP = "192.168.3.100"
INIT_WAIT = 30
SPEED_PERCENT = 10
MOVE_WAIT = 1.5

# ==================== 预设位姿 ====================
POSES = {
    "home":     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "tuck":     [0.0, 10.0, 0.0, 30.0, 0.0, 0.0],
    "ready":    [0.0, 30.0, 0.0, 60.0, 0.0, 0.0],
    "grasp":    [0.0, 90.0, 0.0, 90.0, 0.0, 0.0],
    "handover": [0.0, 60.0, 0.0, 80.0, 0.0, 0.0],
    "lift":     [0.0, 45.0, 0.0, 75.0, 0.0, 0.0],
}

# ==================== 关节限位 ====================
JOINT_LIMITS = {
    "J1": (-70.0, 200.0), "J2": (0.0, 120.0), "J3": (-55.0, 55.0),
    "J4": (0.0, 120.0), "J5": (-85.0, 85.0), "J6": (-20.0, 20.0),
}


class ArmController:
    """机械臂控制封装类"""
    
    def __init__(self, ip=ROBOT_IP):
        self.ctrl = Controller()
        self.robot = None
        self.ip = ip
        self.connected = False
    
    def connect(self):
        """连接机械臂"""
        print(f"  → 连接控制器 ({self.ip})...")
        self.ctrl.Connect(self.ip)
        print(f"  → 等待初始化 ({INIT_WAIT}s)...")
        time.sleep(INIT_WAIT)
        
        print("  → 伺服上电...")
        self.ctrl.SetPowerEnable(True)
        self.robot = self.ctrl.AddRobot(1)
        self.robot.SetSpeed(SPEED_PERCENT)
        
        self.connected = True
        print("  ✓ 机械臂已就绪")
    
    def disconnect(self):
        """安全断开连接"""
        if not self.connected:
            return
        print("\n[断开连接]")
        try:
            self.move_to("tuck", "安全位姿")
            time.sleep(2)
            self.ctrl.SetPowerEnable(False)
            print("  ✓ 已安全关闭")
        except Exception as e:
            print(f"  ✗ 关闭失败: {e}")
        self.connected = False
    
    def check_limits(self, angles):
        """检查关节限位"""
        limits = list(JOINT_LIMITS.values())
        keys = list(JOINT_LIMITS.keys())
        for i, angle in enumerate(angles):
            lo, hi = limits[i]
            if not (lo <= angle <= hi):
                return False, f"{keys[i]} 超限: {angle:.1f}° (范围 [{lo}, {hi}])"
        return True, "OK"
    
    def move_to(self, pose_name, desc=""):
        """移动到预设位姿"""
        if pose_name not in POSES:
            raise ValueError(f"未知位姿: {pose_name}")
        
        angles = POSES[pose_name]
        ok, msg = self.check_limits(angles)
        if not ok:
            print(f"  ✗ [限位错误] {msg}")
            return False
        
        desc_str = f" ({desc})" if desc else ""
        print(f"  → 移动到 [{pose_name}]{desc_str}...")
        self.robot.MoveJ(LocationJ(*angles))
        time.sleep(MOVE_WAIT)
        return True
    
    def move_joints(self, angles, desc=""):
        """移动到指定关节角度"""
        ok, msg = self.check_limits(angles)
        if not ok:
            print(f"  ✗ [限位错误] {msg}")
            return False
        
        desc_str = f" ({desc})" if desc else ""
        print(f"  → 移动{desc_str}...")
        self.robot.MoveJ(LocationJ(*angles))
        time.sleep(MOVE_WAIT)
        return True


def demo_pick_and_place():
    """抓取-放置演示"""
    print("=" * 50)
    print("抓取-放置演示")
    print("=" * 50)
    
    arm = ArmController()
    
    try:
        # 1. 连接
        print("\n[1/6] 连接机械臂...")
        arm.connect()
        atexit.register(arm.disconnect)
        
        # 2. 准备姿态
        print("\n[2/6] 进入准备姿态...")
        arm.move_to("ready", "交互准备")
        
        # 3. 移动到抓取位
        print("\n[3/6] 移动到抓取位...")
        arm.move_to("grasp", "抓取高度")
        
        # 4. 抓取（模拟）
        print("\n[4/6] 执行抓取...")
        print("  → [夹爪控制] 闭合夹爪")
        time.sleep(1)
        print("  ✓ 抓取完成")
        
        # 5. 提起并移动
        print("\n[5/6] 提起物品...")
        arm.move_to("lift", "提升高度")
        arm.move_to("handover", "递送姿态")
        
        # 6. 放置
        print("\n[6/6] 执行放置...")
        arm.move_to("grasp", "放置高度")
        print("  → [夹爪控制] 张开夹爪")
        time.sleep(1)
        print("  ✓ 放置完成")
        
        # 7. 返回
        print("\n[清理] 返回安全位姿...")
        arm.move_to("ready", "待机姿态")
        arm.move_to("home", "HOME位姿")
        
        # 正常完成，取消紧急关闭
        atexit.unregister(arm.disconnect)
        arm.disconnect()
        
        print("\n" + "=" * 50)
        print("✓ 抓取-放置演示完成")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
        arm.disconnect()
    except Exception as e:
        print(f"\n[✗] 错误: {e}")
        arm.disconnect()
        raise


def demo_waypoint_motion():
    """路径点运动演示"""
    print("\n" + "=" * 50)
    print("路径点运动演示")
    print("=" * 50)
    
    arm = ArmController()
    
    try:
        print("\n[1/3] 连接机械臂...")
        arm.connect()
        atexit.register(arm.disconnect)
        
        print("\n[2/3] 执行路径点序列...")
        waypoints = [
            ([0, 30, 0, 60, 0, 0], "路径点 1"),
            ([30, 45, 10, 75, 0, 0], "路径点 2"),
            ([-30, 45, -10, 75, 0, 0], "路径点 3"),
            ([0, 60, 0, 90, 0, 0], "路径点 4"),
            ([0, 30, 0, 60, 0, 0], "路径点 5"),
        ]
        
        for angles, desc in waypoints:
            arm.move_joints(angles, desc)
        
        print("\n[3/3] 返回 HOME...")
        arm.move_to("home")
        
        atexit.unregister(arm.disconnect)
        arm.disconnect()
        
        print("\n" + "=" * 50)
        print("✓ 路径点运动演示完成")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
        arm.disconnect()
    except Exception as e:
        print(f"\n[✗] 错误: {e}")
        arm.disconnect()
        raise


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "waypoint":
        demo_waypoint_motion()
    else:
        demo_pick_and_place()
        print("\n提示: 使用 'python3 pick_and_place.py waypoint' 运行路径点演示")
