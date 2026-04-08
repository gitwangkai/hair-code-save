#!/usr/bin/env python3
"""
自然语言 Skill 调用器（修复版）
通过自然语言指令调用机器人 Skills

修复内容：
- 适配重构后的 ObstacleMonitor（非 Node 类）
- 避免 ROS2 Node 嵌套实例化问题

示例:
- "前进1米开始挥手，挥手时同步向右旋转360度然后左转前进一米点头，最后原路返回"

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

sys.path.insert(0, '/home/aidlux/skills/obstacle_avoidance/src')
from obstacle_monitor import ObstacleMonitor


class NLPSkillCaller(Node):
    """自然语言 Skill 调用器"""
    
    def __init__(self):
        super().__init__('nlp_skill_caller')
        
        # 初始化避障监控器（传入 self 作为父 node）
        self.obstacle_monitor = ObstacleMonitor(
            parent_node=self,
            safety_distance=0.5,
            slow_distance=1.0,
            max_linear_speed=0.3,
            max_angular_speed=0.5
        )
        
        # 发布器
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel_remote_ctrl', 10)
        self.arm_pub = self.create_publisher(String, '/arm_action', 10)
        
        # 当前速度
        self.current_linear = 0.0
        self.current_angular = 0.0
        
        # 速度发布定时器（10Hz）
        self.cmd_timer = self.create_timer(0.1, self.send_velocity)
        
        # 避障监控定时器（10Hz）
        self.obstacle_timer = self.create_timer(0.1, self.obstacle_monitor.spin_once)
        
        self.get_logger().info('='*60)
        self.get_logger().info('自然语言 Skill 调用器已启动')
        self.get_logger().info('='*60)
        
    def send_velocity(self):
        """发送安全速度"""
        target_cmd = Twist()
        target_cmd.linear.x = self.current_linear
        target_cmd.angular.z = self.current_angular
        safe_cmd = self.obstacle_monitor.get_safe_velocity(target_cmd)
        self.cmd_pub.publish(safe_cmd)
        
    # ==================== 底层 Skills ====================
    
    def skill_move(self, distance, speed=0.2):
        """移动 Skill: chassis_control/move"""
        direction = "前进" if distance > 0 else "后退"
        self.get_logger().info(f'[Skill:chassis/move] {direction}{abs(distance)}米')
        
        if distance > 0 and not self.obstacle_monitor.can_move_forward():
            self.get_logger().error('前方有障碍物，移动被阻止！')
            return False
        if distance < 0 and not self.obstacle_monitor.can_move_backward():
            self.get_logger().error('后方有障碍物，移动被阻止！')
            return False
            
        duration = abs(distance) / speed
        self.current_linear = speed * (1 if distance > 0 else -1)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            if distance > 0 and not self.obstacle_monitor.can_move_forward():
                self.current_linear = 0.0
                self.get_logger().warn('移动中检测到障碍物，已停止！')
                return False
            if distance < 0 and not self.obstacle_monitor.can_move_backward():
                self.current_linear = 0.0
                self.get_logger().warn('后退中检测到障碍物，已停止！')
                return False
            time.sleep(0.05)
            
        self.current_linear = 0.0
        return True
        
    def skill_rotate(self, angle, speed=0.5):
        """旋转 Skill: chassis_control/rotate"""
        direction = "左转" if angle > 0 else "右转"
        self.get_logger().info(f'[Skill:chassis/rotate] {direction}{abs(angle)}度')
        
        if angle > 0 and not self.obstacle_monitor.can_turn_left():
            self.get_logger().error('左方有障碍物，旋转被阻止！')
            return False
        if angle < 0 and not self.obstacle_monitor.can_turn_right():
            self.get_logger().error('右方有障碍物，旋转被阻止！')
            return False
            
        angle_rad = abs(angle) * 3.14159 / 180.0
        duration = angle_rad / speed
        self.current_angular = speed * (1 if angle > 0 else -1)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            if angle > 0 and not self.obstacle_monitor.can_turn_left():
                self.current_angular = 0.0
                self.get_logger().warn('左转中检测到障碍物，已停止！')
                return False
            if angle < 0 and not self.obstacle_monitor.can_turn_right():
                self.current_angular = 0.0
                self.get_logger().warn('右转中检测到障碍物，已停止！')
                return False
            time.sleep(0.05)
            
        self.current_angular = 0.0
        return True
        
    def skill_wave(self, duration=3):
        """挥手 Skill: arm_control/wave"""
        self.get_logger().info(f'[Skill:arm/wave] 挥手{duration}秒')
        msg = String()
        msg.data = 'wave_hand'
        self.arm_pub.publish(msg)
        time.sleep(duration)
        
    def skill_nod(self, duration=2):
        """点头 Skill: head_control/nod"""
        self.get_logger().info(f'[Skill:head/nod] 点头{duration}秒')
        msg = String()
        msg.data = 'nod'
        self.arm_pub.publish(msg)
        time.sleep(duration)
        
    # ==================== 自然语言执行 ====================
    
    def execute_natural_command(self, command):
        """
        执行自然语言指令
        
        Args:
            command: 自然语言指令字符串
        """
        self.get_logger().info('')
        self.get_logger().info('='*60)
        self.get_logger().info(f'自然语言指令: "{command}"')
        self.get_logger().info('='*60)
        
        # 等待传感器
        self._wait_for_sensors()
        
        # 解析指令关键词并执行
        cmd = command.lower()
        
        # 步骤1: 前进1米 + 挥手
        if any(kw in cmd for kw in ['前进', '走']) and any(kw in cmd for kw in ['挥手', '摆手']):
            self._step1_move_and_wave()
            
        # 步骤2: 向右旋转360度 (挥手时)
        if any(kw in cmd for kw in ['右转', '向右']) and '360' in cmd:
            self._step2_rotate_right_360()
            
        # 步骤3: 左转 + 前进1米 + 点头
        if any(kw in cmd for kw in ['左转', '向左']):
            self._step3_left_move_nod()
            
        # 步骤4: 返回
        if any(kw in cmd for kw in ['返回', '回去', '原路']):
            self._step4_return()
            
        self.get_logger().info('')
        self.get_logger().info('='*60)
        self.get_logger().info('自然语言指令执行完成！')
        self.get_logger().info('='*60)
        
    def _wait_for_sensors(self):
        """等待传感器就绪"""
        self.get_logger().info('[System] 等待传感器就绪...')
        timeout = 0
        while timeout < 50:
            info = self.obstacle_monitor.get_obstacle_info()
            if info['front'] != float('inf'):
                break
            time.sleep(0.1)
            timeout += 1
            
        info = self.obstacle_monitor.get_obstacle_info()
        self.get_logger().info(f"[Sensor] 前:{info['front']:.1f}m 左:{info['left']:.1f}m 右:{info['right']:.1f}m")
        
    def _step1_move_and_wave(self):
        """步骤1: 前进1米 + 开始挥手"""
        self.get_logger().info('')
        self.get_logger().info('【步骤1】前进1米 + 挥手')
        
        # 启动挥手线程
        wave_thread = threading.Thread(target=self.skill_wave, args=(3,))
        wave_thread.start()
        
        # 前进1米
        success = self.skill_move(1.0)
        return success, wave_thread
        
    def _step2_rotate_right_360(self):
        """步骤2: 向右旋转360度 (挥手继续)"""
        self.get_logger().info('')
        self.get_logger().info('【步骤2】向右旋转360度（挥手继续）')
        
        # 右转360度
        self.skill_rotate(-360)
        
    def _step3_left_move_nod(self):
        """步骤3: 左转 + 前进1米 + 点头"""
        self.get_logger().info('')
        self.get_logger().info('【步骤3】左转 + 前进1米 + 点头')
        
        # 左转90度
        self.skill_rotate(90)
        
        # 前进1米
        self.skill_move(1.0)
        
        # 点头
        self.skill_nod()
        
    def _step4_return(self):
        """步骤4: 原路返回"""
        self.get_logger().info('')
        self.get_logger().info('【步骤4】原路返回')
        
        # 后退1米
        self.skill_move(-1.0)
        
        # 右转90度（恢复方向）
        self.skill_rotate(-90)
        
        # 后退1米
        self.skill_move(-1.0)


def main(args=None):
    rclpy.init(args=args)
    
    caller = NLPSkillCaller()
    
    # 直接执行指令
    caller.execute_natural_command(
        "前进1米开始挥手，挥手时同步向右旋转360度然后左转前进一米点头，最后原路返回"
    )
    
    try:
        rclpy.spin(caller)
    except KeyboardInterrupt:
        pass
    finally:
        # 确保停止
        caller.current_linear = 0.0
        caller.current_angular = 0.0
        caller.send_velocity()
        caller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
