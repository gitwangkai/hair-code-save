#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作独立脚本

功能: 一键执行完整挥手动作（包含连接、执行、断开）
用法: python3 wave_hand_standalone.py

完整流程:
1. 连接机械臂
2. 执行挥手动作（原点→准备→挥手→原点）
3. 断开连接
"""

import sys
import os

# 添加路径以导入 wave_hand_safe
sys.path.insert(0, os.path.dirname(__file__))

from wave_hand_safe import WaveHandController


def main():
    """主函数 - 独立执行完整挥手动作"""
    print("="*60)
    print("挥手动作 - 独立执行版")
    print("="*60)
    
    # 创建控制器
    controller = WaveHandController(ip="192.168.3.100", timeout=10)
    
    # 连接
    if not controller.connect():
        print("\n[错误] 无法连接机械臂，请检查:")
        print("  1. 机械臂电源是否开启")
        print("  2. 网络连接是否正常 (192.168.3.100)")
        return 1
    
    try:
        # 执行挥手动作
        success = controller.wave_hand(times=3)
        
        if success:
            print("\n[完成] 挥手动作执行成功")
            return 0
        else:
            print("\n[完成] 挥手动作执行失败，但已安全恢复")
            return 1
            
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
        return 1
    finally:
        # 确保断开连接
        controller.disconnect()


if __name__ == "__main__":
    sys.exit(main())
