#!/usr/bin/env python3
"""
底盘控制器封装类

使用：
    from chassis_controller import ChassisController
    
    chassis = ChassisController()
    chassis.move(linear_x=0.5, duration=2.0)  # 前进 2 秒
    chassis.rotate(90)  # 左转 90 度
    chassis.destroy()
"""
import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time


class ChassisController:
    """底盘控制器"""
    
    def __init__(self):
        rclpy.init()
        self.node = rclpy.create_node('chassis_controller')
        self.cmd_pub = self.node.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.node.create_subscription(
            Odometry, '/odom', self._odom_callback, 10)
        
        self.current_pose = None
        self.current_twist = None
    
    def _odom_callback(self, msg):
        """里程计回调"""
        self.current_pose = msg.pose.pose
        self.current_twist = msg.twist.twist
    
    def move(self, linear_x=0.0, angular_z=0.0, duration=0.0):
        """
        发送速度指令
        
        Args:
            linear_x: 线速度 (m/s)，正为前进，负为后退
            angular_z: 角速度 (rad/s)，正为左转，负为右转
            duration: 持续时间 (秒)，0 表示只发送一次
        """
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = float(angular_z)
        
        if duration > 0:
            start_time = time.time()
            while time.time() - start_time < duration:
                self.cmd_pub.publish(msg)
                time.sleep(0.1)
            self.stop()
        else:
            self.cmd_pub.publish(msg)
    
    def stop(self):
        """紧急停止"""
        msg = Twist()
        self.cmd_pub.publish(msg)
    
    def rotate(self, angle_deg, speed=0.5):
        """
        旋转指定角度
        
        Args:
            angle_deg: 角度 (度)，正为左转，负为右转
            speed: 角速度 (rad/s)
        """
        angular_z = speed if angle_deg > 0 else -speed
        duration = abs(angle_deg) / (speed * 180 / math.pi)
        self.move(0.0, angular_z, duration)
    
    def move_linear(self, distance_m, speed=0.3):
        """
        直线移动指定距离
        
        Args:
            distance_m: 距离 (米)，正为前进，负为后退
            speed: 速度 (m/s)
        """
        linear_x = speed if distance_m > 0 else -speed
        duration = abs(distance_m) / speed
        self.move(linear_x, 0.0, duration)
    
    def get_pose(self):
        """获取当前位姿"""
        return self.current_pose
    
    def destroy(self):
        """清理资源"""
        self.stop()
        self.node.destroy_node()
        rclpy.shutdown()


def demo():
    """演示"""
    print("=" * 50)
    print("底盘控制演示")
    print("=" * 50)
    
    chassis = ChassisController()
    
    try:
        print("\n1. 前进 1 米...")
        chassis.move_linear(1.0, speed=0.3)
        time.sleep(0.5)
        
        print("\n2. 左转 90 度...")
        chassis.rotate(90, speed=0.5)
        time.sleep(0.5)
        
        print("\n3. 前进 0.5 米...")
        chassis.move_linear(0.5, speed=0.3)
        time.sleep(0.5)
        
        print("\n4. 右转 90 度...")
        chassis.rotate(-90, speed=0.5)
        time.sleep(0.5)
        
        print("\n5. 后退 0.5 米...")
        chassis.move_linear(-0.5, speed=0.3)
        
        print("\n6. 停止")
        chassis.stop()
        
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
    finally:
        chassis.destroy()
        print("\n✓ 演示完成")


if __name__ == '__main__':
    demo()
