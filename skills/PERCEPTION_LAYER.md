# 感知层技能总览

> 机器人感知层负责从环境中采集数据，为决策层提供实时、准确的环境信息

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                      感知层 (Perception)                     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ 超声波感知   │  │ 视觉感知     │  │ 语音感知       │  │
│  │ (已完成)     │  │ (规划中)     │  │ (规划中)       │  │
│  │              │  │              │  │                │  │
│  │ • 前向测距   │  │ • 目标检测   │  │ • 语音识别     │  │
│  │ • 避障检测   │  │ • 人脸识别   │  │ • 声源定位     │  │
│  │ • 安全导航   │  │ • 深度估计   │  │ • 语音合成     │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ 激光雷达     │  │ IMU/GPS      │  │ 深度相机       │  │
│  │ (已有驱动)   │  │ (已有驱动)   │  │ (已有驱动)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │   数据融合层    │
                    │  (待开发)       │
                    └─────────────────┘
```

## 已完成

### 超声波感知 (`ultrasonic_perception`)

**功能**: 通过前向超声波传感器实时检测前方障碍物距离

**硬件配置**:
| 位置 | 话题 | 范围 | 频率 | 连接 |
|------|------|------|------|------|
| 前超声波 | `/ultrasonic_front` | 0.02-1.2m | 10Hz | CAN总线 |
| 前超声波 | `/ultrasonic/range` | 0.02-1.2m | 10Hz | UART |

**核心能力**:
```python
from ultrasonic_perception import UltrasonicPerception

perception = UltrasonicPerception(topic="/ultrasonic_front")

# 获取距离
dist = perception.get_distance()  # 前方距离(m)

# 障碍物检测
if perception.is_obstacle_ahead(threshold=0.5):
    print("前方0.5m内有障碍物！")

# 安全状态
status = perception.get_safe_status()  # 'safe'/'caution'/'danger'
```

**与执行层集成**:
```python
from ultrasonic_perception import UltrasonicPerception
from chassis_control import ChassisControl

perception = UltrasonicPerception()
chassis = ChassisControl()

# 安全前进
dist = perception.get_distance()
if dist and dist > 0.5:
    chassis.move(0.2, 0)  # 前进
else:
    chassis.stop()  # 停止
```

## 进行中 / 规划中

### Phase 1: 基础感知能力

| 模块 | 状态 | 预计时间 | 说明 |
|------|------|---------|------|
| 超声波感知 | ✅ 完成 | - | 前向避障与距离检测 |
| 摄像头接入 | 🔄 调研 | 1-2天 | 确认摄像头型号与驱动 |
| 基础视觉检测 | ⏳ 待开始 | 3-5天 | YOLO目标检测 |

### Phase 2: 融合感知

| 模块 | 状态 | 说明 |
|------|------|------|
| 多传感器融合 | ⏳ 待开始 | 超声波+视觉融合避障 |
| 人体检测与跟踪 | ⏳ 待开始 | 检测并跟踪人体位置 |
| 语音识别 | ⏳ 待开始 | 语音指令识别 |

## 使用示例

### 完整避障导航

```python
from ultrasonic_perception import UltrasonicPerception
from chassis_control import ChassisControl
import time

class SafeNavigator:
    def __init__(self):
        self.perception = UltrasonicPerception()
        self.chassis = ChassisControl()
    
    def safe_forward(self, distance, speed=0.2):
        """带避障的前进"""
        moved = 0
        while moved < distance:
            # 实时检查障碍物
            dist = self.perception.get_distance()
            if dist and dist < 0.5:
                self.chassis.stop()
                print(f"检测到障碍物，距离: {dist:.2f}m，停止！")
                return False
            
            # 移动一小段
            self.chassis.move(speed, 0)
            time.sleep(0.1)
            moved += speed * 0.1
        
        self.chassis.stop()
        return True

# 使用
navigator = SafeNavigator()
navigator.safe_forward(2.0)  # 安全前进2米
```

## 数据流

```
超声波驱动节点 (CAN/UART)
     ↓ (sensor_msgs/Range)
超声波感知Skill
     ↓ (处理后数据)
决策层 / 执行层
     ↓ (控制指令)
底盘/机械臂执行
```

## 下一步计划

1. **视觉感知**: 接入摄像头，实现YOLO目标检测
2. **语音交互**: 集成语音识别与语音合成
3. **感知融合**: 超声波+视觉联合避障
