# 海尔机器人全身整体控制 SKILL
> 平台：ROS2 Humble + PallasSDK（NX-7）
> 更新：2026.03

---

## 一、系统初始化

### 1.1 启动机器人底层

```bash
source ~/Haier_robot_ws/install/setup.bash
ros2 launch robot_bringup robot.launch.py
```

### 1.2 CAN 总线配置（每次重启后执行）

```bash
sudo ip link set can0 down
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up
```

### 1.3 NX-7 机械臂初始化（Python）

```python
import time
from PallasSDK import Controller, HiddenDataType, ComPort, LocationJ

ROBOT_IP    = "192.168.3.100"
SERIAL_NAME = "/dev/ttyUSB0"   # Windows 下改为 "COM2"

joint_pos = [0.0] * 7

def hidden_callback(data_type, robot, data):
    global joint_pos
    if data_type == HiddenDataType.RobotJointPos:
        received = [float(v) for v in data]
        for i in range(min(len(received), 7)):
            joint_pos[i] = received[i]

def init_arm():
    """连接控制器 → 开启关节回传 → 连接灵巧手串口 → 伺服上电。"""
    ctrl = Controller()
    ctrl.SetHiddenCallback(hidden_callback)
    ctrl.Connect(ROBOT_IP)
    time.sleep(30)                              # 等待初始化完成，期间禁止操作
    ctrl.SetHiddenOn(HiddenDataType.RobotJointPos)

    serial_ok = False
    try:
        ctrl.ComOpen(SERIAL_NAME, ComPort.Com_485, 115200, 8, 1, 0, True)
        serial_ok = True
    except Exception:
        print("警告：灵巧手串口未连接")

    ctrl.SetPowerEnable(True)                   # 伺服上电，运动前必须执行
    robot = ctrl.AddRobot(1)
    robot.SetFrameType(1)
    robot.SetSpeed(10)
    return ctrl, robot, serial_ok

def shutdown_arm(ctrl):
    """伺服下电 → 关闭串口。"""
    ctrl.SetPowerEnable(False)
    try:
        ctrl.ComClose(SERIAL_NAME)
    except Exception:
        pass
```

---

## 二、电源管理

> Topic: `/CAN/can1/transmit` | 消息类型: `can_msgs/msg/Frame` | CAN ID: **769**

```bash
# 开启所有电源（底盘 + 云台 + 传感器）
ros2 topic pub --once /CAN/can1/transmit can_msgs/msg/Frame \
  "{id: 769, dlc: 6, data: [1, 1, 1, 1, 0, 1, 0, 0]}"
```

| data 位 | 控制对象 | 0=关 / 1=开 |
|---------|---------|------------|
| data[0] | 24V_1（升降台驱动） | — |
| data[1] | 24V_2（底盘电机） | — |
| data[2] | 12V_1（云台 / HUB） | — |
| data[3] | 12V_2（高通 / 雷达 / 功放） | — |
| data[5] | 5V（超声波 / 悬崖传感器） | — |

```bash
# 关闭所有电源
ros2 topic pub --once /CAN/can1/transmit can_msgs/msg/Frame \
  "{id: 769, dlc: 6, data: [0, 0, 0, 0, 0, 0, 0, 0]}"
```

---

## 三、底盘控制

> Topic: `/cmd_vel` | 类型: `geometry_msgs/msg/Twist`

```bash
# 前进 0.5 m/s
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

# 原地左转
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}"

# 停止
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

> 里程计反馈 Topic: `/odom` | 类型: `nav_msgs/msg/Odometry`

---

## 四、云台控制

> Topic: `/target_head_position` | 类型: `std_msgs/msg/Float32`（单位：弧度）
> 限位 Topic: `/head_upper_limit` / `/head_lower_limit`

```bash
# 云台转至 0.5 rad
ros2 topic pub --once /target_head_position std_msgs/msg/Float32 "{data: 0.5}"

# 云台归中
ros2 topic pub --once /target_head_position std_msgs/msg/Float32 "{data: 0.0}"
```

> 状态反馈 Topic: `/joint_states` | 类型: `sensor_msgs/msg/JointState`（位置 / 速度 / 力矩）

---

## 五、机械臂控制（NX-7）

### 5.1 关节硬限位

**⚠️ 所有运动指令发出前必须通过限位校验，超出范围的指令一律拒绝。**

```python
JOINT_LIMITS = {
    "J1": {"min": -70.0,  "max": 200.0,  "max_speed": 120},  # 底座，水平旋转
    "J2": {"min":   0.0,  "max": 120.0,  "max_speed":  40},  # 大臂，上下摆动
    "J3": {"min": -55.0,  "max":  55.0,  "max_speed":  70},  # 小臂，前后摆动
    "J4": {"min":   0.0,  "max": 120.0,  "max_speed":  65},  # 前臂，旋转调节
    "J5": {"min": -85.0,  "max":  85.0,  "max_speed": 253},  # 腕部关节1
    "J6": {"min": -20.0,  "max":  20.0,  "max_speed": 342},  # 腕部关节2
    "J7": {"min": -10.0,  "max":  10.0,  "max_speed": 342},  # 末端关节
}

def check_joint_limits(angles: list) -> tuple:
    keys = ["J1", "J2", "J3", "J4", "J5", "J6", "J7"]
    for i, angle in enumerate(angles):
        lo = JOINT_LIMITS[keys[i]]["min"]
        hi = JOINT_LIMITS[keys[i]]["max"]
        if not (lo <= angle <= hi):
            return False, f"{keys[i]} 角度 {angle:.2f}° 超出限位 [{lo}, {hi}]"
    return True, ""

