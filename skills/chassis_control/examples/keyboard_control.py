#!/usr/bin/env python3
"""
键盘控制底盘

使用：
    python3 keyboard_control.py
    
按键：
    w - 前进
    s - 后退
    a - 左转
    d - 右转
    q - 退出
"""
import rclpy
from geometry_msgs.msg import Twist
import time
import sys
import select
import termios
import tty


def get_key():
    """获取键盘输入（非阻塞）"""
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None


def main():
    print("=" * 50)
    print("键盘控制底盘")
    print("=" * 50)
    print("\n按键：")
    print("  w - 前进")
    print("  s - 后退")
    print("  a - 左转")
    print("  d - 右转")
    print("  空格 - 停止")
    print("  q - 退出")
    print("\n开始控制...")
    
    # 保存终端设置
    old_settings = termios.tcgetattr(sys.stdin)
    
    try:
        rclpy.init()
        node = rclpy.create_node('keyboard_control')
        pub = node.create_publisher(Twist, '/cmd_vel', 10)
        
        # 设置为非阻塞输入
        tty.setcbreak(sys.stdin.fileno())
        
        msg = Twist()
        speed_linear = 0.3
        speed_angular = 0.5
        
        while True:
            key = get_key()
            
            if key == 'w':
                msg.linear.x = speed_linear
                msg.angular.z = 0.0
                print("前进")
            elif key == 's':
                msg.linear.x = -speed_linear
                msg.angular.z = 0.0
                print("后退")
            elif key == 'a':
                msg.linear.x = 0.0
                msg.angular.z = speed_angular
                print("左转")
            elif key == 'd':
                msg.linear.x = 0.0
                msg.angular.z = -speed_angular
                print("右转")
            elif key == ' ':
                msg.linear.x = 0.0
                msg.angular.z = 0.0
                print("停止")
            elif key == 'q':
                print("\n退出")
                break
            
            pub.publish(msg)
            time.sleep(0.1)
        
        # 停止
        pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()
        
    finally:
        # 恢复终端设置
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
    print("\n✓ 已退出")


if __name__ == '__main__':
    main()
