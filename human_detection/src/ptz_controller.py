#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云台追踪控制器 (PTZ Controller)
支持水平和垂直方向的追踪控制
"""

import time
import threading
from typing import Optional, Tuple, Callable
from dataclasses import dataclass


@dataclass
class PTZPosition:
    """云台位置"""
    pan: float   # 水平角度 (-45 到 45 度)
    tilt: float  # 垂直角度 (-30 到 30 度)
    zoom: float  # 变焦 (0 到 1)


class PTZController:
    """
    云台控制器
    
    功能:
    - 目标追踪 (根据人体/人脸位置调整云台)
    - 平滑移动
    - 边界限制
    - 速度控制
    """
    
    def __init__(self, 
                 pan_range: Tuple[float, float] = (-45, 45),
                 tilt_range: Tuple[float, float] = (-30, 30),
                 smooth_factor: float = 0.3,
                 dead_zone: float = 0.05):
        """
        初始化云台控制器
        
        Args:
            pan_range: 水平角度范围 (最小, 最大)
            tilt_range: 垂直角度范围 (最小, 最大)
            smooth_factor: 平滑系数 (0-1, 越小越平滑)
            dead_zone: 死区比例 (画面中心多大范围内不移动)
        """
        self.pan_range = pan_range
        self.tilt_range = tilt_range
        self.smooth_factor = smooth_factor
        self.dead_zone = dead_zone
        
        # 当前位置
        self.current_pos = PTZPosition(0, 0, 0)
        self.target_pos = PTZPosition(0, 0, 0)
        
        # 控制参数
        self.frame_width = 640
        self.frame_height = 480
        self.frame_center = (320, 240)
        
        # 移动速度限制 (度/秒)
        self.max_pan_speed = 20.0
        self.max_tilt_speed = 15.0
        
        # 控制线程
        self._running = False
        self._control_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # 回调函数 (实际控制云台的接口)
        self.on_move: Optional[Callable[[float, float], None]] = None
        
        print(f"[云台] 控制器初始化完成")
        print(f"       水平范围: {pan_range[0]}° ~ {pan_range[1]}°")
        print(f"       垂直范围: {tilt_range[0]}° ~ {tilt_range[1]}°")
    
    def set_frame_size(self, width: int, height: int):
        """设置画面尺寸"""
        self.frame_width = width
        self.frame_height = height
        self.frame_center = (width // 2, height // 2)
    
    def calculate_target(self, 
                        target_center: Tuple[int, int],
                        target_size: Optional[Tuple[int, int]] = None) -> PTZPosition:
        """
        根据目标位置计算云台目标角度
        
        Args:
            target_center: 目标中心点 (x, y)
            target_size: 目标大小 (w, h)，用于变焦计算
            
        Returns:
            目标云台位置
        """
        cx, cy = target_center
        fx, fy = self.frame_center
        
        # 计算偏移比例 (-0.5 到 0.5)
        offset_x = (cx - fx) / self.frame_width
        offset_y = (cy - fy) / self.frame_height
        
        # 死区检查
        if abs(offset_x) < self.dead_zone:
            offset_x = 0
        if abs(offset_y) < self.dead_zone:
            offset_y = 0
        
        # 计算目标角度
        pan = -offset_x * (self.pan_range[1] - self.pan_range[0])
        tilt = offset_y * (self.tilt_range[1] - self.tilt_range[0])
        
        # 限制范围
        pan = max(self.pan_range[0], min(self.pan_range[1], pan))
        tilt = max(self.tilt_range[0], min(self.tilt_range[1], tilt))
        
        # 计算变焦 (保持目标占画面一定比例)
        zoom = 0
        if target_size:
            tw, th = target_size
            target_ratio = max(tw / self.frame_width, th / self.frame_height)
            # 目标占画面 30% 时 zoom 为 0，占 60% 时 zoom 为 1
            zoom = max(0, min(1, (target_ratio - 0.3) * 3.3))
        
        return PTZPosition(pan, tilt, zoom)
    
    def track_target(self, 
                    target_center: Tuple[int, int],
                    target_size: Optional[Tuple[int, int]] = None):
        """
        追踪目标 (更新目标位置)
        
        Args:
            target_center: 目标中心点
            target_size: 目标大小
        """
        target = self.calculate_target(target_center, target_size)
        
        with self._lock:
            self.target_pos = target
    
    def update(self, dt: float) -> Optional[Tuple[float, float]]:
        """
        更新云台位置 (平滑移动)
        
        Args:
            dt: 时间间隔 (秒)
            
        Returns:
            如果有移动，返回 (pan_delta, tilt_delta)，否则返回 None
        """
        with self._lock:
            target = self.target_pos
            current = self.current_pos
        
        # 计算差值
        pan_diff = target.pan - current.pan
        tilt_diff = target.tilt - current.tilt
        
        # 如果差值很小，不移动
        if abs(pan_diff) < 0.5 and abs(tilt_diff) < 0.5:
            return None
        
        # 平滑移动
        pan_move = pan_diff * self.smooth_factor
        tilt_move = tilt_diff * self.smooth_factor
        
        # 限制最大速度
        max_pan_move = self.max_pan_speed * dt
        max_tilt_move = self.max_tilt_speed * dt
        
        pan_move = max(-max_pan_move, min(max_pan_move, pan_move))
        tilt_move = max(-max_tilt_move, min(max_tilt_move, tilt_move))
        
        # 更新当前位置
        with self._lock:
            self.current_pos.pan += pan_move
            self.current_pos.tilt += tilt_move
        
        return (pan_move, tilt_move)
    
    def start(self):
        """启动控制线程"""
        if self._running:
            return
        
        self._running = True
        self._control_thread = threading.Thread(target=self._control_loop, daemon=True)
        self._control_thread.start()
        print("[云台] 控制线程已启动")
    
    def stop(self):
        """停止控制线程"""
        self._running = False
        if self._control_thread:
            self._control_thread.join(timeout=1.0)
        print("[云台] 控制线程已停止")
    
    def _control_loop(self):
        """控制循环"""
        last_time = time.time()
        
        while self._running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # 更新位置
            movement = self.update(dt)
            
            # 如果有移动，调用回调
            if movement and self.on_move:
                try:
                    self.on_move(self.current_pos.pan, self.current_pos.tilt)
                except Exception as e:
                    print(f"[云台] 移动回调错误: {e}")
            
            # 控制频率 (20Hz)
            time.sleep(0.05)
    
    def reset(self):
        """重置到初始位置"""
        with self._lock:
            self.target_pos = PTZPosition(0, 0, 0)
            self.current_pos = PTZPosition(0, 0, 0)
        print("[云台] 已重置到初始位置")
    
    def get_position(self) -> PTZPosition:
        """获取当前位置"""
        with self._lock:
            return PTZPosition(
                self.current_pos.pan,
                self.current_pos.tilt,
                self.current_pos.zoom
            )


class MockPTZController(PTZController):
    """
    模拟云台控制器 (用于测试)
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_history = []
        self.max_history = 100
    
    def on_move(self, pan: float, tilt: float):
        """模拟移动 (打印日志)"""
        self.move_history.append((time.time(), pan, tilt))
        if len(self.move_history) > self.max_history:
            self.move_history.pop(0)
        
        # 打印移动信息
        print(f"\r[云台] Pan: {pan:6.2f}°, Tilt: {tilt:6.2f}°", end="", flush=True)


