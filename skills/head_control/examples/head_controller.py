#!/usr/bin/env python3
"""
显示器云台控制器封装类 - 基于实际测试验证

使用：
    from head_controller import HeadController
    
    head = HeadController()
    head.move_to(-3.1)    # 抬头
    head.move_to(-3.6)    # 低头
    head.nod(3)           # 点头3次
    head.destroy()
"""
import rclpy
from std_msgs.msg import Float32
import time


class HeadController:
    """
    显示器云台控制器 - 基于实际测试验证
    
    坐标系说明（已验证）：
    - 上限/抬头：-3.0 rad
    - 中间位置：-3.35 rad
    - 下限/低头：-3.7 rad
    
    运动方向：
    - 数值增大（-3.7 → -3.0）= 抬头
    - 数值减小（-3.0 → -3.7）= 低头
    """
    
    # 实际限位（弧度）- 已验证
    UPPER_LIMIT = -3.008   # 最大抬头
    LOWER_LIMIT = -3.709   # 最大低头
    CENTER = -3.35         # 中间位置
    
    def __init__(self):
        rclpy.init()
        self.node = rclpy.create_node('head_controller')
        self.publisher = self.node.create_publisher(
            Float32, '/target_head_position', 10)
        self.current_position = self.CENTER
    
    def move_to(self, angle_rad, duration=0.5):
        """
        移动到指定角度
        
        Args:
            angle_rad: 目标角度（弧度）
                      -3.0 = 最大抬头, -3.7 = 最大低头
            duration: 动画持续时间（秒）
        """
        # 限位检查
        angle_rad = max(self.LOWER_LIMIT, min(self.UPPER_LIMIT, angle_rad))
        
        msg = Float32()
        msg.data = float(angle_rad)
        
        # 持续发送确保执行
        steps = int(duration * 20)
        for _ in range(steps):
            self.publisher.publish(msg)
            time.sleep(0.05)
        
        self.current_position = angle_rad
    
    def look_up(self, angle_deg=10, duration=0.5):
        """
        抬头
        
        Args:
            angle_deg: 抬头角度（相对当前位置）
        """
        import math
        target = self.current_position + (angle_deg * math.pi / 180)
        target = min(target, self.UPPER_LIMIT)
        self.move_to(target, duration)
    
    def look_down(self, angle_deg=10, duration=0.5):
        """
        低头
        
        Args:
            angle_deg: 低头角度（相对当前位置）
        """
        import math
        target = self.current_position - (angle_deg * math.pi / 180)
        target = max(target, self.LOWER_LIMIT)
        self.move_to(target, duration)
    
    def look_center(self, duration=0.5):
        """归中"""
        self.move_to(self.CENTER, duration)
    
    def nod(self, times=3, duration=1.0):
        """
        点头动作
        
        Args:
            times: 点头次数
            duration: 单次点头时间
        """
        for i in range(times):
            # 低头
            self.move_to(self.CENTER - 0.2, duration / 2)
            time.sleep(0.2)
            # 抬头
            self.move_to(self.CENTER + 0.2, duration / 2)
            time.sleep(0.2)
        
        # 归中
        self.look_center()
    
    def destroy(self):
        """清理资源"""
        self.look_center()
        self.node.destroy_node()
        rclpy.shutdown()


def demo():
    """演示"""
    print("=" * 50)
    print("显示器云台控制演示")
    print("=" * 50)
    print("坐标系：-3.0=抬头, -3.7=低头, -3.35=中间")
    
    head = HeadController()
    
    try:
        print("\n1. 抬头到 -3.1...")
        head.move_to(-3.1)
        time.sleep(1)
        
        print("\n2. 低头到 -3.6...")
        head.move_to(-3.6)
        time.sleep(1)
        
        print("\n3. 归中...")
        head.look_center()
        time.sleep(0.5)
        
        print("\n4. 点头 3 次...")
        head.nod(3)
        
        print("\n5. 归中...")
        head.look_center()
        
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
    finally:
        head.destroy()
        print("\n✓ 演示完成")


if __name__ == '__main__':
    demo()