def safe_move(robot, angles: list) -> bool:
    ok, msg = check_joint_limits(angles)
    if not ok:
        print(f"[限位拦截] {msg}")
        return False
    robot.MoveJ(LocationJ(*angles[:6]))
    return True
```

### 5.2 预设安全位姿

```python
HOME_POSE     = [0.0,   0.0,  0.0,  0.0,  0.0,  0.0]   # 归零位
TUCK_POSE     = [0.0,  10.0,  0.0, 30.0,  0.0,  0.0]   # 收回安全位（移动前归位）
DESKTOP_READY = [0.0,  30.0,  0.0, 60.0,  0.0,  0.0]   # 桌面待机
DESKTOP_GRASP = [0.0,  90.0,  0.0, 90.0,  0.0,  0.0]   # 桌面抓取
HANDOVER_POSE = [0.0,  60.0,  0.0, 80.0,  0.0,  0.0]   # 递物位
```

### 5.3 灵巧手指令

```python
CMD_GRASP = "55AA011409014C044C044C04840332003200320032006400C2"
CMD_OPEN  = "55AA011409011400140014008403320032003200320064000E"

def hand_grasp(ctrl): ctrl.ComSend(SERIAL_NAME, CMD_GRASP)
def hand_open(ctrl):  ctrl.ComSend(SERIAL_NAME, CMD_OPEN)
```

---

## 六、灯光控制

> Topic: `/CAN/can1/transmit` | CAN ID: **768**

```bash
# 蓝灯呼吸（待机状态）
ros2 topic pub --once /CAN/can1/transmit can_msgs/msg/Frame \
  "{id: 768, dlc: 3, data: [2, 0, 0, 0, 0, 0, 0, 0]}"

# 绿灯常亮（任务完成）
ros2 topic pub --once /CAN/can1/transmit can_msgs/msg/Frame \
  "{id: 768, dlc: 3, data: [0, 0, 1, 0, 0, 0, 0, 0]}"

# 红灯常亮（报警）
ros2 topic pub --once /CAN/can1/transmit can_msgs/msg/Frame \
  "{id: 768, dlc: 3, data: [0, 1, 0, 0, 0, 0, 0, 0]}"

# 全灭
ros2 topic pub --once /CAN/can1/transmit can_msgs/msg/Frame \
  "{id: 768, dlc: 3, data: [0, 0, 0, 0, 0, 0, 0, 0]}"
```

| data 位 | 颜色 | 0=灭 / 1=常亮 / 2=呼吸 |
|---------|------|----------------------|
| data[0] | 蓝灯 | — |
| data[1] | 红灯 | — |
| data[2] | 绿灯 | — |

---

## 七、导航控制

### 7.1 模式切换

```bash
# 建图模式
ros2 service call /mode_set aid_robot_msgs/srv/StatusChange "{action: 'mapping'}"

# 导航模式
ros2 service call /mode_set aid_robot_msgs/srv/StatusChange "{action: 'navigation'}"
```

### 7.2 重定位

```bash
ros2 topic pub --once /start_init_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'map'},
  pose: {position: {x: 0.0, y: 0.0, z: 0.0},
         orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}"
```

### 7.3 保存地图

```bash
ros2 service call /finish_trajectory cartographer_ros_msgs/srv/FinishTrajectory "{trajectory_id: 0}"
ros2 service call /aid_save_map aid_robot_msgs/srv/MapOperation "{map_file_name: '/home/box/map/my_map'}"
```

---

## 八、自动充电（Docking）

```bash
# 设置充电桩位置（首次使用）
ros2 service call /cmd_dock aid_robot_msgs/srv/SetString "{data: 'set_dock_pose'}"

# 开始自动充电
ros2 service call /cmd_dock aid_robot_msgs/srv/SetString "{data: 'dock'}"

# 脱离充电桩
ros2 service call /cmd_dock aid_robot_msgs/srv/SetString "{data: 'undock'}"

# 取消充电
ros2 service call /cmd_dock aid_robot_msgs/srv/SetString "{data: 'cancel_dock'}"
```

> 充电状态 Topic: `/dock_state` — `undock` / `goto_dock_pose` / `charging`
> 充电结果 Topic: `/dock_result` — `dock_succeeded` / `dock_failed` / `detect_dock_failed`

---

## 九、机器人状态查询

```bash
# 当前位置
ros2 topic echo /base_link_pose

# 电池状态（电压 / 电量 / 电流 / 温度）
ros2 topic echo /battery_data

# 获取 IP 地址
ros2 service call /get_ip_addresses aid_robot_msgs/srv/GetString "{}"
```

---

## 十、注意事项

**机械臂：**
- 移动底盘前，必须先将机械臂移至 `TUCK_POSE`，避免与环境碰撞
- 伺服上电 `SetPowerEnable(True)` 是发送任何运动指令的前提
- 有效负载不超过 1kg；人机协作场景速度建议 ≤ 10%
- EMI 实时控制结束后必须调用 `EMIEnd()`

**底盘 / 系统：**
- CAN 总线每次系统重启后需重新配置波特率
- 导航运行期间禁止直接发布 `/cmd_vel`，应通过导航栈下发目标点
- 自动充电前必须先执行 `set_dock_pose` 记录充电桩位置
