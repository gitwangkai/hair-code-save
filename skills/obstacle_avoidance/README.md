# 避障控制 Skill

> 基于激光雷达的机器人避障控制系统

## 功能特性

- **实时障碍物检测**：通过激光雷达实时监测前方、左方、右方障碍物
- **自动距离判断**：根据障碍物距离自动计算安全速度
- **智能减速/停止**：接近障碍物时自动减速，危险距离时自动停止
- **底盘控制集成**：无缝集成到底盘控制，移动时自动避障

## 快速开始

```bash
# 进入示例目录
cd /home/aidlux/skills/obstacle_avoidance/examples

# 启动避障监控
python3 obstacle_monitor.py

# 安全底盘控制（带避障）
python3 safe_chassis_controller.py

# 避障测试
python3 test_obstacle_detection.py
```

## 文件结构

```
obstacle_avoidance/
├── README.md                    # 本文件
├── SKILL.md                     # 详细文档
├── src/
│   └── obstacle_monitor.py      # 避障监控核心类
└── examples/
    ├── obstacle_monitor.py      # 避障监控节点
    ├── safe_chassis_controller.py  # 安全底盘控制器
    └── test_obstacle_detection.py  # 避障测试
```

## ROS2 话题

| 话题 | 类型 | 说明 |
|------|------|------|
| `/scan` | LaserScan | 激光雷达输入 |
| `/cmd_vel` | Twist | 速度命令输入 |
| `/cmd_vel_safe` | Twist | 安全速度命令输出 |
| `/obstacle_status` | Bool | 障碍物状态 |
| `/obstacle_distance` | Float32 | 最近障碍物距离 |

## 参数配置

```python
safety_distance: 0.5      # 安全距离（米），小于此距离停止
slow_distance: 1.0        # 减速距离（米），小于此距离减速
max_linear_speed: 0.5     # 最大线速度（m/s）
max_angular_speed: 1.0    # 最大角速度（rad/s）
```

## 避障逻辑

```
障碍物距离 > 减速距离：正常速度
减速距离 > 障碍物距离 > 安全距离：线性减速
障碍物距离 < 安全距离：停止
```

## 注意事项

1. 确保激光雷达已启动并发布 `/scan` 话题
2. 避障节点需要在底盘控制前启动
3. 可通过动态参数调整安全距离

## 参考

- 完整文档：`/home/aidlux/skills/obstacle_avoidance/SKILL.md`
- 底盘控制：`/home/aidlux/skills/chassis_control/`
- 全身控制：`/home/aidlux/SKILL.md`
