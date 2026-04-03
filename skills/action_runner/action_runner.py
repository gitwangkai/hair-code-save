#!/usr/bin/env python3
"""
Action Runner - 复合动作执行器（稳定版 v2）

注意：为避免ROS2上下文问题，所有动作使用直接控制
"""
import sys
import time
import threading
import argparse
import yaml
import re
import math
from typing import Dict, List, Tuple, Callable, Union

# 全局变量
rclpy = None
Twist = None
Float32 = None

ACTIONS: Dict[str, Dict[str, Callable]] = {}


def register_action(module: str, name: str, func: Callable):
    if module not in ACTIONS:
        ACTIONS[module] = {}
    ACTIONS[module][name] = func


class ROS2Manager:
    """ROS2 管理器 - 单例"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
            cls._instance.node = None
            cls._instance.cmd_vel_pub = None
            cls._instance.head_pub = None
        return cls._instance
    
    def init(self):
        if self.initialized:
            return True
        
        try:
            global rclpy, Twist, Float32
            import rclpy as rclpy_mod
            from geometry_msgs.msg import Twist as TwistMsg
            from std_msgs.msg import Float32 as Float32Msg
            
            rclpy = rclpy_mod
            Twist = TwistMsg
            Float32 = Float32Msg
            
            rclpy.init()
            self.node = rclpy.create_node('action_runner')
            self.cmd_vel_pub = self.node.create_publisher(Twist, '/cmd_vel', 10)
            self.head_pub = self.node.create_publisher(Float32, '/target_head_position', 10)
            
            self.initialized = True
            print("[ROS2] 初始化完成")
            return True
        except Exception as e:
            print(f"[ROS2] 初始化失败: {e}")
            return False
    
    def shutdown(self):
        if not self.initialized:
            return
        
        try:
            if self.node:
                self.node.destroy_node()
            if rclpy and rclpy.ok():
                rclpy.shutdown()
        except:
            pass
        
        self.initialized = False
        self.node = None
        self.cmd_vel_pub = None
        self.head_pub = None
        print("[ROS2] 已关闭")
    
    def is_ok(self):
        return self.initialized and rclpy and rclpy.ok()
    
    def publish_cmd_vel(self, linear_x=0.0, angular_z=0.0, duration=0.0):
        """发布底盘速度"""
        if not self.is_ok():
            print("  ✗ ROS2未就绪")
            return
        
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.angular.z = float(angular_z)
        
        start = time.time()
        while time.time() - start < duration:
            self.cmd_vel_pub.publish(msg)
            time.sleep(0.1)
        
        # 停止
        self.cmd_vel_pub.publish(Twist())
    
    def publish_head(self, angle_rad, duration=0.5):
        """发布云台角度"""
        if not self.is_ok():
            print("  ✗ ROS2未就绪")
            return
        
        msg = Float32()
        msg.data = float(angle_rad)
        
        steps = int(duration * 20)
        for _ in range(steps):
            self.head_pub.publish(msg)
            time.sleep(0.05)


ros2_mgr = ROS2Manager()


# ========== 底盘动作 ==========
def run_forward(distance: float = 1.0, speed: float = 0.3):
    duration = distance / speed
    print(f"  前进{distance}米...")
    ros2_mgr.publish_cmd_vel(linear_x=speed, duration=duration)
    print(f"  ✓ 前进完成")


def run_backward(distance: float = 1.0, speed: float = 0.3):
    duration = distance / speed
    print(f"  后退{distance}米...")
    ros2_mgr.publish_cmd_vel(linear_x=-speed, duration=duration)
    print(f"  ✓ 后退完成")


def run_rotate(angle: float = 360, speed: float = 0.5):
    angle_rad = math.radians(angle)
    duration = abs(angle_rad) / speed
    
    print(f"  旋转{angle}度...")
    angular_z = speed if angle > 0 else -speed
    ros2_mgr.publish_cmd_vel(angular_z=angular_z, duration=duration)
    print(f"  ✓ 旋转完成")


def run_stop():
    ros2_mgr.publish_cmd_vel(duration=0.1)
    print("  ✓ 停止")


# ========== 云台动作（直接控制） ==========
def run_nod(times: int = 3):
    print(f"  点头{times}次...")
    
    LOOK_UP = -3.2
    LOOK_DOWN = -3.6
    CENTER = -3.35
    
    for i in range(times):
        ros2_mgr.publish_head(LOOK_DOWN, 0.3)
        time.sleep(0.2)
        ros2_mgr.publish_head(LOOK_UP, 0.3)
        time.sleep(0.2)
    
    ros2_mgr.publish_head(CENTER, 0.3)
    print("  ✓ 点头完成")


def run_up():
    print("  抬头...")
    ros2_mgr.publish_head(-3.1, 0.5)
    print("  ✓ 抬头完成")


def run_down():
    print("  低头...")
    ros2_mgr.publish_head(-3.6, 0.5)
    print("  ✓ 低头完成")


def run_center():
    print("  归中...")
    ros2_mgr.publish_head(-3.35, 0.5)
    print("  ✓ 归中完成")


# ========== 机械臂动作（简化版） ==========
def run_wave_simple():
    """
    挥手 - 由于PallasSDK与ROS2冲突，使用提示方式
    实际项目中应该使用独立的进程间通信
    """
    print("  挥手（提示）...")
    print("  [注意] 挥手需要独立执行: python3 /home/aidlux/human_detection/src/wave_hand_standalone.py")
    time.sleep(1)
    print("  ✓ 挥手提示完成")


def run_wait(seconds: float = 1.0):
    print(f"  等待{seconds}秒...")
    time.sleep(seconds)
    print("  ✓ 等待完成")


# 注册动作
register_action("chassis", "forward", run_forward)
register_action("chassis", "backward", run_backward)
register_action("chassis", "rotate", run_rotate)
register_action("chassis", "stop", run_stop)
register_action("head", "nod", run_nod)
register_action("head", "up", run_up)
register_action("head", "down", run_down)
register_action("head", "center", run_center)
register_action("arm", "wave", run_wave_simple)
register_action("util", "wait", run_wait)

# 简化名称
register_action("", "forward", run_forward)
register_action("", "backward", run_backward)
register_action("", "rotate", run_rotate)
register_action("", "stop", run_stop)
register_action("", "nod", run_nod)
register_action("", "up", run_up)
register_action("", "down", run_down)
register_action("", "center", run_center)
register_action("", "wave", run_wave_simple)
register_action("", "wait", run_wait)


class ActionRunner:
    def __init__(self):
        self.actions = ACTIONS
    
    def parse_cmd(self, cmd: str) -> List:
        actions = []
        cmd = cmd.strip()
        i = 0
        
        while i < len(cmd):
            while i < len(cmd) and cmd[i] in ' \t':
                i += 1
            if i >= len(cmd):
                break
            
            if cmd[i:].startswith('parallel('):
                start = i + 9
                depth = 1
                j = start
                while j < len(cmd) and depth > 0:
                    if cmd[j] == '(':
                        depth += 1
                    elif cmd[j] == ')':
                        depth -= 1
                    j += 1
                
                if depth == 0:
                    inner = cmd[start:j-1]
                    parallel_actions = []
                    for part in self._split_actions(inner):
                        action = self._parse_single_action(part.strip())
                        if action:
                            parallel_actions.append(action)
                    if parallel_actions:
                        actions.append(("parallel", parallel_actions))
                i = j
            else:
                j = i
                while j < len(cmd) and cmd[j] != ';':
                    j += 1
                
                action_str = cmd[i:j].strip()
                if action_str:
                    action = self._parse_single_action(action_str)
                    if action:
                        actions.append(action)
                i = j + 1
        
        return actions
    
    def _split_actions(self, cmd: str) -> List[str]:
        parts = []
        depth = 0
        start = 0
        for i, c in enumerate(cmd):
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            elif c == ',' and depth == 0:
                parts.append(cmd[start:i])
                start = i + 1
        parts.append(cmd[start:])
        return parts
    
    def _parse_single_action(self, action_str: str):
        action_str = action_str.strip()
        if not action_str:
            return None
        
        match = re.match(r'(\w+)\s*\((.*)\)', action_str)
        if not match:
            return ("", action_str, ())
        
        name = match.group(1)
        args_str = match.group(2).strip()
        
        args = []
        if args_str:
            for arg in args_str.split(','):
                arg = arg.strip()
                try:
                    if '.' in arg:
                        args.append(float(arg))
                    else:
                        args.append(int(arg))
                except ValueError:
                    args.append(arg)
        
        return ("", name, tuple(args))
    
    def run_action(self, action: Tuple):
        module, name, args = action
        
        func = None
        if module and module in self.actions and name in self.actions[module]:
            func = self.actions[module][name]
        elif name in self.actions.get("", {}):
            func = self.actions[""][name]
        
        if not func:
            print(f"  ✗ 未知动作: {name}")
            return False
        
        try:
            func(*args)
            return True
        except Exception as e:
            print(f"  ✗ 执行失败: {e}")
            return False
    
    def run_parallel(self, actions: List[Tuple]):
        threads = []
        for action in actions:
            t = threading.Thread(target=self.run_action, args=(action,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    
    def run(self, actions: List):
        for i, action in enumerate(actions, 1):
            if isinstance(action, tuple) and len(action) == 2 and action[0] == "parallel":
                print(f"\n【步骤{i}/{len(actions)}】并行执行:")
                for j, sub_action in enumerate(action[1], 1):
                    print(f"  动作{j}: {sub_action[1]}{sub_action[2]}")
                self.run_parallel(action[1])
            else:
                print(f"\n【步骤{i}/{len(actions)}】{action[1]}{action[2]}")
                self.run_action(action)
    
    def run_cmd(self, cmd: str):
        print("="*60)
        print("复合动作执行")
        print("="*60)
        print(f"命令: {cmd}")
        
        # 初始化
        if not ros2_mgr.init():
            print("✗ ROS2初始化失败")
            return
        
        try:
            actions = self.parse_cmd(cmd)
            if not actions:
                print("✗ 无有效动作")
                return
            
            self.run(actions)
            
            print("\n" + "="*60)
            print("✓ 复合动作全部完成！")
            print("="*60)
        except Exception as e:
            print(f"\n✗ 异常: {e}")
        finally:
            ros2_mgr.shutdown()


def main():
    parser = argparse.ArgumentParser(description='复合动作执行器')
    parser.add_argument('cmd', nargs='?', help='动作命令')
    parser.add_argument('--list', '-l', action='store_true', help='列出可用动作')
    
    args = parser.parse_args()
    
    if args.list:
        print("可用动作:")
        print("\n底盘:")
        print("  forward(distance)  - 前进")
        print("  backward(distance) - 后退")
        print("  rotate(angle)      - 旋转")
        print("  stop()             - 停止")
        print("\n云台:")
        print("  nod(times)         - 点头")
        print("  up()               - 抬头")
        print("  down()             - 低头")
        print("  center()           - 归中")
        print("\n机械臂:")
        print("  wave()             - 挥手（提示）")
        print("\n其他:")
        print("  wait(seconds)      - 等待")
        print("\n示例:")
        print('  python3 action_runner.py "forward(1); nod(1); rotate(360)"')
        print('  python3 action_runner.py "nod(3); forward(2); rotate(-90)"')
        return
    
    if args.cmd:
        runner = ActionRunner()
        runner.run_cmd(args.cmd)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
