#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机械臂控制器模块
基于 PallasSDK 的机械臂控制封装

功能:
- 机械臂连接/断开
- 关节运动控制
- 夹爪控制
- 挥手动作
- 迎宾动作
"""

import time
import threading
from typing import List, Optional, Callable
from enum import Enum


class ArmState(Enum):
    """机械臂状态"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    READY = "ready"
    MOVING = "moving"
    ERROR = "error"


class ArmController:
    """
    机械臂控制器
    
    使用 PallasSDK 控制 6 轴机械臂
    """
    
    # 夹爪串口命令
    GRIPPER_OPEN_CMD = "55AA011409011400140014008403320032003200320064000E"
    GRIPPER_CLOSE_CMD = "55AA011409014C044C044C04840332003200320032006400C2"
    
    # 默认 IP
    DEFAULT_IP = "192.168.3.100"
    
    # 安全角度限制 (度)
    JOINT_LIMITS = [
        (-170, 170),   # J1
        (-120, 120),   # J2
        (-150, 150),   # J3
        (-180, 180),   # J4
        (-120, 120),   # J5
        (-360, 360),   # J6
    ]
    
    # 迎宾/挥手动作配置
    WAVE_ACTION = {
        "name": "挥手",
        "poses": [
            # 起始位置 (复位)
            [0, 0, 0, 0, 0, 0],
            # 举起手臂
            [0, -30, -60, 0, -90, 0],
            # 挥手位置1
            [20, -30, -60, 0, -90, 0],
            # 挥手位置2
            [-20, -30, -60, 0, -90, 0],
            # 挥手位置1
            [20, -30, -60, 0, -90, 0],
            # 挥手位置2
            [-20, -30, -60, 0, -90, 0],
            # 复位
            [0, 0, 0, 0, 0, 0],
        ],
        "speed": 15,
        "delay": 0.5
    }
    
    WELCOME_ACTION = {
        "name": "欢迎",
        "poses": [
            # 起始位置
            [0, 0, 0, 0, 0, 0],
            # 举起手臂示意
            [0, -45, -30, 0, -60, 0],
            # 点头示意
            [0, -30, -45, 0, -60, 0],
            # 复位
            [0, 0, 0, 0, 0, 0],
        ],
        "speed": 10,
        "delay": 1.0
    }
    
    def __init__(self, ip: str = DEFAULT_IP, enable_gripper: bool = True):
        """
        初始化机械臂控制器
        
        Args:
            ip: 机械臂控制器 IP 地址
            enable_gripper: 是否启用夹爪
        """
        self.ip = ip
        self.enable_gripper = enable_gripper
        
        # PallasSDK 组件
        self.ctrl = None
        self.robot = None
        self.serial_name = "COM2"
        
        # 状态
        self.state = ArmState.DISCONNECTED
        self.current_joint_pos = [0.0] * 6
        self.is_moving = False
        
        # 回调
        self.on_state_change: Optional[Callable[[ArmState], None]] = None
        self.on_position_update: Optional[Callable[[List[float]], None]] = None
        
        # 执行线程
        self._action_thread: Optional[threading.Thread] = None
        self._stop_action = threading.Event()
        
        print(f"[机械臂] 控制器初始化，目标IP: {ip}")
    
    def connect(self) -> bool:
        """
        连接机械臂
        
        Returns:
            是否连接成功
        """
        try:
            # 延迟导入 PallasSDK (避免启动时加载)
            from PallasSDK import Controller, HiddenDataType
            
            self._set_state(ArmState.CONNECTING)
            print(f"[机械臂] 正在连接 {self.ip}...")
            
            # 创建控制器
            self.ctrl = Controller()
            
            # 设置回调
            self.ctrl.SetHiddenCallback(self._hidden_callback)
            
            # 连接
            self.ctrl.Connect(self.ip)
            
            # 开启关节位置反馈
            self.ctrl.SetHiddenOn(HiddenDataType.RobotJointPos)
            
            # 打开串口 (夹爪)
            if self.enable_gripper:
                try:
                    from PallasSDK import ComPort
                    self.ctrl.ComOpen(
                        self.serial_name,
                        ComPort.Com_485,
                        115200, 8, 1, 0, True
                    )
                    print("[机械臂] 夹爪串口已打开")
                except Exception as e:
                    print(f"[机械臂] 夹爪连接失败: {e}")
            
            # 伺服上电
            self.ctrl.SetPowerEnable(True)
            time.sleep(0.5)
            
            # 添加机器人
            self.robot = self.ctrl.AddRobot(1)
            self.robot.SetFrameType(1)  # 轴坐标
            
            self._set_state(ArmState.READY)
            print("[机械臂] 连接成功，已就绪")
            return True
            
        except Exception as e:
            self._set_state(ArmState.ERROR)
            print(f"[机械臂] 连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.ctrl is None:
            return
        
        try:
            # 停止当前动作
            self.stop_action()
            
            # 伺服下电
            self.ctrl.SetPowerEnable(False)
            
            # 关闭串口
            if self.enable_gripper:
                try:
                    self.ctrl.ComClose(self.serial_name)
                except:
                    pass
            
            self.ctrl = None
            self.robot = None
            
            self._set_state(ArmState.DISCONNECTED)
            print("[机械臂] 已断开连接")
            
        except Exception as e:
            print(f"[机械臂] 断开连接时出错: {e}")
    
    def _hidden_callback(self, type, robot, data):
        """SDK 回调函数"""
        # RobotJointPos = 1 (根据 SDK 文档)
        if type == 1 and data and len(data) >= 6:
            self.current_joint_pos = [float(i) for i in data[:6]]
            if self.on_position_update:
                self.on_position_update(self.current_joint_pos)
    
    def _set_state(self, state: ArmState):
        """设置状态"""
        if self.state != state:
            self.state = state
            if self.on_state_change:
                self.on_state_change(state)
    
    def move_joints(self, angles: List[float], speed: int = 10, wait: bool = True) -> bool:
        """
        移动关节
        
        Args:
            angles: 6个关节角度 [J1, J2, J3, J4, J5, J6]
            speed: 速度百分比 (1-100)
            wait: 是否等待完成
            
        Returns:
            是否成功
        """
        if self.state != ArmState.READY or self.robot is None:
            print("[机械臂] 未就绪，无法移动")
            return False
        
        # 检查并限制角度
        safe_angles = []
        for i, angle in enumerate(angles[:6]):
            min_val, max_val = self.JOINT_LIMITS[i]
            safe_angle = max(min_val, min(max_val, angle))
            safe_angles.append(safe_angle)
        
        try:
            from PallasSDK import LocationJ
            
            self.is_moving = True
            self._set_state(ArmState.MOVING)
            
            # 设置速度
            self.robot.SetSpeed(speed)
            
            # 执行运动
            self.robot.MoveJ(LocationJ(*safe_angles))
            
            if wait:
                # 简单延时等待 (实际应该检查运动完成状态)
                time.sleep(0.5)
            
            self.is_moving = False
            self._set_state(ArmState.READY)
            return True
            
        except Exception as e:
            self.is_moving = False
            self._set_state(ArmState.ERROR)
            print(f"[机械臂] 运动失败: {e}")
            return False
    
    def move_to_home(self, speed: int = 10) -> bool:
        """
        回到初始位置
        
        Args:
            speed: 速度
            
        Returns:
            是否成功
        """
        print("[机械臂] 回到初始位置...")
        return self.move_joints([0, 0, 0, 0, 0, 0], speed)
    
    def gripper_open(self) -> bool:
        """张开夹爪"""
        if not self.enable_gripper or self.ctrl is None:
            return False
        
        try:
            self.ctrl.ComSend(self.serial_name, self.GRIPPER_OPEN_CMD)
            print("[机械臂] 夹爪已张开")
            return True
        except Exception as e:
            print(f"[机械臂] 夹爪控制失败: {e}")
            return False
    
    def gripper_close(self) -> bool:
        """闭合夹爪"""
        if not self.enable_gripper or self.ctrl is None:
            return False
        
        try:
            self.ctrl.ComSend(self.serial_name, self.GRIPPER_CLOSE_CMD)
            print("[机械臂] 夹爪已闭合")
            return True
        except Exception as e:
            print(f"[机械臂] 夹爪控制失败: {e}")
            return False
    
    def execute_action(self, action_name: str, blocking: bool = False) -> bool:
        """
        执行预设动作
        
        Args:
            action_name: 动作名称 ("wave", "welcome")
            blocking: 是否阻塞等待完成
            
        Returns:
            是否成功
        """
        if action_name == "wave":
            action = self.WAVE_ACTION
        elif action_name == "welcome":
            action = self.WELCOME_ACTION
        else:
            print(f"[机械臂] 未知动作: {action_name}")
            return False
        
        print(f"[机械臂] 执行动作: {action['name']}")
        
        if blocking:
            return self._run_action(action)
        else:
            # 后台执行
            self._stop_action.clear()
            self._action_thread = threading.Thread(
                target=self._run_action,
                args=(action,),
                daemon=True
            )
            self._action_thread.start()
            return True
    
    def _run_action(self, action: dict) -> bool:
        """
        运行动作序列
        
        Args:
            action: 动作配置字典
            
        Returns:
            是否成功
        """
        poses = action["poses"]
        speed = action["speed"]
        delay = action["delay"]
        
        for i, pose in enumerate(poses):
            if self._stop_action.is_set():
                print("[机械臂] 动作被中断")
                return False
            
            print(f"[机械臂] 动作 {i+1}/{len(poses)}: {pose}")
            
            if not self.move_joints(pose, speed, wait=True):
                return False
            
            # 等待
            time.sleep(delay)
        
        print(f"[机械臂] 动作 '{action['name']}' 完成")
        return True
    
    def stop_action(self):
        """停止当前动作"""
        self._stop_action.set()
        if self._action_thread and self._action_thread.is_alive():
            self._action_thread.join(timeout=2.0)
    
    def wave_hand(self) -> bool:
        """挥手 (便捷方法)"""
        return self.execute_action("wave", blocking=False)
    
    def welcome_guest(self) -> bool:
        """欢迎动作 (便捷方法)"""
        return self.execute_action("welcome", blocking=False)
    
    def is_ready(self) -> bool:
        """是否就绪"""
        return self.state == ArmState.READY and not self.is_moving
    
    def get_state(self) -> ArmState:
        """获取当前状态"""
        return self.state
    
    def get_joint_positions(self) -> List[float]:
        """获取当前关节角度"""
        return self.current_joint_pos.copy()


class MockArmController(ArmController):
    """
    模拟机械臂控制器 (用于测试)
    """
    
    def __init__(self, ip: str = "127.0.0.1", enable_gripper: bool = True):
        # 不调用父类 __init__，避免导入 PallasSDK
        self.ip = ip
        self.enable_gripper = enable_gripper
        self.state = ArmState.DISCONNECTED
        self.current_joint_pos = [0.0] * 6
        self.is_moving = False
        self.on_state_change = None
        self.on_position_update = None
        self._action_thread = None
        self._stop_action = threading.Event()
        
        print(f"[模拟机械臂] 控制器初始化 (测试模式)")
    
    def connect(self) -> bool:
        """模拟连接"""
        self._set_state(ArmState.READY)
        print("[模拟机械臂] 连接成功 (模拟模式)")
        return True
    
    def disconnect(self):
        """模拟断开"""
        self._set_state(ArmState.DISCONNECTED)
        print("[模拟机械臂] 已断开")
    
    def move_joints(self, angles: List[float], speed: int = 10, wait: bool = True) -> bool:
        """模拟移动"""
        self.is_moving = True
        self._set_state(ArmState.MOVING)
        
        print(f"[模拟机械臂] 移动到: {angles}, 速度: {speed}%")
        time.sleep(0.5)  # 模拟运动时间
        
        self.current_joint_pos = angles.copy()
        self.is_moving = False
        self._set_state(ArmState.READY)
        return True
    
    def gripper_open(self) -> bool:
        """模拟张开"""
        print("[模拟机械臂] 夹爪已张开 (模拟)")
        return True
    
    def gripper_close(self) -> bool:
        """模拟闭合"""
        print("[模拟机械臂] 夹爪已闭合 (模拟)")
        return True


if __name__ == "__main__":
    # 测试模拟控制器
    print("=" * 50)
    print("机械臂控制器测试")
    print("=" * 50)
    
    # 使用模拟模式 (无需真实机械臂)
    arm = MockArmController()
    
    if arm.connect():
        print("\n执行欢迎动作...")
        arm.welcome_guest()
        time.sleep(3)
        
        print("\n执行挥手动作...")
        arm.wave_hand()
        time.sleep(4)
        
        print("\n回到初始位置...")
        arm.move_to_home()
        
        arm.disconnect()
    
    print("\n测试完成!")
