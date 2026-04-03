#!/usr/bin/env python3
"""
点头示例 - 已验证可用

使用：
    python3 nod.py          # 点头3次
    python3 nod.py 5        # 点头5次

注意：本机器人云台坐标系特殊
- 抬头：-3.2 rad（数值增大）
- 低头：-3.6 rad（数值减小）
- 中间：-3.35 rad
"""
import rclpy
from std_msgs.msg import Float32
import time
import sys


def nod(times=3):
    """点头动作 - 已验证"""
    rclpy.init()
    node = rclpy.create_node('nod')
    pub = node.create_publisher(Float32, '/target_head_position', 10)
    
    # 定义角度（基于实际坐标系）
    LOOK_UP = -3.2      # 抬头
    LOOK_DOWN = -3.6    # 低头
    CENTER = -3.35      # 中间
    
    print(f"点头 {times} 次...")
    print(f"  抬头角度：{LOOK_UP} rad")
    print(f"  低头角度：{LOOK_DOWN} rad")
    
    for i in range(times):
        print(f"  第 {i+1}/{times} 次: 低头...")
        msg = Float32()
        msg.data = LOOK_DOWN
        for _ in range(10):
            pub.publish(msg)
            time.sleep(0.05)
        time.sleep(0.3)
        
        print(f"  第 {i+1}/{times} 次: 抬头...")
        msg.data = LOOK_UP
        for _ in range(10):
            pub.publish(msg)
            time.sleep(0.05)
        time.sleep(0.3)
    
    # 归中
    print("归中...")
    msg.data = CENTER
    for _ in range(10):
        pub.publish(msg)
        time.sleep(0.05)
    
    print("✓ 完成")
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    times = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    nod(times)
