#!/usr/bin/env python3
"""
机械臂运动控制脚本 (ROS2版本)
目标：移动到 [10, 10, 10, 10, 30, 10] 然后归位到 [0, 0, 0, 0, 0, 0]
"""

import sys
import time
import rclpy
from rclpy.node import Node
from arm_control_interface.srv import SetPower
from arm_control_interface.msg import ArmRtCtrlCmd
from arm_control_interface.action import ArmRtCtrl
from rclpy.action import ActionClient
from std_msgs.msg import Header

# 目标位置
TARGET_POSE = [10.0, 10.0, 10.0, 10.0, 30.0, 10.0]
HOME_POSE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')
        self.ns = 'wy_robot1'
        
        # 创建发布者、客户端
        self.rt_pub = self.create_publisher(ArmRtCtrlCmd, f'/{self.ns}/A6_rt_control_cmd', 10)
        self.power_client = self.create_client(SetPower, f'/{self.ns}/A6_set_power')
        self.rt_action_client = ActionClient(self, ArmRtCtrl, f'/{self.ns}/A6_rt_control_action')
        
        self.rt_active = False
        self.rt_goal_handle = None
        
    def set_power(self, enable: bool, timeout: float = 5.0):
        """设置电源开关"""
        self.get_logger().info(f'设置电源: {"ON" if enable else "OFF"}')
        
        if not self.power_client.wait_for_service(timeout_sec=timeout):
            return False, '服务不可用'
        
        req = SetPower.Request()
        req.power_enable = enable
        
        future = self.power_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=timeout)
        
        if future.result() is None:
            return False, '调用失败'
        
        res = future.result()
        return res.success, res.error if hasattr(res, 'error') else ''
    
    def start_rt_control(self, timeout: float = 5.0):
        """启动实时控制"""
        self.get_logger().info('启动实时控制...')
        
        if not self.rt_action_client.wait_for_server(timeout_sec=timeout):
            return False, '动作服务器不可用'
        
        goal_msg = ArmRtCtrl.Goal()
        goal_msg.rt_control_type = 'MotionJoint'
        
        send_goal_future = self.rt_action_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_goal_future, timeout_sec=timeout)
        
        goal_handle = send_goal_future.result()
        if not goal_handle or not goal_handle.accepted:
            return False, '目标被拒绝'
        
        self.rt_goal_handle = goal_handle
        self.rt_active = True
        self.get_logger().info('实时控制已启动')
        return True, 'ok'
    
    def stop_rt_control(self, timeout: float = 5.0):
        """停止实时控制"""
        if self.rt_goal_handle is not None:
            self.get_logger().info('停止实时控制...')
            cancel_future = self.rt_goal_handle.cancel_goal_async()
            rclpy.spin_until_future_complete(self, cancel_future, timeout_sec=timeout)
            self.rt_active = False
            self.rt_goal_handle = None
        return True, 'ok'
    
    def move_to(self, angles, duration=3.0):
        """移动到指定角度"""
        self.get_logger().info(f'移动到: {angles}')
        
        # 发送目标角度
        msg = ArmRtCtrlCmd()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_angles = list(angles)
        
        # 持续发送一段时间
        start_time = time.time()
        rate = self.create_rate(50)  # 50Hz
        
        while time.time() - start_time < duration and rclpy.ok():
            msg.header.stamp = self.get_clock().now().to_msg()
            self.rt_pub.publish(msg)
            rate.sleep()
        
        self.get_logger().info(f'移动完成')
        return True


def main():
    print("=" * 50)
    print("海尔机器人 NX-7 机械臂运动控制 (ROS2)")
    print("=" * 50)
    
    rclpy.init()
    controller = ArmController()
    
    try:
        # 1. 设置电源
        print("\n[1/5] 开启电源...")
        ok, msg = controller.set_power(True)
        if not ok:
            print(f"[错误] 电源开启失败: {msg}")
            return 1
        print("电源已开启")
        time.sleep(2)
        
        # 2. 启动实时控制
        print("\n[2/5] 启动实时控制...")
        ok, msg = controller.start_rt_control()
        if not ok:
            print(f"[错误] 启动实时控制失败: {msg}")
            return 1
        print("实时控制已启动")
        time.sleep(1)
        
        # 3. 移动到目标位置
        print(f"\n[3/5] 移动到目标位置: {TARGET_POSE}")
        controller.move_to(TARGET_POSE, duration=5.0)
        print("已到达目标位置")
        time.sleep(2)
        
        # 4. 归位
        print(f"\n[4/5] 归位到: {HOME_POSE}")
        controller.move_to(HOME_POSE, duration=5.0)
        print("已归位")
        time.sleep(1)
        
        # 5. 关闭
        print("\n[5/5] 关闭电源...")
        controller.stop_rt_control()
        ok, msg = controller.set_power(False)
        print("电源已关闭")
        
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"\n[错误] {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.destroy_node()
        rclpy.shutdown()
    
    print("\n" + "=" * 50)
    print("运动序列执行完成")
    print("=" * 50)
    return 0


if __name__ == '__main__':
    sys.exit(main())
