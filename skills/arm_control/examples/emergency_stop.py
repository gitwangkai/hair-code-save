#!/usr/bin/env python3
"""
紧急停止和故障恢复示例

功能：演示异常处理、紧急停止和恢复机制
场景：
    - 用户中断 (Ctrl+C)
    - 关节超限错误
    - 通信超时
    - 未知异常

使用：
    python3 emergency_stop.py

安全特性：
    - 多层异常捕获
    - 强制回位机制
    - 超时保护
    - 状态检查
"""
import time
import atexit
import signal
import sys
from PallasSDK import Controller, LocationJ

# ==================== 配置 ====================
ROBOT_IP = "192.168.3.100"
INIT_WAIT = 30
SPEED_PERCENT = 10
SAFE_POSE = [0.0, 10.0, 0.0, 30.0, 0.0, 0.0]

# ==================== 关节限位 ====================
JOINT_LIMITS = {
    "J1": (-70.0, 200.0), "J2": (0.0, 120.0), "J3": (-55.0, 55.0),
    "J4": (0.0, 120.0), "J5": (-85.0, 85.0), "J6": (-20.0, 20.0),
}


class SafeArmController:
    """带完整安全机制的机械臂控制器"""
    
    def __init__(self, ip=ROBOT_IP):
        self.ctrl = Controller()
        self.robot = None
        self.ip = ip
        self.connected = False
        self.emergency_triggered = False
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """信号处理：捕获 Ctrl+C 等中断信号"""
        signame = signal.Signals(signum).name
        print(f"\n[!] 收到信号: {signame}")
        self.emergency_stop("用户中断")
        sys.exit(0)
    
    def connect(self):
        """连接机械臂"""
        print(f"  → 连接控制器 ({self.ip})...")
        try:
            self.ctrl.Connect(self.ip)
        except Exception as e:
            raise ConnectionError(f"连接失败: {e}")
        
        print(f"  → 等待初始化 ({INIT_WAIT}s)...")
        time.sleep(INIT_WAIT)
        
        print("  → 伺服上电...")
        try:
            self.ctrl.SetPowerEnable(True)
        except Exception as e:
            raise RuntimeError(f"伺服上电失败: {e}")
        
        self.robot = self.ctrl.AddRobot(1)
        self.robot.SetSpeed(SPEED_PERCENT)
        self.connected = True
        
        # 注册退出钩子
        atexit.register(self._cleanup)
        print("  ✓ 机械臂已就绪")
    
    def _cleanup(self):
        """清理函数（由 atexit 调用）"""
        if self.connected and not self.emergency_triggered:
            print("\n[!] 执行清理...")
            self.emergency_stop("程序退出")
    
    def emergency_stop(self, reason="未知原因"):
        """紧急停止：返回安全位姿并下电"""
        if self.emergency_triggered:
            return
        
        self.emergency_triggered = True
        print(f"\n[!] 紧急停止触发: {reason}")
        
        try:
            if self.robot:
                print("  → 移动到安全位姿...")
                self.robot.MoveJ(LocationJ(*SAFE_POSE))
                time.sleep(2)
        except Exception as e:
            print(f"  ✗ 移动失败: {e}")
        
        try:
            print("  → 伺服下电...")
            self.ctrl.SetPowerEnable(False)
            print("  ✓ 已安全关闭")
        except Exception as e:
            print(f"  ✗ 下电失败: {e}")
        
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
    
    def move(self, angles, desc="", wait=1.0):
        """安全移动"""
        if self.emergency_triggered:
            print(f"  ✗ [跳过] 紧急停止已触发")
            return False
        
        ok, msg = self.check_limits(angles)
        if not ok:
            print(f"  ✗ [限位错误] {msg}")
            self.emergency_stop("关节超限")
            return False
        
        desc_str = f" ({desc})" if desc else ""
        print(f"  → 移动{desc_str}...")
        
        try:
            self.robot.MoveJ(LocationJ(*angles))
            time.sleep(wait)
            return True
        except Exception as e:
            print(f"  ✗ [运动失败] {e}")
            self.emergency_stop("运动异常")
            return False


def demo_normal_operation():
    """正常操作流程"""
    print("\n" + "=" * 50)
    print("场景 1: 正常操作流程")
    print("=" * 50)
    
    arm = SafeArmController()
    
    try:
        print("\n[连接]")
        arm.connect()
        
        print("\n[执行动作序列]")
        arm.move([0, 30, 0, 60, 0, 0], "准备位")
        arm.move([0, 60, 0, 90, 0, 0], "工作位")
        arm.move([0, 30, 0, 60, 0, 0], "准备位")
        arm.move([0, 0, 0, 0, 0, 0], "HOME位")
        
        print("\n[正常完成]")
        arm.emergency_stop("正常完成")  # 这会安全关闭
        
    except Exception as e:
        print(f"\n[✗] 异常: {e}")
        arm.emergency_stop(f"异常: {e}")


