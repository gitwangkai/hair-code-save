#!/usr/bin/env python3
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
    def __init__(self):
        super().__init__('nlp_skill_caller')
        self.obstacle_monitor = ObstacleMonitor(
            safety_distance=0.5, slow_distance=1.0,
            max_linear_speed=0.3, max_angular_speed=0.5)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel_remote_ctrl', 10)
        self.arm_pub = self.create_publisher(String, '/arm_action', 10)
        self.current_linear = 0.0
        self.current_angular = 0.0
        self.cmd_timer = self.create_timer(0.1, self.send_velocity)
        self.get_logger().info('自然语言 Skill 调用器已启动')
        
    def send_velocity(self):
        target_cmd = Twist()
        target_cmd.linear.x = self.current_linear
        target_cmd.angular.z = self.current_angular
        safe_cmd = self.obstacle_monitor.get_safe_velocity(target_cmd)
        self.cmd_pub.publish(safe_cmd)
        rclpy.spin_once(self, timeout_sec=0)
        
    def skill_move(self, distance, speed=0.2):
        direction = "前进" if distance > 0 else "后退"
        self.get_logger().info(f'[Skill] {direction}{abs(distance)}米')
        if distance > 0 and not self.obstacle_monitor.can_move_forward():
            self.get_logger().error('前方有障碍物！')
            return False
        duration = abs(distance) / speed
        self.current_linear = speed * (1 if distance > 0 else -1)
        start_time = time.time()
        while time.time() - start_time < duration:
            if distance > 0 and not self.obstacle_monitor.can_move_forward():
                self.current_linear = 0.0
                return False
            time.sleep(0.05)
        self.current_linear = 0.0
        return True
        
    def skill_rotate(self, angle, speed=0.5):
        direction = "左转" if angle > 0 else "右转"
        self.get_logger().info(f'[Skill] {direction}{abs(angle)}度')
        if angle > 0 and not self.obstacle_monitor.can_turn_left():
            self.get_logger().error('左方有障碍物！')
            return False
        angle_rad = abs(angle) * 3.14159 / 180.0
        duration = angle_rad / speed
        self.current_angular = speed * (1 if angle > 0 else -1)
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(0.05)
        self.current_angular = 0.0
        return True
        
    def skill_wave(self, duration=3):
        self.get_logger().info(f'[Skill] 挥手{duration}秒')
        msg = String()
        msg.data = 'wave_hand'
        self.arm_pub.publish(msg)
        time.sleep(duration)
        
    def skill_nod(self, duration=2):
        self.get_logger().info(f'[Skill] 点头{duration}秒')
        msg = String()
        msg.data = 'nod'
        self.arm_pub.publish(msg)
        time.sleep(duration)
        
    def execute_natural_command(self, command):
        self.get_logger().info(f'自然语言指令: {command}')
        # 等待传感器
        timeout = 0
        while timeout < 50:
            info = self.obstacle_monitor.get_obstacle_info()
            if info['front'] != float('inf'):
                break
            time.sleep(0.1)
            timeout += 1
        # 执行动作序列
        self.get_logger().info('【步骤1】前进1米 + 挥手')
        wave_thread = threading.Thread(target=self.skill_wave, args=(3,))
        wave_thread.start()
        self.skill_move(1.0)
        self.get_logger().info('【步骤2】向右旋转360度（挥手继续）')
        self.skill_rotate(-360)
        wave_thread.join()
        self.get_logger().info('【步骤3】左转 + 前进1米 + 点头')
        self.skill_rotate(90)
        self.skill_move(1.0)
        self.skill_nod()
        self.get_logger().info('【步骤4】原路返回')
        self.skill_move(-1.0)
        self.skill_rotate(-90)
        self.skill_move(-1.0)
        self.get_logger().info('指令执行完成！')
        
def main(args=None):
    rclpy.init(args=args)
    caller = NLPSkillCaller()
    # 直接执行指令
    caller.execute_natural_command("前进1米开始挥手，挥手时同步向右旋转360度然后左转前进一米点头，最后原路返回")
    try:
        rclpy.spin(caller)
    except KeyboardInterrupt:
        pass
    finally:
        caller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
