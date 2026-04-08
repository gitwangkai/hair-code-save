#!/usr/bin/env python3
"""
安全底盘控制器示例
集成避障功能的底盘控制

使用方法：
python3 safe_chassis_controller.py
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import os
import select
import termios
import tty

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from obstacle_monitor import ObstacleMonitor


class SafeChassisController(Node):
    """带避障功能的底盘控制器"""
    
    def __init__(self):
        super().__init__('safe_chassis_controller')
        
        # 创建避障监控器
        self.obstacle_monitor = ObstacleMonitor(
            safety_distance=0.5,
            slow_distance=1.0,
            max_linear_speed=0.5,
            max_angular_speed=1.0
        )
        
        # 发布速度命令（使用海尔机器人系统的话题）
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel_remote_ctrl', 10)
        
        # 当前速度
        self.current_linear = 0.0
        self.current_angular = 0.0
        self.target_linear = 0.0  # 目标速度
        self.target_angular = 0.0
        
        # 状态显示定时器
        self.display_timer = self.create_timer(0.5, self.display_status)
        
        # 速度发布定时器（10Hz）
        self.cmd_timer = self.create_timer(0.1, self.send_velocity)
        
        self.get_logger().info('安全底盘控制器已启动')
        self.get_logger().info('使用键盘控制（带避障保护）：')
        self.get_logger().info('  w/s - 前进/后退')
        self.get_logger().info('  a/d - 左转/右转')
        self.get_logger().info('  space - 停止')
        self.get_logger().info('  q - 退出')
        
    def display_status(self):
        """显示状态信息"""
        info = self.obstacle_monitor.get_obstacle_info()
        
        # 清屏
        print('\033[2J\033[H')
        
        print("=" * 60)
        print("       安全底盘控制器（带避障）")
        print("=" * 60)
        print()
        
        # 障碍物信息
        print("【障碍物检测】")
        front_str = f"{info['front']:.2f}m" if info['front'] != float('inf') else "--"
        left_str = f"{info['left']:.2f}m" if info['left'] != float('inf') else "--"
        right_str = f"{info['right']:.2f}m" if info['right'] != float('inf') else "--"
        print(f"  前方距离: {front_str}")
        print(f"  左方距离: {left_str}")
        print(f"  右方距离: {right_str}")
        print()
        
        # 避障状态
        if info['detected']:
            print(f"  ⚠️  障碍物警告！方向: {info['direction']}, 距离: {info['min']:.2f}m")
        else:
            print("  ✅ 安全，无障碍物")
        print()
        
        # 控制状态
        print("【控制状态】")
        print(f"  目标线速度: {self.target_linear:.2f} m/s")
        print(f"  目标角速度: {self.target_angular:.2f} rad/s")
        print(f"  实际线速度: {self.current_linear:.2f} m/s")
        print(f"  实际角速度: {self.current_angular:.2f} rad/s")
        
        # 安全状态
        if not self.obstacle_monitor.can_move_forward():
            print("  ⛔ 禁止前进 - 前方有障碍物")
        if not self.obstacle_monitor.can_turn_left():
            print("  ⛔ 禁止左转 - 左方有障碍物")
        if not self.obstacle_monitor.can_turn_right():
            print("  ⛔ 禁止右转 - 右方有障碍物")
        
        print()
        print("=" * 60)
        
    def move_forward(self, speed=0.3):
        """前进（带避障检查）"""
        self.target_linear = speed
        if not self.obstacle_monitor.can_move_forward():
            self.get_logger().warn('前方有障碍物，无法前进！')
            return False
        return True
            
    def move_backward(self, speed=0.3):
        """后退（带避障检查）"""
        self.target_linear = -speed
        if not self.obstacle_monitor.can_move_backward():
            self.get_logger().warn('后方有障碍物，无法后退！')
            return False
        return True
            
    def turn_left(self, speed=0.5):
        """左转（带避障检查）"""
        self.target_angular = speed
        if not self.obstacle_monitor.can_turn_left():
            self.get_logger().warn('左方有障碍物，无法左转！')
            return False
        return True
            
    def turn_right(self, speed=0.5):
        """右转（带避障检查）"""
        self.target_angular = -speed
        if not self.obstacle_monitor.can_turn_right():
            self.get_logger().warn('右方有障碍物，无法右转！')
            return False
        return True
            
    def stop(self):
        """停止"""
        self.target_linear = 0.0
        self.target_angular = 0.0
        
    def send_velocity(self):
        """发送速度命令（定时器回调）"""
        # 创建目标速度命令
        target_cmd = Twist()
        target_cmd.linear.x = self.target_linear
        target_cmd.angular.z = self.target_angular
        
        # 通过避障监控器获取安全速度
        safe_cmd = self.obstacle_monitor.get_safe_velocity(target_cmd)
        
        # 更新当前实际速度
        self.current_linear = safe_cmd.linear.x
        self.current_angular = safe_cmd.angular.z
        
        # 发布安全速度
        self.cmd_pub.publish(safe_cmd)
        
        # 处理ROS回调
        rclpy.spin_once(self, timeout_sec=0)
        
    def keyboard_control(self):
        """键盘控制"""
        # 保存终端设置
        old_settings = termios.tcgetattr(sys.stdin)
        
        try:
            tty.setcbreak(sys.stdin.fileno())
            
            while rclpy.ok():
                # 非阻塞读取
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1)
                    
                    if key == 'w':
                        self.move_forward(0.3)
                    elif key == 's':
                        self.move_backward(0.3)
                    elif key == 'a':
                        self.turn_left(0.5)
                    elif key == 'd':
                        self.turn_right(0.5)
                    elif key == ' ':
                        self.stop()
                    elif key == 'q' or key == '\x03':
                        break
                        
        finally:
            # 恢复终端设置
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            self.stop()


def main(args=None):
    """主函数"""
    rclpy.init(args=args)
    
    try:
        controller = SafeChassisController()
        controller.keyboard_control()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
