#!/usr/bin/env python3
"""
复合动作演示
执行指令：前进2米开始挥手，挥手时同步向左旋转360度然后右转前进一米点头，最后原路返回

作者: gitwangkai
日期: 2026-04-07
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys
import os
import time
import threading

# 添加避障skill路径
sys.path.insert(0, '/home/aidlux/skills/obstacle_avoidance/src')
sys.path.insert(0, '/home/aidlux/skills/action_runner')

from obstacle_monitor import ObstacleMonitor


class ComplexActionDemo(Node):
    """复合动作演示节点"""
    
    def __init__(self):
        super().__init__('complex_action_demo')
        
        # 避障监控器
        self.obstacle_monitor = ObstacleMonitor(
            safety_distance=0.5,
            slow_distance=1.0,
            max_linear_speed=0.3,  # 降低速度保证安全
            max_angular_speed=0.5
        )
        
        # 发布速度命令（海尔系统话题）
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel_remote_ctrl', 10)
        
        # 动作发布（用于触发挥手、点头等）
        self.action_pub = self.create_publisher(String, '/robot_action', 10)
        
        # 当前速度
        self.current_linear = 0.0
        self.current_angular = 0.0
        
        # 定时器（10Hz发布速度）
        self.cmd_timer = self.create_timer(0.1, self.send_velocity)
        
        self.get_logger().info('复合动作演示节点已启动')
        self.get_logger().info('执行指令：前进2米开始挥手，挥手时同步向左旋转360度然后右转前进一米点头，最后原路返回')
        
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
        """
        移动指定距离（带避障检查）
        
        Args:
            distance: 距离（米），正数前进，负数后退
            speed: 速度（m/s）
        """
        if distance > 0 and not self.obstacle_monitor.can_move_forward():
            self.get_logger().warn('前方有障碍物，无法前进！')
            return False
        if distance < 0 and not self.obstacle_monitor.can_move_backward():
            self.get_logger().warn('后方有障碍物，无法后退！')
            return False
            
        # 计算时间
        duration = abs(distance) / speed
        direction = 1 if distance > 0 else -1
        
        self.get_logger().info(f'移动 {distance}米，预计 {duration:.1f}秒')
        
        # 开始移动
        self.current_linear = speed * direction
        
        start_time = time.time()
        while time.time() - start_time < duration:
            # 检查障碍物
            if distance > 0 and not self.obstacle_monitor.can_move_forward():
                self.get_logger().warn('移动中被障碍物阻挡，停止！')
                self.current_linear = 0.0
                return False
            if distance < 0 and not self.obstacle_monitor.can_move_backward():
                self.get_logger().warn('后退中被障碍物阻挡，停止！')
                self.current_linear = 0.0
                return False
            time.sleep(0.05)
            
        # 停止
        self.current_linear = 0.0
        self.get_logger().info('移动完成')
        return True
        
    def rotate_angle(self, angle, speed=0.3):
        """
        旋转指定角度（带避障检查）
        
        Args:
            angle: 角度（度），正数左转，负数右转
            speed: 角速度（rad/s）
        """
        if angle > 0 and not self.obstacle_monitor.can_turn_left():
            self.get_logger().warn('左方有障碍物，无法左转！')
            return False
        if angle < 0 and not self.obstacle_monitor.can_turn_right():
            self.get_logger().warn('右方有障碍物，无法右转！')
            return False
            
        # 计算时间
        angle_rad = abs(angle) * 3.14159 / 180.0
        duration = angle_rad / speed
        direction = 1 if angle > 0 else -1
        
        self.get_logger().info(f'旋转 {angle}度，预计 {duration:.1f}秒')
        
        # 开始旋转
        self.current_angular = speed * direction
        
        start_time = time.time()
        while time.time() - start_time < duration:
            # 检查障碍物
            if angle > 0 and not self.obstacle_monitor.can_turn_left():
                self.get_logger().warn('旋转中被障碍物阻挡，停止！')
                self.current_angular = 0.0
                return False
            if angle < 0 and not self.obstacle_monitor.can_turn_right():
                self.get_logger().warn('旋转中被障碍物阻挡，停止！')
                self.current_angular = 0.0
                return False
            time.sleep(0.05)
            
        # 停止
        self.current_angular = 0.0
        self.get_logger().info('旋转完成')
        return True
        
    def wave_hand(self):
        """挥手动作"""
        self.get_logger().info('执行挥手动作')
        action_msg = String()
        action_msg.data = 'wave_hand'
        self.action_pub.publish(action_msg)
        time.sleep(3)  # 挥手持续3秒
        
    def nod_head(self):
        """点头动作"""
        self.get_logger().info('执行点头动作')
        action_msg = String()
        action_msg.data = 'nod'
        self.action_pub.publish(action_msg)
        time.sleep(2)
        
    def execute_complex_action(self):
        """执行复合动作"""
        self.get_logger().info('=' * 60)
        self.get_logger().info('开始执行复合动作')
        self.get_logger().info('=' * 60)
        
        # 步骤1：前进2米 + 开始挥手
        self.get_logger().info('\n【步骤1】前进2米并挥手')
        
        # 创建挥手线程（并行执行）
        wave_thread = threading.Thread(target=self.wave_hand)
        wave_thread.start()
        
        # 同时前进2米
        if not self.move_distance(2.0, speed=0.2):
            self.get_logger().error('前进被阻挡，任务终止')
            return False
            
        wave_thread.join()
        
        # 步骤2：向左旋转360度
        self.get_logger().info('\n【步骤2】向左旋转360度')
        if not self.rotate_angle(360, speed=0.5):
            self.get_logger().error('旋转被阻挡')
            
        # 步骤3：右转并前进1米
        self.get_logger().info('\n【步骤3】右转并前进1米')
        # 先右转90度
        if not self.rotate_angle(-90, speed=0.5):
            self.get_logger().warn('右转被阻挡，尝试继续前进')
            
        # 前进1米
        if not self.move_distance(1.0, speed=0.2):
            self.get_logger().error('前进被阻挡')
            
        # 步骤4：点头
        self.get_logger().info('\n【步骤4】点头')
        self.nod_head()
        
        # 步骤5：原路返回
        self.get_logger().info('\n【步骤5】原路返回')
        
        # 后退1米
        if not self.move_distance(-1.0, speed=0.2):
            self.get_logger().warn('后退被阻挡')
            
        # 左转90度（恢复方向）
        if not self.rotate_angle(90, speed=0.5):
            self.get_logger().warn('左转被阻挡')
            
        # 后退2米
        if not self.move_distance(-2.0, speed=0.2):
            self.get_logger().warn('后退被阻挡')
            
        self.get_logger().info('\n' + '=' * 60)
        self.get_logger().info('复合动作执行完成！')
        self.get_logger().info('=' * 60)
        
        return True
        
    def run(self):
        """主运行函数"""
        # 等待激光雷达数据
        self.get_logger().info('等待激光雷达数据...')
        timeout = 0
        while timeout < 50:
            info = self.obstacle_monitor.get_obstacle_info()
            if info['front'] != float('inf'):
                self.get_logger().info('激光雷达已就绪')
                break
            time.sleep(0.1)
            timeout += 1
        else:
            self.get_logger().error('激光雷达未就绪，退出')
            return
            
        # 显示初始状态
        info = self.obstacle_monitor.get_obstacle_info()
        self.get_logger().info(f"前方距离: {info['front']:.2f}m")
        self.get_logger().info(f"左方距离: {info['left']:.2f}m")
        self.get_logger().info(f"右方距离: {info['right']:.2f}m")
        
        # 执行复合动作
        self.execute_complex_action()


def main(args=None):
    """主函数"""
    rclpy.init(args=args)
    
    try:
        demo = ComplexActionDemo()
        demo.run()
    except KeyboardInterrupt:
        pass
    finally:
        # 确保停止
        demo.current_linear = 0.0
        demo.current_angular = 0.0
        demo.send_velocity()
        demo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
