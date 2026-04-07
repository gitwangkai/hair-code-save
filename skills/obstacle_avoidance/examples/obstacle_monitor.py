#!/usr/bin/env python3
"""
避障监控节点示例
直接运行此文件启动避障监控

使用方法：
1. 确保ROS2环境已加载
2. 运行：python3 obstacle_monitor.py
3. 在另一个终端发布速度命令进行测试
"""

import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from obstacle_monitor import ObstacleMonitor, main

if __name__ == '__main__':
    main()
