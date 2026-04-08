#!/usr/bin/env python3
"""
简单复合动作演示（无避障版本）
执行指令：前进1米开始挥手，挥手时同步向右旋转360度然后左转前进一米点头，最后原路返回

作者: gitwangkai
日期: 2026-04-07
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys
import time
import threading


class SimpleActionDemo(Node):
    """简单复合动作演示"""
    
    def __init__(self):
        super().__init__('simple_action_demo')
        
        # 发布器
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel_remote_ctrl', 10)
        self.arm_pub = self.create_publisher(String, '/arm_action', 10)
        
        # 当前速度
        self.current_linear = 0.0
        self.current_angular = 0.0
        
        # 定时器（10Hz发布速度）
        self.cmd_timer = self.create_timer(0.1, self.send_velocity)
        
        self.get_logger().info('='*60)
        self.get_logger().info('简单复合动作演示（无避障版本）')
        self.get_logger().info('='*60)
        
    def send_velocity(self):
        """发送速度命令"""
        cmd = Twist()
        cmd.linear.x = self.current_linear
        cmd.angular.z = self.current_angular
        self.cmd_pub.publish(cmd)
        
    def skill_move(self, distance, speed=0.2):
        """移动"""
        direction = "前进" if distance > 0 else "后退"
        self.get_logger().info(f'[Skill] {direction}{abs(distance)}米')
        
        duration = abs(distance) / speed
        self.current_linear = speed * (1 if distance > 0 else -1)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(0.05)
            
        self.current_linear = 0.0
        return True
        
    def skill_rotate(self, angle, speed=0.5):
        """旋转"""
        direction = "左转" if angle > 0 else "右转"
        self.get_logger().info(f'[Skill] {direction}{abs(angle)}度')
        
        angle_rad = abs(angle) * 3.14159 / 180.0
        duration = angle_rad / speed
        self.current_angular = speed * (1 if angle > 0 else -1)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(0.05)
            
        self.current_angular = 0.0
        return True
        
    def skill_wave(self, duration=3):
        """挥手"""
        self.get_logger().info(f'[Skill] 挥手{duration}秒')
        msg = String()
        msg.data = 'wave_hand'
        self.arm_pub.publish(msg)
        time.sleep(duration)
        
    def skill_nod(self, duration=2):
        """点头"""
        self.get_logger().info(f'[Skill] 点头{duration}秒')
        msg = String()
        msg.data = 'nod'
        self.arm_pub.publish(msg)
        time.sleep(duration)
        
    def execute(self):
        """执行复合动作"""
        self.get_logger().info('')
        self.get_logger().info('='*60)
        self.get_logger().info('开始执行：前进1米挥手 → 右转360° → 左转前进1米点头 → 返回')
        self.get_logger().info('='*60)
        
        # 步骤1：前进1米 + 挥手
        self.get_logger().info('')
        self.get_logger().info('【步骤1】前进1米 + 挥手')
        wave_thread = threading.Thread(target=self.skill_wave, args=(3,))
        wave_thread.start()
        self.skill_move(1.0)
        
        # 步骤2：向右旋转360度（挥手继续）
        self.get_logger().info('')
        self.get_logger().info('【步骤2】向右旋转360度（挥手继续）')
        self.skill_rotate(-360)
        wave_thread.join()
        
        # 步骤3：左转 + 前进1米 + 点头
        self.get_logger().info('')
        self.get_logger().info('【步骤3】左转 + 前进1米 + 点头')
        self.skill_rotate(90)
        self.skill_move(1.0)
        self.skill_nod()
        
        # 步骤4：原路返回
        self.get_logger().info('')
        self.get_logger().info('【步骤4】原路返回')
        self.skill_move(-1.0)
        self.skill_rotate(-90)
        self.skill_move(-1.0)
        
        self.get_logger().info('')
        self.get_logger().info('='*60)
        self.get_logger().info('✅ 复合动作执行完成！')
        self.get_logger().info('='*60)


def main(args=None):
    rclpy.init(args=args)
    demo = SimpleActionDemo()
    
    try:
        demo.execute()
        # 保持运行一段时间
        time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        demo.current_linear = 0.0
        demo.current_angular = 0.0
        demo.send_velocity()
        demo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
