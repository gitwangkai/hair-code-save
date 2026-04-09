# NX-7 机械臂控制 Skill

> **一句话描述**：基于 PallasSDK 的 NX-7 七自由度仿生机械臂控制技能，提供安全、易用的关节运动控制接口。

---

## 能力

- **连接管理**：一键连接/断开控制器，自动上电/下电
- **关节运动**：MoveJ 关节空间运动，支持角度和速度控制
- **挥手动作**：J1=75°水平侧伸，J3=±20°摆动，自动回零位
- **预设位姿**：HOME、DESKTOP_READY、TUCK_POSE 等安全位姿
- **限位保护**：硬限位检查，防止机械损伤
- **错误恢复**：通信超时处理，异常安全恢复

---

## 使用场景

| 场景 | 描述 | 适用示例 |
|------|------|----------|
| **迎宾交互** | 检测到人员时主动挥手 | `wave_hand.py` |
| **物料搬运** | 抓取→移动→放置完整流程 | `pick_and_place.py` |
| **示教编程** | 记录-回放关节轨迹 | `record_playback.py` |
| **功能测试** | 关节运动范围验证 | `joint_range_test.py` |

---

## 快速开始

### 1. 基础连接

```python
import time
from PallasSDK import Controller, LocationJ

ROBOT_IP = "192.168.3.100"

# 连接控制器
ctrl = Controller()
ctrl.Connect(ROBOT_IP)
time.sleep(30)  # 等待初始化完成

# 开启伺服电源（必须！）
ctrl.SetPowerEnable(True)

# 获取机器人实例
robot = ctrl.AddRobot(1)
robot.SetSpeed(10)  # 设置速度 10%
```

### 2. 执行第一个动作

```python
# 定义目标位姿（角度，单位：度）
HOME_POSE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# 执行关节运动
robot.MoveJ(LocationJ(*HOME_POSE))
```

### 3. 安全断开

```python
# 返回安全位姿
robot.MoveJ(LocationJ(0, 10, 0, 30, 0, 0))

# 关闭伺服电源
time.sleep(1)
ctrl.SetPowerEnable(False)
```

---

## 详细用法

### 关节限位配置

**⚠️ 所有运动指令前必须通过限位校验**

```python
JOINT_LIMITS = {
    "J1": {"min": -70.0,  "max": 200.0, "max_speed": 120},
    "J2": {"min":   0.0,  "max": 120.0, "max_speed":  40},
    "J3": {"min": -55.0,  "max":  55.0, "max_speed":  70},
    "J4": {"min":   0.0,  "max": 120.0, "max_speed":  65},
    "J5": {"min": -85.0,  "max":  85.0, "max_speed": 253},
    "J6": {"min": -20.0,  "max":  20.0, "max_speed": 342},
    "J7": {"min": -10.0,  "max":  10.0, "max_speed": 342},
}

def check_joint_limits(angles: list) -> tuple:
    """检查关节角度是否在安全范围内"""
    keys = ["J1", "J2", "J3", "J4", "J5", "J6", "J7"]
    for i, angle in enumerate(angles):
        lo = JOINT_LIMITS[keys[i]]["min"]
        hi = JOINT_LIMITS[keys[i]]["max"]
        if not (lo <= angle <= hi):
            return False, f"{keys[i]} 角度 {angle:.2f}° 超出限位 [{lo}, {hi}]"
    return True, ""
```

### 预设安全位姿

```python
# 归零位 - 所有关节归零
HOME_POSE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# 收回位 - 移动底盘前使用，避免碰撞
TUCK_POSE = [0.0, 10.0, 0.0, 30.0, 0.0, 0.0]

# 桌面待机位 - 交互准备姿态
DESKTOP_READY = [0.0, 30.0, 0.0, 60.0, 0.0, 0.0]

# 桌面抓取位 - 低高度抓取姿态
DESKTOP_GRASP = [0.0, 90.0, 0.0, 90.0, 0.0, 0.0]

# 递物位 - 向人递送物品的姿态
HANDOVER_POSE = [0.0, 60.0, 0.0, 80.0, 0.0, 0.0]

# 挥手准备位 - J1水平侧伸，适合挥手
WAVE_PREPARE = [75.0, 0.0, 0.0, 80.0, -80.0, 0.0, 0.0]

# 挥手左摆
WAVE_LEFT = [75.0, 0.0, 20.0, 80.0, -80.0, 0.0, 0.0]

# 挥手右摆
WAVE_RIGHT = [75.0, 0.0, -20.0, 80.0, -80.0, 0.0, 0.0]
```

### 安全运动封装

```python
def safe_move(robot, angles: list) -> bool:
    """带限位检查的运动执行"""
    ok, msg = check_joint_limits(angles)
    if not ok:
        print(f"[限位拦截] {msg}")
        return False
    robot.MoveJ(LocationJ(*angles[:6]))
    return True
```

### 超时保护

```python
import signal

def set_timeout(seconds=10):
    """设置操作超时"""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"操作超时（>{seconds}秒）")
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)

def clear_timeout():
    """清除超时"""
    signal.alarm(0)
```

### 异常恢复

