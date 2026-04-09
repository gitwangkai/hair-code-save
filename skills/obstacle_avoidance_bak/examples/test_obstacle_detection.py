#!/usr/bin/env python3
"""
避障功能测试脚本
测试避障监控器的各项功能

使用方法：
python3 test_obstacle_detection.py
"""

import rclpy
import sys
import os
import time

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from obstacle_monitor import ObstacleMonitor


def test_obstacle_monitor():
    """测试避障监控器"""
    rclpy.init()
    
    print("=" * 60)
    print("避障功能测试")
    print("=" * 60)
    print()
    
    # 创建避障监控器
    monitor = ObstacleMonitor(
        safety_distance=0.5,
        slow_distance=1.0
    )
    
    print("【测试1】障碍物检测")
    print("等待激光雷达数据...")
    
    # 等待数据
    timeout = 0
    while timeout < 50:  # 5秒超时
        rclpy.spin_once(monitor, timeout_sec=0.1)
        
        info = monitor.get_obstacle_info()
        if info['front'] != float('inf'):
            print(f"✓ 激光雷达数据已接收")
            print(f"  前方距离: {info['front']:.2f}m")
            print(f"  左方距离: {info['left']:.2f}m")
            print(f"  右方距离: {info['right']:.2f}m")
            break
        timeout += 1
    else:
        print("✗ 超时：未收到激光雷达数据")
        print("  请检查激光雷达是否已启动")
        return
        
    print()
    print("【测试2】安全状态检查")
    
    can_forward = monitor.can_move_forward()
    can_left = monitor.can_turn_left()
    can_right = monitor.can_turn_right()
    
    print(f"  可以前进: {can_forward}")
    print(f"  可以左转: {can_left}")
    print(f"  可以右转: {can_right}")
    
    print()
    print("【测试3】安全速度计算")
    
    from geometry_msgs.msg import Twist
    
    # 测试前进
    cmd = Twist()
    cmd.linear.x = 0.5
    safe_cmd = monitor.get_safe_velocity(cmd)
    
    print(f"  输入线速度: 0.5 m/s")
    print(f"  安全线速度: {safe_cmd.linear.x:.2f} m/s")
    
    if safe_cmd.linear.x < cmd.linear.x:
        print("  ✓ 已自动减速")
    elif safe_cmd.linear.x == 0:
        print("  ✓ 已自动停止（前方有障碍物）")
    else:
        print("  ✓ 正常行驶")
        
    print()
    print("【测试4】动态参数调整")
    
    old_safety = monitor.safety_distance
    monitor.safety_distance = 0.8
    
    print(f"  原安全距离: {old_safety}m")
    print(f"  新安全距离: {monitor.safety_distance}m")
    print("  ✓ 参数已更新")
    
    # 恢复
    monitor.safety_distance = old_safety
    
    print()
    print("【测试5】持续监测（10秒）")
    print("按 Ctrl+C 提前结束")
    print()
    
    start_time = time.time()
    try:
        while time.time() - start_time < 10:
            rclpy.spin_once(monitor, timeout_sec=0.1)
            
            info = monitor.get_obstacle_info()
            status = "⚠️ 障碍物!" if info['detected'] else "✓ 安全"
            
            print(f"\r前方: {info['front']:.2f}m | "
                  f"左方: {info['left']:.2f}m | "
                  f"右方: {info['right']:.2f}m | {status}", 
                  end='', flush=True)
                  
    except KeyboardInterrupt:
        pass
        
    print()
    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)
    
    monitor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    test_obstacle_monitor()
