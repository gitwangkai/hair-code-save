#!/usr/bin/env python3
"""
底盘控制器（无避障版本）
基础移动控制，不依赖避障模块

作者: gitwangkai
日期: 2026-04-07
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time


class ChassisController(Node):
    """底盘控制器"""
    
    def __init__(self):
        super().__init__('chassis_controller')
        
        # 发布速度命令
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 当前速度
        self.current_linear = 0.0
        self.current_angular = 0.0
        
        # 定时器（10Hz）
        self.cmd_timer = self.create_timer(0.1, self.send_velocity)
        
        self.get_logger().info('='*60)
        self.get_logger().info('底盘控制器已启动（无避障版本）')
        self.get_logger().info('='*60)
        
    def send_velocity(self):
        """发送速度命令"""
        cmd = Twist()
        cmd.linear.x = self.current_linear
        cmd.angular.z = self.current_angular
        self.cmd_pub.publish(cmd)
        
    def move_forward(self, distance, speed=0.2):
        """前进"""
        self.get_logger().info(f'[移动] 前进{distance}米')
        
        duration = distance / speed
        self.current_linear = speed
        
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(0.05)
            
        self.current_linear = 0.0
        self.get_logger().info('✓ 前进完成')
        return True
        
    def move_backward(self, distance, speed=0.2):
        """后退"""
        self.get_logger().info(f'[移动] 后退{distance}米')
        
        duration = distance / speed
        self.current_linear = -speed
        
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(0.05)
            
        self.current_linear = 0.0
        self.get_logger().info('✓ 后退完成')
        return True
        
    def rotate_left(self, angle, speed=0.5):
        """左转"""
        self.get_logger().info(f'[旋转] 左转{angle}度')
        
        angle_rad = angle * 3.14159 / 180.0
        duration = angle_rad / speed
        self.current_angular = speed
        
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(0.05)
            
        self.current_angular = 0.0
        self.get_logger().info('✓ 左转完成')
        return True
        
    def rotate_right(self, angle, speed=0.5):
        """右转"""
        self.get_logger().info(f'[旋转] 右转{angle}度')
        
        angle_rad = angle * 3.14159 / 180.0
        duration = angle_rad / speed
        self.current_angular = -speed
        
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(0.05)
            
        self.current_angular = 0.0
        self.get_logger().info('✓ 右转完成')
        return True
        
    def stop(self):
        """停止"""
        self.current_linear = 0.0
        self.current_angular = 0.0
        self.send_velocity()
        self.get_logger().info('[控制] 停止')


def main(args=None):
    rclpy.init(args=args)
    controller = ChassisController()
    
    try:
        # 测试动作
        controller.move_forward(1.0)
        time.sleep(1)
        controller.rotate_right(360)
        time.sleep(1)
        controller.stop()
        
        # 保持运行
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
