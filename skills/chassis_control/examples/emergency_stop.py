#!/usr/bin/env python3
"""
底盘紧急停止

使用：
    python3 emergency_stop.py
"""
import rclpy
from geometry_msgs.msg import Twist


def emergency_stop():
    """发送紧急停止指令"""
    rclpy.init()
    node = rclpy.create_node('emergency_stop')
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    print("=" * 50)
    print("底盘紧急停止")
    print("=" * 50)
    
    # 连续发送多次确保停止
    stop_msg = Twist()
    print("\n发送停止指令...")
    for i in range(5):
        pub.publish(stop_msg)
        print(f"  第 {i+1}/5 次")
    
    print("\n✓ 紧急停止已发送")
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    emergency_stop()
