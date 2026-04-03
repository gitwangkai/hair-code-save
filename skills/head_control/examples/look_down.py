#!/usr/bin/env python3
"""
低头示例 - 基于实际测试验证

使用：
    python3 look_down.py

注意：本机器人云台坐标系特殊
- 抬头：数值增大（向 -3.0 移动）
- 中间：-3.35
- 低头：数值减小（向 -3.7 移动）
"""
import rclpy
from std_msgs.msg import Float32
import time


def look_down():
    """低头到接近下限位置"""
    rclpy.init()
    node = rclpy.create_node('look_down')
    pub = node.create_publisher(Float32, '/target_head_position', 10)
    
    print("低头...")
    print("目标角度：-3.6 rad（数值减小=低头）")
    
    msg = Float32()
    msg.data = -3.6  # 低头位置（数值减小）
    
    # 持续发送确保执行
    for _ in range(10):
        pub.publish(msg)
        time.sleep(0.05)
    
    print("✓ 完成")
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    look_down()
