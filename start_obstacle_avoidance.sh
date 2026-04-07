#!/bin/bash
# 启动手动避障控制节点

echo "=============================================="
echo "    手动避障控制系统启动脚本"
echo "=============================================="
echo ""

# 检查ROS2环境
if [ -z "$ROS_DISTRO" ]; then
    echo "正在加载ROS2环境..."
    source /opt/ros/humble/setup.bash 2>/dev/null || {
        echo "错误: 无法加载ROS2环境"
        echo "请确保已安装ROS2 Humble"
        exit 1
    }
fi

echo "ROS2版本: $ROS_DISTRO"
echo ""

# 检查工作空间
WS_DIR="/home/aidlux/Haier_robot_ws"
if [ -f "$WS_DIR/install/setup.bash" ]; then
    echo "加载工作空间: $WS_DIR"
    source "$WS_DIR/install/setup.bash"
fi

echo ""
echo "启动手动避障控制节点..."
echo ""
echo "使用说明:"
echo "  w/s - 前进/后退"
echo "  a/d - 左转/右转"
echo "  q/e - 增加/减少最大速度"
echo "  space - 紧急停止"
echo "  x - 退出程序"
echo ""
echo "=============================================="
echo ""

# 运行Python节点
python3 /home/aidlux/manual_obstacle_avoidance.py

echo ""
echo "程序已退出"
