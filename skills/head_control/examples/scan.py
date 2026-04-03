#!/usr/bin/env python3
"""
扫描示例（上下扫视）

使用：
    python3 scan.py          # 扫描 ±30°
    python3 scan.py 45       # 扫描 ±45°
"""
import rclpy
from std_msgs.msg import Float32
import time
import math
import sys


def scan(range_deg=30, duration=2.0):
    """
    扫描动作（上下扫视）
    
    Args:
        range_deg: 扫描角度范围
        duration: 扫描周期
    """
    rclpy.init()
    node = rclpy.create_node('scan')
    pub = node.create_publisher(Float32, '/target_head_position', 10)
    
    print(f"扫描 ±{range_deg}°...")
    
    range_rad = math.radians(range_deg)
    steps = int(duration * 20)
    
    for i in range(steps):
        t = i / steps
        # 正弦波运动
        angle = range_rad * math.sin(t * 2 * math.pi)
        
        msg = Float32()
        msg.data = float(angle)
        pub.publish(msg)
        time.sleep(0.05)
    
    # 归中
    msg = Float32()
    msg.data = 0.0
    pub.publish(msg)
    
    print("✓ 完成")
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    range_deg = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    scan(range_deg)
