#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超声波感知模块 - Ultrasonic Perception Module
提供机器人超声波传感器的感知与避障能力

硬件配置: 单路前向超声波传感器 (UETCH101)
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
import threading
import time
from typing import Optional


class UltrasonicPerception:
    """
    超声波感知类 - 单路前向超声波
    
    使用底盘前侧超声波传感器:
    - 话题: /ultrasonic_front (CAN总线) 或 /ultrasonic/range (UART)
    """
    
    # 默认值
    DEFAULT_MIN_RANGE = 0.02  # 最小测距范围 (m)
    DEFAULT_MAX_RANGE = 4.0   # 最大测距范围 (m)
    DEFAULT_TIMEOUT = 1.0     # 数据超时时间 (s)
    
    def __init__(
        self,
        topic: str = "/ultrasonic_front",
        timeout: float = 1.0
    ):
        """
        初始化超声波感知模块
        
        Args:
            topic: 超声波话题 (默认: /ultrasonic_front)
                   可选: /ultrasonic/range (UART驱动发布的话题)
            timeout: 数据超时时间 (秒)
        """
        self.topic = topic
        self.timeout = timeout
        
        # 传感器数据存储
        self._data = {
            'range': None,
            'stamp': 0.0,
            'valid': False
        }
        
        # 创建独立ROS2上下文（避免与主程序冲突）
        if not rclpy.ok():
            rclpy.init()
        
        self.node = rclpy.create_node('ultrasonic_perception')
        
        # 创建订阅者
        self._subscriber = self.node.create_subscription(
            Range, topic, self._callback, 10
        )
        
        # 启动后台线程处理ROS2回调
        self._running = True
        self._thread = threading.Thread(target=self._spin)
        self._thread.daemon = True
        self._thread.start()
        
        # 等待数据初始化
        time.sleep(0.5)
        
        print(f"[Ultrasonic] 感知模块初始化完成")
        print(f"  - 话题: {topic}")
    
    def _spin(self):
        """后台线程: 处理ROS2回调"""
        while self._running and rclpy.ok():
            rclpy.spin_once(self.node, timeout_sec=0.1)
    
    def _callback(self, msg: Range):
        """超声波数据回调"""
        self._data = {
            'range': msg.range,
            'stamp': time.time(),
            'valid': self._is_valid_range(msg.range, msg.min_range, msg.max_range)
        }
    
    def _is_valid_range(self, range_val: float, min_range: float, max_range: float) -> bool:
        """检查距离值是否有效"""
        if range_val is None:
            return False
        # 排除 inf 和超出范围的值
        if range_val == float('inf') or range_val == float('-inf'):
            return False
        return min_range <= range_val <= max_range
    
    def _is_data_fresh(self) -> bool:
        """检查数据是否新鲜"""
        return (time.time() - self._data['stamp']) < self.timeout
    
    def get_distance(self) -> Optional[float]:
        """
        获取前方距离
        
        Returns:
            float: 距离(米)，数据无效时返回None
        """
        if self._data['valid'] and self._is_data_fresh():
            return self._data['range']
        return None
    
    def is_obstacle_ahead(self, threshold: float = 0.5) -> bool:
        """
        检查前方是否有障碍物
        
        Args:
            threshold: 障碍物检测阈值(米)
        
        Returns:
            bool: 有障碍物返回True
        """
        dist = self.get_distance()
        if dist is None:
            return False  # 数据无效时保守判断
        return dist < threshold
    
    def get_safe_status(self) -> str:
        """
        获取安全状态
        
        Returns:
            str: 'safe'/'caution'/'danger'/'unknown'
        """
        dist = self.get_distance()
        if dist is None:
            return 'unknown'
        
        if dist < 0.3:
            return 'danger'  # < 30cm 危险
        elif dist < 0.6:
            return 'caution'  # 30-60cm 警告
        else:
            return 'safe'  # > 60cm 安全
    
    def wait_for_obstacle_cleared(
        self,
        threshold: float = 0.5,
        timeout: float = 30.0,
        check_interval: float = 0.5
    ) -> bool:
        """
        等待障碍物清除
        
        Args:
            threshold: 障碍物距离阈值
            timeout: 最大等待时间(秒)
            check_interval: 检查间隔(秒)
        
        Returns:
            bool: 障碍物已清除返回True，超时返回False
        """
        start_time = time.time()
        print(f"[Ultrasonic] 等待前方障碍物清除...")
        
        while time.time() - start_time < timeout:
            if not self.is_obstacle_ahead(threshold):
                print(f"[Ultrasonic] 障碍物已清除")
                return True
            time.sleep(check_interval)
        
        print(f"[Ultrasonic] 等待超时")
        return False
    
    def get_status_report(self) -> str:
        """获取状态报告字符串"""
        dist = self.get_distance()
        
        lines = ["=" * 40, "超声波传感器状态", "=" * 40]
        
        if dist is not None:
            status = self.get_safe_status()
            status_icon = {"safe": "✓ 安全", "caution": "⚠ 注意", "danger": "✗ 危险"}.get(status, "?")
            lines.append(f"  前超声波: {dist:5.2f}m [{status_icon}]")
            
            # 障碍物提示
            if status == 'danger':
                lines.append("  [警告] 前方距离过近，建议停止！")
            elif status == 'caution':
                lines.append("  [提示] 前方有障碍物，建议减速")
        else:
            lines.append("  前超声波: -- 无数据")
        
        lines.append("=" * 40)
        return "\n".join(lines)
    
    def close(self):
        """关闭感知模块，释放资源"""
        print("[Ultrasonic] 关闭感知模块...")
        self._running = False
        self._thread.join(timeout=2.0)
        self.node.destroy_node()
    
    def __del__(self):
        """析构函数"""
        if self._running:
            self.close()


def main():
    """测试程序"""
    print("=" * 50)
    print("超声波感知模块测试")
    print("=" * 50)
    
    perception = UltrasonicPerception()
    
    try:
        while True:
            print("\033[2J\033[H")  # 清屏
            print(perception.get_status_report())
            print("\n按 Ctrl+C 退出")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n\n测试结束")
    finally:
        perception.close()


if __name__ == "__main__":
    main()
