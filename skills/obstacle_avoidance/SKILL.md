# 避障控制 Skill - 详细文档

## 概述

本 Skill 提供基于激光雷达的机器人避障控制能力，可实时监测周围环境障碍物，并在机器人移动时自动调整速度，防止碰撞。

## 核心组件

### 1. ObstacleMonitor 类

避障监控核心类，负责：
- 订阅激光雷达数据
- 计算各方向障碍物距离
- 评估碰撞风险
- 生成安全速度命令

### 2. 安全策略

#### 2.1 三层安全防护

| 层级 | 距离范围 | 动作 |
|------|----------|------|
| 正常行驶 | > 减速距离 | 正常速度 |
| 减速区域 | 减速距离 ~ 安全距离 | 线性减速 |
| 危险区域 | < 安全距离 | 紧急停止 |

#### 2.2 方向感知

- **前方障碍物**：禁止前进
- **左方障碍物**：禁止左转
- **右方障碍物**：禁止右转

## API 接口

### ObstacleMonitor 类

```python
from obstacle_monitor import ObstacleMonitor

# 创建实例
monitor = ObstacleMonitor(
    safety_distance=0.5,      # 安全距离
    slow_distance=1.0,        # 减速距离
    max_linear_speed=0.5,     # 最大线速度
    max_angular_speed=1.0     # 最大角速度
)

# 获取安全速度
safe_cmd = monitor.get_safe_velocity(desired_cmd)

# 检查是否可以移动
can_move = monitor.can_move_forward()
can_turn_left = monitor.can_turn_left()
can_turn_right = monitor.can_turn_right()

# 获取障碍物信息
obstacle_info = monitor.get_obstacle_info()
```

### 回调函数

```python
# 障碍物状态变化回调
def on_obstacle_detected(direction, distance):
    print(f"检测到障碍物：{direction}，距离：{distance}m")

def on_obstacle_cleared():
    print("障碍物已清除")

monitor.set_callbacks(
    on_obstacle_detected=on_obstacle_detected,
    on_obstacle_cleared=on_obstacle_cleared
)
```

## 使用示例

### 示例1：基础避障监控

```python
import rclpy
from obstacle_monitor import ObstacleMonitor

rclpy.init()
monitor = ObstacleMonitor()

# 主循环
while rclpy.ok():
    info = monitor.get_obstacle_info()
    print(f"前方：{info['front']:.2f}m")
    print(f"左方：{info['left']:.2f}m")
    print(f"右方：{info['right']:.2f}m")
    time.sleep(0.5)
```

### 示例2：集成到底盘控制

```python
from chassis_controller import ChassisController
from obstacle_monitor import ObstacleMonitor

class SafeChassisController:
    def __init__(self):
        self.chassis = ChassisController()
        self.obstacle_monitor = ObstacleMonitor()
        
    def move_forward(self, speed=0.3):
        # 检查前方是否安全
        if self.obstacle_monitor.can_move_forward():
            self.chassis.move_forward(speed)
        else:
            self.chassis.stop()
            print("前方有障碍物，无法前进")
            
    def turn_left(self, speed=0.5):
        # 检查左方是否安全
        if self.obstacle_monitor.can_turn_left():
            self.chassis.turn_left(speed)
        else:
            self.chassis.stop()
            print("左方有障碍物，无法左转")
```

### 示例3：动态调整安全距离

```python
# 在狭窄环境中减小安全距离
monitor.set_safety_distance(0.3)

# 在开阔环境中增大安全距离
monitor.set_safety_distance(0.8)

# 获取当前安全距离
current_distance = monitor.get_safety_distance()
```

## 参数说明

### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| safety_distance | float | 0.5 | 安全距离（米） |
| slow_distance | float | 1.0 | 减速距离（米） |
| max_linear_speed | float | 0.5 | 最大线速度（m/s） |
| max_angular_speed | float | 1.0 | 最大角速度（rad/s） |
| front_angle_range | float | 30.0 | 前方检测角度范围（度） |
| side_angle_range | float | 30.0 | 侧方检测角度范围（度） |

### 动态参数

```python
# 运行时修改参数
monitor.safety_distance = 0.6
monitor.slow_distance = 1.2
monitor.max_linear_speed = 0.4
```

## 激光雷达数据处理

### 扫描角度定义

```
          前方 (0°)
             |
    左方     |     右方
  (-90°) ----+---- (+90°)
             |
          后方 (180°)
```

### 区域划分

- **前方区域**：-30° ~ +30°
- **左方区域**：+60° ~ +120°
- **右方区域**：-120° ~ -60°

## 状态监控

### 发布的话题

| 话题名 | 类型 | 频率 | 说明 |
|--------|------|------|------|
| /obstacle_status | Bool | 10Hz | True=有障碍物 |
| /obstacle_distance | Float32 | 10Hz | 最近障碍物距离 |
| /obstacle_direction | String | 10Hz | 障碍物方向 |

### 订阅的话题

| 话题名 | 类型 | 说明 |
|--------|------|------|
| /scan | LaserScan | 激光雷达数据 |
| /cmd_vel | Twist | 期望速度命令 |

## 故障排除

### 问题1：无法检测到障碍物

**检查清单：**
1. 激光雷达是否启动：`ros2 topic list | grep scan`
2. 激光雷达数据是否正常：`ros2 topic echo /scan`
3. 避障节点是否订阅了正确的话题

### 问题2：避障过于敏感

**解决方案：**
```python
# 增大安全距离
monitor.safety_distance = 0.8

# 或者增大减速距离
monitor.slow_distance = 1.5
```

### 问题3：避障反应延迟

**可能原因：**
1. 激光雷达发布频率过低
2. 节点处理延迟

**优化方案：**
```python
# 提高激光雷达频率（在激光雷达驱动中设置）
# 或使用更快的回调处理方式
```

## 性能优化

### 1. 降低CPU占用

```python
# 降低发布频率
monitor.publish_rate = 5  # Hz
```

### 2. 减少内存占用

```python
# 限制激光雷达数据缓存
monitor.scan_buffer_size = 10
```

## 扩展功能

### 添加深度相机支持

```python
class AdvancedObstacleMonitor(ObstacleMonitor):
    def __init__(self):
        super().__init__()
        # 订阅点云数据
        self.pointcloud_sub = self.create_subscription(
            PointCloud2,
            '/camera/points',
            self.pointcloud_callback,
            10
        )
        
    def pointcloud_callback(self, msg):
        # 处理3D点云数据
        pass
```

### 多传感器融合

```python
# 融合激光雷达和超声波数据
class FusionObstacleMonitor:
    def __init__(self):
        self.lidar_monitor = LidarMonitor()
        self.ultrasonic_monitor = UltrasonicMonitor()
        
    def get_safe_velocity(self, cmd):
        # 取两个传感器的最小距离
        lidar_safe = self.lidar_monitor.get_safe_velocity(cmd)
        ultrasonic_safe = self.ultrasonic_monitor.get_safe_velocity(cmd)
        
        # 返回更保守的命令
        return min(lidar_safe, ultrasonic_safe)
```

## 参考文档

- [ROS2 导航文档](https://navigation.ros.org/)
- [激光雷达消息格式](http://docs.ros.org/en/api/sensor_msgs/html/msg/LaserScan.html)
- [底盘控制 Skill](../chassis_control/SKILL.md)
