#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超声波感知 + 底盘控制 集成示例
演示如何在移动中使用前向超声波进行避障
"""

import sys
import time
sys.path.insert(0, '/home/aidlux/skills/ultrasonic_perception')
sys.path.insert(0, '/home/aidlux/skills/chassis_control')

from ultrasonic_perception import UltrasonicPerception
from chassis_control import ChassisControl


class SafeNavigator:
    """
    安全导航器 - 结合超声波感知和底盘控制
    实现带避障的前向移动功能
    """
    
    def __init__(self):
        print("=" * 50)
        print("初始化安全导航器...")
        print("=" * 50)
        
        self.perception = UltrasonicPerception()
        self.chassis = ChassisControl()
        
        # 安全参数
        self.SAFETY_DISTANCE = 0.5   # 安全距离 0.5m
        self.DANGER_DISTANCE = 0.3   # 危险距离 0.3m
        self.CAUTION_DISTANCE = 0.6  # 警告距离 0.6m
        
        print("✓ 初始化完成\n")
    
    def check_front_safe(self) -> bool:
        """检查前方是否安全"""
        dist = self.perception.get_distance()
        if dist is None:
            print("  [警告] 传感器无数据，保守判断为不安全")
            return False
        return dist >= self.SAFETY_DISTANCE
    
    def safe_forward(self, distance: float, speed: float = 0.2) -> bool:
        """
        安全前进 - 带避障检测
        
        Args:
            distance: 目标距离(米)
            speed: 速度(m/s)
        
        Returns:
            bool: 是否成功到达目标
        """
        print(f"\n【安全前进】目标: {distance}m, 速度: {speed}m/s")
        print("-" * 40)
        
        # 检查初始状态
        if not self.check_front_safe():
            front_dist = self.perception.get_distance()
            print(f"  ✗ 初始状态不安全，前方距离: {front_dist:.2f}m")
            return False
        
        # 计算预计时间
        duration = distance / speed
        start_time = time.time()
        check_interval = 0.1  # 每100ms检查一次
        
        # 开始移动
        self.chassis.move(speed, 0.0)
        
        try:
            while time.time() - start_time < duration:
                # 检查障碍物
                front_dist = self.perception.get_distance()
                
                if front_dist and front_dist < self.DANGER_DISTANCE:
                    # 紧急停止
                    self.chassis.stop()
                    print(f"  ✗ 紧急停止! 障碍物距离: {front_dist:.2f}m")
                    return False
                
                if front_dist and front_dist < self.CAUTION_DISTANCE:
                    # 减速
                    self.chassis.move(speed * 0.5, 0.0)
                    print(f"  ⚠ 减速行驶，前方距离: {front_dist:.2f}m")
                
                time.sleep(check_interval)
            
            # 到达目标
            self.chassis.stop()
            print(f"  ✓ 安全到达目标位置")
            return True
            
        except KeyboardInterrupt:
            self.chassis.stop()
            print(f"  ✗ 用户中断")
            return False
    
    def demo_safe_movement(self):
        """演示安全移动"""
        print(f"\n{'=' * 50}")
        print("安全移动演示")
        print(f"{'=' * 50}")
        
        # 显示初始状态
        print("\n初始传感器状态:")
        print(self.perception.get_status_report())
        
        # 演示1: 安全前进
        input("\n按回车开始【安全前进1米】...")
        self.safe_forward(1.0, speed=0.2)
        
        time.sleep(1)
        
        # 演示2: 旋转
        input("\n按回车开始【旋转360°】...")
        self.chassis.rotate(360)
        
        print(f"\n{'=' * 50}")
        print("演示完成")
        print(f"{'=' * 50}")
    
    def close(self):
        """关闭导航器"""
        print("\n关闭安全导航器...")
        self.chassis.stop()
        self.perception.close()
        self.chassis.destroy_node()
        print("✓ 已关闭")


def main():
    """主程序"""
    navigator = SafeNavigator()
    
    try:
        print("""
请选择演示模式:
  1. 安全前进演示
  2. 实时状态监控
  0. 退出
        """)
        
        choice = input("请输入选项 (0-2): ").strip()
        
        if choice == '1':
            navigator.demo_safe_movement()
        elif choice == '2':
            print("\n实时状态监控 (按Ctrl+C停止)...")
            try:
                while True:
                    print("\033[2J\033[H")
                    print(navigator.perception.get_status_report())
                    time.sleep(0.5)
            except KeyboardInterrupt:
                print("\n监控已停止")
        else:
            print("退出")
            
    finally:
        navigator.close()


if __name__ == "__main__":
    main()
