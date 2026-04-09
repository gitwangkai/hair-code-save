#!/usr/bin/env python3
"""
避障监控核心类（重构版）
功能：实时监测激光雷达数据，检测障碍物，提供安全速度控制

重构说明：
- 不再继承 Node，改为接收 parent_node 参数
- 避免 ROS2 中多个 Node 嵌套实例化的问题

作者: gitwangkai
日期: 2026-04-07
"""

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, Float32, String
import math
from typing import Callable, Optional, Dict


class ObstacleMonitor:
    """
    避障监控器（非 Node 类）
    
    使用方式：
        class MyNode(Node):
            def __init__(self):
                self.obstacle_monitor = ObstacleMonitor(self)
                
            def timer_callback(self):
                self.obstacle_monitor.spin_once()
    """
    
    def __init__(
        self,
        parent_node,
        safety_distance: float = 0.5,
        slow_distance: float = 1.0,
        max_linear_speed: float = 0.5,
        max_angular_speed: float = 1.0,
        front_angle_range: float = 30.0,
        side_angle_range: float = 30.0
    ):
        """
        初始化避障监控器
        
        Args:
            parent_node: 父 ROS2 Node 实例
            safety_distance: 安全距离（米），小于此距离停止
            slow_distance: 减速距离（米），小于此距离减速
            max_linear_speed: 最大线速度（m/s）
            max_angular_speed: 最大角速度（rad/s）
            front_angle_range: 前方检测角度范围（度）
            side_angle_range: 侧方检测角度范围（度）
        """
        self._parent = parent_node
        self._safety_distance = safety_distance
        self._slow_distance = slow_distance
        self._max_linear_speed = max_linear_speed
        self._max_angular_speed = max_angular_speed
        self._front_angle_range = math.radians(front_angle_range)
        self._side_angle_range = math.radians(side_angle_range)
        
        # 状态变量
        self._scan_data: Optional[LaserScan] = None
        self._obstacle_detected = False
        self._min_obstacle_dist = float('inf')
        self._obstacle_direction = ""
        
        # 距离数据
        self._front_distance = float('inf')
        self._left_distance = float('inf')
        self._right_distance = float('inf')
        self._rear_distance = float('inf')
        
        # 回调函数
        self._on_obstacle_detected: Optional[Callable] = None
        self._on_obstacle_cleared: Optional[Callable] = None
        
        # 使用父 node 创建订阅器和发布器
        self._scan_sub = parent_node.create_subscription(
            LaserScan,
            '/scan',
            self._scan_callback,
            10
        )
        
        # 发布障碍物状态
        self._obstacle_status_pub = parent_node.create_publisher(Bool, '/obstacle_status', 10)
        self._obstacle_distance_pub = parent_node.create_publisher(Float32, '/obstacle_distance', 10)
        self._obstacle_direction_pub = parent_node.create_publisher(String, '/obstacle_direction', 10)
        
        parent_node.get_logger().info('避障监控器已初始化')
        parent_node.get_logger().info(f'安全距离: {safety_distance}m, 减速距离: {slow_distance}m')
        
    def _scan_callback(self, msg: LaserScan):
        """处理激光雷达数据"""
        self._scan_data = msg
        
        ranges = msg.ranges
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment
        num_points = len(ranges)
        
        # 收集各方向的点
        front_points = []
        left_points = []
        right_points = []
        rear_points = []
        
        for i in range(num_points):
            angle = angle_min + i * angle_increment
            
            # 归一化角度
            while angle > math.pi:
                angle -= 2 * math.pi
            while angle < -math.pi:
                angle += 2 * math.pi
                
            distance = ranges[i]
            
            # 过滤无效数据
            if distance <= 0 or distance > msg.range_max or math.isinf(distance) or math.isnan(distance):
                continue
                
            # 前方区域 (-front_angle_range ~ +front_angle_range)
            if abs(angle) < self._front_angle_range:
                front_points.append(distance)
            # 左方区域 (+60° ~ +120°)
            elif 1.05 < angle < 2.09:  # 60° ~ 120°
                left_points.append(distance)
            # 右方区域 (-120° ~ -60°)
            elif -2.09 < angle < -1.05:  # -120° ~ -60°
                right_points.append(distance)
            # 后方区域 (150° ~ 210°)
            elif abs(abs(angle) - math.pi) < self._front_angle_range:
                rear_points.append(distance)
        
        # 计算最小距离
        self._front_distance = min(front_points) if front_points else float('inf')
        self._left_distance = min(left_points) if left_points else float('inf')
        self._right_distance = min(right_points) if right_points else float('inf')
        self._rear_distance = min(rear_points) if rear_points else float('inf')
        
        # 更新障碍物状态
        prev_detected = self._obstacle_detected
        self._min_obstacle_dist = min(self._front_distance, self._left_distance, self._right_distance)
        self._obstacle_detected = self._min_obstacle_dist < self._safety_distance
        
        # 确定障碍物方向
        if self._front_distance < self._safety_distance:
            self._obstacle_direction = "front"
        elif self._left_distance < self._safety_distance:
            self._obstacle_direction = "left"
        elif self._right_distance < self._safety_distance:
            self._obstacle_direction = "right"
        else:
            self._obstacle_direction = ""
        
        # 触发回调
        if not prev_detected and self._obstacle_detected and self._on_obstacle_detected:
            self._on_obstacle_detected(self._obstacle_direction, self._min_obstacle_dist)
        elif prev_detected and not self._obstacle_detected and self._on_obstacle_cleared:
            self._on_obstacle_cleared()
            
    def spin_once(self):
        """单次处理，应由父 node 的 timer 调用"""
        # 发布障碍物状态
        status_msg = Bool()
        status_msg.data = self._obstacle_detected
        self._obstacle_status_pub.publish(status_msg)
        
        # 发布距离
        dist_msg = Float32()
        dist_msg.data = self._min_obstacle_dist if self._min_obstacle_dist != float('inf') else -1.0
        self._obstacle_distance_pub.publish(dist_msg)
        
        # 发布方向
        dir_msg = String()
        dir_msg.data = self._obstacle_direction
        self._obstacle_direction_pub.publish(dir_msg)
        
    def get_safe_velocity(self, desired_cmd: Twist) -> Twist:
        """
        根据障碍物情况获取安全速度
        
        Args:
            desired_cmd: 期望的速度命令
            
        Returns:
            Twist: 安全速度命令
        """
        safe_cmd = Twist()
        
        # 线速度限制
        if desired_cmd.linear.x > 0:  # 前进
            if self._front_distance < self._safety_distance:
                # 危险区域，禁止前进
                safe_cmd.linear.x = 0.0
                self._parent.get_logger().warn(
                    f'前方障碍物距离: {self._front_distance:.2f}m，禁止前进！',
                    throttle_duration_sec=1.0
                )
            elif self._front_distance < self._slow_distance:
                # 减速区域
                speed_factor = max(
                    0.0,
                    (self._front_distance - self._safety_distance) / 
                    (self._slow_distance - self._safety_distance)
                )
                safe_cmd.linear.x = desired_cmd.linear.x * speed_factor
            else:
                # 安全区域
                safe_cmd.linear.x = min(desired_cmd.linear.x, self._max_linear_speed)
        elif desired_cmd.linear.x < 0:  # 后退
            if self._rear_distance < self._safety_distance:
                safe_cmd.linear.x = 0.0
                self._parent.get_logger().warn(
                    f'后方障碍物距离: {self._rear_distance:.2f}m，禁止后退！',
                    throttle_duration_sec=1.0
                )
            else:
                safe_cmd.linear.x = max(desired_cmd.linear.x, -self._max_linear_speed)
        else:
            safe_cmd.linear.x = 0.0
            
        # 角速度限制
        if desired_cmd.angular.z > 0:  # 左转
            if self._left_distance < self._safety_distance:
                safe_cmd.angular.z = 0.0
                self._parent.get_logger().warn(
                    f'左方障碍物距离: {self._left_distance:.2f}m，禁止左转！',
                    throttle_duration_sec=1.0
                )
            else:
                safe_cmd.angular.z = min(desired_cmd.angular.z, self._max_angular_speed)
        elif desired_cmd.angular.z < 0:  # 右转
            if self._right_distance < self._safety_distance:
                safe_cmd.angular.z = 0.0
                self._parent.get_logger().warn(
                    f'右方障碍物距离: {self._right_distance:.2f}m，禁止右转！',
                    throttle_duration_sec=1.0
                )
            else:
                safe_cmd.angular.z = max(desired_cmd.angular.z, -self._max_angular_speed)
        else:
            safe_cmd.angular.z = 0.0
            
        # Z轴速度直接通过
        safe_cmd.linear.z = desired_cmd.linear.z
        safe_cmd.angular.x = desired_cmd.angular.x
        safe_cmd.angular.y = desired_cmd.angular.y
        
        return safe_cmd
        
    def can_move_forward(self) -> bool:
        """检查是否可以前进"""
        return self._front_distance >= self._safety_distance
        
    def can_move_backward(self) -> bool:
        """检查是否可以后退"""
        return self._rear_distance >= self._safety_distance
        
    def can_turn_left(self) -> bool:
        """检查是否可以左转"""
        return self._left_distance >= self._safety_distance
        
    def can_turn_right(self) -> bool:
        """检查是否可以右转"""
        return self._right_distance >= self._safety_distance
        
    def get_obstacle_info(self) -> Dict:
        """
        获取障碍物信息
        
        Returns:
            Dict: 包含各方向距离和状态的字典
        """
        return {
            'front': self._front_distance,
            'left': self._left_distance,
            'right': self._right_distance,
            'rear': self._rear_distance,
            'min': self._min_obstacle_dist,
            'detected': self._obstacle_detected,
            'direction': self._obstacle_direction
        }
        
    def is_obstacle_detected(self) -> bool:
        """检查是否检测到障碍物"""
        return self._obstacle_detected
        
    def get_closest_obstacle_distance(self) -> float:
        """获取最近障碍物距离"""
        return self._min_obstacle_dist
        
    def set_callbacks(
        self,
        on_obstacle_detected: Optional[Callable] = None,
        on_obstacle_cleared: Optional[Callable] = None
    ):
        """
        设置回调函数
        
        Args:
            on_obstacle_detected: 检测到障碍物时的回调函数，参数：(direction, distance)
            on_obstacle_cleared: 障碍物清除时的回调函数
        """
        self._on_obstacle_detected = on_obstacle_detected
        self._on_obstacle_cleared = on_obstacle_cleared
        
    # 属性访问器
    @property
    def safety_distance(self) -> float:
        return self._safety_distance
        
    @safety_distance.setter
    def safety_distance(self, value: float):
        self._safety_distance = value
        self._parent.get_logger().info(f'安全距离已更新为: {value}m')
        
    @property
    def slow_distance(self) -> float:
        return self._slow_distance
        
    @slow_distance.setter
    def slow_distance(self, value: float):
        self._slow_distance = value
        self._parent.get_logger().info(f'减速距离已更新为: {value}m')
        
    @property
    def max_linear_speed(self) -> float:
        return self._max_linear_speed
        
    @max_linear_speed.setter
    def max_linear_speed(self, value: float):
        self._max_linear_speed = value
        
    @property
    def max_angular_speed(self) -> float:
        return self._max_angular_speed
        
    @max_angular_speed.setter
    def max_angular_speed(self, value: float):
        self._max_angular_speed = value
