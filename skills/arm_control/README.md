# NX-7 机械臂控制 Skill

> 基于 PallasSDK 的 NX-7 七自由度仿生机械臂控制技能

## 快速开始

```bash
# 1. 进入示例目录
cd /home/aidlux/skills/arm_control/examples

# 2. 运行挥手示例
python3 wave_hand.py

# 3. 运行抓取示例
python3 pick_and_place.py
```

## 文件结构

```
arm_control/
├── examples/               # 示例脚本
│   ├── wave_hand.py       # 挥手动作
│   ├── pick_and_place.py  # 抓取放置
│   ├── emergency_stop.py  # 紧急停止
│   └── action_loader.py   # 配置驱动动作
├── templates/             # 配置模板
│   └── robot_actions.yaml # 动作配置
└── README.md              # 本文件
```

## 示例说明

### 1. 挥手示例 (wave_hand.py)

```bash
python3 wave_hand.py
```

功能：机械臂挥手打招呼
流程：连接 → HOME → 准备位 → 挥手3次 → HOME → 断开

### 2. 抓取放置示例 (pick_and_place.py)

```bash
# 抓取放置流程
python3 pick_and_place.py

# 路径点运动
python3 pick_and_place.py waypoint
```

### 3. 紧急停止示例 (emergency_stop.py)

```bash
python3 emergency_stop.py

# 选择场景:
# 1. 正常操作流程
# 2. 用户中断 (Ctrl+C)
# 3. 关节超限错误
# 4. 超时保护
# 5. 优雅降级
# 6. 运行所有场景
```

### 4. 配置驱动动作 (action_loader.py)

```bash
# 查看可用序列
python3 action_loader.py --list

# 执行挥手
python3 action_loader.py wave_hand

# 执行抓取放置
python3 action_loader.py pick_and_place
```

## 配置说明

动作配置文件：`templates/robot_actions.yaml`

### 添加新位姿

```yaml
poses:
  my_pose:
    name: "我的位姿"
    description: "描述信息"
    angles: [0, 30, 0, 60, 0, 0]
    tags: ["custom"]
```

### 添加新序列

```yaml
sequences:
  my_sequence:
    name: "我的序列"
    description: "描述信息"
    repeat: 1
    poses:
      - pose: home
        wait: 1.0
      - pose: my_pose
        wait: 1.0
```

## 安全提示

1. **移动底盘前必须收臂**：使用 `tuck` 位姿
2. **伺服上电是运动前提**：确保 `SetPowerEnable(True)` 已调用
3. **人机协作速度限制**：建议 ≤ 10%
4. **最大负载**：1kg

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 连接失败 | 检查 IP (192.168.3.100) 和网络 |
| 初始化超时 | 增加等待时间至 45-60 秒 |
| 段错误 | 避免与 Flask 同时使用，使用独立进程 |
| 关节超限 | 使用限位检查函数预验证 |

## 参考

- 完整文档：`/home/aidlux/skills/arm_control/SKILL.md`
