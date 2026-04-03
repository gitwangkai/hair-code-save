#!/usr/bin/env python3
"""
前进后退示例

使用：
    python3 move_forward.py          # 前进后退
    python3 move_forward.py forward  # 只前进
    python3 move_forward.py backward # 只后退
"""
import rclpy
from geometry_msgs.msg import Twist
import time
import sys


def move(direction='forward', speed=0.3, duration=2.0):
    """
    移动
    
    Args:
        direction: 'forward' 或 'backward'
        speed: 速度 (m/s)
        duration: 时间 (秒)
    """
    rclpy.init()
    node = rclpy.create_node('move_example')
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    linear_x = speed if direction == 'forward' else -speed
    
    print(f"\n{'前进' if direction == 'forward' else '后退'} {duration} 秒...")
    print(f"速度: {linear_x} m/s")
    
    msg = Twist()
    msg.linear.x = linear_x
    
    start = time.time()
    while time.time() - start < duration:
        pub.publish(msg)
        time.sleep(0.1)
    
    # 停止
    pub.publish(Twist())
    print("✓ 已停止")
    
    node.destroy_node()
    rclpy.shutdown()


def main():
    print("=" * 50)
    print("底盘移动示例")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        direction = sys.argv[1]
        if direction == 'forward':
            move('forward')
        elif direction == 'backward':
            move('backward')
        else:
            print(f"未知方向: {direction}")
            print("用法: python3 move_forward.py [forward|backward]")
    else:
        # 前进后退
        move('forward')
        time.sleep(1)
        move('backward')
    
    print("\n✓ 完成")


if __name__ == '__main__':
    main()
