#!/bin/bash
# 运行复合动作 Skill：前进挥手旋转返回
# Skill: action_runner/complex_wave_return

echo "=============================================="
echo "    复合动作 Skill：前进挥手旋转返回"
echo "=============================================="
echo ""

# 检查ROS2环境
if [ -z "$ROS_DISTRO" ]; then
    echo "加载ROS2环境..."
    source /opt/ros/humble/setup.bash 2>/dev/null || {
        echo "错误: 无法加载ROS2"
        exit 1
    }
fi

# 加载工作空间
WS_DIR="/home/aidlux/Haier_robot_ws"
if [ -f "$WS_DIR/install/setup.bash" ]; then
    source "$WS_DIR/install/setup.bash"
fi

echo "ROS2: $ROS_DISTRO"
echo ""

# 动作说明
echo "【动作序列】"
echo "  1. 前进1米 + 挥手"
echo "  2. 向右旋转360度（挥手同步）"
echo "  3. 左转 + 前进1米 + 点头"
echo "  4. 原路返回"
echo ""
echo "【依赖 Skills】"
echo "  - obstacle_avoidance: 避障监控"
echo "  - chassis_control: 底盘移动"
echo "  - arm_control: 挥手点头"
echo ""
echo "=============================================="
echo ""

# 执行 Skill
python3 /home/aidlux/skills/action_runner/actions/complex_wave_return.py