# 实际的云台控制接口示例
class SerialPTZController(PTZController):
    """
    串口云台控制器 (需要根据实际硬件实现)
    """
    
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 9600, **kwargs):
        super().__init__(**kwargs)
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        
        try:
            import serial
            self.serial = serial.Serial(port, baudrate, timeout=1)
            print(f"[云台] 串口已打开: {port}")
        except ImportError:
            print("[错误] 未安装 pyserial，请运行: pip install pyserial")
        except Exception as e:
            print(f"[错误] 无法打开串口: {e}")
    
    def on_move(self, pan: float, tilt: float):
        """发送串口命令"""
        if not self.serial:
            return
        
        # 这里需要根据实际云台协议编写
        # 示例: 发送 "PAN,TILT\n"
        command = f"{pan:.2f},{tilt:.2f}\n".encode()
        try:
            self.serial.write(command)
        except Exception as e:
            print(f"[云台] 串口写入错误: {e}")


class ROS2PTZController(PTZController):
    """
    ROS2 云台控制器 (通过 ROS2 话题控制)
    """
    
    def __init__(self, topic: str = "/ptz/cmd", **kwargs):
        super().__init__(**kwargs)
        self.topic = topic
        self.publisher = None
        
        try:
            import rclpy
            from std_msgs.msg import Float64MultiArray
            
            if not rclpy.ok():
                rclpy.init()
            
            self.node = rclpy.create_node("ptz_controller")
            self.publisher = self.node.create_publisher(
                Float64MultiArray, topic, 10
            )
            print(f"[云台] ROS2 发布者已创建: {topic}")
        except ImportError:
            print("[错误] 未安装 rclpy")
        except Exception as e:
            print(f"[错误] ROS2 初始化失败: {e}")
    
    def on_move(self, pan: float, tilt: float):
        """发布 ROS2 消息"""
        if not self.publisher:
            return
        
        try:
            from std_msgs.msg import Float64MultiArray
            msg = Float64MultiArray()
            msg.data = [pan, tilt]
            self.publisher.publish(msg)
        except Exception as e:
            print(f"[云台] ROS2 发布错误: {e}")


if __name__ == "__main__":
    # 测试模拟云台
    print("云台控制器测试")
    
    ptz = MockPTZController(smooth_factor=0.2)
    ptz.set_frame_size(640, 480)
    ptz.start()
    
    # 模拟追踪
    import time
    targets = [
        (200, 150),  # 左上
        (440, 150),  # 右上
        (440, 330),  # 右下
        (200, 330),  # 左下
        (320, 240),  # 中心
    ]
    
    for target in targets:
        print(f"\n[测试] 追踪目标: {target}")
        ptz.track_target(target)
        time.sleep(2)
    
    ptz.stop()
    print("\n测试完成")
