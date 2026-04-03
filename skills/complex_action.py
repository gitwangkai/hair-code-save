#!/usr/bin/env python3
"""
复合动作：前进1米 → 挥手+左转360度 → 点头

使用：
    python3 complex_action.py
"""
import subprocess
import time
import sys

def run_command(cmd, desc, timeout=120):
    """执行命令"""
    print(f"\n{'='*50}")
    print(f"【{desc}】")
    print(f"{'='*50}")
    print(f"命令: {cmd}")
    
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"错误: {result.stderr}", file=sys.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"超时！", file=sys.stderr)
        return False
    except Exception as e:
        print(f"异常: {e}", file=sys.stderr)
        return False

def main():
    print("="*60)
    print("复合动作执行")
    print("="*60)
    print("\n动作序列：")
    print("1. 前进1米")
    print("2. 挥手 + 左转360度（同时进行）")
    print("3. 点头")
    
    # 步骤1：前进1米
    print("\n" + "="*60)
    print("【步骤1/3】前进1米")
    print("="*60)
    
    import rclpy
    from geometry_msgs.msg import Twist
    
    rclpy.init()
    node = rclpy.create_node('move_forward_1m')
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    print("前进1米，速度0.3m/s，预计3.3秒...")
    msg = Twist()
    msg.linear.x = 0.3
    
    start = time.time()
    while time.time() - start < 3.3:
        pub.publish(msg)
        time.sleep(0.1)
    
    # 停止
    pub.publish(Twist())
    print("✓ 前进完成")
    node.destroy_node()
    rclpy.shutdown()
    time.sleep(1)
    
    # 步骤2：挥手 + 左转360度（同时进行）
    print("\n" + "="*60)
    print("【步骤2/3】挥手 + 左转360度（同时进行）")
    print("="*60)
    
    # 启动挥手（后台）
    print("启动挥手...")
    wave_proc = subprocess.Popen([
        'python3', '/home/aidlux/human_detection/src/wave_hand_standalone.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 等待挥手连接
    time.sleep(2)
    
    # 同时执行左转360度
    print("启动左转360度...")
    rclpy.init()
    node = rclpy.create_node('rotate_left')
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    print("左转360度，速度0.5rad/s，预计12.6秒...")
    msg = Twist()
    msg.angular.z = 0.5  # 左转
    
    start = time.time()
    while time.time() - start < 12.6:
        pub.publish(msg)
        time.sleep(0.1)
    
    # 停止
    pub.publish(Twist())
    print("✓ 左转完成")
    node.destroy_node()
    rclpy.shutdown()
    
    # 等待挥手完成
    print("等待挥手完成...")
    try:
        wave_proc.wait(timeout=30)
        print("✓ 挥手完成")
    except subprocess.TimeoutExpired:
        print("挥手超时，终止...")
        wave_proc.terminate()
    
    time.sleep(1)
    
    # 步骤3：点头
    print("\n" + "="*60)
    print("【步骤3/3】点头")
    print("="*60)
    
    import rclpy
    from std_msgs.msg import Float32
    
    rclpy.init()
    node = rclpy.create_node('nod_final')
    pub = node.create_publisher(Float32, '/target_head_position', 10)
    
    LOOK_UP = -3.2
    LOOK_DOWN = -3.6
    CENTER = -3.35
    
    print("点头1次...")
    
    # 低头
    print("  低头...")
    msg = Float32()
    msg.data = LOOK_DOWN
    for _ in range(10):
        pub.publish(msg)
        time.sleep(0.05)
    time.sleep(0.3)
    
    # 抬头
    print("  抬头...")
    msg.data = LOOK_UP
    for _ in range(10):
        pub.publish(msg)
        time.sleep(0.05)
    time.sleep(0.3)
    
    # 归中
    print("  归中...")
    msg.data = CENTER
    for _ in range(10):
        pub.publish(msg)
        time.sleep(0.05)
    
    print("✓ 点头完成")
    node.destroy_node()
    rclpy.shutdown()
    
    # 完成
    print("\n" + "="*60)
    print("✓ 复合动作全部完成！")
    print("="*60)
    print("\n执行序列：")
    print("  ✓ 前进1米")
    print("  ✓ 挥手 + 左转360度")
    print("  ✓ 点头")

if __name__ == '__main__':
    main()