```python
import atexit

def emergency_shutdown(ctrl):
    """紧急关闭：返回安全位姿并下电"""
    try:
        robot = ctrl.AddRobot(1)
        robot.MoveJ(LocationJ(0, 10, 0, 30, 0, 0))
        time.sleep(2)
        ctrl.SetPowerEnable(False)
        print("[紧急关闭] 已返回安全位姿并下电")
    except Exception as e:
        print(f"[紧急关闭] 失败: {e}")

# 注册退出钩子
atexit.register(emergency_shutdown, ctrl)
```

---

## 示例代码

### 示例 1：挥手动作

```python
#!/usr/bin/env python3
"""
挥手动作示例（优化版）
流程：连接 → HOME → 准备位 → 挥手3次 → HOME → 断开

参数说明：
- J1 = 75° (水平侧伸，适合挥手)
- J3 = ±20° (摆动幅度，适中)
- 速度 = 45 (适度加快)
- 延迟 = 0.25s
"""
import time
import atexit
import signal
from PallasSDK import Controller, LocationJ

ROBOT_IP = "192.168.3.100"

# 挥手位姿（优化参数）
WAVE_PREPARE  = [75.0, 0.0, 0.0, 80.0, -80.0, 0.0, 0.0]
WAVE_SWING_L  = [75.0, 0.0, 20.0, 80.0, -80.0, 0.0, 0.0]
WAVE_SWING_R  = [75.0, 0.0, -20.0, 80.0, -80.0, 0.0, 0.0]

JOINT_LIMITS = {
    "J1": {"min": -70, "max": 200}, "J2": {"min": 0, "max": 120},
    "J3": {"min": -55, "max": 55}, "J4": {"min": 0, "max": 120},
    "J5": {"min": -85, "max": 85}, "J6": {"min": -20, "max": 20},
}

def check_limits(angles):
    keys = ["J1", "J2", "J3", "J4", "J5", "J6"]
    for i, a in enumerate(angles):
        lo, hi = JOINT_LIMITS[keys[i]]["min"], JOINT_LIMITS[keys[i]]["max"]
        if not (lo <= a <= hi):
            return False, f"{keys[i]} 超限"
    return True, ""

def safe_move(robot, angles):
    ok, msg = check_limits(angles)
    if not ok:
        print(f"[拦截] {msg}")
        return False
    robot.MoveJ(LocationJ(*angles))
    time.sleep(1)
    return True

def main():
    ctrl = Controller()
    ctrl.Connect(ROBOT_IP)
    time.sleep(30)  # 初始化等待
    
    ctrl.SetPowerEnable(True)
    robot = ctrl.AddRobot(1)
    robot.SetSpeed(45)  # 适度加快（原10，现45）
    
    # 注册紧急关闭
    def shutdown():
        try:
            robot.MoveJ(LocationJ(0, 10, 0, 30, 0, 0))
            time.sleep(2)
            ctrl.SetPowerEnable(False)
        except:
            pass
    atexit.register(shutdown)
    
    try:
        # 1. 回到 HOME
        safe_move(robot, [0, 0, 0, 0, 0, 0])
        
        # 2. 到挥手准备位
        safe_move(robot, WAVE_PREPARE)
        
        # 3. 挥手3次
        for i in range(3):
            safe_move(robot, WAVE_SWING_L)
            safe_move(robot, WAVE_SWING_R)
        
        # 4. 回到准备位
        safe_move(robot, WAVE_PREPARE)
        
        # 5. 返回 HOME
        safe_move(robot, [0, 0, 0, 0, 0, 0])
        
    finally:
        shutdown()

if __name__ == "__main__":
    main()
```

### 示例 2：完整动作流程

