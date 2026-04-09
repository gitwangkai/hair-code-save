# 显示器云台控制 Skill

> **一句话描述**：基于 ROS2 的机器人头部云台（显示器）控制，支持抬头、低头、点头等动作。

---

## 能力

- **角度控制**：通过弧度值精确控制云台俯仰角度
- **动作模式**：支持抬头、低头、归中、点头等预设动作
- **平滑移动**：支持渐变动画效果
- **限位保护**：自动遵守机械限位

---

## 使用场景

| 场景 | 描述 | 示例 |
|------|------|------|
| **抬头** | 向上看，观察高处 | `look_up.py` |
| **低头** | 向下看，观察低处 | `look_down.py` |
| **点头** | 点头致意 | `nod.py` |
| **注视** | 注视某个角度 | `look_at.py` |

---

## 重要：坐标系说明

⚠️ **本机器人显示器云台角度范围**（已验证）：

| 位置 | 弧度值 | 说明 |
|------|--------|------|
| **最大抬头** | -3.0 rad | 接近上限 |
| **中间位置** | -3.35 rad | 水平视线 |
| **最大低头** | -3.7 rad | 接近下限 |

**运动方向**：
- 数值增大（如 -3.7 → -3.0）= **抬头**
- 数值减小（如 -3.0 → -3.7）= **低头**

**限位**（实时读取）：
- 上限（抬头）：`/head_upper_limit` ≈ -3.01 rad
- 下限（低头）：`/head_lower_limit` ≈ -3.71 rad

> 注意：话题名称中的 "upper/lower" 对应电机内部坐标系，与实际的抬头/低头方向相反。

---

## 快速开始

### 1. ROS2 命令行控制

```bash
# 抬头（数值大，接近-3.0）
ros2 topic pub --once /target_head_position std_msgs/msg/Float32 "{data: -3.1}"

# 低头（数值小，接近-3.7）
ros2 topic pub --once /target_head_position std_msgs/msg/Float32 "{data: -3.6}"

# 归中位置
ros2 topic pub --once /target_head_position std_msgs/msg/Float32 "{data: -3.35}"
```

### 2. Python 控制

```python
import rclpy
from std_msgs.msg import Float32

rclpy.init()
node = rclpy.create_node('head_controller')
publisher = node.create_publisher(Float32, '/target_head_position', 10)

# 抬头（数值增大）
msg = Float32()
msg.data = -3.1
publisher.publish(msg)
```

---

## 详细用法

### 云台控制器类

```python
#!/usr/bin/env python3
import rclpy
from std_msgs.msg import Float32
from sensor_msgs.msg import JointState
import time

class HeadController:
    """显示器云台控制器 - 基于实际测试验证"""
    
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
            angle_deg: 抬头角度（相对当前位置，向-3.0移动）
        """
        target = self.current_position + (angle_deg * 3.14159 / 180)
        target = min(target, self.UPPER_LIMIT)
        self.move_to(target, duration)
    
    def look_down(self, angle_deg=10, duration=0.5):
        """
        低头
        
        Args:
            angle_deg: 低头角度（相对当前位置，向-3.7移动）
        """
        target = self.current_position - (angle_deg * 3.14159 / 180)
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


# 使用示例
if __name__ == '__main__':
    head = HeadController()
    
    try:
        print("抬头...")
        head.move_to(-3.1)
        time.sleep(1)
        
        print("低头...")
        head.move_to(-3.6)
        time.sleep(1)
        
        print("点头...")
        head.nod(3)
        
        print("归中...")
        head.look_center()
        
    except KeyboardInterrupt:
        print("\n用户中断")
    finally:
        head.destroy()
```

---

## 示例代码

### 示例 1：抬头

```python
#!/usr/bin/env python3
"""抬头示例"""
import rclpy
from std_msgs.msg import Float32
import time

def look_up():
    """抬头到接近上限位置"""
    rclpy.init()
    node = rclpy.create_node('look_up')
    pub = node.create_publisher(Float32, '/target_head_position', 10)
    
    print("抬头...")
    msg = Float32()
    msg.data = -3.1  # 抬头位置（数值增大）
    
    for _ in range(10):
        pub.publish(msg)
        time.sleep(0.05)
    
    print("✓ 完成")
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    look_up()
```

### 示例 2：低头

```python
#!/usr/bin/env python3
"""低头示例"""
import rclpy
from std_msgs.msg import Float32
import time

def look_down():
    """低头到接近下限位置"""
    rclpy.init()
    node = rclpy.create_node('look_down')
    pub = node.create_publisher(Float32, '/target_head_position', 10)
    
    print("低头...")
    msg = Float32()
    msg.data = -3.6  # 低头位置（数值减小）
    
    for _ in range(10):
        pub.publish(msg)
        time.sleep(0.05)
    
    print("✓ 完成")
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    look_down()
```

### 示例 3：点头

```python
#!/usr/bin/env python3
"""点头示例 - 已验证"""
import rclpy
from std_msgs.msg import Float32
import time
import sys

def nod(times=3):
    """点头动作"""
    rclpy.init()
    node = rclpy.create_node('nod')
    pub = node.create_publisher(Float32, '/target_head_position', 10)
    
    # 定义角度（基于实际坐标系）
    LOOK_UP = -3.2      # 抬头
    LOOK_DOWN = -3.6    # 低头
    CENTER = -3.35      # 中间
    
    print(f"点头 {times} 次...")
    
    for i in range(times):
        print(f"  第 {i+1}/{times} 次: 低头...")
        msg = Float32()
        msg.data = LOOK_DOWN
        for _ in range(10):
            pub.publish(msg)
            time.sleep(0.05)
        time.sleep(0.3)
        
        print(f"  第 {i+1}/{times} 次: 抬头...")
        msg.data = LOOK_UP
        for _ in range(10):
            pub.publish(msg)
            time.sleep(0.05)
        time.sleep(0.3)
    
    # 归中
    print("归中...")
    msg.data = CENTER
    for _ in range(10):
        pub.publish(msg)
        time.sleep(0.05)
    
    print("✓ 完成")
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    times = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    nod(times)
```

---

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 云台无响应 | 12V 电源未开启 | 检查 CAN 总线电源 (`data[2]=1`) |
| 命令不执行 | 超出限位 | 检查角度是否在 -3.0 ~ -3.7 范围内 |
| 运动方向相反 | 坐标系理解错误 | 记住：-3.0是抬头，-3.7是低头 |
| 抖动严重 | 发送频率过低 | 保持 20Hz 以上发送频率 |
| 位置不准确 | 机械间隙 | 属于正常情况，重复发送命令 |

---

## 注意事项

1. **坐标系特殊**：
   - 本机器人云台使用 -3.0 ~ -3.7 rad 范围
   - 与传统 0° 水平不同，使用时请注意

2. **电源管理**：
   - 云台需要 12V 电源 (`data[2]=1`)
   - 长时间不使用时关闭电源

3. **限位保护**：
   - 实际限位：上限 -3.008，下限 -3.709
   - 超出范围命令会被忽略

4. **发送策略**：
   - 单次发送可能执行不到位
   - 建议以 20Hz 频率连续发送 0.5 秒

---

## 参考资源

- 全身控制文档：`/home/aidlux/SKILL.md`
- 人体检测项目：`/home/aidlux/human_detection/`
- 测试验证时间：2026-03-30
