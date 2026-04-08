#!/usr/bin/env python3
"""
复合动作：前进挥手旋转返回
Skill: action_runner

动作序列：
1. 前进1米 + 开始挥手
2. 挥手时同步向右旋转360度
3. 左转 + 前进1米 + 点头
4. 原路返回

依赖 Skills:
- obstacle_avoidance: 避障监控
- chassis_control: 底盘移动
- arm_control: 挥手、点头
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys
import os
import time
import threading

# 添加 skills 路径
sys.path.insert(0, '/home/aidlux/skills/obstacle_avoidance/src')
sys.path.insert(0, '/home/aidlux/skills/arm_control/examples')

from obstacle_monitor import ObstacleMonitor


class ComplexWaveReturnSkill(Node):
    """复合动作 Skill"""
    
    def __init__(self):
        super().__init__('complex_wave_return_skill')
        
        # 初始化避障监控器
        self.obstacle_monitor = ObstacleMonitor(
            safety_distance=0.5,
            slow_distance=1.0,
            max_linear_speed=0.3,
            max_angular_speed=0.5
        )
        
        # 发布器
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel_remote_ctrl', 10)
        self.action_pub = self.create_publisher(String, '/robot_action', 10)
        self.arm_pub = self.create_publisher(String, '/arm_action', 10)
        
        # 当前速度
        self.current_linear = 0.0
        self.current_angular = 0.0
        
        # 速度发布定时器（10Hz）
        self.cmd_timer = self.create_timer(0.1, self.send_velocity)
        
        self.get_logger().info('复合动作 Skill 已加载')
        self.get_logger().info('动作: 前进1米挥手 → 右转360度 → 左转前进1米点头 → 返回')
        
    def send_velocity(self):
        """发送安全速度"""
        target_cmd = Twist()
        target_cmd.linear.x = self.current_linear
        target_cmd.angular.z = self.current_angular
        
        # 通过避障获取安全速度
        safe_cmd = self.obstacle_monitor.get_safe_velocity(target_cmd)
        self.cmd_pub.publish(safe_cmd)
        
        # 处理ROS回调
        rclpy.spin_once(self, timeout_sec=0)
        
    def move_distance(self, distance, speed=0.2):
        """移动指定距离（带避障）"""
        if distance > 0 and not self.obstacle_monitor.can_move_forward():
            self.get_logger().error('前方有障碍物，无法前进！')
            return False
        if distance < 0 and not self.obstacle_monitor.can_move_backward():
            self.get_logger().error('后方有障碍物，无法后退！')
            return False
            
        duration = abs(distance) / speed
        direction = 1 if distance > 0 else -1
        
        self.current_linear = speed * direction
        
        start_time = time.time()
        while time.time() - start_time < duration:
            if distance > 0 and not self.obstacle_monitor.can_move_forward():
                self.get_logger().warn('移动中被障碍物阻挡！')
                self.current_linear = 0.0
                return False
            if distance < 0 and not self.obstacle_monitor.can_move_backward():
                self.get_logger().warn('后退中被障碍物阻挡！')
                self.current_linear = 0.0
                return False
            time.sleep(0.05)
            
        self.current_linear = 0.0
        return True
        
    def rotate_angle(self, angle, speed=0.5):
        """旋转指定角度（带避障）"""
        if angle > 0 and not self.obstacle_monitor.can_turn_left():
            self.get_logger().error('左方有障碍物，无法左转！')
            return False
        if angle < 0 and not self.obstacle_monitor.can_turn_right():
            self.get_logger().error('右方有障碍物，无法右转！')
            return False
            
        angle_rad = abs(angle) * 3.14159 / 180.0
        duration = angle_rad / speed
        direction = 1 if angle > 0 else -1
        
        self.current_angular = speed * direction
        
        start_time = time.time()
        while time.time() - start_time < duration:
            if angle > 0 and not self.obstacle_monitor.can_turn_left():
                self.get_logger().warn('旋转中被障碍物阻挡！')
                self.current_angular = 0.0
                return False
            if angle < 0 and not self.obstacle_monitor.can_turn_right():
                self.get_logger().warn('旋转中被障碍物阻挡！')
                self.current_angular = 0.0
                return False
            time.sleep(0.05)
            
        self.current_angular = 0.0
        return True
        
    def wave_hand(self):
        """挥手动作"""
        self.get_logger().info('执行挥手动作')
        msg = String()
        msg.data = 'wave_hand'
        self.arm_pub.publish(msg)
        time.sleep(3)
        
    def nod_head(self):
        """点头动作"""
        self.get_logger().info('执行点头动作')
        msg = String()
        msg.data = 'nod'
        self.arm_pub.publish(msg)
        time.sleep(2)
        
    def execute(self):
        """执行复合动作"""
        self.get_logger().info('=' * 60)
        self.get_logger().info('开始执行复合动作 Skill')
        self.get_logger().info('=' * 60)
        
        # 等待激光雷达就绪
        self.get_logger().info('等待传感器就绪...')
        timeout = 0
        while timeout < 50:
            info = self.obstacle_monitor.get_obstacle_info()
            if info['front'] != float('inf'):
                break
            time.sleep(0.1)
            timeout += 1
            
        info = self.obstacle_monitor.get_obstacle_info()
        self.get_logger().info(f"前方: {info['front']:.2f}m, 左方: {info['left']:.2f}m, 右方: {info['right']:.2f}m")
        
        # ===== 步骤1：前进1米 + 挥手 =====
        self.get_logger().info('\n【Skill Action 1/4】前进1米 + 挥手')
        
        wave_thread = threading.Thread(target=self.wave_hand)
        wave_thread.start()
        
        if not self.move_distance(1.0):
            self.get_logger().error('前进被阻挡，终止任务')
            return False
            
        # ===== 步骤2：右转360度（挥手继续） =====
        self.get_logger().info('【Skill Action 2/4】向右旋转360度')
        
        if not self.rotate_angle(-360):
            self.get_logger().warn('旋转被阻挡')
            
        wave_thread.join()
        
        # ===== 步骤3：左转 + 前进1米 + 点头 =====
        self.get_logger().info('【Skill Action 3/4】左转 + 前进1米 + 点头')
        
        if not self.rotate_angle(90):
            self.get_logger().warn('左转被阻挡')
            
        if not self.move_distance(1.0):
            self.get_logger().error('前进被阻挡')
            
        self.nod_head()
        
        # ===== 步骤4：原路返回 =====
        self.get_logger().info('【Skill Action 4/4】原路返回')
        
        if not self.move_distance(-1.0):
            self.get_logger().warn('后退被阻挡')
            
        if not self.rotate_angle(-90):
            self.get_logger().warn('右转被阻挡')
            
        if not self.move_distance(-1.0):
            self.get_logger().warn('后退被阻挡')
            
        self.get_logger().info('\n' + '=' * 60)
        self.get_logger().info('复合动作 Skill 执行完成！')
        self.get_logger().info('=' * 60)
        
        return True


def main(args=None):
    rclpy.init(args=args)
    
    try:
        skill = ComplexWaveReturnSkill()
        skill.execute()
    except KeyboardInterrupt:
        pass
    finally:
        skill.current_linear = 0.0
        skill.current_angular = 0.0
        skill.send_velocity()
        skill.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