```python
#!/usr/bin/env python3
"""
完整动作流程：抓取 → 移动 → 放置
"""
import time
from PallasSDK import Controller, LocationJ

class ArmController:
    """机械臂控制封装类"""
    
    # 预设位姿
    POSES = {
        "home": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "tuck": [0.0, 10.0, 0.0, 30.0, 0.0, 0.0],
        "ready": [0.0, 30.0, 0.0, 60.0, 0.0, 0.0],
        "grasp": [0.0, 90.0, 0.0, 90.0, 0.0, 0.0],
        "handover": [0.0, 60.0, 0.0, 80.0, 0.0, 0.0],
    }
    
    JOINT_LIMITS = {
        "J1": (-70, 200), "J2": (0, 120), "J3": (-55, 55),
        "J4": (0, 120), "J5": (-85, 85), "J6": (-20, 20),
    }
    
    def __init__(self, ip="192.168.3.100"):
        self.ctrl = Controller()
        self.robot = None
        self.ip = ip
    
    def connect(self):
        """连接机械臂"""
        self.ctrl.Connect(self.ip)
        time.sleep(30)
        self.ctrl.SetPowerEnable(True)
        self.robot = self.ctrl.AddRobot(1)
        self.robot.SetSpeed(10)
        print("[连接] 机械臂已就绪")
    
    def disconnect(self):
        """断开连接"""
        self.move_to("tuck")
        time.sleep(2)
        self.ctrl.SetPowerEnable(False)
        print("[断开] 机械臂已安全关闭")
    
    def check_limits(self, angles):
        """检查关节限位"""
        for i, (name, (lo, hi)) in enumerate(self.JOINT_LIMITS.items()):
            if not (lo <= angles[i] <= hi):
                return False, f"{name} 超限: {angles[i]}"
        return True, "OK"
    
    def move_to(self, pose_name, wait=1):
        """移动到预设位姿"""
        if pose_name not in self.POSES:
            raise ValueError(f"未知位姿: {pose_name}")
        
        angles = self.POSES[pose_name]
        ok, msg = self.check_limits(angles)
        if not ok:
            print(f"[错误] {msg}")
            return False
        
        self.robot.MoveJ(LocationJ(*angles))
        time.sleep(wait)
        return True
    
    def move_joints(self, angles, wait=1):
        """移动到指定关节角度"""
        ok, msg = self.check_limits(angles)
        if not ok:
            print(f"[错误] {msg}")
            return False
        
        self.robot.MoveJ(LocationJ(*angles))
        time.sleep(wait)
        return True

# 使用示例
def demo_pick_place():
    arm = ArmController()
    
    try:
        arm.connect()
        
        # 1. 准备姿态
        arm.move_to("ready")
        
        # 2. 移动到抓取位
        arm.move_to("grasp")
        
        # 3. 抓取（这里可以添加夹爪控制）
        print("[动作] 执行抓取...")
        time.sleep(1)
        
        # 4. 提起
        arm.move_to("handover")
        
        # 5. 放置
        arm.move_to("grasp")
        print("[动作] 执行放置...")
        
        # 6. 返回
        arm.move_to("ready")
        arm.move_to("home")
        
    finally:
        arm.disconnect()

if __name__ == "__main__":
    demo_pick_place()
```

---

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| **连接失败** | IP 地址错误<br>控制器未启动<br>网络不通 | 检查 ROBOT_IP (默认 192.168.3.100)<br>确认控制器电源已开启<br>ping 测试网络连通性 |
| **初始化超时** | 30 秒等待不足<br>控制器 busy | 增加等待时间至 45-60 秒<br>重启控制器后重试 |
| **运动无响应** | 伺服未上电<br>速度设置为 0 | 确保 SetPowerEnable(True) 已调用<br>检查 SetSpeed() 参数 > 0 |
| **段错误** | PallasSDK 与 Flask 冲突<br>多线程问题 | 将 SDK 调用放入独立子进程<br>避免多线程同时访问 Controller |
| **关节超限** | 目标角度超出限位 | 使用 check_joint_limits() 预检查<br>参考 JOINT_LIMITS 调整目标值 |
| **通信超时** | 网络不稳定<br>控制器响应慢 | 设置 signal.alarm() 超时保护<br>增加运动等待时间 |

---

## 最佳实践

### 安全第一

1. **移动底盘前必须收臂**
   ```python
   # 移动前
   robot.MoveJ(LocationJ(0, 10, 0, 30, 0, 0))  # TUCK_POSE
   time.sleep(2)
   # 现在可以安全移动底盘
   ```

2. **伺服上电是运动前提**
   ```python
   ctrl.SetPowerEnable(True)  # 必须！
   ```

3. **人机协作速度限制**
   ```python
   robot.SetSpeed(10)  # 人机协作建议 ≤ 10%
   ```

4. **负载限制**
   - 最大有效负载：**1kg**
   - 重心偏移：尽量靠近末端中心

### 异常处理

```python
import atexit
import signal

def safe_run(robot_action):
    """安全执行装饰器"""
    def wrapper(*args, **kwargs):
        ctrl = Controller()
        try:
            ctrl.Connect(ROBOT_IP)
            time.sleep(30)
            ctrl.SetPowerEnable(True)
            robot = ctrl.AddRobot(1)
            robot.SetSpeed(10)
            
            # 注册紧急关闭
            def emergency():
                try:
                    robot.MoveJ(LocationJ(0, 10, 0, 30, 0, 0))
                    time.sleep(2)
                    ctrl.SetPowerEnable(False)
                except:
                    pass
            atexit.register(emergency)
            
            # 执行动作
            result = robot_action(robot, *args, **kwargs)
            
            # 清理
            emergency()
            return result
            
        except Exception as e:
            print(f"[错误] {e}")
            try:
                ctrl.SetPowerEnable(False)
            except:
                pass
            raise
    return wrapper
```

### EMI 实时控制注意事项

```python
# 启用实时控制后必须调用 EMIEnd()
robot.EMIMoveJ(...)
# ... 实时控制逻辑 ...
robot.EMIEnd()  # 必须调用，否则后续运动异常
```

---

## 版本信息

- **Skill 版本**: v2.0.0
- **更新日期**: 2026-03-30
- **适用平台**: AidLux (ARM64)
- **SDK 版本**: PallasSDK
- **机械臂型号**: NX-7 七自由度仿生臂

---

## 参考资源

- PallasSDK 官方文档
- NX-7 机械臂用户手册
- `skills/arm_control/examples/` - 完整示例代码
- `human_detection/wave_hand_standalone.py` - 集成项目中的挥手实现
