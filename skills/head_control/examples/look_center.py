#!/usr/bin/env python3
"""
云台归中示例 - 基于实际测试验证

使用：
    python3 look_center.py

中间位置：-3.35 rad
"""
import rclpy
from std_msgs.msg import Float32
import time


def look_center():
    """归中"""
    rclpy.init()
    node = rclpy.create_node('look_center')
    pub = node.create_publisher(Float32, '/target_head_position', 10)
    
    print("云台归中...")
    print("目标角度：-3.35 rad")
    
    msg = Float32()
    msg.data = -3.35  # 中间位置
    
    # 持续发送确保执行
    for _ in range(10):
        pub.publish(msg)
        time.sleep(0.05)
    
    print("✓ 完成")
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    look_center()
