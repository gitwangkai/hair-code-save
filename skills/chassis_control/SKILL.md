# 底盘控制 Skill

> **一句话描述**：基于 ROS2 的机器人底盘运动控制，支持速度控制、里程计反馈和紧急停止。

---

## 能力

- **速度控制**：通过 `/cmd_vel` 发布线速度和角速度
- **里程计反馈**：订阅 `/odom` 获取位置和姿态
- **紧急停止**：快速发送零速度停止底盘
- **运动模式**：支持前进/后退/旋转/弧线运动

---

## 使用场景

| 场景 | 描述 | 示例 |
|------|------|------|
| **原地旋转** | 机器人原地左转/右转 | `rotate.py` |
| **直线行驶** | 前进/后退指定距离 | `move_linear.py` |
| **人体跟随** | 根据目标位置跟随移动 | `tracker.py` |
| **紧急停止** | 立即停止所有运动 | `emergency_stop.py` |

---

## 快速开始

### 1. ROS2 命令行控制

```bash
# 前进 0.5 m/s
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

# 原地左转（0.5 rad/s）
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}"

# 停止
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

### 2. Python 控制

```python
import rclpy
from geometry_msgs.msg import Twist

# 初始化
rclpy.init()
node = rclpy.create_node('chassis_controller')
publisher = node.create_publisher(Twist, '/cmd_vel', 10)

# 创建速度指令
msg = Twist()
msg.linear.x = 0.5   # 前进速度 m/s
msg.angular.z = 0.0  # 旋转速度 rad/s

# 发布
publisher.publish(msg)
```

---

## 详细用法

### 底盘控制器类

```python
#!/usr/bin/env python3
import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time

class ChassisController:
    """底盘控制器"""
    
    def __init__(self):
        rclpy.init()
        self.node = rclpy.create_node('chassis_controller')
        self.cmd_pub = self.node.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.node.create_subscription(
            Odometry, '/odom', self._odom_callback, 10)
        
        self.current_pose = None
        self.current_twist = None
    
    def _odom_callback(self, msg):
        """里程计回调"""
        self.current_pose = msg.pose.pose
        self.current_twist = msg.twist.twist
    
    def move(self, linear_x=0.0, angular_z=0.0, duration=0.0):
        """
        发送速度指令
        
        Args:
            linear_x: 线速度 (m/s)，正为前进，负为后退
            angular_z: 角速度 (rad/s)，正为左转，负为右转
            duration: 持续时间 (秒)，0 表示只发送一次
        """
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = float(angular_z)
        
        if duration > 0:
            # 持续发送
            start_time = time.time()
            while time.time() - start_time < duration:
                self.cmd_pub.publish(msg)
                time.sleep(0.1)
            # 停止
            self.stop()
        else:
            self.cmd_pub.publish(msg)
    
    def stop(self):
        """紧急停止"""
        msg = Twist()  # 全零
        self.cmd_pub.publish(msg)
    
    def rotate(self, angle_deg, speed=0.5):
        """
        旋转指定角度
        
        Args:
            angle_deg: 角度 (度)，正为左转，负为右转
            speed: 角速度 (rad/s)
        """
        angular_z = speed if angle_deg > 0 else -speed
        duration = abs(angle_deg) / (speed * 180 / math.pi)
        self.move(0.0, angular_z, duration)
    
    def move_linear(self, distance_m, speed=0.3):
        """
        直线移动指定距离
        
        Args:
            distance_m: 距离 (米)，正为前进，负为后退
            speed: 速度 (m/s)
        """
        linear_x = speed if distance_m > 0 else -speed
        duration = abs(distance_m) / speed
        self.move(linear_x, 0.0, duration)
    
    def get_pose(self):
        """获取当前位姿"""
        return self.current_pose
    
    def destroy(self):
        """清理资源"""
        self.stop()
        self.node.destroy_node()
        rclpy.shutdown()


