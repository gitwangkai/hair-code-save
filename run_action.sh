#!/bin/bash
# 执行复合动作：前进1米挥手 → 右转360° → 左转前进1米点头 → 返回

echo "=============================================="
echo "    执行复合动作"
echo "=============================================="
echo ""
echo "动作序列："
echo "  1. 前进1米 + 挥手"
echo "  2. 向右旋转360度（挥手同步）"
echo "  3. 左转 + 前进1米 + 点头"
echo "  4. 原路返回"
echo ""
echo "=============================================="
echo ""

# 加载ROS2环境
source /opt/ros/humble/setup.bash 2>/dev/null
source /home/aidlux/Haier_robot_ws/install/setup.bash 2>/dev/null

# 执行
python3 /home/aidlux/simple_action_demo.py
