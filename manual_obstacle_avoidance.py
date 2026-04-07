#!/usr/bin/env python3
"""
手动移动避障控制节点
功能：
1. 发布手动控制命令到 /cmd_vel_remote_ctrl
2. 监听安全控制输出 /cmd_vel_remote_ctrl_safe
3. 监听激光雷达数据 /scan 进行障碍物检测
4. 实时显示避障状态和传感器数据

使用方法：
1. 先启动 ROS2: source /opt/ros/humble/setup.bash
2. 运行: python3 manual_obstacle_avoidance.py
3. 使用键盘控制机器人移动

作者: gitwangkai
日期: 2026-04-03
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point
from sensor_msgs.msg import LaserScan, PointCloud2
from std_msgs.msg import Bool, Float32
import threading
import sys
import termios
import tty
import select
import time
import math


class ManualObstacleAvoidance(Node):
    """手动避障控制节点"""
    
    def __init__(self):
        super().__init__('manual_obstacle_avoidance')
        
        # 参数配置
        self.declare_parameter('max_linear_speed', 0.5)  # 最大线速度 m/s
        self.declare_parameter('max_angular_speed', 1.0)  # 最大角速度 rad/s
        self.declare_parameter('safety_distance', 0.5)    # 安全距离 m
        self.declare_parameter('slow_distance', 1.0)      # 减速距离 m
        
        self.max_linear = self.get_parameter('max_linear_speed').value
        self.max_angular = self.get_parameter('max_angular_speed').value
        self.safety_dist = self.get_parameter('safety_distance').value
        self.slow_dist = self.get_parameter('slow_distance').value
        
        # 发布者：手动控制命令
        self.cmd_pub = self.create_publisher(
            Twist, 
            '/cmd_vel_remote_ctrl', 
            10
        )
        
        # 订阅者：安全控制输出
        self.safe_cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel_remote_ctrl_safe',
            self.safe_cmd_callback,
            10
        )
        
        # 订阅者：激光雷达数据
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        # 订阅者：点云数据（深度相机）
        self.pointcloud_sub = self.create_subscription(
            PointCloud2,
            '/aurora_2/points2_filted',
            self.pointcloud_callback,
            10
        )
        
        # 状态变量
        self.current_cmd = Twist()      # 当前发送的命令
        self.safe_cmd = Twist()         # 安全控制命令
        self.obstacle_detected = False  # 是否检测到障碍物
        self.min_obstacle_dist = float('inf')  # 最近障碍物距离
        self.obstacle_direction = ""    # 障碍物方向
        
        # 激光雷达数据
        self.scan_data = None
        self.front_distance = float('inf')
        self.left_distance = float('inf')
        self.right_distance = float('inf')
        
        # 控制线程
        self.running = True
        self.control_thread = threading.Thread(target=self.keyboard_control)
        self.control_thread.daemon = True
        
        self.get_logger().info('手动避障控制节点已启动')
        self.get_logger().info('使用键盘控制：')
        self.get_logger().info('  w/s - 前进/后退')
        self.get_logger().info('  a/d - 左转/右转')
        self.get_logger().info('  q/e - 加速/减速')
        self.get_logger().info('  space - 停止')
        self.get_logger().info('  x - 退出')
        
    def safe_cmd_callback(self, msg):
        """接收安全控制命令"""
        self.safe_cmd = msg
        
    def scan_callback(self, msg):
        """处理激光雷达数据"""
        self.scan_data = msg
        
        # 计算前方、左方、右方距离
        ranges = msg.ranges
        angle_min = msg.angle_min
        angle_max = msg.angle_max
        angle_increment = msg.angle_increment
        
        num_points = len(ranges)
        
        # 前方（-15° 到 15°）
        front_indices = []
        left_indices = []
        right_indices = []
        
        for i in range(num_points):
            angle = angle_min + i * angle_increment
            # 归一化角度到 -pi ~ pi
            while angle > math.pi:
                angle -= 2 * math.pi
            while angle < -math.pi:
                angle += 2 * math.pi
                
            # 前方区域 (-15° ~ 15°)
            if abs(angle) < 0.26:  # 15度 = 0.26弧度
                if 0 < ranges[i] < msg.range_max:
                    front_indices.append(ranges[i])
            # 左方区域 (75° ~ 105°)
            elif 1.3 < angle < 1.83:  # 75° ~ 105°
                if 0 < ranges[i] < msg.range_max:
                    left_indices.append(ranges[i])
            # 右方区域 (-105° ~ -75°)
            elif -1.83 < angle < -1.3:  # -105° ~ -75°
                if 0 < ranges[i] < msg.range_max:
                    right_indices.append(ranges[i])
        
        # 计算最小距离
        self.front_distance = min(front_indices) if front_indices else float('inf')
        self.left_distance = min(left_indices) if left_indices else float('inf')
        self.right_distance = min(right_indices) if right_indices else float('inf')
        
        # 检测障碍物
        self.min_obstacle_dist = min(self.front_distance, self.left_distance, self.right_distance)
        self.obstacle_detected = self.min_obstacle_dist < self.safety_dist
        
        # 确定障碍物方向
        if self.front_distance < self.safety_dist:
            self.obstacle_direction = "前方"
        elif self.left_distance < self.safety_dist:
            self.obstacle_direction = "左方"
        elif self.right_distance < self.safety_dist:
            self.obstacle_direction = "右方"
        else:
            self.obstacle_direction = ""
            
    def pointcloud_callback(self, msg):
        """处理点云数据（深度相机）"""
        # 这里可以添加点云处理逻辑
        pass
        
    def keyboard_control(self):
        """键盘控制线程"""
        # 保存终端设置
        old_settings = termios.tcgetattr(sys.stdin)
        
        try:
            tty.setcbreak(sys.stdin.fileno())
            
            while self.running:
                # 非阻塞读取键盘输入
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1)
                    
                    if key == 'w':  # 前进
                        self.current_cmd.linear.x = min(self.current_cmd.linear.x + 0.1, self.max_linear)
                    elif key == 's':  # 后退
                        self.current_cmd.linear.x = max(self.current_cmd.linear.x - 0.1, -self.max_linear)
                    elif key == 'a':  # 左转
                        self.current_cmd.angular.z = min(self.current_cmd.angular.z + 0.2, self.max_angular)
                    elif key == 'd':  # 右转
                        self.current_cmd.angular.z = max(self.current_cmd.angular.z - 0.2, -self.max_angular)
                    elif key == 'q':  # 加速
                        self.max_linear = min(self.max_linear + 0.1, 1.0)
                        self.get_logger().info(f'最大线速度: {self.max_linear:.2f} m/s')
                    elif key == 'e':  # 减速
                        self.max_linear = max(self.max_linear - 0.1, 0.1)
                        self.get_logger().info(f'最大线速度: {self.max_linear:.2f} m/s')
                    elif key == ' ':  # 停止
                        self.current_cmd.linear.x = 0.0
                        self.current_cmd.angular.z = 0.0
                    elif key == 'x':  # 退出
                        self.running = False
                        break
                    elif key == '\x03':  # Ctrl+C
                        self.running = False
                        break
                        
        finally:
            # 恢复终端设置
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            
    def check_safety(self, cmd):
        """安全检查：根据障碍物距离调整速度"""
        safe_cmd = Twist()
        
        # 线速度限制
        if self.front_distance < self.safety_dist and cmd.linear.x > 0:
            # 前方有障碍物，禁止前进
            safe_cmd.linear.x = 0.0
            self.get_logger().warn(f'前方障碍物距离: {self.front_distance:.2f}m，禁止前进！')
        elif self.front_distance < self.slow_dist and cmd.linear.x > 0:
            # 前方接近障碍物，减速
            speed_factor = (self.front_distance - self.safety_dist) / (self.slow_dist - self.safety_dist)
            safe_cmd.linear.x = cmd.linear.x * max(speed_factor, 0.1)
        else:
            safe_cmd.linear.x = cmd.linear.x
            
        # 角速度限制（转弯时）
        if cmd.angular.z > 0 and self.left_distance < self.safety_dist:
            # 左方有障碍物，禁止左转
            safe_cmd.angular.z = 0.0
            self.get_logger().warn(f'左方障碍物距离: {self.left_distance:.2f}m，禁止左转！')
        elif cmd.angular.z < 0 and self.right_distance < self.safety_dist:
            # 右方有障碍物，禁止右转
            safe_cmd.angular.z = 0.0
            self.get_logger().warn(f'右方障碍物距离: {self.right_distance:.2f}m，禁止右转！')
        else:
            safe_cmd.angular.z = cmd.angular.z
            
        return safe_cmd
        
    def print_status(self):
        """打印状态信息"""
        # 清屏
        print('\033[2J\033[H')
        
        print("=" * 60)
        print("       手动避障控制系统")
        print("=" * 60)
        print()
        
        # 传感器状态
        print("【传感器状态】")
        print(f"  前方距离: {self.front_distance:.2f}m" if self.front_distance != float('inf') else "  前方距离: --")
        print(f"  左方距离: {self.left_distance:.2f}m" if self.left_distance != float('inf') else "  左方距离: --")
        print(f"  右方距离: {self.right_distance:.2f}m" if self.right_distance != float('inf') else "  右方距离: --")
        print()
        
        # 避障状态
        print("【避障状态】")
        if self.obstacle_detected:
            print(f"  ⚠️  检测到障碍物！方向: {self.obstacle_direction}")
            print(f"  📏 最近距离: {self.min_obstacle_dist:.2f}m")
        else:
            print("  ✅ 安全，无障碍物")
        print()
        
        # 控制命令
        print("【控制命令】")
        print(f"  目标线速度: {self.current_cmd.linear.x:.2f} m/s")
        print(f"  目标角速度: {self.current_cmd.angular.z:.2f} rad/s")
        print(f"  安全线速度: {self.safe_cmd.linear.x:.2f} m/s")
        print(f"  安全角速度: {self.safe_cmd.angular.z:.2f} rad/s")
        print()
        
        # 操作说明
        print("【操作说明】")
        print("  w/s - 前进/后退")
        print("  a/d - 左转/右转")
        print("  q/e - 增加/减少最大速度")
        print("  space - 紧急停止")
        print("  x - 退出程序")
        print()
        print("=" * 60)
        
    def run(self):
        """主循环"""
        # 启动键盘控制线程
        self.control_thread.start()
        
        # 创建定时器，定期发布控制命令
        timer_period = 0.1  # 10Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # 状态显示定时器
        self.display_timer = self.create_timer(0.5, self.display_callback)
        
        try:
            while self.running and rclpy.ok():
                rclpy.spin_once(self, timeout_sec=0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            # 发送停止命令
            stop_cmd = Twist()
            self.cmd_pub.publish(stop_cmd)
            self.control_thread.join(timeout=1.0)
            self.get_logger().info('程序已退出')
            
    def timer_callback(self):
        """定时发布控制命令"""
        # 安全检查
        safe_cmd = self.check_safety(self.current_cmd)
        
        # 发布命令
        self.cmd_pub.publish(safe_cmd)
        
    def display_callback(self):
        """定时显示状态"""
        self.print_status()


def main(args=None):
    """主函数"""
    rclpy.init(args=args)
    
    try:
        node = ManualObstacleAvoidance()
        node.run()
    except Exception as e:
        print(f"错误: {e}")
    finally:
        # 确保ROS2正确关闭
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
