# 底盘控制 Skill

> 基于 ROS2 的机器人底盘运动控制

## 快速开始

```bash
# 进入示例目录
cd /home/aidlux/skills/chassis_control/examples

# 前进后退
python3 move_forward.py

# 原地旋转
python3 rotate.py left   # 左转
python3 rotate.py right  # 右转
python3 rotate.py 90     # 左转 90 度

# 紧急停止
python3 emergency_stop.py

# 键盘控制
python3 keyboard_control.py

# 完整演示
python3 chassis_controller.py
```

## 文件结构

```
chassis_control/
├── SKILL.md                    # 详细文档
├── README.md                   # 本文件
└── examples/
    ├── chassis_controller.py   # 控制器封装类
    ├── move_forward.py         # 前进后退
    ├── rotate.py               # 原地旋转
    ├── emergency_stop.py       # 紧急停止
    └── keyboard_control.py     # 键盘控制
```

## ROS2 命令行控制

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

## 注意事项

1. 底盘运动前确保周围无障碍物
2. 机械臂必须先回到 `TUCK_POSE` 再移动底盘
3. 导航运行期间禁止直接发布 `/cmd_vel`

## 参考

- 完整文档：`/home/aidlux/skills/chassis_control/SKILL.md`
- 全身控制文档：`/home/aidlux/SKILL.md`