def demo_user_interrupt():
    """用户中断演示"""
    print("\n" + "=" * 50)
    print("场景 2: 用户中断 (按 Ctrl+C)")
    print("=" * 50)
    
    arm = SafeArmController()
    
    try:
        print("\n[连接]")
        arm.connect()
        
        print("\n[执行长时动作...]")
        print("  (按 Ctrl+C 模拟用户中断)")
        
        for i in range(10):
            print(f"  步骤 {i+1}/10...")
            arm.move([0, 30 + i*5, 0, 60 + i*3, 0, 0], f"步骤 {i+1}")
            time.sleep(0.5)
        
        arm.emergency_stop("正常完成")
        
    except KeyboardInterrupt:
        print("\n[!] 主循环捕获中断")
        arm.emergency_stop("用户中断")


def demo_joint_limit_error():
    """关节超限错误演示"""
    print("\n" + "=" * 50)
    print("场景 3: 关节超限错误处理")
    print("=" * 50)
    
    arm = SafeArmController()
    
    try:
        print("\n[连接]")
        arm.connect()
        
        print("\n[执行安全动作]")
        arm.move([0, 30, 0, 60, 0, 0], "安全位姿")
        
        print("\n[尝试超限动作]")
        print("  → 目标: J2=150° (限位: 0-120°)")
        result = arm.move([0, 150, 0, 60, 0, 0], "超限位姿")
        
        if not result:
            print("  ✓ 限位检查正常工作")
        
        print("\n[恢复]")
        arm.move([0, 0, 0, 0, 0, 0], "HOME位")
        arm.emergency_stop("正常完成")
        
    except Exception as e:
        print(f"\n[✗] 异常: {e}")
        arm.emergency_stop(f"异常: {e}")


def demo_timeout_recovery():
    """超时恢复演示"""
    print("\n" + "=" * 50)
    print("场景 4: 超时保护")
    print("=" * 50)
    
    arm = SafeArmController()
    
    def timeout_handler(signum, frame):
        raise TimeoutError("操作超时")
    
    try:
        print("\n[连接]")
        
        # 设置超时
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)  # 10秒超时
        
        arm.connect()
        signal.alarm(0)  # 取消超时
        
        print("\n[执行动作]")
        arm.move([0, 30, 0, 60, 0, 0], "准备位", wait=0.5)
        arm.move([0, 0, 0, 0, 0, 0], "HOME位", wait=0.5)
        
        arm.emergency_stop("正常完成")
        
    except TimeoutError as e:
        print(f"\n[!] 超时: {e}")
        arm.emergency_stop("连接超时")
    except Exception as e:
        print(f"\n[✗] 异常: {e}")
        arm.emergency_stop(f"异常: {e}")


def demo_graceful_degradation():
    """优雅降级演示"""
    print("\n" + "=" * 50)
    print("场景 5: 优雅降级")
    print("=" * 50)
    
    arm = SafeArmController()
    
    try:
        print("\n[连接]")
        arm.connect()
        
        print("\n[执行动作序列（允许失败）]")
        poses = [
            ([0, 30, 0, 60, 0, 0], "准备位"),
            ([0, 60, 0, 90, 0, 0], "工作位"),
            ([0, 200, 0, 90, 0, 0], "超限位（将失败）"),  # 这会失败
            ([0, 30, 0, 60, 0, 0], "恢复位"),
        ]
        
        for angles, desc in poses:
            success = arm.move(angles, desc)
            if not success:
                print(f"  [!] 动作 '{desc}' 失败，尝试恢复...")
                if not arm.emergency_triggered:
                    arm.move([0, 10, 0, 30, 0, 0], "安全位")
                break
        
        if not arm.emergency_triggered:
            arm.move([0, 0, 0, 0, 0, 0], "HOME位")
            arm.emergency_stop("正常完成")
        
    except Exception as e:
        print(f"\n[✗] 异常: {e}")
        arm.emergency_stop(f"异常: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("紧急停止和故障恢复示例")
    print("=" * 50)
    
    print("\n可用场景:")
    print("  1. 正常操作流程")
    print("  2. 用户中断 (Ctrl+C)")
    print("  3. 关节超限错误")
    print("  4. 超时保护")
    print("  5. 优雅降级")
    print("  6. 运行所有场景")
    
    choice = input("\n选择场景 (1-6): ").strip()
    
    if choice == "1":
        demo_normal_operation()
    elif choice == "2":
        demo_user_interrupt()
    elif choice == "3":
        demo_joint_limit_error()
    elif choice == "4":
        demo_timeout_recovery()
    elif choice == "5":
        demo_graceful_degradation()
    elif choice == "6":
        demo_normal_operation()
        demo_joint_limit_error()
        demo_graceful_degradation()
        print("\n[跳过后续场景，请单独运行以体验中断]")
    else:
        print("无效选择")
