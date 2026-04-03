# 显示器云台控制 Skill

> 基于 ROS2 的机器人头部云台（显示器）控制 - **已验证可用**

## ⚠️ 重要：坐标系说明

本机器人显示器云台使用特殊坐标系（已验证）：

| 位置 | 弧度值 | 说明 |
|------|--------|------|
| **最大抬头** | -3.0 rad | 上限位置 |
| **中间位置** | -3.35 rad | 水平视线 |
| **最大低头** | -3.7 rad | 下限位置 |

**运动方向**：
- 数值增大（如 -3.7 → -3.0）= **抬头**
- 数值减小（如 -3.0 → -3.7）= **低头**

## 快速开始

```bash
# 进入示例目录
cd /home/aidlux/skills/head_control/examples

# 抬头
python3 look_up.py

# 低头
python3 look_down.py

# 点头
python3 nod.py

# 归中
python3 look_center.py

# 完整演示
python3 head_controller.py
```

## ROS2 命令行控制

```bash
# 抬头到上限
ros2 topic pub --once /target_head_position std_msgs/msg/Float32 "{data: -3.0}"

# 低头到下限
ros2 topic pub --once /target_head_position std_msgs/msg/Float32 "{data: -3.7}"

# 归中位置
ros2 topic pub --once /target_head_position std_msgs/msg/Float32 "{data: -3.35}"
```

## 接口说明

| Topic | 类型 | 说明 |
|-------|------|------|
| `/target_head_position` | `std_msgs/Float32` | 目标角度（弧度） |
| `/head_upper_limit` | `std_msgs/Float32` | 上限角度 (-3.008) |
| `/head_lower_limit` | `std_msgs/Float32` | 下限角度 (-3.709) |

## 文件结构

```
head_control/
├── SKILL.md                    # 详细文档
├── README.md                   # 本文件
└── examples/
    ├── head_controller.py      # 控制器封装类
    ├── look_up.py              # 抬头
    ├── look_down.py            # 低头
    ├── look_center.py          # 归中
    └── nod.py                  # 点头
```

## 测试状态

| 动作 | 状态 | 备注 |
|------|------|------|
| 抬头 | ✅ 已验证 | 向 -3.0 rad 移动 |
| 低头 | ✅ 已验证 | 向 -3.7 rad 移动 |
| 点头 | ✅ 已验证 | 循环动作正常 |
| 归中 | ✅ 已验证 | -3.35 rad |

**测试时间**：2026-03-30

## 参考

- 详细文档：`/home/aidlux/skills/head_control/SKILL.md`
- 全身控制文档：`/home/aidlux/SKILL.md`
