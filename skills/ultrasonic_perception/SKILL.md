# 超声波感知技能 (Ultrasonic Perception Skill)

## 功能概述

本Skill提供机器人单路前向超声波传感器的感知能力，支持：
- 实时前方距离检测
- 障碍物检测与预警
- 安全导航辅助

## 硬件配置

机器人配备**1个前向超声波传感器**：

| 传感器位置 | ROS话题 | 用途 | 连接方式 |
|-----------|---------|------|---------|
| 前超声波 | `/ultrasonic_front` | 前方障碍物检测 | CAN总线 |
| 前超声波 | `/ultrasonic/range` | 前方障碍物检测 | UART串口 |

**技术参数**（UETCH101传感器）：
- 测距范围：0.02m ~ 1.2m (默认数据类型)
- 视场角：0.785 rad (~45°)
- 发布频率：10Hz
- 消息类型：`sensor_msgs/msg/Range`

## 使用方法

### 1. 查看传感器数据

```bash
# 查看前超声波数据 (CAN总线话题)
ros2 topic echo /ultrasonic_front

# 或查看UART驱动话题
ros2 topic echo /ultrasonic/range
```

### 2. 使用Python接口

```python
from ultrasonic_perception import UltrasonicPerception

# 初始化感知模块 (使用CAN总线话题)
perception = UltrasonicPerception(topic="/ultrasonic_front")

# 获取前方距离
distance = perception.get_distance()
print(f"前方距离: {distance}m")

# 检查前方是否有障碍物
if perception.is_obstacle_ahead(threshold=0.5):
    print("前方0.5米内有障碍物！")

# 获取安全状态
status = perception.get_safe_status()
# 返回: 'safe'/'caution'/'danger'/'unknown'
```

## API参考

### `UltrasonicPerception` 类

#### 初始化参数
- `topic`: 超声波话题 (默认: `/ultrasonic_front`)
- `timeout`: 数据超时时间，秒 (默认: `1.0`)

#### 方法

| 方法 | 返回类型 | 说明 |
|------|---------|------|
| `get_distance()` | `float` | 获取前方距离(m)，无效返回`None` |
| `is_obstacle_ahead(threshold=0.5)` | `bool` | 前方threshold距离内是否有障碍物 |
| `get_safe_status()` | `str` | 返回安全状态: `safe`/`caution`/`danger`/`unknown` |
| `wait_for_obstacle_cleared(timeout=30)` | `bool` | 等待障碍物清除 |

## 避障策略建议

```
前方障碍物检测:
├── 距离 < 0.3m: 危险状态，紧急停止
├── 距离 < 0.6m: 警告状态，减速慢行
└── 距离 >= 0.6m: 安全状态，正常通行
```

## 与底盘控制集成

```python
from ultrasonic_perception import UltrasonicPerception
from chassis_control import ChassisControl

perception = UltrasonicPerception()
chassis = ChassisControl()

# 安全前进
distance = perception.get_distance()
if distance and distance > 0.5:
    chassis.move(0.2, 0)  # 前进
else:
    chassis.stop()  # 停止
```

## 故障排查

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| 数据为inf | 超出测距范围 | 检查传感器指向，确保在1.2m范围内有物体 |
| 数据为0 | 传感器故障/未连接 | 检查硬件连接，查看`dmesg` |
| 无话题发布 | 驱动未启动 | 检查CAN总线或UART连接 |
| 数据跳变大 | 多径反射 | 调整传感器角度，避免光滑表面 |

## 相关话题

- `/ultrasonic_front` - 前超声波 (CAN总线) (sensor_msgs/Range)
- `/ultrasonic/range` - 前超声波 (UART) (sensor_msgs/Range)

## 依赖

- ROS2 Humble
- sensor_msgs
