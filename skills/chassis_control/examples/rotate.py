#!/usr/bin/env python3
"""
原地旋转示例

使用：
    python3 rotate.py        # 左转 3 秒
    python3 rotate.py left   # 左转
    python3 rotate.py right  # 右转
    python3 rotate.py 90     # 左转 90 度
"""
import rclpy
from geometry_msgs.msg import Twist
import time
import sys
import math


def rotate_by_time(direction='left', speed=0.5, duration=3.0):
    """
    按时间旋转
    
    Args:
        direction: 'left' 或 'right'
        speed: 角速度 (rad/s)
        duration: 时间 (秒)
    """
    rclpy.init()
    node = rclpy.create_node('rotate_example')
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    angular_z = speed if direction == 'left' else -speed
    
    print(f"\n原地{ '左转' if direction == 'left' else '右转' } {duration} 秒...")
    print(f"角速度: {angular_z} rad/s")
    
    msg = Twist()
    msg.angular.z = angular_z
    
    start = time.time()
    while time.time() - start < duration:
        pub.publish(msg)
        time.sleep(0.1)
    
    # 停止
    pub.publish(Twist())
    print("✓ 已停止")
    
    node.destroy_node()
    rclpy.shutdown()


def rotate_by_angle(angle_deg=90, speed=0.5):
    """
    按角度旋转
    
    Args:
        angle_deg: 角度 (度)，正为左转，负为右转
        speed: 角速度 (rad/s)
    """
    angular_z = speed if angle_deg > 0 else -speed
    duration = abs(angle_deg) / (speed * 180 / math.pi)
    direction = 'left' if angle_deg > 0 else 'right'
    
    print(f"\n原地{ '左转' if direction == 'left' else '右转' } {abs(angle_deg)} 度...")
    rotate_by_time(direction, speed, duration)


def main():
    print("=" * 50)
    print("底盘旋转示例")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == 'left':
            rotate_by_time('left')
        elif arg == 'right':
            rotate_by_time('right')
        elif arg.lstrip('-').isdigit():
            rotate_by_angle(float(arg))
        else:
            print(f"未知参数: {arg}")
            print("用法: python3 rotate.py [left|right|角度]")
    else:
        # 默认左转 3 秒
        rotate_by_time('left')
    
    print("\n✓ 完成")


if __name__ == '__main__':
    main()