# 使用示例
if __name__ == '__main__':
    chassis = ChassisController()
    
    try:
        print("前进 1 米...")
        chassis.move_linear(1.0)
        
        print("左转 90 度...")
        chassis.rotate(90)
        
        print("后退 0.5 米...")
        chassis.move_linear(-0.5)
        
        print("停止")
        chassis.stop()
        
    except KeyboardInterrupt:
        print("\n用户中断")
    finally:
        chassis.destroy()
```

---

## 示例代码

### 示例 1：前进后退

```python
#!/usr/bin/env python3
"""前进后退示例"""
import rclpy
from geometry_msgs.msg import Twist
import time

def main():
    rclpy.init()
    node = rclpy.create_node('move_example')
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    # 前进 2 秒
    print("前进...")
    msg = Twist()
    msg.linear.x = 0.3
    for _ in range(20):  # 2 秒
        pub.publish(msg)
        time.sleep(0.1)
    
    # 停止
    print("停止...")
    pub.publish(Twist())
    time.sleep(1)
    
    # 后退 2 秒
    print("后退...")
    msg.linear.x = -0.3
    for _ in range(20):
        pub.publish(msg)
        time.sleep(0.1)
    
    # 停止
    print("停止")
    pub.publish(Twist())
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 示例 2：原地旋转

```python
#!/usr/bin/env python3
"""原地旋转示例"""
import rclpy
from geometry_msgs.msg import Twist
import time

def rotate(duration=3.0, speed=0.5):
    """
    原地旋转
    
    Args:
        duration: 旋转时间（秒）
        speed: 角速度（rad/s），正为左转，负为右转
    """
    rclpy.init()
    node = rclpy.create_node('rotate_example')
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    print(f"原地旋转 {duration} 秒...")
    msg = Twist()
    msg.angular.z = speed
    
    start = time.time()
    while time.time() - start < duration:
        pub.publish(msg)
        time.sleep(0.1)
    
    # 停止
    pub.publish(Twist())
    print("停止")
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    import sys
    direction = sys.argv[1] if len(sys.argv) > 1 else 'left'
    speed = -0.5 if direction == 'right' else 0.5
    rotate(speed=speed)
```

### 示例 3：紧急停止

```python
#!/usr/bin/env python3
"""紧急停止"""
import rclpy
from geometry_msgs.msg import Twist

def emergency_stop():
    """发送紧急停止指令"""
    rclpy.init()
    node = rclpy.create_node('emergency_stop')
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    # 连续发送多次确保停止
    stop_msg = Twist()
    for _ in range(5):
        pub.publish(stop_msg)
    
    print("[紧急停止] 已发送")
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    emergency_stop()
```

---

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 底盘不响应 | 底盘电源未开启 | 检查 CAN 总线电源 (`data[1]=1`) |
| 运动抖动 | 指令发送频率过低 | 保持 10Hz 以上发送频率 |
| 漂移严重 | 里程计未校准 | 检查 `/odom` 话题数据 |
| 无法停止 | 指令未送达 | 连续发送多次停止指令 |
| 旋转不准 | 地面摩擦力不均 | 降低旋转速度 |

---

## 注意事项

1. **安全优先**：
   - 底盘运动前确保周围无障碍物
   - 机械臂必须先回到 `TUCK_POSE` 再移动底盘
   - 保持急停按钮可触及

2. **导航冲突**：
   - 导航运行期间禁止直接发布 `/cmd_vel`
   - 应通过导航栈下发目标点

3. **电源管理**：
   - 底盘电机需要 24V 电源 (`data[1]=1`)
   - 长时间不使用时关闭电源

---

## 参考资源

- 完整文档：`/home/aidlux/SKILL.md`
- 人体跟随实现：`Haier_robot_ws/build/aid_robot_py/build/lib/aid_robot_py/tracker.py`
- ROS2 geometry_msgs: http://docs.ros.org/en/noetic/api/geometry_msgs/html/msg/Twist.html
